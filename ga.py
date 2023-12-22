# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from llama_cpp import Llama
from fitness_function import *

# Libraries
import pandas as pd
import random
import json
from datasets import load_dataset
import re
import math
import random
import spacy

def get_random_test_object(dataset):
    if "test" in dataset and len(dataset["test"]) > 0:
        random_index = random.randint(0, len(dataset["test"]) - 1)
        test_object = dataset["test"][random_index]
        
        # Assuming each object in the dataset has 'question' and 'answer' keys
        question = test_object.get("question", "No question found")
        answer = test_object.get("answer", "No answer found")
        
        return question, answer
    else:
        return None, None
    
def get_random_mutation(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path, header=None, encoding='utf-8', delimiter='.') 
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file_path, header=None, encoding='ISO-8859-1', delimiter='.') 

    random_prompt = random.choice(df[1].tolist())
    return random_prompt

def get_random_mutation_txt(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remove any leading/trailing whitespace and filter out empty lines
    prompts = [line.strip() for line in lines if line.strip()]
    
    if prompts:
        return random.choice(prompts)
    else:
        return "No mutation prompts found."

class llamathwiz:
    def __init__(self, model_path):
        # self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        # self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        self.dataset = load_dataset("gsm8k", "main")
        self.dataset["test"][5]
        self.gen = 0
        self.llm = Llama(
            model_path=model_path,
            n_threads=2,
            n_batch=512,
            n_gpu_layers=32
            )
        
    def run_ga(self, prompt, iterations=5):
        self.scores_avg = []
        self.gens = []
        self.best_instr_per_gen = []

        self.iteration_first()
        if iterations > 1:
            for i in range(iterations-1):
                self.scores_avg.append(self.average(self.scores))
                self.gens.append(self.gen)
                self.iteration_prepare()
                self.best_instr_per_gen.append(self.best_instructions[0])
                self.iteration_execute()
        
        self.gens.append(self.gen)
        self.scores_avg.append(self.average(self.scores))
        best_score, best_score_index = self.find_best_score(self.scores)
        best_instr = self.generated_prompts[best_score_index]
        self.best_instr_per_gen.append(best_instr)
        
        return f'Q:{prompt} I:{best_instr}', best_score 
    
    def average(self, lst): 
        return sum(lst) / len(lst)
        
    def generate_instructions(self, question, task_description, max_tokens=100):
        formatted_input = f"{task_description} {question}"
        output = self.llm(formatted_input)

        return output["choices"][0]["text"]
    
    def generate_instructions1(self, num_instructions, max_tokens=1000):
        instructions = []
        for num in range(num_instructions):
            formatted_input = "Generate an instruction on how to solve a simple math problem without the need of a question"
            generated_text = self.llm(formatted_input)["choices"][0]["text"]
            instructions.append(generated_text)

        return instructions

    def process_with_llm(self, prompt):
        return self.llm(prompt)["choices"][0]["text"]
    
    def apply_mutation(self, instruction, mutation_prompt):
        # Example mutation - this can be customized based on your mutation logic
        return self.llm(f"{instruction} \n Rewrite this and apply the following mutation. Mutation: {mutation_prompt}")["choices"][0]["text"]
    
    def fitness(self, database_answer, output):
        final_answer = database_answer.split()[-1]

        score = 0

        logic = get_logic(database_answer)

        tokenised_logic_sentences = []

        for l in logic:
            tokenised_logic_sentences.append(tokenise_logic(l))

        total_score = 10 + len(tokenised_logic_sentences)*10

        for line in output.split("."):
            for sentence in tokenised_logic_sentences:
                if check_logic_sentence(line, sentence):
                    tokenised_logic_sentences.pop(tokenised_logic_sentences.index(sentence))
                    score += 10
                    break
        last_line = line

        num_answer = 'a'

        for word in output.split(" "):
            try:
                num_answer = str(int(word))
            except:
                pass
            
        score += check_answer(final_answer.strip(), num_answer.strip())
        return score/total_score
    
    def iteration_first(self, num_instructions=10):
        self.gen = 1
        self.generated_prompts = []
        self.generated_answers = []
        self.iteration_questions = []
        self.scores = []
        self.best_instructions = []
        
        mutation_prompt = get_random_mutation_txt("./Prompt-Engineering-OpenDI/mutation_prompts.txt")
        for _ in range(num_instructions):
            question, database_answer = get_random_test_object(self.dataset)  # Fetch a random question from your dataset
            self.iteration_questions.append((question, database_answer))
            instruction = self.generate_instructions1(1)
            # mutated_instruction = self.apply_mutation(instruction, mutation_prompt)
            # self.generated_prompts.append(mutated_instruction)
            self.generated_prompts.append(instruction)
            processed_output = self.process_with_llm(f'Q:{question} I:{instruction} A:') 
            self.generated_answers.append(processed_output)
            self.scores.append(self.fitness(database_answer, processed_output))
            
    
    def iteration_execute(self):
        self.gen += 1
        self.generated_prompts = []
        self.generated_answers = []
        self.iteration_questions = []
        self.scores = []

        mutation_prompt = get_random_mutation_txt("./Prompt-Engineering-OpenDI/mutation_prompts.txt")
        for instruction in self.best_instructions:
            question, database_answer = get_random_test_object(self.dataset)  # Fetch a random question from your dataset
            self.iteration_questions.append((question, database_answer))
            mutated_instruction = self.apply_mutation(instruction, mutation_prompt)
            self.generated_prompts.append(mutated_instruction)
            processed_output = self.process_with_llm(f'Q:{question} I:{mutated_instruction} A:')
            self.generated_answers.append(processed_output)
            self.scores.append(self.fitness(database_answer, processed_output))
    
    def iteration_prepare(self):
        self.best_instructions = []
        self.find_best_scores(self.scores)
        self.best_instructions.append(self.replace_pos(self.best_instructions[0], self.best_instructions[1], ['ADV', 'ADJ', 'NOUN']))
        self.best_instructions.append(self.replace_pos(self.best_instructions[1], self.best_instructions[0], ['ADV', 'ADJ', 'NOUN']))
        for instr in self.generate_instructions1(4):
            self.best_instructions.append(instr)
        for i in range(2):
            mutation_prompt = get_random_mutation_txt("./Prompt-Engineering-OpenDI/mutation_prompts.txt")
            self.best_instructions.append(self.apply_mutation(self.best_instructions[i], mutation_prompt))
        
    def find_best_scores(self, scores):
        for i in range(2):
            maximum_val = 0
            maximum_index = 0
            while i < len(scores):
                if scores[i] > maximum_val:
                    maximum_val = scores[i]
                    maximum_index = i
                i += 1
            scores.pop(maximum_index)
            self.best_instructions.append(self.generated_prompts.pop(maximum_index))
            
    def find_best_score(self, scores):
        i=0
        maximum_val = 0
        maximum_index = 0
        while i < len(scores):
            if scores[i] > maximum_val:
                maximum_val = scores[i]
                maximum_index = i
            i += 1
        return maximum_val, maximum_index
            
    def replace_pos(self, string1, string2, POS):

        """
        Replace tokens of specific parts of speech (POS) in string1 with corresponding
        tokens of the same POS from string2.

        Parameters:
        - string1 (str): The input string where certain POS will be replaced.
        - string2 (str): The reference string from which POS replacements will be taken.
        - POS (list): A list of POS tags to identify which tokens to replace in string1.

        Returns:
        - str: The modified string with replacements of tokens based on specified POS tags.

        Possible POS:
        "ADJ": "adjective",
        "ADP": "adposition",
        "ADV": "adverb",
        "AUX": "auxiliary",
        "CONJ": "conjunction",
        "CCONJ": "coordinating conjunction",
        "DET": "determiner",
        "INTJ": "interjection",
        "NOUN": "noun",
        "NUM": "numeral",
        "PART": "particle",
        "PRON": "pronoun",
        "PROPN": "proper noun",
        "PUNCT": "punctuation",
        "SCONJ": "subordinating conjunction",
        "SYM": "symbol",
        "VERB": "verb".
        """
        nlp = spacy.load("en_core_web_sm")
        doc1 = nlp(string1)
        doc2 = nlp(string2)

        new_tokens = []

        for token1 in doc1:
            if token1.pos_ in POS:
                #generating a list of all matching tokens
                matching_tokens = [token2.text for token2 in doc2 if token2.pos_ == token1.pos_]
                #use a random token if possible, or else use the same
                if matching_tokens:
                    new_token = random.choice(matching_tokens)
                else:
                    new_token = token1.text
            else:
                new_token = token1.text
            new_tokens.append(new_token)

        # Join the modified tokens to form the final string
        result = ' '.join(new_tokens)
        return result
    
    
