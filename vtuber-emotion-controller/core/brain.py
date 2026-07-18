import re
from typing import cast

from openai import OpenAI
import os
from dotenv import load_dotenv
from openai.types.chat import ChatCompletionMessageParam

load_dotenv()  #加载环境变量.env文件

class Brain:
    """
    情绪分析器
    发送文本给DeepSeek，让它同时给出回答和情绪标签
    """

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"  # DeepSeek API地址
        )

        # 定义可用的情绪标签
        self.emotion_tags = [
            "happy",
            "sad",
            "surprised",
            "neutral",
            "excited",
            "confused",
            "smug",
            "shy"
        ]

        # 系统提示词：要求DeepSeek在回答开头标注情绪
        self.system_prompt = f"""
你是一个虚拟主播，名叫auture。请根据用户的问题，用最合适的情绪来回答。
严格在回答的第一行用标签标注情绪，格式为：[EMOTION:情绪名称]
可用的情绪标签有：{', '.join(self.emotion_tags)}

规则：
1. 第一行必须是 [EMOTION:标签] ，不能有任何其他内容
2. 情绪标签必须从可用列表中选择
3. 从第二行开始才是正常回答内容

示例：
用户：你今天开心吗？
你：[EMOTION:happy]
当然开心啦！和大家聊天最快乐了～
"""

    def get_response_and_emotion(self, user_input: str) -> dict:
        """
        获取DeepSeek的“回复”和“情绪标签”

        返回:
            {
                "emotion": "happy",
                "response": "当然开心啦！...",
                "raw_text": "[EMOTION:happy]\n当然开心啦！..."
            }
        """
        try:
            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model="deepseek-chat",  # 或 deepseek-reasoner
                messages=cast(
                                list[ChatCompletionMessageParam],
                                [
                                    {"role": "system", "content": self.system_prompt},
                                    {"role": "user", "content": user_input}
                                ]
                            ),
                temperature=0.8,
                max_tokens=500
            )

            raw_text = response.choices[0].message.content

            # 解析情绪标签
            emotion, clean_response = self._parse_emotion_tag(raw_text)

            return {
                "emotion": emotion,
                "response": clean_response,
                "raw_text": raw_text
            }

        except Exception as e:
            print(f"[错误] DeepSeek API调用失败: {e}")
            return {
                "emotion": "neutral",
                "response": "抱歉，我暂时无法回答这个问题...",
                "raw_text": ""
            }

    def _parse_emotion_tag(self, text: str) -> tuple:
        """
        从文本中提取情绪标签

        参数:
            text: 包含 [EMOTION:标签] 的原始文本

        返回:
            (emotion, clean_response) 元组
        """
        # 正则匹配 [EMOTION:xxx] 格式
        pattern = r'\[EMOTION:(\w+)\]'
        match = re.search(pattern, text)

        if match:
            emotion = match.group(1).lower()
            # 移除标签行，保留纯净的回答
            clean_response = re.sub(pattern + r'\s*', '', text, count=1).strip()

            # 验证情绪标签是否在预定义列表中
            if emotion not in self.emotion_tags:
                print(f"[警告] 未知情绪标签: {emotion}，使用 neutral 代替")
                emotion = "neutral"

            return emotion, clean_response
        else:
            # 如果没有标签，默认返回neutral
            print("[警告] 未找到情绪标签，使用 neutral")
            return "neutral", text.strip()


# 测试代码
if __name__ == "__main__":
    analyzer = Brain()

    # 测试不同情绪
    test_messages = [
        "我中彩票了！",
        "我的宠物去世了...",
        "你相信有外星人吗？",
    ]

    for msg in test_messages:
        result = analyzer.get_response_and_emotion(msg)
        print(f"用户: {msg}")
        print(f"情绪: {result['emotion']}")
        print(f"回答: {result['response']}")
        print("-" * 50)

    #msg="我的宠物去世了..."
    #result = analyzer.get_response_and_emotion(msg)
    #  result[dict]:
    #  {'emotion': 'excited',
    #  'response': '当然相信啦！宇宙这么大，怎么可能只有我们呢～说不定外星人正在遥远的星球上看直播呢！',
    #  'raw_text': '[EMOTION:excited]\n当然相信啦！宇宙这么大，怎么可能只有我们呢～说不定外星人正在遥远的星球上看直播呢！'}