---
name: pm-review
description: PM reviews gate submission with 6-item checklist and recommendation
allowed-tools: Read, Edit, Glob, Grep
---

# PM Gate 審核

PM 審核 L1 提交的 Gate 回報，執行 6 項 checklist。

## 使用方式
```
/pm-review <gate-type>
```

## 參數
- `$0`: Gate 類型（G2 / G3 / G4）

## 6 項 Checklist

| # | 檢查項 | 說明 |
|---|--------|------|
| 1 | 交付物完整性 | Gate 要求的所有交付物是否齊全 |
| 2 | 數據正確性 | 報告中的數字是否與實際一致 |
| 3 | 驗收標準對照 | 逐項比對提案書/計畫書的驗收標準 |
| 4 | 流程合規 | 阻斷規則是否遵守、前置 Gate 是否已通過 |
| 5 | 計畫書紀錄 | 開發計畫書第 10 節是否已填寫 |
| 6 | 附帶問題 | 過程中發現的問題是否已記錄 |

## 執行步驟

1. 讀取當前 dev-plan：
   使用 Glob tool 搜尋 `proposal/sprint*-dev-plan.md`，取最新的，用 Read tool 讀取完整內容。

2. 讀取提案書：
   使用 Glob tool 搜尋 `proposal/sprint*-proposal.md`，取最新的，用 Read tool 讀取完整內容。

3. 逐項執行 6 項 checklist
4. 產出 PM 建議（供老闆決策時參考，不直接寫入 Gate 紀錄）：
   - **通過** — 建議老闆核准
   - **駁回** — 建議老闆退回
   - **附條件通過** — 建議老闆附條件核准
5. 整理摘要報告供老闆決策

> **注意**：PM 審核結果不直接寫入 dev-plan 第 10 節 Gate 紀錄。
> Gate 紀錄由老闆決策後透過 `/gate-record` 寫入，格式必須遵守 gate-record skill 的規範：
> `| G{N} | YYYY-MM-DD | ✅ 通過 / ❌ 駁回 / ⚠️ 附條件通過 | 審核意見 |`
