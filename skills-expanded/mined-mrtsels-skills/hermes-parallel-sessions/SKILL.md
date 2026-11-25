---
name: hermes-parallel-sessions
description: 'Parallel Hermes sessions: find, message, don''t touch WIP.'
license: MIT
metadata:
  hermes:
    tags:
    - hermes
    - parallel-sessions
    - multi-agent
    - coordination
    related_skills:
    - hermes-claude-workflow
    - coding-agents
    - dynamic-workflow
  source_frontmatter:
    version: 1.0.0
    author: hermes-curator
  imported_from: hermes
---

# Hermes Parallel Sessions

用户经常在同一仓库/项目上并行开多个 Hermes TUI 会话（如本会话 + 一个叫 "campus-bus" 的会话同时推进一个 feature 的不同部分）。他们会说「X 指的是 hermes 会话，你直接发信息过去」——预期本会话能直接给另一个会话发消息，而不是替它做或问用户转达。

## When to Use

- 用户提到另一个 Hermes 会话（「X 指的是 hermes 会话，你直接发信息过去」）并要求直接联系它。
- 需要等另一个会话/PR 完成后再推进自己的部分（如叠加 PR 的 base retarget、依赖分支合入）。
- 工作区出现不属于自己的未提交改动，需要判断归属并避免破坏并行会话的 WIP。

## 找到目标会话

- `hermes sessions list`：标题 / workspace / Last Active / 会话 ID（如 `20260813_104437_e3660f`）。并行会话通常有描述性标题（campus-bus）且 workspace 相同。
- **注入前确认它空闲**：Last Active 应与已知最后一条消息吻合（无新用户轮次）；用 `session_search(session_id="<id>")` 看尾部——最后是 assistant 以问句收尾 = 在等输入，安全。

## 给另一个会话发消息

- `hermes chat -q '<消息>' --resume <session-id>`：把消息作为用户轮次注入该会话并**直接跑完一个 agent 轮次**（写同一个 session DB；目标 agent 会带完整工具权限执行指令，如改代码、commit）。
- **⚠️ 目标 TUI 不会实时显示这次注入**（campus-bus 案例）：注入进程写的是 session DB，而目标 TUI 界面由它自己的 gateway 进程内存驱动——用户在那个终端里看不到新消息/工具过程，会以为会话「卡了」（用户原话：「为什么campus-bus会话卡了，agent一直没反应」）。注入其实成功了：目标 agent 完成了指令、commit 已落盘。处理：(1) 注入前就预告「该会话终端不会实时更新，重启/恢复它即可看到」；(2) 用户报卡时让其退出目标终端并 `hermes -c <标题>` / `hermes --resume <id>` 重开（从 DB 重载即见完整轮次）；(3) 恢复后若出现「previous turn was interrupted」系统提示，是注入与 gateway 状态错位的残留，忽略即可。
- 放后台跑：`terminal(background=true, notify_on_complete=true)`——注入的轮次可能长达数分钟。
- **注入后验证（从外部，别看 TUI）**：目标工作区 `git log` 出现新 commit、`session_search(session_id=...)` 看它的回复、或后台进程输出 tail（含该会话最终总结）。
- 若目标会话活跃（正在跑轮次）就不要注入——两个 agent 进程写同一 session 会打架。等它空闲。

## 并行会话礼仪（用户强制）

- **别人的未提交文件别碰**：「跟你无关你就不用管，我本来就在并行」。工作区里不是你碰过的 modified/untracked 文件 = 并行会话的 WIP。切分支/清工作区前先 `git status` 辨认归属。
- 你自己的未提交改动和对方的 WIP 混在同一文件时：用 tracked-only `git stash push`（**勿加 -u**，untracked 留给对方），或者干脆不动工作区、用 `git worktree add wt/<name> <分支>` 在独立目录干活。
- 向对方会话转达指令时，主动标注哪些未提交文件是你的（对方会识别为「子代理的，不动」），避免互踩。
- 转达模糊指令时注明你的理解（例：用户说「原点」实为同音「圆点」——地图车辆圆点标记改图标），并说「如果你说的不是这个，随时纠正」。

## 监控另一个 PR/会话的进度

- 等对方合入依赖 PR 再推进自己的 PR：后台轮询 `for i in $(seq 1 240); do line=$(gh pr view <n> --json state,mergedAt --jq '[.state, (.mergedAt // "null")] | @tsv'); case "$line" in MERGED*) echo "MERGED $line"; exit 0;; CLOSED*) echo "CLOSED_UNMERGED"; exit 0;; esac; sleep 30; done`（background + notify_on_complete），MERGED 通知到达后再执行自己的部分（如 retarget base、跑 CI、merge）。
