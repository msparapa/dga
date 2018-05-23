from dga.algorithm import Algorithm
from numpy.random import randint, shuffle
from statistics import mean
from dga.Gene import Gene
from dga.problem import Problem

from multiprocessing_on_dill import pool



class dga(Algorithm):
    Name = 'dga'
    FloatDisplayFormatting = '{0:12.4f}' # Sets the formatting for when stats are displayed each generation

    def __new__(cls, *args, **kwargs):
        obj = super(dga, cls).__new__(cls)

        obj.display_flag = kwargs.get('display_flag', 1)
        obj.termination_bit_string_affinity = kwargs.get('termination_bit_string_affinity', 0.9)
        obj.population_size = kwargs.get('population_size', None)
        obj.probability_crossover = kwargs.get('probability_crossover', None)
        obj.probability_mutation = kwargs.get('probability_mutation', None)
        obj.max_generations = kwargs.get('max_generations', 200)
        obj.num_cpu = kwargs.get('num_cpu', 1)

        if len(args) == 0:
            return obj
        elif type(args[0]) is not Problem:
            return obj
        else:
            xopt = cls.__call__(obj, problem=args[0])
            return xopt


    def __call__(self, problem, *args):
        '''
            Inputs:
            problem definition (problem)

            Outputs:
            xopt (list of floats)
        '''

        # Perform some error checking with each state
        total_bits = 0
        for state in problem.state:
            # Verify every state has a lower and an upper bound.
            if state.lower_bound is None or state.upper_bound is None:
                raise ValueError(self.__str__() + ': All states must have both a lower and an upper bound')
            # Verify each state has a number of bits associated with it
            if state.bits is None or state.bits <= 0 or round(state.bits) != state.bits:
                raise ValueError(self.__str__() + ': All states must have a positive integer valued number of bits.')
            total_bits += state.bits

        num_states = len(problem.state)

        # Create initial population size
        if self.population_size is None:
            self.population_size = total_bits * 4

        # Set the probability of mutation
        if self.probability_mutation is None:
            self.probability_mutation = (total_bits + 1) / (2 * self.population_size * total_bits)

        # Begin initial population generation
        population = list()
        for ii in range(self.population_size):
            population.append(list())
            for jj in range(num_states):
                population[ii].append(Gene(bits=problem.state[jj].bits, lower_bound=problem.state[jj].lower_bound, upper_bound=problem.state[jj].upper_bound))
                population[ii][jj].init_random()

        xopt, valueopt = self.get_best_individual(problem.cost[0],population)

        # Begin the main loop
        loop_counter = 0
        converged = False

        if self.display_flag > 0:
            print('Generation\t\tMinimum\t\t\tMean\t\t\tMax\t\t\t\tBSA') # TODO: Display the stats of generation 0

        if self.num_cpu > 1:
            proc = pool.Pool(4)

        while loop_counter < self.max_generations and not converged:
            self.tournament(problem.cost[0], population)
            self.crossover(population)

            if self.num_cpu > 1:
                fitness_values = proc.map(lambda i: self.get_fitness(problem.cost[0],i), population)
            else:
                fitness_values = [self.get_fitness(problem.cost[0], individual) for individual in population]

            xopt_current, valueopt_current = self.get_best_individual(problem.cost[0], population)
            if valueopt_current < valueopt:
                xopt = xopt_current
                valueopt = valueopt_current

            BSA_current = self.get_bit_string_affinity(population, total_bits)

            # TODO: Add other stopping criteria. There was a few other ones but I only remember BSA at the moment
            if BSA_current > self.termination_bit_string_affinity:
                converged = True

            loop_counter += 1
            if self.display_flag > 0:
                print(str('{0:8.0f}'.format(loop_counter)) + '\t' + str(self.FloatDisplayFormatting.format(min(fitness_values))) + '\t' + str(self.FloatDisplayFormatting.format(mean(fitness_values))) + '\t' + str(self.FloatDisplayFormatting.format(max(fitness_values))) + '\t' + str(self.FloatDisplayFormatting.format(BSA_current)))

        if 0 == 1:
            print('the phantom, exterior like fish eggs, interior suicide wrist red. I could excercise you, this could be your phys-ed cheat on your man homie AAH! I tried to sneak through the door man! Can\'t make it, can\'t make it, the shit\'s stuck! Outta my way son! DOOR STUCK! DOOR STUCK! Please. I beg you! We\'re dead! You\'re a g-g-genuine dick sucker!')

        if self.display_flag > 0 and loop_counter >= self.max_generations and not converged:
            print(self.__str__() + ': Max iterations reached')
        elif self.display_flag > 0 and converged:
            if BSA_current > self.termination_bit_string_affinity:
                print(self.__str__() + ': Stopped based on bit-string affinity value.')
            else:
                print(self.__str__() + ': Converged')


        out = dict()
        out['xopt'] = [gene.decode() for gene in xopt]
        out['cost'] = valueopt
        return out


    def get_best_individual(self, cost, population):
        ''' Find the best individual in a given population. '''
        best_individual = population[0] # Begin by assuming the first individual is the best.
        best_cost = self.get_fitness(cost, best_individual)
        for individual in population:
            temp_cost = self.get_fitness(cost, individual)
            if temp_cost < best_cost:
                best_cost = temp_cost
                best_individual = individual

        return best_individual, best_cost


    def crossover(self, population):
        shuffle(population) # Shuffling the current population to randomize the crossover
        for ii in range(0, len(population), 2):
            child1, child2 = self.generate_offspring(population[ii], population[ii+1])
            self.mutate_individual(child1, self.probability_mutation)
            self.mutate_individual(child2, self.probability_mutation)
            population.append(child1)
            population.append(child2)


    def tournament(self, cost, population):
        shuffle(population) # Begin by shuffling the current population to ensure we have a randomized tournament
        fitness_value = list()
        for individual in population:
            fitness_value.append(self.get_fitness(cost, individual))

        remove_set = list()
        for ii in range(0, len(population), 2):
            if fitness_value[ii] < fitness_value[ii+1]:
                remove_set.append(ii+1)
            else:
                remove_set.append(ii)

        for index in sorted(remove_set, reverse=True):
            del population[index]


    @staticmethod
    def get_bit_string_affinity(population, total_bits):
        # TODO: There's too many loops here. Try to pythonify this for speed. My head hurts
        individual_ideal = population[0]
        affinity = list()
        for gene in individual_ideal:
            affinity.append([1]*len(gene.bitarray))

        for individual in population:
            for gene_number in range(len(individual)):
                for gene_bit in range(len(individual[gene_number].bitarray)):
                    if individual_ideal[gene_number].bitarray[gene_bit] != individual[gene_number].bitarray[gene_bit]:
                        affinity[gene_number][gene_bit] = 0

        BSA_current = 0
        for gene in affinity:
            BSA_current += sum(gene)/total_bits
        return BSA_current



    @staticmethod
    def mutate_individual(individual, Pm):
        for gene in individual:
            gene.mutate(Pm)


    @staticmethod
    def generate_offspring(parent1, parent2):
        child1 = list()
        child2 = list()
        for gene1, gene2 in zip(parent1, parent2):
            newgene1 = Gene(bits=gene1.bits, lower_bound=gene1.lower_bound, upper_bound=gene1.upper_bound)
            newgene2 = Gene(bits=gene1.bits, lower_bound=gene1.lower_bound, upper_bound=gene1.upper_bound)
            for ii in range(len(gene1.bitarray)):
                coin_toss = randint(2)
                if coin_toss == 0:
                    newgene1.bitarray[ii] = gene1.bitarray[ii]
                    newgene2.bitarray[ii] = gene2.bitarray[ii]
                else:
                    newgene1.bitarray[ii] = gene2.bitarray[ii]
                    newgene2.bitarray[ii] = gene1.bitarray[ii]
            child1.append(newgene1)
            child2.append(newgene2)

        return child1, child2


    @staticmethod
    def get_fitness(cost, individual):
        decoded_state = [ii.decode() for ii in individual]
        return cost.func(*decoded_state)


    @staticmethod
    def _get_default_options():
        return [1,0.9,None,None,None,None,None,None,None,None,None,None,None,200]