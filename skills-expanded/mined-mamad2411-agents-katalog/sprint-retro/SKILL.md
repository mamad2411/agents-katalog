---
name: sprint-retro
description: Generate sprint retrospective by analyzing section 10 data
allowed-tools: Read, Write, Glob, Grep
---

# Sprint 回顧

自動帶入第 10 節數據，產出回顧報告。

## 使用方式
```
/sprint-retro <sprint-number>
```

## 參數
- `$0`: Sprint 編號

## 執行步驟

1. 讀取 dev-plan 第 10 節：
!`cat proposal/sprint$0-dev-plan.md 2>/dev/null | grep -A 100 "任務與審核紀錄"`

2. 讀取提案書驗收標準：
!`cat proposal/sprint$0-proposal.md 2>/dev/null | grep -A 30 "驗收標準"`

3. 分析並產出回顧：
   - **完成狀況**：任務完成率、準時率
   - **品質指標**：Review 通過率、Gate 通過率
   - **時程分析**：預估 vs 實際
   - **做得好的**：值得延續的做法
   - **需改進的**：下次 Sprint 要注意的
   - **行動項目**：具體改善措施

4. 寫入 `proposal/sprint$0-retro.md`
