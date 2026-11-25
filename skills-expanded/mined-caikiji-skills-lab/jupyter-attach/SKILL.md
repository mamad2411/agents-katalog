---
name: jupyter-attach
description: 管理长驻 Jupyter 会话时必须读取并执行本 skill 的调用方式：start 后多次 exec 共享变量，标准 Jupyter 协议实现。凡任务需跨调用/跨轮次保留 Python 状态、分多步跑长任务、反复接入同一环境（含 pandas/scipy）、执行或验证 .ipynb，或用户说"attach""常驻内核""持久变量""notebook 验证"时使用；一次性脚本直接运行即可，无需本 skill。
---

# jupyter-attach: 长驻 Jupyter 会话

## 它是什么

- 以独立进程常驻：`start` 一次，之后任意次 `exec` 都能读到之前的变量，`stop` 才结束——tmux 对 shell 的 attach 语义。
- 实现：走标准 Jupyter 协议（jupyter_client + connection file），不依赖特定工具的内部机制。

## 配置

未配置过的环境先运行 `check`，它会逐项自检并给出可直接复制的修复命令：

```bash
python {baseDir}/scripts/jupyter-attach.py check
```

没有解释器时优先装 uv 后运行 `setup`（由 uv 自动搭建环境，`setup` 幂等）：

```bash
python {baseDir}/scripts/jupyter-attach.py setup
```

解释器优先级：`JUPYTER_ATTACH_PYTHON` 环境变量 → `setup` 创建的默认 venv → 系统
`python`/`python3`。`start` 前也会做同样检查，缺依赖会报修复命令。

## 使用

```bash
python {baseDir}/scripts/jupyter-attach.py start     # 启动会话
python {baseDir}/scripts/jupyter-attach.py exec "x = 41\nprint(x)"   # 执行
python {baseDir}/scripts/jupyter-attach.py exec "print(x + 1)"       # 状态仍在
python {baseDir}/scripts/jupyter-attach.py exec -f code.py   # 从文件执行
python {baseDir}/scripts/jupyter-attach.py vars          # 查看变量
python {baseDir}/scripts/jupyter-attach.py stop          # 关闭
```

`exec` 返回 JSON：`stdout`/`stderr`/`result`/`error`（未运行会提示先 `start`）。

适合把数据处理 → 训练 → 报告拆成多次 `exec`，中间结果留在会话里。执行
`.ipynb` 时用会话解释器验证：`python -m jupyter nbconvert --to notebook
--execute --inplace 文件.ipynb`。

## 环境变量

| 变量 | 作用 |
|------|------|
| `JUPYTER_ATTACH_PYTHON` | 指定内核解释器 |

状态文件在 `~/.jupyter-attach/`（kernel.json / state.json / kernel.log），异常先看
`kernel.log`。
