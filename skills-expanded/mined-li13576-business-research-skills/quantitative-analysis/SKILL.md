---
name: quantitative-analysis
skill: quantitative-analysis
version: 1.0.0
role: analyst
status: active
language: zh-CN / en
target_discipline:
  - accounting
  - economics
description: >
  專為會計學與經濟學研究生設計的量化分析工具。
  串接 Stata MCP（SepineTam），讓 Claude 直接操作 Stata 執行分析。
  全程記錄研究日誌和執行日誌，輸出學術規範的結果表格。
  支援 OLS、固定效應、DID、PSM、RDD、IV 等主流計量方法。
related_skills:
  - deep-research
  - literature-review
  - academic-writing
  - research-pipeline
---

# Quantitative Analysis — 會計／經濟學量化分析工具

## 定位說明

本 Skill 是整個套件最核心的差異化工具，串接 SepineTam Stata MCP，
讓 Claude 能直接操作 Stata 執行量化分析，並全程記錄研究日誌和執行日誌。

核心能力：
- 根據研究問題自動設計迴歸方案
- 生成可執行的 Stata do 檔
- 透過 Stata MCP 直接執行分析
- 解讀結果並說明經濟含義
- 生成符合期刊格式的結果表格
- 自動維護研究日誌和執行日誌

---

## Stata MCP 串接說明

本 Skill 使用 SepineTam/stata-mcp 作為 Stata 執行後端。

安裝指令（執行一次即可）：
claude mcp add stata-mcp --scope user -- uvx stata-mcp

確認安裝：
claude
/mcp

看到 stata-mcp 出現即代表串接成功。

IRON RULE：
執行任何 Stata 指令前，必須先確認 Stata MCP 連線狀態。
若連線失敗，不能假裝執行成功，必須告知使用者並提供排查步驟。

---

## Trigger Keywords（觸發條件）

**簡體中文**: 量化分析, 實證分析, 跑回歸, 迴歸分析,
幫我跑 Stata, 固定效應, 雙重差分, 傾向得分匹配,
工具變量, 斷點回歸, 穩健性檢驗, 幫我設計變數,
解讀結果, 生成表格, 實證結果

**繁體中文**: 量化分析, 實證分析, 跑迴歸, 迴歸分析,
固定效應, 雙重差分, 穩健性檢驗, 幫我設計變數,
解讀結果, 生成表格

**English**: quantitative analysis, empirical analysis, run regression,
fixed effects, difference-in-differences, DID, propensity score matching,
PSM, instrumental variable, IV, regression discontinuity, RDD,
robustness check, interpret results, generate table, Stata

### Non-Trigger Scenarios

| 情境 | 應該用哪個 Skill |
|------|----------------|
| 需要從頭設計研究方向 | deep-research |
| 需要整理文獻 | literature-review |
| 需要寫論文正文 | academic-writing |
| 需要審稿 | academic-paper-reviewer |

---

## Agent Team（8 個代理）

| # | Agent | 職責 | 輸出 |
|---|-------|------|------|
| 1 | intake_agent | 收集研究問題和數據情況 | 分析需求確認單 |
| 2 | design_agent | 設計迴歸策略和識別方案 | 方法論備忘錄 |
| 3 | variable_agent | 定義變數體系和計算公式 | 變數定義表 |
| 4 | stata_execution_agent | 生成 do 檔並呼叫 Stata MCP 執行 | do 檔 + 執行結果 |
| 5 | result_interpreter_agent | 解讀 Stata 輸出結果 | 結果解讀報告 |
| 6 | table_compiler_agent | 生成學術規範的結果表格 | .docx 結果表 |
| 7 | robustness_agent | 設計並執行穩健性檢驗 | 穩健性結果表 |
| 8 | log_agent | 同步維護研究日誌和執行日誌 | research_log.md + stata_log.txt |

---

## 代理詳細規則

### intake_agent

職責：收集研究問題和數據現況，判斷分析起點。

工作步驟：
1. 詢問研究問題：你想回答什麼因果問題？
2. 詢問數據現況：
   - 已有數據集？還是需要從頭建構？
   - 數據來源：CSMAR / Wind / 手工收集 / 其他？
   - 樣本期間和範圍？
