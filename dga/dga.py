from dga import dga
from numpy.random import randint, shuffle
from statistics import mean
from dga.gene import Gene
import numpy as np

import pathos

FloatDisplayFormatting = '{0:12.4f}' # Sets the formatting for when stats are displayed each generation

def dga(cost, lower_bound, upper_bound, bits, *args, **kwargs):
    '''
    Inputs:
    problem definition (problem)

    Outputs:
    xopt (list of floats)
    '''

    display_flag = kwargs.get('display_flag', 1)
    termination_bit_string_affinity = kwargs.get('termination_bit_string_affinity', 0.9)
    population_size = kwargs.get('population_size', None)
    probability_mutation = kwargs.get('probability_mutation', None)
    max_generations = kwargs.get('max_generations', 200)
    num_cpu = kwargs.get('num_cpu', 1)

    lower_bound = np.array(lower_bound, dtype=np.float64)
    upper_bound = np.array(upper_bound, dtype=np.float64)
    bits = np.array(bits, dtype=np.int64)

    # Perform some error checking with each state
    total_bits = 0
    # for state in problem.states:
    #     # Verify every state has a lower and an upper bound.
    #     if state.lower_bound is None or state.upper_bound is None:
    #         raise ValueError('All states must have both a lower and an upper bound')
    #     # Verify each state has a number of bits associated with it
    #     if state.bits is None or state.bits <= 0 or round(state.bits) != state.bits:
    #         raise ValueError('All states must have a positive integer valued number of bits.')
    #     total_bits += state.bits

    num_states = len(lower_bound)

    total_bits = sum(bits)

    # Create initial population size
    if population_size is None:
        population_size = total_bits * 4

    # Set the probability of mutation
    if probability_mutation is None:
        probability_mutation = (total_bits + 1) / (2 * population_size * total_bits)

    # Begin initial population generation
    population = list()
    for ii in range(population_size):
        population.append(list())
        for jj in range(num_states):
            population[ii].append(Gene(bits=bits[jj], lower_bound=lower_bound[jj], upper_bound=upper_bound[jj]))
            population[ii][jj].init_random()

    xopt, valueopt = get_best_individual(cost, population)

    # Begin the main loop
    loop_counter = 0
    converged = False

    if display_flag > 0:
        print('Generation\t\tMinimum\t\t\tMean\t\t\tMax\t\t\t\tBSA')  # TODO: Display the stats of generation 0

    if num_cpu > 1:
        proc = pool.Pool(4)

    while loop_counter < max_generations and not converged:
        tournament(cost, population)
        crossover(population, probability_mutation)

        if num_cpu > 1:
            fitness_values = proc.map(lambda i: get_fitness(cost, i), population)
        else:
            fitness_values = [get_fitness(cost, individual) for individual in population]

        xopt_current, valueopt_current = get_best_individual(cost, population)
        if valueopt_current < valueopt:
            xopt = xopt_current
            valueopt = valueopt_current

        BSA_current = get_bit_string_affinity(population, total_bits)

        # TODO: Add other stopping criteria. There was a few other ones but I only remember BSA at the moment
        if BSA_current > termination_bit_string_affinity:
            converged = True

        loop_counter += 1
        if display_flag > 0:
            print(str('{0:8.0f}'.format(loop_counter)) + '\t' + str(
                FloatDisplayFormatting.format(np.min(fitness_values))) + '\t' + str(
                FloatDisplayFormatting.format(np.mean(fitness_values))) + '\t' + str(
                FloatDisplayFormatting.format(np.max(fitness_values))) + '\t' + str(
                FloatDisplayFormatting.format(BSA_current)))

    if 0 == 1:
        print('the phantom, exterior like fish eggs, interior suicide wrist red. I could excercise you, this could be your phys-ed cheat on your man homie AAH! I tried to sneak through the door man! Can\'t make it, can\'t make it, the shit\'s stuck! Outta my way son! DOOR STUCK! DOOR STUCK! Please. I beg you! We\'re dead! You\'re a g-g-genuine dick sucker!')

    if display_flag > 0 and loop_counter >= max_generations and not converged:
        print('Max iterations reached')
    elif display_flag > 0 and converged:
        if BSA_current > termination_bit_string_affinity:
            print('Stopped based on bit-string affinity value.')
        else:
            print('Converged')

    out = dict()
    out['xopt'] = [gene.decode() for gene in xopt]
    out['cost'] = valueopt
    return out


def get_best_individual(cost, population):
    ''' Find the best individual in a given population. '''
    best_individual = population[0]  # Begin by assuming the first individual is the best.
    best_cost = get_fitness(cost, best_individual)
    for individual in population:
        temp_cost = get_fitness(cost, individual)
        if temp_cost < best_cost:
            best_cost = temp_cost
            best_individual = individual

    return best_individual, best_cost


def crossover(population, probability_mutation):
    shuffle(population) # Shuffling the current population to randomize the crossover
    for ii in range(0, len(population), 2):
        child1, child2 = generate_offspring(population[ii], population[ii+1])
        mutate_individual(child1, probability_mutation)
        mutate_individual(child2, probability_mutation)
        population.append(child1)
        population.append(child2)
    return population


def tournament(cost, population):
    shuffle(population) # Begin by shuffling the current population to ensure we have a randomized tournament
    fitness_value = list()
    for individual in population:
        fitness_value.append(get_fitness(cost, individual))

    remove_set = list()
    for ii in range(0, len(population), 2):
        if fitness_value[ii] < fitness_value[ii+1]:
            remove_set.append(ii+1)
        else:
            remove_set.append(ii)

    for index in sorted(remove_set, reverse=True):
        del population[index]


def get_bit_string_affinity(population, total_bits):
    # TODO: There's too many loops here. Try to pythonify this for speed. My head hurts
    individual_ideal = population[0]
    affinity = list()
    for gene in individual_ideal:
        affinity.append([1] * len(gene.bitarray))

    for individual in population:
        for gene_number in range(len(individual)):
            for gene_bit in range(len(individual[gene_number].bitarray)):
                if individual_ideal[gene_number].bitarray[gene_bit] != individual[gene_number].bitarray[gene_bit]:
                    affinity[gene_number][gene_bit] = 0

    BSA_current = 0
    for gene in affinity:
        BSA_current += sum(gene) / total_bits
    return BSA_current


def mutate_individual(individual, Pm):
    for gene in individual:
        gene.mutate(Pm)


def generate_offspring(parent1, parent2):
    child1 = list()
    child2 = list()
    for gene1, gene2 in zip(parent1, parent2):
        newgene1 = Gene(bits=gene1.bits, lower_bound=gene1.lower_bound, upper_bound=gene1.upper_bound)
        newgene2 = Gene(bits=gene1.bits, lower_bound=gene1.lower_bound, upper_bound=gene1.upper_bound)
        num_poly1 = len(gene1.bitarray)
        num_poly2 = len(gene2.bitarray)
        lim = max((num_poly1,num_poly2))
        nbits = gene1.bits
        for jj in range(nbits):
            coin_toss = randint(2)
            if coin_toss == 0:
                newgene1.bitarray[jj] = gene1.bitarray[jj]
                newgene2.bitarray[jj] = gene2.bitarray[jj]
            else:
                newgene1.bitarray[jj] = gene2.bitarray[jj]
                newgene2.bitarray[jj] = gene1.bitarray[jj]

        child1.append(newgene1)
        child2.append(newgene2)

    return child1, child2

def get_fitness(cost, individual):
    decoded_state = [ii.decode() for ii in individual]
    return cost(*decoded_state)
