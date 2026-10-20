---
name: claude-seo-flow
description: >
  FLOW framework integration — evidence-led SEO using the Find → Leverage →
  Optimize → Win loop. Surfaces stage-specific AI prompts from the FLOW
  knowledge base (41 prompts, CC BY 4.0). Use when user says "FLOW", "FLOW
  framework", "seo flow", "evidence-led SEO", "find leverage optimize win",
  or wants stage-specific SEO prompts.
license: MIT
metadata:
  author: AgriciDaniel
  version: "2.2.0"
  category: seo
---

> **Nota per Kimi Code:** questa skill è convertita dal plugin Claude Code `claude-seo`. I comandi slash (`/seo ...`) non sono disponibili; descrivi semplicemente in linguaggio naturale cosa vuoi analizzare. Gli script sono in `~/.kimi/skills/claude-seo/scripts/`.



# FLOW Framework — Find · Leverage · Optimize · Win

> Framework and prompts © Daniel Agrici, CC BY 4.0 — github.com/AgriciDaniel/flow

FLOW is an evidence-led SEO operating model built for the AI-search era. Claude SEO
integrates the FLOW prompt library (41 prompts across 5 stages) so every analysis can
be driven by structured, evidence-backed AI prompts rather than improvised queries.

**Runtime context:** Load `references/flow-framework.md` on every `flow` activation.
Load prompt files on demand — only for the stage the user requests.

---

## Commands

| Command | What it does |
|---------|-------------|
| `flow` | Show FLOW overview + stage menu |
| `flow find [url\|topic]` | Find-stage: keyword research, gap analysis, SERP intent mapping (5 prompts) |
| `flow leverage [url]` | Leverage-stage: backlink strategy, off-site authority (1 prompt) |
| `flow optimize [url]` | Optimize-stage: select 2-3 most relevant of 21 prompts based on context |
| `flow win [url]` | Win-stage: BOFU, conversion rate, dual-surface scorecard (3 prompts) |
| `flow local [url]` | Local-stage: GBP optimization, meta, title tags, local audits (11 prompts) |
| `flow prompts` | Full index of all 41 prompts — stage, name, trigger conditions |
| `flow sync` | Pull latest prompt files from github.com/AgriciDaniel/flow |

---

## Orchestration Logic

### On `flow` (no sub-command)
1. Read `references/flow-framework.md`
2. Show the FLOW stage overview with a one-line description of each stage
3. Ask: which stage matches the user's current situation?

### On `flow find [url|topic]`
1. Read all files in `references/prompts/find/`
2. Apply each prompt to the URL or topic
3. Cross-reference: "For deeper SERP clustering, see `cluster`"

### On `flow leverage [url]`
1. Read the file in `references/prompts/leverage/`
2. Apply to the URL's current backlink context
3. Cross-reference: "For raw backlink data, see `backlinks`"

### On `flow optimize [url]`
1. Read all file names in `references/prompts/optimize/`
2. Read prior analysis context (URL, industry vertical, any prior skill output in conversation)
3. Select 2-3 most relevant prompts; load only those files
4. Apply selected prompts; note the others are accessible via `flow prompts`
5. Cross-reference: "For full content quality analysis, see `content` and `geo`"

### On `flow win [url]`
1. Read all files in `references/prompts/win/`
2. Apply each prompt to the URL's conversion and BOFU context
3. Cross-reference: "For SXO persona scoring, see `sxo`"

### On `flow local [url]`
1. Read all files in `references/prompts/local/`
2. Apply to the URL's local SEO context
3. Cross-reference: "For full local SEO analysis, see `local` and `maps [command]`"

### On `flow prompts`
1. Read `references/prompts/README.md`
2. Display the full index: all 41 prompts with stage, name, trigger conditions

### On `flow sync`
1. Run: `~/.kimi/skills/claude-seo/.venv/bin/python ~/.kimi/skills/claude-seo/scripts/sync_flow.py`
2. Display the JSON summary (files added, updated, unchanged)
3. Show attribution notice after sync completes

---

## Context Matching (Optimize stage)

The optimize stage has 21 prompts. Dumping all 21 is noise. Select by priority:

1. **Industry vertical** (SaaS → on-page + technical; local → citations + GBP; publisher → E-E-A-T + freshness)
2. **Prior skill output** (claude-seo-technical flagged crawl issues → technical optimize prompts; claude-seo-content flagged E-E-A-T gaps → content optimize prompts)
3. **URL signals** (product pages → conversion; blog → freshness + authority)

Always surface exactly 2-3 prompts. State which prompts you chose and why.

---

## Reference Files

Load on-demand — do NOT load all at startup:
- `references/flow-framework.md` — FLOW operating model (load on every `flow` activation)
- `references/bibliography.md` — Evidence sources; load when citing studies or statistics
- `references/prompts/README.md` — Prompt index; load for `flow prompts`
- `references/prompts/find/` — 5 prompts; load for `flow find`
- `references/prompts/leverage/` — 1 prompt; load for `flow leverage`
- `references/prompts/optimize/` — 21 prompts; load selectively for `flow optimize`
- `references/prompts/win/` — 3 prompts; load for `flow win`
- `references/prompts/local/` — 11 prompts; load for `flow local`

---

## Attribution

Every `flow` activation (any sub-command) outputs before analysis:

```
Framework and prompts © Daniel Agrici, CC BY 4.0 — github.com/AgriciDaniel/flow
```

Do not omit or modify the attribution.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| `references/flow-framework.md` missing | "FLOW reference files not synced. Run: `flow sync`" |
| Prompt file missing | "Run `flow sync` to pull the latest prompts from the FLOW repo." |
| `sync_flow.py` network error | Display the script's stderr. Check rate limits: `gh api rate_limit`. |
| `sync_flow.py` auth error | Run `gh auth login` then retry. |
