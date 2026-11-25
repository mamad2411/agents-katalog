---
name: codebase-inspection
description: "Inspect codebases w/ pygount: LOC, languages, ratios."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [LOC, Code Analysis, pygount, Codebase, Metrics, Repository]
    related_skills: [github]
prerequisites:
  commands: [pygount]
---

# 使用 pygount 进行代码库分析

通过 `pygount` 工具，可分析代码库的代码行数、语言分布、文件数量以及代码与注释的比例。

## 适用场景

- 用户需要查询代码行数（LOC）
- 用户希望了解代码库中的语言构成
- 用户想了解代码库的规模或结构
- 用户需要获取代码与注释的比例数据
- 其他关于“该代码库有多大”的一般性询问

## 前提条件

```bash
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

## 1. 基本概览（最常用）

获取包含文件数量、代码行数及注释行数的完整语言分析数据：

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**重要提示：** 请务必使用 `--folders-to-skip` 参数来排除依赖项目录和构建目录，否则 pygount 会遍历这些目录，从而导致处理时间过长甚至程序挂起。

## 2. 常见需排除的目录

请根据项目类型进行相应调整：

```bash
# Python projects
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript projects
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# General catch-all
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

## 3. 按特定语言进行筛选

```bash
# Only count Python files
pygount --suffix=py --format=summary .

# Only count Python and YAML
pygount --suffix=py,yaml,yml --format=summary .
```

## 4. 详细的逐文件输出内容

```bash
# Default format shows per-file breakdown
pygount --folders-to-skip=".git,node_modules,venv" .

# Sort by code lines (pipe through sort)
pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20
```

## 5. 输出格式

```bash
# Summary table (default recommendation)
pygount --format=summary .

# JSON output for programmatic use
pygount --format=json .

# Pipe-friendly: Language, file count, code, docs, empty, string
pygount --format=summary . 2>/dev/null
```

## 6. 结果解读

摘要表格的列说明：
- **Language** — 检测到的编程语言
- **Files** — 该语言对应的文件数量
- **Code** — 实际代码行数（包含可执行代码与声明性代码）
- **Comment** — 注释或文档行数
- **%** — 占比，即各类别占总数의百分比

特殊的伪语言类型：
- `__empty__` — 空文件
- `__binary__` — 二进制文件（如图片、编译后的文件等）
- `__generated__` — 自动生成的文件（通过规则识别得出）
- `__duplicate__` — 内容完全相同的文件
- `__unknown__` — 无法识别的文件类型

## 常见问题与注意事项

1. **务必排除 .git、node_modules、venv 目录** — 若未使用 `--folders-to-skip` 参数，pygount 会扫描所有目录，对于依赖关系复杂的庞大项目，这可能导致扫描耗时数分钟甚至卡住。
2. **Markdown 文件显示的代码行数为 0** — pygount 会将所有 Markdown 内容视为注释而非代码，这是正常现象。
3. **JSON 文件的代码行数偏低** — pygount 可能会对 JSON 文件的行数进行保守统计。如需获取准确的行数，建议直接使用 `wc -l` 命令。
4. **大型单仓库项目** — 对于规模极大的项目，建议使用 `--suffix` 参数指定要扫描的特定语言，而非全面扫描。
