---
name: rsun-capture-dec
description: 把對話中剛做出的決定落地成 DEC 引用單元。當用戶說「記下這個決定」「存成 DEC」「這個決定要記下」「capture dec」「reflex dec」或對話出現「那就這樣決定」「先 A 再說」「採用 X 方案」等關鍵句時觸發。產出 knowledge/nodes/decisions/DEC-{AREA}-{XXX}.md 並補上 frontmatter、references、relations。
user-invocable: true
allowed-tools: "Bash(ls *) Bash(python3 *) Bash(grep *) Bash(cat *) Read Write Edit Glob Grep"
---

# /rsun-capture-dec — 決策反射（Decision Reflex）

## 為什麼

你每天在對話中做 10+ 個小決定，但 95% 都飛走了。這個 skill 讓決定即時落地成
可被下次 session 引用的 `DEC-*` 單元。比 ADR 輕量（不用三選一 + 利弊表），
但比隨口說還強（有 id、有日期、有 references、有 cited_by）。

**ADR vs DEC 的分界**：
- **ADR**：影響多個模組的架構決策，需要正式 decision record（例：ADR-001 用 CF Workers）
- **DEC**：單一場景的戰術決定（例：這份估價要用 1.8x 毛利；這個客戶先做 MVP；這個 module 改用 V2 schema）

## 參數

`$ARGUMENTS` —
- 若有文字 → 當成決策標題/內容（例：「報價給 Apex Gold 走 1.8x 毛利」）
- 若空 → 從最近對話推導（讀最近 10 輪對話的關鍵句）

## 執行流程

### Step 1：確認決策內容

和用戶確認 5 項（若用戶 `$ARGUMENTS` 已明確提供，則直接往下；不要過度追問）：

| 欄位 | 說明 | 範例 |
|---|---|---|
| **title** | 一句話 | "Apex Gold 報價用 1.8x 毛利" |
| **area** | 所屬領域 | CRM / ESTIMATE / DEPLOY / DESIGN / CLIENT / ... |
| **decision** | 決定是什麼（1-2 句） | "毛利倍數從 2.0x 降到 1.8x，換取成交率" |
| **rationale** | 為什麼（1-2 句） | "Apex Gold 預算卡在 200k，降 10% 讓他們更容易點頭" |
| **references** | 相關單元 ID | CASE-APEX-GOLD-PROPOSAL / SOP-ESTIMATE-01 |

### Step 2：決定 DEC ID

ID 格式：`DEC-{AREA}-{NNN}`（AREA 大寫，NNN 三位數遞增）

```bash
# 找該 area 現有最大編號
ls /Users/ezonelai/Projects/TRACKER/knowledge/nodes/decisions/ | grep -i "DEC-{AREA}-" | sort | tail -1
```

若無任何 DEC 於該 area，則從 001 開始。

### Step 3：寫檔

路徑：`/Users/ezonelai/Projects/TRACKER/knowledge/nodes/decisions/dec-{area-lowercase}-{nnn}.md`

模板：

```markdown
---
id: DEC-{AREA}-{NNN}
title: {一句話決策}
type: dec
status: accepted
date: {YYYY-MM-DD}
decider: PERSON-eugene-lai
area: {crm|estimate|deploy|design|client|...}
scope_case: {CASE-XXX 若適用}
scope_module: {MOD-XXX 若適用}
tags: [dec, {area}, {額外 tag}]
references:
  - PERSON-eugene-lai
  - {相關 ADR / CASE / SOP / MOD id}
relations:
  - rel: decided_by
    target: PERSON-eugene-lai
  - rel: applies_in        # 若鎖定某 case
    target: {CASE-XXX}
  - rel: refines           # 若是對某 ADR 的戰術落地
    target: {ADR-XXX}
cited_by: []
---
## 決策

{一段話：決定是什麼}

## 為什麼

{一段話：rationale + constraint}

## 影響範圍

- {哪些 module / case / 人會受影響}

## 後續追蹤

- [ ] {若有需驗證的假設或 metric}
```

### Step 4：重跑 validator + build

```bash
cd /Users/ezonelai/Projects/TRACKER
python3 scripts/validate-citations.py
python3 scripts/build-knowledge.py
```

確認：
- ✅ all citations valid
- DEC 類計數 +1

### Step 5：回報

告訴用戶：
- DEC ID 與檔案路徑
- 該 DEC 的 references 自動連到哪些已存在的單元
- 若發現 references 裡的 id 不存在 → 提醒用戶（可能打錯或該單元還沒建立）

## 原則

- **不要**替用戶做太主觀的判斷 — 讓用戶明確說「就記這個」再寫
- **不要**在對話裡冒出就自動寫 — 要等明確觸發語句
- 快就是王道：整個流程應該 3-5 次 tool call 結束
- 若 area 真的沒法歸類，用 `MISC` 或問用戶
- **DEC 是戰術，ADR 是戰略** — 發現內容其實該是 ADR（多選項比較、長期影響），主動建議升格成 ADR-XXX
