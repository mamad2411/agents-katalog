---
name: chub
description: Fetch authoritative API docs from context-hub registry (Andrew Ng). Use before writing integration code for any third-party API to reduce hallucination. Search, fetch, annotate, and rate documentation.
---

# Context-Hub (chub)

Fetch curated, LLM-optimized API documentation from the context-hub registry.
**Always run `chub search` before writing integration code for a third-party API.**

## Commands

**Search registry:**
```bash
chub search "stripe"
chub search "openai" --tags llm
chub search              # list all available docs
```

**Fetch documentation:**
```bash
chub get stripe/api
chub get openai/api --lang py       # Python-specific variant
chub get anthropic/sdk --lang js    # JS-specific variant
chub get stripe/api --full          # all files, not just entry point
chub get stripe/api --json          # structured JSON output for parsing
```

**Persist learnings across sessions:**
```bash
chub annotate stripe/api "webhook events missing from docs"
chub annotate openai/api "rate limit header: x-ratelimit-remaining-requests"
```

**Rate documentation quality:**
```bash
chub feedback stripe/api accurate
chub feedback openai/api incomplete
```

**Keep registry fresh:**
```bash
chub update              # pull latest registry
chub update --force      # force full refresh
chub cache status        # check cache state
chub cache clear         # wipe local cache
```

## When to use
- Before writing code that integrates any third-party API
- When uncertain about API auth patterns, error codes, or request shape
- After discovering a documentation gap — annotate it for future sessions

## Typical agentic workflow
1. User asks to integrate an API (e.g. Stripe)
2. Run `chub search stripe` → find the registry ID
3. Run `chub get stripe/api --lang py` → read authoritative docs
4. Write integration code grounded in actual docs
5. If gap found: `chub annotate stripe/api "note about gap"`

## Save docs to vault
```bash
chub get stripe/api --lang py > "Sources/chub - stripe-api-py.md"
```

## Notes
- Installed at `/opt/homebrew/bin/chub` (v0.1.3)
- Config at `~/.chub/config.yaml`
- Registry is community-maintained markdown; all docs are inspectable
- Use `--json` flag when piping output to other tools or scripts
