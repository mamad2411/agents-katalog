---
name: hypothesis-test
description: >
  執行假設驅動的量化研究。強制 H0/H1 陳述 → 統計設計 → 數據查詢 → 顯著性檢定 →
  效果大小 → 結構化輸出。適用於驗證新的 alpha 因子、比較議員/院別績效差異、
  評估信號增強效果、探索交易模式。
  觸發詞: 假設, hypothesis, 統計驗證, 顯著性, p-value, 回測新因子, 驗證,
  statistical test, 因子檢定, 相關性分析, 差異分析, 研究驗證, alpha 驗證,
  是否顯著, RB研究, 假說檢定, 變數影響, factor test, validate signal
---

# Hypothesis Test — 量化假設驗證工作流程

本 Skill 用於對 PAM 資料庫中的交易信號進行嚴格的統計假設檢定。
每次研究必須遵循以下 6 步驟，不可跳過。

## 資料庫位置

`data/data.db` (SQLite, read-only 模式查詢)

## Step 1: 假設陳述

**在執行任何查詢之前**，先明確陳述:

```
H0 (虛無假設): [兩組無差異 / 無相關 / 無效果]
H1 (研究假設): [具體的方向性假設]
顯著水準: α = 0.05 (除非使用者指定)
```

範例:
- H0: Senate 與 House 議員的 expected_alpha_20d 無差異
- H1: Senate 議員的 expected_alpha_20d 顯著高於 House

如果使用者沒有明確說出假設，根據他們的問題推導並確認。

## Step 2: 統計設計

根據假設類型選擇方法:

| 研究問題 | 推薦方法 | Python 函數 |
|----------|----------|-------------|
| 兩組均值比較 | Independent t-test 或 Mann-Whitney U | `scipy.stats.ttest_ind` / `mannwhitneyu` |
| 多組均值比較 | One-way ANOVA 或 Kruskal-Wallis | `scipy.stats.f_oneway` / `kruskal` |
| 兩變數相關 | Pearson r 或 Spearman rho | `scipy.stats.pearsonr` / `spearmanr` |
| 比例差異 | Chi-squared test | `scipy.stats.chi2_contingency` |
| 回歸分析 | OLS | `statsmodels.api.OLS` |

**選擇 parametric vs non-parametric**: 先用 Shapiro-Wilk 檢查正態性 (n<5000)。
p < 0.05 → 非正態 → 用 non-parametric。

報告: 選擇的方法 + 理由。

## Step 3: 數據查詢與樣本驗證

用 Python 查詢 `data/data.db`，**先報告樣本描述統計再執行檢定**:

```python
python -c "
import sqlite3, json
conn = sqlite3.connect('file:data/data.db?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# 替換為實際查詢
cur.execute('''
    SELECT chamber, expected_alpha_20d
    FROM alpha_signals
    WHERE expected_alpha_20d IS NOT NULL
''')
rows = cur.fetchall()
# ... 計算描述統計
conn.close()
"
```

**驗證清單** (必須全部通過才進 Step 4):
- [ ] 總樣本 n ≥ 30 (否則警告統計檢力不足)
- [ ] 每組 n ≥ 15
- [ ] 遺漏值比率 < 20%
- [ ] 無明顯的 data leakage

如果驗證不通過，報告問題並建議替代方案（放寬條件/換方法/等更多數據）。

## Step 4: 統計檢定執行

用外部腳本或 inline Python 執行統計檢定。

```bash
python .claude/skills/hypothesis-test/scripts/stat_test.py \
  --db data/data.db \
  --query "SELECT ..." \
  --method ttest \
  --group-col chamber \
  --value-col expected_alpha_20d
```

如果腳本不可用，用 inline Python + scipy:

```python
python -c "
import sqlite3
import numpy as np
from scipy import stats

conn = sqlite3.connect('file:data/data.db?mode=ro', uri=True)
# ... 查詢和計算
# 輸出: test_statistic, p_value, effect_size, ci_95
conn.close()
"
```

**必須報告**:
1. 統計量 (t / F / U / chi2 / r)
2. p-value (精確到 4 位小數)
3. 效果大小 (Cohen's d / eta² / r² / Cramér's V)
4. 95% 信賴區間
5. 樣本大小 (每組)

## Step 5: 結果解讀

**三層解讀** (缺一不可):

### 5a. 統計結論
- p < α → 拒絕 H0，差異統計顯著
- p ≥ α → 無法拒絕 H0

### 5b. 效果大小解讀
| Cohen's d | 解讀 | 交易意義 |
|-----------|------|----------|
| < 0.2 | 微弱 | 可能不值得交易成本 |
| 0.2-0.5 | 小 | 大量交易可累積 |
| 0.5-0.8 | 中等 | 值得納入策略 |
| > 0.8 | 大 | 高優先級因子 |

### 5c. 業務意義
- 這對 PAM 的交易策略意味著什麼？
- 是否需要修改現有模組？如果是，哪個模組？
- 是否與先前研究 (RB-001~007) 一致或矛盾？

**RB-006 教訓**: 統計顯著 ≠ 方向正確。SQS conviction 與 alpha 顯著相關 (p<0.05)
但方向是**負的** (r=-0.51)。永遠報告效果的方向，不只是顯著性。

## Step 6: 結構化輸出

以下格式輸出研究結果:

```markdown
# [研究標題] (RB-XXX)

**執行時間**: YYYY-MM-DD HH:MM
**資料庫**: data/data.db (congress_trades: N筆, alpha_signals: N筆)

## 假設
- H0: [虛無假設]
- H1: [研究假設]
- α = 0.05

## 方法
- 統計方法: [方法名稱]
- 選擇理由: [為何選此方法]
- 樣本: n₁=[X], n₂=[Y]

## SQL 查詢
[完整 SQL，可重現]

## 描述統計
| 組別 | n | Mean | Std | Median | Min | Max |
|------|---|------|-----|--------|-----|-----|

## 統計結果
| 指標 | 數值 |
|------|------|
| 統計量 | ... |
| p-value | ... |
| 效果大小 | ... |
| 95% CI | [..., ...] |

## 結論
- 統計結論: [拒絕/無法拒絕 H0]
- 效果大小: [微弱/小/中等/大]
- 業務意義: [對 PAM 交易策略的影響]
- 限制: [樣本偏差、時間範圍、數據品質]

## 後續行動
- [ ] [具體建議]
```

如果使用者要求存檔，存入 `docs/research/RB-XXX_[主題].md`。
RB 編號延續現有序列 (目前最新 RB-012)。

## PAM 研究背景 (快速參考)

載入詳細背景: Read `.claude/skills/hypothesis-test/references/pam-research-context.md`

**已驗證的關鍵發現**:
- Buy alpha: +0.77% CAR_5d, +1.10% CAR_20d (59.2% WR) [RB-001/004]
- Sale: 反向 alpha (contrarian) [RB-001]
- Senate > House: +1.39% vs -1.27% 20d [RB-004]
- $15K-$50K 最強: +93% vs $1K-$15K [RB-001/Quant]
- SQS conviction: r=-0.51 負預測 [RB-006]
- PACS Q4/Q1 = 3.04x [RB-006/Quant]
- Filing lag <15d: 4.6x alpha [Quant]
- Convergence: +36% EA20d premium [Quant]
- VIX Goldilocks 14-16: best regime [RB-004]
