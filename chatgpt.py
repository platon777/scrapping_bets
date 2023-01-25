import openai
openai.api_key = "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"





def chatGpt():
    while True:
        ask = input("Question: ")
        if(ask== 't'):
            return False
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=ask,
            temperature=1,
            max_tokens=4000,
            top_p=0,
            frequency_penalty=2,
            presence_penalty=0
        )
        text = response['choices'][0]['text']
        print ('Response :'+text)





# if __name__ == "__main__":
#     main()



