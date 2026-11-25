---
name: gate-record
description: Record a gate review decision in the dev plan section 10
allowed-tools: Read, Edit, Glob
---

# Gate 審核紀錄

在開發計畫書第 10 節附加 Gate 審核紀錄。

## 使用方式
```
/gate-record <gate-type> <decision> [comment]
```

## 參數
- `$0`: Gate 類型（G0 / G1 / G2 / G3 / G4 / G5 / G6）
- `$1`: 決策（見下方格式規範）
- `$ARGUMENTS`: 完整參數（含審核意見）

## 格式規範（系統解析依賴，務必遵守）

### Gate 類型（第 1 欄）
必須為：`G0` / `G1` / `G2` / `G3` / `G4` / `G5` / `G6`

### 決策（第 3 欄）— 嚴格使用以下純文字值

| 決策值 | 對應系統狀態 | 說明 |
|--------|-------------|------|
| `✅ 通過` | approved | 審核通過 |
| `❌ 駁回` | rejected | 審核不通過 |
| `⚠️ 附條件通過` | approved | 有條件通過 |

> **禁止**使用其他格式（如純文字「通過」、英文「approved」）。
> 系統解析器 `decisionToStatus()` 依賴上述關鍵字判斷狀態。

### 日期（第 2 欄）
格式：`YYYY-MM-DD`（如 `2026-03-26`）

### 審核意見（第 4 欄）
自由文字，簡述審核理由。

## 執行步驟

1. 找到當前 Sprint 的 dev-plan：
   使用 Glob tool 搜尋 `proposal/sprint*-dev-plan.md`，取最新的檔案路徑。

2. 讀取 dev-plan 找到第 10 節的 Gate 紀錄表：
   使用 Read tool 讀取上述 dev-plan 完整內容，找到 `Gate 紀錄` 表格區段。

3. 找到對應的 Gate 行（如 `| G0 |`），**更新該行**而非新增：
   - 如果該行已有資料（日期/決策非空），直接覆蓋
   - 如果該行是空的（`| G0 | | | |`），填入資料
```
| $0 | {YYYY-MM-DD} | {決策值} | {審核意見} |
```

4. 使用 Edit 工具精確替換該行，不改動其他內容。

## 範例

```
| G0 | 2026-03-26 | ✅ 通過 | 老闆確認需求，提案通過 |
| G1 | 2026-03-27 | ❌ 駁回 | 圖稿缺少手機版響應式設計 |
| G2 | 2026-03-28 | ✅ 通過 | 程式碼品質合格 |
```
