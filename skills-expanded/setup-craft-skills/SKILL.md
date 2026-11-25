---
name: setup-craft-skills
description: "Run once per repository after installing craft-skills, or when the project's vocabulary or conventions have drifted. Scaffolds an optional CONTEXT.md — domain glossary, stack, conventions, untouchables — that the craft skills read to match the codebase. The skills work without it."
---

# Setup Craft Skills

## The failure mode this fixes

The craft skills are generic by default — and generic is the failure: `name-things` proposing vocabulary your team doesn't use, `delete-this` not knowing your webhook registry resolves handlers by string, `fit-in` guessing at conventions the team settled years ago. Without shared context, every skill re-detects (or mis-guesses) these per run. This skill captures the project's vocabulary, conventions, and untouchables **once**, in a file all the other skills read.

## When to Use This Skill

- First time using the craft-skills plugin in a repository
- The project's domain vocabulary or conventions have changed and `CONTEXT.md` is stale

Run this **once per repo** (recommended, not required) before `explain-back`, `name-things`, `delete-this`, `seams`, `loud-errors`, `boyscout`, `why-comments`, or `fit-in`. Those skills read the file this creates *if it's present* — so their output matches *your* codebase instead of generic defaults. Skip it and the skills still work; they just fall back to detecting conventions on the fly.

## What it creates

A `CONTEXT.md` at the repo root capturing the shared context the craft skills consume:
- **Domain glossary** — the real nouns of the product, so `name-things` uses your vocabulary
- **Language & stack** — so examples and idioms match (TS vs Go vs Python conventions differ)
- **Conventions** — testing style, error-handling style, file layout, what "done" means
- **Untouchables** — public APIs, plugin surfaces, and dynamically-referenced code that `delete-this` must never remove

## Instructions

### 1. Detect, don't interrogate

Inspect the repo first — read `package.json` / `go.mod` / `pyproject.toml`, the test setup, a few representative source files, and any existing `README`/`CONTRIBUTING`. Infer the stack, test runner, and layout. Only ask the human about things you genuinely cannot detect.

### 2. Extract the domain glossary

Pull the recurring domain nouns from the code and docs (the entities, not the framework terms). Present the list and let the human correct or canonicalize names. This is what `name-things` aligns to. For each term capture:
- **What it means** — one line, in the team's words.
- **Avoid** — the near-synonyms that should *not* be used for it (this becomes a project-specific ban list for `name-things`: e.g. "Issue tracker — _avoid_: backlog, backlog backend").
- **Relationships** — how the core entities relate ("an Order has many LineItems"), so explanations and names stay consistent.
- **Flagged ambiguities** — any word that was being used for two different things, and the resolution. Recording the *resolved* split is what stops the codebase from drifting back into two vocabularies.

### 3. Capture conventions

Record the observed conventions so the craft skills don't fight them:
- Test framework and where tests live
- Error-handling pattern (exceptions? result types? error returns?) — informs `loud-errors`
- How side effects are usually isolated (informs `seams`)
- Commit/PR granularity expectations (informs `boyscout` and `delete-this` staging)

### 4. Mark the untouchables

List public entry points, exported package surfaces, plugin/extension points, route tables, and anything accessed dynamically (reflection, string keys, DI). `delete-this` treats these as never-auto-delete.

### 5. Write CONTEXT.md and confirm

Write the file, show it to the human, and confirm it's accurate before finishing. A wrong glossary is worse than none.

### 6. Make it discoverable

If the repo has a `CLAUDE.md` (or an equivalent agent-instructions file), add a one-line pointer to `CONTEXT.md` — "Domain glossary, conventions, and untouchables live in `CONTEXT.md`." — so agents that never fire a craft skill still find it. Without the pointer, the file is skill-private state; with it, it's shared project memory.

## Output format

```
DETECTED (from the repo, not asked)
  stack: <languages> | tests: <framework, location> | build: <command>

GLOSSARY CANDIDATES (for human confirmation)
  - <Term> — <one-line meaning> — avoid: <banned near-synonyms>

UNTOUCHABLES
  - <surface> @ <file> — why it must never be auto-removed

WRITTEN
  CONTEXT.md @ repo root — confirmed by human: <yes / pending>
  CLAUDE.md pointer: <added / no CLAUDE.md present>
```

## CONTEXT.md template

```markdown
# Project Context

> If this file contradicts the code, trust the code — then re-run `/setup-craft-skills` to re-capture.

## Stack
- Language(s):
- Test framework:
- Build/typecheck command:

## Domain Glossary

### <Term>
What it means — one line, in the team's words.
_Avoid_: <near-synonyms that must not be used for this thing>

## Relationships
- <Entity> has many <Entity>
- <Entity> carries one <Entity> at a time

## Flagged ambiguities
- "<word>" was used for both <X> and <Y> — resolved: <X> is now **<canonical term>**; "<word>" is no longer a domain term.

## Conventions
- Error handling:        (exceptions? result types? error returns? — informs loud-errors)
- Side-effect isolation: (how I/O is kept out of logic — informs seams)
- Tests live in:
- Commit granularity:

## Untouchables (delete-this must never auto-remove)
- Public exports:
- Dynamic access points:
- Plugin/route surfaces:
```

## Worked example

A filled-in `CONTEXT.md` for a payments service — note how the glossary feeds `name-things` (vocabulary + the `Avoid` ban list) and the untouchables feed `delete-this`:

```markdown
# Project Context

> If this file contradicts the code, trust the code — then re-run `/setup-craft-skills` to re-capture.

## Stack
- Language(s): TypeScript (Node)
- Test framework: Vitest
- Build/typecheck command: `pnpm typecheck && pnpm build`

## Domain Glossary

### Charge
A single attempt to capture money from a customer's card via the gateway.
_Avoid_: payment, transaction, txn (those mean other things below)

### Invoice
The billable record a Charge pays down. Can be partially paid.
_Avoid_: bill, statement

### Refund
A reversal of a settled Charge. Always references the original Charge.
_Avoid_: chargeback (a chargeback is bank-initiated and is a different entity)

## Relationships
- An Invoice has many Charges (retries, partial payments)
- A Refund references exactly one Charge

## Flagged ambiguities
- "transaction" was used for both a Charge and a DB transaction — resolved: money movement is a **Charge**; "transaction" now refers only to the database primitive.

## Conventions
- Error handling: domain errors as typed classes (PaymentDeclined) with `cause` preserved; no swallowing
- Side-effect isolation: pure pricing/decision logic in `domain/`, gateway/db calls in `adapters/`
- Tests live in: `*.test.ts` next to the source
- Commit granularity: one concern per commit; deletions separate from behavior

## Untouchables (delete-this must never auto-remove)
- Public exports: everything re-exported from `src/index.ts`
- Dynamic access points: webhook handlers resolved by `event.type` string in `webhooks/registry.ts`
- Plugin/route surfaces: Express routes registered in `routes/*.ts`
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| Interrogating instead of detecting | Twenty questions and the human closes the session. Read the repo; ask only what the code can't answer. |
| Framework nouns in the glossary | `Controller`, `Middleware`, `Repository` aren't your domain — they're everyone's. The glossary is for the product's entities. |
| Writing the file without confirmation | A wrong glossary is worse than none: every skill that reads it propagates the error. |
| Treating CONTEXT.md as permanent | Vocabulary and conventions drift. A stale glossary re-introduces the two-vocabularies problem it exists to prevent. |

## Mental Model

> Capture the project's vocabulary and rules once, so every craft skill speaks your codebase's language instead of a generic one.