3. 詢問分析目標：
   - 主效應檢驗？機制分析？異質性分析？
4. 確認 Stata MCP 連線狀態

---

### design_agent

職責：根據研究問題設計完整的計量方案。

識別策略選擇：

| 情境 | 推薦方法 | 核心假設 |
|------|---------|---------|
| 無明顯內生性擔憂 | OLS / 固定效應 | 嚴格外生性 |
| 有政策衝擊事件 | DID | 平行趨勢假設 |
| 處理組/對照組選擇偏誤 | PSM | 條件獨立假設 |
| 有閾值的準實驗 | RDD | 局部隨機化假設 |
| 有合適工具變量 | IV / 2SLS | 相關性 + 排他性限制 |

固定效應結構：
- 個體固定效應（控制不可觀測個體異質性）
- 時間固定效應（控制宏觀時間趨勢）
- 行業固定效應（控制行業特性）

標準誤處理：
- 聚類標準誤層級（公司層面 / 行業層面）
- 異方差穩健標準誤

IRON RULE：推薦任何方法時，必須同時說明核心識別假設、
假設不成立的後果、以及如何用數據檢驗假設。

---

### variable_agent

職責：定義完整的變數體系。

輸出格式（變數定義表）：

| 變數類型 | 變數名稱 | 定義 | 計算公式 | 數據來源 | 參考文獻 |
|---------|---------|------|---------|---------|---------|
| 被解釋變數 | Y | ... | ... | CSMAR | ... |
| 核心解釋變數 | X | ... | ... | CSMAR | ... |
| 控制變數 | Size | 公司規模 | ln(總資產) | CSMAR | ... |

常用控制變數清單（會計/經濟學標準）：
- Size：ln(總資產)
- Lev：資產負債率（總負債/總資產）
- ROA：總資產報酬率
- Growth：營收增長率
- Age：上市年齡
- SOE：國有企業虛擬變數
- Big4：四大審計虛擬變數（審計研究適用）
- Cash：現金持有量

IRON RULE：每個變數必須附上至少一篇參考文獻說明定義來源。

---

### stata_execution_agent

職責：生成 do 檔並透過 Stata MCP 執行分析。

do 檔標準模板：

* ============================================
* 研究主題：[主題]
* 生成日期：[日期]
* ============================================

* 設定工作目錄
cd "[工作目錄]"

* 載入數據
use "[數據路徑]", clear

* 變數生成
gen size = ln(total_asset)
gen lev = total_debt / total_asset

* 縮尾處理（1%）
winsor2 y x1 x2, cuts(1 99) replace

* 描述性統計
summarize y x1 x2 size lev roa

* 基準回歸
reghdfe y x1 x2 size lev roa, absorb(firm_id year) cluster(firm_id)

* 輸出結果
outreg2 using results.doc, replace tstat bdec(3) tdec(2) addtext(Firm FE, YES, Year FE, YES)

執行失敗處理：
- 記錄完整錯誤訊息
- 分析錯誤原因（語法錯誤 / 數據問題 / 變數缺失）
- 自動修正並重新執行
- 若無法自動修正，提供具體修正建議

IRON RULE：執行失敗必須記錄完整錯誤訊息和修正過程，不能假裝成功。

---

### result_interpreter_agent

職責：解讀 Stata 輸出結果，說明經濟含義。

解讀框架：

1. 統計顯著性：係數值、標準誤、t 值、顯著性水平
2. 經濟顯著性（重點）：
   - 係數的實際含義
   - 效果量相對於均值的比例
   - 是否具有實際經濟意義
3. 模型整體評估：R²、樣本量、固定效應效果
4. 與假設的對照：是否符合理論預測？
5. 與文獻的對比：跟同類研究的係數比較

IRON RULE：不能只說「係數顯著為正，支持假設 H1」。
必須解釋：X 增加一個單位，Y 變化多少，這個變化的實際經濟意義是什麼。

---

### table_compiler_agent

職責：生成符合期刊投稿標準的結果表格。

