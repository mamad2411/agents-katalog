---
name: claude
description: 在 Codex 聊天中通过 /claude、$claude 或明确调用 Claude 的请求，使用本机 Claude 读取、创建、编辑任务指定的文件，并返回真实执行结果。提到 Claude 但未要求调用时不执行。
---
<!-- managed-by: peer-agent -->

# 调用本机 Claude

用户在当前 Codex 聊天选择 `/claude` 或 `$claude`，附上任务，由 Codex 调用本机 Claude，结果返回当前聊天。不要让用户另开终端，也不要以 Codex 自己的意见或改动冒充 Claude 的执行。

## 解析任务与范围

- 以命令后的文字、附件及当前任务确定工作目录、目标文件、动作与验收标准；可以从当前上下文明确推定的内容不重复询问。只有缺少具体任务或文件目标时才补问。
- 将用户请求与必要规则组成一份任务提示传给 Claude；不转发整段聊天历史、凭证或无关私人文件。
- 强度：默认高（`--effort high`）。用户写了“超高”或“超高强度”作为强度要求时，本次用 `--effort xhigh`。
- 默认以当前项目或 worktree 为工作目录；用户指定其他目录时使用该目录。额外 `--add-dir` 仅限用户明确授权的目录。

## 运行环境与权限

- **提升权限（Escalated）**：Codex 默认沙箱无网络、不能写工作区外，而 Claude 需要访问 API、写会话记录并读取登录凭证。因此调用 Claude 的命令必须申请提升权限运行（`sandbox_permissions: "require_escalated"`），justification 写“调用本机 Claude，需要网络权限”。
- **统一入口优先**：优先使用 `peer` 统一调度器（`peer ask claude`），确保享有工作区快照（Snapshot）、改动对比（Diff）、防死循环深度标记（`PEER_DEPTH`）与安全熔断停机锁（`STOP`）保护。
- **环境隔离**：脚本启动前移除所有第三方 API 环境变量污染（如 `ANTHROPIC_BASE_URL` 等），确保走本机官方登录通道。

## 调用方式

分两步。用户原文只经文件编辑工具落盘，**严禁**把用户原文写进 Python / Shell 源码（字符串字面量、heredoc、echo 都不行），避免引号、反斜杠或换行破坏脚本或被当成代码执行；脚本只接收文件路径。

1. **落盘请求文件（文件编辑工具，如 apply_patch）**：在工作目录下新建 `.peer-review/requests/<YYYYMMDD-HHMMSS>-<6 位随机字母数字>-codex-claude.md`（随机段避免同一秒两次调用互相覆盖）。第一行写 `# 任务`，第二行起写用户原始任务及目标路径，逐字照抄用户原话，不改写、不转义（`peer route` 只看这一小节判定类型和授权原话）。Claude 是独立进程，看不到本次对话；用户原话需要对话上下文才能看懂时，在 `# 任务` 之后由你补写 `## 目标`、`## 原始需求与证据`、`## 需要阅读的文件`、`## 背景与约束` 小节（标题照写，`peer route` 遇到即停止）：列出要评的对象、绝对路径和已有决定；“背景与约束”每条标注【用户原话】/【已核实事实】/【主代理推断/方案假设】，【已核实事实】附“文件:行号”或“命令与输出”证据。补充内容不扩大授权、不写密钥与私人账号信息；原话指代不明且对话里也找不到对象时，先问用户，不调用。
2. **调用（提升权限运行下述 Python）**：只把第一行 `__REQ_FILE__` 换成上一步的文件路径（路径里不能有引号），其余按需改 `effort` / `allow_web`：

```python
import os, re, shutil, subprocess, sys, json
from pathlib import Path

req_file = Path("__REQ_FILE__").expanduser().resolve()
workdir = Path(os.getcwd()).resolve()
effort = "high"  # 默认高；用户写“超高”时改为 "xhigh"
allow_web = None  # 只读调用是否联网：None 跟随 config（默认联网）；用户明确要求不联网时改为 False
timeout_seconds = 1800

# 只接受第一步落盘的请求文件
if (req_file.parent != workdir / ".peer-review" / "requests"
        or not re.fullmatch(r"\d{8}-\d{6}-[A-Za-z0-9]{4,}-codex-claude\.md", req_file.name)
        or not req_file.is_file()):
    raise SystemExit("【错误】请求文件不是第一步落盘的路径或不存在：%s" % req_file)

peer_bin = shutil.which("peer")
if not peer_bin:
    peer_home = os.environ.get("PEER_HOME") or os.path.expanduser("~/.peer-review")
    for candidate in (os.path.join(peer_home, "bin", "peer"), os.path.expanduser("~/.local/bin/peer")):
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            peer_bin = candidate
            break
if not peer_bin:
    # 未找到 peer 调度工具时严格报错，拒绝无保护裸跑
    raise SystemExit("【错误】未找到 peer 调度工具（请运行 ./install.sh 或确保 peer 在 PATH 中）。所有跨端调用必须经过 peer 以保证沙箱安全、快照回滚与熔断保护。")

# 1. 任务类型与授权原话统一由 peer route 判定（三端共用同一套规则，否定与只读优先）
route = subprocess.run([peer_bin, "route", "--request", str(req_file)], capture_output=True, text=True)
if route.returncode != 0:
    print(route.stdout + route.stderr, file=sys.stderr)
    sys.exit(route.returncode)
if route.stderr.strip():
    print(route.stderr.strip(), file=sys.stderr)  # 被判为只读时的提示
parsed = json.loads(route.stdout)
kind, quote = parsed["kind"], parsed["quote"]
if kind == "image":
    raise SystemExit("【提示】Claude 没有图片生成能力：请改用 /codex 生图，或让 Claude 用 exec 写 SVG / 绘图代码。")

# 2. 通过 peer 调度（享有快照、diff 与统一熔断保护）；只有 exec 可写并带上授权原话
ask_cmd = [peer_bin, "ask", "claude", kind, "--request", str(req_file), "--cwd", str(workdir), "--caller", "Codex"]
if kind == "exec":
    ask_cmd += ["--quote", quote]
elif allow_web is not None:
    ask_cmd += ["--web" if allow_web else "--no-web"]
if effort:
    ask_cmd += ["--effort", effort]

proc = subprocess.run(ask_cmd, capture_output=True, text=True)
print(proc.stdout)
if proc.returncode != 0:
    print(proc.stderr, file=sys.stderr)
    sys.exit(proc.returncode)

# 3. 提取运行编号并等待；退出码 10 只再次 wait，绝不重新 ask
match = re.search(r"运行编号：([0-9a-zA-Z_-]+)", proc.stdout)
if match:
    wait_cmd = [peer_bin, "wait", match.group(1).strip(), "--cwd", str(workdir), "--timeout", str(timeout_seconds)]
    sys.exit(subprocess.run(wait_cmd).returncode)
sys.exit(0)
```

## 等待与汇报

- 汇报由 `peer wait` 自动格式化输出（包含状态、模型、用量、耗时及改动 diff）。
- 退出码 10 表示还在运行：只再次运行 `peer wait <运行编号> --cwd <工作目录>`，不要重新 ask。
- 执行完成后由 Codex 核对改动与生成结果，并向用户呈现。
