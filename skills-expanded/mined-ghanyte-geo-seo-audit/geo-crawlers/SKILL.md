---
name: geo-crawlers
description: >
  Parse a site's robots.txt and report AI-bot policy coherence. Classifies
  every relevant user-agent into 3 categories (training / RAG-search /
  user-request) and surfaces inversions (e.g. GPTBot allowed but
  OAI-SearchBot blocked — backwards configuration). Use when user asks
  about robots.txt, AI bots, GPTBot, ClaudeBot, crawler access.
allowed-tools: Bash, Read, WebFetch
---

# geo-crawlers — AI crawler policy audit

Single-call audit of a domain's robots.txt with 3-category bot taxonomy.

## Command

```bash
python3 -m scripts.checks.crawlers <url>
```

The script fetches `<url>/robots.txt`, parses every relevant directive (user-agent, allow, disallow), and classifies each AI-related bot it sees.

## Bot taxonomy (3 categories)

The toolkit groups AI bots by **what they do with the data**, not by which company runs them. The three categories have *opposite default policies*:

| Category | Default policy | Examples |
|---|---|---|
| 🔴 **Training** | Block by default — fetched to train base models, no live citation benefit | GPTBot, ClaudeBot, anthropic-ai, CCBot, Applebot-Extended, Google-Extended |
| 🟢 **RAG / search** | Allow by default — fetched at query time to cite live in answers | OAI-SearchBot, PerplexityBot, Claude-SearchBot |
| 🟢 **User-request** | Allow by default — fetched only when a user explicitly asks the assistant to read a URL | ChatGPT-User, Claude-User, Perplexity-User, Google-Agent, MistralAI-User |

29 bots are catalogued in `docs/CRAWLERS_TAXONOMY.md`.

## What gets flagged

- `CR1` — A high-intent bot (RAG or user-request) is **explicitly blocked**. Likely an oversight; biggest hit on AI search visibility.
- `CR2` — Inverted config (e.g. ClaudeBot allowed, Claude-SearchBot blocked). The "wrong" bot of the pair has the right policy.
- `CR-INFO2` — RAG bot not explicitly listed (allowed via `User-agent: *`). Cosmetic — a `low` finding for clarity / future-proofing.
- `CR-INFO3` — User-request bot not explicitly listed. Same.

## Why this matters

Most public guides repeat "allow GPTBot to be visible in ChatGPT" — that's wrong. **GPTBot is a training crawler**; allowing it does not help you appear in ChatGPT search results. The bot to allow for ChatGPT live citation is **OAI-SearchBot**. Same pattern for Anthropic (ClaudeBot trains, Claude-SearchBot retrieves). The `geo-crawlers` audit catches this confusion.

Source: `docs/sources/02-rankit-crawlers-ia-2026-03.md` (archived).

## Output

Markdown report to stdout. When called from `run_audit.py`, feeds Annex B.

## Dependencies

- `scripts/checks/crawlers.py`
- Python: `requests`
