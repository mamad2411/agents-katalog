---
name: gitnexus-auto
description: 在修改代码前自动运行 GitNexus 索引和影响分析。当用户要求分析、测试、优化、修改、重构代码时触发。在修改任何函数/类/方法前先做 impact 分析，改完后做 detect-changes 检查。
---

# GitNexus 自动分析 Skill

## 概述

该 Skill 让 CodeBuddy 在修改代码前自动调用 GitNexus 做代码分析，确保每次修改都是安全的。

**GitNexus 命令路径**: `D:\npm-global\gitnexus.cmd`
**辅助脚本路径**: `scripts/gitnexus_runner.py`

## 触发条件

用户说了以下内容时自动触发（不需要用户专门说"用 gitnexus"）：
- "帮我分析一下 / 分析代码 / 分析项目"
- "帮我测试 / 跑测试"
- "优化 / 优化代码 / 性能优化"
- "修改代码 / 改代码 / 重构 / refactor"
- "修复bug / debug / 调试"
- "添加功能 / 实现 / 开发"
- 任何涉及修改代码的请求

## 工作流程

### 第一步：检查并更新索引

在任何代码修改前，先检查索引状态：

```python
# 使用辅助脚本
python scripts/gitnexus_runner.py status <项目路径>
```

如果索引不是最新的，先更新索引（大型项目可能需要等待）：
```python
python scripts/gitnexus_runner.py analyze <项目路径>
```

### 第二步：理解要修改的代码

对将要修改的符号执行 360 度上下文分析：

```python
# 查看符号的完整上下文（调用者、被调用者、参与的执行流）
python scripts/gitnexus_runner.py context <项目路径> "<符号名>"

# 查询该功能相关的执行流
python scripts/gitnexus_runner.py query <项目路径> "<功能关键词>"
```

### 第三步：影响分析（最关键）

**在修改任何函数、类、方法之前必须先做 impact 分析**：

```python
# 查看修改某个符号会影响到哪些文件
python scripts/gitnexus_runner.py impact <项目路径> "<符号名>"
```

根据影响级别处理：
- **HIGH (20+ 文件)**：必须向用户报告影响范围，等待确认后再改
- **MEDIUM (5-19 文件)**：报告影响范围，可以继续但要小心
- **LOW (0-4 文件)**：可以直接修改，但改完后要做变化检测

### 第四步：修改代码

完成影响分析并确认安全后，再进行实际的代码修改。

### 第五步：修改后检查

修改完代码后，运行变化检测验证没有遗漏：

```python
python scripts/gitnexus_runner.py detect-changes <项目路径>
```

如果检测出意外的影响，需修复后再提交。

## 快速参考

| 任务 | 命令 |
|------|------|
| 检查索引 | `python scripts/gitnexus_runner.py status <path>` |
| 更新索引 | `python scripts/gitnexus_runner.py analyze <path>` |
| 查询功能 | `python scripts/gitnexus_runner.py query <path> "关键词"` |
| 查看上下文 | `python scripts/gitnexus_runner.py context <path> "符号"` |
| 影响分析 | `python scripts/gitnexus_runner.py impact <path> "符号"` |
| 变化检测 | `python scripts/gitnexus_runner.py detect-changes <path>` |
