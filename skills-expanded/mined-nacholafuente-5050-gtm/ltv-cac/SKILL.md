---
name: ltv-cac
description: Compute SaaS LTV, CAC payback, and LTV/CAC ratio with multiple frameworks side by side (Skok basic, NDR-adjusted, AI-inference-adjusted, Sequoia contribution margin). Outputs a styled Excel workbook with verdict, sensitivity heatmap, and 36-month cohort projection. Use when the user says "/ltv-cac", "calculate LTV", "LTV CAC ratio", "is this business healthy", "unit economics", or "should I scale acquisition". One-shot, no warehouse.
---

# LTV / CAC

Compute LTV, CAC payback, and LTV/CAC ratio with the four canonical formulas side by side. Anchor the verdict on Skok's 3:1 rule, layer on a16z NDR, Sequoia contribution-margin, and Tunguz AI-inference adjustments. Output a styled Excel workbook with a sensitivity heatmap and a 36-month synthetic cohort projection.

## Step 1: Ask the user up to 6 inputs

Ask in order. The first 3 are required; the rest have defaults.

1. **ARPU** (monthly revenue per customer, $), e.g. `200`
2. **Customer churn rate** (monthly, decimal), e.g. `0.03` for 3%/mo
3. **CAC** (customer acquisition cost, $), e.g. `1500`
4. **Net revenue expansion** (monthly, decimal, optional), e.g. `0.005` for 0.5%/mo. Default `0`. If they have NDR > 100%, this is positive.
5. **Gross margin** (decimal, optional), e.g. `0.78`. Default `0.78` (78%, typical SaaS).
6. **Inference / variable cost per customer per month** ($, optional), only relevant for AI products. Default `0`.

If the user is hesitant on inputs, suggest they start with the example fixture (`examples/inputs.json`).

## Step 2: Run

```bash
python skills/ltv-cac/run.py \
  --arpu 200 \
  --churn 0.03 \
  --cac 1500 \
  --expansion 0.005 \
  --gross-margin 0.78 \
  --inference-cost 0 \
  --out-dir /tmp/ltv-cac-<client>-<date>
```

Or load all inputs from a JSON file:

```bash
python skills/ltv-cac/run.py --inputs path/to/inputs.json --out-dir /tmp/ltv-cac
```

## Step 3: KPIs the user gets

**Verdict sheet (the headline)**
- **Skok basic LTV**: `ARPU × GM / churn` (the canonical 3:1 reference)
- **NDR-adjusted LTV**: `ARPU × GM / (churn − expansion)` (a16z framework)
- **AI-adjusted LTV**: `(ARPU × GM − inference) / churn` (Tunguz inference erosion)
- **Sequoia contribution-margin LTV**: combines the above two: `(ARPU × GM − inference) / (churn − expansion)`
- **CAC Payback**: months to recover CAC from gross profit. Basic and AI-adjusted.
- **LTV/CAC ratio**: color-coded: red <1, yellow 1-3, green 3-5, blue >5
- **Verdict statement**: plain-English read with Skok 3:1 anchor + AI flag if inference erodes LTV >20%
- **NDR**: monthly and annual-compounded
- **Citations**: every formula tagged with its source

**Sensitivity sheet**
- LTV/CAC heatmap across **monthly churn** (1% to 10%) × **gross margin** (50% to 90%)
- Same color coding as the verdict
- Lets the founder see "if I cut churn from 5% to 3% at the same GM, where does my LTV/CAC land?"

**Cohort Projection sheet**
- Synthetic 100-customer cohort projected forward 36 months with the user's churn + expansion + inference inputs
- Columns: customers retained, MRR, cumulative gross profit, vs cohort CAC
- Line chart of cumulative GP vs CAC
- Payback callout: "Cohort breaks even at lifetime month N" or "Doesn't break even within 36mo"

## Step 4: Output

Default output (`--output all`) writes to `/tmp/ltv-cac-<client>-<date>/`:

- **`ltv_cac_workbook.xlsx`**: the 3-sheet styled Excel file
- `summary.md`, markdown digest with the verdict + tables, paste-able into a doc
- `inputs.json`, the inputs you used (re-runnable: pass with `--inputs`)
- `ltv_summary.csv`, every formula's LTV + ratio
- `cac_payback.csv`, basic and AI-adjusted payback months
- `ndr.csv`, monthly + annual NDR
- `sensitivity.csv`, full heatmap data
- `cohort_projection.csv`, month-by-month projection

## Step 5: After running

Show the user 4-5 lines:
1. The headline verdict (one of: Underwater 🔴 / Tight 🟡 / Healthy 🟢 / Possibly under-investing 🟦)
2. Skok basic LTV/CAC ratio
3. CAC payback months
4. NDR (annual)
5. Path to the workbook

If the AI-adjusted LTV diverges from the basic LTV by >20%, flag inference cost as a key sensitivity.

## When to use

- A founder asks "is my SaaS healthy?" / "should I scale paid acquisition?"
- An investor wants LTV, CAC payback, NDR for a deck
- Modeling unit economics for a new pricing tier
- Comparing scenarios: "what if I raise prices 10%?" / "what if I cut churn from 5% to 3%?"

## When NOT to use

- The user has actual cohort data and wants observed retention curves → use `/cohort-analysis` instead. This skill is for forward-looking modeling from assumptions.
- Pre-revenue product with no churn data → there's nothing to compute. Suggest gathering 3-6 months of data first, then running both `/cohort-analysis` (observed) and `/ltv-cac` (modeled) side by side.

## Try it without thinking

The `examples/inputs.json` ships with a typical mid-stage B2B-SaaS profile (ARPU $200, 3% churn, $1,500 CAC, 78% GM, no inference cost). Run:

```bash
python skills/ltv-cac/run.py --inputs skills/ltv-cac/examples/inputs.json --out-dir /tmp/ltv-cac-demo
open /tmp/ltv-cac-demo/ltv_cac_workbook.xlsx
```

## Frameworks referenced

- **David Skok / Matrix Partners**: "SaaS Metrics 2.0", origin of the 3:1 LTV/CAC rule and the canonical `LTV = ARPU × GM / churn` formula.
- **a16z**: "The 16 Startup Metrics", introduced NDR (Net Dollar Retention) as a first-class LTV input.
- **Sequoia Capital**: argues for contribution-margin LTV (deduct variable costs from GM) over headline gross-margin LTV.
- **Tomasz Tunguz / Theory**: "Unit Economics of LLMs", showing how variable inference costs erode AI-product LTV in ways the traditional formulas miss.

The skill computes all four side by side so the user sees where they agree (and where AI economics break the textbook).
