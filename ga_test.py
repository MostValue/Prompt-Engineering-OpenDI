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

if __name__ == '__main__':
    
    model_name = "TheBloke/Llama-2-7B-Chat-GGUF"
    model_basename = "./llama-2-7b-chat.Q5_K_M.gguf"
    
    model_path = hf_hub_download(repo_id=model_name, filename=model_basename)
    
    ai = llamathwiz(model_path)
    
    print(ai.run_ga("What is 2+2?", 1))
    
    
    # model_path = hf_hub_download(repo_id=model_name, filename=model_basename)