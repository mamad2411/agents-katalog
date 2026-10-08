---
name: sop-execute
description: L2 任務執行 SOP — 強制規範載入 + 驗收確認，不得跳過任何 checkpoint
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# L2 任務執行 SOP

L2 執行任務時，**必須依序完成以下所有步驟**，不得跳過任何 ⛔ CHECKPOINT。

## 使用方式
```
/sop-execute <task-id>
```

## 參數
- `$0`: 任務 ID（如 `T3`）

## 執行步驟

### STEP 1 — 標記任務開始
執行 `/task-start $0`（讀取 `.claude/commands/task-start.md` 並依步驟執行）

---

### ⛔ STEP 2 — 載入任務規格
找到任務檔案：
!`find .tasks -name "$0-*" -o -name "$0.*" 2>/dev/null | head -1`

確認並記錄：
- 任務描述
- 指派對象確認（確認是本 Agent 的任務）
- 依賴任務（確認依賴項目均已 `done`，否則回報 blocked）
- 驗收標準（逐項列出 `- [ ]` 清單）

> ✋ 確認任務規格清楚、依賴已解除後再繼續。若依賴未完成，執行 `/task-status $0 blocked 等待 {依賴任務} 完成` 並停止。

---

### ⛔ STEP 3 — 載入對應規範

讀取 `.knowledge/company-rules.md`

依任務類型讀取對應規範：

| 任務類型 | 必讀規範 |
|---------|---------|
| 後端 / API | `.knowledge/specs/api-design.md` + `.knowledge/specs/data-model.md` |
| 前端 / UI | `.knowledge/specs/feature-spec.md` |
| 全端 | 以上全部 |
| 不確定 | 全部讀取 |

讀取 `.knowledge/postmortem-log.md`，找出與本次任務相關的地雷條目。

輸出：
```
📋 規範載入完成
- company-rules ✅
- [對應規範] ✅
- postmortem 相關地雷：[列出，或「無」]

本次任務需特別注意：
- [從規範中提取與任務直接相關的限制條目]
```

> ✋ 確認規範已讀、相關限制已列出後再繼續。

---

### STEP 4 — 實作

依規範實作。過程中：

- **遇到阻塞**（技術問題、依賴未就緒、需求不明）：
  執行 `/task-status $0 blocked {具體原因}`，回報 L1 後停止等待

- **需要變更規範範圍外的內容**：
  先回報 L1，不得擅自修改規範文件或驗收標準

---

### ⛔ STEP 5 — 自我驗收

逐項確認任務檔案中 `## 驗收標準` 的每個 `- [ ]`：

- 已完成 → 標記為 `- [x]`
- 無法確認 → 在備註中說明，不可跳過

> ✋ **所有驗收標準必須打勾或有說明後才可繼續。** 若有未完成項目，返回 STEP 4 繼續實作。

---

### STEP 6 — 提交審查
執行 `/task-done $0 {完成備註}`（讀取 `.claude/commands/task-done.md` 並依步驟執行）

---

### STEP 7 — 輸出摘要

```
✅ $0 執行完成，已提交 L1 審查

驗收標準：全部通過 ✅
規範對照：完成 ✅
地雷防呆：[已處理 / 無相關]

等待 L1 執行 /sop-review $0
```
