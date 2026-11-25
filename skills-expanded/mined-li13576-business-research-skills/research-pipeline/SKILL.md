---
name: research-pipeline
skill: research-pipeline
version: 1.0.0
role: orchestrator
status: active
language: zh-CN / en
target_discipline:
  - accounting
  - economics
description: >
  整個套件的總指揮，把五個 Skill 串成完整的研究流水線。
  從深度研究到論文定稿，8 個階段全自動調度。
  內建兩次強制誠信查核，確保論文品質。
  支援全流程、斷點續跑、自定義階段三種模式。
related_skills:
  - deep-research
  - literature-review
  - quantitative-analysis
  - academic-writing
  - academic-paper-reviewer
---

# Research Pipeline — 會計／經濟學研究全流程調度工具

## 定位說明

本 Skill 是整個套件的總指揮，負責把五個 Skill 串成一條完整的研究流水線。

你只需要說「幫我跑完整的研究流程」，它就自動調度每個 Skill，
從文獻到論文定稿一次跑完。

調度的五個 Skill：
- deep-research：深度研究
- literature-review：文獻綜述
- quantitative-analysis：量化分析（串接 Stata MCP）
- academic-writing：論文寫作
- academic-paper-reviewer：審稿

---

## Trigger Keywords（觸發條件）

**簡體中文**: 幫我跑完整研究流程, 從頭到尾幫我做研究,
完整的研究 pipeline, 從研究到論文, 全流程研究,
從第幾階段繼續, 只跑某些階段

**繁體中文**: 幫我跑完整研究流程, 從頭到尾幫我做研究,
完整的研究 pipeline, 從研究到論文

**English**: run full research pipeline, complete research workflow,
end-to-end research, from research to paper, resume from stage,
custom pipeline

### Non-Trigger Scenarios

| 情境 | 應該用哪個 Skill |
|------|----------------|
| 只需要做文獻研究 | deep-research |
| 只需要整理文獻 | literature-review |
| 只需要跑回歸 | quantitative-analysis |
| 只需要寫論文 | academic-writing |
| 只需要審稿 | academic-paper-reviewer |

---

## Agent Team（4 個代理）

| # | Agent | 職責 |
|---|-------|------|
| 1 | orchestrator_agent | 總指揮，決定走哪個階段、調度哪個 Skill |
| 2 | state_tracker_agent | 追蹤目前到哪個階段，記錄每階段輸出 |
| 3 | integrity_checkpoint_agent | 強制誠信查核，擁有暫停權 |
| 4 | quality_evaluator_agent | 每階段結束評估品質，決定是否繼續 |

---

## 代理詳細規則

### orchestrator_agent

職責：總指揮，負責調度所有 Skill 和決策流程走向。

工作步驟：
1. 確認使用模式（full / resume / custom）
2. 確認 Stata MCP 連線狀態（Stage 3 之前）
3. 按順序調度每個 Skill
4. 在每個強制確認點等待使用者輸入
5. 根據品質評估結果決定是否繼續或回退

分支決策規則：

Stage 3.5 誠信查核後：
  PASS → 繼續 Stage 4
  WARNING → 告知使用者，等待修正後繼續
  CRITICAL → 流程暫停，必須修正後重新查核

Stage 5 審稿結果後：
  Accept → 直接進 Stage 6.5 最終誠信查核
  Minor Revision → 進 Stage 6 修改
  Major Revision → 進 Stage 6 修改（提醒使用者修改幅度較大）
  Reject → 流程暫停，與使用者討論是否重寫或放棄

⚠️ IRON RULE：
強制確認點不能自動通過。
orchestrator_agent 必須等待使用者明確輸入（如「確認」「繼續」）
才能進入下一個階段。不能假設使用者同意。

---

### state_tracker_agent

職責：全程追蹤流程狀態，確保任何時候都可以從中斷點繼續。

狀態記錄格式（pipeline_state.md）：

# Pipeline 狀態記錄

## 基本資訊
- 研究主題：[主題]
- 開始時間：[時間]
- 目前階段：Stage [X]
- 整體狀態：進行中 / 暫停 / 完成

## 各階段狀態

### Stage 1：深度研究
狀態：✅ 完成 / 🔄 進行中 / ⏸️ 暫停 / ⬜ 未開始
完成時間：[時間]
主要輸出：[研究設計摘要]
使用者確認：[已確認 / 未確認]

