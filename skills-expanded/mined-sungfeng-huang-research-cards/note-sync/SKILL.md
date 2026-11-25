---
name: note-sync
description: "ONE entry point for the note-surface STAR: local (plain .md) is always the hub, every enabled surface (Heptabase, HackMD, …) syncs over its own local↔surface segment per the config backends list (first = canonical). Converges HackMD write-backs onto Heptabase in the same run and aggregates all segments' conflicts into one report. --mode heptabase|hackmd runs a single segment (obsidian is the accepted legacy alias). Use when the user asks to sync notes / sync everything / 同步筆記、全部同步、跑同步、note sync、把三方筆記收斂, or any request naming the legacy obsidian-sync / hackmd-sync engines."
---

# note-sync — 筆記面同步的單一入口

拓撲是**星狀**：local（純 .md 資料底座）恆為中樞，每個啟用的筆記面
各有一段 local ↔ 面 的雙向同步；`backends` 只決定啟用哪些面＋首位＝
正本。list 沒寫 `"local"` 而有其他面時，中樞會**隱式注入**（store 預設
`~/.local/share/research-cards/store`——使用者不用碰它，但 write-back
的安全著陸點與純文字資料底座恆在）：

```
Heptabase ◀─（heptabase 段）─▶ local ◀─（hackmd 段）─▶ HackMD
```

| 段（--mode） | 引擎 | 需要 |
|---|---|---|
| `heptabase`（舊名 `obsidian` 仍相容） | `skills/heptabase-sync/sync.py`——區塊級 level-2 雙向 | `backends` 含 `"heptabase"` |
| `hackmd` | `skills/hackmd-sync/sync.py`——段落級 write-back、宣告式權限、Book 目錄 | `backends` 含 `"hackmd"` |
| 反向模式：`backends: ["local", "heptabase"]`（local 正本、Heptabase＝可重建視圖） | 同一 heptabase 段引擎——刪 .md 正本→Heptabase 卡自動 trash；Heptabase 端移卡→解除綁定、下輪 adoption 重建 | `backends` 首位＝`"local"` |

## 日常

| 你說 | 指令 |
|---|---|
| 「同步筆記」「全部同步」 | `python3 <此 skill 目錄>/sync.py` |
| 「只同步到 HackMD」 | `python3 <…>/sync.py --mode hackmd` |
| 「只跑 Heptabase↔local」 | `python3 <…>/sync.py --mode heptabase` |
| 「先看會動哪些」 | `python3 <…>/sync.py --dry-run` |

全鏈執行順序＝由正本向外（heptabase 段 → hackmd 段）；若 hackmd 段有 write-back
落進 local，**同一次呼叫自動補跑一次 heptabase 段**把它送回 Heptabase——
不用你記得跑第二次。

輸出：一份彙總 JSON——`plan`（實際跑的段）、`segments`（各段完整報告）、
`total_conflicts`＋`conflicts`（跨段衝突總覽，agent 跑完攤給使用者）。

## 邊界

- 各段的細節語義（衝突規則、write-back 信任邊界、權限宣告、Book 目錄、
  限流退避）都在各引擎（`skills/heptabase-sync/`、`skills/hackmd-sync/`）
  的 SKILL.md／wiki——note-sync 只做編排，不改語義。
- 單段引擎仍可直接執行（cron 相容；hackmd 段的 state 鎖防止與
  note-sync 併發互踩）。
- 觸發時機：手動／agent 呼叫，無獨立自動排程——想掛 cron 就對本 skill
  的 `sync.py` 掛一條即可（一條就涵蓋全鏈）。例外是啟用 cluster
  project-log handoff 時，Mac 的 `project-card-log/post_log_sync.py` 會在
  repair 後對整批事件呼叫一次本入口，再刷新 canvas。
