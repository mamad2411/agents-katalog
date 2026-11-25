---
name: hermes-session-coordination
description: Use when messaging or coordinating parallel Hermes sessions.
metadata:
  imported_from: hermes
---

# Hermes Session Coordination

用户经常并行开多个 Hermes TUI 会话（不同终端窗口）分工干活（如 "campus-bus" 会话做校巴功能），并用「告诉 session X …」把工作路由给并行会话。本技能覆盖：检测会话、判断空闲/忙碌、跨会话发消息、以及外部注入后目标 TUI 显示卡死的恢复。

## 检测与状态判断

- `hermes sessions list` — 全部会话（标题 / 工作区 / Last Active / ID）。**Last Active 距今几分钟且尾部是 assistant 提问 = 空闲可注入**；活跃中（正在跑 turn）别注入。
- 读会话尾部了解它在干什么：`session_search(session_id="<id>")`（首 20 + 尾 10 条，含压缩摘要的 Goal / Completed Actions / Active State / Blocked）。
- 会话重启会产生**新 session ID**（标题同名）——对比 ID 变化可知用户重启过目标会话。

## 给并行会话发消息（hermes chat -q --resume）

```bash
hermes chat -q '<指令>' --resume <session-id>
```

- 后台跑 + notify_on_complete：注入的 turn 由**你的进程**执行，加载目标会话的完整 transcript（可能几百条消息），一次 turn 可能跑 10+ 分钟。
- 指令用清晰中文、注明「用户让我转达（来自另一个 Hermes 会话）」——目标 agent 需要知道指令来源与用户意图。
- 工作会真实落地：目标会话的 agent 会读文件、commit、push 共享分支；事后用 `git log` / session 尾部验证。
- `hermes send` 只发到消息平台（Telegram/Discord/WeChat…）且是**出站**方向（bot→用户），**不能**作为注入手段；目标会话在本地 TUI 时没有平台路由可用。

## ⚠️ 关键坑：目标 TUI 显示卡死

外部 `hermes chat -q --resume` 写入的是 session DB；TUI 的 gateway 持有**内存态**，不会实时同步。结果：

- 目标会话的 agent 其实**做了活**（commit 会出现），但用户看那个终端 → 界面停在旧状态、像「agent 卡了/没反应」。
- **恢复：让用户重启/恢复目标 TUI**（`hermes -c "<会话名>"` 或退出重进）从 DB 重载，即可看到注入的 turn 与结果。
- **注入前先告知用户这个副作用**，避免被误判为故障。

## 并行会话礼仪

- 用户并行会话会动同一个 repo：提交、stash、worktree、rebase。**不是你的事别碰**——用户明确说「跟你无关你就不用管」。
- 发现分支/工作区变化异常时只做**只读核查**（`git log --oneline`、`git reflog`、`git stash list`、`git show origin/<branch>:<file>`），不动那些改动。
- 并行会话可能把你未提交的改动**一起 commit 进共享分支**（stash pop 后工作区与分支内容差异消失）——推/拆 PR 前用 `git show origin/<branch>:<file> | grep <特征串>` 验证 base 是否已含你的 hunk，包含则该文件的 PR 改动可直接丢弃（详见 cupedia-development 的 PR workflow 章节）。
- 用户可能把你当「某 PR 的观察者」：只读监控（`gh pr view/checks`）是常态任务；明确说停监控就停，转手动。

## References
- `references/parallel-session-case.md` — 2026-08-13 campus-bus 并行会话实操案例时间线：注入成功→工作落地→TUI 卡死→重启恢复。
