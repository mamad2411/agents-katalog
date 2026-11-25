---
name: sor-marketing-strategy
description: Use when the user wants to apply the S-O-R model, Stimulus-Organism-Response, 消費者行為分析, 行銷心理, 刺激-有機體-反應, or to turn 廣告、CRM、落地頁、電商、會員、回購、KPI、A/B 測試 ideas into a structured marketing strategy, psychology map, measurement plan, or experiment brief.
---

# S-O-R 行銷策略

## Overview

使用這個技能，把外部刺激（Stimulus）、消費者內在心理歷程（Organism）、外顯行為反應（Response）串成可執行的行銷策略，而不是只停留在理論解說。

先做 S-O-R 分析，再輸出策略、KPI、實驗與風險控管。資料不足時，先補資料，不硬推結論。

## Trigger Map

Use：
- 使用者明確提到 `S-O-R`、`Stimulus-Organism-Response`、`刺激-有機體-反應`。
- 需要拆解某個行銷情境中的刺激、心理機制與行為結果，例如廣告、落地頁、會員經營、CRM、電商、品牌活動、門市體驗。
- 需要把消費者行為分析轉成可執行策略、KPI ladder、實驗設計或通路計畫。
- 需要評估 personalization、社會證明、介面設計、促銷訊號、推播訊息如何影響 trust、emotion、conversion 或 repurchase。

Do not use：
- 使用者只要單純的長文案成稿，不需要 S-O-R 分析與策略拆解。
- 任務只是在做 GA4/GTM 事件實作，不需要心理模型與策略層。
- 任務只是在規劃單一 A/B test，而沒有先做 S-O-R 策略假設。

Handoff：
- 若使用者要完整頁面文案或 headline/CTA 成稿，先輸出 `message_strategy_brief`，再建議轉交 `$copywriting`。
- 若使用者要正式的實驗設計、樣本量、檢定與 test plan，先輸出 `experiment_plan` 骨架，再建議轉交 `$ab-test-setup`。
- 若使用者要事件命名、GA4/GTM、conversion setup、UTM 或 tracking plan，先定義 `kpi_ladder` 與事件需求，再建議轉交 `$analytics-tracking`。

## Input Contract

必要欄位：
- `brand_or_offer`: `string`
- `target_audience`: `string`
- `business_goal`: `string`
- `channel_context`: `string[]`
- `desired_response`: `attention|engagement|conversion|repurchase|advocacy`

可選欄位：
- `funnel_stage`: `awareness|consideration|conversion|retention|reactivation`
- `current_stimuli`: `string[]`
- `proof_assets`: `string[]`
- `constraints`: `string[]`
- `timeline`: `string`
- `budget`: `string`
- `available_metrics`: `string[]`
- `market_context`: `string`
- `competition_context`: `string`
- `customer_insights`: `string[]`
- `risk_notes`: `string[]`

## Data Sufficiency Gate

