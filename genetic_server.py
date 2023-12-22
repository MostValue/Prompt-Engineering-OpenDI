"""
OpenDI HyperCycle Hackathon 2023
Challenge 3: Genetic Algorithm for Automated Prompt Engineering
Made by: Quantum Syntax
"""
import os
from huggingface_hub import hf_hub_download

#-e git+https://github.com/hypercycle-development/pyhypercycle-aim.git#egg=pyhypercycle_aim

from pyhypercycle_aim import SimpleServer, JSONResponseCORS, aim_uri

from ga import llamathwiz

PORT = os.environ.get("PORT", 4002)


model_name = "TheBloke/Llama-2-7B-Chat-GGUF"
model_basename = "./1lama-2-7b-chat.05_K_M…gguf"
model_path = hf_hub_download(repo_id=model_name, filename=model_basename)

class MathWiz(SimpleServer):
    manifest = {"name": "MathWiz",
                "short_name": "MathWiz",
                "version": "0.1",
                "license": "Apache 2.0",
                "author": "Quantum Syntax"
                }

    def __init__(self):
        self.llama_wizard = llamathwiz(model_path=model_path)

    @aim_uri(uri="/prompt", methods=["POST"],
             endpoint_manifest={
                 "input_query": "",
                 "input_headers": "",
                 "output": {},
                 "documentation": "Returns the best prompt based on the desired output", 
                 "example_calls": [{
                     "body": {"question": "Jimmy has 3 apples. If susan gives him 2 apples, how many apples does he have now?"},
                     "method": "POST",
                     "query": "",
                     "headers": "",
                     "output": {"prompt": "Solve the problem, thinking logically step by step"}
                 }]
             })
    async def prompt(self, request):
        request_json = await request.json()
        target_output = request_json['target_output']

        best_prompt, best_score = self.llama_wizard.run_ga(target_output, 3)

        # Format the response
        return JSONResponseCORS({"prompt": best_prompt, "score": best_score})



def main():
    # example usage:
    app = MathWiz()
    app.run(uvicorn_kwargs={"port": PORT, "host": "0.0.0.0"})


if __name__ == '__main__':
    main()
