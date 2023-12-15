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

def get_logic(answer):
    return re.findall("<<(.*?)>>", answer)

if __name__ == '__main__':
    database_answer = 'Natalia sold 48/2 = <<48/2=24>>24 clips in May. Natalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May. #### 72'
    
    # The way I got the answer was <Question> + <Instruction>
    # Where the instruction appended was 'solve this mathematical equation. leave the final answer on the last line. do not store numbers in variables'
    llm_answer_file = 'test answer.txt'
    
    score = 0
    
    logic = get_logic(database_answer)
    print(logic)

    with open(llm_answer_file, 'r') as f:
        for line in f:
            pass
        last_line = line

    print(last_line)
    for word in last_line.split(" "):
        try:
            num_answer = str(int(word))
        except:
            pass
        
    score += check_answer(num_answer, last_line)
    
    