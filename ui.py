import tkinter as tk
from tkinter import ttk, messagebox
import psutil
from cleaner_safe import clean_memory  # 使用安全的清理模块
from monitor_realtime import SystemMonitor  # 导入我们的监控系统
import threading
import time

def get_memory_percent():
    return psutil.virtual_memory().percent

def run_cleaning():
    mode = mode_var.get()
    if not mode:
        messagebox.showwarning("提示", "请选择一个模式")
        return

    mem_percent = get_memory_percent()
    result_text.insert(tk.END, f"\n当前内存占用：{mem_percent:.1f}%\n")
    result_text.insert(tk.END, f"正在以【{mode}】模式清理...\n")
    
    clean_memory(mode=mode)

    result_text.insert(tk.END, "✅ 清理完成。\n")
    result_text.see(tk.END)



root = tk.Tk()
root.title("Memwatch - 智能内存管家")
root.geometry("580x500")  # 稍微加宽
root.resizable(False, False)
root.configure(bg='#f8f9fa')  # 现代化背景色

# 现代化样式
style = ttk.Style()
style.theme_use('clam')  # 使用更现代的主题

# 自定义样式
style.configure('Modern.TLabelframe', 
                background='#ffffff',
                borderwidth=1,
                relief='solid',
                bordercolor='#e9ecef')

style.configure('Modern.TLabelframe.Label',
                background='#ffffff',
                foreground='#495057',
                font=('Segoe UI', 9, 'bold'))
                


mode_var = tk.StringVar()
mode_frame = ttk.LabelFrame(root, text="🎯 选择模式", padding=20, style='Modern.TLabelframe')
mode_frame.pack(fill='x', padx=20, pady=15)

office_radio = ttk.Radiobutton(
    mode_frame, 
    text="办公模式", 
    variable=mode_var, 
    value="office", 
    # command=lambda: mode_var.set("office")
)
game_radio = ttk.Radiobutton(
    mode_frame,
    text="游戏模式",
    variable=mode_var,
    value="game",
    # command=lambda: mode_var.set("game")
)

office_radio.grid(row=0, column=0, padx=10, pady=5)
game_radio.grid(row=0, column=1, padx=10, pady=5)

# 创建监控面板
monitor_frame = ttk.LabelFrame(root, text="📊 实时系统监控", padding=20, style='Modern.TLabelframe')
monitor_frame.pack(fill='x', padx=20, pady=10)

# 内存显示
mem_frame = ttk.Frame(monitor_frame)
mem_frame.pack(fill='x', pady=2)

mem_label = ttk.Label(mem_frame, text="内存使用:")
mem_label.pack(side='left')

# mem_progress = ttk.Progressbar(mem_frame, length=200, mode='determinate')
# mem_progress.pack(side='left', padx=10)
# 自定义内存进度条
# mem_canvas = tk.Canvas(mem_frame, width=200, height=20, bg='lightgray', relief='sunken', bd=1)
# mem_canvas.pack(side='left', padx=10)
# 现代化内存进度条
mem_canvas = tk.Canvas(mem_frame, width=220, height=24, bg='white', highlightthickness=0)
mem_canvas.pack(side='left', padx=10)

mem_value_label = ttk.Label(mem_frame, text="0.0%")
mem_value_label.pack(side='left')

# CPU显示  
cpu_frame = ttk.Frame(monitor_frame)
cpu_frame.pack(fill='x', pady=2)

cpu_label = ttk.Label(cpu_frame, text="CPU使用:")
cpu_label.pack(side='left')

# cpu_progress = ttk.Progressbar(cpu_frame, length=200, mode='determinate')
# cpu_progress.pack(side='left', padx=10)
# 自定义CPU进度条  
# cpu_canvas = tk.Canvas(cpu_frame, width=200, height=20, bg='lightgray', relief='sunken', bd=1)
# cpu_canvas.pack(side='left', padx=10)
cpu_canvas = tk.Canvas(cpu_frame, width=220, height=24, bg='white', highlightthickness=0)
cpu_canvas.pack(side='left', padx=10)

cpu_value_label = ttk.Label(cpu_frame, text="0.0%")
cpu_value_label.pack(side='left')

# 进程数显示
process_label = ttk.Label(monitor_frame, text="进程数: 0")
process_label.pack(pady=2)
mem_label.pack(pady=5)


# 全局变量存储监控器
system_monitor = None

