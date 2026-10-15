---
name: investment-research-prompts
description: Use when the user needs stock screening, portfolio risk review, dividend portfolio design, pre-earnings analysis, industry competition analysis, DCF valuation, technical analysis, or stock trend/anomaly detection. Trigger on requests like 選股, 投資組合風險, 股息策略, 財報前瞻, DCF 估值, 技術面分析, 產業競爭研究, 趨勢識別, or investment research prompts.
---

# Investment Research Prompts

## Overview

把投資研究需求先路由到正確場景，再檢查必要輸入，最後從提示詞庫取用對應模板。這個 skill 以 prompt 模板與分析框架為核心，不負責程式化抓取金融資料。

## Use This Skill

Use when:

- 使用者想要股票篩選、選股框架或研究報告模板
- 使用者要拆解投資組合風險、再平衡或避險方向
- 使用者要規劃股息投資組合與被動收入藍圖
- 使用者要做財報前瞻、產業競爭、DCF 估值、技術分析或異常模式辨識
- 使用者明確要「prompt」「模板」「分析框架」「研究 brief」

Do not use when:

- 使用者只要單一即時股價或單一財務指標，沒有研究框架需求
- 任務是實作金融資料 API、回測程式或交易系統
- 任務是一般理財建議，且不需要股票研究輸出格式

## Routing Rule

先判斷請求屬於哪一類：

1. `stock-screening`
2. `portfolio-risk-review`
3. `dividend-portfolio-blueprint`
4. `pre-earnings-brief`
5. `industry-competition-report`
6. `dcf-valuation-memo`
7. `technical-analysis-report`
8. `trend-anomaly-memo`

若使用者描述同時包含多個類型，優先問清楚主要決策目的是：

- 找標的
- 估值
- 交易時機
- 組合風險
- 產業比較

細節模板與欄位規則見 [references/prompt-library.md](./references/prompt-library.md)。

## Input Gate

先檢查該場景的必要資訊是否齊全。若不足，先回 `MissingDataOutput`，不要直接輸出空模板。

`MissingDataOutput` 必須包含：

- `detected_scenario`
- `missing_fields`
- `why_needed`
- `follow_up_questions`
- `next_step`

追問原則：

- 只問最少必要欄位
- 優先問能改變分析結論的資訊
- 若日期不明但可合理推進，先標示假設再繼續

## Freshness Rule

以下資訊具有時效性，執行分析時必須查證最新來源，不可把模板當成離線事實：

- 最新股價
- 估值倍數
- 財報日期
- 分析師共識
- 殖利率
- 配息紀錄
- 市值
- 期權隱含波動或 implied move
- 空頭比例、內部人交易、機構持股變化

若使用者要求「最新」「今天」「目前」「即將公布」之類的內容，必須先取得最新資料與來源，再套用模板。

## Output Rule

若資訊足夠，可以有兩種輸出方式：

- 直接產出適合該情境的完整研究 prompt
- 依模板結構直接展開分析框架，並明確標示已知資訊、待補資訊、假設與資料來源需求

輸出時應保留：

- 專業角色設定
- 分析項目清單
- 輸出格式要求
- 使用者需補的變數槽位

不要：

- 捏造即時市場數據
- 在缺必要欄位時硬做結論
- 把多個場景模板混在一起而不說明主軸

## Suggested Workflow

1. 辨識主要場景
2. 檢查必要輸入
3. 若缺資料，回 `MissingDataOutput`
4. 讀取對應模板段落
5. 視需求保留模板，或轉成當前任務的分析框架
6. 若內容依賴即時市場資訊，先查證再回答

