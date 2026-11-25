---
name: handoff
description: 壓縮當前對話成交接文檔，讓下一個 session 的 Agent 可以無縫接續。說「交接」「handoff」「存檔給下個 session」時觸發。
argument-hint: 下個 session 會用來做什麼？
---

把當前對話總結成交接文檔，讓新的 Agent 可以接續工作。存到 `.claude/agent-memory/ceo/` 目錄下。

列出下個 session 建議使用的 skills。

不要重複已經存在於其他文件（PRD、CONTEXT.md、commit、diff）的內容 — 引用路徑或 URL 即可。

如果用戶傳了參數，將其視為下個 session 的重點描述，據此調整文檔。
