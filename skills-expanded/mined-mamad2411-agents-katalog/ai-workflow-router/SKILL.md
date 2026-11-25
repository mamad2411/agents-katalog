---
name: ai-workflow-router
description: 依任務複雜度、上下文壓力與目前 AI agent 能力，建議最小工作流、context mode、技能搭配及提示詞；僅在要求規劃或長任務可能過載時使用。
---

# AI Workflow Router

這是工作流建議器，不是自動執行器。它以「任務複雜度 × 上下文壓力 × agent 可用機制」選擇最小可行流程，避免小任務被過度規劃，也避免長任務因 context 污染而失去一致性。

## 使用原則

- 只在使用者要求工作流／技能搭配，或長任務確有規劃與 context 管理價值時使用。
- 只提供建議；不要自動要求分級、執行技能、建立子代理或套用固定進度格式。
- 不假設特定模型、外掛、指令、context window 或子代理存在；先以目前工具與系統機制為準。
- 使用者已有流程時，只補最小缺口。既有 spec、tickets、決策與驗證可直接沿用。
- 沒有可靠 token 指標時，不捏造使用率；改以重讀、遺忘、矛盾、範圍漂移等壓力訊號判斷。

## Step 1：三維判斷

1. **任務複雜度**：Level 0 直接處理；1 明確小修；2 單一模組；3 多檔功能；4 跨層／跨系統；5 範圍或解法模糊。
2. **上下文壓力**：`low`、`medium`、`high`、`critical`。長任務、重複 tool output 或壓力達 `medium` 時，完整讀取 [context-management.md](references/context-management.md) 再建議。
3. **Agent 機制**：確認 skills、子代理、平行／背景任務、外部 artifacts、獨立 review context 與測試／CI 是否可用。

## Step 2：選擇最小工作流

| 層級 | 建議流程 |
| --- | --- |
| Level 0–1 | 直接處理 → focused check |
| Level 2 | 簡短 spec（需要時）→ 實作／TDD → focused verification |
| Level 3 | 對齊需求 → spec → 小型切分 → 實作 → review |
| Level 4 | spec → tickets／相依關係 → 分階段或平行實作 → 各切片驗證 → 整合 QA |
| Level 5 | research／`wayfinder` → 決策紀錄 → spec → tickets → 實作與整合 QA |

技能只在目前環境可用且能降低風險時才建議：需求模糊用 `wayfinder`／`grill-with-docs`；需求整理用 `to-spec`；拆分用 `to-tickets`；實作用 `implement`／`tdd`；除錯用 `hunt`／`diagnosing-bugs`；驗證用 `verification-loop`／`code-review`。

## Step 3：選擇 Context Mode

| Mode | 適用情境 |
| --- | --- |
| `direct` | 小型、低壓力、單一路徑 |
| `compact` | 同一任務仍需延續，但歷史與 tool output 已膨脹 |
| `subagent` | 可隔離的探索、research、無相依切片或高噪音工具工作 |
| `handoff-reset` | 階段切換、壓力過高，或需要乾淨 context 繼續實作 |
| `fresh-review` | 實作完成後，以獨立 context 審查 diff、需求與驗證證據 |

子代理的目的優先是隔離噪音，其次才是平行化。共享 mutable state、關鍵產品決策、嚴格循序工作或小任務不要委派；不支援子代理時，改用分階段單 agent 與結構化 checkpoint。

## Step 4：輸出建議

用繁體中文簡潔輸出：

```text
建議：Level <0-5> — <最小流程與理由>
Context mode：<direct|compact|subagent|handoff-reset|fresh-review>
搭配：<只列目前可用的 skill／agent 機制；無則寫「直接處理」>
提示詞：<一段可直接使用的提示詞>
```

使用者要求提示詞或建議中需要提示詞時，完整讀取 [prompt-templates.md](references/prompt-templates.md)，只選一個最貼近情境的範本，不要一次貼出全部。若 context 管理會改變路由，提示詞必須包含 checkpoint、artifact 或 handoff 要求。
