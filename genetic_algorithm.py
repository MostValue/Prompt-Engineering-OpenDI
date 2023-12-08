# genetic algorithm as shown in their hackathon tutorial example

from numpy.random import rand
from numpy.random import randint

# Class genetic algorithm
class GeneticAlgorithm():

    @classmethod
    def genetic_algorithm(cls, fitness, length, n_iter, n_pop, r_cross, r_mut):
        """
        Execute a genetic algorithm to optimize a given objective function.

        Parameters:
        - fitness (function): The fitness function to be optimized.
        - length (int): The length of bits in the bitstring representing an individual.
        - n_iter (int): The number of generations to run the genetic algorithm.
        - n_pop (int): The size of the population in each generation.
        - r_cross (float): The probability of crossover (recombination) between individuals.
        - r_mut (float): The probability of mutation in an individual's bitstring.

        Returns:
        - list: A list containing the best individual found and its corresponding objective value.
        """
        # GENERATES A POPULATION
        population = [randint(0,  2, length).tolist() for _ in range(n_pop)]

        # KEEPING TRACK OF BEST SOLUTION
        best, best_eval = population[0], fitness(population[0])

        # ENUMERATE OVER GENERATIONS
        for gen in range(n_iter):
        
            # evaluate the fitness of all candidates in the population
            scores = [fitness(c) for c in population]
            print("Generation {} - Best Score: {:.3f}".format(gen, max(scores)))

            # check for new best solution
            for i in range(n_pop):
                if scores[i] > best_eval:
                    best, best_eval = population[i], scores[i]
                    print(f">{0}, new best f({1}) = {2:.3f}".format(gen, population[i], scores[i]))

            # SELECT PARENTS
            selected = [cls._selection(population, scores) for _ in range(n_pop)]

            # CREATE NEXT GENERATION
            children = list()
            for i in range(0, n_pop, 2):
                # randomly select 2 parents from the population
                p1, p2 = selected[i], selected[i + 1]

                # perform crossover and mutation
                for c in cls._crossover(p1, p2, r_cross):
                    # mutation
                    cls._mutation(c, r_mut)
                    # store for next generation
                    children.append(c)

            # replace population
            population = children
        return [best, best_eval]

    @classmethod
    def _selection(cls, population, scores, k=3):
        """
        Perform selection of individuals based on their fitness scores using tournament selection.

        Parameters:
        - population (list): The population of individuals.
        - scores (list): The fitness scores corresponding to each individual.
        - k (int): The tournament size for selection. Default is 3.

        Returns:
        - list: The best selected individual based on the tournament selection.
        """

        # first random selection
        x1 = randint(len(population))
        for x in randint(0, len(population), k - 1):
            # check if better than 3 random individuals (performing a tournament)
            if scores[x] > scores[x1]:
                x1 = x
        return population[x1]

    @classmethod
    def _crossover(cls, p1, p2, r_cross):
        """
        Perform crossover (recombination) between two parent individuals.

        Parameters:
        - p1 (list): The first parent individual.
        - p2 (list): The second parent individual.
        - r_cross (float): The probability of crossover. If random value is less than r_cross, crossover occurs.

        Returns:
        - list: A list containing two child individuals resulting from crossover.
        """

        # children are copies of parents by default
        c1, c2 = p1.copy(), p2.copy()
        # check for recombination
        if rand() < r_cross:
            # select crossover point that is not on the end of the string
            pt = randint(1, len(p1) - 2)
            # perform crossover
            c1 = p1[:pt] + p2[pt:]
            c2 = p2[:pt] + p1[pt:]
        return [c1, c2]

    @classmethod
    def _mutation(cls, bitstring, r_mut):
        """
        Introduce mutations in an individual's bitstring.

        Parameters:
        - bitstring (list): The bitstring of an individual.
        - r_mut (float): The probability of mutation for each bit. If random value is less than r_mut, a bit is flipped.

        Returns:
        - None: The bitstring is modified in place.
        """
        for i in range(len(bitstring)):
            # check for a mutation
            if rand() < r_mut:
                # flip the bit
                bitstring[i] = 1 - bitstring[i]