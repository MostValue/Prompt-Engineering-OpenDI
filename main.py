# SOME PSEUDOCODE FOR OUR MAIN GENETIC ALGORITHM LOOP

# from dataset extract subset of questions

questions = dataset[:]

# generate initial population of possible prompts, n_pop
population = []
prompt = LLM("Generate a prompt to give to the LLM so that it can solve the math problem")
population.append(prompt)


# selection criteria


for prompt in population:
    




#START GENETIC ALGORITHM


# from mutation_list choose one mutation prompt

mutation_prompt  = np.random.choice(mutation_list)



mutation_prompt + 
for i in range(len(n_pop)):
    population.append(LLM())