---
name: vc-evaluator
description: "Simulate a VC investment panel evaluating your startup. Researches real investors in your sector via web search, builds personas from their investment thesis, portfolio, and known preferences, then each investor evaluates independently. Synthesizes a partner meeting deliberation with funding verdict and specific feedback. Use when: VC feedback, investor pitch, fundraising prep, would VCs fund this, pitch evaluation, startup funding, series A prep."
license: MIT
metadata:
  version: 1.0.0
  category: evaluation
  tags: [vc, startup, fundraising, pitch, investment, multi-agent, evaluation]
---

# VC Panel Evaluator

Simulate a complete venture capital investment panel evaluating your startup. Given a startup description, pitch deck, or project path, this skill researches real investors in your sector, builds personalized investor personas, and evaluates from each VC's perspective.

## How It Works

1. **Parse Input** — startup description, pitch deck, or project path + target stage (pre-seed/seed/A/B) + sector
2. **Startup Discovery** — analyze the project's architecture, traction, market positioning, and team if a path is given; otherwise take the description as-is
3. **Investor Research** — use WebSearch to find real VCs who invest in this sector and stage (see `agents/researcher.md`)
4. **Panel Construction** — build 3-5 investor personas based on real people with distinct investment theses
5. **Parallel Evaluation** — dispatch each investor as a parallel agent using `agents/investor.md`, each evaluating from their unique lens
6. **Partner Meeting Synthesis** — simulate Monday partner meeting using `agents/synthesizer.md`, modeling championing dynamics and fund-level strategy

## Usage

```
"Would VCs fund this? It's a B2B SaaS for construction site logistics"
"Evaluate my startup for Series A — project is at ./my-saas"
"I'm raising a seed round for an AI agent marketplace, give me VC feedback"
"How would top fintech investors evaluate this pitch deck?"
```

## Output

The evaluation produces:

1. **Verdict** — PASS / PARTNER MEETING / TERM SHEET LIKELY
2. **Panel Scorecard** — per-criterion scores from each VC with weighted averages
3. **Individual VC Feedback** — what impressed them, what concerned them, key questions they'd ask in the pitch meeting
4. **Partner Meeting Simulation** — who champions, who passes, key debates, outcome
5. **Funding Probability** — X% at target stage with current pitch
6. **What Would Change The Outcome** — max 5 specific actions that would move investors from pass to proceed
7. **Pitch Coaching** — tailored to this specific panel's priorities and blind spots

## Agent Files

| Agent | Purpose |
|-------|---------|
| `agents/researcher.md` | Researches real VCs in the sector/stage, their thesis, portfolio, and preferences |
| `agents/investor.md` | Role-plays as a specific VC partner, evaluates from their investment lens |
| `agents/synthesizer.md` | Simulates Monday partner meeting, models championing dynamics and fund strategy |

## References

| File | Content |
|------|---------|
| `references/default-criteria.md` | Default VC evaluation criteria when sector-specific ones aren't available (team, market, product, traction, moat, unit economics) |

## Important Notes

- **WebSearch is critical** — the value is in researching REAL investors and their actual thesis, not fabricating them
- If specific investor info is scarce, construct archetypes based on known fund strategies and public portfolio data
- Always include at least one technical/product-focused investor and one growth/market-focused investor
- Be brutally honest — sugarcoating defeats the purpose of fundraising prep
- Score relative to the target stage and sector (pre-seed expectations differ wildly from Series B)
- Consider the current funding climate and sector sentiment when estimating probability
- The partner meeting simulation should reflect real VC dynamics: one partner must champion the deal

## Example Output

A condensed version of the panel scorecard produced by this skill:

```
| Criterion        | Weight | Investor 1 (SaaS) | Investor 2 (Infra) | Investor 3 (Generalist) | Avg  |
|------------------|--------|--------------------|---------------------|-------------------------|------|
| Team             | 40%    | 7                  | 8                   | 6                       | 7.0  |
| Market           | 25%    | 8                  | 6                   | 8                       | 7.3  |
| Product          | 15%    | 7                  | 9                   | 6                       | 7.3  |
| Traction         | 10%    | 5                  | 5                   | 6                       | 5.3  |
| Moat             | 10%    | 6                  | 7                   | 5                       | 6.0  |
| **Overall**      |        | **6.9**            | **7.1**             | **6.4**                 | **6.8** |

Verdict: PARTNER MEETING — Two investors would take the meeting, one passes on stage fit
Funding Probability: 35% at Seed with current pitch
```

This is followed by individual investor feedback (what impressed them, deal-breakers, questions they'd ask in the pitch), a partner meeting simulation, funding probability analysis, what would change the outcome (max 5 actions), and pitch coaching.

## Without WebSearch

If WebSearch is not available, the skill uses default criteria from `references/default-criteria.md` and constructs archetype investors instead of researching real people:

- **Technical/Product VC** — evaluates technical moat, product-market fit, architecture, and engineering talent
- **Growth/Market VC** — evaluates market size, go-to-market strategy, unit economics, and scalability
- **Generalist VC** — evaluates team quality, timing, narrative, and overall portfolio fit

The evaluation is still valuable but loses the personalization that comes from researching real investors, their specific portfolio companies, and their published investment criteria. When WebSearch is available, always prefer it for more accurate and targeted feedback.
