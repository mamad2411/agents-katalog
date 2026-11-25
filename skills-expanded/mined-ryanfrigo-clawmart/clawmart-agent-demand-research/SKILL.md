---
name: clawmart-agent-demand-research
description: Use this skill during the autopilot ideate phase to research what autonomous agents actually pay for — mining local reference corpora (karpathy-skills, public-apis) and scraping agent marketplaces — and emit 3+ fresh hypotheses into autopilot-state/hypothesis-backlog.md.
---

# Researching agent demand

## Why this exists

Clawmart is "Walmart for agents" — but Walmart only works because it stocks what people actually buy. The hard question is: *what do autonomous agents actually hand over USDC for?* We have no canonical answer yet; the autopilot exists to find it empirically. This skill is the research half of that.

## Research order (do them in order; stop when you have 3+ fresh, scored hypotheses)

### 1. Local corpora — free, fast, zero-rate-limit

**`/Users/ryanfrigo/dev/andrej-karpathy-skills/skills/`**
Read 5–10 skill folders. For each, note: what problem does it solve? Is it *stateful* (needs user account) or *stateless* (pure function of input)? Stateless + bounded-compute skills are x402-friendly; stateful is harder to monetize per-call.

**`/Users/ryanfrigo/dev/public-apis/README.md`**
Scan the table of contents. Identify categories where:
- The underlying API has a free tier with rate limits (we can proxy + rate-limit ourselves, charging a tiny USDC premium for unmetered access)
- The data has high per-call value for agents (financial, location, identity verification, translation)
- No existing clawmart skill covers the category

### 2. External sources via scrapling

Binary is at `/Users/ryanfrigo/.pyenv/shims/scrapling`. Prefer it over WebFetch for sites that block common user-agents.

Queue (pick 2–3, not all):
- `https://smithery.ai/servers?sort=popular` — top MCP servers by install. MCP ≠ x402, but popularity signals demand for the underlying capability.
- `https://github.com/search?q=%22x402%22+language%3Atypescript&type=repositories&s=updated` — who else is building on x402? Where are the gaps?
- `https://news.ycombinator.com/from?site=agent.ai` and HN Algolia `?query=%22agent%22+%22api%22&sortBy=byDate` — what agent-devs are complaining about / wishing for
- Avoid login-gated content (X, LinkedIn). Text-only scrape.

### 3. Self-audit

```bash
ls src/app/api/x402/
```

Current lineup: web-summarize, sentiment-analyzer, data-extractor, code-reviewer, voicecharm-receptionist. Categorize them. What's the coverage gap? E.g. if all 5 are "NLP over text input", we probably lack: structured data (prices, weather, forex), verification/identity, image/vision, communication primitives.

## Hypothesis format — write to `autopilot-state/hypothesis-backlog.md`

Each hypothesis is one block:

```markdown
## H-NNN: <short title>

- **Category:** new-skill | pricing-change | landing-copy | seo | product-pivot | schema
- **Hypothesis:** <one sentence, falsifiable: "If we X, then Y will increase">
- **Source:** <why do we believe this? which research input>
- **Test:** <what change ships> + <what metric we watch>
- **Effort:** <S/M/L in hours>
- **Reversibility:** <high (copy), med (new route), low (schema)>
- **Expected signal window:** <48h / 1 week>
- **Kill criteria:** <what result would send this to graveyard>
```

## Dedup rules (critical)

Before writing a new hypothesis, check:

1. Is a hypothesis with the same `title` or same `test` already in `hypothesis-backlog.md` pending? → skip.
2. Is it in `graveyard.md` with `status: killed`? → skip unless the `graveyard` reason was "timing" (not "doesn't work"). If you re-propose a killed idea, quote the graveyard entry and explain what's changed.
3. Is an active experiment already testing it? → skip.

## Things not to do

- Don't propose "rewrite the whole site with better design" — out of scope (>400 LOC).
- Don't propose protocol changes (away from x402/USDC/Base) — requires `protocol-change: true` flag which the autopilot cannot grant itself.
- Don't hallucinate metrics from scraped pages. Smithery's "install count" is a signal; your inference about "agents want X" is a hypothesis, not a fact. Flag which is which.
- Don't go wide — depth on one source beats shallow reads of ten. Three solid hypotheses > ten hand-wavy ones.
