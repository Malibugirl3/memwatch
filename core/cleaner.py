# cleaner.py
import psutil
from config.default_config import WHITELIST, GAMELIST, MEMORY_THRESHOLD

def clean_memory(mode='office'):
    """
    清理内存，根据传入模式决定清理策略：
    - office：保留 IDE、浏览器、QQ 等办公工具
    - game：在不杀游戏进程和常用进程的前提下更激进清理
    """
    mem = psutil.virtual_memory()
    if mem.percent < MEMORY_THRESHOLD:
        print(f"✅ 当前内存占用为 {mem.percent}%，无需清理")
        return

    print(f"⚠️ 当前内存占用为 {mem.percent}%，启动 {mode} 模式清理...")

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name']
            if name is None:
                continue

            name = name.lower()

            # 保留白名单进程
            if name in [n.lower() for n in WHITELIST]:
                continue

            # 游戏模式下保留游戏进程
            if mode == 'game' and name in [n.lower() for n in GAMELIST]:
                continue

            # 尝试终止进程
            proc.terminate()
            print(f"🧹 已终止：{name}")

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
