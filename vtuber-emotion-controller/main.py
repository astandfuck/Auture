
from emotion_analyzer import EmotionAnalyzer
from vts_controller import VTSController
from loguru import logger
from tts_controller import TTSController
from function import play_to_vtube
import asyncio

class VTuberSystem:
    """
    虚拟主播主系统
    整合情绪分析和表情控制
    """

    def __init__(self):
        self.emotion_analyzer = EmotionAnalyzer()
        self.vts_controller = VTSController()
        self.is_running = False

        # 表情持续时间（秒）
        self.emotion_duration = 4.0

        self.tts_controller = TTSController()
    async def start(self):
        """启动系统"""
        print("=" * 50)
        print("  表情控制系统 v2.0")
        print("=" * 50)

        # 连接VTube Studio
        print("\n正在连接VTube Studio...")
        if not await self.vts_controller.connect():
            print("\n[错误] 无法连接到VTube Studio")
            print("请检查:")
            print("  1. VTube Studio是否正在运行")
            print("  2. API是否已启用 (设置 → API → 开启)")
            print("  3. 端口设置 (默认 8001)")
            return False

        print("\n✓ 系统就绪！输入问题开始互动")
        print("  (输入 'quit' 退出程序)\n")

        self.is_running = True
        await self._interaction_loop()
        return True

    async def _interaction_loop(self):
        """主交互循环"""
        while self.is_running:
            try:
                # 获取用户输入（在线程中运行，不阻塞事件循环）
                user_input = (await asyncio.to_thread(input, "你: ")).strip()

                if not user_input:
                    continue

                logger.info('triggered')
                logger.info(user_input)

                if user_input.lower() in ['quit', 'exit', 'q']:
                    await self.shutdown()
                    break

                # 处理消息
                await self.process_message(user_input)

            except KeyboardInterrupt:
                print("\n\n正在退出...")
                await self.shutdown()
                break
            except Exception as e:
                print(f"[错误] {e}")

    async def process_message(self, user_input: str):
        """
        处理单条消息的完整流程

        步骤:
        1. 发送给DeepSeek获取回复和情绪
        2. 触发对应表情
        3. 显示回复内容
        """
        print("\n[思考中...]")
        # 第一步：获取DeepSeek回复和情绪标签
        # get_response_and_emotion 是同步方法，用 to_thread 包装
        result = await asyncio.to_thread(
            self.emotion_analyzer.get_response_and_emotion, user_input
        )
        emotion = result["emotion"]
        response = result["response"]

        # 第二步：显示回复
        print(f"\nauture: {response}\n")
        print("-" * 50)

        # 第三步：触发VTS表情
        print(f"[情绪检测: {emotion}]")
        emotion_task = asyncio.create_task(self.vts_controller.trigger_emotion(emotion, self.emotion_duration))

        #第三：tts的实现,与表情并行运行
        tts_task = asyncio.create_task(self.tts_controller.speak(response))


        audio_file, _ = await asyncio.gather(tts_task, emotion_task)
        await asyncio.to_thread(play_to_vtube,audio_file)#无法独立近行


    async def shutdown(self):
        """关闭系统"""
        print("\n正在关闭连接...")
        await self.vts_controller.close()
        self.is_running = False
        print("再见！")


# ========== 程序入口 ==========
if __name__ == "__main__":
    vtuber = VTuberSystem()
    asyncio.run(vtuber.start())