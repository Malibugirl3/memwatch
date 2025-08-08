# Memwatch - 智能内存管理器

一个基于Python的智能内存管理工具，支持办公模式和游戏模式，提供实时监控和自动清理功能。

## 📁 项目结构

```
memwatch/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖包列表
├── config/                # 配置管理模块
│   ├── __init__.py
│   ├── default_config.py  # 默认配置
│   └── config_manager.py  # 配置管理器
├── core/                  # 核心功能模块
│   ├── __init__.py
│   ├── monitor.py         # 系统监控
│   ├── monitor_realtime.py # 实时监控
│   ├── cleaner.py         # 基础清理
│   └── cleaner_safe.py    # 安全清理
├── ui/                    # 用户界面模块
│   ├── __init__.py
│   └── main_window.py     # 主窗口
├── utils/                 # 工具模块
│   └── __init__.py
├── data/                  # 数据目录
│   └── logs/              # 日志目录
└── docs/                  # 文档目录
```

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行程序
```bash
# 命令行版本
python main.py

# GUI版本
python -c "from ui.main_window import *; root.mainloop()"
```

## 🎯 功能特性

### 双模式支持
- **办公模式**：保护IDE、浏览器、QQ等办公工具
- **游戏模式**：保护游戏进程和语音软件

### 安全清理机制
- 系统关键进程保护
- 白名单机制
- 温和清理策略（先请求关闭，再等待）

### 实时监控
- 内存使用率监控
- CPU使用率监控
- 进程数量统计

## ⚙️ 配置系统

配置文件位置：`data/user_config.json`

### 主要配置项
- 内存阈值设置
- 白名单管理
- 清理参数配置
- UI设置

## 🔧 开发计划

### 已完成
- ✅ 项目架构重构
- ✅ 模块化设计
- ✅ 配置系统基础框架
- ✅ 导入路径修复

### 待实现
- 🔄 托管模式（自动清理）
- 🔄 GUI配置界面
- 🔄 托盘系统
- 🔄 启动优化
- 🔄 安装助手

## 📝 技术栈

- **Python 3.7+**
- **psutil** - 系统监控
- **tkinter** - GUI界面
- **rich** - 终端美化（可选）

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License
