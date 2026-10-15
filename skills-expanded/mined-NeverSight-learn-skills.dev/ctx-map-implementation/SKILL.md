---
name: ctx-map-implementation
description: Explore all repos in the workspace to build the implementation.md for a feature, mapping its current state end-to-end. Use when documenting how an existing feature is actually built.
metadata:
  author: nicolasse
  version: "2.0.0"
---

# Map Feature Implementation

You are an expert at this workspace's architecture. Your job is to explore the codebase and generate an accurate `implementation.md` for a feature — a complete description of how it's built today across all repos.

This skill produces a factual map of the current implementation. It does NOT design or propose changes. It describes reality.

## Input

The user provides a **feature name** (e.g., "follow-ups", "RAG catalog", "web chat", "campaigns").

### Feature Resolution

1. List all directories under `context/`
2. Match the user's request semantically (e.g., "seguimiento", "follow up", "followUps" → `follow-up/`)
3. **If confident:** confirm which feature you matched and proceed
4. **If ambiguous or no match:** list available features and ask the user to pick

If the feature directory doesn't exist yet, ask the user if they want to create it (with all three template files from `_template/`) before proceeding.

### Overwrite Check

If `context/{feature}/implementation.md` already exists and has content beyond the template:
- Show the user what's currently there
- Ask explicitly: overwrite, merge with new findings, or cancel
- Do NOT overwrite without confirmation

## Process

### Phase 1: Load existing context

Read whatever already exists for this feature:
- `context/{feature}/product.md` — understand what this feature is supposed to do
- `context/{feature}/engineering.md` — understand the expected interfaces and constraints

These files give you a hypothesis of what to look for. If they don't exist or are empty, work from the feature name alone.

### Phase 2: Discover repos

List all directories at the workspace root (skip `context/`). Each directory with a `.git` folder is a repo to potentially explore.

### Phase 3: Deep exploration across repos

This is the critical phase. You must explore **all relevant repos** to build a complete picture of how this feature is implemented today. **Use a single agent** to explore across all repos — cross-repo context matters more than parallelism.

For each repo that might be involved, search for:

- **Models/types**: domain models, database schemas, ORM models, proto definitions, types
- **Handlers/controllers**: event handlers, API routes, Lambda handlers, RPC methods
- **Business logic**: services, use cases, processors, state machines
- **Data access**: repositories, queries, ORM calls, vector store operations
- **Config**: environment variables, feature flags, queue names, topic names
- **Tests**: test files reveal behavior, edge cases, and expected flows

Search strategy:
- Use multiple keywords related to the feature (e.g., for "follow-ups": `follow_up`, `followUp`, `follow-up`, `reminder`, `scheduled_message`)
- Follow the trail: when you find a handler, trace what it calls; when you find a model, find who reads/writes it
- Read key files in full to understand behavior, not just grep matches
- Cross-reference with `product.md` use cases — find the code path for each one

### Phase 4: Map the implementation

From your exploration, build a complete picture:

1. **Entry points**: How does this feature get triggered? (UI action, cron job, event, API call)
2. **Key files**: Every file that contains logic for this feature, organized by repo
3. **Flows**: For each use case in `product.md` (or discovered behavior if no product.md), trace the step-by-step code path from trigger to outcome
4. **Processing**: What transformations or logic happen at each step along the flow
5. **Data model**: Actual schemas, tables, types — copy the real definitions from code
6. **Communication**: Message queues, RPC calls, HTTP endpoints with actual names
7. **Config**: Env vars and feature flags that affect behavior
8. **Error handling**: What happens on failure — retries, dead letter queues, fallbacks
9. **Edge cases & quirks**: Non-obvious behavior, performance considerations, known gotchas
10. **Known limitations**: Things that are missing, broken, or incomplete based on what you see in code vs what `product.md` or `engineering.md` expect

### Phase 5: Generate implementation.md

Write the file to `context/{feature}/implementation.md` using the project template as a base (`context/_template/implementation.md`) but filling it with real data from your exploration.

Key principles:
- **Be specific.** File paths, function names, table names, queue names — all real, all from the code.
- **Be honest.** If something described in `product.md` isn't actually implemented, say so.
- **Be complete.** If you found code for this feature in a repo you didn't expect, include it.
- **Be current.** Describe what IS, not what should be.

### Phase 6: Cross-reference with contracts

After generating, do a quick sanity check:

- Does every use case in `product.md` have a corresponding flow in `implementation.md`?
- Are the interfaces in `engineering.md` consistent with what you found in code?
- Flag any gaps or inconsistencies as a note at the end of the file.

## Quality checklist

Before finishing, verify:
- [ ] You explored at least 3+ repos (features typically span multiple services)
- [ ] Every file path listed actually exists in the codebase
- [ ] Every flow is traceable step-by-step with real function/handler names
- [ ] Data model includes actual schema definitions from code, not summaries
- [ ] Events and queues use actual names from the codebase
- [ ] Known limitations are documented honestly
- [ ] Edge cases and non-obvious behavior are captured

## Output

Show the user:
1. A summary of what you found — which repos, how many files, any surprises
2. The generated `implementation.md` content
3. Any gaps or inconsistencies found vs `product.md` / `engineering.md`
4. Ask for feedback before writing the file
