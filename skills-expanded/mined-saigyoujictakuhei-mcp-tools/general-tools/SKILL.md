---
name: General Tools
description: 通用工具集，涵盖文件系统操作、搜索、计算、网络、系统管理等 37 个 MCP 工具
version: 1.0.0
author: KazeMiMiRin
---

# 通用工具集 (General Tools) 操作手册

## 功能概览
通用工具集提供 **37 个 MCP 工具**，覆盖以下核心能力：

| 分类 | 工具数 | 工具列表 |
|------|--------|---------|
| 🧮 数学计算 | 2 | `add`, `calculate` |
| 📁 文件操作 | 5 | `read_file`, `write_file`, `delete_file`, `create_directory`, `file_info` |
| 🔍 搜索工具 | 6 | `search`, `complex_search`, `search_files`, `web_search`, `web_fetch`, `grep` |
| 🕐 时间日期 | 2 | `get_time`, `get_current_date` |
| 🖥️ 系统信息 | 2 | `get_system_info`, `get_dangerous_patterns` |
| 🌐 网络工具 | 2 | `get_weather`, `download_file` |
| 🔧 开发工具 | 4 | `create_tool`, `run_command`, `python_eval`, `run_python_script` |
| 📂 目录操作 | 3 | `list_directory`, `git_clone`, `git_pull` |
| 📊 统计工具 | 1 | `count_lines` |
| 🎯 管理工具 | 2 | `manage_approved`, `manage_blacklist` |
| 📡 MCP 工具 | 5 | `list_mcp_tools`, `list_mcp_prompts`, `list_skills`, `use_skill`, `test_tool_dummy` |
| 🎪 其他 | 7 | `hello_world`, `reverse_text`, `get_everything_info`, `web_search`, `web_fetch`, `search_files`, `grep` |

## 核心工具对比

### run_command vs python_eval vs run_python_script

| 维度 | `run_command` | `python_eval` | `run_python_script` |
|------|---------------|---------------|---------------------|
| **执行环境** | 系统 Shell（默认 PowerShell） | 当前 Python 解释器（线程内执行） | 独立 Python 子进程 |
| **进程创建** | 子进程 | 无（线程复用） | 新 Python 进程 |
| **输入** | Shell 命令字符串 | Python 代码字符串 | 脚本文件路径 + 命令行参数 |
| **上下文隔离** | 隔离（环境变量隔离） | 共享（当前解释器状态） | 隔离（进程级隔离） |
| **适用场景** | 系统命令、外部程序 | 代码片段、快速计算、数据处理 | 复杂脚本、需要隔离、命令行参数 |

### 场景选择决策树

| 场景 | 推荐工具 | 原因 |
|------|----------|------|
| 执行 `git`/`pip`/`dir` 等系统命令 | `run_command` | Shell 命令原生支持 |
| 数学计算/列表推导/字典操作 | `python_eval` | Python 原生支持，无进程开销 |
| 读取文件内容并处理 | `python_eval` | 可直接操作 Python 对象 |
| 执行已有 `.py` 脚本文件 | `run_python_script` | 原生支持文件路径和参数传递 |
| 需要命令行参数传递 | `run_python_script` | 支持 `args` 参数 |
| 复杂逻辑/多文件依赖 | `run_python_script` | 进程隔离，避免状态污染 |
| 正则表达式/JSON 解析 | `python_eval` | Python 标准库直接可用 |

## 注册工具清单

| # | 工具名 | 分类 | 参数数量 |
|---|--------|------|---------|
| 1 | `add` | 数学计算 | 2 |
| 2 | `calculate` | 数学计算 | 1 |
| 3 | `read_file` | 文件操作 | 1 |
| 4 | `write_file` | 文件操作 | 2 |
| 5 | `delete_file` | 文件操作 | 1 |
| 6 | `create_directory` | 文件操作 | 1 |
| 7 | `file_info` | 文件操作 | 1 |
| 8 | `search` | 搜索工具 | 1 |
| 9 | `complex_search` | 搜索工具 | 9 |
| 10 | `search_files` | 搜索工具 | 2 |
| 11 | `web_search` | 搜索工具 | 1 |
| 12 | `web_fetch` | 搜索工具 | 1 |
| 13 | `grep` | 搜索工具 | 1 |
| 14 | `get_time` | 时间日期 | 0 |
| 15 | `get_current_date` | 时间日期 | 0 |
| 16 | `get_system_info` | 系统信息 | 0 |
| 17 | `get_dangerous_patterns` | 系统信息 | 0 |
| 18 | `get_weather` | 网络工具 | 1 |
| 19 | `download_file` | 网络工具 | 2 |
| 20 | `create_tool` | 开发工具 | 4 |
| 21 | `run_command` | 开发工具 | 1 |
| 22 | `python_eval` | 开发工具 | 1 |
| 23 | `run_python_script` | 开发工具 | 1 |
| 24 | `list_directory` | 目录操作 | 0 |
| 25 | `git_clone` | 目录操作 | 1 |
| 26 | `git_pull` | 目录操作 | 1 |
| 27 | `count_lines` | 统计工具 | 1 |
| 28 | `manage_approved` | 管理工具 | 1 |
| 29 | `manage_blacklist` | 管理工具 | 1 |
| 30 | `list_mcp_tools` | MCP 工具 | 0 |
| 31 | `list_mcp_prompts` | MCP 工具 | 0 |
| 32 | `list_skills` | MCP 工具 | 0 |
| 33 | `use_skill` | MCP 工具 | 1 |
| 34 | `hello_world` | 测试工具 | 1 |
| 35 | `test_tool_dummy` | 测试工具 | 1 |
| 36 | `reverse_text` | 字符串处理 | 1 |
| 37 | `get_everything_info` | Everything 工具 | 0 |

## 注意事项
- 所有工具使用 `@tool` 装饰器注册，导入路径为 `from Lib.base.scripts.base import tool`
- MCP 传输层可能将 integer/boolean 转为字符串，部分工具内置安全转换函数
- 依赖安装清单：`httpx`, `selectolax`, `ddgs`, `everytools`, `pyautogui`, `psutil`, `pywin32`
- `run_command` 默认使用 PowerShell 执行，解决 CMD 对中文路径编码问题
- `python_eval` 使用 `exec()` 在子线程中执行，共享当前 Python 解释器上下文
- `run_python_script` 使用 `subprocess.run()` 启动新 Python 进程

## 版本历史
- **v1.0.0** - 更新工具数量至 37 个
- **v0.9.0** - Anthropic Skills 标准化改造（scripts/ + skills/ 双目录结构）
- **v0.8.x** - MCP 传输层类型转换修复
- **v0.7.x** - Everything 搜索功能还原

---

**归档完成**  
**生成时间**: 2026-06-11-2236 (Beijing Time)  
**项目维护**: 风见魅铃的猫娘
