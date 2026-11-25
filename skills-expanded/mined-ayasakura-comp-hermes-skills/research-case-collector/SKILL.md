---
name: research-case-collector
description: 將使用者提供的模型失敗對話整理成去識別化、可追溯的 agentic LoRA 候選資料，驗證資料並回報距離 pilot／正式訓練門檻還差幾筆。使用者說「收集案例」、「整理成訓練資料」、「加入查證資料集」或要求更新並上傳 Qwen 搜尋查證案例時使用。
---

# Research Case Collector

把真實失敗事件轉成可審查的訓練候選，不把摘要、舊 Agent 自稱查證或使用者推測冒充事實。

## 預設位置

- Canonical private repo：`/home/chihmin/backups/qwen-agentic-lora-audit`
- Dataset：`datasets/v12-search-diligence/`
- Validator：`scripts/validate_dataset.py`（相對於本 skill）
- 收集模板：[assets/incident-template.md](assets/incident-template.md)
- 欄位與分流：[references/schema.md](references/schema.md)

若路徑不存在，先詢問使用者要建立新資料集還是指定其他 repo；不要猜遠端 URL。

## 必守界線

1. 資料整理、來源查證、訓練、部署、上傳是不同授權。只做使用者這次明確允許的階段。
2. 涉及日期、相對時間或營業狀態時先取權威時間；保留時區與原始精度，不補造秒數。
3. 私人對話預設去識別化；原始私人匯出不上傳，除非使用者明確要求且確認 repo visibility。
4. 舊 Agent 說「查證過」、搜尋摘要、使用者推測都不是來源證據。
5. 沒有 raw tool output／來源節錄時，只能建立 `safe_prefix`、`clarification` 或 `direct_no_tool`；不可編造 tool result 或 grounded final answer。
6. 同一對話所有 prefix 視為一個 trajectory，不能跨 train／validation／heldout。
7. JSONL row 數不等於獨立資料筆數；readiness 一律按 independent trajectory 計算。
8. 達到數量門檻仍不等於獲准訓練。必須另做 dataset review、tokenizer/mask gates、split 檢查、GPU preflight，並取得明確 training authorization。

## 流程

### 1. 接收與標準化

- 接受自然對話、Markdown 摘要、JSON 或截圖轉錄。
- 保留使用者原句；Assistant 若只有摘要就標記 `summarized_not_verbatim`。
- 校對日期／星期／跨日，但不得改寫原本語意。
- 將名稱換成 `participant-NNN`；移除 token、Email、電話、私人地址、session ID 等識別資料。

### 2. 判斷資料路徑

每一事件只能按證據強度選擇：

- `grounded completion`：已有可追溯來源，且來源實際支持答案。
- `safe prefix`：只監督下一個正確行動，如澄清、`gettime`、`web_search` 或 `crawl`。
- `direct_no_tool`：穩定知識、翻譯、運算等反例。
- `clarification`：人物、地點、時間、範圍不足。
- `quarantine`：事實衝突、來源缺失、隱私風險或測試保留。

先讀 [references/schema.md](references/schema.md) 再建立資料。

### 3. 寫入候選池

每案至少建立：

- `source/case-NNN.md`
- `cases/case-NNN.json`
- `trainable/candidates.jsonl` 的零到多個 rows
- 更新 `manifest.json`

只監督 assistant span；tool result、system、user 內容不得設為 target。沒有真實工具結果時，安全 prefix 必須停在 assistant tool call。

### 4. 驗證與回報缺口

在 canonical repo 根目錄執行：

```bash
python3 skills/research-case-collector/scripts/validate_dataset.py \
  datasets/v12-search-diligence \
  --output readiness-report.json
python3 skills/research-case-collector/scripts/validate_dataset.py \
  datasets/v12-search-diligence \
  --verify-published
python3 skills/research-case-collector/tests/test_validate_dataset.py -v
```

回報至少包含：

- 新增 independent trajectories
- 新增 trainable rows
- grounded completion／safe prefix／quarantine 數
- bounded pilot 尚差幾筆及各 bucket 缺口
- full candidate 尚差幾筆
- 本次沒做的階段（來源查證、訓練、部署等）

### 5. 上傳（僅在明確授權時）

- 確認 remote 與 repo visibility，不把 credential 或原始私人聊天放入 commit。
- 跑測試、validator、secret scan 與獨立 code/data review。
- review 通過後才 commit/push；push 後確認 `HEAD == origin/main`。
- 若 private repo 權限不足，保留本機 commit 並如實回報，不能宣稱已上傳。

## 呼叫方式

```text
/skill:research-case-collector <貼上新的失敗對話或事件摘要>
```

若使用者只貼案例但未要求上傳，預設只整理到本機候選池並回報 readiness，不自動 push、不啟動訓練。
