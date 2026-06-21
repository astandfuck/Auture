import pygame
import time
import sys11

def play_to_vtube(audio_file_path: str, device_name: str = "CABLE Input (VB-Audio Virtual Cable)"):
    # 1. 初始化混音器时直接指定设备
    # 这一步是关键，提前告诉Pygame要用哪个声卡
    pygame.mixer.init(devicename=device_name)
    print(f"音频输出已锁定至设备: {device_name}")

    # 2. 加载并播放音频
    try:
        pygame.mixer.music.load(audio_file_path)
        print(f"正在播放: {audio_file_path}")
        pygame.mixer.music.play()

        # 3. 等待播放完成
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        print("播放完成。")

    except Exception as e:
        print(f"播放音频时出错: {e}")
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    # 示例：替换为你自己的.mps文件路径
    play_to_vtube(r"/output.mp3")