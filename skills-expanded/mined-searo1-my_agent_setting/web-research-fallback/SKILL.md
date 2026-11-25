---
name: web-research-fallback
description: 上網 research 嘅 fallback 方法 — 當 DSH 內置 web_search 工具失敗／backend 唔可用時，用 pwsh + Bing HTML 解析或者直接 fetch 目標網站。當需要上網查資料、睇 docs、搜尋文章時使用。
whenToUse: web_search 工具報錯／backend down／結果異常時先用；平時上網 research 直接用內置 web_search（已有 Exa backend）。
---

# Web Research Fallback（pwsh + Bing / 直接 fetch）

**背景**：DSH 內置 `web_search` 已有 Exa backend（free tier，見 DSH-Setup-Guide.md），實測正常 work，平時直接用好唔使 fallback。以下方法淨係喺 `web_search` 失敗／backend 唔可用時先用。

## 方法 A：Bing HTML 搜尋（pwsh）
```powershell
$q = [uri]::EscapeDataString($query)
$r = Invoke-WebRequest -Uri "https://www.bing.com/search?q=$q&count=10" -UseBasicParsing -TimeoutSec 20 -Headers @{ 'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' }
```
- 結果區塊：`<li class="b_algo">`，標題喺 `<h2><a href="...">`，snippet 喺 `<p>`
- 注意：URL 係 `bing.com/ck/a?...&u=a1aHR0...` 形式（base64 編碼喺 `u=` 參數），要 decode 先攞到真 URL；或者直接用標題+snippet 判斷
- 警告：Bing 有時會出無關結果（特別係 generic query + 特定 market 設定），要交叉驗證

## 方法 B：DuckDuckGo Lite
`https://lite.duckduckgo.com/lite/?q=...` — 快，但**好容易食 CAPTCHA**（anomaly modal），見到 `anomaly-modal` 就轉用 Bing。

## 方法 C：直接 fetch 目標網站
- Docs / 文章頁：`Invoke-WebRequest` 拎 HTML，剝走 script/style tag，用 regex 轉純文字
- 有 sitemap 嘅站（例如 docs 站）：先拎 `/sitemap.xml` 睇結構再決定 fetch 邊頁
- Mintlify 類型 docs：內容通常喺 `<main>` 入面，直接 extract

## 通用貼士
- 用 `Get-PageText` 函數模式：剝 script/style → 換 block tags 做換行 → 剝 tags → HTML decode → 壓縮空白
- 搜尋引擎結果做「發現」用，**內容以官方 docs / 原始網站為準**
- 多個查詢一次過跑，慳時間