def update_monitor_display(stats):
    """
    更新监控显示的回调函数
    这个函数会被监控线程调用
    """
    def update_ui():
        """在主线程中更新UI"""
        try:
            # 更新内存显示
            mem_value_label.config(text=f"{stats['memory_percent']}%")
            
            # 绘制内存进度条
            draw_progress_bar(mem_canvas, stats['memory_percent'], get_memory_color(stats['memory_percent']))
            
            # 更新CPU显示
            cpu_value_label.config(text=f"{stats['cpu_percent']}%")
            
            # 绘制CPU进度条
            draw_progress_bar(cpu_canvas, stats['cpu_percent'], get_cpu_color(stats['cpu_percent']))
            
            # 更新进程数
            process_label.config(text=f"进程数: {stats['process_count']}")
            
        except Exception as e:
            print(f"UI更新出错: {e}")
    
    # 线程安全的UI更新
    root.after(0, update_ui)

def draw_progress_bar(canvas, percentage, color):
    """绘制现代化圆角渐变进度条"""
    canvas.delete("all")
    
    # 背景圆角矩形
    draw_rounded_rect(canvas, 4, 4, 216, 20, 10, '#f5f5f5', '#e8e8e8')
    
    # 进度条
    if percentage > 0:
        bar_width = max(20, int((percentage / 100) * 208))  # 最小宽度20px显示圆角
        
        # 主进度条
        draw_rounded_rect(canvas, 6, 6, 6 + bar_width, 18, 8, color, '')
        
        # 高光效果
        highlight_color = get_highlight_color(color)
        draw_rounded_rect(canvas, 6, 6, 6 + bar_width, 11, 8, highlight_color, '')
        
        # 光泽效果
        if bar_width > 40:
            gloss_width = min(30, bar_width // 3)
            canvas.create_oval(15, 7, 15 + gloss_width, 10, 
                             fill='white', stipple='gray25', outline='')

def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, fill_color, outline_color):
    """绘制圆角矩形"""
    # 四个圆角
    canvas.create_oval(x1, y1, x1 + radius*2, y1 + radius*2, 
                      fill=fill_color, outline=outline_color, width=0)
    canvas.create_oval(x2 - radius*2, y1, x2, y1 + radius*2, 
                      fill=fill_color, outline=outline_color, width=0)
    canvas.create_oval(x1, y2 - radius*2, x1 + radius*2, y2, 
                      fill=fill_color, outline=outline_color, width=0)
    canvas.create_oval(x2 - radius*2, y2 - radius*2, x2, y2, 
                      fill=fill_color, outline=outline_color, width=0)
    
    # 中间矩形
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                          fill=fill_color, outline='', width=0)
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                          fill=fill_color, outline='', width=0)

def get_highlight_color(color):
    """获取高光颜色"""
    highlight_map = {
        '#ff4444': '#ff7777',  # 红色高光
        '#ff8800': '#ffbb44',  # 橙色高光
        '#44aa44': '#77cc77',  # 绿色高光
        '#4488ff': '#77bbff'   # 蓝色高光
    }
    return highlight_map.get(color, '#ffffff')

def get_memory_color(percentage):
    """现代化内存颜色方案"""
    if percentage > 85:
        return '#ff3b30'  # iOS红色
    elif percentage > 70:
        return '#ff9500'  # iOS橙色
    elif percentage > 50:
        return '#ffcc00'  # iOS黄色
    else:
        return '#34c759'  # iOS绿色

def get_cpu_color(percentage):
    """现代化CPU颜色方案"""
    if percentage > 80:
        return '#ff3b30'  # iOS红色
    elif percentage > 60:
        return '#ff9500'  # iOS橙色
    elif percentage > 30:
        return '#007aff'  # iOS蓝色
    else:
        return '#32d74b'  # iOS绿色

def start_real_time_monitoring():
    """启动实时监控"""
    global system_monitor
    
    if system_monitor is None:
        system_monitor = SystemMonitor()
        system_monitor.add_update_callback(update_monitor_display)
        system_monitor.start_monitoring()
        print("✅ 实时监控已启动")

def stop_real_time_monitoring():
    """停止实时监控"""
    global system_monitor
    
    if system_monitor:
        system_monitor.stop_monitoring()
        print("🛑 实时监控已停止")


clean_btn = ttk.Button(root, text="开始清理", command = run_cleaning)
clean_btn.pack(pady=10)

result_text = tk.Text(root, height=10, wrap='word')
result_text.pack(fill='both', padx=10, pady=5)

# 启动实时监控
start_real_time_monitoring()

# 程序退出时清理
def on_closing():
    """程序退出时的清理工作"""
    stop_real_time_monitoring()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# 启动GUI主循环
root.mainloop()