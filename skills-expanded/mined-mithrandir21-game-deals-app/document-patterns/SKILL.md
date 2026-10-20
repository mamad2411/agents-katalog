---
name: document-patterns
description: Survey, document, and maintain a living guide to the coding patterns, architectural conventions, and design idioms used in this codebase. Output is `docs/PATTERNS.md` (slim narrative index) plus deep `docs/patterns/<category>.md` files, written for mid-level engineers with optional senior deep-dive sections. Tone is opinionated guideline — not iron rules. Trigger when the user invokes `/document-patterns`, or says "document our patterns", "survey the conventions", "map out our coding style", "update the patterns doc", "what conventions does this project follow", or asks Claude to explain how the codebase is structured stylistically. Auto-detects bootstrap (no doc yet — wide first pass across categories) vs incremental update (per-category cursor; only re-verify what changed). Optional flags: `--scope <category>` to restrict the run to one slice; `--deep <category>` for a heavier re-verify pass. Independent of `.claude/lessons.md` — patterns may cite lesson IDs but never absorb lesson content.
---

# Document Patterns

Maintain a living guide to *what patterns this codebase uses, and why*, so engineers and future agents can apply them confidently without re-deriving conventions every session.

The output is `docs/PATTERNS.md` (a slim narrative index) plus one file per category under `docs/patterns/`. Written for **mid-level engineers** — descriptive, plain language, opinionated guideline (not iron rules). Each entry can carry an optional `Deep dive (senior)` section for advanced readers.

This skill is independent of `.claude/lessons.md`. Lessons are micro-grain corrective entries; patterns are mid-grain descriptive entries. A pattern entry **may** cite a lesson by ID under `Related lessons`, but the patterns doc never absorbs or replaces lessons.

## Scope

In scope:
- Architectural and code-level conventions: layering, MVVM, UI state shapes, data flow, DI, concurrency, testing, build setup, KMP boundaries, Compose correctness, observability, error handling, resource lifecycle.
- Anti-patterns the codebase explicitly avoids — included as a `## What we don't do` subsection inside each category file (not as standalone entries).

Out of scope:
- Non-code patterns (PR conventions, commit messages, CI workflows, branch naming) — those belong in `CONTRIBUTING.md` / `AGENTS.md`.
- `.claude/CLAUDE.md`, `AGENTS.md`, or any other agent-internal docs — never touched by this skill.
- Auto-committing. The skill writes files and stops.

## Output structure

```
docs/
├── PATTERNS.md                 # slim narrative index — entry point
└── patterns/
    ├── architecture.md
    ├── ui-state.md
    ├── compose-correctness.md
    ├── data.md
    ├── concurrency.md
    ├── errors.md
    ├── resources.md
    ├── di.md
    ├── kmp.md
    ├── testing.md
    ├── observability.md
    └── build.md
```

The seed list above is recommended, not mandatory. Empty categories are skipped — no stubs. New categories may be proposed at survey time when a coherent cluster doesn't fit existing buckets, but only with user approval.

### Categories — one-line guide

- **architecture** — module boundaries, layering, navigation surface
- **ui-state** — MVVM shape, StateFlow → Compose, state hoisting, source-of-truth flows
- **compose-correctness** — recomposition, side effects, stability, `remember` / `rememberSaveable`
- **data** — repositories, data sources, caching, networking (Ktor), persistence
- **concurrency** — coroutine scoping, dispatchers, structured cancellation, Flow operators
- **errors** — typed errors, `Result`, exception strategy, surfacing to UI
- **resources** — lifecycle of `Cursor` / `InputStream` / `Response` / `ContentProviderClient` / cancellation handles
- **di** — Koin/Hilt module organization, scoping conventions
- **kmp** — `expect` / `actual` boundaries, what lives in `commonMain`, Swift interop
- **testing** — what to test where, fakes vs mocks, virtual time, Turbine, integration vs unit
- **observability** — logging, analytics, crash reporting, telemetry
- **build** — version catalog, convention plugins, KSP/KAPT, lint/detekt

## Pattern entry schema

Every entry inside a category file follows this shape:

