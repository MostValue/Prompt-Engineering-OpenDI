import re


def check_answer(answer, output):
    if not (isinstance(answer, str) and isinstance(output, str)):
        raise TypeError("Must be of type str")
    if re.search("\s" + answer +"\s*", output):
        print("answer is correct")
        return 10
    print("answer is wrong")
    return 0

def get_logic(answer):
    return re.findall("<<(.*?)>>", answer)

def tokenise_logic(logic):
    tokenised_logic = []
    operators = "+-/*="
    current_token = ""
    
    for c in logic:
        if c in operators:
            tokenised_logic.append(current_token)
            tokenised_logic.append(c)
            current_token = ""
        elif c == '.' or c.isnumeric():
            current_token += c
    tokenised_logic.append(current_token)
    
    return tokenised_logic

def check_logic_sentence(line, logic_tokens):
    i = 0

    for token in logic_tokens:
        if token in line:
            i += 1

    if len(logic_tokens) == i:
        return True
    return False