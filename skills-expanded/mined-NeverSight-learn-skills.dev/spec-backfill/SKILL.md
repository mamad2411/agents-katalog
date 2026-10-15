---
name: spec-backfill
description: Backfill missing specifications, reconcile spec/code drift, maintain changelog.
---

# Objective

Reconstruct specifications from a repository's codebase, existing documentation, and git history.
You're doing archaeology — finding the *features* buried in code and docs, then surfacing them as structured specs.

A spec is warranted when code implements user-facing functionality or business logic. Not every module needs a spec.
Your job is to find the functional boundaries and document them.

Maintain state in files so work isn't lost if the conversation ends.

# Entry Point

1. Check for existing session state (`specs/spec-backfill-state.yaml`) — if present, offer to resume from cursor position (see `references/session-state-schema.md`)
2. Check for existing mapping (`specs/spec-mapping.yaml`) — determines phase:
   - No mapping → First Run
   - Mapping exists → Incremental
   - User specifies files → Targeted

# Phases

Three modes of operation. The agent runs the phase that matches the situation.

| Phase | When | Steps |
|-------|------|-------|
| **First run** | No `spec-mapping.yaml` exists | Classify → Map → Gaps → Generate → Verify |
| **Incremental** | Mapping exists, detect drift | Detect stale → Reconcile → Generate if needed |
| **Targeted** | User picks specific files/modules | Classify targets → Map → Generate → Verify |

## Phase: First Run

```
1. CLASSIFY CODE
   - Scan codebase, classify each path:
     functional (needs spec) | architectural (needs ADR) | utility (needs neither)
   - Judgment call: "If a PM asked 'what does this do for users?',
     would there be a meaningful answer?" If yes → functional.
   - Show classification to user for validation

2. MAP CODE TO SPECS
   - For each functional path: does a spec exist? Check alignment.
   - No spec → gap. Spec conflicts with code → conflict.
   - Conflict types: code-ahead | spec-ahead | semantic-mismatch | stale-spec
   - Output: coverage report per references/report-format.md

3. ASK — surface unknowns, prioritize gaps
   - "I found N code paths without specs. Which are highest priority?"
   - Never generate without confirmation.

4. GENERATE SPECS (per gap, one at a time)
   - Extract observable behavior from code
   - Identify inputs, outputs, side effects, business rules
   - Ask user for: purpose, user story, acceptance criteria
   - Generate spec only after confirmation
   - Templates: references/spec-templates.md

5. VERIFY
   - All functional code has spec mapping
   - No relevant legacy content dropped (diff old vs new, surface differences)
   - No internal contradictions
   - Cross-references valid (ADRs, code paths)
   - Archive superseded specs to _archive after confirmation

6. PERSIST
   - Update spec-mapping.yaml (including SHAs) per references/mapping-schema.md
   - Update changelog
   - Output report per references/report-format.md
```

## Phase: Incremental

```
1. DETECT STALENESS — compare stored SHAs against current HEAD
   - code_sha stale, spec_sha current → code-ahead-of-spec
   - code_sha current, spec_sha stale → spec edited (intentional or drift?)
   - Both stale → full reconciliation needed
   - New code files → candidates for classification
   - Deleted code files → flag for mapping cleanup
   - Nothing stale/new → report "all current" and stop

2. SURFACE stale mappings and new files to user

3. RECONCILE each stale mapping
   - Re-read code and spec, assess alignment
   - Update status: aligned | gap | conflict

4. GENERATE / UPDATE if needed (same as First Run step 4)

5. PERSIST (same as First Run step 6)
```

## Phase: Targeted

```
1. User specifies files or modules
2. CLASSIFY targets (if not already in mapping)
3. MAP → GENERATE → VERIFY → PERSIST (same as First Run steps 2–6, scoped to targets)
```

# Spec Hierarchies

## Build (source of truth, time-oriented)

```
specs/build/
  0.md           # Vision — why the product exists
  1.1.md         # Epic — large user-facing goal
  1.1.1.md       # User Story — specific user need
```

Build captures *intent* — what we set out to do and when.

## Functional (derived view, navigation-oriented)

```
specs/functional/
  0.md           # Product description — what it is today
  1.1.md         # Domain — bounded context
  1.1.1.md       # Feature — specific capability
```

