import os
import pygame
import time

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

def write_env(key: str, value: str):
    env_path = "../.env"
    content = ""
    # 读取原有内容
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read()
    # 替换已有key / 新增
    lines = content.splitlines()
    new_lines = []
    found = False
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"{key}={value}")
    # 写回
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

# 使用
# write_env("TOKEN", "gggggggggggggggggggggggggggggggg")
# write_env("PASSWORD", "123456")

if __name__ == "__main__":
    pass