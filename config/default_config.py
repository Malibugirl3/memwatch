# 系统关键进程 - 绝对不能终止，否则会导致蓝屏
SYSTEM_CRITICAL = [
    'System', 'System Idle Process', 'smss.exe', 'csrss.exe', 'wininit.exe',
    'winlogon.exe', 'services.exe', 'lsass.exe', 'svchost.exe', 'explorer.exe',
    'dwm.exe', 'audiodg.exe', 'conhost.exe', 'spoolsv.exe', 'taskhostw.exe',
    'RuntimeBroker.exe', 'WmiPrvSE.exe', 'SearchIndexer.exe', 'MsMpEng.exe',
    'NisSrv.exe', 'SecurityHealthService.exe', 'SystemSettings.exe'
]

# 办公模式白名单 - 保留办公相关应用
OFFICE_WHITELIST = [
    'chrome.exe', 'msedge.exe', 'firefox.exe',          # 浏览器
    'idea64.exe', 'pycharm64.exe', 'Cursor.exe', 'code.exe',  # 开发工具
    'WINWORD.EXE', 'EXCEL.EXE', 'POWERPNT.EXE', 'OUTLOOK.EXE',  # Office
    'QQ.exe', 'WeChat.exe', 'DingTalk.exe', 'TIM.exe',  # 通讯工具
    'QQMusic.exe', 'netease.exe', '163MusicDesktop.exe',  # 音乐
    'Notepad.exe', 'notepad++.exe', 'typora.exe',       # 文本编辑
    'kazumi.exe', 'PotPlayerMini64.exe'                  # 视频播放
]

# 游戏模式白名单 - 保留游戏相关应用
GAME_WHITELIST = [
    'valorant.exe', 'cs2.exe', 'genshinimpact.exe', 'starrail.exe',
    'steam.exe', 'epicgameslauncher.exe', 'riotclientservices.exe',
    'GameBar.exe', 'GameBarFTServer.exe', 'XboxGameBar.exe',  # Xbox游戏栏
    'Discord.exe', 'TeamSpeak3.exe', 'YY.exe',               # 语音通讯
    'obs64.exe', 'XSplit.Broadcaster.exe',                   # 直播录制
    'chrome.exe', 'msedge.exe'  # 保留一个浏览器
]

# 内存清理阈值配置
MEMORY_THRESHOLD = {
    'office': 75.0,  # 办公模式：75%以上才清理
    'game': 80.0     # 游戏模式：80%以上才清理（更保守）
}

# 安全清理配置
SAFE_CLEANUP_CONFIG = {
    'max_processes_per_batch': 3,    # 每批最多清理3个进程
    'cleanup_interval': 2.0,         # 清理间隔2秒
    'memory_limit_mb': 100,          # 只清理占用超过100MB的进程
    'cpu_limit_percent': 50.0        # 只清理CPU占用超过50%的进程
}
