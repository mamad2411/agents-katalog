---
name: commercial-proposal-writing
description: Use when drafting or reviewing internal proposals, fundraising decks, partnership proposals, proposal rewrites, and decision-oriented business plans that must persuade a specific audience to approve resources, invest money, or commit to collaboration. Trigger on requests such as 商業企劃, 內部提案, 募資提案, 合作提案, 提案優化, 提案審稿, 董事會版本, 投資人版本, ask 撰寫, 資料不足處理.
---

# 商業企劃寫作

## Overview

把企劃書視為「讓決策者說 Yes 的商業說服文件」。
本 skill 採雙模式：`generate` 產出完整企劃，`review` 審查既有企劃並重寫關鍵段落。
主流程固定為：提案分類 -> Audience 與 Ask 明確化 -> 企劃五問 -> 九段式說服結構 -> 健檢。

這不是全包式市場研究 skill。商業模式深化：使用 `business-model-architect`。統計方法與 `scripts/*.py` 僅在明確要求研究分析時載入。

## Input Contract

必要欄位如下，不直接跳寫正文：

- `proposal_type`: `internal|fundraising|partnership`
- `audience`: 誰做決策、誰影響決策、誰使用
- `decision_goal`: 這份企劃想推動什麼決策
- `ask`: 要對方批准什麼、投入什麼、何時決定
- `problem_statement`: 核心問題與不行動代價
- `target_customer`: 目標客群或受影響對象
- `available_evidence`: 可用資料、來源、可信度與限制
- `goal_kpi`: 成功定義與門檻
- `budget`: 預算、資源或投資需求
- `timeline`: 里程碑、時程與決策節點
- `mode`: `generate|review`
- `tone_profile`: `executive_formal|investor_formal|consulting_formal|gov_formal|auto`
- `formality_level`: `standard|strict`，預設 `strict`

## Data Sufficiency Gate

所有請求先檢查：

- `proposal_type`
- `audience`
- `decision_goal`
- `ask`
- `problem_statement`
- `target_customer`
- `available_evidence`
- `goal_kpi`

`budget` 與 `timeline` 若缺失，不得默默補完；應補件，或依 A/B/C/D 方案處理。

規則：

1. 缺核心欄位時，不進入 `generate` 或 `review`，先輸出 `MissingDataQueryOutput`。
2. 明確表示「資料不足」時，輸出 A/B/C/D 路徑，不直接編寫數字。
3. 所有代填資訊都必須標示 `Assumption`、`Validation Needed`、`Risk`。
4. `review` 模式若缺原稿或關鍵段落，輸出補件要求，不可憑空審稿。

### MissingDataQueryOutput

- `missing_fields`
- `why_needed`
- `questions_to_user`
- `no_data_options`
- `next_step_rule`

### No-Data Options

- **A. 最快假設版**
  - 以保守假設產出草案，全部假設顯式標註。
- **B. 輕量訪談驗證版**
  - 執行 2-5 個關鍵訪談或內部訪談後產出企劃。
- **C. 小規模數據蒐集後正式版**
  - 蒐集最小可用數據後產出決策版。
- **D. 客製方案**
  - 依時程、資料可得性與受眾壓力重排流程。

預設不替使用者自動選擇 A/B/C/D。

## Mode Routing

未提供 `mode` 時：

- 題目、想法、摘要型需求 -> `generate`
- 已貼草稿、要求修改或審稿 -> `review`

若 `tone_profile=auto`：

- `internal -> executive_formal`
- `fundraising -> investor_formal`
- `partnership -> consulting_formal`

再依受眾覆寫：

- 政府、標案、法遵、審議 -> `gov_formal`
- 董事會、經營層、主管會議 -> `executive_formal`
- 投資人、VC、基金、IR -> `investor_formal`
- 顧問、策略合作、跨部門整合 -> `consulting_formal`

## Non-Negotiable Rules

以下是硬性禁則，違反時不得視為可交付版本：

1. 禁止空洞開場。
   - 不可用「本企劃旨在」「為了提升」這類無資訊開頭。
   - 執行摘要必須以痛點數據、對比或結果切入。
2. 禁止只貼產業報告。
   - 市場論述必須回到市場規模、成長率、需求缺口。
3. 禁止把問題寫成「大家都有這個問題」。
   - 必須交代誰痛、痛多大、現有方案為何不行、不做會怎樣。
4. 禁止 KPI 只有目標沒有推導。
   - 目標必須可由客戶數、客單價、轉換、曝光或里程碑反推。
5. 禁止把競品分析寫成名單。
   - 只選 2-3 個真正有對比價值的對象，回答「為什麼選我」。
6. 禁止只賣功能不賣成果。
   - 每個方案段落都要出現「功能 -> 好處 -> 成果」鏈。
7. 禁止只列通路不證明有效。
   - 行銷段落必須連到漏斗與單位經濟效益，如 `CAC/LTV/ROAS`。
8. 禁止只放甘特圖不建立信任。
   - 執行計畫必須同時交代關鍵能力、過往證明、Go/No-Go 決策點。
9. 禁止財務數字無推導。
   - 營收、成本、回收期都必須拆成公式或假設鏈。
10. 禁止隱藏風險。
   - 至少揭露三個高機率風險與對應動作。
