import psutil
import threading
import time
from collections import deque

class SystemMonitor:
    def __init__(self, max_data_points=60):
        """
        初始化系统监视器
        max_data_points: 保存的最大数据点数量（默认60秒）
        """
        self.max_data_points = max_data_points

        self.memory_data = deque(maxlen=max_data_points)
        self.cpu_data = deque(maxlen=max_data_points)
        self.timestamps = deque(maxlen=max_data_points)

        self.is_running = False
        self.monitor_thread = None

        self.update_callbacks = []

        print("📊 系统监控器初始化完成")

    def get_current_stats(self):
        """
        获取当前系统状态
        返回包含内存、CPU等信息的字典
        """         
        try:
            memory = psutil.virtual_memory()

            cpu_percent = psutil.cpu_percent(interval=None)

            process_count = len(psutil.pids())

            stats = {
                'memory_percent': round(memory.percent, 1),
                'memory_used_gb': round(memory.used / 1024**3, 2),
                'memory_total_gb': round(memory.total / 1024**3, 2),
                'memory_available_gb': round(memory.available / 1024**3, 2),
                'cpu_percent': round(cpu_percent, 1),
                'process_count': process_count,
                'timestamp': time.time()
            }

            return stats

        except Exception as e:
            print(f"❌ 获取系统状态失败: {e}")
            return None

    def add_update_callback(self, callback_func):
        """
        添加更新回调函数
        当有新数据时会调用这些函数
        """
        if callback_func not in self.update_callbacks:
            self.update_callbacks.append(callback_func)
            print(f"✅ 已注册更新回调函数")  

    def remove_updata_callback(self, callback_func):
        """移除回调函数"""
        if callback_func in self.update_callbacks:
            self.update_callbacks.remove(callback_func)

    def start_monitoring(self):
        """
        启动后台监控线程
        """
        if self.is_running:
            print("⚠️ 监控线程已运行")
            return

        print("🚀 启动系统实时监控...")
        self.is_running = True

        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True,
            name="SystemMonitor"
        )
        self.monitor_thread.start()

    def stop_monitoring(self):
        """
        停止监控线程
        """
        if not self.is_running:
            return

        print("🛑 停止系统监控...")
        self.is_running = False        

        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)

    def _monitor_loop(self):
        """
        监控主循环（运行在后台线程中）
        这个方法前面有下划线，表示是内部方法
        """
        print("📊 监控线程已启动，开始收集数据...")

        while self.is_running:
            try:
                stats = self.get_current_stats()

                if stats:
                    self.memory_data.append(stats['memory_percent'])
                    self.cpu_data.append(stats['cpu_percent'])
                    self.timestamps.append(stats['timestamp'])

                    self._notify_callbacks(stats)

                time.sleep(1)

            except Exception as e:
                print(f"❌ 监控循环出错: {e}")
                time.sleep(1)

        print("📊 监控线程已停止")

    def _notify_callbacks(self, stats):
        """
        安全地通知所有回调函数
        """
        for callback in self.update_callbacks.copy():   # 复制列表避免并发修改
            try:
                callback(stats)
            except Exception as e:
                print(f"⚠️ 回调函数执行失败: {e}")

# 测试代码
if __name__ == "__main__":
    def test_callback(stats):
        print(f"📊 [{time.strftime('%H:%M:%S')}] "
              f"内存: {stats['memory_percent']}% "
              f"CPU: {stats['cpu_percent']}% "
              f"进程: {stats['process_count']}")      

    # 创建监控器
    monitor = SystemMonitor()           

    # 注册回调函数
    monitor.add_update_callback(test_callback)

    # 启动监控
    monitor.start_monitoring()

    try:
        print("🎯 监控测试运行中，按 Ctrl+C 停止...")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 用户终端，停止监控...")
        monitor.stop_monitoring()
        print("✅ 监控测试已停止")


