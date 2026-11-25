---
name: retroactive-spec-update
description: >
  Sync an EXISTING spec to the as-is code (code = evidence, git = scope) —
  only "what does the code already do that the spec omits", never "what
  could be added". Use when a spec has drifted from the code and must catch
  up; reach for it instead of hand-patching the spec. NOT for authoring a
  new spec (use spec_authoring) or amending a locked spec by intent (use
  spec-amendment-discipline).
status: active
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: [spec_amendment_verification, spec_board]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: retroactive-spec-update

## Guiding principle (keep in mind before every run)

**The spec defines the product. Incidents are fixed in the spec,
not in the code.**

This skill exists because in practice it often runs the other way
round: code evolves, specs lag behind. That is technical debt
which this skill pays off. Every run is a **reversal** of that
order — the spec reclaims what is hers by describing the code
that already exists.

**What this skill does NOT do:** invent new features, suggest
features, ask "what else could be there". The skill operates
strictly retroactively — the source of truth is the existing
source code, not the reviewer's imagination.

**Guiding question per section:** *"What does the code do that
the spec does not fully describe?"* — NOT *"What is missing from
the product?"*. Write the answer at contract level; cases a test
already pins stay in the test (`framework/spec-engineering.md`
§Convention: spec carriers).

---

## When to call

- Pre-launch sweep: bring the spec corpus to as-is code state
  before public release.
- Post-incident: the bug fix changed behaviour; the spec must
  reflect it.
- Feature drift: a feature shipped without a spec update
  (technical debt).
- Periodic catch-up: N weeks / months without a spec sync; code
  is ahead.

## Do not call for

- **Writing new specs** → `spec_authoring` (interview-based).
- **New sections for new features in existing specs** →
  `spec_authoring` (because an interview is needed to clarify
  user intent, even on section additions).
- **Read-only cross-spec verification** →
  `spec_amendment_verification` (post-amendment).
- **Spec-quality review** → `spec_board` (rebuild-readiness
  check).

---

## Input

Buddy identifies and passes:

- **`target_specs`:** list of spec files that potentially have
  drift.
- **Optional `last_sync_ref`:** git ref of the last confirmed
  spec-sync commit. When present, it forms the scope entry.
  Otherwise: Buddy searches the git log for the last "sync all
  specs" or similar commit, or falls back to "all commits in N
  weeks".
- **Optional `scope_hints`:** additional source-file patterns
  that are relevant (when the spec doesn't reference code
  explicitly).

---

## Default dispatch path (per spec 306 §14.5)

Phase 1 (git scope) and Phases 3-5 (DIM check, cross-spec verify,
commit-bookkeeping) are Buddy-direct. **Phase 2 (spec walkthrough)
is dispatched to `brief-architect` in `mode=retro_spec_update`** —
the architect reads each relevant source file completely in fresh
context, classifies findings (MATCH / SPEC-GAP / SPEC-DRIFT /
CODE-BUG), and returns proposed prose + DIM-map per section
**inline**. Buddy integrates the architect's findings into the spec
file (architect has no Write target per spec 306 §14.4), bumps
`spec_version`, and continues to Phase 4.

The architect dispatch is the default. The skip path
(`--skip retroactive-spec-update --reason "buddy-context-already-loaded"`)
exists for the rare case where Buddy just finished writing the code
in scope and the read-cost has already been paid; in that case
Buddy executes Phase 2 inline. The default-architect choice
preserves fresh-context discipline on the typical retro run, which
is code-read-heavy by construction.

CODE-BUG escalations from the architect's findings list trigger the
phase 4b ledger flow (Buddy-direct, user-decision-required). The
architect identifies CODE-BUG candidates per the four-classification
model; Buddy owns the user-decision loop.

---

## Phase 1 — GIT SCOPE (structural, the entry door)

**Goal:** identify the relevant source files. Commits are hints,
not ground truth.

Steps:

1. **Find the last sync point:**
   - Read the spec header for `Board-Reviews` / `Last Update` /
     `spec_version`.
   - Or git log grep:
     `git log --grep="sync all specs\|spec sync" --oneline -5`.
   - Or passed in by the user.

2. **List commits since the last sync:**
   ```
   git log <last_sync>..HEAD --oneline
   ```
   Filter roughly for behaviour-relevant commits (feat, fix,
   refactor with behaviour impact). Infra / docs / release
   commits are irrelevant.

3. **Aggregate relevant source files** from two sources:
   - **From git log:** which files were changed in the relevant
     commits?
     `git log <last_sync>..HEAD --name-only --format=""`.
   - **From spec self-declaration:** grep the spec for
     file-path patterns, component names, class names. The
     spec often mentions `CallProvider`, `VideoGrid`,
     `AudioVideoSettings`, etc. — those are the entry points.

4. **Cross-reference:** files that appear in both lists are
   high-confidence. Files that appear in only one list are
   coverage warnings (either code was changed but the spec
   ignores the area, or the spec describes something that has
   no current code).

**Phase 1 output** (working doc
`docs/spec/_update-notes/{spec}-scope.md` or inline in Buddy's
context):

