from genetic_algorithm import GeneticAlgorithm


#Just some mock LLM and fitness function to make sure gentic algorithm works

def run_LLM(prompt):
    words = ['cat', 'dog', 'mouse', 'rabbit']
    try:
        result = words[sum(prompt) // 10]
    except:
        result = "rabbit"
    return result

def fitness_funtion(output):
    answer = "dog"
    return int(output == answer) 

#  running fitness for one individual

def fitness(individual):
    output = run_LLM(individual)
    return fitness_funtion(output)

# def alternator(x):
#     x = [y - 0.5 for y in x]
#     return abs(sum(x))

# define the total iterations
n_iter = 100
# length
length = 10
# define the population size
n_pop = 100
# crossover rate
r_cross = 0.9
# mutation rate
r_mut = 1.0 / float(length)

# perform the genetic algorithm search
best, score = GeneticAlgorithm.genetic_algorithm(fitness,
                                                 length,
                                                 n_iter,
                                                 n_pop,
                                                 r_cross,
                                                 r_mut)

print('Done!')
print(f'Best individual: {best}, Best score: {score:.2f}')




#  Chromosome and gene formation
# from typing import List
# Genome = List[int]
# Population = List[Genome]

# def generate_genome(length: int) -> Genome:
#     '''Generates a genome of random numbers of size length'''
#     return np.randint(9, length)

# def generate_population(size: int, genome_length: int) -> Population:
#     '''Generates population of genomes'''
#     return [generate_genome(genome_length) for i in range(size)]