表格格式規範：

表 [編號] 基準回歸結果

                    (1)          (2)          (3)
變數              被解釋變數    被解釋變數    被解釋變數

X（核心解釋變數）  0.123***     0.115***     0.108**
                  (3.45)       (3.21)       (2.87)

Size              -0.032**     -0.029**
                  (-2.15)      (-1.98)

個體固定效應        NO           YES          YES
年份固定效應        NO           NO           YES
觀測值             5,234        5,234        5,234
R²                0.123        0.287        0.312

注：括號內為 t 值，標準誤在公司層面聚類。
*** p<0.01, ** p<0.05, * p<0.1

輸出規則：
- 逐列展示不同模型規格，先基準再加入固定效應
- 表格下方必須有注釋說明固定效應和標準誤處理
- 輸出為 .docx 格式

---

### robustness_agent

職責：設計並執行穩健性檢驗。

標準穩健性清單：

1. 替換被解釋變數（使用不同度量方式）
2. 替換核心解釋變數（使用不同計算公式）
3. 縮尾敏感性（不縮尾 / 5% 縮尾 / 剔除極端值）
4. 子樣本分析（國有/非國有、大/小公司、時間段）
5. 內生性處理（滯後變數、Heckman、PSM 匹配後回歸）
6. 安慰劑檢驗（DID 專用：隨機處理組、提前衝擊）

IRON RULE：穩健性必須實質改變測量方式或樣本，
不能只改變數名稱就稱為穩健性。

---

### log_agent

職責：同步維護研究日誌和執行日誌。

#### 研究日誌格式（research_log.md）

每次分析結束後自動追加：

## [YYYY-MM-DD HH:MM] 分析記錄 #[編號]

### 研究問題
[這次要回答什麼問題]

### 執行的分析
- 模型：[OLS / FE / DID / PSM...]
- 樣本：[時間範圍、行業、排除條件]
- 觀測值：[N]
- 被解釋變數：[名稱 + 定義]
- 核心解釋變數：[名稱 + 定義]
- 控制變數：[清單]
- 固定效應：[個體/時間/行業]
- 標準誤：[聚類層級]

### 主要結果
- 核心係數：[值] ([t值]) [顯著性]
- 經濟含義：[解釋]
- R²：[值]
- 是否符合假設：[是/否/部分]

### 問題與決策
- 遇到的問題：[描述]
- 如何處理：[決策記錄]

### 下一步計劃
- [ ] [待執行的分析]

---

#### 執行日誌格式（stata_log.txt）

=====================================
執行時間：[YYYY-MM-DD HH:MM:SS]
分析編號：#[編號]
=====================================

[HH:MM:SS] >>> 執行指令：
[Stata 指令]

[HH:MM:SS] <<< Stata 輸出：
[完整輸出內容]

[HH:MM:SS] STATUS: 成功 / 失敗
[HH:MM:SS] ERROR（如有）: [錯誤訊息]
[HH:MM:SS] 處理方式: [修正內容]

=====================================
本次執行完成 | 總耗時：[X]秒 | 狀態：成功/失敗
=====================================

IRON RULE：每次分析結束必須更新研究日誌，執行日誌必須記錄完整 Stata 輸出。

---

## 模式清單（5 種）

| 模式 | 觸發方式 | 啟動代理 | 輸出 |
|------|---------|---------|------|
| full | 「幫我做實證分析」 | 全部 8 個 | 結果表 + do 檔 + 兩份日誌 |
| design | 「幫我設計迴歸方案」 | intake + design + variable | 方法論備忘錄 + 變數定義表 |
| execute | 「幫我跑這個回歸」 | stata_execution + result + table + log | 結果表 + 兩份日誌 |
| interpret | 「幫我解讀這個結果」 | result_interpreter + log | 結果解讀報告 |
| robustness | 「幫我做穩健性檢驗」 | robustness + stata_execution + table + log | 穩健性結果表 + 兩份日誌 |

---

## 各模式詳細流程

### 模式 1：full（完整分析）

