---
name: claude-seo-unlighthouse
description: Multi-page Lighthouse audit via the MIT-licensed Unlighthouse CLI. Free-tier alternative to running PageSpeed against every URL on a site — no API quota burn, runs locally.

compatibility: "Requires Node 18+ and the unlighthouse npm package. Run extensions/unlighthouse/install.sh to pre-warm."
metadata:
  version: "2.2.0"
---

> **Nota per Kimi Code:** questa skill è convertita dal plugin Claude Code `claude-seo`. I comandi slash (`/seo ...`) non sono disponibili; descrivi semplicemente in linguaggio naturale cosa vuoi analizzare. Gli script sono in `~/.kimi/skills/claude-seo/scripts/`.



# seo-unlighthouse

Run Lighthouse against every URL on a site (up to a configurable cap)
and aggregate the results. Useful when:

- PageSpeed Insights' free quota (25k QPD) isn't enough for a large site.
- You want offline / local CWV measurement (CI integration, restricted environments).
- You need a quick site-wide regression check after a deploy.

## Prerequisites

- Run `extensions/unlighthouse/install.sh` (no API key needed).
- Node 18+ on `$PATH`.

## Routing

| Command | Effect |
|---|---|
| `unlighthouse` | Mobile audit, up to 200 routes, JSON+HTML report in a temp dir |
| `unlighthouse <url> --device desktop` | Desktop form factor |
| `unlighthouse <url> --max-routes 50 --output-dir ./reports` | Cap + persist |

All flags forward to `~/.kimi/skills/claude-seo/scripts/unlighthouse_run.py` which handles
url_safety pre-flight and subprocess timeout management.

## Output handling

The wrapper reads `ci-result.json` from the Unlighthouse output dir and
returns it parsed. Aggregate fields:

- `score.performance` (median across audited routes)
- `score.accessibility`, `score.bestPractices`, `score.seo`
- Per-route breakdown is available in `<output_dir>/ci-result.json`

## Cross-skill delegation

- For single-URL field data (CrUX), use `claude-seo-google psi` / `claude-seo-google crux`.
- For LCP subpart decomposition on slow pages, use the
  `~/.kimi/skills/claude-seo/scripts/lcp_subparts.py` workflow (Phase C).
