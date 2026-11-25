# Health Check — Subjective Scoring Prompt

Use this structured prompt when running a thesis health check as the agent. The CLI uses a neutral 50 placeholder; this prompt produces real subjective scores.

## Input

Before scoring, gather:
1. The thesis from `data/artifacts/{TICKER}/thesis/thesis.json`
2. Recent financial data from `GET /api/financials/{TICKER}/metrics`
3. Recent price action from `GET /api/financials/{TICKER}/prices?period=3mo`
4. Any recent updates from `data/artifacts/{TICKER}/thesis/updates.json`

## Prompt Template

For each assumption in the thesis, evaluate and score 0-100:

```
Ticker: {TICKER}
Core thesis: {core_thesis}

For each assumption below, provide:
  1. A subjective score (0-100)
  2. A 1-2 sentence justification referencing specific recent events

Scoring guide:
  90-100: Strong tailwinds, assumption clearly validated by recent evidence
  70-89:  Assumption intact, no material concerns
  50-69:  Neutral or mixed signals
  30-49:  Concerning developments, assumption under pressure
  0-29:   Assumption likely broken, material negative evidence

Assumptions:
{for each assumption: index, description, weight, kpi_metric}

Consider these qualitative factors:
- Competitive dynamics: new entrants, technology shifts, market share trends
- Management quality: capital allocation, execution track record, guidance credibility
- Regulatory / geopolitical: policy changes, trade restrictions, legal proceedings
- Sentiment: narrative shifts, analyst consensus changes, institutional positioning
- Thesis coherence: does the original story still make sense given recent developments?

Requirements:
- Reference SPECIFIC recent events, not generic assessments
- If no recent developments affect an assumption, score 50 (neutral)
- Be honest about disconfirming evidence — do not inflate scores
```

## Expected Output

Return a JSON object:

```json
{
  "subjective_score": 72.0,
  "assumption_scores": [
    {
      "assumption_idx": 0,
      "subjective": 85.0,
      "justification": "Blackwell ramp exceeded expectations in Q4, validating strong data center demand trajectory."
    },
    {
      "assumption_idx": 1,
      "subjective": 70.0,
      "justification": "Gross margins held at 73% despite new product mix shift. Monitoring Blackwell margin dilution."
    }
  ]
}
```

The overall `subjective_score` is the weighted average of per-assumption subjective scores, using weights from `thesis.json`.