```markdown
### <Pattern name>

**Status:** established | emerging | in-transition | deprecated
**First documented:** <YYYY-MM-DD>   **Last verified:** <YYYY-MM-DD> @ <SHA>
**Coverage:** <"consistent across feature ViewModels" | "5 of ~30 screens" | …>

**The pattern.**
2–6 sentences in plain language: what we do and why. Mid-level audience — descriptive, not technical-dense.

**Why this works for us.**
The concrete pros, specific to this codebase. Avoid generic platitudes.

**Known trade-offs / when it strains.**
Honest cons. Where the pattern is awkward, imperfect, or has a known cost.

**How to apply it.**
~10 lines of pseudocode (Kotlin-flavored is fine). Show the shape, not a full implementation.

**Seen in.**
- path/to/Foo.kt
- path/to/Bar.kt

**Deep dive (senior).**  *(optional)*
Anything only worth reading if you're going to extend or rework the pattern.

**When to deviate.**  *(optional)*
Conditions under which this pattern is the wrong choice. Treat as guideline, not iron rule.

**References.**  *(optional)*
- [Android official guide on X](https://...)
- [NIA sample: Y](https://...)

**Related lessons.**  *(optional)*
- L-2026-05-02-07 (StateFlow conflation)
```

Field rules:

- **Seen in** uses **file paths only — never line numbers.** Line numbers rot under refactors; file-path drift is what the verify agent checks.
- **How to apply it** is pseudocode, not real-snippets-from-the-repo. Pseudocode survives repo churn; real snippets go stale.
- **Deep dive** and **When to deviate** are optional. Don't pad them — leave them out if there's nothing real to say.
- **References** is structured (markdown link list). Use it when a pattern aligns with upstream guidance (Android dev docs, NIA samples, official Compose guides) so engineers can see at a glance whether something is upstream-blessed or project-invented.

## Lifecycle states

- `established` — consistent in the relevant scope; the safe default to follow.
- `emerging` — seen in 1–3 places, not yet enforced; documented so engineers can choose to follow but know it's not load-bearing.
- `in-transition` — codebase is mid-migration; old + new coexist on purpose. Name the target shape in the entry.
- `deprecated` — no longer the desired pattern; kept for historical reading.

When a pattern is decommissioned, **move its entry to a `## Decommissioned` section at the bottom of the same category file**. Add a `**Why decommissioned:**` one-liner. Never delete the entry — the audit trail matters.

## Category file structure

Each `docs/patterns/<category>.md` follows this shape:

```markdown
---
**Path scope:** <comma-separated file/dir globs that this category covers>
**Last surveyed:** <SHA> on <YYYY-MM-DD>
---

# <Category title>

<1-paragraph intro: what this category covers, why we care.>

## Patterns

<entries, newest-documented first>

## What we don't do

<anti-patterns the project explicitly avoids; one paragraph each with a `**Why we avoid it:**` line.>

## Decommissioned

<deprecated entries moved here, newest-deprecated first.>
```

The `Path scope` field in the frontmatter declares which file/dir globs belong to this category. The update flow uses it to decide whether a category needs re-verification after a `git diff`.

## Index file structure — `docs/PATTERNS.md`

```markdown
# Patterns and Conventions

A living guide to the coding patterns and architectural conventions in this codebase. Written for mid-level engineers; deep dives are flagged for senior readers. Maintained via the `document-patterns` Claude Code skill.

Statuses: `established` (safe default) · `emerging` (1–3 places, not enforced) · `in-transition` (mid-migration) · `deprecated` (don't apply).

These are **opinionated guidelines, not iron rules**. Each entry may carry a `When to deviate` note. Use judgment.

## Categories

| Category                                              | Summary                                                          | Last surveyed     |
|-------------------------------------------------------|------------------------------------------------------------------|-------------------|
| [architecture](patterns/architecture.md)              | Module layering and the navigation surface.                      | abc1234 · 2026-05-03 |
| [ui-state](patterns/ui-state.md)                      | StateFlow → Compose, source-of-truth flows, screen state shapes. | abc1234 · 2026-05-03 |
| ...                                                                                                                                        |
```

The index aggregates per-category cursors — there is no global cursor file.

## Process

### 1. Detect mode and parse flags

