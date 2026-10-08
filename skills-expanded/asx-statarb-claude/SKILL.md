# CLAUDE.md

Working plan and conventions for this repo. Read this before doing anything substantive.

## Project context

ASX 200 statistical arbitrage. Cointegration-based pairs trading. Walk-forward out-of-sample. The project is for Rajveer's portfolio targeting Sydney quant/strategies seats. The differentiator is methodological honesty, not novelty.

## Locked methodology decisions

These are not up for re-litigation mid-build. If a phase reveals a real reason to revisit one, raise it explicitly.

| Decision | Choice | Rationale |
|---|---|---|
| Data source | yfinance, daily OHLCV | Free, reproducible. Limitations flagged in writeup. |
| Universe | ~50 large-caps grouped by GICS sector | Within-sector pairs only. Reduces multiple-testing burden. |
| Period | 2010-01-01 to present | Captures pre-2015 and post-2015 regimes for alpha decay study. |
| Pair selection | Engle-Granger two-step within sector | Standard. ADF + BH correction + half-life + Hurst filters. |
| Multiple testing | Benjamini-Hochberg at 10% FDR | Honest about ~94-pair search space per window. |
| Half-life filter | 5 to 60 trading days | Excludes too-fast (noise) and too-slow (capital-tied) reversion. |
| Hurst filter | H < 0.5 | Confirms anti-persistent behaviour beyond ADF. |
| Spread model | OU via AR(1) regression | Closed-form parameters, well-understood. |
| Signal | Rolling 60-day z-score | Enter at \|z\|=2, exit at \|z\|=0.5, stop at \|z\|=4 or 2 × half-life. |
| Sizing | Equal-dollar legs, inverse-vol pair scaling, 10 concurrent max | Limits concentration. |
| Backtest | Walk-forward, 24m train / 6m trade, monthly roll | Strict out-of-sample. |
| Costs | 10bps base, 25bps stress (per side per leg) | Two scenarios for fragility check. |

## Phase plan

### Phase 1: Foundation (current)

Goal: clean data pipeline and universe definition.

Tasks:
- [x] Universe defined in `src/data.py` (sector-grouped dict)
- [x] yfinance fetch with parquet cache
- [x] Per-ticker QC (row counts, missing days, suspicious returns)
- [ ] Notebook `01_data_quality.ipynb` walking through coverage by ticker and date range
- [ ] Document any tickers excluded for data quality reasons in `reports/excluded_tickers.md`

Definition of done: 10+ years of clean data for 80%+ of universe, gaps and exclusions documented.

### Phase 2: Cointegration screening

Goal: produce a list of candidate pairs with statistical evidence for cointegration.

Tasks:
- `src/cointegration.py`: Engle-Granger function returning beta, alpha, residuals, ADF statistic, p-value
- `src/ou_process.py`: half-life estimation via AR(1) on residuals
- Hurst exponent function (R/S analysis or DFA)
- BH correction across the screening window's pair universe
- Notebook `02_cointegration.ipynb`: visualise spread for top 10 pairs by survivor metric

Definition of done: function `screen_pairs(prices, sectors, window) -> DataFrame` that returns ranked candidate pairs with all filter columns. Reproduces sensible economic pairs (e.g. CBA/WBC, BHP/RIO).

### Phase 3: Signals and sizing

Goal: turn surviving pairs into a tradeable signal stream.

Tasks:
- `src/signals.py`: rolling z-score, entry/exit/stop logic
- Position sizing function (equal-dollar legs, inverse-vol pair weight)
- Notebook `03_signals.ipynb`: signal performance on a single pair as a sanity check

Definition of done: given a pair and a price series, output a signal series and a position series.

### Phase 4: Walk-forward backtest

Goal: full out-of-sample backtest with realistic costs.

Tasks:
- `src/backtest.py`: walk-forward loop. For each rolling window: re-screen pairs from training, generate signals on trading window, accumulate PnL.
- `src/costs.py`: flat per-side cost model. Stress with 2.5x.
- Performance metrics: Sharpe, Sortino, max drawdown, hit rate, average holding period, turnover.
- Notebook `04_backtest.ipynb`: equity curve, drawdown plot, per-year metrics.

