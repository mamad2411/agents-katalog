---
name: rsun-capture-metric
description: 交付完成後，把實際工時/成本/滿意度寫進 METRIC 單元，形成估準率校準迴圈。當用戶說「記錄這次的實際值」「回填 metric」「專案收尾 metric」「這案子花了 X 小時」「capture metric」或在 rsun-session-end 流程尾聲需要落實際數字時觸發。產出 knowledge/nodes/metrics/{target}-YYYYMMDD.md。
user-invocable: true
allowed-tools: "Bash(ls *) Bash(python3 *) Bash(grep *) Bash(cat *) Read Write Edit Glob Grep"
---

# /rsun-capture-metric — 交付後 METRIC 回填

## 為什麼

**沒有 METRIC，估價永遠停留在「直覺」階段。**

每個 CASE / MOD 做完都該留下一組真實數據：
- 實際工時 / 人月
- 實際成本
- 對比估價的 variance
- 自評滿意度
- 催生的 ADR / DEC / GOTCHA

這些數字是下次估同類 case 的 anchor，也是架構頁「估準率」趨勢的原料。

## 觸發時機（別錯過）

- 一個 CASE 交付後（客戶驗收 / 上線）
- 一個 MOD 首次生產級使用完成
- `/rsun-session-end` 判斷本 session 關閉某 milestone 時，自動提議跑這個
- 用戶說「這案子做完花了 X 小時」「這個 module 超出預估」

## 參數

`$ARGUMENTS` —
- 若有 target id（CASE-XXX / MOD-XXX / EST-XXX） → 直接鎖定
- 若空 → 讀 TRACKER 近 30 天的 CASE / MOD，列出可回填的候選，問用戶選哪個

## 執行流程

### Step 1：鎖定 target

確認 target_id（必要 — METRIC 必須指向某個可量化對象）：
- `CASE-*` — 客戶交付案
- `MOD-*` — 模組化投資
- `EST-*` — 估價單（事後對照）

如果該 target 已有 METRIC（查 `knowledge/nodes/metrics/`），問用戶：
- 要**更新**（提升 status preliminary → final）
- 還是**新增**（例如同一 case 的 3 個月後追蹤）

### Step 2：收集數據（五問五答）

和用戶確認：

| 欄位 | 問法 | 類型 |
|---|---|---|
| `actuals_hours` | 實際工時？ | 數字 |
| `actuals_mm` | 實際人月？（hours ÷ 160） | 自動算 |
| `actuals_cost` | 實際成本（NT$）？ | 數字 |
| `variance` | 對比估價差多少？（可沒有 — 填「無正式估價」） | 一句話 |
| `satisfaction` | 自評滿意度 1-10？ | 一句話 + 分數 |

若原本有 `EST-*` 估價單，讀它的 total 並自動算 variance%。

### Step 3：決定 METRIC ID

格式：`METRIC-{TARGET-UPPER}-{YYYYMMDD}`

例：
- `METRIC-CASE-RSUN-CRM-20260421`
- `METRIC-MOD-AUTH-COOKIE-20260601`

若同一天同一 target 已有 METRIC → 加尾碼 `-02`, `-03`（但這不符 regex `\d{8}$`，改成下一天）。建議直接改日期為今天。

### Step 4：寫檔

路徑：`/Users/ezonelai/Projects/TRACKER/knowledge/nodes/metrics/{case-lowercase}-{YYYYMMDD}.md`

模板：

```markdown
---
id: METRIC-{TARGET}-{YYYYMMDD}
title: {target 標題} 交付後實際值回填
type: metric
status: final           # or preliminary（還要追蹤）
metric_kind: delivery-actuals
target_id: {CASE-XXX / MOD-XXX / EST-XXX}
measured_at: {YYYY-MM-DD}
actuals_hours: {N}
actuals_mm: {N/160}
actuals_cost: {NT$}
est_hours: {若有 EST}
est_cost: {若有 EST}
variance: "實際 X hr / 估 Y hr / 差 ±Z%"
satisfaction: "N/10 — {一句話}"
date: {YYYY-MM-DD}
tags: [metric, {target slug}, actuals]
references:
  - {target id}
  - PERSON-eugene-lai
  - {若有 EST-XXX}
relations:
  - rel: measures
    target: {target id}
  - rel: calibrates       # 若回頭修正 rate-card 假設
    target: SOP-ESTIMATE-01
  - rel: recorded_by
    target: PERSON-eugene-lai
cited_by: []
---
## 關鍵數據

| 項目 | 估計 | 實際 | 差異 |
|------|------|------|------|
| 工時 | {est_hr} | {actual_hr} | {±%} |
| 人月 | {est_mm} | {actual_mm} | {±%} |
| 成本 | NT$ {est} | NT$ {actual} | {±%} |

## 發現

- {意料之外的事}
- {催生了哪些 ADR / DEC / GOTCHA}

## 對下次估價的啟示

- {未來估類似 case 時應該調整的 baseline}
- {要改哪條 rate-card 或 SOP 假設}
```

### Step 5：連動

寫檔後：

1. 在 target 單元（CASE / MOD）的 frontmatter 加上 `metrics: [METRIC-...-YYYYMMDD]`（若還沒有）
2. `python3 scripts/validate-citations.py` 確認 ID pattern 通過
3. `python3 scripts/build-knowledge.py` 重建 citation-index
4. 若有 `EST-*` 估價，提議用戶建立 `DEC-ESTIMATE-XXX` 記錄校準決定（例：「下次估 CRM 類案把 activity 模組從 M 降到 S」）

### Step 6：回報

告訴用戶：
- METRIC ID 與路徑
- variance%（如果有估價對照）
- 本次最大的「意外」是什麼
- 建議下次估類似案時要調整什麼

## 原則

- **不要**用未驗證的數字 — 寧可讓用戶明確講「大約 X 小時」也不自己估
- **variance 必填** — 即使是「無正式估價」也要寫，這本身就是資訊（下次要補 EST）
- **satisfaction 必填** — 純主觀沒關係，趨勢才重要
- **建議升格 MOD** — 若發現某功能是可複用模組（做了 > 1 次），提議用戶寫 MOD-XXX