### Stage 2：文獻綜述
狀態：[同上]
完成時間：[時間]
主要輸出：[文獻綜述摘要]
使用者確認：[已確認 / 未確認]

### Stage 3：量化分析
狀態：[同上]
完成時間：[時間]
主要輸出：[分析結果摘要]
Stata MCP 狀態：[連線成功 / 失敗]
使用者確認：[已確認 / 未確認]

### Stage 3.5：誠信查核（第一次）
狀態：[同上]
查核結果：PASS / WARNING / CRITICAL
問題清單：[若有]

### Stage 4：論文寫作
狀態：[同上]
完成時間：[時間]
輸出檔案：[檔名]
使用者確認：[已確認 / 未確認]

### Stage 5：審稿
狀態：[同上]
審稿決定：Accept / Minor Revision / Major Revision / Reject
總分：[XX/100]

### Stage 6：修改
狀態：[同上]
修改版本：第 [X] 次修改

### Stage 6.5：誠信查核（第二次）
狀態：[同上]
查核結果：PASS / WARNING / CRITICAL

### Stage 7：定稿
狀態：[同上]
最終輸出：[檔案清單]

### Stage 8：流程總結
狀態：[同上]
協作品質評分：[XX/100]

⚠️ IRON RULE：
每個階段開始和結束時必須更新 pipeline_state.md。
使用者可以隨時要求查看目前狀態。

---

### integrity_checkpoint_agent

職責：在 Stage 3.5 和 Stage 6.5 執行強制誠信查核。

查核項目：

引用誠信：
  □ 隨機抽查 10 篇引用，確認能在 CNKI 或 WoS 查到
  □ 確認引用格式一致
  □ 標記疑似捏造引用為 CRITICAL

數據一致性：
  □ 正文描述的數字與表格是否一致
  □ 不同章節之間的數字是否前後一致
  □ 描述性統計是否合理

結果輸出：

PASS：
  所有查核項目通過，可以繼續下一階段。

WARNING：
  發現以下問題需要修正：
  [問題清單]
  修正後告知 orchestrator_agent 繼續。

CRITICAL：
  發現以下嚴重問題：
  [問題清單]
  流程暫停。必須修正所有 CRITICAL 問題後，
  重新執行誠信查核才能繼續。

⚠️ IRON RULE：
integrity_checkpoint_agent 擁有暫停權。
發現 CRITICAL 問題時，orchestrator_agent 必須暫停流程，
不能在有 CRITICAL 問題的情況下繼續往下走。

---

### quality_evaluator_agent

職責：每個主要階段結束後評估品質，給出繼續或調整的建議。

評估框架：

Stage 1 結束後評估：
  □ 研究問題是否清晰可測試？
  □ 方法論設計是否合理？
  □ 數據來源是否可及？
  建議：繼續 / 調整研究設計後繼續

Stage 2 結束後評估：
  □ 文獻覆蓋是否完整？
  □ 研究缺口是否清楚說明？
  □ 引用品質是否符合標準？
  建議：繼續 / 補充文獻後繼續

Stage 3 結束後評估：
  □ 基準回歸結果是否顯著？
  □ 穩健性是否通過？
  □ 結果是否符合假設？
  建議：繼續 / 調整分析後繼續 / 重新考慮假設

Stage 4 結束後評估：
  □ 論文結構是否完整？
  □ 假設推導是否嚴謹？
  □ 寫作品質是否符合期刊標準？
  建議：繼續審稿 / 修改後再審稿

Stage 6 結束後評估：
  □ 修改路線圖是否逐一回應？
  □ 修改是否有效解決問題？
  建議：進入定稿 / 再次修改

---

## 模式清單（3 種）

| 模式 | 觸發方式 | 說明 |
|------|---------|------|
| full | 「幫我跑完整研究流程」 | 8 個階段全跑 |
| resume | 「從第 X 階段繼續」 | 從指定階段繼續，讀取已有狀態 |
| custom | 「只跑研究和寫作，跳過分析」 | 自定義跑哪些階段 |

---

## 各模式詳細流程

### 模式 1：full（完整流程）

觸發：「幫我跑完整研究流程」/ 「從頭到尾幫我做研究」

前置確認：
- 確認研究主題
- 確認 Stata MCP 連線狀態
- 確認目標期刊（CSSCI / SSCI / 學位論文）
- 初始化 pipeline_state.md

---

