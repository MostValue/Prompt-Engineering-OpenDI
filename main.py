# SOME PSEUDOCODE FOR OUR MAIN GENETIC ALGORITHM LOOP



# generate initial population of possible prompts, n_pop
population = []

while i < n_pop:
    instructions = LLM_generate("List of 100 Diverse ideas helpful in solving tasks like this one")
    population.append(instructions)

# from mutation_list choose one mutation prompt

mutation_prompt  = np.random.choice(mutation_list)


for instruction in population:
    instruction_mutant = LLM1(mutation_prompt + instruction)

    
#evaluate fitness of instruction

# from dataset extract subset of questions
questions = dataset[5:]

score = 0 
def scoring(instruction, questions) -> score:
    for question in questions:
        fitness(LLM2(instruction+ question))
    return score

#Extract the answer from the LLM output


result = [scoring(instruction, questions) for instruction in instructions]
    
#SELECT BEST INSTRUCTIONS

#select the best 10 (can change anytime) instructions
best_instructions = result.sort()[-10:]
new_pop = []
new_pop.append(best_instructions)

#MUTATION
def mutate(instruction):
    #blah
    # Should have function call to LLM( )  -> new instruction
def crossover(p1, p2):
    #blah

for instruction in best_instructions:
    new_pop.append(mutate(instruction))

for i in range(num_crossover):
    p1 = random.choice(result.sort()[:-10])
    p2 = random.choice(result.sort()[:-10])
    new_pop.append(crossover(p1,p2))


# Pass new_pop into LLM2
# Restart genetic algo


new_instruction = instruction1.split() + instruction2.split()