11. 禁止沒有 Ask。
   - 每份企劃都必須明說要什麼資源、何時決策、下一步是什麼。
12. 禁止翻譯腔與空話。
   - 語言要正式但自然，避免官樣句、抽象動詞堆疊、無主詞空話。

## Strategy Engine

動筆前執行企劃五問：

1. 為誰解決什麼問題
2. 為什麼是現在
3. 憑什麼是我們
4. 要花多少、賺多少
5. 成功長什麼樣

這五問的回答固定輸出到 `strategy_answers`，然後再進入正文生成。

## Generate Output Contract

通過 Data Sufficiency Gate 後輸出：

- `strategy_answers`
- `narrative_body`
- `key_numbers_logic`
- `assumption_register`
- `ask_block`
- `coverage_status`

`narrative_body` 必須是可直接送審的連續正文，並固定包含九段式結構：

1. 執行摘要
2. 問題定義
3. 目標客群與決策旅程
4. 競爭分析與差異化
5. 方案設計與商業模式
6. 行銷策略與推廣計畫
7. 執行計畫與團隊可信度
8. 財務預估與風險評估
9. Ask / 決策請求 / 下一步

`key_numbers_logic` 至少說明：

- 營收推導
- 成本推導
- KPI 反推
- 單位經濟效益

`assumption_register` 固定欄位：

- `Assumption`
- `Validation Needed`
- `Risk`

## Review Output Contract

審稿時固定輸出：

- `findings_by_severity`
- `logic_gaps`
- `numerical_inconsistencies`
- `missing_sections`
- `common_mistake_flags`
- `rewrite_priorities`
- `reintegrated_rewrite`

`review` 固定流程：

1. 檢查 `Why -> What -> How -> Proof -> Ask`
2. 檢查九段式章節缺漏
3. 檢查數字推導與前後一致
4. 檢查常見錯誤
5. 依 `Critical / Major / Minor` 輸出重寫建議與整合版改寫

## Quality Gates

提交前強制檢查：

1. `Why -> What -> How -> Proof -> Ask` 是否完整
2. 九段式章節是否齊全
3. Ask 是否具體且可執行
4. 財務、KPI、時程是否前後一致
5. 關鍵結論是否來自證據或顯式假設
6. 是否觸犯任何 Non-Negotiable Rules
7. 是否通過 [08-output-polish-and-pitch-checklist.md](./references/08-output-polish-and-pitch-checklist.md)

## Mode Workflow

### Generate

1. 依 [01-intake-and-audience-routing.md](./references/01-intake-and-audience-routing.md) 收斂輸入、模式與受眾。
2. 先過 Data Sufficiency Gate。
3. 缺資料時，輸出 `MissingDataQueryOutput`。
4. 通過後，依 [02-strategy-thinking-engine.md](./references/02-strategy-thinking-engine.md) 完成企劃五問。
5. 依 [03-proposal-structure-by-type.md](./references/03-proposal-structure-by-type.md) 判定情境重點。
6. 依 [04-section-writing-playbook.md](./references/04-section-writing-playbook.md) 生成九段式正文。
7. 依 [05-financial-assumption-and-risk-guide.md](./references/05-financial-assumption-and-risk-guide.md) 檢查數字與風險。
8. 依 [07-formal-tone-style-guide.md](./references/07-formal-tone-style-guide.md) 與 [08-output-polish-and-pitch-checklist.md](./references/08-output-polish-and-pitch-checklist.md) 做最終修整。
9. 輸出 `DraftOutput`。

### Review

1. 確認有可審核原稿。
2. 先過 Data Sufficiency Gate。
3. 依 [06-review-rubric-and-rewrite-rules.md](./references/06-review-rubric-and-rewrite-rules.md) 做結構、數字、常見錯誤檢查。
4. 針對缺漏章節與 Ask 做 `reintegrated_rewrite`。
5. 輸出 `ReviewOutput`。

## Resources

- Intake 與受眾路由： [01-intake-and-audience-routing.md](./references/01-intake-and-audience-routing.md)
- 企劃五問： [02-strategy-thinking-engine.md](./references/02-strategy-thinking-engine.md)
- 三種提案結構差異： [03-proposal-structure-by-type.md](./references/03-proposal-structure-by-type.md)
- 章節寫作手冊： [04-section-writing-playbook.md](./references/04-section-writing-playbook.md)
- 財務假設與風險： [05-financial-assumption-and-risk-guide.md](./references/05-financial-assumption-and-risk-guide.md)
- 審稿與重寫規則： [06-review-rubric-and-rewrite-rules.md](./references/06-review-rubric-and-rewrite-rules.md)
- 正式語氣指南： [07-formal-tone-style-guide.md](./references/07-formal-tone-style-guide.md)
- 輸出健檢與簡報演練： [08-output-polish-and-pitch-checklist.md](./references/08-output-polish-and-pitch-checklist.md)
- 產出模板： [proposal_full_template.md](./assets/templates/proposal_full_template.md), [review_report_template.md](./assets/templates/review_report_template.md)
- 研究分析腳本： `scripts/*.py`，僅在明確要求研究分析時使用

## Note

需求升級為商業模式重設、通路與收入設計、30 天驗證實驗時，使用 `business-model-architect`。
