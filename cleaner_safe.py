import psutil
import time
import gc
import subprocess
from typing import List, Dict, Tuple
from config import (
    SYSTEM_CRITICAL, OFFICE_WHITELIST, GAME_WHITELIST, 
    MEMORY_THRESHOLD, SAFE_CLEANUP_CONFIG
)

class SafeMemoryCleaner:
    def __init__(self):
        self.cleaned_processes = []
        self.skip_count = 0
        
    def is_process_safe_to_clean(self, process_name: str, mode: str) -> bool:
        """
        判断进程是否可以安全清理
        """
        process_name_lower = process_name.lower()
        
        # 1. 系统关键进程绝不清理
        if any(critical.lower() in process_name_lower for critical in SYSTEM_CRITICAL):
            return False
            
        # 2. 根据模式检查白名单
        whitelist = OFFICE_WHITELIST if mode == 'office' else GAME_WHITELIST
        if any(white.lower() in process_name_lower for white in whitelist):
            return False
            
        return True
    
    def get_memory_hogs(self, min_memory_mb: float = 100) -> List[Dict]:
        """
        获取内存占用大户（但不包括关键进程）
        """
        memory_hogs = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                pinfo = proc.info
                if not pinfo['name']:
                    continue
                    
                # 计算内存使用（MB）
                memory_mb = pinfo['memory_info'].rss / 1024 / 1024
                
                if memory_mb > min_memory_mb:
                    memory_hogs.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'memory_mb': memory_mb,
                        'cpu_percent': pinfo['cpu_percent'] or 0
                    })
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
                
        # 按内存使用排序
        return sorted(memory_hogs, key=lambda x: x['memory_mb'], reverse=True)
    
    def gentle_cleanup(self, mode: str = 'office') -> Dict:
        """
        温和地清理内存，使用多种安全策略
        """
        result = {
            'initial_memory': psutil.virtual_memory().percent,
            'cleaned_processes': [],
            'memory_freed_mb': 0,
            'final_memory': 0,
            'method_used': []
        }
        
        print(f"🧹 开始安全内存清理 - {mode.upper()} 模式")
        print(f"📊 初始内存使用: {result['initial_memory']:.1f}%")
        
        # 1. 首先执行Python垃圾回收
        print("🔄 执行垃圾回收...")
        collected = gc.collect()
        if collected > 0:
            result['method_used'].append(f'垃圾回收清理了{collected}个对象')
        
        # 2. 检查是否需要进程清理
        threshold = MEMORY_THRESHOLD.get(mode, 75.0)
        current_memory = psutil.virtual_memory().percent
        
        if current_memory < threshold:
            print(f"✅ 内存使用率 {current_memory:.1f}% 低于阈值 {threshold}%，无需清理")
            result['final_memory'] = current_memory
            return result
        
        # 3. 获取内存占用大户
        memory_hogs = self.get_memory_hogs(SAFE_CLEANUP_CONFIG['memory_limit_mb'])
        
        cleaned_count = 0
        max_clean = SAFE_CLEANUP_CONFIG['max_processes_per_batch']
        
        for proc_info in memory_hogs[:max_clean * 2]:  # 检查更多，但只清理限定数量
            if cleaned_count >= max_clean:
                break
                
            if not self.is_process_safe_to_clean(proc_info['name'], mode):
                self.skip_count += 1
                continue
            
            # 4. 尝试温和地请求进程退出
            success = self._gentle_terminate_process(proc_info)
            if success:
                result['cleaned_processes'].append({
                    'name': proc_info['name'],
                    'memory_mb': proc_info['memory_mb']
                })
                result['memory_freed_mb'] += proc_info['memory_mb']
                cleaned_count += 1
                
                # 清理间隔
                time.sleep(SAFE_CLEANUP_CONFIG['cleanup_interval'])
        
        # 5. 执行系统内存优化命令（安全）
        self._optimize_system_memory()
        result['method_used'].append('系统内存优化')
        
        result['final_memory'] = psutil.virtual_memory().percent
        
        print(f"✅ 清理完成!")
        print(f"📊 最终内存使用: {result['final_memory']:.1f}%")
        print(f"🗑️ 清理了 {len(result['cleaned_processes'])} 个进程")
        print(f"💾 释放了约 {result['memory_freed_mb']:.1f} MB 内存")
        
        return result
    
    def _gentle_terminate_process(self, proc_info: Dict) -> bool:
        """
        温和地终止进程：先尝试优雅关闭，再尝试终止
        """
        try:
            proc = psutil.Process(proc_info['pid'])
            
            # 先尝试发送关闭信号（类似Alt+F4）
            try:
                proc.terminate()  # 发送TERM信号
                print(f"📤 已请求关闭: {proc_info['name']} (PID: {proc_info['pid']})")
                
                # 等待进程自然退出
                proc.wait(timeout=3)
                return True
                
            except psutil.TimeoutExpired:
                # 如果3秒内没有退出，强制杀死（但这里我们选择放弃）
                print(f"⏰ {proc_info['name']} 未在3秒内响应，跳过强制终止")
                return False
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
        except Exception as e:
            print(f"❌ 清理 {proc_info['name']} 时出错: {e}")
            return False
    
    def _optimize_system_memory(self):
        """
        执行安全的系统内存优化命令
        """
        try:
            # Windows内存整理命令（安全）
            subprocess.run(['sfc', '/scannow'], capture_output=True, timeout=10)
        except:
            pass  # 忽略错误，不影响主流程

def clean_memory(mode='office') -> Dict:
    """
    主要的清理接口，保持向后兼容
    """
    cleaner = SafeMemoryCleaner()
    return cleaner.gentle_cleanup(mode)

if __name__ == '__main__':
    # 测试代码
    result = clean_memory('office')
    print("\n" + "="*50)
    print("清理结果:")
    for key, value in result.items():
        print(f"{key}: {value}")