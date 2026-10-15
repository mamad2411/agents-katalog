---
name: venv-manager
description: 自动管理 Python 虚拟环境。当其他技能需要隔离的 Python 环境时，本技能帮助 AI 创建、激活和管理虚拟环境，确保依赖不冲突。
---

# Python 虚拟环境管理器

用于管理 Python 虚拟环境的指南和工具。

## 何时使用

- 技能需要安装 Python 依赖时
- 执行需要隔离环境的 Python 脚本时
- 避免全局 Python 环境被污染
- 多个项目需要不同版本的依赖时

## 快速开始

```bash
# 1. 创建虚拟环境
python scripts/create-venv.py <path> [--python <version>]

# 2. 激活虚拟环境
source scripts/activate-venv.sh <path>

# 3. 安装依赖
pip install -r requirements.txt
```

## 工作流程

1. **检查现有虚拟环境**
   - 检查 `.venv/` 或 `venv/` 目录是否存在
   - 检查 `.venv_path` 文件中的路径

2. **创建虚拟环境（如需要）**
   ```bash
   python scripts/create-venv.py <path>
   ```

3. **激活虚拟环境**
   ```bash
   source scripts/activate-venv.sh <path>
   # 或使用 Python API
   python scripts/activate-venv.py --activate <path>
   ```

4. **在虚拟环境中执行命令**
   - 所有 pip install 应在激活后执行
   - 所有 Python 脚本应在激活后运行

5. **清理（可选）**
   ```bash
   python scripts/cleanup-venv.py <path>
   ```

## 参考文件

| 文件 | 用途 |
|------|------|
| `scripts/create-venv.py` | 创建新的虚拟环境 |
| `scripts/activate-venv.py` | 激活虚拟环境（Python API） |
| `scripts/activate-venv.sh` | 激活虚拟环境（Shell 脚本） |
| `scripts/cleanup-venv.py` | 清理/删除虚拟环境 |
| `references/venv-guide.md` | 虚拟环境管理最佳实践 |
| `references/common-issues.md` | 常见问题解决方案 |
