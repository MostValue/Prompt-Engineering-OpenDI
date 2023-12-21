"""
OpenDI HyperCycle Hackathon 2023
Challenge 3: Genetic Algorithm for Automated Prompt Engineering
Made by: Quantum Syntax
"""
import os


#-e git+https://github.com/hypercycle-development/pyhypercycle-aim.git#egg=pyhypercycle_aim

from pyhypercycle_aim import SimpleServer, JSONResponseCORS, aim_uri

from genetic_algorithm import GeneticAlgorithm
from prompt_objective import PromptObjective

PORT = os.environ.get("PORT", 4002)

class MathWiz(SimpleServer):
    manifest = {"name": "MathWiz",
                "short_name": "MathWiz",
                "version": "0.1",
                "license": "Apache 2.0",
                "author": "Quantum Syntax"
                }

    def __init__(self):
        pass

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

        # Replace with our own function here
        request_json = await request.json()

        question = request_json['question']
        pa = PromptObjective(n_bits, target_output)

        # perform the genetic algorithm search
        best_genotype, score = GeneticAlgorithm.genetic_algorithm(pa.objective,
                                                                  n_bits,
                                                                  n_iter,
                                                                  n_pop,
                                                                  r_cross,
                                                                  r_mut)
        best = pa.phenotype(best_genotype)
        #REPLACE
        return JSONResponseCORS({"prompt": best, "score": score})


def main():
    # example usage:
    app = MathWiz()
    app.run(uvicorn_kwargs={"port": PORT, "host": "0.0.0.0"})


if __name__ == '__main__':
    main()
