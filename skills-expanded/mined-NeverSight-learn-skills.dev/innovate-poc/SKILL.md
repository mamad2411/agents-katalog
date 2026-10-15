---
name: innovate-poc
description: "創新 Phase 3：POC 原型實作。產出可執行的 proof-of-concept 程式碼。Use when 'build POC', 'prototype', '做原型', 'proof of concept'."
agent: general-purpose
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, Task
---

# /innovate-poc — POC 原型實作

讀 `docs/innovation_state.json` 取得掃描和映射結果，自主建立 POC。

## POC 原則

- **最小可行** — 只實作核心邏輯
- **可測量** — 必須產出可比較的數字（CAR, hit rate, alpha vs SPY）
- **可重現** — 記錄所有參數和資料版本
- **Anti look-ahead bias** — 使用 filing_date, benchmark=SPY

## Step 1: 建立 POC 目錄

```
poc/
└── YYYY-MM-DD-<topic>/
    ├── README.md          # 說明與結論
    ├── poc_<topic>.py     # 主程式
    ├── requirements.txt   # 額外依賴（如有）
    └── results/           # 輸出結果
```

## Step 2: 寫 POC 程式碼

```python
"""
POC: [Topic]
Date: [YYYY-MM-DD]
Author: PAM Innovation Engine

Hypothesis: [一句話]
Expected: [預期結果]
Anti look-ahead bias: [如何確保]
"""
import sqlite3
import pandas as pd
from src.config import DB_PATH

# ===== CONFIG =====
TOPIC = "[topic]"
DB = DB_PATH
BENCHMARK = "SPY"
EVENT_DATE_COL = "filing_date"  # 必須用 filing_date

# ===== DATA =====
conn = sqlite3.connect(DB)
trades = pd.read_sql("SELECT * FROM congress_trades WHERE ticker IS NOT NULL", conn)

# ===== IMPLEMENTATION =====
# ... minimal core logic ...

# ===== EVALUATION =====
# Must output: CAR_5d, CAR_20d, hit_rate, sample_size, p_value
# Compare with baseline: RB-001 Buy CAR_5d = +0.77%
```

## Step 3: 執行測試

```bash
# 確保不破壞現有測試
pytest tests/ -v

# 執行 POC
cd poc/YYYY-MM-DD-<topic>/
python poc_<topic>.py
```

## Step 4: 記錄結果

寫 `poc/YYYY-MM-DD-<topic>/README.md`：

```markdown
# POC: [Topic]

## Hypothesis
[一句話]

## Setup
- Data: congress_trades from data/data.db
- Period: [start] to [end]
- Sample: [N] trades
- Benchmark: SPY

## Results
| Metric | Value | vs Baseline |
|--------|-------|-------------|
| CAR_5d | X.XX% | [+/-] vs RB-001 0.77% |
| CAR_20d | X.XX% | [+/-] vs RB-001 0.79% |
| Hit Rate | X% | [+/-] vs 55% baseline |
| p-value | X.XXX | [sig/not sig] |

## Conclusion
[2-3 句]

## Bias Compliance
- [x] Event date = filing_date
- [x] Benchmark = SPY
- [x] No future information used
- [x] Sample size >= 30
```

## Step 5: 輸出

更新 `docs/innovation_state.json` 的 poc phase 為 done。

```markdown
## POC Report: [Topic]

- Directory: `poc/YYYY-MM-DD-<topic>/`
- Key metric: [CAR/hit_rate/etc.] = [value]
- Baseline comparison: [+/- delta vs RB-001]

### Next: `/innovate-verdict`
```