Definition of done: equity curves for both cost scenarios, per-year breakdown, written assessment.

### Phase 5: Critique and writeup

Goal: the part that makes this project actually credible.

Tasks:
- Alpha decay study: Sharpe by year, regression of Sharpe on year
- Multiple-testing diagnostic: how many pairs survive in shuffled / random data
- Capacity analysis: position size vs ADV, market impact estimate
- Survivorship sensitivity: re-run with the most volatile names removed, see how much the result changes
- `reports/writeup.md`: full prose writeup. Pass through humanizer skill.
- `reports/figures/`: all plots.

Definition of done: writeup that an experienced quant would read and think "this person knows what they're doing and isn't lying to themselves."

## Coding conventions

- Type hints on public functions
- Docstrings: one line summary, then numpy-style if complex
- No notebooks for production logic. Notebooks are for exploration and figure generation only. All reusable logic lives in `src/`.
- Cache aggressively to parquet. yfinance is slow and rate-limited.
- All randomness seeded explicitly. We do not have non-determinism in this project.
- Logging via stdlib `logging`, not print.

## Anti-patterns to avoid

- Reporting in-sample Sharpe without flagging it as in-sample
- "I got 3.0 Sharpe" without cost assumptions, without capacity analysis, without out-of-sample
- Testing 1000 pair configurations and presenting the best one
- Cherry-picking the time period
- Hiding losing periods in the writeup

## Writing conventions

When generating any markdown for `reports/` or `README.md`, run the output through `/mnt/skills/user/humanizer/SKILL.md` before considering it done. Specifically:

- No em dashes
- No "underscores", "highlights", "showcases", "underscoring"
- No "in the rapidly evolving landscape" or similar
- No generic positive conclusions
- Vary sentence length and rhythm
- Have opinions where they're warranted

The writeup is the deliverable a recruiter actually reads. It needs to sound like a person wrote it.

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. The
skill has multi-step workflows, checklists, and quality gates that produce better
results than an ad-hoc answer. When in doubt, invoke the skill. A false positive is
cheaper than a false negative.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke /office-hours
- Strategy, scope, "think bigger", "what should we build" → invoke /plan-ceo-review
- Architecture, "does this design make sense" → invoke /plan-eng-review
- Design system, brand, "how should this look" → invoke /design-consultation
- Design review of a plan → invoke /plan-design-review
- Developer experience of a plan → invoke /plan-devex-review
- "Review everything", full review pipeline → invoke /autoplan
- Bugs, errors, "why is this broken", "wtf", "this doesn't work" → invoke /investigate
- Test the site, find bugs, "does this work" → invoke /qa (or /qa-only for report only)
- Code review, check the diff, "look at my changes" → invoke /review
- Visual polish, design audit, "this looks off" → invoke /design-review
- Developer experience audit, try onboarding → invoke /devex-review
- Ship, deploy, create a PR, "send it" → invoke /ship
- Merge + deploy + verify → invoke /land-and-deploy
- Configure deployment → invoke /setup-deploy
- Post-deploy monitoring → invoke /canary
- Update docs after shipping → invoke /document-release
- Weekly retro, "how'd we do" → invoke /retro
- Second opinion, codex review → invoke /codex
- Safety mode, careful mode, lock it down → invoke /careful or /guard
- Restrict edits to a directory → invoke /freeze or /unfreeze
- Upgrade gstack → invoke /gstack-upgrade
- Save progress, "save my work" → invoke /context-save
- Resume, restore, "where was I" → invoke /context-restore
- Security audit, OWASP, "is this secure" → invoke /cso
- Make a PDF, document, publication → invoke /make-pdf
- Launch real browser for QA → invoke /open-gstack-browser
- Import cookies for authenticated testing → invoke /setup-browser-cookies
- Performance regression, page speed, benchmarks → invoke /benchmark
- Review what gstack has learned → invoke /learn
- Tune question sensitivity → invoke /plan-tune
- Code quality dashboard → invoke /health
