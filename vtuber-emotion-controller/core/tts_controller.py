
import edge_tts
import tempfile

class TTSController:
    def __init__(self, voice="zh-CN-XiaoxiaoNeural"):
        self.voice = voice

    async def speak(self, text: str) -> str:
        """异步生成TTS音频并返回文件路径"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            output_path = tmp_file.name
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        print(f"[TTS] 语音已生成: {output_path}")
        return output_path