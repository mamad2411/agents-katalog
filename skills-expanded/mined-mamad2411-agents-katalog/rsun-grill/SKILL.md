---
name: rsun-grill
description: Alignment phase — 開工前先狠 grill user，揪出 misalignment。觸發詞：「grill me」「grill 我」「拷問我」「先確認」「對齊一下」「客戶需求書讀了嗎」。沿襲 mattpocock/skills/productivity/grill-me + 容晟客戶情境特化。**客戶 deliverable 第一動作必跑此 skill**。
user-invocable: true
---

# /rsun-grill — 容晟強制 alignment phase

## 為什麼這個 skill

**真實事件**：2026-04-26 Apex Gold 案誤判為 ESG 諮詢業，Zenya 寫 3 個 ESG variant 後才發現是房產 listing 平台 → **重寫 3 variants 浪費 200+ hr**。

根因：Zenya 沒先 grill user 跟讀客戶需求書 → 直接動手。

`/rsun-grill` 強制 alignment phase 在動手前。

## 何時必跑

- ✅ **客戶 deliverable 第一個 commit 前**（強制）
- ✅ 跨 repo 任務（同時動 ≥ 2 repos）
- ✅ 重構 ≥ 5 檔
- ✅ 觸碰 production secrets / DB schema migration
- ✅ user 說「grill me」「拷問」「先對齊」
- ❌ 單檔 < 50 行 bug fix 不需要
- ❌ 純文檔 / 註釋更新不需要
- ❌ monitoring / status check 不需要

## 執行步驟

### Step 0 — 識別 Paradigm（**Apex Gold 失敗 lesson 後新加 2026-05-02**）

**強制問**：「客戶 demo 時最想看到什麼？」

| 答案 | Paradigm | 主軸 |
|---|---|---|
| 「**好用的後台**讓我自己改」 | A: CMS-driven | 編輯體驗 + 媒體管理 + SEO |
| 「**完整的功能流程**自動跑」 | B: SaaS-functional | domain logic + workflow + integration |
| 「**多系統串通**沒漏資料」 | C: Process-orchestration | webhook + queue + sync |

**容晟預設思維是 B**。看到客戶要 A 或 C → **主動校正**，不要硬塞 B 方案。

詳細決定原則見 [DEC-CLIENT-PARADIGM-001](../../../Projects/TRACKER/knowledge/nodes/decisions/DEC-CLIENT-PARADIGM-001.md)。

### Step 1 — 讀客戶需求書 / 對話歷史

若 user 提到客戶名（apex / horizen / 房產 / esg / wismath ...）：
1. 先讀 `~/Projects/TRACKER/knowledge/nodes/clients/{client}.md`
2. 若有 form URL（如 https://rsun.me/api/forms/view/xxx）→ 用 WebFetch 抓
3. 萃取 3 關鍵詞：**domain / scale / 期望時程**

若無客戶名 → 直接 Step 1.5。

### Step 1.5 — 查 past runs + 相關 ADR / DEC（**2026-05-10 加 — combined_search wire**）

開工前必查「這個任務以前做過嗎？哪些 doctrine 適用？」用 MCP tool `combined_search`：

```
mcp__rsun-citation__combined_search({
  task_summary: "<本次任務一句話>",
  top_k_runs: 3,
  top_k_knowledge: 5,
})
```

回傳:
- `runs[]` — 過去 sub-agent 跑過類似任務的紀錄（cosine + lexical via agent_memory）
- `knowledge[]` — 相關 ADR / DEC / METRIC chunks（bge-m3 cosine via citation）
- `ranked[]` — 兩者依 score desc 合一

**處理結果**：
- 若 `runs` 有舊紀錄：看 outcome 是否 success / 學到什麼 → 避免重蹈覆轍
- 若 `knowledge` 命中 ADR：必讀，**主動跟 user 提**「ADR-XXX 已決定 Y，這次也走 Y 對嗎？」
- 若兩邊都空：純新題目，照常 grill

不查就動手 = 重複犯錯。

### Step 2 — 對齊 contingency profile

讀 `~/Projects/TRACKER/knowledge/architecture/contingency-matrix.md` 4 個 client profile：
- apex-gold-realestate（強稽核 / 強多租 / ESG 法遵）
- rsun-dashboard-internal（速度優先 / 弱多租 / SMB）
- legal-single-tenant（強加密 / 單租部署 / 律所）
- fortune-teller-d2c（edge cache / 高並發 / D2C）

跟 user 顯式確認：「我讀到客戶 3 大需求是 X / Y / Z，對齊 profile A，對嗎？」

### Step 3 — Relentless 拷問

借 mattpocock /grill-me 精神：

> Interview user relentlessly about every aspect of this plan until 達成 shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer. Ask the questions one at a time, waiting for feedback on each question before continuing.

問題類型：
- **範圍**：「這次只做 X 對嗎？Y 算 out of scope 嗎？」
- **約束**：「customer 預算 / 時程 / 技術棧 / 必要 vs 加分？」
- **成功定義**：「完成的 acceptance criteria 是什麼？怎麼算 done？」
- **隱性假設**：「我假設 X，但若 Y 則需要 Z — 哪個對？」
- **Edge case**：「如果客戶要 W 怎麼辦？提早設計還是事後加？」

**每次只問一個問題**，等回答再進下一個。**對 user 答案有疑慮就再追**。

### Step 4 — 寫 alignment summary

拷問完寫一段 100-200 字 summary：
```markdown
## Alignment Summary（{date}）

**任務**：...
**Profile 對齊**：...
**Past runs 參考**：（Step 1.5 combined_search 命中的 run_id 列表，無則「無」）
**ADR 對齊**：（Step 1.5 命中的 ADR-XXX 列表 + 各自怎麼適用）
**範圍**（in / out）：...
**約束**：...
**成功定義**：...
**已確認假設**：...
**留 TODO 給後續釐清**：...
```

存進 `data/grill-summary-{slug}-{date}.md` 或直接寫進當前 task 的 PRD。

### Step 5 — Get user OK 才動手

最後一句：「以上對齊 OK 嗎？OK 就動手。」

User 說 OK → 開始實作。

User 說有要改 → 回 Step 3 再 grill。

## 紅線

- ❌ **不准**沒讀客戶需求書就動手寫客戶 variant
- ❌ **不准**跳 Step 1.5 — past runs + ADR 沒查就動手 = 重複犯錯
- ❌ **不准**一口氣問 5 個問題（壓力大 user 答不完）
- ❌ **不准**自己 assume 客戶意圖（直接問）
- ✅ 拷問可以挑釁（"你說的 X 跟 Y 衝突，哪個是真的？"）
- ✅ 拷問可以提推薦答案（"我建議 A 因為 ...，可以嗎？"）

## 特別適用容晟情境

- 客戶開新案子第一次 session（Phase 0）
- /rsun-architect [cat] 開始前
- /rsun-estimate 開始前
- 任何 cross-repo orchestration 開始前
- 派 Sonnet sub-agent 寫客戶 deliverable 前

對齊 CLAUDE.md Anti-Pattern F「跳過讀客戶需求書」+ Zenya 派 Sonnet SOP D 段。
