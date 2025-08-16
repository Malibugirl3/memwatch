# 调度器
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import threading
import time
import psutil
from typing import Optional, Callable

# 修改为绝对导入
from core.cleaner_safe import SafeMemoryCleaner
from config.config_manager import config_manager

class MemoryScheduler:

    def __init__(self):
        self.is_running = False     # 是否运行中
        self.thread: Optional[Threading.Tread]= None
        self.cleaner = SafeMemoryCleaner()
        self.check_interval = 60
        self.current_mode = None
        self.last_cleanup_time = 0
        self.status_callback: Optional[Callable] = None

    def start(self, mode='office') -> bool:
        """
        启动托管模式
        
        Argus:
            mode: enum ('office', 'game', 'auto')

        Returns:
            bool: if running
        """
        if  self.is_running:
            print("⚠️ 托管模式已经在运行中")
            return True
        
        if mode not in ['office', 'game', 'auto']:
            print(f"❌ 无效的模式: {mode}")
            return False

        self.is_running = True
        self.current_mode = mode

        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

        print(f"🚀 托管模式已启动 - {mode.upper()} 模式")
        return True

    def _monitor_loop(self):
        print(f"🔄 托管调度器启动，检查间隔: {self.check_interval // 60} 分钟")

        while self.is_running:
            try:
                memory_usage = psutil.virtual_memory().percent

                threshold = self._get_threshold(self.current_mode)

                print(f"📊 内存使用: {memory_usage:.1f}% (阈值: {threshold}%)")

                if self._should_cleanup(memory_usage, threshold):
                    self._perform_cleanup()

                self._smart_sleep()

            except Exception as e:
                print(f"❌ 托管调度器错误: {e}")
                time.sleep(10) 


    def _get_threshold(self, mode):
        if mode == 'office':
            return config_manager.get('thresholds.office', 75.0)    # 这有什么用
        elif mode == 'game':
            return config_manager.get('thresholds.game', 80.0)
        elif mode == 'auto':
            return config_manager.get('thresholds.auto', 85.0)
        else:
            return 75.0

    def _should_cleanup(self, current_usage: float, threshold: float) -> bool:
        if current_usage < threshold:
            return False
        
        if time.time() - self.last_cleanup_time < self.check_interval:
            print("⏰ 距离上次清理时间太短，跳过本次清理")
            return False
        
        return True

    def _perform_cleanup(self):
        print(f"🧹 开始清理内存 - {self.current_mode.upper()} 模式")

        cleanup_mode = self.current_mode

        if cleanup_mode == 'auto':
            current_hour = time.loacltime().tm_hour
            if 8 < current_hour <= 22:
                cleanup_mode = 'office'
            else:
                cleanup_mode = 'game'

        result = self.cleaner.gentle_cleanup(cleanup_mode)
        self.last_cleanup_time = time.time()

        freed_mb = result.get('memory_freed_mb', 0)
        print(f"✅ 清理完成，释放内存: {freed_mb:.1f} MB")

    def _smart_sleep(self):
        sleep_time = self.check_interval
        elapsed = 0

        while elapsed < sleep_time and self.is_running:
            time.sleep(min(10, sleep_time - elapsed))
            elapsed += 10

    def stop(self):
        if not self.is_running:
            print("⚠️ 托管模式未在运行")
            return False

        self.is_running = False

        if self.thread and self.thread.is_alive():
            print("⏹️ 正在停止托管模式...")
            self.thread.join(timeout=5)

        print("✅ 托管模式已停止")
        return True      


    def get_status(self) -> dict:
        return {
            'is_running': self.is_running,
            'mode': self.mode,
            'check_interval': self.check_interval,
            'last_cleanup_time': self.last_cleanup_time
        }               



scheduler = MemoryScheduler()

if __name__ == '__main__':
    print("测试托管调度器...")

    # scheduler = MemoryScheduler()
    scheduler.start('office')
    
    try:
        time.sleep(15)
        scheduler.stop()
    except KeyboardInterupt:
        print("\n 用户中断测试")
    finally:
        scheduler.stop()
        print("测试完成")