- If `docs/PATTERNS.md` does not exist → **bootstrap** mode.
- If it exists → **update** mode.
- `--scope <category>` restricts the run to one category file.
- `--deep <category>` runs a heavier re-verify pass on that category (full re-explore, not just citation sampling).

### 2. Bootstrap mode — wide first pass

1. Announce the 12-category seed list to the user. Ask which to skip (e.g., "no `:shared` KMP module yet — skip kmp?").
2. For each remaining category, spawn an **Explore sub-agent in parallel** — one Agent call per category, all in a single message. Brief each with: the category's scope, the entry schema, the `Path scope` it should claim in the frontmatter, and instructions to identify 3–8 patterns max plus a `What we don't do` list.
3. Wait for all sub-agents. Collect proposed entries.
4. Present one combined triage plan (see *Triage UX*).
5. On approval, write all category files at once. Write `docs/PATTERNS.md` last as the narrative index.
6. Stamp every file with `Last surveyed: <HEAD-SHA> on <today>`.

### 3. Update mode — incremental

1. Read `docs/PATTERNS.md` and each category file's frontmatter to collect per-category cursors and `Path scope` globs.
2. Run `git diff <oldest-cursor>..HEAD --stat`. For each category, intersect the changed-path set with that category's `Path scope` to decide whether the category needs re-verification.
3. For each category that needs it, spawn **two sub-agents in parallel**:
   - **Verify agent** — checks each existing entry against current code. Returns `still-matches` / `drifted` / `gone` / `dominant-shifted` per entry.
   - **Discovery agent** — looks only for *emergent* patterns not yet documented in that category file.
4. Spawn all agents across all affected categories in parallel (one message, multiple Agent calls).
5. Auto-classify the verify results into proposed triage actions (table below).
6. Present one combined triage plan covering all affected categories.
7. On approval, edit files in place: update entries, append new ones, move decommissioned ones to `## Decommissioned`, bump per-category cursors, update each touched entry's `Last verified`. Update the index table.

### 4. Verify agent brief

Per existing entry in the category, the verify agent must:

1. For each path in `Seen in`: confirm the file still exists and contains code that **semantically** matches the pattern (same shape, same intent — exact line match is not required).
2. Sample 2–3 *adjacent* files in the same category (sibling files in the same module/package) that are **not** in `Seen in`. Check whether they follow the pattern too.
3. Return one of:
   - `still-matches` — pattern intact across cited files; adjacent files conform.
   - `drifted` — some files have diverged; list them. Pattern is no longer uniform.
   - `gone` — the cited code is no longer there.
   - `dominant-shifted` — a different pattern is now more common in this area than the documented one; describe the new dominant shape.

The verify agent must NOT propose new patterns. That's the discovery agent's job. Combining the two briefs produces false positives — keep them separate.

In `--deep` mode, the verify agent also re-explores the full category from scratch (not just sampling) and can re-write any entry's `The pattern` / `Why this works` / `Trade-offs` prose if it has drifted from current reality.

### 5. Discovery agent brief

Per affected category, the discovery agent must:

1. Look for coherent patterns repeated in 3+ places in the category's `Path scope` that are not already documented.
2. Bias toward fewer entries. Patterns seen in 1–2 places may be flagged as candidates with `Status: emerging`, but only if clearly load-bearing.
3. Output proposed entries in the schema. Pseudocode in `How to apply it`. File paths only (no line numbers) in `Seen in`.
4. If a coherent cluster doesn't fit any existing category, propose a new category file with name + scope + first entries.

### 6. Auto-classify on triage

Map verify results to proposed triage actions. The skill auto-classifies — the user reviews and overrides at triage.

| Verify result        | Triage action                                                                                                                |
|----------------------|------------------------------------------------------------------------------------------------------------------------------|
| `still-matches`      | KEEP — bump `Last verified`, no other change.                                                                                |
| `drifted`            | UPDATE — keep `Status: established`, add a one-line "exception" note listing the diverging files (dominant + exceptions style). |
| `gone`               | DECOMMISSION — propose with reason from the verify agent.                                                                    |
| `dominant-shifted`   | FLIP — propose the new dominant as the active pattern; mark the old as `deprecated` and move to `## Decommissioned`.         |

