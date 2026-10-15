---
name: wise-scraper
description: "Structured web scraping for AI coders: explore, then exploit with shipped templates, runner, and hooks."
metadata:
  author: kundeng
  version: "1.0.0"
---

# WISE Scraper

WISE teaches an AI coding agent **structured, repeatable web scraping** for JS-rendered sites. The goal is a **working scraping project** built from shipped WISE assets.

> **Rule 0 — Orient before acting.** Before opening a browser or writing any code, read `references/guide.md § Big Picture` to understand what you're building and what decisions you need to make. Only then start exploration.

```
Orient → Explore → Evidence → Choose tier → Exploit → JSONL → Assemble
```

1. **Orient** — read the schema, templates, and runner options; understand what's shipped
2. **Explore** — inspect the live site with `agent-browser`, test selectors, map navigation
3. **Evidence** — record selector proof and DOM observations before designing the exploit
4. **Choose tier** — prefer shipped plumbing, escalate only when justified; ask about runtime preference if unclear
5. **Exploit** — assemble a profile from template fragments, run it, extend with hooks or task-local code
6. **Process** — JSONL is the intermediate truth; assemble markdown/CSV/JSON later

Use when: JS-rendered sites, pagination, UI state, filter combos, structured repeatable output.
Not when: a stable API/export exists, or static `curl` is clearly enough.

## Agent Contract

1. **Orient first.** Read `references/guide.md § Big Picture` and scan `templates/*.yaml` before touching `agent-browser` or writing code.
2. **Explore before exploiting.** Use `agent-browser` to inspect DOM, interactions, and state.
3. **Show evidence.** Record selectors, DOM snippets, or snapshots before writing profiles.
4. **Assemble from fragments.** Templates in `templates/*.yaml` are composable — combine them. They are not alternatives.
5. **Infer runtime preference.** If the user mentions Crawlee, Scrapy, or a Python pipeline, use Tier 4. If unclear, ask.
6. **DOM eval for live extraction.** HTML parsing libraries are for post-processing only.

### Exploit Tiers

| Tier | When | What |
|---|---|---|
| 1 | Target fits declarative flow | Assemble template fragments + shipped `agent-browser` runner |
| 2 | Target needs adaptation | Copy/adapt runner modules, hooks, helpers, or AI adapter |
| 3 | Target exceeds reference boundary | Bespoke project, carrying WISE discipline |
| 4 | User prefers alternative runtime | Same YAML profile, executed via Crawlee or Scrapy+Playwright runner |

When escalating, explain why the simpler tier is insufficient. For Tier 4, the user's runtime preference (or project context like existing `package.json`/`requirements.txt`) determines the choice.

### Runner Boundary

The **shipped runner** (`references/runner/`) uses `agent-browser` for browser driving. It handles: YAML profile interpretation, DOM-eval extraction, selectors, interactions, pagination, matrix, post-processing.

**Alternative runners** interpret the same YAML profile with a different backend. See `references/comparisons.md` for Crawlee and Scrapy+Playwright runner designs.

The agent may extend beyond any runner: hooks, helper scripts, chaining, AI-assisted extraction.

## Read Next — by step

Do **not** read all references upfront. Read only what the current step needs:

| Step | Read |
|---|---|
| Orient | `references/guide.md § Big Picture` |
| Explore | `agent-browser` CLI help (`agent-browser --help`) |
| Choose tier / runtime | SKILL.md § Exploit Tiers, `references/comparisons.md` (if Tier 4) |
| Write profile | `references/field-guide.md`, `references/schema.cue`, scan `templates/*.yaml` |
| Add hooks | `references/guide.md § Hook System` |
| Add AI adapter | `references/ai-adapter.md` |
| Config / CLI | `references/guide.md § Config Composition`, `§ Runner CLI Reference` |
| Worked examples | `examples/overview.md` |

## Working Rules

- **Assemble from template fragments** — combine pieces, don't pick one template
- **Header-based table mapping** — not positional
- **Sort verification required** — verify state changed after sort interactions
- **Avoid ambiguous clicks** — scope by CSS/role/context
- **JSONL is intermediate truth** — assemble final formats later

## Common Failure Modes

- Jumping to `agent-browser` or code before reading the framework
- Designing the exploit before collecting exploration evidence
- Jumping to bespoke code when template fragments would work
- Using HTML parsing on the live page instead of DOM eval
- Reaching for AI when selectors and plumbing are sufficient
- Ignoring user runtime preference (Crawlee/Scrapy) and defaulting to shipped runner
