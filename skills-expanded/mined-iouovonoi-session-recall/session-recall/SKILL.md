---
name: session-recall
description: Let your agent proactively recall local Copilot CLI sessions and reconnect past ideas.
allowed-tools: "powershell"
---

# Session Recall

Session Recall 會把使用者自己的 Copilot CLI session store 同步到 `~\SessionRecall`，建立可搜尋的本機索引。它適合在使用者明確要求，或目前對話和過去工作可能有具體連結時，用來找回相似 session、補充想法、產生 context pack，或輸出 memory graph。

Session Recall synchronizes the user's own Copilot CLI session store into `~\SessionRecall` and builds a searchable local index. Use it when the user explicitly asks for recall, or when the current conversation appears concretely related to past work and similar sessions could add useful context or ideas.

## 觸發時機 / Trigger

當出現以下任一情境時使用本 skill：

Use this skill in either of these cases:

1. 使用者明確要求回想、搜尋、同步或匯出過去 session。
2. 目前對話和過去工作有具體連結，回想相似 session 可能提供有用的背景、替代想法或未完成線索。

1. The user explicitly asks to recall, search, sync, or export prior sessions.
2. The current conversation has a concrete connection to past work, and similar sessions may provide useful context, alternate ideas, or unfinished threads.

- session recall、previous context、similar sessions、search memory
- 回想先前對話、查找過去 session、尋找相關上下文
- sync Copilot session、context pack、memory graph
- 同步 Copilot session、匯出 context pack、建立記憶關聯圖

可以主動觸發，但要有明確理由，例如使用者提到曾經做過的專案、延續前一次設計、想找相似解法、或目前問題可能受益於過去決策脈絡。

You may trigger it proactively, but only with a clear reason, such as a project the user worked on before, continuation of a previous design, looking for similar solutions, or a task that may benefit from prior decisions.

不要因為一般聊天、一次性的普通程式問題、或和 session history 沒有明確關係的要求而自動執行。

Do not run it for ordinary chat, one-off general coding questions, or requests with no concrete connection to session history.

## 主要指令 / Main Command

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\skills\session-recall\scripts\session-recall.ps1" sync-copilot --limit 50 --compare "<current message>" --compare-limit 5
```

## 如何使用結果 / How to Use the Result

優先看這三個欄位：

Start with these three fields:

| 欄位 / Field | 意義 / Meaning |
|---|---|
| `compare.context_used` | 是否找到高信心匹配 / Whether a high-confidence match was found |
| `compare.matched_sessions` | 可注入的相關 session / Relevant sessions suitable for context |
| `compare.candidate_sessions` | 低信心候選，只作參考 / Lower-confidence candidates for reference only |

如果 `context_used=true`，可以摘要 `matched_sessions` 中最相關的 1 到 2 筆資訊作為回覆上下文。

If `context_used=true`, summarize the top 1-2 items from `matched_sessions` as context for the response.

如果 `context_used=false`，可簡短說明目前沒有高信心相關 session。

If `context_used=false`, briefly state that no high-confidence related session was available.

## 驗證 / Validation

在作者本機索引的小型測試中，一次 report query 將建議 context 從 18,382 chars 降到 505 chars。3 筆 benchmark 得到 `hit@1 = hit@5 = 66.7%`。這些數字只代表作者本機資料，不是通用 benchmark。

In a small local validation run, one report query reduced recommended context from 18,382 chars to 505 chars. A 3-query benchmark got `hit@1 = hit@5 = 66.7%`. These numbers are from the author's local data only, not a general benchmark.

Details: `docs/validation.md`

## 安裝 / Install

如果索引不存在，先請使用者同意，然後執行：

If the index does not exist, ask for user consent first, then run:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.copilot\skills\session-recall\install.ps1"
```

## 隱私規則 / Privacy Rules

- 只讀取使用者自己的 `~\.copilot\session-store.db`。
- Read only the user's own `~\.copilot\session-store.db`.
- 預設輸出都在 `~\SessionRecall`。
- Generated data is stored under `~\SessionRecall` by default.
- 不要分享 `~\SessionRecall`、`~\.copilot\session-store.db`、`~\.copilot\session-state` 或其他 memory store。
- Do not share `~\SessionRecall`, `~\.copilot\session-store.db`, `~\.copilot\session-state`, or other memory stores.

## 更多文件 / More Documentation

| 文件 / File | 用途 / Purpose |
|---|---|
| `README.md` | 安裝與日常使用 / Install and daily use |
| `REFERENCE.md` | 完整欄位、FAQ、內部設計 / Full fields, FAQ, internals |
| `docs/validation.md` | report 與 benchmark 說明 / Report and benchmark explanation |
