import psutil
import time
from rich import print
from rich.table import Table


def get_cpu_usage():
    """
    获取当前 CPU 使用率（整体）
    interval=1 表示以 1 秒为间隔采样一次
    """
    return psutil.cpu_percent(interval=1)

def get_memory_info():
    """
    获取内存信息，包括总内存、可用内存、已用内存、使用百分比等
    返回一个字典，便于调用者处理
    """
    mem = psutil.virtual_memory()
    return {
        "total": mem.total,
        "available": mem.available,
        "used": mem.used,
        "percent": mem.percent
    }

def get_top_processes(limit=5):
    """
    获取当前系统中 CPU 占用最高的前几个进程（默认5个）。
    返回进程的 PID、名称、CPU 占用率、内存占用率。   
    """
    processes = []
    skipped = 0

    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(1)

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            pinfo = proc.info

            if pinfo['cpu_percent'] > 0.1 and pinfo["name"] not in ("System Idle Process", "System"):
                processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            skipped += 1
            continue

    top = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)

    if skipped > 0:
        print(f"[red]⚠️ 跳过了 {skipped} 个进程（无权限或已终止）[/red]")

    return top[:limit]


def display_system_status():
    """
    打印当前系统状态，包括 CPU、内存、进程。
    使用 rich 库格式化输出。   
    """
    print("[bold cyan]\n🖥️ 当前系统状态[/bold cyan]")

    cpu = get_cpu_usage()
    print(f"[green]CPU 使用率: [/green]{cpu}%")

    mem = get_memory_info()
    print(f"[green]内存使用率: [/green]{cpu}%")
    print(f"总内存: {mem['total'] / 1024 / 1024:.2f} GB")
    print(f"已用内存: {mem['used'] / 1024 / 1024:.2f} GB")
    print(f"可用内存: {mem['available'] / 1024 / 1024:.2f} GB")

    print("\n[bold yellow]高 CPU 占用进程:[/bold yellow]")

    # 使用 rich 表格输出进程信息
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("PID", width=6)
    table.add_column("进程名", width=25)
    table.add_column("CPU%", justify="right")
    table.add_column("内存%", justify="right")

    for proc in get_top_processes():
        table.add_row(
            str(proc['pid']),
            proc["name"][:25] if proc["name"] else "Unknown"
            f'{proc["cpu_percent"]:.1f}',
            f'{proc["memory_percent"]:.1f}'
        )

    print(table)

def show_system_status():
    print("\n📊 系统状态监控")
    print("-" * 30)

    # 内存信息
    mem = psutil.virtual_memory()
    print(f"内存使用: {mem.percent:.1f}% ({mem.used // (1024 ** 2)} MB / {mem.total // (1024 ** 2)} MB)")

    # CPU 信息
    cpu = psutil.cpu_percent(interval=0.5)
    print(f"CPU 使用: {cpu:.1f}%")

    # 活跃进程数量
    processes = list(psutil.process_iter())
    print(f"进程数量: {len(processes)}")

    print("-" * 30)