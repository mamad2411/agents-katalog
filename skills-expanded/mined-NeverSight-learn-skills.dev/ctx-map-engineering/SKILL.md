---
name: ctx-map-engineering
description: Build the engineering.md for a feature by exploring the codebase to extract the key interfaces, constraints, and patterns. Use when mapping an existing feature's technical contracts.
metadata:
  author: nicolasse
  version: "2.0.0"
---

# Map Feature Engineering

Your job is to generate an `engineering.md` for a feature — a short technical reference with only the things that matter.

## Tone & Length

**This is critical.** The output must be concise and useful, not exhaustive. Think "senior engineer explaining the feature to a new teammate in 2 minutes", not "auto-generated API docs".

- The entire file should be **under 50 lines**
- Architecture: 2-3 sentences about which services are involved and how they talk
- Key interfaces: **only the ones that would break things if changed.** Skip internal helpers, skip obvious CRUD.
- Constraints: plain language, one line each
- Patterns: one line each
- **Minimal code snippets.** Only include a type or schema if it's truly the contract — the thing another service depends on. If it's internal, skip it.
- **No exhaustive API docs.** List the endpoint and what it does, not every field.

## Input

The user provides a **feature name**.

### Feature Resolution

1. List all directories under `context/`
2. Match the user's request semantically
3. **If confident:** confirm and proceed
4. **If ambiguous or no match:** list available features and ask

If the feature directory doesn't exist yet, ask the user if they want to create it (with all three template files from `_template/`) before proceeding.

### Overwrite Check

If `context/{feature}/engineering.md` already exists and has content beyond the template:
- Show the user what's currently there
- Ask explicitly: overwrite, merge with new findings, or cancel
- Do NOT overwrite without confirmation

## Process

### Phase 1: Load existing context

If available, read `context/{feature}/product.md` to understand what use cases to look for.

### Phase 2: Discover and explore repos

List directories at the workspace root (skip `context/`). **Use an agent to explore the repos** — spawn a single agent to search across all repos for contracts, interfaces, and patterns. Focus on:

- API contracts and event schemas — the boundaries between services
- Inter-service communication — Kafka topics, SQS queues, RPC calls, HTTP endpoints with actual names
- Shared types and interfaces — what other code depends on
- Configuration — env vars, feature flags, and settings that affect behavior
- Technical constraints visible in retries, timeouts, limits
- Patterns that repeat across the feature's code

### Phase 3: Filter ruthlessly

You will find a lot. **Most of it doesn't belong in engineering.md.** Apply this filter:

- Would changing this break another service or feature? → **Include it**
- Is this an internal implementation detail? → **Skip it, that's for implementation.md**
- Is this a pattern someone needs to follow when adding code? → **Include it**
- Is this just a standard CRUD endpoint? → **Skip it unless it has non-obvious constraints**

### Phase 4: Write engineering.md

Follow the template at `context/_template/engineering.md`. Keep it minimal. When you include a code snippet, include **only** the type/schema itself — no surrounding context, no imports, no comments.

### Phase 5: Review

Show the developer the file before writing. It should be short enough to read in under a minute.

## Output

1. Short summary of key interfaces and patterns found
2. The generated `engineering.md`
3. Ask for feedback before writing
