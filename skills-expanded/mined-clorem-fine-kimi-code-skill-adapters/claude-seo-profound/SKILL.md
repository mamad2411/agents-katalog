---
name: claude-seo-profound
description: Profound LLM citation tracker (extension). Time-series brand citation rates across ChatGPT, Perplexity, and other LLMs. Pairs with seo-seranking for triangulated AI visibility coverage.

compatibility: "Requires a Profound API key (set PROFOUND_API_KEY by running extensions/profound/install.sh)."
metadata:
  version: "2.2.0"
---

> **Nota per Kimi Code:** questa skill è convertita dal plugin Claude Code `claude-seo`. I comandi slash (`/seo ...`) non sono disponibili; descrivi semplicemente in linguaggio naturale cosa vuoi analizzare. Gli script sono in `~/.kimi/skills/claude-seo/scripts/`.



# seo-profound

Profound is purpose-built for LLM brand-mention tracking. While
SE Ranking samples prompts on demand, Profound continuously polls and
publishes time-series so trend deltas (week-over-week, month-over-month)
are first-class.

## Prerequisites

- Run `extensions/profound/install.sh` or `install.ps1`.
- Profound API key.
- Before any tool call, check `~/.claude/settings.json` has `env.PROFOUND_API_KEY`.

## Routing

| Command | Purpose |
|---|---|
| `profound citations <brand>` | Current citation rate per LLM + 30-day trend |
| `profound prompts <brand>` | Top prompts that surface (or fail to surface) the brand |
| `profound competitors <brand>` | Brands cited alongside `brand` for the same prompts |
| `profound alerts <brand>` | Spike/drop alerts vs. 7-day baseline |

## Output conventions

- Cite Profound on every metric: "Profound (live, confidence 0.90)".
- Profound covers ChatGPT + Perplexity natively; for Gemini / AI
  Overviews / AI Mode coverage, defer to `claude-seo-seranking`.
- For Google AI Overviews citation rate, also cross-reference
  `claude-seo-dataforseo` AI visibility tools when available.

## Cross-skill delegation

- For end-to-end AI search audit (passage citability + brand mentions + platform-specific tuning), hand back to `claude-seo-geo`.
- For prompt-set design + AI Cleanup pattern detection in cited content, fall back to `claude-seo-content`.
