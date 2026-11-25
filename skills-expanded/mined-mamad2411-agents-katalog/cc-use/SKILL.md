---
name: cc-use
description: >
  把较长的编码、排查、测试或交互式 CLI 工作交给 tmux 中的内层命令行编码 Agent，
  由当前外层 Agent 负责拆解任务、读取稳定屏幕快照、纠正方向、执行最终验收，并在本次
  任务结束后销毁内层 session。适用于用户明确要求使用 cc-use、希望把长时间实现工作
  交给内层 Agent、需要在真实 Codex CLI 或 Claude Code TUI 中完成受监督工作，或需要
  评估如何由 cron、launchd、systemd 等外部调度器触发 cc-use。
---

# cc-use

把当前 Agent 作为外层监督者，把 tmux 中的 Codex CLI 或 Claude Code 作为内层执行者。

`scripts/cc-use` 只负责创建 session、发送输入、观察屏幕、记录内层进程退出状态和清理资源。它不理解任务内容，也不判断屏幕表示完成、失败或阻塞。所有任务语义判断都由外层 Agent 完成。

## 运行模型与关键概念

cc-use 用 tmux 把执行上下文和监督上下文分开。内层 Agent 可以读取大量文件、运行长命令并产生很多终端输出；外层 Agent 保留用户目标、风险和验收标准，只在适合判断的时刻查看屏幕证据。

```text
用户目标
  ↓
外层 Agent：拆解、判断、纠偏、验收
  ↓ 短 prompt                         ↑ observation
cc-use helper：输入、等待稳定、保存快照
  ↓                                  ↑ tmux pane
内层 Agent：调查、编码、执行命令
```

关键概念：

- 外层 Agent：保留用户目标、拆解任务、检查风险、阅读快照、纠正方向并完成最终验收。
- 内层 Agent：调查问题、修改代码、运行命令和执行交互式工作。
- cc-use helper：管理 tmux、可靠发送文本、在屏幕稳定时保存快照。
- tmux socket：cc-use 固定使用 `~/.cc-use/tmux/cc-use`，与用户默认 tmux server 及 sandbox 私有的 `/tmp` 视图隔离。
- session：一个完整用户任务对应的 tmux session，其中保留同一个内层 Agent 对话。
- session 所有权：自动生成唯一名称，所有 tmux 操作使用精确 target；创建它的外层 Agent 负责顺序调用 `send`、`keys`、`monitor` 和 `finish`，不要并发操作同一个 session。
- 屏幕快照：observation 产生时当前 tmux pane 的标准化文本，只代表当时可见区域。
- observation：helper 在屏幕连续稳定后输出的结构化 JSON 事件，告诉外层“现在适合查看”，不替外层判断任务状态。
- scrollback：当前快照不足时临时读取的 tmux 历史，由外层渐进式向前翻看。

不要把整个长期任务一次性塞给内层 Agent。每次只发送一个边界清楚的调查、实现、测试或验证请求，然后根据真实结果决定下一步。

## 适用场景

- 对大型实现或重构按调查、编码、测试和修正分阶段推进。
- 让内层执行耗时排查、复现、构建、测试、下载或其他可能产生大量输出的命令。
- 由外层设计端到端、边界条件或对抗性测试，再让内层在真实环境中执行。
- 验证 Codex CLI、Claude Code、Skill、插件、MCP 或其他必须连续交互的 TUI 工作流。
- 用户明确要求使用 cc-use，或短任务需要真实内层 TUI 隔离和验证。

简单问答、一次文件读取、单条低风险命令或外层可以快速直接完成的修改，通常不要启动 cc-use。需要频繁选择账号、输入凭证或持续等待用户即时决策的任务，不适合无人监督执行。

## 生命周期

一次完整的用户任务使用一个独立 session，不要为每个 prompt 创建新 session。长程任务应在同一个内层 Agent 对话中连续发送多个短而明确的 prompt，以保留调查结果、代码上下文和前几轮对话。session 可以连续运行很久，也可以跨越多次外层交互；不要因为运行时间长而主动关闭。

一次调查、实现或验收没有达到预期时，只要整体任务仍在继续，就在原 session 中发送修正 prompt。短任务也遵循相同粒度，只是可能一次 `send` 后即可验收。只有整体任务最终成功、用户取消、外层决定以失败结束，或确认无法继续时，才执行 `finish`。

标准流程：