When `drifted` looks intentionally bidirectional (a real migration is happening), prefer `Status: in-transition` over `dominant + exceptions`. The skill makes this call automatically based on the verify agent's description; the user can override during triage.

### 7. Triage UX

Present a single combined plan in chat, one markdown table per affected category:

```
## Triage plan — `ui-state.md`

| # | Action       | Entry                                   | Reason                                       |
|---|--------------|-----------------------------------------|----------------------------------------------|
| 1 | KEEP         | StateFlow as single source of truth     | still-matches; bump Last verified            |
| 2 | UPDATE       | combine() of upstream flows             | drifted: 2 new screens use different shape   |
| 3 | DECOMMISSION | LiveData bridging via asLiveData()      | gone; no callers remaining on dev            |
| 4 | ADD          | RefreshOutcome → combine() error model  | new pattern in 3 ViewModels                  |
```

**Do not inline the proposed entry text in the triage plan** — that explodes the chat. The user reviews row-level intent (KEEP / UPDATE / DECOMMISSION / FLIP / ADD) and reasons. Entry text is written into files only after approval. If the user wants a preview of any specific entry before approving, they'll ask.

User responds with `approve all`, `approve except 2 and 4`, or freeform edits. **Write nothing until the user approves.**

### 8. Persist

On approval:

1. Edit category files in place. Add / update / decommission entries per the approved plan.
2. Bump each touched category's `Last surveyed: <HEAD-SHA> on <today>`.
3. Update each touched entry's `Last verified` field.
4. Update `docs/PATTERNS.md` index table to reflect new cursors and any added/decommissioned entries in the category one-liners.
5. **Do not `git add` or `git commit`.** Stop after writing.

## Tone & writing guide

- **Mid-level engineer audience.** Plain language. Concrete pros and cons. Explain *why*, not just *what*.
- **Opinionated guideline, not iron rule.** Hedge honestly when a pattern has known weak spots. The `When to deviate` field exists precisely so engineers don't feel boxed in.
- **Senior content goes in `Deep dive`.** Don't smuggle dense technical detail into the main `The pattern` body — split it out so the mid-level reader can skim past.
- **No emojis.** No filler. No "this codebase strives to..." language.
- **Pseudocode only in `How to apply it`.** Never paste real snippets from the repo into entries — they go stale. Real-code anchoring lives in `Seen in`.

## What's out of scope

- **Lessons content.** A pattern entry may cite an `L-` ID under `Related lessons`. It must never inline lesson prose or replicate a lesson's structure.
- **Non-code conventions.** PR templates, commit messages, CI shape, branch naming → `CONTRIBUTING.md` / `AGENTS.md`, not here.
- **Agent-internal docs.** This skill never modifies `.claude/CLAUDE.md`, `.claude/lessons.md`, `AGENTS.md`, or any file outside `docs/PATTERNS.md` and `docs/patterns/`.
- **Auto-commit.** The skill writes files and stops. The user decides when to commit.

## Anti-patterns — for the skill itself

- **Don't write before approval.** Triage is mandatory. The user always sees the plan first.
- **Don't generate stub files for empty categories.** If a category has no observable patterns, skip the file entirely.
- **Don't include line numbers in `Seen in`.** Code moves; line numbers rot. File paths only.
- **Don't combine verify and discovery briefs.** Separate sub-agents. Combining them yields false positives where verify agents over-propose new patterns to look productive.
- **Don't auto-commit.** Stop after writing the files.
- **Don't touch `.claude/`, `CLAUDE.md`, or `AGENTS.md`.** Scope is `docs/PATTERNS.md` + `docs/patterns/*.md` only.
- **Don't absorb lessons.** A pattern may cite an `L-` ID; never inline lesson content here.
- **Don't be terse-technical in entry bodies.** Mid-level audience: descriptive, plain language, concrete pros/cons. Senior depth goes in `Deep dive`, not the main body.
- **Don't pad with optional fields.** `Deep dive`, `When to deviate`, `References`, `Related lessons` are all optional. If there's nothing real to say, leave them out — empty fields signal the doc is performative.
- **Don't propose new categories silently.** If the discovery agent finds a cluster that doesn't fit, surface it in triage as a candidate new category with a name and proposed scope. The user approves before any new category file is created.