Stage 1：深度研究
  調度：deep-research（full mode）
  輸入：研究主題
  輸出：研究設計 + 方法論備忘錄 + 文獻清單
  state_tracker：記錄 Stage 1 完成
  【強制確認點 1】：
    「Stage 1 完成。研究設計如上。
     請確認後輸入『繼續』進入文獻綜述階段。」

---

Stage 2：文獻綜述
  調度：literature-review（auto mode）
  輸入：Stage 1 的文獻清單 + 研究主題
  輸出：文獻綜述報告（.docx）
  state_tracker：記錄 Stage 2 完成
  quality_evaluator：評估文獻覆蓋度
  【強制確認點 2】：
    「Stage 2 完成。文獻綜述報告已生成。
     請確認後輸入『繼續』進入量化分析階段。」

---

Stage 3：量化分析
  調度：quantitative-analysis（full mode）
  輸入：Stage 1 的研究設計 + 變數定義
  確認 Stata MCP 連線
  輸出：結果表格（.docx）+ research_log.md + stata_log.txt
  state_tracker：記錄 Stage 3 完成
  quality_evaluator：評估分析結果品質
  【強制確認點 3】：
    「Stage 3 完成。分析結果如上。
     請確認後輸入『繼續』進入誠信查核。」

---

Stage 3.5：誠信查核（第一次，強制）
  調度：integrity_checkpoint_agent
  查核：引用真實性 + 數據一致性
  結果 PASS → 繼續 Stage 4
  結果 WARNING → 等待修正後繼續
  結果 CRITICAL → 流程暫停

⚠️ IRON RULE：Stage 3.5 不能跳過，不能自動通過。

---

Stage 4：論文寫作
  調度：academic-writing（full mode）
  輸入：Stage 1 研究設計 + Stage 2 文獻綜述 + Stage 3 結果表格
  輸出：論文草稿（.docx）
  state_tracker：記錄 Stage 4 完成
  quality_evaluator：評估論文品質
  【強制確認點 4】：
    「Stage 4 完成。論文草稿已生成。
     請確認後輸入『繼續』進入審稿階段。」

---

Stage 5：審稿
  調度：academic-paper-reviewer（full mode）
  輸入：Stage 4 的論文草稿
  輸出：審稿報告 + 修改路線圖（.docx）
  state_tracker：記錄審稿決定和總分

  分支：
  Accept → 進 Stage 6.5
  Minor / Major Revision → 進 Stage 6
  Reject →
    「審稿結果為退稿。主要原因如下：[原因]
     請選擇：1. 大幅修改後重新提交 2. 結束流程」

---

Stage 6：修改
  調度：academic-writing（revision mode）
  輸入：Stage 4 論文草稿 + Stage 5 修改路線圖
  輸出：修改後論文（.docx）
  state_tracker：記錄修改版本
  【強制確認點 5】：
    「Stage 6 完成。修改後論文已生成。
     請確認後輸入『繼續』進入最終誠信查核。」

---

Stage 6.5：誠信查核（第二次，強制）
  調度：integrity_checkpoint_agent
  查核：修改後的引用 + 數據一致性
  結果 PASS → 繼續 Stage 7
  結果 WARNING / CRITICAL → 必須修正後重新查核

⚠️ IRON RULE：Stage 6.5 不能跳過。

---

Stage 7：定稿
  整合所有輸出，生成最終完整論文
  輸出清單：
  □ 最終論文（final_paper.docx）
  □ 研究日誌（research_log.md）
  □ Stata 執行日誌（stata_log.txt）
  □ Pipeline 狀態記錄（pipeline_state.md）
  □ 審稿報告（review_report.docx）

---

Stage 8：流程總結
  調度：quality_evaluator_agent
  輸出：協作品質報告

  協作品質評分（6 個維度）：
  □ 研究設計品質：[XX/20]
  □ 文獻覆蓋品質：[XX/15]
  □ 量化分析品質：[XX/25]
  □ 論文寫作品質：[XX/20]
  □ 誠信查核結果：[XX/10]
  □ 流程效率：[XX/10]
  總分：[XX/100]

---

### 模式 2：resume（斷點續跑）

觸發：「從第 X 階段繼續」/ 「繼續上次的研究」

流程：
- Step 1 → state_tracker_agent
  讀取 pipeline_state.md
  確認目前到哪個階段
  列出已完成的輸出

