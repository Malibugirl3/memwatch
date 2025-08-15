# 调度器
import threading
from threading import Timer, Lock
import time
import psutil
from config.config_manager import config_manager
from core.cleaner_safe import clean_memory

class Scheduler:

    def __init__(self):
        self.is_running = False     # 是否运行中
        self.is_paused = False      # 是否暂停
        self.Timer = None
        self.lock = Lock()
        self.next_run_at = None
        self.mode = 'office'
        self.last_clean_esult = None
        self.on_update = None

    def _get_interval_minutes():
        """
        从 config_manager 读取键 scheduler.interval_minutes，不存在就用默认 5。
        返回：float 或 int，表示分钟。
        """
        interval = config_manager.get('shceduler.interval_minutes')