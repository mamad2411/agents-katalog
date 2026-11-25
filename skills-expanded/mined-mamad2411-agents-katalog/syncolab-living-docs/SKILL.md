---
name: syncolab-living-docs
description: Searches and reads Syncolab Living Docs (SKS) and proposes human-reviewed patches via sks_docs_* tools. Use for authoritative platform docs, internal/external facets, and minimal doc drift fixes.
---

# Syncolab Living Docs (SKS)

## Purpose

Use the Syngles Knowledge System (SKS) as the source of truth for Syncolab platform documentation: search before answering platform questions, fetch full docs by stable id, and propose patches for human review—never edit live docs directly.

## When to Use

- Before answering about Syncolab platform behavior, schemas, integrations, or runbooks.
- Internal flows (CML, SKS, planning, work-sync, agent runtime) when unsure—search with the right `facet`.
- Proposing doc fixes when content drifts from code (minimal patch via `sks_docs_propose_patch`).

## When NOT to Use

- Tenant agent memory (CML) → **syncolab-cognitive-memory**.
- Arbitrary vector indexes → **vectorize**.
- Direct live doc edits without the patch/review flow.

## Expected Outcome

- Answers cite SKS doc ids used (e.g. `[sks: platform.sks.architecture]`).
- Search returns lightweight summaries; full body from `sks_docs_get`.
- Patches return contribution id; not applied until human approval.

## Inputs to Gather

- Focused `query` for search.
- `facet`: `internal`, `external`, or both (default both).
- Optional `scope`, `domain`, `loadTier` (`always` | `on_demand`), `limit`.
- For patches: `docId`, one-line `summary`, minimal `bodyPatch`, optional `reasoning`.

## Workflow

1. **Search first** for platform questions: `sks_docs_search` with focused query and correct `facet`.
2. **Get full doc** when needed: `sks_docs_get` with stable `id` from search.
3. Cite doc id in the reply.
4. If content is wrong: `sks_docs_propose_patch` with smallest diff; never direct live edit.
5. External runtimes: use hydrated `sks_layer` endpoints with Bearer JWT same as tool semantics.

### Tools

- **`sks_docs_search`** — `query` (required), `facet`, `scope`, `domain`, `loadTier`, `limit`. Returns id, title, summary, scope, domain, authority, updatedAt.
- **`sks_docs_get`** — stable `id`; full markdown, headings, references, source binding, load tier.
- **`sks_docs_propose_patch`** — `docId`, `summary`, `bodyPatch` (full body or unified diff), optional `reasoning`; returns contribution id pending review.

### Facets

- **internal** — engineering/platform (architecture, integrations).
- **external** — customer/partner-facing docs.

### Hydration

- `sks_layer` on external runtimes: `endpoints`, `auth` (Bearer JWT), `enabled`, `agentPromptHint`.

### Etiquette

- Cite SKS doc ids relied on.
- Minimal patches; preserve voice and structure.
- No secrets, tokens, customer PII, or credentials in patch bodies.

## Tool Availability Rules

| Access | Behavior |
|--------|----------|
| sks_docs_* tools | Search, get, propose patch. |
| Read-only external | Search/get only; draft patches for user. |
| SKS disabled | Do not invent platform doc content. |

### Related tool sets

- `internal-wiki`
- `docs-as-code`
- `notion`

## Review / Decision / Execution Criteria

- Search before speculative platform answers.
- Patches smallest possible scope.

## Output Format

1. Query and facet used.
2. Answer with cited doc ids.
3. Patch contribution id if proposed.
4. Gaps if SKS has no coverage.

## Quality Bar

- Authoritative SKS over model guesswork for platform facts.
- No live doc mutation outside patch flow.

## Safety and Boundaries

- No secrets in patches or quotes.
- External facet for customer-facing tone when answering externals.

## Escalation / Dispatch Rules

- Memory/query APIs → **syncolab-cognitive-memory**.
- Notion customer wiki copy → **notion** only when explicitly outside SKS scope.

## References

- Legacy: `skills/old_skills.json` (`syncolab-living-docs`).
- `skills/skill.instruction.md`, `skills/meta.instructions.md`
