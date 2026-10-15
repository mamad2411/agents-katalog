---
name: fix-import-error
description: |
  解决 Python 项目根目录模块导入问题。当用户遇到 ModuleNotFoundError、需要配置可编辑安装模式、或想要设置 pip install -e . 时触发此技能。

  触发场景：
  - 用户报告 ModuleNotFoundError 或 ImportError
  - 用户问"如何让项目根目录可导入"
  - 用户想要配置 pip install -e .（可编辑安装模式）
  - 用户问"pyproject.toml 怎么配置包"

  注意：此技能专注于项目结构导致的导入问题，不处理缺少第三方包的情况。
---

# Python 可编辑安装模式配置技能

## 概述

此技能帮助用户配置 Python 项目的可编辑安装模式（`pip install -e .`），解决项目根目录模块无法导入的问题。

## 问题根因

当执行 `python scripts/foo.py` 时：
1. Python 自动将脚本所在目录加入 `sys.path`
2. **不会**将项目根目录加入 `sys.path`
3. 导致项目根目录下的包无法被导入 → `ModuleNotFoundError`

## 解决方案

使用 `pip install -e .`（可编辑安装）将项目以可编辑模式安装到虚拟环境，让 Python 能正确找到项目包。

## 执行步骤

### 第一步：检查项目结构

确认项目有以下文件：
- `pyproject.toml`（必需）
- 包目录（如 `lib/`、`src/` 等，包含 `__init__.py`）

### 第二步：检查并完善 pyproject.toml

确保 `pyproject.toml` 包含基本项目信息和包配置：

```toml
[project]
name = "项目名"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    # 项目依赖
]

[tool.setuptools.packages.find]
# 白名单：指定哪些目录是可导入的包
include = ["lib*"]  # 根据实际包名修改
```

**注意**：如果项目使用 `src/` 布局，配置会有所不同：
```toml
[tool.setuptools.packages.find]
where = ["src"]
```

### 第三步：执行可编辑安装

根据项目的包管理器选择命令：

**使用 uv（推荐）**：
```bash
uv pip install -e .
```

**使用 pip**：
```bash
pip install -e .
```

### 第四步：验证安装成功

检查安装状态：
```bash
pip show <项目名>
```

确认输出中 `Location` 指向项目根目录（可编辑模式特征）。

查看 `.pth` 文件：
```bash
# Linux/macOS
ls .venv/lib/python*/site-packages/*.pth

# Windows
ls .venv/Lib/site-packages/*.pth
```

应该看到 `__editable__.<项目名>-*.pth` 文件。

### 第五步：验证导入功能

运行项目中的脚本，确认模块可以正常导入：
```bash
python scripts/your_script.py --help
```

## 常见问题

### Q: 修改代码后需要重新安装吗？

**不需要**。可编辑安装模式下，代码修改即时生效。只有修改 `pyproject.toml` 中的元数据（如 `name`、`version`、依赖列表）或包配置时才需要重新安装。

### Q: 新增顶级包目录怎么办？

如果新增了一个顶级包目录（如新增 `utils/`），需要：
1. 更新 `pyproject.toml` 的 `include` 配置
2. 重新运行 `pip install -e .`

### Q: 为什么 PyCharm 能跑但命令行不行？

PyCharm 会自动将标记为 "Sources Root" 的目录加入 Python Path，而命令行执行不会。这导致了"在我机器上能跑"的问题。使用 `pip install -e .` 可以确保所有环境行为一致。

## 技术原理

可编辑安装通过在 `site-packages/` 中创建 `.pth` 文件或 Finder 机制，将包名映射到源代码目录，无需复制代码文件。

**传统方式（setuptools < 64.0）**：
- 直接在 `.pth` 文件中写入源代码路径

**现代方式（PEP 660，setuptools >= 64.0）**：
- 生成 `.pth` 文件 + Finder 脚本
- 通过路径映射字典精确控制哪些模块可被导入
- 避免将项目根目录下所有 `.py` 文件都变成可导入模块

## 输出格式

完成配置后，向用户报告：
1. 已修改的 `pyproject.toml` 配置（如有修改）
2. 执行的安装命令
3. 验证结果（安装成功/失败）
4. 后续使用提示
