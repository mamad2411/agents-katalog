---
name: cross-session
description: 用 mcp__crosssession__* tools 睇其他 DSH session 做緊咩，或者通知佢哋自己做緊咩。當用戶提到「另一個 session／另一個 window／另一邊」、要做可能同其他 session 撞嘅嘢（同一個 repo、長任務、改同一批檔案）、或者想知係咪已經有 session 處理緊同一件事時使用。
---

# Cross-session awareness（DSH）

`mcp__crosssession__*` 係一個唯讀 DSH session log 嘅 MCP server（source：`Desktop/agent_cross-session_mcp`），
令一個 session 知道其他 session 做緊咩。

## 幾時用邊個 tool

| 情況 | Tool |
|---|---|
| 開一個會改 repo／跑長任務之前 | `peers` — 睇下有冇其他 session 喺同一個 workspace 做緊嘢 |
| 用戶話「另一邊／另一個 session 做緊」 | `peers` 搵到之後用 `session_detail` 睇佢做過咩 |
| 要改一個可能有第二個 session 郁緊嘅 repo | `overlaps` — 列邊啲檔案兩個 session 都掂過、有冇 git 撞 |
| 自己要霸住某個 repo／做長時間改動 | `announce` 一句（一句起兩句止，用返對話語言） |
| 想知有冇人留低嘢俾你 | `board` |
| 唔肯定自己係邊個 session | `whoami` |

## 規則
- **唔好每個 turn 都 call** — 開工前、交更、或者用戶問到先 call。
- `peers` 入面標住 `← this session` 嘅就係你自己，唔好當佢係其他 session。
- 呢啲 tools 唔會改其他 session 嘅嘢；唯一會寫嘢嘅係 `announce`（寫入 `~/.dsh/cross-session/board.jsonl`）。
- 見到另一個 session 已經做緊同一件事：**唔好照做**，同用戶講聲先。
- `overlaps` 報 `⚠ CONFLICT` 或者「兩個 session 都跑 git」：停手同用戶講，建議其中一邊開 `git worktree`（用 `using-git-worktrees` skill）。
- Session log 係 live append 嘅，所以 `peers` 睇到嘅係「幾秒前」嘅狀態，唔係歷史。
