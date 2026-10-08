---
name: affine-review-code-design
description: Review a branch's diff for adherence to architectural patterns, conventions, and design consistency — consistency with existing codebase patterns, abstraction level and separation of concerns, naming and file/module organization, unnecessary complexity or duplication, and alignment with team conventions. Use on "does this follow our patterns", "review the design/architecture of this PR", "is this idiomatic", or "check this against our conventions". Answers "is it written the right way" — not "does it work" (that is affine-review-code-quality).
argument-hint: [base-ref]
---

# Review Code Design

## Purpose

Catch structural and convention defects in a change: code that works but is built the
wrong way for this codebase. Output is a set of design findings (pattern deviations,
structural concerns, suggested refactor directions) with severity, distinct from and not
blocking on quality findings.

## Inputs

- The current branch's diff against the default branch, or against `[base-ref]` if given.
- The surrounding codebase — design review is comparative; the neighbors of every changed
  file define "idiomatic here".
- `~/.affine/code-patterns/` — read `CATALOG.md` and pull the entries relevant to this
  diff. Project override: if the repo contains `.affine/<same-path>`, use it instead of
  `~/.affine/<same-path>` (applies to every `~/.affine` reference in this skill). If the
  collection is missing, review against the codebase's own observable conventions and say
  so in the report.
- `plans/<TICKET-ID>/SPEC.md` when present — deviations from the agreed design are
  findings even when the alternative is defensible in isolation.
- `~/.affine/severity-scale.md` for P0–P5 definitions (fallback: P0 blocker → P5 nit).

## Procedure

1. Establish scope: `git diff <base>...HEAD`, changed files in full, plus sibling
   files/modules that establish the local pattern (how do existing services, handlers,
   tests in this area look?).
2. Consistency: does the change follow the patterns the codebase already uses for this
   kind of thing (error handling shape, layering, DI, module boundaries), or invent a
   parallel one?
3. Abstraction: right level for the job — neither premature generalization nor copy-paste
   where an existing abstraction fits. Separation of concerns across the changed units.
4. Organization: naming (files, modules, symbols) and placement match conventions;
   changes live where a maintainer would look for them.
5. Complexity and duplication: unnecessary indirection, dead flexibility, duplicated
   logic that an existing utility already covers.
6. Cross-artifact consistency: when the diff changes a public API, config schema, data
   model, or operational behavior, check the artifacts that describe it (docs/, README,
   runbooks, the plan's Documentation impact line) — were they updated, and do they
   match what the code now does? A changed behavior with a stale describing artifact is
   a finding. Report `not-applicable` when the diff implicates no such artifact.
7. Convention alignment: check the diff against each applicable `~/.affine/code-patterns/`
   entry (e.g. comment discipline per `minimal-comments.md`).
8. Assign each finding a P0–P5 severity with a one-line consequence. A design finding is
   P2 or higher only if it introduces a correctness/safety risk or materially damages
   maintainability; most design findings are P3–P5.
9. Write the report (Output below) and reply with a ≤5-line summary.

## Output

`plans/<TICKET-ID>/reviews/code-design.md` (derive `<TICKET-ID>` from plans/ or the branch
name; if no ticket context exists, report inline instead and say so):

```markdown
---
skill: affine-review-code-design
base: <base-ref>
verdict: pass | fail
reviewed: <ISO timestamp>
---
## Findings
- **P3** `src/user/service.ts:88` — <pattern deviation / structural claim>. Consequence: <one line>. Suggested direction: <one line, not a patch>.
## Patterns consulted
<catalog entries and codebase exemplars used as the baseline>
```

The verdict fails only on P0–P2 findings.

## Boundaries

- Does not evaluate correctness, security, test adequacy, or whether the implementation
  satisfies the ticket's requirements — that is affine-review-code-quality. If a change
  needs both, run both skills.
- Does not review org-specific policy — that is affine-review-org-concerns.
- Read + execute only: may run linters/builds; writes only its report file; never edits
  application code; never runs git commands that write.
