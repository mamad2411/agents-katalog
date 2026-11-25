---
name: python-use
description: 定义 Python 环境管理和依赖管理的强制规范。当 Agent 需要使用 Python、创建虚拟环境、安装依赖、管理 Python 版本时必须应用此技能。强制使用 uv 工具，禁止 pip/conda，确保项目级环境隔离。
---

# Python 环境管理与依赖管理规范

本技能定义了 Agent 在使用 Python 时必须严格遵循的环境管理和依赖管理规则，确保项目环境的隔离性、可复现性和安全性。

---

## 核心规则

### 规则 1：必须使用 uv 工具管理环境和依赖

**规则说明：**
- 所有 Python 环境创建、依赖安装、版本管理操作必须通过 `uv` 工具执行
- **严禁**使用 `pip`、`conda`、`poetry`、`pipenv` 或其他包管理工具
- 唯一例外：当项目明确要求使用特定工具且用户显式确认时

**原因：**
1. **速度优势**：uv 比 pip 快 10-100 倍，显著提升开发效率
2. **一致性保障**：uv 提供统一的工作流，减少工具切换带来的配置差异
3. **内置环境管理**：uv 集成了虚拟环境创建、Python 版本管理、依赖锁定等功能
4. **更好的依赖解析**：uv 拥有更先进的依赖解析算法，减少冲突

**违反风险：**
- 混用不同包管理器可能导致依赖冲突
- 环境状态难以追踪和复现
- 可能意外修改系统 Python 环境

---

### 规则 2：根据依赖要求选择合适的 Python 版本

**规则说明：**
- 安装依赖前，必须确认所需库对 Python 版本的兼容性要求
- 优先使用项目中 `pyproject.toml` 或 `.python-version` 指定的版本
- 若无指定，选择依赖库支持的最新稳定 Python 版本

**原因：**
1. 避免因版本不兼容导致的安装失败或运行时错误
2. 确保能使用依赖库的所有功能
3. 某些库可能需要特定版本的 Python 特性

**标准操作流程：**
```bash
# 查看可用的 Python 版本
uv python list

# 安装特定 Python 版本
uv python install 3.11

# 为当前项目固定 Python 版本
uv python pin 3.11

# 查找已安装的 Python 版本
uv python find
```

**违反风险：**
- 依赖安装失败
- 运行时出现兼容性错误
- 某些功能无法正常使用

---

### 规则 3：依赖安装仅限当前项目目录

**规则说明：**
- 所有依赖必须安装在项目本地的虚拟环境中（默认为 `.venv` 目录）
- **严禁**使用任何全局安装参数，包括但不限于：
  - `--global`
  - `--user`
  - `--system`
  - `--target` 指向项目外路径
- **严禁**直接向系统 Python 环境安装包

**原因：**
1. 全局安装可能破坏系统 Python 环境
2. 影响其他项目或系统工具的正常运行
3. 难以追踪和清理不再需要的依赖
4. 导致项目在不同机器上难以复现

**违反风险：**
- 污染系统环境或其他项目环境
- 造成依赖版本冲突
- 可能破坏操作系统依赖的 Python 工具
- 项目无法在其他环境正确运行

---

### 规则 4：确保项目环境完全隔离

**规则说明：**
- 每个项目必须拥有独立的虚拟环境
- 虚拟环境必须位于项目目录内（推荐使用默认的 `.venv`）
- 不同项目间不得共享虚拟环境
- 虚拟环境目录（`.venv`）应加入 `.gitignore`

**原因：**
1. 避免项目间依赖冲突
2. 确保项目的可移植性和可复现性
3. 便于项目清理（删除项目目录即可完全清理）
4. 保护系统 Python 环境的稳定性

**违反风险：**
- 项目间依赖相互干扰
- 升级一个项目的依赖可能破坏另一个项目
- 难以确定每个项目的真实依赖

---

## 标准命令参考

### 项目初始化

```bash
# 初始化新项目（创建 pyproject.toml）
uv init

# 初始化并指定项目名称
uv init my-project

# 创建虚拟环境（默认在 .venv 目录）
uv venv

# 创建指定 Python 版本的虚拟环境
uv venv --python 3.11

# 创建指定名称的虚拟环境
uv venv .venv
```

### 依赖管理

```bash
# 添加依赖到项目
uv add requests

# 添加指定版本的依赖
uv add "requests>=2.28.0"

# 添加开发依赖
uv add --dev pytest

# 添加可选依赖组
uv add --group test pytest pytest-cov

# 从 Git 仓库添加依赖
uv add "package @ git+https://github.com/user/repo.git"

# 移除依赖
uv remove requests

# 同步项目依赖（根据 pyproject.toml 和 uv.lock）
uv sync

# 生成/更新锁文件
uv lock

# 查看依赖树
uv tree
```

