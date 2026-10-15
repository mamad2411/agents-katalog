---
name: ito-search
description: 處理所有外部查詢需求，包含套件用法與 API、錯誤訊息、GitHub issue/PR、方法論與一般知識。以「幫忙查」、「搜尋一下」等自然語觸發，或明確呼叫 `/ito-search`。不適用於 codebase 搜尋、需直接實作的任務、需存檔的調研任務。
---

# ito-search

## 概覽

提供多種外部搜尋工具，由 agent 依 query 自行挑選合適工具（單用、並用或平行）。結果經劣質網域黑名單過濾後，依輸出原則回覆。整個流程為一次性查詢，不存檔。

## 使用時機

- 使用者明確呼叫 `/ito-search`
- 使用者以自然語觸發外部資訊查詢：「幫我查⋯」「搜尋一下⋯」「找一下⋯」「XXX 怎麼用」「XXX 是什麼」

**不應使用的情況：** 任何 codebase 搜尋，需要直接實作、修改檔案、跑測試的任務，需產出研究報告或需存檔的調研任務。

## 核心流程

### 步驟 1：依 query 自選工具

從下列工具清單擇一或擇數使用，query 明確橫跨兩個以上工具分類時平行執行對應工具，否則序列執行。執行至各工具回傳結果為止。

#### 工具 A：找官方文件（/find-docs skill，context7 MCP 備援）

- 用途：查 lib/framework/SDK/CLI 的官方 API、syntax、code snippet、設定與版本特定資訊
- 區分訊號：query 含具體 lib 名稱與「怎麼用」「API」「語法」「snippet」「設定」等實作詞
- 執行順序：
  1. 呼叫 `/find-docs` skill 執行查詢
  2. `/find-docs` 失敗（任何原因，包含 quota/auth fail）時，忽略 find-docs 的錯誤處理邏輯，改用 context7 MCP 執行相同查詢

#### 工具 B：deepwiki（MCP）

- 用途：查 GitHub repo 內部運作、架構問答、為何如此設計
- 區分訊號：query 含具體 GitHub `owner/repo` 與「怎麼運作」「為什麼這樣設計」「架構」等問答詞；非 SDK/lib 名稱（後者改用工具 A）

#### 工具 C：exa（MCP）

- 用途：bug 訊息/社群討論、best practice/方法論/架構、非技術一般知識
- 區分訊號：query 為錯誤訊息、抽象方法論詞（best practice/pattern/architecture）、或非技術問題

#### 工具 D：gh（CLI）

- 用途：追蹤 GitHub issue/PR/release/action、社群討論
- 區分訊號：query 含 repo 名與 issue/PR 編號或具體議題關鍵字

#### Fallback：harness 內建搜尋工具

上述所有工具失敗或回傳零結果時，靜默改用 harness 內建 `WebSearch`/`WebFetch`，不告知使用者工具切換。

### 步驟 2：過濾結果

讀取 `references/source-filter.md` 以取得黑名單清單，對所有結果 URL 做 substring match，命中黑名單者整筆剔除。

### 步驟 3：依輸出原則回覆

格式由 agent 依 query 性質自決：

- **簡單 query**（一句話可答）：直接回答，末段附「來源」區塊，列出可點擊 URL 清單
- **複雜/資訊豐富 query**：TL;DR 段（一至三句核心摘要）、說明段（展開細節，可含 code block）、末段「來源」區塊

## 常見合理化藉口

| 合理化藉口 | 實際情況 |
|---|---|
| 「/find-docs 失敗，直接跳 exa 搜就好」 | /find-docs 失敗要先 fallback 到 context7 MCP，不是跳過工具 A 整個分支 |
| 「query 很短，跳過工具選擇直接 exa 搜就好」 | 短 query 可能是 API 語法問題，跳過工具選擇讓文件命中率大幅下降 |
| 「結果過濾後沒幾筆，補幾筆黑名單域名的結果」 | 過濾後結果少時應靜默 fallback WebSearch，不放行黑名單域名 |
| 「使用者沒說要附來源，可省略來源區塊」 | 來源區塊是輸出契約，供使用者驗證，不可省略 |

## 警訊

- 輸出缺少「來源」區塊
- 結果含黑名單域名（如 `csdn.net`、`w3schools.com`）未過濾
- `/find-docs` 失敗後未嘗試 context7 MCP 直接跳至下一工具
- 複雜 query 無 摘要 直接展開大段說明

## 驗證

- [ ] 結果經 `references/source-filter.md` 黑名單過濾，輸出無命中域名
- [ ] 輸出含「來源」區塊與可點擊 URL 清單
- [ ] 未建立任何檔案（不存檔）
- [ ] `/find-docs` 失敗時已嘗試 context7 MCP fallback

## 錯誤處理

- **工具 A 失敗**（/find-docs quota/auth fail 或任何錯誤）：忽略 find-docs 錯誤邏輯，靜默改用 context7 MCP
- **其他工具失敗**（quota/auth fail/零結果）：靜默 fallback 至下一個合理工具
- **所有工具失敗**：靜默改用 harness 內建 `WebSearch`/`WebFetch`，不中斷回覆
- **使用者要求 codebase 搜尋**：明確告知本 skill 不負責 codebase 範圍

## 延伸參考

- `references/source-filter.md`：劣質網域黑名單清單
- `/find-docs` skill：ctx7 CLI 的兩步驟用法（library → docs）
- `context7` MCP：`/find-docs` CLI 失敗時的備援，提供相同文件查詢能力
- `exa` MCP：網路搜尋、網頁爬取與深度研究
- `deepwiki` MCP：GitHub repo AI 生成文件，可直接問答架構與設計
