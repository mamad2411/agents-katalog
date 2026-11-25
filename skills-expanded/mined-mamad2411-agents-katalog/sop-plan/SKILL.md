---
name: sop-plan
description: L1 計畫模式 SOP — 強制上下文載入 + Plan Mode 評估 + 任務拆解
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# L1 計畫模式 SOP

L1 收到任務分派後，**必須依序完成以下所有步驟**，不得跳過任何 ⛔ CHECKPOINT。

## 使用方式
```
/sop-plan
```

## 執行步驟

### ⛔ STEP 1 — 載入 Sprint 計畫書
讀取當前 Sprint dev-plan：
!`ls -t proposal/sprint*-dev-plan.md 2>/dev/null | head -1`

確認並記錄：
- Sprint 目標（第 1 節）
- 技術方案（第 4 節）
- 任務清單（第 6 節）：**任務總數、各任務的指派對象、P0/P1/P2 分布、依賴關係**

> ✋ 確認已閱讀 dev-plan，整理出任務清單後再繼續。

---

### ⛔ STEP 2 — 載入踩坑紀錄
讀取：`.knowledge/postmortem-log.md`

標記出與本次任務**相關的地雷**，後續在驗收標準中必須加入對應防呆。

> ✋ 確認已列出相關地雷（或確認無相關項目）後再繼續。

---

### ⛔ STEP 3 — 載入架構文件
讀取：`.knowledge/architecture.md`（若不存在則跳過並說明）

確認：
- 系統層次與模組邊界
- 現有服務與依賴關係
- 本次任務涉及的模組範圍

> ✋ 確認架構限制已納入考量後再繼續。

---

### ⛔ STEP 4 — 複雜度評估 + Plan Mode 建議

根據前三步收集的資訊，產出評估報告：

```
📊 任務複雜度評估
─────────────────────────────
任務總數：N 個
P0 任務：N 個
跨模組依賴：N 條
最長依賴鏈：T1 → T3 → T5（N 層）
涉及模組：[列出]
postmortem 相關地雷：N 條

建議：[進入 Plan Mode ✅ / 不需要 ⚪]

建議理由：
- [說明原因，例如：有 3 條跨模組依賴、P0 任務涉及核心架構變更...]
─────────────────────────────
```

**建議進入 Plan Mode 的條件（符合任一即建議）：**
- 任務總數 ≥ 5
- 存在 P0 任務
- 跨模組依賴 ≥ 2
- 最長依賴鏈 ≥ 3 層
- postmortem 有直接相關地雷

**詢問老闆：**
> 以上是本次 Sprint 的複雜度評估。是否要進入 Plan Mode 後再開始拆解任務？
> 進入 Plan Mode 後，我會先提出完整計畫供您審核，確認後再執行。

若老闆確認進入 → 使用 `EnterPlanMode` 工具進入計畫模式
若老闆選擇跳過 → 直接進入 STEP 5

> ✋ 等待老闆決策後再繼續。

---

### ⛔ STEP 5 — 執行任務拆解
執行 `/task-delegation`（讀取 `.claude/commands/task-delegation.md` 並依步驟執行）

> ✋ 確認所有 `.tasks/sprint-{N}/` 檔案已建立後再繼續。

---

### STEP 6 — 輸出計畫摘要

```
✅ L1 計畫完成

Sprint：Sprint N
已讀文件：dev-plan ✅ | postmortem ✅ | architecture ✅
Plan Mode：[已進入 / 跳過]

已建立任務：
- T1: {名稱} → {agent} (P0)
- T2: {名稱} → {agent} (P1)
- ...

依賴關係：
T1 → T3 → T5
T2 → T4

地雷提醒：
- {相關 postmortem 條目}

下一步：通知各 L2 執行 /sop-execute {task-id}
```