Functional captures *current state* — what exists now and how it's organized.

## Relationship

- Build **generates** Functional: epics/stories become domains/features when implemented
- Functional gaps **trigger** build investigation: missing feature → check epic history
- During backfill: **populate build first**, derive functional from it

## Derivation trigger

An epic becomes a domain when all its stories are implemented (code mapped). Ask user to confirm before creating a functional entry from build.

## Numbering convention

Hierarchical: `1.1.md` = first child of root, `1.1.1.md` = first child of 1.1, `1.2.md` = sibling of 1.1.

# Gates (when to stop and ask)

**Code classification ambiguity**
> "I'm unsure whether `src/lib/pricing_engine.py` is functional or utility.
> It computes discounts based on customer tier. How do you see it?"

**Spec mapping unclear**
> "Code in `src/orders/fulfillment.py` handles shipping, returns, and tracking. One feature or three?"

**Business intent unknown**
> "This module processes webhook events from Stripe. I can see *what* it does but not *why*."

**Conflict resolution**
> "Spec says max 5 projects. Code enforces max 10. Which is correct?"

**Gap prioritization**
> "I found 12 code paths without specs. Which are highest priority?"

Always ask before generating a spec.

## Confidence levels

- **inferred-pending-review**: Agent derived from code analysis
- **confirmed**: User explicitly validated at a gate

Transition: `inferred` → `confirmed` only after explicit user approval.

# Quality Bar

A good backfilled spec:
- Could have been written before the code was built
- Describes *what* and *for whom*, not implementation details
- Stands alone (reader doesn't need to read the code)
- Is honest about what's confirmed vs. inferred
- Links to relevant ADRs for *why* decisions were made

A bad backfilled spec:
- Just describes the code structure
- Invents requirements the user didn't confirm
- Mixes multiple features in one document
- Contains implementation details instead of behavior

# Anti-patterns

- **Inventing requirements**: If you don't know the business need, ask.
- **Generating without code validation**: Every spec claim must be verifiable against code.
- **Guessing business intent**: Code shows *what*, not *why for users*. Ask.
- **Dropping legacy content silently**: Always surface what's being removed.
- **Over-specifying implementation**: Specs describe behavior, not code structure.
- **Ignoring conflicts**: Surface mismatches explicitly.

# Integration

- **black-box-red-testing**: Generated specs become test oracles. After backfilling, consider invoking black-box to verify code matches the documented behavior.
- **code-spec-backfill**: This skill handles feature-level specs. code-spec-backfill handles function-level contracts (docstrings, type annotations). They complement, not overlap.
- **adr-backfill**: Architectural code paths flagged during classification are candidates for ADR backfill, not spec backfill.

# Tooling

## YAML state management

Prefer `scripts/` over raw file editing for mapping updates — LLM YAML editing is fragile.

| Script | Purpose |
|--------|---------|
| `scripts/detect-stale.sh [mapping-file]` | Compare stored SHAs against HEAD. Outputs one line per entry: `CURRENT`, `CODE_AHEAD`, `SPEC_EDITED`, `BOTH_STALE`, `DELETED`, `NEW` |
| `scripts/update-mapping.sh <mapping-file> <code-path> [options]` | Update a single mapping entry. Supports `--status`, `--code-sha auto`, `--spec-sha auto`, `--spec-path`, `--classify`, `--remove` |

Both require `yq` (mikefarah/yq). Run `detect-stale.sh` first in Incremental phase, then `update-mapping.sh` per entry after reconciliation.

## Subagent delegation

First-run classification on large codebases (>50 files): delegate scanning to a subagent (via your preferred subagent mechanism — e.g. generic-subagent skill, Task tool, or equivalent). The main agent retains classification decisions but the subagent does the file-by-file reading and initial categorization.

Delegation triggers:
- Input size >250KB (many files to scan)
- >2 intermediate tool calls whose outputs aren't needed in final delivery

# References

Consult on demand, not upfront:

| Reference | When needed |
|-----------|-------------|
| `references/mapping-schema.md` | Persisting or reading mapping state |
| `references/session-state-schema.md` | Resuming across conversation boundaries |
| `references/spec-templates.md` | Generating specs (step 4) |
| `references/report-format.md` | Producing output reports |
