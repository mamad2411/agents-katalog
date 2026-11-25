---
name: jupyter-notebook
description: "Iterative Python via live Jupyter kernel (hamelnb)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [jupyter, notebook, repl, data-science, exploration, iterative]
    category: data-science
---

# Jupyter Notebook（hamelnb 实时内核）

通过实时 Jupyter 内核为您提供一个**具有状态保存功能的 Python REPL**。变量会在多次执行之间保持不变。当您需要逐步构建状态、测试 API、查看 DataFrame 或迭代处理复杂代码时，建议使用此功能而非 `execute_code`。

## 何时选择该工具而非其他工具

| 工具 | 适用场景 |
|------|----------|
| **本功能** | 迭代式探索、跨步骤保持状态、数据科学、机器学习任务，以及“先试试看再验证”的场景 |
| `execute_code` | 需要使用 hermes 工具（如网络搜索、文件操作）的一次性脚本，且无状态需求 |
| `terminal` | 执行 Shell 命令、构建项目、安装软件、操作 Git 以及进程管理 |

**经验法则：** 如果某项任务适合用 Jupyter Notebook 完成，那就选择此功能。

## 先决条件

1. 必须已安装 **uv**（检查方法：`which uv`）
2. 必须已安装 **JupyterLab**：`uv tool install jupyterlab`
3. 必须有正在运行的 Jupyter 服务器（详见下方的设置说明）

## 设置步骤

hamelnb 脚本的存放位置：
```
SCRIPT="$HOME/.agent-skills/hamelnb/skills/jupyter-live-kernel/scripts/jupyter_live_kernel.py"
```

如果尚未克隆：
```
git clone https://github.com/hamelsmu/hamelnb.git ~/.agent-skills/hamelnb
```

### 启动 JupyterLab

首先检查服务器是否已在运行：
```
uv run "$SCRIPT" servers
```

如果未找到任何服务器，请启动一个：
```
jupyter-lab --no-browser --port=8888 --notebook-dir=$HOME/notebooks \
  --IdentityProvider.token='' --ServerApp.password='' > /tmp/jupyter.log 2>&1 &
sleep 3
```

注意：本地代理访问模式下已禁用令牌/密码功能，且服务器以无界面模式运行。

### 创建用于 REPL 的笔记本

如果您仅需要 REPL 环境（无需现有笔记本），可创建一个最简的笔记本文件：
```
mkdir -p ~/notebooks
```
创建一个仅包含一个空代码单元格的最简版 .ipynb JSON 文件，然后通过 Jupyter REST API 启动内核会话：
```
curl -s -X POST http://127.0.0.1:8888/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"path":"scratch.ipynb","type":"notebook","name":"scratch.ipynb","kernel":{"name":"python"}}'
```

## 核心工作流程

所有命令都会返回结构化的 JSON 数据。为节省令牌使用量，请始终使用 `--compact` 参数。 

### 1. 发现服务器与笔记本

```
uv run "$SCRIPT" servers --compact
uv run "$SCRIPT" notebooks --compact
```

### 2. 执行代码（主要功能）

```
uv run "$SCRIPT" execute --path <notebook.ipynb> --code '<python code>' --compact
```

在多次执行调用之间，状态会保持不变。变量、导入内容以及对象都会继续存在。

使用 $'...' 引号格式即可支持多行代码：
```
uv run "$SCRIPT" execute --path scratch.ipynb --code $'import os\nfiles = os.listdir(".")\nprint(f"Found {len(files)} files")' --compact
```

### 3. 查看实时变量

```
uv run "$SCRIPT" variables --path <notebook.ipynb> list --compact
uv run "$SCRIPT" variables --path <notebook.ipynb> preview --name <varname> --compact
```

### 4. 编辑笔记本单元格

```
# View current cells
uv run "$SCRIPT" contents --path <notebook.ipynb> --compact

# Insert a new cell
uv run "$SCRIPT" edit --path <notebook.ipynb> insert \
  --at-index <N> --cell-type code --source '<code>' --compact

# Replace cell source (use cell-id from contents output)
uv run "$SCRIPT" edit --path <notebook.ipynb> replace-source \
  --cell-id <id> --source '<new code>' --compact

# Delete a cell
uv run "$SCRIPT" edit --path <notebook.ipynb> delete --cell-id <id> --compact
```

### 5. 验证（重启并运行全部）

仅当用户要求进行彻底的验证，或您需要确认代码笔记本能从始至终正常运行时才使用此选项。

```
uv run "$SCRIPT" restart-run-all --path <notebook.ipynb> --save-outputs --compact
```

## 实战经验技巧

1. **服务器启动后的首次执行可能会超时**——内核需要一些时间来初始化。如果出现超时情况，只需重新尝试即可。

2. **内核使用的 Python 即为 JupyterLab 的 Python**——所有包都必须安装在该环境中。如果需要额外的包，请先将其安装到 JupyterLab 的工具环境中。

3. **`--compact` 标志可大幅节省令牌数量**——务必使用该标志。不使用该标志时，JSON 输出可能会非常冗长。

4. **若仅用于纯 REPL 模式**，可创建一个 `scratch.ipynb` 文件，无需进行单元格编辑，只需反复使用 `execute` 命令即可。

5. **参数顺序很重要**——诸如 `--path` 这类的子命令标志应放在子子命令之前。例如：正确用法为 `variables --path nb.ipynb list`，而非 `variables list --path nb.ipynb`。

6. **如果尚未创建会话**，需通过 REST API 启动一个会话（详见“设置”部分）。没有活跃的内核会话，该工具将无法执行任务。

7. **错误信息会以包含堆栈跟踪的 JSON 格式返回**——请查看 `ename` 和 `evalue` 字段以了解具体问题所在。

8. **偶尔会出现 WebSocket 超时现象**——某些操作在首次尝试时可能会超时，尤其是在内核重启之后。在升级处理之前，先尝试重新执行一次。

9. **如果在该主机上 WebSocket 连接持续超时**，可强制使用 ZMQ 传输方式：
   `uv run "$SCRIPT" execute --transport zmq ...`。出现此问题的表现为：每次执行都会返回
   “Websocket 执行可能已到达内核层，因此跳过了自动回退机制”。实际上内核运行正常（REST 接口显示 execution_state 为 idle，且 execution_count 会递增）——仅是 WebSocket 回复通道出现了故障。ZMQ 传输方式直接使用 jupyter_client，从而避免了该问题。

10. **在启动仅用于 REST 接口的全新服务器时**，请添加参数
    `--ServerApp.disable_check_xsrf=True` —— 否则 POST /api/sessions 请求会返回
    “POST 请求中缺少 ‘_xsrf’ 参数”，从而导致内核会话创建失败。

## 超时默认设置

该脚本的默认每次执行超时时间为 30 秒。对于需要长时间运行的操作，可设置 `--timeout 120`。在初始设置或进行复杂计算时，建议使用较长的超时时间（60 秒以上）。
