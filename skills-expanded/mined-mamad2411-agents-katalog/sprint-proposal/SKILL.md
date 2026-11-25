---
name: sprint-proposal
description: Generate a sprint proposal document with scope, risks, and G0 checklist
allowed-tools: Read, Write, Glob, Grep
---

# Sprint 提案書產生器

根據需求討論產出標準化的 Sprint 提案書。

## 使用方式
```
/sprint-proposal <sprint-number> <project-name>
```

## 參數
- `$0`: Sprint 編號（如 `2`）
- `$1`: 專案名稱（如 `AgentHub`）

## 執行步驟

1. 讀取提案書範本：
   使用 Read tool 讀取 `.knowledge/templates/sprint-proposal.md.template`。
   若檔案不存在，略過此步驟，改用預設格式。

2. 讀取現有提案書參考格式：
   使用 Glob tool 搜尋 `proposal/sprint*-proposal.md`，取最後一個（編號最大），用 Read tool 讀取前 30 行。
   若無既有提案書，略過此步驟。

3. 產出 `proposal/sprint$0-proposal.md`，包含：
   - 目標（1-2 句話）
   - 範圍定義（做/不做）
   - 流程決策（步驟勾選 + 關卡）
   - 團隊分配
   - 風險評估
   - 驗收標準
   - G0 審核區塊（空白待填）

## 產出格式
嚴格遵循 `.knowledge/templates/sprint-proposal.md.template` 的結構。
若範本不存在，遵循 `proposal/` 下既有提案書的格式。