### pip 接口命令（传统工作流）

```bash
# 在虚拟环境中安装包
uv pip install requests

# 安装指定版本
uv pip install "requests==2.28.0"

# 从 requirements.txt 安装
uv pip install -r requirements.txt

# 查看已安装的包
uv pip list

# 冻结当前环境依赖
uv pip freeze > requirements.txt

# 检查依赖兼容性
uv pip check

# 卸载包
uv pip uninstall requests

# 编译 requirements（生成锁定版本）
uv pip compile requirements.in -o requirements.txt

# 同步环境与锁文件
uv pip sync requirements.txt
```

### 运行命令

```bash
# 在项目环境中运行 Python 脚本
uv run python script.py

# 在项目环境中运行模块
uv run python -m pytest

# 运行项目定义的入口点
uv run my-cli-tool

# 临时添加依赖运行
uv run --with httpx python script.py
```

### 工具管理

```bash
# 临时运行工具（不安装）
uvx ruff check .

# 安装工具到用户目录
uv tool install ruff

# 列出已安装的工具
uv tool list

# 卸载工具
uv tool uninstall ruff
```

---

## 最佳实践

### 1. 项目标准工作流

```bash
# 1. 进入项目目录
cd my-project

# 2. 初始化项目（如果尚未初始化）
uv init

# 3. 设置 Python 版本
uv python pin 3.11

# 4. 创建虚拟环境
uv venv

# 5. 添加项目依赖
uv add requests pandas numpy

# 6. 添加开发依赖
uv add --dev pytest black ruff

# 7. 锁定依赖版本
uv lock

# 8. 同步环境
uv sync
```

### 2. 克隆项目后的环境恢复

```bash
# 克隆项目
git clone https://github.com/user/project.git
cd project

# 创建虚拟环境并同步依赖
uv sync
```

### 3. .gitignore 配置

确保将以下内容添加到 `.gitignore`：

```gitignore
# Python 虚拟环境
.venv/
venv/

# uv 缓存
.uv_cache/

# Python 编译文件
__pycache__/
*.py[cod]
*$py.class
*.so

# 分发/打包
dist/
build/
*.egg-info/
```

### 4. 项目文件结构推荐

```
my-project/
├── .venv/              # 虚拟环境（不提交到版本控制）
├── .python-version     # Python 版本固定
├── pyproject.toml      # 项目配置和依赖声明
├── uv.lock             # 依赖锁文件（提交到版本控制）
├── src/                # 源代码
│   └── my_project/
├── tests/              # 测试代码
└── README.md
```

---

## 常见错误及避免方法

### 错误 1：使用 pip 安装依赖

```bash
# ❌ 错误做法
pip install requests

# ✅ 正确做法
uv add requests
# 或
uv pip install requests
```

### 错误 2：全局安装包

```bash
# ❌ 错误做法
pip install --user requests
uv pip install --system requests

# ✅ 正确做法
# 确保在项目目录中，使用虚拟环境
uv venv
uv add requests
```

### 错误 3：忘记创建虚拟环境

```bash
# ❌ 错误做法 - 直接安装到系统环境
cd my-project
uv pip install --system requests

# ✅ 正确做法 - 先创建虚拟环境
cd my-project
uv venv
uv add requests
```

### 错误 4：在错误的目录操作

```bash
# ❌ 错误做法 - 在错误目录创建环境
cd /
uv venv
uv add requests

# ✅ 正确做法 - 在项目目录操作
cd ~/projects/my-project
uv venv
uv add requests
```

### 错误 5：共享虚拟环境

```bash
# ❌ 错误做法 - 多个项目使用同一个虚拟环境
cd project-a
uv venv /shared/venv
cd ../project-b
source /shared/venv/bin/activate

# ✅ 正确做法 - 每个项目独立环境
cd project-a
uv venv
cd ../project-b
uv venv
```

---

## 环境激活（可选）

虽然 `uv run` 命令可以自动在虚拟环境中执行，但有时手动激活环境也很有用：

**Windows (PowerShell)：**
```powershell
.venv\Scripts\activate
```

**Windows (CMD)：**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux (bash/zsh)：**
```bash
source .venv/bin/activate
```

**退出虚拟环境：**
```bash
deactivate
```

---

## 检查清单

在执行 Python 相关操作前，请确认：

- [ ] 当前工作目录是否为项目根目录
- [ ] 是否已创建项目虚拟环境（`.venv` 目录存在）
- [ ] 是否使用 `uv` 命令（而非 pip/conda 等）
- [ ] 依赖安装命令是否包含全局参数（如有则移除）
- [ ] Python 版本是否与依赖要求兼容

---

## 参考资源

- [uv 官方文档](https://docs.astral.sh/uv/)
- [uv GitHub 仓库](https://github.com/astral-sh/uv)
- [pyproject.toml 规范](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
