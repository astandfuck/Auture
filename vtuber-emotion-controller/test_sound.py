import asyncio
import edge_tts

async def tts_edge(text, voice="zh-CN-XiaoxiaoNeural", output_file="output.mp3"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

asyncio.run(tts_edge("当然相信啦！宇宙这么大，怎么可能只有我们呢～说不定外星人正在遥远的星球上看直播呢！"))