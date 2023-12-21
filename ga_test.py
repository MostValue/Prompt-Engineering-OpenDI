# Libraries
import pandas as pd
import random
import json
from datasets import load_dataset
import re
import math
import random
import spacy

from huggingface_hub import hf_hub_download

from ga import llamathwiz

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

if __name__ == '__main__':
    dataset = load_dataset("gsm8k", "main")
    dataset["test"][5]
    
    model_name = "TheBloke/Llama-2-7B-Chat-GGUF"
    model_basename = "./llama-2-7b-chat.Q5_K_M.gguf"
    
    model_path = hf_hub_download(repo_id=model_name, filename=model_basename)
    
    ai = llamathwiz(model_path)
    
    print(ai.process_with_llm("what is 2+2?"))
    
    
    # model_path = hf_hub_download(repo_id=model_name, filename=model_basename)