```markdown
# {spec_file} — Retroactive Update Scope

**Last sync:** <commit hash + date>
**Commits since:** <count>

**Source files in scope:**
- src/path/to/fileA.ts
- src/path/to/fileB.tsx
- ...

**Commits as hints (not as the diff basis):**
- <hash> <subject>
- ...

**Spec-declared references:**
- Consumed: <list from header>
- Components mentioned: <from grep>
```

**Phase 1 is scope, not content.** No spec edits in phase 1.

---

## Phase 2 — SPEC WALKTHROUGH (code-driven, architect-dispatched)

When dispatching Phase 2 to `brief-architect` (`mode=retro_spec_update`), and before walking the spec inline on the
skip path: read and follow `skills/retroactive_spec_update/walkthrough.md` (the dispatch and per-section walkthrough
2a–2e: section scope, complete code reading, code description, the four findings MATCH / SPEC-GAP / SPEC-DRIFT /
CODE-BUG, the update along the 5 primitives; Phase 2b leftover check of unassigned source files).

---

## Phase 3 — DIM map per section (self-check)

Once the Phase 2 / 2b findings are integrated into the spec, before the DIM self-check, and whenever Phase 2 produced
a CODE-BUG finding: read and follow `skills/retroactive_spec_update/verify-and-commit.md` (Phase 3 DIM map per
changed section; Phase 4 cross-spec verify via `spec_amendment_verification`; Phase 4b Code Gap Ledger, NORMATIVE;
Phase 5 commit; the post-pass checklist, NON-NEGOTIABLE).

---

## Contract

### INPUT

- **Required:** `target_specs` — list of affected spec files.
- **Required:** access to the project's source code.
- **Required:** git log accessible (for phase 1).
- **Required:** `framework/spec-engineering.md` (5 primitives).
- **Optional:** `last_sync_ref`, or the skill finds it itself.
- **Optional:** `scope_hints` for additional source patterns.

### OUTPUT

**DELIVERS:**
- Updated spec files (with `spec_version` bumps).
- Scope working doc (can be committed or gitignored —
  project-specific).
- DIM map per changed section.
- `spec_amendment_verification` result.
- Commits with conventional messages.
- `context/history.md` entry.

**DOES NOT DELIVER:**
- No new features, no feature suggestions.
- No interview — the code is evidence; the user is not in the
  loop except on a CODE-BUG escalation.
- No board review — that is `spec_board`; can be requested
  afterwards.

**ENABLES:**
- Pre-launch sweep: as-is sync of every relevant spec.
- Post-incident update: the spec matches the new
  behaviour-fix.
- `spec_board` input: updated specs are review-ready.

### DONE

- All sections of `target_specs` were compared with the source
  code.
- The 5 primitives were applied per update.
- The 5 dimensions were self-checked via the DIM map (no
  `Missing`).
- `spec_amendment_verification` PASS or escalated issues.
- `spec_version` bumps, commits, history entry.

### FAIL

- **Retry:** cross-spec verify `ISSUES_FOUND` → fix →
  re-verify.
- **Escalate:**
  - CODE-BUG found, user decision needed.
  - Phase 2b unassigned source file, classification unclear.
  - Spec and code contradict each other and intent is unclear.
- **Abort:** not foreseen.

---

## Boundary

- **No interview authoring** → `spec_authoring` (for NEW specs
  or new sections that need an interview).
- **No read-only verify** → `spec_amendment_verification`.
- **No quality review** → `spec_board` (rebuild-readiness).
- **No code review** → `code_review_board`.

---

## Anti-patterns

- **NOT** treat git diffs as a substitute for code reading.
  INSTEAD: read the whole function / component. Because: diffs
  show delta, not context. The context contains the edge cases
  the spec has to describe.

- **NOT** ask "what's missing as a feature?". INSTEAD: "what
  does the code do that the spec doesn't describe?". Because:
  the first one is design review and leads to feature creep;
  the second is fidelity review and leads to accurate specs.

- **NOT** silently document bugs as intended behaviour. INSTEAD
  on suspicious code passages, escalate as CODE-BUG. Because:
  the guiding principle demands that the spec documents intent,
  not implementation accidents.

- **NOT** skip phase 2b (leftover check). INSTEAD actively
  triage unassigned source files. Because: "there's still
  something in the code" is often the real find of a
  retroactive run — a whole functionality the spec never
  mentioned.

- **NOT** walk multiple specs in parallel. INSTEAD one after
  the other, with a full walkthrough. Because: context
  switching between specs leads to shallow walkthroughs — the
  deep comparison needs dedicated focus.

- **NOT** treat the scope doc as a committed artifact. INSTEAD
  working doc (gitignored or ephemeral). Because: the scope
  doc is a process note, not spec output. Specs are the only
  committable artifact of the skill.

---

## Relation to other skills

```
spec_authoring             (NEW specs or new sections, interview-based)
     ↓
retroactive_spec_update    ← YOU ARE HERE (existing specs, code-as-evidence catch-up)
     ↓
spec_amendment_verification (phase 4, cross-spec consistency)
     ↓
spec_board                 (rebuild-readiness quality review)
```

The `retroactive_spec_update` skill is explicitly **retroactive**
— it compensates technical debt between code and spec. The name
says what it is and rules out the feature-creep route.
