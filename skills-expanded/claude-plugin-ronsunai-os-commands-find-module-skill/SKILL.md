---
name: find-module
description: 在寫新功能前，先查 rsun 模組庫是否有現成方案。當用戶說「找模組」「有沒有現成的」「先查模組庫」「pre-flight」「find module」或任何新功能開始前（email、auth、payment、storage、cms、crm 等常見需求）自動觸發。
user-invocable: true
allowed-tools: "Bash(python3 /Users/ezonelai/Projects/TRACKER/scripts/mcp_rsun_modules.py *) Read"
---

# /find-module — 模組庫 pre-flight 查詢

## 精神

**寫 code 前先查有沒有現成的。**

容晟科技累積了 10 個生產級模組（`~/Projects/modules/`）+ 95 個候選模組（從 package.json 收割而來）。 在寫任何新功能前：

1. **先問：有沒有現成模組？** — 用關鍵字查 `search_modules`
2. **若有 production 模組** → 直接套用，讀 `gotchas` + `decision_notes` 避坑
3. **若只有 candidate 模組** → 參考它的 `usage_count` 與 `verified_in`，評估風險
4. **若無** → 才開始寫新 code，完成後考慮是否沉澱為新模組
5. **完成套用後**：呼叫 `record_usage` 記錄結果（success/failed + 新坑）

## 參數

`$ARGUMENTS` — 關鍵字（email / auth / payment...）或完整描述（例：「想要在 Next.js 加 JWT 登入」）。

## 執行流程

### Step 1：取得分類總覽（第一次使用時）

透過 MCP 工具 `rsun-modules` → `list_categories`，了解目前有哪些分類。

### Step 2：關鍵字搜尋

透過 `search_modules`，帶入：
- `query`: 從 `$ARGUMENTS` 抽取核心關鍵字
- `stack`: 目前專案的技術棧（通常是 `["nextjs", "vercel"]`）
- `status`: 優先 `production`；若無結果再查 `candidate`
- `limit`: 5

### Step 3：讀取最相關模組的完整資料

對排名第 1 的結果呼叫 `get_module`，取得：
- `gotchas` — 過去踩過的坑，必讀
- `decision_notes` — 為什麼選這個（vs 替代方案）
- `env_required` — 需要哪些環境變數
- `depends_on` / `works_with` — 是否需要搭配其他模組
- `body` — 完整操作步驟

### Step 4：呈現決策建議

輸出格式（給用戶決策）：

```
📦 模組查詢結果：<query>

【最相關】<module_id>（status=production, maturity=0.9）
  ✓ 已在 <verified_in> 驗證
  💡 決策：<decision_notes>
  ⚠️  踩過的坑：
     - <gotcha 1>
     - <gotcha 2>
  🔑 需要環境變數：<env_required>
  🧩 搭配：<works_with>

【替代方案】<alternative_to>

【建議】
  直接套用此模組 → 預期 1 小時內完成
  步驟：讀 `<source_path>` 的完整 body
```

### Step 5（套用後）：記錄結果

完成套用後，呼叫 `record_usage`：

```
record_usage({
  module_id: "email-resend",
  project: "apex-gold",
  outcome: "success",         # 或 partial / failed / rejected
  new_gotcha: "ESM import 要加 .js 副檔名"  # 選填
})
```

這會 append 到 `~/Projects/modules/_usage_log.jsonl`，累積使用證據 —  下次別人（或你自己）搜尋時就能看到這個 outcome。

## 沒有找到怎麼辦？

1. 放寬條件：去掉 `stack` 或 `category` 再查一次
2. 若仍無，查 `candidate/`（`status: "candidate"`）：可能是 package.json 中已出現但未沉澱的套件
3. 若 candidate 中有但尚未驗證 → 先小規模試，成功後手動升級為 production module（移出 `candidates/`，補 frontmatter `maturity`、`decision_notes`、`gotchas`）

## 為什麼重要？

- **避免重複造輪子**：10 個 production 模組 = 10 次踩坑經驗
- **避免重複踩坑**：`gotchas` 欄位是血淚累積
- **形成飛輪**：每次 `record_usage` → 下次決策更準 → 套用更快

> 這是「拼裝式開發」的第一步：先拼，不得已才寫。
