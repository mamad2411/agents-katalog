# Agent Operating Notes

This repository is shared by Codex, Antigravity, Gemini CLI, and human operators.

## Current Objective

Focus on making the Polymarket BTC 5-minute strategy profitable with evidence. Do not spend effort on broad refactors, UI polish, or speculative strategy features unless they directly support measurable profitability validation.

## Canonical Runtime

Use this runtime spine as the source of truth:

`SessionManager -> EngineRuntime -> MarketSpawner -> MarketLifecycle -> Strategy/RiskGate/Client/UserChannel`

`EarlyBird` is retained as a legacy compatibility wrapper. Do not restore it as the canonical runtime.

## Profitability Rules

- Do not claim a strategy is profitable from a tiny smoke run.
- Prefer same-sample and holdout replay evidence with conservative fill scoring.
- Track PnL, drawdown, capital utilization, settlement PnL, missed fills, good/bad blocks, fill realism, adverse selection, and trade count.
- Treat inferred public trade flow as diagnostic only unless an explicit research run opts into it.
- Keep `fvm-v1.1.0-raw-ungated` as the broad-replay benchmark until a variant beats it on stronger evidence.
- Treat Avellaneda/momentum/calibrated variants as research candidates until they beat the benchmark on broad validation.

## Workspace Hygiene

- Keep generated logs, large data, and temporary state out of git.
- Archive one-off repair scripts under `AI_WORKSPACE/archive/` if they are useful for audit history.
- Commit source, tests, small reports, and handoff docs that help the next agent continue safely.
- Before promotion or live/paper work, run the verification commands in `AI_WORKSPACE/HANDOFF.md`.