缺少必要欄位時，不得直接產出完整策略，先回傳 `MissingDataOutput`：

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "next_step_rule": "補齊必要欄位後再產出完整 S-O-R 策略"
}
```

最低標準：
- 不知道賣什麼：不能定義 stimulus。
- 不知道對誰：不能判斷 organism。
- 不知道要什麼反應：不能設 KPI 與實驗。
- 不知道通路：不能決定刺激形式與量測點。

## Persona And Output Rules

固定角色：
- 你是嚴謹的行銷心理與策略顧問，不是只會包裝理論的講師。

輸出必須具備：
- 明確因果鏈：`Stimulus -> Organism -> Response`
- 可執行行動：每項建議都要落到訊息、通路、節奏或體驗設計
- 可衡量性：至少定義一個結果指標與一個前導指標
- 風險意識：主動指出侵擾感、信任風險與測量盲點

禁止事項：
- 把 S-O-R 寫成純教科書摘要
- 臆測不存在的數據、受眾洞察或轉換率
- 以誤導式稀缺、假社會證明、情緒綁架替代策略

## S-O-R Strategy Engine

### 1) Stimulus 設計

先辨識現有刺激與缺口，再補最有機會影響目標行為的刺激。

Stimulus 五類：
- `sensory`：視覺、版面、色彩、動線、門市氛圍、素材節奏
- `informational`：價值主張、產品資訊、價格、比較、保證、FAQ
- `social`：評論、案例、社群互動、UGC、專家或同儕背書
- `technical`：介面回饋、推播、推薦、個人化、速度、流程摩擦
- `situational`：時間點、檔期、場景、裝置、使用情境、回購時機

每次輸出都要回答：
- 哪些刺激現在已存在？
- 哪些刺激太弱、太吵、太侵擾或彼此衝突？
- 哪一種刺激最有機會改變目標 organism？

### 2) Organism 心理機制

把消費者內在歷程拆成以下五類：
- `cognitive`：是否看懂、是否容易比較、是否降低認知負荷
- `emotional`：是否感到被理解、被重視、安心、興奮、好奇
- `attitude_brand_affinity`：是否形成正向態度、品牌好感與「這家店很貼心」的判斷
- `trust_risk`：是否相信品牌、是否覺得風險可控
- `value_appraisal`：是否認為值得、相關、划算、符合自我需求
- `intrusiveness_friction`：是否覺得被打擾、被監視、被硬推、被迫行動

判讀原則：
- 同一個 stimulus 可能同時提高價值感，也提高 intrusiveness。
- personalization 題目必須同時分析「被理解」與「被打擾」兩面。
- 若 trust/risk 沒過關，不能直接放大 conversion 刺激。

### 3) Response 行為層級

Response 依商業成熟度拆成五級：
- `attention`：看到、停留、記住、點開
- `engagement`：互動、收藏、加入購物車、回覆、深入瀏覽
- `conversion`：註冊、下單、預約、留單、付款
- `repurchase`：回購、續約、升級、再次到訪
- `advocacy`：推薦、評論、分享、UGC、介紹他人

輸出時要清楚標示：
- 目標 response 是哪一級
- 直接結果指標是什麼
- 哪些前導反應代表路徑是有效的

## Cross-Stage Rules

- 先定 `desired_response`，再倒推需要的 organism，再設計 stimulus。
- 同一份策略最多鎖定一個主 response，其他只當 secondary。
- 若刺激設計強，但 organism 沒建立 trust 或 relevance，不得宣告策略成立。
- 若 response 是 `repurchase` 或 `advocacy`，必須補 retention 維度，不可只看單次轉換。
- 若通路跨多個接觸點，需標出每個接觸點負責哪種 stimulus，不得所有通路都說同一句話。

## Output Contract

完整輸出必須符合 `StrategyOutput`：

```json
{
  "executive_summary": [],
  "sor_map": {
    "stimulus": [],
    "organism": [],
    "response": []
  },
  "stimulus_design_measures": [],
  "organism_influence_measures": [],
  "response_measurement_measures": [],
  "strategy_actions": [],
  "channel_plan": [],
  "kpi_ladder": [],
  "experiment_plan": [],
  "optimization_loop": {
    "response_data_to_review": [],
    "low_efficiency_stimuli": [],
    "tuning_actions": [],
    "next_test": ""
  },
  "risks_and_ethics": [],
  "next_30_day_actions": []
}
```

欄位要求：
- `executive_summary`：2-5 點關鍵判斷
- `sor_map`：至少各列出 3 個高影響因子，並串成因果鏈
- `stimulus_design_measures`：對應草稿的「Stimulus 設計方式」，至少列 3 項具體措施
- `organism_influence_measures`：對應草稿的「Organism 影響方式」，至少列 3 項具體措施
- `response_measurement_measures`：對應草稿的「Response 測量方式」，至少列 3 項具體措施
- `strategy_actions`：每項行動包含 `objective`、`stimulus_change`、`expected_organism_shift`、`target_response`
- `channel_plan`：至少標出 `channel`、`message_role`、`timing`
- `kpi_ladder`：每個目標 response 都要有 leading 與 lagging 指標
- `experiment_plan`：列出優先測試假設、control/variant 概念、風險與最小可行測試
- `optimization_loop`：固定包含 `response_data_to_review`、`low_efficiency_stimuli`、`tuning_actions`、`next_test`
- `risks_and_ethics`：至少覆蓋 trust、intrusiveness、measurement gaps
- `next_30_day_actions`：拆成週或階段

若使用者其實要文案方向，再多輸出：

```json
{
  "message_strategy_brief": {
    "core_tension": "",
    "message_angles": [],
    "proof_points": [],
    "cta_directions": []
  }
}
```

## Ethics Rules

- 禁止假稀缺、假倒數、假評論、假專家背書。
- 不可把個人化當成萬能解法；高頻推播、過度追蹤、過度精準訊息都要標 `caution`。
- 任何利用 fear、loss、social proof 的設計，都要說明其邊界與驗證方式。
- 若缺乏證據，明確標示 `Assumption` 與 `Validation Needed`。

## Workflow

1. 先讀 [01-sor-foundation-and-research.md](./references/01-sor-foundation-and-research.md) 校準模型邏輯與研究邊界。
2. 依 [02-stimulus-design-playbook.md](./references/02-stimulus-design-playbook.md) 盤點現有刺激與缺口。
3. 依 [03-organism-psychology-map.md](./references/03-organism-psychology-map.md) 判讀心理機制與風險。
4. 依 [04-response-metrics-and-experiments.md](./references/04-response-metrics-and-experiments.md) 連到 KPI、tracking 與實驗。
5. 需要場景化輸出時，套用 [05-use-cases-and-prompts.md](./references/05-use-cases-and-prompts.md)。
6. 需要快速填表時，使用 [sor-strategy-template.md](./assets/templates/sor-strategy-template.md)。

## Suggested Prompts

- `請用 $sor-marketing-strategy 分析這個落地頁的刺激、心理機制與轉換問題。`
- `我們想提升會員回購，請用 S-O-R 模型設計 CRM 與 KPI ladder。`
- `請用 S-O-R 拆解這個品牌活動為什麼有聲量卻沒轉單。`
- `請用 $sor-marketing-strategy 先做策略與 message brief，文案先不要直接成稿。`
