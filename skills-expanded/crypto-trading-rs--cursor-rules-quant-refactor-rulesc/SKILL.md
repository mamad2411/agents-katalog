---
description: Must-follow constraints for /quant-refactor. Readability-first, user-centric refactoring with rich documentation and explicit performance trade-off tracking.
globs: python/pairs_eda/**,python/tests/**,reference/python_pairstrading/**
alwaysApply: false
---

# Quant Refactor — Hard Rules

> These constraints apply to ALL code refactored by `/quant-refactor`.
> Priority order: **Readability > Correctness documentation > Performance**.

## ⚠ ABSOLUTE CONSTRAINT: Do NOT Change Logic

**Refactoring = structural improvement ONLY. Never change what the code does.**

- NO changing formulas, thresholds, financial constants, or algorithm logic
- NO reordering operations that would produce different numerical results
- NO replacing one algorithm with a "better" one (e.g., switching correlation method)
- NO "fixing" what looks like a bug — flag it in a comment, leave the code unchanged
- Performance trade-offs (PERF-NNN) are acceptable. Logic changes are NOT.

If the existing code computes `X`, the refactored code MUST compute exactly `X` — same inputs, same outputs, bit-for-bit.

---

## 1. Extract Functions — Make Code Scannable

- **Multi-line inline scripts (≥5 lines of cohesive logic) → extract into a named function.**
- The function name should read like a sentence: `filter_pairs_by_overlap()`, not `process()`.
- Extracted functions go into the appropriate `python/pairs_eda/` module, then **import at call site**.
- Notebook cells should read like a high-level outline:

```python
# GOOD — scannable, hover-friendly
from pairs_eda.correlation import filter_pairs_by_overlap, apply_dual_condition

candidates = filter_pairs_by_overlap(data, min_years=5)
final_pairs = apply_dual_condition(candidates, recent_years=3)
```

```python
# BAD — logic buried inline
min_periods = int(5 * 252)
full_corr = data.pct_change().corr(min_periods=min_periods)
n = full_corr.shape[0]
mask = np.triu(np.ones((n, n), dtype=bool), k=1)
# ... 20 more lines ...
```

---

## 2. Hover-Friendly Docstrings — The IDE Is the Documentation

Every extracted function MUST have a docstring designed for **mouse-hover preview**.
The first 3-5 lines should give the reader everything they need without clicking through.

**Required structure:**

```python
def calculate_rolling_zscore(
    spread: pd.Series,
    window: int = 60,
) -> pd.Series:
    """Rolling Z-score of a spread series for mean-reversion signal detection.

    ┌─────────────────────────────────────────────┐
    │  spread[t] - rolling_mean(spread, window)   │
    │  ─────────────────────────────────────────   │
    │       rolling_std(spread, window)            │
    └─────────────────────────────────────────────┘

    Flow:
        raw spread → rolling mean/std (window) → Z-score → signal

    Args:
        spread: Price spread between two tickers (A - β*B).
        window: Lookback period in trading days. Default 60 ≈ 3 months.

    Returns:
        Z-score series. NaN for first (window-1) rows.

    Performance note:
        Uses two separate .rolling() calls instead of .rolling().apply(lambda).
        ~10x faster but creates one extra intermediate Series in memory.
        See: PERF-001 in this docstring.

    Example:
        >>> zscore = calculate_rolling_zscore(spread, window=60)
        >>> entries = zscore[zscore.abs() > 2.0]
    """
```

---

## 3. ASCII Logic Diagrams in Docstrings

For functions with multi-step logic, include a **text-based flow diagram**.
This is the most valuable part of hover preview — a visual at-a-glance understanding.

**Patterns to use:**

```python
"""
Pipeline:
    prices ──→ pct_change() ──→ .corr(min_periods) ──→ upper triangle ──→ filter band
                  │                     │                                      │
              NaN row 0          NaN if overlap < min              [0.40, 0.85]

Decision tree:
    full_corr in band?
    ├── NO  → exclude
    └── YES → recent_corr in band?
              ├── NO  → exclude (degraded relationship)
              └── YES → ✓ candidate pair
"""
```

---

## 4. Readability > Performance (with Tracking)

Readability is the primary goal. Performance MAY be sacrificed if it improves clarity.

**BUT: every performance trade-off MUST be documented** with a tag for future optimization.

```python
# PERF-001: Using explicit intermediate variable for clarity.
# A single chained expression would avoid this ~2MB copy.
# To optimize: returns = prices.pct_change(); corr = returns.corr(...)
rolling_mean = spread.rolling(window).mean()
rolling_std = spread.rolling(window).std()
zscore = (spread - rolling_mean) / rolling_std
```

**Tag format:** `PERF-NNN` (sequential within the file).

Each function's docstring should list its performance notes:

```python
"""
Performance notes:
    PERF-001: Intermediate variable for rolling_mean (~2MB copy). Chainable.
    PERF-002: Python loop over pairs instead of matrix op. O(n²) → O(n) possible.
"""
```

---

## 5. Comment Philosophy — Explain the WHY and the SHAPE

- **DO** comment: mathematical rationale, business logic, non-obvious constraints, "why this threshold"
- **DO** comment: data shape transformations (`# (dates × tickers) → (pairs × corr_value)`)
- **DO** comment: units and ranges (`# Z-score: typically [-4, +4], mean-reverting to 0`)
- **DON'T** comment: obvious operations (`# increment counter`, `# return result`)

```python
# 252 trading days/year — converts year-based parameter to row count
# for .corr(min_periods=...) which operates on DataFrame rows
min_periods = int(min_overlap_years * 252)

# Upper triangle only: avoid (A,B) and (B,A) duplicates
# np.triu with k=1 excludes the diagonal (self-correlation = 1.0)
mask = np.triu(np.ones((n, n), dtype=bool), k=1)
```

---

## 6. Naming — Code Reads Like English

- Functions: `verb_noun()` — `filter_pairs_by_overlap()`, `calculate_rolling_zscore()`
- Variables: descriptive, no abbreviations — `correlation_matrix` not `corr_mat`, `trading_days_per_year` not `tdy`
- Exception: universally known abbreviations are OK — `df`, `np`, `pd`, `n`, `i`, `j`
- Boolean variables: `is_*` or `has_*` — `is_valid_pair`, `has_sufficient_overlap`

---

## 7. Do NOT Change Math (Reinforcement of Absolute Constraint)

This repeats the top-level constraint for emphasis within the checklist.

- Refactoring is **structural**, not **logical**. Same inputs → same outputs.
- If mathematical logic looks wrong → **flag it in a `# REVIEW:` comment**, do NOT change it.
- If an algorithm could be better → **flag it in a `# REVIEW:` comment**, do NOT change it.
- Changes to formulas, thresholds, or financial logic require **explicit user approval via `/quant-coding`**.

```python
# REVIEW: This threshold (2.0) may be suboptimal for high-volatility pairs.
# Consider regime-adaptive thresholds (see docs/pipeline-backlog.md).
# Logic unchanged per refactor policy — use /quant-coding to modify.
ENTRY_ZSCORE_THRESHOLD = 2.0
```
