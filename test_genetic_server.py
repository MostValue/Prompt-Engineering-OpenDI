import requests


def test_prompt_endpoint():
    url = 'http://localhost:4002'
    # Test the prompt endpoint
    target_output = 'Kylar went to the store to buy glasses for his new apartment. One glass costs $5, but every second glass costs only 60% of the price. Kylar wants to buy 16 glasses. How much does he need to pay for them?'
    response = requests.post(url + '/prompt', json={'target_output': target_output})
    response_json = response.json()
    print(response_json)

    # Use pytest's assertion style
    assert 'prompt' in response_json, "Response does not contain 'prompt'"
    assert 'score' in response_json, "Response does not contain 'score'"
    assert isinstance(response_json['prompt'], str), "'prompt' is not a string"
    assert isinstance(response_json['score'], (int, float)), "'score' is not a number"
    assert len(response_json['prompt']) > 0, "'prompt' is empty"

def main():
    #run test:
    test_prompt_endpoint()
    
if __name__=='__main__':
    main()