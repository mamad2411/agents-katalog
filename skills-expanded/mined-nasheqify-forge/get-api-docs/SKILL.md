---
name: get-api-docs
description: >
  Fetch current API documentation for external libraries before
  coding against them. Prevents hallucinated parameters and stale
  interfaces.
  Triggers when about to write code against an unfamiliar or version-sensitive external API/library; NOT for the stdlib or well-known stable APIs.
status: active
relevant_for: ["main-code-agent"]
invocation:
  primary: workflow-step
  secondary: [user-facing, sub-skill]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: get-api-docs

## Purpose

Fetch current, curated API documentation for external libraries
before coding against them. Prevents hallucinated parameters and
stale interfaces.

## When to call

- Before the first API call against an external library in a
  task.
- On uncertainty whether a parameter / method is still current.
- When a reviewer reports an "API currency" finding.

## Prerequisite

```bash
chub --version 2>/dev/null || echo "MISSING: npm install -g @aisuite/chub"
```

## Workflow

### 1. Search

```bash
chub search "<library-name>"
```

Returns available doc IDs (format: `author/entry-name`).

### 2. Fetch the docs

```bash
chub get <id>                    # default (Python)
chub get <id> --lang js          # JavaScript variant
chub get <id> --version 2.0.0    # specific version
chub get <id> --full             # main + every reference
chub get <id> --file advanced    # specific reference file
```

Markdown is printed directly. Read it, then code.

### 3. Annotate (on discoveries)

```bash
chub annotate <id> "<precise note>"
```

Annotations show up on the next `chub get` automatically.
Cross-session persistent.

## Common doc IDs

```bash
chub search "fastapi"
chub search "nats"
chub search "pydantic"
chub search "postgres asyncpg"
chub search "litellm"
chub search "ollama"
chub search "apscheduler"
chub search "pgvector"
chub search "neo4j"
```

## Behaviour rule

Default: always run `chub get` before the first API call against
a new library inside a task. Exception: the library is trivial
(stdlib, well-known APIs like `os.path`, `json`).

Existing annotations are appended automatically — watch for
`[ANNOTATION]` blocks.

## WebFetch fallback (edge-case behavior questions)

chub returns curated SDK overviews — good for "what is the API
surface" questions: which methods, which parameters, which shapes.

For **specific behavior questions** chub typically does NOT have
the answer:

- Header emission (does `GET /v1/models` return rate-limit headers?)
- Parameter shapes at edge cases (what does `stream_options=` emit
  on the final chunk vs intermediate chunks?)
- Per-endpoint version-specific changes
- Per-mediator pass-through behavior (does the proxy forward
  upstream's `x-ratelimit-*` headers?)

For these, fall back to `WebFetch` on canonical first-party docs
(`console.<vendor>.com/docs/...`, `docs.<lib>.ai/...`). chub is a
layer above first-party docs — it trades depth for curation, and
the depth is where edge-case answers live.

When in doubt: chub first (cheap), then WebFetch if the chub
answer is generic. Concrete recurrence shape: chub returns a
generalized SDK overview; specific behavior questions
(per-endpoint rate-limit-header emission, streaming-cost-header
trailing behavior, mediator-side pass-through) only resolve from
canonical first-party docs via WebFetch.

## Boundary

- No research workflow → research/WORKFLOW.md (`get_api_docs` is
  only API lookup, not domain research).
- No code generation — MCA writes the code; `get_api_docs` only
  delivers the docs.
- No library comparison — research workflow on alternatives
  evaluation.

## Anti-patterns

- **NOT** write code against a library without `chub get` when
  the library is new. INSTEAD always lookup before the first
  API call in a new lib. Because: API assumptions from memory
  are often stale.
- **NOT** ignore ANNOTATION blocks. INSTEAD read them; they
  contain consumer-specific conventions. Because: annotations
  are the gap between lib defaults and the consumer's stack.
- **NOT** drop the docs on a "well-known" lib when the last
  check is >6 months old. INSTEAD lookup when uncertain.
  Because: APIs change.
