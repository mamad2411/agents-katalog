---
name: compute-gate
description: >
  用在把實驗升到下一個 Compute Gate 級別之前（L0 理論檢查到 L5 完整執行），
  或 pilot／消融的結果出來、要決定走不走下去的時候。它強制逐級推進，
  並確定性地檢查中止與升級規則。觸發語：「可以放大規模了嗎」、
  「跑完整實驗」、「這個 run 該不該中止」。
---

# Compute Gate

`AGENTS.md` 定義的六級：L0 理論／靜態檢查 → L1 合成資料／確定性測試 → L2 小型資料集 → L3 小規模試跑 → L4 消融／敏感度分析 → L5 完整規模執行。這個技能負責機械判定「現在能不能升到下一級」，不負責決定「這個實驗到底有沒有前途」——那是 evidence-review／compare-runs／claim-audit 的事。

## 核心規則：不准跳級，門檻凍結在 Contract

`experiment_records compute-gate` 只認 `L0→L1→L2→L3→L4→L5` 這個順序，跳一級就直接擋（exit code 2），沒有例外，也沒有「這次先跳過 pilot 直接跑 full」這種選項——昂貴的實驗不是預設權利，這是規則 12 講的。

Contract 裡的 `scale_up_rule`／`abort_rule` 是自然語言，例如「pilot recall 提升 > 3pp 才跑 full」。**你要自己把這句話翻成 `compute_cascade` 的欄位**，而且翻完之後跟 Contract 一起凍結：

```json
{
  "stage": "main", "level": "L4",
  "budget": { "max_wall_clock_seconds": 5400, "max_cost_usd": 18.0, "max_runs": 4 },
  "promotion": {
    "metric": "recall_at_10", "source": "comparison", "field": "absolute_diff",
    "comparator": ">=", "threshold": 0.03
  },
  "abort": {
    "metric": "latency_ms", "source": "run", "field": "value",
    "run_scope": "all",
    "comparator": ">", "threshold": 400, "reason": "延遲超過 guardrail，這條路線終止"
  }
}
```

翻得對不對是你的責任，`experiment_records compute-gate` 不判斷「0.03 這個門檻合不合理」。但翻譯只做一次，寫進 Contract，之後同一組紀錄重跑會得到同一個判定——門檻散在某次呼叫的命令列參數裡，就沒有這個性質。

`stage` 是研究階段（`preflight`／`pilot`／`main`／`replication`／`independent_review`），`level` 是花多少算力。兩個是不同的軸，所以分開記。

## 用法

```bash
uv run --project .agents/tools/experiment-records python -m experiment_records compute-gate \
  records/experiments/gates/<experiment_id>.json \
  --contract records/experiments/definitions/<experiment_id>.json \
  --request-level L4 \
  --comparison records/experiments/comparisons/<xxx>.json \
  --run records/experiments/runs/<pilot-baseline>.json \
  --run records/experiments/runs/<pilot-treatment>.json
```

第一個 `gate-state.json` 參數同時是唯一輸入與唯一寫入目標；命令原子更新它，不接受第二個 `--output` 路徑。`--run` 可以重複。預算檢查與 `source` 為 `run` 的規則都靠它；`source` 為 `comparison` 的規則要 `--comparison`。

Contract 的 `evidence_policy.eligible_run_stages` 定義哪些 run stage 可作正式證據。Gate 會重查所有輸入 run。status、stage、experiment、run ID 或 lineage 有問題時，Gate 會 fail closed。`source: run` 的規則必須設定 `run_scope`：`baseline`、`treatment` 或 `all`。Promotion 對所選 runs 使用 `all`；abort 使用 `any`。History 的 `run_ids` 只由實際 `--run` 輸入推導。沒有 `--run-ids` 參數。

判定順序固定：`sequence` → `evidence` → `abort` → `budget` → `promotion`，任一步失敗就停。中止檢查排在升級檢查前面，因為升級條件過了也不能蓋過中止條件。

取不到值時判 `failed`，不判通過——「不知道」不等於「符合」。

## 讀結果

- `PASSED`：`current_level` 更新，可以往下一級走。
- `FAILED`：這次帶的證據不夠，`current_level` 不動，可以補證據後重新申請同一級——不是死路。
- `ABORTED`：abort_rule 觸發，這條路線終止。後續申請一律拒絕且不再追加 history；不要繞過去改參數重跑。

`gate-state.json` 是可更新的狀態投影，不是不可變 event 檔；每次以原子替換寫入，但 `history` 只能附加，既有項目不得修改或刪除。失敗與中止的申請也必須保留。

每一筆 `history` 帶 `checks`，逐項記下這次做了哪些檢查與各自的數字。決定要能回溯到數字，不能只留一句結論。要驗證判定可重現，用 `--decided-at` 固定時間戳重跑，比對兩次的 `history` 最後一筆。