1. 用 `start` 创建 session；用户没有指定特殊组合时，启动同一 Agent 家族的内层 TUI。
2. 读取启动阶段返回的 `screen_path`，确认 TUI 已经可以正常接收任务。
3. 用 `send` 发送一个短而具体的请求。
4. 读取工作阶段快照，决定继续等待、在同一 session 发送下一个请求、询问用户或开始验收。
5. 从外层环境检查真实文件、测试结果和用户要求；如果验收未通过但仍可修复，继续使用原 session。
6. 整个用户任务最终结束时，用 `finish` 请求内层 TUI 正常退出并销毁本次 session。

## 命令速览

| 命令 | 用途 | 主要参数 |
|---|---|---|
| `start` | 创建任务 session，启动内层 TUI 并返回启动 observation | `--project`、`--agent`、`--session` |
| `send "TASK"` | 向现有内层 Agent 对话发送一个短 prompt | `--project`、`--session` |
| `keys KEY...` | 对启动菜单或明确的交互提示发送原始按键 | `--project`、`--session` |
| `monitor` | 不发送输入，等待现有屏幕稳定并返回 observation | `--project`、`--session` |
| `status` | 查看 session 是否存在和当前观察状态 | `--project`、`--session`、`--json` |
| `scrollback` | 临时读取当前快照之前的 tmux 历史 | `--session`、`--lines`、`--start`、`--end` |
| `finish` | 请求内层 TUI 退出，判断真实退出状态，再关闭 session 并删除观察状态 | `--project`、`--session` |
| `snapshot` / `list` | 立即抓屏或列出 cc-use session，用于诊断 | `snapshot` 使用位置参数传入 session；`list` 无参数 |

`--project` 默认为当前目录。`start` 可以自动生成唯一 session 名称，其他任务命令都应显式传入 `--session`。`--agent` 支持 `codex`、`claude` 和 `auto`，默认 `auto`。`keys` 接受字母、数字和 `Enter`、`Escape`、方向键等常用 tmux key 名称。

`start`、`send`、`keys` 和 `monitor` 支持 `--initial-quiet-seconds` 与 `--poll-interval`，默认分别为 30 秒和 2 秒；它们只控制屏幕观察，不表示任务进度或下次检查建议。

这些命令只有在 helper 最终退出并返回 observation 后才算完成。宿主执行工具如果暂时返回仍在运行的进程、session、cell 或其他可继续等待的句柄，保留该句柄并继续等待同一次调用；不要把中间阶段的空输出解释为成功、失败或回执缺失。使用包装脚本调用时，同时保留输出、退出状态和仍在运行的句柄，直到实际命令结束。

## 启动内层 Agent

从目标项目根目录运行：

```bash
<skill_dir>/scripts/cc-use start --project "$PWD" --agent codex
```

在 Claude Code 外层会话中使用：

```bash
<skill_dir>/scripts/cc-use start --project "$PWD" --agent claude
```

如果用户没有明确指定跨 Agent 组合，也没有其他特殊要求，始终让内外层使用同一 Agent 家族：不要从 Codex 外层启动 Claude Code，也不要从 Claude Code 外层启动 Codex。

`start` 会生成唯一 session 名称。保存返回 JSON 中的 `session`，后续命令都显式传入它。

默认 session 名称为 `ccu-<agent>-<project>-<timestamp>-<pid>`。多个任务共享专用 socket `~/.cc-use/tmux/cc-use`，但各自使用独立 session。用户显式传入 `--session` 时保留该名称。

### 启动检查

`start` 只启动 TUI，不发送任务，也不会额外盲按 Enter。返回 `screen_stable` 后，必须读取 `screen_path` 并进行语义检查。

如果画面显示以下情况，先不要发送任务 prompt：

- 登录、认证或账号选择；
- Agent、CLI、Skill 或其他工具的更新提示；
- 权限、信任或确认问题；
- shell 错误、命令不存在或进程退出；
- 无法确认 TUI 是否已经可用。

外层 Agent 可以处理结果明确、低风险并且不会改变环境的启动交互。例如升级提示提供“暂不升级”“跳过”或“继续使用当前版本”时，选择这类选项并继续检查启动画面。不要接受升级、安装或迁移，不要替用户选择账号、登录方式或凭证。权限、信任或确认提示只有在含义明确且已被用户当前授权覆盖时才能处理；否则保存必要证据，执行 `finish`，然后报告阻塞。

使用 `keys` 发送启动菜单明确要求的按键：

```bash
<skill_dir>/scripts/cc-use keys Escape \
  --project "$PWD" \
  --session SESSION_NAME
```

根据当前快照选择最小的按键序列，例如 `Escape`、`n Enter` 或方向键加 `Enter`。`keys` 只发送显式按键并等待新的稳定快照，不会使用 `send` 的多次 Enter 兼容流程。每次交互后都重新读取 `screen_path`，确认已经进入正常输入界面。不要根据关键词让脚本自动选择菜单项。

