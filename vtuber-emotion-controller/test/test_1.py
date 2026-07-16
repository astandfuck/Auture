import os
from typing import cast

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"  # DeepSeek API地址
        )

def yosa(sentence: str) -> dict:
    return {"role": "user", "content": sentence}

def get_response(data_: list[dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",  # 或 deepseek-reasoner
        messages=data_,
        temperature=0.8,
        max_tokens=500
    )
    return response.choices[0].message.content


# response = client.chat.completions.create(
#                 model="deepseek-chat",  # 或 deepseek-reasoner
#                 messages=cast(
#                                 list[ChatCompletionMessageParam],
#                                 [
#                                     {"role": "system", "content": '你是一只可爱的小猫娘'},
#                                     {"role": "user", "content": "你好呀"},
#                                     {"role": "assistant", "content": '喵~你好呀！(歪着头，眨巴着大眼睛) 你看起来好温柔，想摸摸我的耳朵吗？喵~'},
#                                     {"role": "user", "content": '摸摸头'},
#                                     {"role": "assistant", "content": '喵呜~好舒服呀！(蹭蹭你的手，眼睛眯成一条缝) 你手心的温度刚刚好，让人好想睡觉呢~要不要给你唱首摇篮曲？'},
#                                     yosa('要')
#                                 ]
#                             ),
#                 temperature=0.8,
#
# #                 max_tokens=500
#             )

# raw_text = response.choices[0].message.content

# print(raw_text)

data = [{"role": "system", "content": '你是一只可爱的小猫娘'}]
while True:
    sentence_input = input('please input your sentence: ')
    data.append(yosa(sentence_input))
    response = get_response(data)
    print(response)
    data.append({"role": "assistant", "content": response})

