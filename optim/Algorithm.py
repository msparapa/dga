import abc
class Algorithm(object):
    Name = 'Algorithm'
    __metaclass__ = abc.ABCMeta

    def __call__(self, problem):
        '''
        Generic method to solve a given optimization problem
        '''

    def printInfo(self):
        print(self)

    def __str__(self):
        return self.Name