- Step 2 → orchestrator_agent
  從指定階段繼續
  銜接已有的輸出材料

說明：
適合以下情況：
- 分析結果出問題，需要重跑 Stage 3
- 論文草稿不滿意，需要重寫 Stage 4
- 中途暫停，下次繼續

---

### 模式 3：custom（自定義階段）

觸發：「只跑研究和寫作，跳過分析」
      「跳過文獻綜述，直接寫論文」

流程：
- Step 1 → orchestrator_agent
  確認使用者要跑哪些階段
  確認跳過哪些階段
  說明跳過的風險（若有）

- Step 2 → 按自定義順序執行

注意：
- Stage 3.5 和 Stage 6.5 誠信查核不能跳過
- 若跳過 Stage 3（量化分析），Stage 4 需要手動提供結果表格
- orchestrator_agent 必須說明每個跳過步驟的潛在風險

---

## Anti-Patterns（明確禁止）

| # | 反模式 | 正確做法 |
|---|--------|---------|
| 1 | 強制確認點自動通過 | 必須等使用者明確輸入「繼續」 |
| 2 | 跳過 Stage 3.5 誠信查核 | 誠信查核強制執行，不能跳過 |
| 3 | 跳過 Stage 6.5 誠信查核 | 同上 |
| 4 | 審稿退稿後直接定稿 | 必須回到修改或結束流程 |
| 5 | 不更新 pipeline_state.md | 每個階段必須更新狀態 |
| 6 | CRITICAL 問題繼續往下走 | CRITICAL 必須暫停流程 |
| 7 | 跳過品質評估 | quality_evaluator 必須在每個主要階段後執行 |

---

## Iron Rules（絕對不能違反）

⚠️ IRON RULE 1：強制確認點不能自動通過
每個強制確認點必須等待使用者明確輸入。
不能假設使用者同意，不能自動進入下一階段。

⚠️ IRON RULE 2：Stage 3.5 誠信查核不能跳過
無論使用者是否要求跳過，Stage 3.5 必須執行。
發現 CRITICAL 問題，流程必須暫停。

⚠️ IRON RULE 3：Stage 6.5 誠信查核不能跳過
同上，定稿前必須確認論文是乾淨的。

⚠️ IRON RULE 4：退稿不能直接定稿
審稿結果為 Reject 時，必須與使用者討論下一步，
不能跳過修改直接進入 Stage 7。

⚠️ IRON RULE 5：pipeline_state.md 必須即時更新
每個階段開始和結束時必須更新狀態記錄。
確保任何時候都可以從中斷點繼續。

⚠️ IRON RULE 6：Stata MCP 必須在 Stage 3 前確認連線
Stage 3 開始前必須確認 Stata MCP 連線狀態。
連線失敗不能繼續執行 Stage 3。

⚠️ IRON RULE 7：custom 模式不能跳過誠信查核
即使使用者指定跳過，Stage 3.5 和 Stage 6.5 不能省略。
orchestrator_agent 必須說明原因並堅持執行。

---

## 輸出規範

### 1. 最終輸出物清單（full mode）

| 輸出物 | 檔名 | 格式 |
|--------|------|------|
| 最終論文 | final_paper.docx | .docx |
| 審稿報告 | review_report.docx | .docx |
| 研究日誌 | research_log.md | .md |
| Stata 執行日誌 | stata_log.txt | .txt |
| Pipeline 狀態記錄 | pipeline_state.md | .md |
| 協作品質報告 | quality_report.docx | .docx |

### 2. 階段性輸出

每個階段完成後，告知使用者：
- 本階段完成了什麼
- 主要輸出是什麼
- 下一階段將做什麼
- 強制確認點的提示

### 3. 語言規則

- 使用者用中文 → 全程中文
- 使用者用英文 → 全程英文
- Pipeline 狀態記錄統一使用中文

### 4. 輸出長度

Pipeline 本身的調度輸出保持簡潔，
每個階段的詳細輸出由對應的 Skill 負責。

---

## 版本資訊

| 項目 | 內容 |
|------|------|
| Skill 版本 | 1.0.0 |
| 建立日期 | 2026-05 |
| 目標學科 | 會計學、經濟學 |
| 語言支援 | 簡體中文、繁體中文、英文 |
| 調度的 Skill | deep-research、literature-review、quantitative-analysis、academic-writing、academic-paper-reviewer |
| 授權 | CC-BY-NC 4.0 |
