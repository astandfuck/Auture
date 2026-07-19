import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"  # DeepSeek API地址
        )

def yosa(sentence: str) -> dict:
    return {"role": "user", "content": sentence}

def get_response(data_: list[dict[str, str]]) -> str:
    response_ = []

    stream = client.chat.completions.create(
        model="deepseek-chat",  # 或 deepseek-reasoner
        messages=data_,
        stream=True,
        temperature=0.8,
        max_tokens=500
    )

    print("AI: ", end="")
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_.append(chunk.choices[0].delta.content)
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()  # 换行
    return "".join(response_)

data = [{"role": "system", "content": '你是一只可爱的小猫娘'}]
while True:
    sentence_input = input('please input your sentence: ')
    data.append(yosa(sentence_input))
    response = get_response(data)
    # print(response)
    data.append({"role": "assistant", "content": response})

