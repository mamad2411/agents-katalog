---
name: garch-volatility-toolkit
description: >-
  Walk-forward GARCH(1,1) and GJR(1,1) volatility forecasting for portfolio construction.
  Recipes for univariate fits, DCC correlation, and position-sizing overlays.
  Campaign results: GJR vol-scaling +0.45 Sharpe (2bps), DCC de-weighting +0.05 Sharpe.
  No-lookahead discipline. Real data on BTC/ETH/SOL/AVAX futures.
allowed-tools: Read, Bash
---

# GARCH Volatility Toolkit

> **Self-Evolving skill** — if a recipe drifts from what actually reproduces (model spec, cost regime, campaign Sharpe numbers, library API), fix this SKILL.md in the same change; see the Post-Execution Reflection at the bottom.

Walk-forward GARCH(1,1) and GJR(1,1) recipes for volatility forecasting and portfolio construction. Tested on 20 seeds, 2025-26 test window, 2bps and 7bps cost regimes.

> **Campaign Results (honest)**: A negative-to-marginal result set, not a deployable edge. GJR
> inverse vol-sizing helps at LOW cost only (ensemble Sharpe +0.49→+1.00 @2bps) but is COST-FRAGILE —
> its +35% turnover erases the benefit at retail 7bps (Δ+0.02, p=0.54, coin-flip). DCC de-weighting is
> economically immaterial (+0.05–0.07). GARCH-as-features is a flat null. Per-seed p<0.0001 figures are
> inflated by applying a deterministic overlay to correlated seeds — use ensemble PSR instead. See
> [CAMPAIGN_VERDICT.md](references/CAMPAIGN_VERDICT.md). This skill's value is the METHODOLOGY (fitting
> recipes + leakage traps), not an alpha claim.

## Quick Start

### 1. Univariate GARCH(1,1) Forecast Volatility

```python
import pandas as pd
import numpy as np

def garch_forecast(returns_series, window=252):
    """
    Walk-forward GARCH(1,1) fitting and forecast.

    h_t = ω + α·r²_{t-1} + β·h_{t-1}

    Parameters:
    - window: Rolling estimation window (default 252 bars ≈ 1 year)
    - Returns: pd.Series of forecast volatilities (sqrt(h_t))
    """
    ret = returns_series.values if isinstance(returns_series, pd.Series) else returns_series
    T = len(ret)
    h = np.full(T, np.var(ret), dtype=np.float64)
    fc = np.full(T, np.nan, dtype=np.float64)

    for t in range(1, T):
        r = ret[max(0, t-window):t]
        if len(r) > 10:
            om = max(np.var(r) * 0.01, 1e-6)
            al = min(0.1, max(0.01, 0.1 * np.mean(r**2) / (np.var(r) + 1e-10)))
            be = 0.8
        else:
            om, al, be = np.var(ret) * 0.01, 0.05, 0.85

        h[t] = max(om + al * ret[t-1]**2 + be * h[t-1], 1e-8)
        fc[t] = np.sqrt(h[t])

    return pd.Series(fc, index=returns_series.index if isinstance(returns_series, pd.Series) else None)
```

**Usage**:

```python
returns = pd.Series(btc_daily_returns, index=dates)
vol_forecast = garch_forecast(returns)
```

### 2. GJR(1,1): GARCH with Leverage Effect

```python
def gjr_forecast(returns_series, window=252):
    """
    GJR (Glosten-Jagannathan-Runkle) GARCH(1,1).

    h_t = ω + α·r²_{t-1} + γ·r²_{t-1}·𝟙[r_{t-1}<0] + β·h_{t-1}

    Key: γ (leverage effect) captures how negative shocks amplify volatility more than positive.
    This is empirically important for equity/crypto returns (volatility clusters on downturns).

    Returns: pd.Series of forecast volatilities
    """
    ret = returns_series.values if isinstance(returns_series, pd.Series) else returns_series
    T = len(ret)
    h = np.full(T, np.var(ret), dtype=np.float64)
    fc = np.full(T, np.nan, dtype=np.float64)

    for t in range(1, T):
        r = ret[max(0, t-window):t]

        if len(r) > 20:
            om = max(np.var(r) * 0.005, 1e-7)
            al = min(0.15, max(0.01, 0.08 * np.mean(r**2) / (np.var(r) + 1e-10)))
            be = 0.75

            # Leverage effect: shocks are larger when r < 0
            neg_shocks = (r < 0)
            if neg_shocks.sum() > 0:
                ga = min(0.20, max(0.01, 0.05 * np.mean((r[neg_shocks])**2) / (np.var(r) + 1e-10)))
            else:
                ga = 0.01
        else:
            om, al, be, ga = np.var(ret) * 0.005, 0.05, 0.8, 0.02

        # GJR recursion: leverage effect term only when r_{t-1} < 0
        shock_term = al * ret[t-1]**2
        if ret[t-1] < 0:
            shock_term += ga * ret[t-1]**2  # Amplify negative shocks

        h[t] = max(om + shock_term + be * h[t-1], 1e-8)
        fc[t] = np.sqrt(h[t])

    return pd.Series(fc, index=returns_series.index if isinstance(returns_series, pd.Series) else None)
```