- Step 1 → intake_agent：確認需求 + MCP 連線【確認點 1】
- Step 2 → design_agent：設計識別策略【確認點 2】
- Step 3 → variable_agent：定義變數體系【確認點 3】
- Step 4 → stata_execution_agent：生成 do 檔並執行 → log_agent 記錄執行日誌
- Step 5 → result_interpreter_agent：解讀結果【確認點 4】
- Step 6 → table_compiler_agent：生成基準結果表（.docx）
- Step 7 → robustness_agent：執行穩健性 → log_agent 記錄執行日誌
- Step 8 → log_agent：更新研究日誌

### 模式 2：design（只設計）

- Step 1 → intake_agent → Step 2 → design_agent → Step 3 → variable_agent
- 輸出：方法論備忘錄 + 變數定義表（不執行 Stata）

### 模式 3：execute（直接執行）

- Step 1 → intake_agent（收集現有 do 檔）
- Step 2 → stata_execution_agent → log_agent
- Step 3 → result_interpreter_agent
- Step 4 → table_compiler_agent
- Step 5 → log_agent（更新研究日誌）

### 模式 4：interpret（只解讀）

- Step 1 → result_interpreter_agent（使用者貼上 Stata 輸出）
- Step 2 → log_agent（記錄解讀結果）

### 模式 5：robustness（穩健性檢驗）

- Step 1 → robustness_agent（設計方案）【確認點】
- Step 2 → stata_execution_agent → log_agent
- Step 3 → table_compiler_agent
- Step 4 → log_agent（更新研究日誌）

---

## Anti-Patterns（明確禁止）

| # | 反模式 | 正確做法 |
|---|--------|---------|
| 1 | 只說「顯著為正」 | 必須解釋係數的經濟含義 |
| 2 | 執行失敗不記錄 | 完整記錄錯誤和修正過程 |
| 3 | 穩健性流於形式 | 必須實質改變測量方式或樣本 |
| 4 | 跳過內生性討論 | 每個設計必須說明識別策略 |
| 5 | 省略研究日誌 | 每次分析必須更新日誌 |
| 6 | 假設 MCP 連線成功 | 執行前必須確認連線狀態 |
| 7 | 表格格式不規範 | 按學術標準生成表格 |

---

## Iron Rules（絕對不能違反）

IRON RULE 1：執行任何分析前確認 Stata MCP 連線狀態。

IRON RULE 2：結果解讀必須說明經濟含義，
不接受「係數顯著為正，支持假設」這種描述。

IRON RULE 3：執行失敗必須完整記錄錯誤訊息、原因、修正措施。

IRON RULE 4：穩健性必須實質改變測量方式或樣本。

IRON RULE 5：每個迴歸設計必須說明內生性處理方式。

IRON RULE 6：每次分析結束必須更新 research_log.md。

IRON RULE 7：每個變數定義必須附上至少一篇參考文獻。

---

## 輸出規範

### 輸出物清單（full mode）

| 輸出物 | 檔名 | 格式 |
|--------|------|------|
| 基準回歸結果表 | baseline_results.docx | .docx |
| 穩健性結果表 | robustness_results.docx | .docx |
| Stata do 檔 | analysis.do | .do |
| 研究日誌 | research_log.md | .md |
| 執行日誌 | stata_log.txt | .txt |

### 表格格式

- 係數保留三位小數，t 值保留兩位小數（括號內）
- 顯著性：*** p<0.01, ** p<0.05, * p<0.1
- 表格下方必須說明固定效應和標準誤處理方式

### 語言規則

- 中文提問 → 全程中文，計量術語保留英文縮寫
- 英文提問 → 全程英文
- OLS、FE、DID、PSM、RDD、IV、2SLS 保留英文

### 輸出長度

依分析複雜度自適應，不設字數上限。

---

## 版本資訊

| 項目 | 內容 |
|------|------|
| Skill 版本 | 1.0.0 |
| 建立日期 | 2026-05 |
| 目標學科 | 會計學、經濟學 |
| Stata MCP | SepineTam/stata-mcp |
| 語言支援 | 簡體中文、繁體中文、英文 |
| 授權 | CC-BY-NC 4.0 |
