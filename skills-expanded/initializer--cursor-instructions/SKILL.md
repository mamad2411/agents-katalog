# Linux System Initializer - Cursor AI 指令

## 🎯 项目概述

这是一个 Linux 系统自动化初始化工具，使用现代 Python 技术栈构建：

- **UI**: Rich + Textual (终端用户界面)
- **配置**: YAML 驱动的模块化设计
- **架构**: 现代 Python 项目 (pyproject.toml)

## 🚨 关键执行规则

### 🔍 环境检测

**重要**：根据用户环境应用不同的执行规则：

- **WSL (Windows子系统)**: Shell 包含 `wsl.exe` 或 OS 显示 `win32` 但有 Linux 环境
- **标准 Windows/Mac**: 常规桌面环境
- **原生 Linux**: 直接 Linux 安装

### 执行限制（依环境而定）

#### 对于非 WSL 环境

**严格要求远端执行！所有脚本必须在远端服务器 192.168.0.33 上运行。**

- ❌ ./install.sh
- ❌ ./run.sh  
- ❌ python main.py
- ❌ 创建本地虚拟环境

#### 对于 WSL 环境

- ✅ **允许**：本地测试和开发
- ✅ **允许**：创建本地虚拟环境用于测试
- ✅ **允许**：本地运行脚本进行开发/测试
- ⚠️ **建议**：生产环境仍优先使用远端执行

### 正确工作流程

#### 默认（远端执行）

```bash
# 1. 同步代码（推荐使用内置脚本）
tools/sync-to-remote.sh           # 同步到 root@192.168.0.33:~/Initializer
tools/sync-to-remote.sh -n        # 预览（Dry-Run）
tools/sync-to-remote.sh -d        # 删除远端多余文件
tools/sync-to-remote.sh -H 192.168.0.33 -u root -D ~/Initializer

# 2. 远端执行
ssh root@192.168.0.33
cd ~/Initializer
./install.sh
./run.sh
```

#### WSL 例外

```bash
# 1. 本地测试（WSL 用户）
./install.sh
./run.sh
python main.py

# 2. 远端验证（推荐）
tools/sync-to-remote.sh
ssh root@192.168.0.33
cd ~/Initializer && ./run.sh
```

## 📁 项目结构

```text
src/              # Python 源代码 (本地编辑)
  ├── app.py      # 主应用类
  ├── config_manager.py  # 配置管理
  └── modules/    # 功能模块
config/           # YAML 配置文件 (本地编辑)
  ├── app.yaml    # 应用配置
  └── presets/    # 预设配置
legacy/           # 原始 Bash 脚本 (参考)
install.sh          # 安装脚本 (仅远端执行)
run.sh            # 启动脚本 (仅远端执行)
main.py           # 程序入口 (仅远端执行)
```

## ⚙️ 技术配置

- **Python 版本**: 3.8+
- **虚拟环境**: `initializer-venv` (不是 venv)
  - **WSL**: 可在本地创建用于测试
  - **非 WSL**: 仅在远端服务器创建
- **远端服务器**: 192.168.0.33
- **包管理**: pyproject.toml (支持 pip install -e .)

## 🔧 依赖管理

- **核心依赖**: rich, textual, pyyaml, click, psutil, distro
- **开发依赖**: pytest, black, flake8, mypy
- **安装方式**: `pip install -e .` 和 `pip install -e .[dev]`

## 📚 文档参考

- **主规则**: `.cursorrules` (Cursor 自动读取)
- **项目说明**: `README.md`
- **开发指南**: `DEVELOPMENT.md`

## 🎨 用户界面特性

- TUI (Terminal User Interface) 应用
- 模块化配置系统
- 预设支持 (server, desktop, minimal)
- 实时系统信息显示
- 彩色主题支持

## 💡 AI 助手行为准则

### 环境检测优先

1. **首先检测**: 用户环境 (WSL vs 非 WSL)
2. **应用规则**: 根据检测到的环境应用相应规则
3. **告知选项**: 根据用户环境提供可用选项

### 行为规则

#### 对于 WSL 用户

1. **代码编辑**: 可以建议本地编辑源文件
2. **脚本执行**: 可以建议本地测试，推荐远端验证
3. **依赖安装**: 允许本地安装用于测试
4. **测试验证**: 本地测试 + 远端验证
5. **工作流程**: 本地开发测试 → 远端生产验证

#### 对于非 WSL 用户

1. **代码编辑**: 可以建议本地编辑源文件
2. **脚本执行**: 必须引导到远端服务器
3. **依赖安装**: 必须在远端进行
4. **测试验证**: 必须在远端环境
5. **规则提醒**: 始终强调远端执行要求
