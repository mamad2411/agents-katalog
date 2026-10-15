---
name: fyers-supercharge
description: >-
  Supercharge Mode — an iterative, multi-agent optimization loop for FYERS trading
  strategies. Offered automatically after a strategy's first successful backtest. A central
  orchestrator convenes a council of specialist strategists (risk, return, entry, exit,
  regime, execution, options, capital efficiency, robustness, backtest integrity) that study
  the strategy, debate improvements, generate optimized variants, backtest them, and search
  for measurably better versions across rounds — pausing for the user every three rounds. No
  single agent decides; the output is council consensus, and the original strategy is always
  preserved as the baseline. Use when the user wants to optimize, improve, harden, evolve, or
  stress-test a strategy, or accepts the "Unlock Supercharge Mode?" offer. Triggers:
  "supercharge", "supercharge mode", "optimize my strategy", "improve my strategy",
  "make my strategy better", "strategy variants", "strategy council", "evolve my strategy",
  "stress test my strategy".
version: 0.1.0
license: MIT
allowed-tools:
  - Agent
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
---

# Supercharge Mode — Multi-Agent Optimization Loop

Turn a single backtested strategy into an evolving research project. A central **orchestrator**
convenes a **council of specialist strategists** that study the strategy, debate improvements,
generate optimized variants, backtest them, and keep searching for measurably better versions —
in iterative rounds, keeping the user involved every three rounds.

The objective is **not to validate** a strategy — it is to **improve** it. Instead of "Is this
strategy good?", the question is "How can this strategy become significantly better?" — while
protecting against overfitting and needless complexity. Every change is justified, tested, and
compared against previous versions. **No single agent decides — the output is council consensus.**

> **The original strategy is always preserved as the immutable baseline.** Every variant is
> measured against it. Never modify the baseline.

> **Depends on `fyers-trading`.** This skill optimizes a strategy that `fyers-trading` built and
> backtested; it reuses that skill's backtest path (`references/backtesting.md`) and metrics
> (`scripts/quantstats_report.py`) so variants are scored on the same yardstick as the baseline.
> Install both skills together. **All of `fyers-trading`'s real-money safety rules apply unchanged**
> (secrets via env, dry-run by default, symbol validation, live-order confirmation, rate limits):
> the council may *recommend* deploying or going live, but never places a live order itself.

## When this activates

Supercharge Mode is offered **automatically after a strategy completes its first successful
backtest** (the `fyers-trading` skill hands off here). Present the offer:

> **Your strategy is ready.**
>
> **Unlock Supercharge Mode?**
>
> Our AI team of professional trading strategists will analyze your strategy, debate improvements,
> generate multiple optimized variants, backtest them, and recommend stronger alternatives. The
> optimization runs in iterative cycles and keeps you involved every three rounds before continuing.

If the user says **Yes**, launch immediately. Also activate on explicit intent to optimize /
improve / evolve / stress-test a strategy. If the user only wants to *build or run* a strategy,
that's `fyers-trading` — come back here once a backtest exists.

## How it works — hybrid orchestration

**You (the host agent) are the orchestrator.** You run the reasoning and debate by spawning one
subagent per council seat via the `Agent` tool. The **deterministic** work — scoring, ranking, and
persistence — is delegated to three bundled scripts so every variant is measured identically and
the journey is reproducible:

- `scripts/scorecard.py` — one standardized metric dict per variant (reuses `fyers-trading`'s
  `quantstats_report.key_metrics()`; computes trade-level metrics itself).
- `scripts/dashboard.py` — ranks the baseline + all variants for the active objective.
- `scripts/evolution_log.py` — append-only JSONL journal of every round, variant, and decision.

## The optimization loop

Each round runs six phases — read **`references/optimization-loop.md`** for the full lifecycle and
the consensus rule:

1. **Understand** — every seat studies the rules, sizing, capital, timeframe, and backtest evidence.
2. **Diagnose** — each seat names strengths, weaknesses, hidden risks, and metrics to improve.
3. **Debate** — seats challenge each other; the orchestrator resolves conflicts into experiments.
4. **Generate variants** — candidates that each change only a few variables (`references/variants.md`).
5. **Backtest** — every variant, identical assumptions, via `fyers-trading`; scored by `scorecard.py`.
6. **Learn** — what worked / failed feeds the next round; results recorded via `evolution_log.py`.

Produce variants each aimed at a specific objective: higher returns, lower drawdown, better
risk-adjusted performance, higher win rate, better capital efficiency, better execution, or better
robustness across regimes. The goal is a **library** of deployment-ready variants, not one "best".

## The council

One subagent per seat, spawned via `Agent`, briefed from **`references/council.md`** (12 seats:
Risk, Return, Entry Precision, Exit Intelligence, Market Regime, Backtest Integrity, Execution,
Options, Capital Efficiency, Simplicity & Robustness, Variant Generation, Performance Ranking).
The roster is **extensible without changing the loop** — add a seat by adding an entry.

## Checkpoint every three rounds

**Never continue silently.** After every three rounds, pause and present the optimization report
(improvements, variants created/discarded, metrics improved/worsened, major disagreements, current
leader, recommended next direction), then wait for the user to choose a direction — continue, focus
on drawdown / returns / consistency / frequency / execution, or finalize. See
**`references/checkpoints.md`**.

## Final deliverables

When the user finalizes: an Executive Summary, the Strategy Evolution Timeline, the Variant
Library, the Comparison Dashboard, and the AI Consensus. See **`references/deliverables.md`**.

## References

| Topic | Read |
|---|---|
| The 6-phase loop + consensus rule | `references/optimization-loop.md` |
| Council roster (12 seats, mandates, vetoes) | `references/council.md` |
| Variant contract, strategy interface, Variant Library | `references/variants.md` |
| Metrics + Comparison Dashboard (where each number comes from) | `references/metrics.md` |
| User checkpoints every 3 rounds | `references/checkpoints.md` |
| Final deliverables + success criteria | `references/deliverables.md` |
| Overfitting / robustness guardrails | `references/overfitting.md` |

## Scripts

- `scripts/scorecard.py` — standardized per-variant metric dict; reuses `fyers-trading`'s
  `quantstats_report.key_metrics()` with a stdlib fallback; computes trade-level metrics and a
  robustness score. CLI: `demo`.
- `scripts/dashboard.py` — ranks the baseline + variants for an objective and renders the
  Comparison Dashboard as Markdown. CLI: `demo`.
- `scripts/evolution_log.py` — append-only JSONL journal (mirrors `fyers-trading`'s
  `trade_logger.py`): `log_round`/`log_variant`/`log_decision`/`log_checkpoint` +
  `timeline`/`checkpoint_report`/`summary`. CLI: `demo` / `timeline` / `summary` / `tail`.

> Full-fidelity scoring needs `fyers-trading` **and** QuantStats installed. Without them the
> scripts still run (stdlib fallback), but CAGR/Calmar and the HTML tear sheet are unavailable.
