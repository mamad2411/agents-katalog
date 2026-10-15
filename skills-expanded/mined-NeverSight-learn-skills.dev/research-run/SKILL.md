---
name: research-run
description: "研究 Phase 3：實作程式碼、執行回測、驗證結果。Use when 'run experiment', '跑回測', 'run research'."
agent: general-purpose
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, Task
---

# /research-run — 實作 + 執行

讀 `docs/research_state.json` 取得實驗設計，自主完成實作和執行。

## Step 1: 實作程式碼

根據 research-design 的 Implementation Path 撰寫程式碼。

**必須遵守**：
- 使用 `filing_date` 作為事件日（非 transaction_date）
- Benchmark = SPY 同期報酬
- 樣本量需 ≥ 30
- Anti look-ahead bias：不使用事件日後才能知道的資訊
- 標記清楚實驗變更（`# EXPERIMENT: ...` 註解）

## Step 2: 執行驗證

```bash
# 確保沒破壞現有測試
pytest tests/ -v

# 執行實驗腳本
python <script>.py
```

## Step 3: Git 管理

```bash
# 建立 research branch（如尚未建立）
git checkout -b research/<topic> 2>/dev/null || git checkout research/<topic>
git add -A && git commit -m "research: <topic> experiment setup"
git push -u origin research/<topic>
```

## Step 4: 數據收集

根據實驗類型收集結果：

**Event Study 路徑**：
```python
# 使用 alpha_backtest.py 框架
from src.alpha_backtest import EventStudyBacktester
backtester = EventStudyBacktester()
results = backtester.run(trades_df, windows=[5, 20, 60])
```

**統計檢定路徑**：
```python
# 使用 stat_test.py 框架
from tests.stat_test import run_test
result = run_test(control_group, treatment_group, test='mann_whitney')
```

## Step 5: 輸出執行報告

```markdown
## Execution Report: [Topic] (RB-[XXX])

- Branch: `research/<topic>`
- Script: [filename]
- Trades analyzed: [N]
- Data period: [start] to [end]

### Code Changes
- [列出修改的檔案和關鍵變更]

### Tests
- pytest: [PASS/FAIL] ([N] tests)

### Preliminary Results
- [初步數字，供 /research-analyze 深度分析]

### Next: `/research-analyze`
```

更新 `docs/research_state.json` 的 `run` phase 為 done。

## Important

- **Event Study 用 yfinance 取股價** — 注意 API rate limit
- **Fama-French 用 `src/fama_french.py`** — factor data cached in `data/ff_factors_daily.csv`
- **所有 SQL 查詢用 `src/database.py` 的 `get_connection()`**