## 发送任务

确认启动画面正常后发送一个请求：

```bash
<skill_dir>/scripts/cc-use send "TASK_TEXT" \
  --project "$PWD" \
  --session SESSION_NAME
```

把 `TASK_TEXT` 原样传给 helper。任务拆解在外层完成，不要让 helper 添加角色说明、策略文字或包装提示。

`send` 会使用经过验证的 tmux buffer 和 Enter 提交流程发送文本，然后等待屏幕连续稳定一段时间并返回快照。

一个长程任务可以多次调用 `send`，每次都显式传入同一个 session 名称。不要在子任务之间调用 `finish`。

## 等待和观察

如果快照显示测试、构建、下载、服务或其他命令可能仍在安静运行，由外层 Agent 根据语义决定等待多久。等待后调用：

```bash
<skill_dir>/scripts/cc-use monitor \
  --project "$PWD" \
  --session SESSION_NAME
```

helper 不提供语义上的“下次检查建议”。外层 Agent 自己选择等待时长。

`status` 中的 `seconds_until_stable` 只是当前观察窗口距离“屏幕连续稳定”还差多少秒，不代表任务进度，也不代表建议多久后再次查看：

```bash
<skill_dir>/scripts/cc-use status \
  --project "$PWD" \
  --session SESSION_NAME \
  --json
```

## 补充屏幕上下文

`screen_path` 只保存 observation 产生时的当前 pane。内层最终回答可能比终端可见区域更长，关键错误、调查结论或命令输出也可能位于更早的历史中。稳定快照不够时，临时读取最近的 tmux scrollback：

```bash
<skill_dir>/scripts/cc-use scrollback \
  --session SESSION_NAME \
  --lines 2000
```

需要分段查看更早内容时：

```bash
<skill_dir>/scripts/cc-use scrollback \
  --session SESSION_NAME \
  --start -4000 \
  --end -2001
```

负数表示 tmux 历史行，`0` 表示当前可见区域第一行，`-` 表示当前 pane 末尾。

采用渐进方式阅读：先看最近一段；如果内容从中间开始、引用了更早细节或证据仍不完整，再用不重叠的范围继续向前。每读完一段，都由外层 Agent 根据语义决定是否已经足够、是否继续翻、下一段读取多大范围。不要预设固定页数，也不要为了“完整”而默认读取全部历史。

只在快照上下文不足时使用 scrollback。不要重复读取相同范围，不要把它当作持续日志流，也不要在屏幕仍快速变化时反复读取。

## 理解 observation

observation 是 helper 与外层 Agent 之间的观察协议。`start`、`send`、`keys` 或 `monitor` 会反复抓取并计算屏幕哈希；屏幕持续变化时继续等待，连续稳定达到静默阈值后保存 `.txt` 快照并输出一条 observation。

observation 以单行 JSON 打印到命令标准输出，同时追加到项目内 `.cc-use/state/<session>/watch.observations.jsonl`。`watch.json` 保存最近的观察状态。典型事件：

```json
{
  "event": "screen_stable",
  "phase": "work",
  "session": "ccu-codex-project-20260804120000-12345",
  "observed_at": 1785816000,
  "silence_seconds": 30,
  "screen_digest": "sha256...",
  "screen_path": "/project/.cc-use/state/.../screens/...txt"
}
```

字段含义：

| 字段 | 含义 |
|---|---|
| `event` | `screen_stable` 表示屏幕已连续稳定；session 消失时为 `session_unavailable` |
| `phase` | observation 来自 `startup`、`work`、`interaction` 或 `monitor` 阶段 |
| `session` | 本次完整用户任务对应的精确 tmux session 名称 |
| `observed_at` | observation 产生时的 Unix 时间戳 |
| `silence_seconds` | 当前屏幕连续未变化的秒数 |
| `screen_digest` | 标准化屏幕文本的哈希，用于检测变化 |
| `screen_path` | 保存当前 pane 文本的 `.txt` 文件路径，不是完整 transcript |

`screen_stable` 只表示当前屏幕在静默窗口内没有变化，适合外层 Agent 阅读。它不表示：

- 任务已经完成；
- 任务已经失败；
- Agent 正在等待；
- 命令仍在运行；
- 当前需要用户输入。

外层 Agent 必须读取 `screen_path` 后自行判断。

`session_unavailable` 表示 tmux 中已经没有目标 session。检查必要证据后，决定报告失败或重新开始本次任务。

## 外层决策

读取快照后：

