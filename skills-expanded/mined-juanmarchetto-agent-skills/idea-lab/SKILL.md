---
name: idea-lab
description: "Automated idea laboratory — generates multiple diverse ideas from a context, pre-screens them, evaluates the best with multi-agent scoring via /architect, and ranks the winners. Configurable idea count, diversity axes, score thresholds, and dimension filters. Composes with /founder-mode to build the winning idea. Use when: brainstorm ideas, generate ideas, hackathon ideas, idea lab, idea factory, compare ideas, evaluate multiple ideas, which idea should I build, batch evaluation, ideation."
license: MIT
metadata:
  version: 1.0.0
  category: evaluation
  tags: [ideation, brainstorming, evaluation, multi-agent, ranking, hackathon, divergent-thinking]
---

# Idea Lab — Automated Idea Generation & Evaluation

Generate multiple diverse ideas, evaluate the best ones with 6-evaluator scoring, rank and surface the winners.

## How It Works

```
/idea-lab "FinTech hackathon, 48h, team of 2, must use AI"
        │
        ▼
  Phase 0: Bootstrap ─── config.json + context setup
        │
        ▼
  Phase 1: Generate ─── N diverse ideas via forced divergence axes
        │
        ▼
  Phase 2: Pre-screen ─── quick 1-agent score per idea, filter weak ones
        │
        ▼
  ══ PRE-SCREEN DASHBOARD ══ see all ideas ranked by estimate
        │
        ▼
  Phase 3: Deep Eval ─── top-K ideas → /architect (6 evaluators each)
        │
        ▼
  ══ FINAL DASHBOARD ══ comparative matrix, top recommendation
        │
        ▼
  [expand N] — full evaluation details
  [build N]  — launch /founder-mode with the winner
  [refine]   — adjust context, generate more
  [stop]     — save and exit
```

## Phases

| Phase | What It Does | Agent |
|-------|-------------|-------|
| 0 - Bootstrap | Config generation, context capture | `bootstrapper.md` |
| 1 - Generate | N ideas with forced diversity (SCAMPER, cross-domain, axis rotation) | `generator.md` |
| 2 - Pre-screen | Quick 1-agent score per idea, filters below threshold | `prescreener.md` |
| 3 - Deep Eval | Top-K ideas evaluated via `/architect` (6 parallel evaluators each) | `deep-evaluator.md` |
| 4 - Ranking | Comparative matrix, scenario recommendations, top pick | `ranker.md` |

## Diversity Engine

Ideas are forced to diverge across configurable axes:
- B2B SaaS, B2C consumer, open-source tool, educational, mobile-first
- SCAMPER method applied per idea
- Cross-domain analogies forced for at least 2 ideas
- Anti-obvious filter removes generic suggestions

## Config

Generated at `.idea-lab/config.json` during bootstrap:

- `ideaCount`: how many to generate (default 5, max 20)
- `topK`: how many advance to deep evaluation (default 3)
- `minScore`: minimum pre-screen score to advance (default 5.0)
- `diversityAxes`: categories for forced divergence
- `dimensionFilters`: e.g., `{"Commercial": 7}` — only show ideas with Commercial >= 7

## Composition

```
/idea-lab → best idea selected → /founder-mode → built product with GTM kit
```

From "I don't have an idea" to "launched product" in one pipeline.

## Dependencies

- **Required:** `architect` skill (for Phase 3 deep evaluation)
- **Optional:** `founder-mode` (to build the winning idea)

## Usage

```
/idea-lab "I need an idea for a FinTech hackathon, 48 hours, team of 2"
/idea-lab "SaaS product for remote teams, must be profitable in 6 months"
/idea-lab "Open source developer tool that solves a real pain point"
/idea-lab resume
```

## Crash Recovery

State persisted to `.idea-lab/state.json`. If your session crashes mid-evaluation, run `/idea-lab resume` to continue from the next unevaluated idea.
