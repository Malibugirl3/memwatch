import json
import os
from typing import Dict, Any, Optional
from .default_config import (
    SYSTEM_CRITICAL, OFFICE_WHITELIST, GAME_WHITELIST,
    MEMORY_THRESHOLD, SAFE_CLEANUP_CONFIG
)

class ConfigManager:
    def __init__(self, config_file: str = "data/user_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "thresholds": {
                "office": MEMORY_THRESHOLD.get('office', 75.0),
                "game": MEMORY_THRESHOLD.get('game', 80.0),
                "auto": 85.0
            },
            "scheduler": {
                "interval_minutes": 5,
                "enabled": False,
                "smart_mode": True
            },
            "whitelist": {
                "office": OFFICE_WHITELIST.copy(),
                "game": GAME_WHITELIST.copy(),
                "system_critical": SYSTEM_CRITICAL.copy()
            },
            "cleanup": {
                "max_processes_per_batch": SAFE_CLEANUP_CONFIG.get('max_processes_per_batch', 3),
                "cleanup_interval": SAFE_CLEANUP_CONFIG.get('cleanup_interval', 2.0),
                "memory_limit_mb": SAFE_CLEANUP_CONFIG.get('memory_limit_mb', 100),
                "cpu_limit_percent": SAFE_CLEANUP_CONFIG.get('cpu_limit_percent', 50.0)
            },
            "ui": {
                "notification_duration": 5,
                "minimize_to_tray": True,
                "start_minimized": False
            }
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件，如果不存在则创建默认配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置，确保所有字段都存在
                    default_config = self._get_default_config()
                    return self._merge_configs(default_config, config)
            else:
                # 创建配置文件目录
                os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
                config = self._get_default_config()
                self._save_config(config)
                return config
        except Exception as e:
            print(f"⚠️ 加载配置文件失败: {e}")
            return self._get_default_config()
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """合并默认配置和用户配置"""
        result = default.copy()
        
        def merge_dict(base: Dict, update: Dict):
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
        
        merge_dict(result, user)
        return result
    
    def _save_config(self, config: Dict[str, Any]) -> bool:
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        # 导航到父级字典
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
        return self._save_config(self.config)
    
    def save(self) -> bool:
        """保存当前配置"""
        return self._save_config(self.config)
    
    def reset_to_default(self) -> bool:
        """重置为默认配置"""
        self.config = self._get_default_config()
        return self._save_config(self.config)
    
    def get_threshold(self, mode: str) -> float:
        """获取指定模式的内存阈值"""
        return self.get(f"thresholds.{mode}", 75.0)
    
    def get_whitelist(self, mode: str) -> list:
        """获取指定模式的白名单"""
        return self.get(f"whitelist.{mode}", [])
    
    def is_scheduler_enabled(self) -> bool:
        """检查托管模式是否启用"""
        return self.get("scheduler.enabled", False)
    
    def get_scheduler_interval(self) -> int:
        """获取托管模式间隔（分钟）"""
        return self.get("scheduler.interval_minutes", 5)

# 全局配置管理器实例
config_manager = ConfigManager()
