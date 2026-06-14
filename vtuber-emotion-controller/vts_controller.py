import asyncio
import pyvts
import loguru

class VTSController:
    def __init__(self):
        self.plugin_info = {
            "plugin_name": "DeepSeekEmotionController",
            "developer": "YourName",
            "authentication_token_path": "./token.txt"
        }
        self.vts = pyvts.vts(plugin_info=self.plugin_info)

        # 热键名称必须和VTube Studio中设定的完全一致
        self.emotion_hotkey_map = {
            "happy": "开心",
            "excited": "兴奋",
            "sad": "悲伤",
            "neutral": "默认",
            "confused": "疑惑",
            "surprised": "惊讶",
            "shy": "羞涩",
            "smug": "沾沾自喜",
        }
            # "disgusted",
            # "fearful": "害怕",
            # "confused",
            #"angry": "生气",
        self.current_emotion = "neutral"
        self.is_connected = False

    async def connect(self):
        try:
            await self.vts.connect()
            await self.vts.request_authenticate_token()
            await self.vts.request_authenticate()
            self.is_connected = True
            print("[VTS] ✓ 连接成功")
            return True
        except Exception as e:
            print(f"[VTS] 连接失败: {e}")
            return False

    async def trigger_emotion(self, emotion: str, duration: float = 3.0):
        if not self.is_connected:
            return
        hotkey_name = self.emotion_hotkey_map.get(emotion, "默认")
        try:
            await self.vts.request(
                self.vts.vts_request.requestTriggerHotKey(hotkey_name)
            )
            print(f"[VTS] 表情: {hotkey_name}")
            if duration > 0 and emotion != "neutral":
                await asyncio.sleep(duration)
                await self.vts.request(
                    self.vts.vts_request.requestTriggerHotKey("默认")
                )
        except Exception as e:
            print(f"[VTS] 触发失败: {e}")

    async def close(self):
        if self.is_connected:
            await self.vts.close()
            self.is_connected = False