### 3. Application: Inverse Vol-Scaling Position Sizing

```python
def inverse_vol_scale_positions(positions_df, vol_forecast, ref_vol=None):
    """
    Scale positions inversely to forecast volatility.

    pos_scaled[t] = pos[t] × (ref_vol / σ̂[t])

    Intuition: When volatility is HIGH, reduce position size to maintain constant risk.
              When volatility is LOW, increase positions to maintain target risk.

    Parameters:
    - positions_df: DataFrame of positions (columns=assets, index=dates)
    - vol_forecast: Series of forecast volatilities (same index as positions)
    - ref_vol: Reference volatility for scaling. If None, use mean of vol_forecast

    Returns: DataFrame of scaled positions
    """
    if ref_vol is None:
        ref_vol = vol_forecast.dropna().mean()

    # Compute scaling factors
    scale_factors = (ref_vol / (vol_forecast + 1e-8)).clip(0.5, 2.0)  # Bound scaling to [0.5, 2.0]

    # Apply scaling
    return positions_df.mul(scale_factors, axis=0)
```

## Campaign Verdict

Independently re-verified ensemble net-Sharpe (equal-weight 20 seeds, non-IID PSR), baseline
reconstruction-gated. See [CAMPAIGN_VERDICT.md](references/CAMPAIGN_VERDICT.md) for full provenance.

| Overlay (ensemble Sharpe) | 2 bps                               | 7 bps               | Honest verdict                            |
| ------------------------- | ----------------------------------- | ------------------- | ----------------------------------------- |
| **DCC de-weighting**      | +0.49→+0.56 (PSR 0.71→0.73)         | −1.64→−1.58         | Immaterial (mild risk overlay)            |
| **GJR vol-scaling**       | +0.49→**+1.00** (PSR 0.71→**0.86**) | +0.02, p=0.54, 9/20 | Real @2bps, **cost-fragile — dies @7bps** |

### Key findings (honest)

1. **GJR vol-sizing is real at low cost, not at retail**: +0.49→+1.00 ensemble Sharpe @2bps (genuine
   vol-targeting), but its +35% turnover erases the edge at 7bps (Δ+0.02, coin-flip). Low-cost/maker-venue
   lever only — NOT ready for live deployment at retail cost.
2. **DCC de-weighting is economically immaterial** (+0.05–0.07), a mild risk overlay, not an edge.
3. **GARCH-as-features is a flat null** (20-seed paired lift −0.01, CI ±0.6).
4. **Do NOT trust per-seed paired p-values here**: a deterministic overlay applied to correlated seeds
   inflates significance. The ensemble PSR is the honest test, and it clears no threshold except C@2bps.
5. **Two subagent bugs were caught by re-verification** (symbol-mismatch zeroing; turnover-Δ/2 halving
   costs). The lesson: reconstruction-gate every baseline against a known truth before trusting a lift.

## Leakage Traps (Gotchas)

### ✗ Symbol Naming Mismatch

**Problem**: Using `BTCUSDT` instead of `BTC/USDT` will silently break everything — positions zero out.

**Fix**:

```python
# Check your data
print(close_wide.columns)  # Should be ['BTC/USDT', 'ETH/USDT', ...]

# Use exact symbol names
symbols = close_wide.columns.tolist()
pos = pos[[col for col in symbols if col in pos.columns]]
```

### ✗ Index Misalignment (Returns vs Prices)

**Problem**: `returns = prices.pct_change()` shifts the index by 1 (first return is NaN). If you don't align carefully:

- GARCH forecast is off-by-one vs prices
- DCC correlations don't match the positions index
- You're comparing apples to oranges

**Fix**:

```python
# Prices: 24,184 bars
# Returns: 24,183 bars (first is NaN, dropped)
# Positions: align to returns index, not prices

close_wide = df.pivot_table(...).dropna()  # 24,184 rows
ret = close_wide.pct_change().iloc[1:]     # 24,183 rows

# Now GARCH is 24,183 long and aligned with ret
vol_forecast = garch_forecast(ret[sym])    # Same length as ret
```

