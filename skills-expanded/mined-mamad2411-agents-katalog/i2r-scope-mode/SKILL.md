---
name: i2r-scope-mode
description: Scope firewall for i2r-scope-architect; draws in_scope/out_of_scope/deferred, seeds MoSCoW, and blocks anti-scope-creep from entering 03-scope.json.
when_to_use: Always — i2r-scope-architect loads this skill before writing 03-scope.json; it is the only agent that may write that file.
user-invocable: false
---

# i2r-scope-mode

## Role in the pipeline

`i2r-scope-architect` uses this skill as the rulebook for producing `03-scope.json`
(schema: `schemas/03-scope.schema.json`). Scope is the single most consequential
artifact in the pipeline: a wrong boundary poisons every downstream FR, NFR, and
acceptance criterion. This skill is the firewall.

## Output contract

File: `.i2r/runs/<slug>/<run-id>/internal/stages/03-scope.json`
Owner agent: `i2r-scope-architect`
Must include `_meta.skills_used: ["i2r-scope-mode"]`.

Required top-level fields (per schema):
- `in_scope[]` — capabilities confirmed in boundary, each with `capability`, `moscow`, `source_ref`
- `out_of_scope[]` — explicitly excluded items with `reason`
- `deferred[]` — out-of-scope for now but not forever, with `reason` and a `revisit_trigger` (when to reconsider)
- `capability_inventory[]` — flat slug list of every in-scope capability
- `scope_risks[]` — risks of misinterpretation (optional but recommended)
- `scope_confirmed: true` — the architect's explicit sign-off

## Boundary-drawing procedure

### Step 1 — Capability harvest

Read `01-intake.json` (`stated[]`, `decisions[]`) and `02-context.json`
(`jobs_to_be_done[]`, `actors[]`). For every capability mentioned or implied,
classify it as candidate `in_scope`, `out_of_scope`, or `deferred`.

### Step 2 — Boundary test (the stack-swap check)

For every candidate `in_scope` entry, apply the boundary test from
`references/scope-boundary-rules.md`:

> If swapping the database or framework forces a rewrite of this capability
> statement → it leaked HOW → rewrite it at WHAT level or move it out.

Any capability that describes an API endpoint shape, a database table, a
specific library, or an architectural pattern is a HOW leak → out or rewrite.

### Step 3 — MoSCoW seeding

Apply seeding rules from `references/moscow-rules.md`. Every `in_scope` entry
must carry a `moscow` value. The seed is a starting point; downstream agents
(`i2r-functional-author`, `i2r-nfr-author`) may refine but not contradict.

### Step 4 — Source traceability

Every `in_scope` entry must carry `source_ref` pointing into `raw/` or a
clarification file. Capabilities with no traceable source → raise as
`requires_discussion: blocking` in `01-intake.json` first; do not add to scope.

### Step 5 — Anti-creep scan (the Requirements Minimalism Ladder)

Apply the RML ladder (root skill `requirements-minimalism.md`) to every candidate capability. Before keeping
one, stop at the first rung that holds:

1. **Needs to exist at all?** Features mentioned once in passing, "nice to have" phrasing, or capabilities
   that solve a problem the user did not state → `deferred` or `out_of_scope` with a reason. (Gold-plating.)
2. **Already covered by another capability?** Two capabilities that are one behaviour → merge.
3. **Already guaranteed by a platform / standard / regulation the project is bound to?** A capability whose
   only content restates a platform/standard given (TLS, JSON responses, password hashing the stack mandates)
   → state it once in `out/CONSTRAINTS.md` as a constraint, do not carry it as a delivered capability.
4. **Already implied by a locked decision or existing constraint?** Do not restate the consequence as a fresh
   capability.

Move every cut to `deferred` or `out_of_scope` with a clear reason.

**The safety floor never moves.** Never defer or drop a capability covering security, data-loss prevention,
accessibility, a trust boundary, regulatory obligation, or anything the user explicitly asked to keep —
those are MoSCoW `MUST`. RML shrinks the count, never the floor (see `requirements-minimalism.md` §safety floor).

**Every `deferred[]` item carries a `revisit_trigger`** — the concrete condition under which it should
re-enter scope (see schema `03-scope.schema.json`). A deferral with no trigger silently rots; the gate flags
it (`deferral_has_trigger`, MAJOR — never blocks, only surfaces).

### Step 6 — Scope risks

For every capability likely to be misread downstream (by FR authors, GSD planners,
or implementers), add a `scope_risks` entry with a mitigation note.

## Debate trigger

If `03b-scope-debate.json` is required by the L0 router
(`debate_mode != "not_required"`), the scope-architect still writes `03-scope.json`
first, then the debate layer (`i2r-debate-review-mode`) produces `03b-scope-debate.json`
and may request scope amendments via `changes_requested[]`. The architect
then rewrites `03-scope.json` incorporating the resolution.

## Hard rules

- One writer: only `i2r-scope-architect` writes `03-scope.json`.
- `scope_confirmed` must be `true` before downstream agents run.
- Never output phases, timelines, team assignments, or architecture.
- `WONT` in `moscow` means excluded from this product entirely — use `deferred`
  for "not in this release".

## References

- `references/scope-boundary-rules.md` — boundary test, capability inventory rules, anti-creep
- `references/moscow-rules.md` — MUST/SHOULD/COULD/WONT definitions and seeding rules
- root skill `requirements-minimalism.md` — the RML ladder, safety floor, and deferral-with-trigger convention

Vendored sources: Spec Kit specify/clarify discipline; BMAD product brief scope taxonomy; ponytail laziness ladder (→ RML, see requirements-minimalism.md).
