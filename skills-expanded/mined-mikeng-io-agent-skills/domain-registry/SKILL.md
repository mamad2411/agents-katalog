---
name: domain-registry
description: Reference library of domain definitions used by deep-* skills to select appropriate expert agents. Not invocable standalone — read via the Read tool by context, deep-audit, deep-verify, deep-review, deep-research, deep-explorer, and deep-council.
location: managed
context: reference
---

# Domain Registry

This is a REFERENCE LIBRARY. Skills read it via the `Read` tool to determine which domain experts to spawn for a given artifact type. It is never invoked directly.

## Files

- `domains/technical.md` — Software engineering, infrastructure, security, testing, performance
- `domains/business.md` — Finance, legal, product, strategy, marketing, operations
- `domains/creative.md` — Design, UX, content, brand

## How Skills Use It

1. Skill analyzes conversation context for domain signals
2. Skill reads one or more `domains/*.md` files
3. Skill matches signals against each domain's `trigger_signals`
4. Skill spawns expert agents resolved from matching entries

See `README.md` for the full Lookup Protocol (Exact Match → Adapted Match → Virtual Expert Synthesis).