### ✗ Z-Score NaN Propagation in DCC

**Problem**: If any z-score is NaN in the DCC correlation loop, the entire Q matrix can degrade.

**Fix**:

```python
# Before DCC recursion, ensure z-scores are clean
z_arr = np.column_stack([z[sym] for sym in symbols])
z_clean = z_arr[~np.isnan(z_arr).any(axis=1)]  # Drop rows with ANY NaN

# Initialize Q from clean subset only
Qbar = np.corrcoef(z_clean.T)

# Then run DCC recursion (will skip NaN rows automatically)
```

### ✗ Non-Convergent Assets in DCC

**Problem**: DCC assumes all assets are correlated. If you include real estate + bonds + crypto, the correlation matrix may not converge (degenerate case).

**Fix**:

- Verify your assets move together (sample correlation > 0.2)
- If building a multi-asset model, ensure homogeneous risk regimes
- For heterogeneous assets, use asset-specific volatility models (DCC may be wrong)

### ✓ No-Lookahead Discipline

**Pattern**: Fit parameters on a CLOSED training window only.

```python
# Good: Closed window [2024-01-01, 2024-12-31]
idx_2024 = (ret.index.year == 2024)
vol_ref = vol_forecast[idx_2024].quantile(0.75)  # Fit on 2024 only

# Bad: Open-ended or overlapping window
vol_ref = vol_forecast.quantile(0.75)  # Includes test data! (lookahead)
```

## Exercises

### Exercise 1: Reproduce GJR Result on BTC Only

```python
# Load BTC daily returns for 2024-2026
btc_ret = ...  # pd.Series with daily returns

# Fit GJR on 2024
idx_2024 = (btc_ret.index.year == 2024)
vol_ref = gjr_forecast(btc_ret[idx_2024]).mean()

# Forecast on 2025-26
idx_test = (btc_ret.index.year >= 2025)
vol_test = gjr_forecast(btc_ret).loc[idx_test]

# Expected: vol_test varies from 0.003 to 0.015 daily
# Verify: GJR should capture volatility spikes on -5% days
print(btc_ret[btc_ret < -0.05].describe())  # Should have high vol around these dates
print(vol_test[btc_ret[idx_test] < -0.05].describe())  # Should be high
```

### Exercise 2: Compare GARCH vs GJR

Build side-by-side forecasts and compare on "bad news" days:

```python
vol_garch = garch_forecast(returns)
vol_gjr = gjr_forecast(returns)

# On worst days, GJR should forecast higher vol than GARCH
worst_days = returns.nsmallest(100).index
print("GARCH avg vol (worst 100 days):", vol_garch[worst_days].mean())
print("GJR avg vol (worst 100 days):", vol_gjr[worst_days].mean())
# Expected: GJR > GARCH on worst days due to leverage effect
```

### Exercise 3: Turnover-Aware Sizing

The GJR approach trades 27% more. Can you reduce this while keeping the edge?

```python
# One approach: less aggressive scaling (wider bounds)
scale_factors = (ref_vol / vol_forecast).clip(0.7, 1.3)  # Narrower than [0.5, 2.0]

# Another: apply only on large vol deviations
def smart_scale(vol_forecast, ref_vol, threshold_pct=0.2):
    scale = ref_vol / vol_forecast
    # Only apply scaling if vol is >20% away from ref
    return scale.where(scale.abs() - 1 > threshold_pct, 1.0).clip(0.5, 2.0)
```

## References

- López de Prado, M., Lipton, A., & Zoonekynd, V. (2026). "How to Use the Sharpe Ratio." ADIA Lab.
- Glosten, L., Jagannathan, R., & Runkle, D. (1993). "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks." Journal of Finance.
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." Journal of Econometrics.
- Nelson, D. (1991). "Conditional Heteroskedasticity in Asset Returns." Econometric Reviews.

## Post-Execution Reflection

After using a recipe, check before closing: (1) Did the fit reproduce the quoted campaign result within noise, or did the numbers drift? Update the figures here if the model/data/cost regime changed. (2) Did a no-lookahead boundary need re-checking (walk-forward split, standardization window)? If a leak was possible, document the guard. (3) Did an `arch`/library API change break a snippet? Fix the snippet, not just your local copy. Only update for real, reproducible drift — not speculation.

---

**Last Updated**: 2026-07-20  
**Author**: Terry Li (terrylica)  
**License**: PolyForm Noncommercial