- 显示最终回答或已回到输入提示符：从外层运行验收检查；如果仍需修复，在同一 session 发送下一个短请求。
- 显示仍在运行的命令：等待合适时间，再调用 `monitor`。
- 显示错误：发送一个短的修正请求，或报告阻塞。
- 显示需要普通交互输入：只有在意图明确且授权充分时才用 `keys` 发送响应。
- 显示可明确拒绝的更新提示：选择“不升级”或等价选项，重新检查画面。
- 显示登录、认证、账号选择或含义不清的更新提示：停止，清理 session 并报告。
- 内容被截断或不足以理解：从最近历史开始使用 `scrollback`，逐段向前补充，直到证据足够。

内层 Agent 的文字汇报不能作为成功证明。最终验收必须在外层执行，包括检查真实文件、运行相关测试、验证命令行为或检查 UI。

## 结束任务

任务结束时执行：

```bash
<skill_dir>/scripts/cc-use finish \
  --project "$PWD" \
  --session SESSION_NAME
```

以下所有终止路径都必须调用 `finish`：

- 整体实现和验收成功；
- 外层确认任务最终失败并停止继续修复；
- 用户取消或更换任务；
- 内层 Agent 无法继续；
- 登录、无法安全处理的更新或启动问题阻塞；
- 外层决定放弃当前执行。

不要设置基于运行时间的自动清理规则。一个合法任务可能持续数小时或跨天；只根据任务生命周期结束 session。

外层 Agent 只负责判断整个任务何时结束并调用 `finish`，不需要再看退出画面。`finish` 的后续判断是机械过程：

1. 用独立的单次提交流程向内层 TUI 粘贴 `/exit`，只发送一次 `Enter`；
2. 启动内层 TUI 的 runner 是其直接父进程，会等待子进程结束并取得真实 exit code；
3. exit code 为 `0` 时返回 `shutdown: graceful`，非 `0` 时返回 `shutdown: abnormal`；
4. 等待 10 秒仍没有退出记录时，精确关闭目标 tmux session，并返回 `shutdown: forced`；
5. 最后删除这个 session 的观察状态。

runner 取得 exit code 的机制等价于父进程通过 `wait`/`waitpid` 接收子进程状态，不读取 shell prompt，也不让外层 Agent 根据屏幕猜测。正常或异常退出后，登录 shell 仍可能留在 tmux 中；此时关闭 tmux 只是资源清理，不会把结果改成 `forced`。10 秒只是在显式调用 `finish` 后给 `/exit` 的退出宽限期，不是按任务运行时长自动清理。

## 环境与启动命令

cc-use 先让 tmux 启动正常登录 shell，再通过 shell 启动内部 runner。runner 随后执行：

```text
command codex ...
command claude ...
```

runner 保持为内层 TUI 的父进程，以便在 TUI 结束时记录 exit code。登录 shell 按用户自己的正常规则加载 PATH、凭证和其他环境设置。cc-use 不扫描、不拼装、不注入环境变量，也不依次 source 各种 shell 配置文件。

`command` 会绕过 shell alias 和 function，但仍然使用登录 shell 最终得到的 PATH。如果用户刚修改了正常 shell 启动文件，新建 session 会重新读取；已经运行的旧 session 不会自动刷新环境。

## 诊断命令

helper 的所有 tmux 操作都使用专用 socket `~/.cc-use/tmux/cc-use`。只有 helper 无法表达所需诊断时才直接调用 tmux；fallback 命令必须同时使用 `-S ~/.cc-use/tmux/cc-use` 和精确 target。同一 session 的一个 helper 调用尚未返回时，不要并发调用 `send`、`keys`、`monitor` 或 `finish`。

只读 attach：

```bash
tmux -S ~/.cc-use/tmux/cc-use attach -r -t '=SESSION_NAME'
```

立即抓取当前 pane：

```bash
<skill_dir>/scripts/cc-use snapshot SESSION_NAME
```

列出 cc-use 命名的 session：

```bash
<skill_dir>/scripts/cc-use list
```

这些命令用于诊断。正常任务通过 `start`、`send`、`keys`、`monitor` 和 `finish` 管理。

## TUI 录制

只有用户明确要求录制终端演示或生成 GIF 时，才读取 `references/tui-recording.md`。

## 定时任务

用户要求用 cron、launchd、systemd timer 或其他外部调度器触发 cc-use 时，先读取 [references/scheduled-tasks.md](references/scheduled-tasks.md)。把它作为环境和生命周期设计参考，不要恢复 schedule 命令、定时规则数据库或 cc-use 内部调度框架。

具体调度方式必须根据任务所属用户、登录 shell、环境变量来源、机器休眠行为、重叠执行策略和通知方式决定。cc-use helper 仍然只负责 tmux session、输入、观察和清理；外部调度器负责触发，外层 Agent 或控制器负责语义监督。
