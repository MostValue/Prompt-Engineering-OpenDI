import re

# From ipynb file. Returns score
def check_answer(answer, output):
    if not (isinstance(answer, str) and isinstance(output, str)):
        raise TypeError("Must be of type str")
    if re.search("\s" + answer +"\s*", output):
        print("answer is correct")
        return 3
    print("answer is wrong")
    return -1


# finds the logical steps from database answer
def get_logic(answer):
    return re.findall("<<(.*?)>>", answer)


# splits database answer into tokens
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


# checks to see if the database answer is in the line
def check_logic_sentence(line, logic_tokens):
    i = 0

    for word in line.split(" "):
        # print(f'{word} compared to {logic_tokens[i]} at i = {i}')
        if word == logic_tokens[i]:
            i += 1
        else:
            if i > 0:
                i = 0
        if i == len(logic_tokens)-1:
            return True
        
    return False
            

if __name__ == '__main__':
    database_answer = 'Natalia sold 48/2 = <<48/2=24>>24 clips in May. Natalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May. #### 72'
    
    # The way I got the answer was <Question> + <Instruction>
    # Where the instruction appended was 'solve this mathematical equation. leave the final answer on the last line. do not store numbers in variables'
    llm_answer_file = 'test answer.txt'
    
    score = 0
    
    logic = get_logic(database_answer)
    print(logic)
    
    tokenised_logic_sentences = []
    
    for l in logic:
        tokenised_logic_sentences.append(tokenise_logic(l))

    with open(llm_answer_file, 'r') as f:
        for line in f:
            for sentence in tokenised_logic_sentences:
                if check_logic_sentence(line, sentence):
                    score += 1
                    break
        last_line = line

    for word in last_line.split(" "):
        try:
            num_answer = str(int(word))
        except:
            pass
        
    score += check_answer(num_answer, last_line)
    print(score)
    
