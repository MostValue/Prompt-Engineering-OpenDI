import re

# From ipynb file. Returns score
def check_answer(answer, output):
    if not (isinstance(answer, str) and isinstance(output, str)):
        raise TypeError("Must be of type str")
    if re.search("\s" + answer +"\s*", output):
        print("answer is correct")
        return 1
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
        

if __name__ == '__main__':
    database_answer = 'Maila read 12 x 2 = <<12*2=24>>24 pages today. So she was able to read a total of 12 + 24 = <<12+24=36>>36 pages since yesterday. There are 120 - 36 = <<120-36=84>>84 pages left to be read. Since she wants to read half of the remaining pages tomorrow, then she should read 84/2 = <<84/2=42>>42 pages. #### 42'
    
    final_answer = database_answer.split()[-1]
    
    
    # database_answer = 'In a week, Jen works for 7.5 hours/day x 6 days = <<7.56=45>>45 hours/week So in a month, she works for 45 hours/week x 4 weeks =<<454=180>>180 hours. 180 hours of work is equal to 180 hours x $1.5 = $<<180*1.5=270>>270. Since she has complete attendance, she will receive a total of $270 + $10 = $<<270+10=280>>280. #### 280'
    
    # The way I got the answer was <Question> + <Instruction>
    # Where the instruction appended was 'solve this mathematical equation. leave the final answer on the last line. do not store numbers in variables'
    llm_answer_file = 'test answer.txt'
    # llm_answer_file = 'qna/a1.txt'
    
    score = 0
    
    logic = get_logic(database_answer)
    print(logic)
    
    tokenised_logic_sentences = []
    
    for l in logic:
        tokenised_logic_sentences.append(tokenise_logic(l))
    print(tokenised_logic_sentences)
    
    total_score = 1 + len(tokenised_logic_sentences)

    with open(llm_answer_file, 'r') as f:
        for line in f:
            for sentence in tokenised_logic_sentences:
                if check_logic_sentence(line, sentence):
                    tokenised_logic_sentences.pop(tokenised_logic_sentences.index(sentence))
                    score += 1
                    break
        last_line = line

    for word in last_line.split(" "):
        try:
            num_answer = str(int(word))
        except:
            pass
        
    score += check_answer(final_answer, num_answer)
    print(score)
    print(score/total_score)
    
