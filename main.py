from core.monitor import show_system_status
from core.cleaner_safe import clean_memory

def run_memwatch():
    mode = input("请选择模式 (office/game): ").strip().lower()

    if mode not in ['office', 'game']:
        print("❌ 无效模式，请输入 office 或 game")
        return 

    print("🚀 Memwatch 启动中...")
    print(f"\n当前模式: {mode.upper()}")
    show_system_status()
    clean_memory(mode=mode)


if __name__ == '__main__':
    run_memwatch()
