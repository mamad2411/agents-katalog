# Repo Ref
- source: https://github.com/tingyulu/myr2d2 (path: skills/ai-search/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 帶引用的即時網路查證：把問題交給有網路搜尋能力的後端，要求結論先行、每個關鍵事實附來源連結、查不到就說查不到、可能過時的頁面主動標注。附單檔 POSIX shell 腳本（預設走 Codex CLI 的內建網路搜尋，可用 AI_SEARCH_CMD 換成任何會上網的後端）；偵測不到後端時明講「本次略過查證」而不是靜默跳過，也不會中斷你的流程。當使用者說「查證」「上網查一下」「即時查」「fact-c
