---
name: psychological-trigger-marketing
description: Use when generating high-conversion marketing angles, campaign hooks, landing page messaging, promotional copy directions, social post hooks, or CTA concepts with psychological triggers such as FOMO, justification, desire, priming, anchoring, and framing, especially for offers, launches, limited-time promotions, and Traditional Chinese marketing for Taiwan audiences.
---

# Psychological Trigger Marketing

## Overview

用這個 skill 為促銷活動、商品服務、頁面文案與 CTA 設計高轉換心理觸發策略。預設輸出使用繁體中文與台灣用語，重點不是解釋理論，而是把心理觸發改寫成可直接拿去寫文案、排版與設計訊息層次的策略。

## When to Use

Use when:

- 需要產出 campaign angle、促銷主軸、頁面訊息架構或 CTA 方向
- 需要把「限時、限量、優惠、組合、價差、社會認同」轉成更有推進力的行銷說法
- 需要為廣告、Landing page、社群貼文、活動宣傳、限時促銷設計高轉換訊息
- 需要把抽象賣點改寫成更能推動決策的心理觸發語言
- 需要台灣市場語境的繁中行銷策略，而不是一般英文式 growth copy

Do not use:

- 純學術說明、心理學教學或文獻整理
- 品牌價值宣言、企業願景、長篇敘事型品牌故事，且沒有轉換目標
- 涉及醫療、法律、金融等高風險宣稱，且需要專業合規審核的最終文案
- 使用者要求捏造數據、假稀缺、假見證、假倒數或其他明顯誤導手法

## Input Contract

最低必要輸入：

- `product_or_offer`: `string`
- `target_audience`: `string`
- `goal`: `string`
- `channel`: `ad | landing-page | social | event | promotion`
- `conversion_stage`: `cold | warm | hot`

選填但強烈建議：

- `price_point`: `string`
- `urgency_context`: `string`
- `proof_assets`: `string[]`
- `brand_tone`: `string`
- `constraints`: `string[]`

## Data Sufficiency Gate

