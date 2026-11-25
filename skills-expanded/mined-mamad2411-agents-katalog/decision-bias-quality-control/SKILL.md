---
name: decision-bias-quality-control
description: Use when evaluating high-stakes decisions with bias-aware quality control, including proposal review, decision meeting facilitation, and personal coaching. Trigger on requests such as 重大決策、偏誤檢查、提案審查、決策會議引導、決策教練、go/no-go 決策。
---

# Decision Bias Quality Control

## Overview

使用此技能來執行「決策品管」，把重大決策從直覺推進到可追溯、可檢查、可比較的判斷流程。

遵循兩個核心原則：
- 維持「雙軌輸出」：每次都同時輸出質性洞察與量化評分。
- 檢查「提案過程」而非只看「提案結論」：用 12 問檢查清單找出偏誤來源。

先閱讀下列參考檔：
- 核心原則與來源：[references/01-source-principles.md](./references/01-source-principles.md)
- 12 問題庫：[references/02-12-question-bank.md](./references/02-12-question-bank.md)
- 三種模式流程：[references/03-mode-workflows.md](./references/03-mode-workflows.md)
- 評分與門檻：[references/04-scoring-thresholds.md](./references/04-scoring-thresholds.md)
- 統一輸出模板：[references/05-output-templates.md](./references/05-output-templates.md)

## Input Contract

接收下列結構化輸入；欄位不足時走 Data Sufficiency Gate。

- `mode`: `proposal-review | meeting-facilitation | personal-coaching | auto`
- `decision_statement`: `string`（必要）
- `decision_context`: `string`（必要）
- `proposal_snapshot`: `string`（提案審查時建議提供）
- `decision_size_factors`:
  - `financial_impact`: `1|2|3`
  - `reversibility`: `1|2|3`
  - `org_blast_radius`: `1|2|3`

## Mode Routing

若 `mode=auto`，依需求語意路由：

- 出現「審查提案、投資案、核准、go/no-go」等語意時，路由 `proposal-review`。
- 出現「主持、引導討論、會議流程、追問順序」等語意時，路由 `meeting-facilitation`。
- 出現「我該怎麼選、個人抉擇、職涯選擇」等語意時，路由 `personal-coaching`。

若語意混合，先以 `proposal-review` 執行主流程，並在附錄提供會議引導問題。

## Data Sufficiency Gate

先檢查必要欄位：

- `decision_statement`
- `decision_context`

再檢查評分所需欄位：

- `decision_size_factors.financial_impact`
- `decision_size_factors.reversibility`
- `decision_size_factors.org_blast_radius`

缺資料時，輸出 `MissingDataOutput`：

- `missing_fields`
- `why_needed`
- `questions_to_user`
- `temporary_assumption`
- `risk_of_assumption`

預設規則：
- 若三因子缺漏且使用者仍要求繼續，暫定 `decision_size=Medium`，並標註風險。

## Output Contract (Mandatory Dual Track)

每次輸出都必須同時包含以下兩軌，不得省略其中任一軌。

### A. 質性軌

- `bias_diagnosis`: 偏誤診斷摘要（依 12 問分組）
- `key_risks`: 3-5 個核心風險（附證據來源）
- `recommended_actions`: 3-5 個可執行行動（含優先級）

### B. 量化軌

- `question_scores`: 12 題逐題分數（`0|1|2`）與簡要理由
- `group_scores`: 三組標準化分數（0-100）
- `weighted_total_score`: 加權總分（0-100）
- `decision_size`: `Low|Medium|High`
- `risk_level`: `Green|Yellow|Red`
- `threshold_profile_used`: 對應門檻表

## Scoring Rules

依 [references/04-scoring-thresholds.md](./references/04-scoring-thresholds.md) 計算，使用固定模型：

- 題目分數：每題 `0|1|2`
- 分組加權：
  - Q1-3 = `30%`
  - Q4-9 = `40%`
  - Q10-12 = `30%`
- 分組先標準化至 0-100，再算加權總分
- 動態門檻依決策大小調整風險等級

## Execution Workflow

1. 確認模式與決策邊界。
2. 進行 Data Sufficiency Gate。
3. 逐題執行 12 問，收集證據與評分。
4. 計算分組分數、總分、風險等級。
5. 輸出雙軌結果與 mode-specific 結論。
6. 附上「下一步驗證行動」與「可逆/不可逆提醒」。

## Mode-Specific Decision Output

- `proposal-review`: 輸出 `go | conditional-go | no-go`。
- `meeting-facilitation`: 輸出會議腳本、追問順序、決策收斂規則。
- `personal-coaching`: 輸出選項比較、偏誤提醒、48 小時驗證行動。

詳見 [references/03-mode-workflows.md](./references/03-mode-workflows.md)。

## Quality Rules

- 不可跳過 12 問中的任何一題。
- 不可輸出無證據支持的結論。
- 不可只給結論不給計算過程。
- 不可把單一觀點誤當團隊共識。
- 必須標註假設與不確定性來源。

## Suggested Prompt

Use `$decision-bias-quality-control` to evaluate this high-stakes decision in dual-track mode with full 12-question scoring and dynamic risk thresholds.
