---
name: gortex-src-engine-2-dirs
description: "Work in the src/engine +2 dirs area — 155 symbols across 9 files (89% cohesion)"
---

# src/engine +2 dirs

155 symbols | 9 files | 89% cohesion

## When to Use

Use this skill when working on files in:
- `apps/backtester/src/engine/context.ts`
- `apps/backtester/src/engine/dataset.ts`
- `apps/backtester/src/engine/indicators/engine.ts`
- `apps/backtester/src/engine/module-executor.ts`
- `apps/backtester/src/engine/overlay.ts`
- `apps/backtester/src/engine/portfolio.ts`
- `apps/backtester/src/engine/runner.ts`
- `packages/research-contracts/src/research/context.ts`
- `packages/research-contracts/src/research/decision.ts`

## Key Files

| File | Symbols |
|------|---------|
| `apps/backtester/src/engine/context.ts` | carriesMarket, deepFreeze, value, propKey, indicatorEngine, ... |
| `apps/backtester/src/engine/dataset.ts` | indicatorApiFor, engine, barIndex |
| `apps/backtester/src/engine/indicators/engine.ts` | accessorAt, barIndex |
| `apps/backtester/src/engine/module-executor.ts` | ctx, fn, InProcessTrustedModuleExecutor, ctx, ctx, ... |
| `apps/backtester/src/engine/overlay.ts` | decision, branch, OverlayDecisionSource, compose, patched, ... |
| `apps/backtester/src/engine/portfolio.ts` | take, grossAtSize, isFlat, position, _pending, ... |
| `apps/backtester/src/engine/runner.ts` | base, final, candles, prot, id, ... |
| `packages/research-contracts/src/research/context.ts` | IndicatorApi |
| `packages/research-contracts/src/research/decision.ts` | StrategyDecision, OverlayDecision |

## Entry Points

- `apps/backtester/src/engine/runner.ts::runSymbol`

## Connected Communities

- **src/engine +1 dirs · evaluate** (6 cross-edges)
- **src/engine · settlePending** (2 cross-edges)
- **src/engine · buildTrade** (1 cross-edges)
- **src/engine +1 dirs · smaAsOf** (1 cross-edges)
- **src/engine +1 dirs · pointInTimeMarketApi** (1 cross-edges)
- **src/engine +1 dirs · runBacktest** (1 cross-edges)

## How to Explore

```
get_communities with id: "community-81"
smart_context with task: "understand src/engine +2 dirs", format: "gcx"
find_usages with id: "apps/backtester/src/engine/runner.ts::runSymbol", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