若最低必要輸入不足，不要直接硬寫策略；先輸出 `MissingDataOutput`：

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "temporary_assumptions": [],
  "risk_of_assumption": []
}
```

Gate 規則：

- 缺 `product_or_offer` 或 `goal`：不能進入策略生成
- 缺 `target_audience`：只能先給低信心通用方向，必須明列假設
- 缺 `channel` 或 `conversion_stage`：不能決定訊息節奏與刺激強度，必須先追問或暫時假設
- `proof_assets` 為空時，不得虛構證據、口碑、數據或限量依據

## Trigger Engine

主框架採雙軌命名，先選 1-2 個主驅動，再配 1-2 個輔助模組。

### 1. 嚇唬 / 失落驅動

- 核心：放大錯過、延遲、沒有行動的代價
- 常見用法：限時、限量、錯過要再等、現在不買之後更貴
- 適合：高意圖、促銷、倒數、名額制活動、稀缺供給

### 2. 安撫 / 正當化驅動

- 核心：降低購買阻力，替消費者提供合理化理由
- 常見用法：省時、省力、對家人更好、支持在地、買得有意義
- 適合：高單價、非必需品、價值感需要被說清楚的產品

### 3. 引誘 / 渴望驅動

- 核心：讓人先想像擁有後的畫面與感受
- 常見用法：生活方式投射、感官描述、身份升級、理想情境
- 適合：體驗型商品、生活風格產品、旅宿、餐飲、美感消費

### 4. 促發

- 核心：先用語言、場景或符號把消費者帶進特定心理狀態
- 常見用法：在標題、首屏、視覺或按鈕前文字植入關鍵暗示

### 5. 錨定

- 核心：透過比較基準改變價格、價值或條件的感受
- 常見用法：原價對比、方案階梯、先高後低、主推方案夾在兩側

### 6. 框架

- 核心：同一件事，用不同說法會導致不同決策
- 常見用法：損失規避、收益放大、限購、門檻、資格式優惠

### 7. 共享優惠 / 同伴驅動

- 核心：用「一起買更划算」推動社交參與，放大決策動能
- 常見用法：雙件價、湊單、團購、雙人方案、分享解鎖優惠
- 適合：多件折扣、朋友同行、伴侶同行、需要拉升件數的促銷

詳細定義、文案動作與台灣示例，讀 [references/01-trigger-playbook.md](./references/01-trigger-playbook.md)。

## Trigger Selection Rules

- 每次選 `2-4` 個觸發器，不要全部堆滿
- `cold` 流量：優先 `引誘 / 渴望驅動` + `促發`，先讓人停下來
- `warm` 流量：優先 `安撫 / 正當化驅動` + `錨定`，補足理由與價值感
- `hot` 流量：優先 `嚇唬 / 失落驅動` + `框架`，直接推進決策
- 高單價：至少搭配一個 `安撫 / 正當化驅動`
- 限時促銷：至少搭配一個 `嚇唬 / 失落驅動` 或 `框架`
- 有方案價差：優先使用 `錨定`
- 有 `多件更划算/團購/雙人方案`：優先 `同伴驅動 + 錨定`；若要衝件數，再加 `框架`
- 沒有可信證據時，不要硬上強烈 FOMO；改用 `引誘` 或 `安撫`

依 channel 與目標的套用方式，讀 [references/02-application-matrix.md](./references/02-application-matrix.md)。

## Output Contract

固定輸出以下欄位：

```json
{
  "strategy_summary": "",
  "trigger_stack": [],
  "message_angles": [],
  "headline_options": [],
  "cta_options": [],
  "risk_flags": [],
  "assumptions_used": []
}
```

欄位規則：

- `strategy_summary`: 2-5 句，說明本次用哪些心理驅動、為何這樣組合
- `trigger_stack`: 列出主驅動與輔助模組，每個都要附 `why` 與 `role`
- `message_angles`: 提供 3-5 個可延伸成頁面或廣告的角度
- `headline_options`: 提供 3 個以上標題方向，需符合台灣用語
- `cta_options`: 提供 3 個以上 CTA，避免空泛動詞
- `risk_flags`: 明列可能踩線、過度承諾、證據不足或刺激過強的地方
- `assumptions_used`: 缺資料時必填

## Workflow

1. 先跑 Data Sufficiency Gate
2. 判斷目前是 `cold / warm / hot` 哪一段轉換
3. 從三個主驅動中選 1-2 個，從四個輔助模組中選 1-2 個
4. 先寫 `strategy_summary`，再展開 `message_angles`
5. 最後才寫 `headline_options` 與 `cta_options`
6. 補上 `risk_flags` 與 `assumptions_used`

## Hard Rules

- 允許高刺激、高推進力表達，但不得虛構數據、假見證、假限量、假倒數或假比較
- 若使用「限量」、「最後一波」、「只剩」等說法，必須有可驗證依據；沒有就改寫成真實條件
- 不要把焦慮當成唯一手段；強刺激後要有合理承接，不可只靠情緒轟炸
- 不要把在地、公益、永續、支持小農當成空洞裝飾詞；若無真實內容，不得拿來安撫
- 不得生成違法、歧視、羞辱、恐嚇或明顯誤導 claims
- 預設使用繁體中文與台灣市場說法，不用中國用語

## References

- Trigger 定義與案例：[references/01-trigger-playbook.md](./references/01-trigger-playbook.md)
- Channel 套用矩陣：[references/02-application-matrix.md](./references/02-application-matrix.md)

## Suggested Prompts

- `Use $psychological-trigger-marketing to design a Taiwan Traditional Chinese campaign angle and CTA set for a limited-time offer.`
- `Use $psychological-trigger-marketing to turn this product offer into a high-conversion landing page messaging strategy in Traditional Chinese.`
- `Use $psychological-trigger-marketing to create a trigger stack, headline options, and CTA directions for this promotion without inventing fake scarcity or fake proof.`
