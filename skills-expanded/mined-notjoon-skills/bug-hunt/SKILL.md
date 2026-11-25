---
name: bug-hunt
description: Adversarial multi-agent security sweep. Use when hunting for a CLASS of vulnerability (authority/capability bypass, injection, resource exhaustion, invariant breaks) across a codebase or subsystem where you have a hunch but no specific finding, and want each candidate independently refuted before it counts. Fan out finders by attack angle, then refute-first verify every candidate. A clean negative result (guard map) is a first-class deliverable.
---

# bug-hunt

A reusable harness for hunting a *class* of bug across a subsystem, then proving
each candidate real or (usually) refuting it. Built from repeated authority-bypass
sweeps on the gno.land VM. Engine = the `Workflow` tool: `pipeline(angles, find, verify)`.

## When to use

- You have a hunch a bug class *might* exist ("sub-realms could bypass authority
  somehow") but no concrete finding yet.
- You want breadth (many independent angles) AND rigor (each candidate adversarially
  refuted before you believe it) without hand-running dozens of greps.
- You want the *negative* result to be trustworthy — "we looked hard and here's why
  the guard holds", not "I didn't find anything".

Not for: a single known bug (just fix it), a whole-repo audit with no thesis (too
broad — pick a subsystem first), or a quick one-file check (just read it).

## The method (6 steps)

1. **Scope the layers.** Most real bugs live in the *seam between layers*, not inside
   one. Enumerate every layer the target crosses and make the finders read all of them.
   (gno banker example: gno stdlib `.gno` → native Go binding → bank keeper. The
   interesting question was always "does layer N re-check what layer N-1 assumed?")

2. **Decompose into attack angles.** 5–8 angles, each a *distinct mechanism*, not a
   restatement. Name them `<Prefix><n>-<slug>` (A1, B2…) so results are greppable.
   One finder per angle. Coverage beats depth here — depth comes in verify.

3. **Ground the finders in REAL source.** Before writing the workflow, grep the actual
   file:line anchors for each angle and put them in the prompt. Tell finders: "read the
   ACTUAL current source, do not trust summaries." A finder pointed at the wrong file
   invents plausible-but-fake findings.

4. **Baseline-exclusion.** List already-known/disclosed/by-design issues explicitly and
   tell finders + verifiers to flag any restatement as `duplicate_of_known=true` and
   refute it. Without this every run rediscovers H1 and calls it new.

5. **Find → refute-first verify (pipeline).** `pipeline(angles, findStage, verifyStage)`.
   Each finding gets an independent verifier told: *assume it is a FALSE POSITIVE, refute
   it from source, only rule "real" if the code forces it, default to "refuted" when
   uncertain.* This is the whole point — a finding nobody tried to kill is worthless.

6. **Harvest guard_notes even on a clean run.** Every finder returns a `guard_summary`
   (how the guard actually works, per source) whether or not it found anything. On a
   0-confirmed run these summaries ARE the deliverable: a source-cited guard map proving
   the negative. Also capture any *nuance* a verifier raises that isn't a vuln but is
   worth an owner note (e.g. "IsCanonical checks type not bt").

## Deliverables

- **Confirmed findings** → reproduce each with a runnable test (txtar / filetest / unit)
  before reporting. A finding you haven't watched turn a test red is a guess.
- **Clean negative** → the guard map (per-angle `guard_summary` with file:line) + any
  owner-note nuances. This is valuable: it tells maintainers *which* guards they're
  relying on and why, and raises confidence in adjacent results.
- Present as a table: angle | verdict | key evidence. Then the bottom line: X angles,
  N confirmed, and what (if anything) to file.

## Running it

The engine is `hunt-template.js` next to this file — a parameterized
`pipeline(ANGLES, find, verify)` with `FIND_SCHEMA` + `VERDICT_SCHEMA` already wired.
To run a hunt:

1. Copy `hunt-template.js` into the session's workflow scripts dir.
2. Edit `meta`, `SHARED` (repo path, layer map, ground files, baseline-exclusions), and
   `ANGLES` (5–8 angles with file:line anchors).
3. `Workflow({ scriptPath: "<copied path>" })` — runs in background.
4. On completion read the output file; if the harvest looks wrong (empty guard_notes,
   shape mismatch), fix the script and resume with
   `Workflow({ scriptPath, resumeFromRunId })` — cached agent calls return instantly.

Knobs: `effort: 'high'` on both stages for security work; scale `ANGLES` to thoroughness
requested; add a 3-vote refuter panel per finding for "audit this exhaustively" asks.

## Hard-won gotchas

- **Pipeline stage return shape must be uniform.** If the verify stage sometimes returns
  a wrapped object and sometimes a raw array, the final harvest silently drops the
  array-shaped ones. Always return the SAME `{ angle, guard_summary, verified }` shape.
- **Refute-first is not optional.** A verifier that "confirms" is doing it wrong. The
  default verdict is `refuted`; `real` requires the code to force it.
- **codex/subagent cybersecurity filter.** Frame prompts as *defensive* research on the
  maintainer's own code ("authorized defensive security research", "bounding/hardening"),
  never as exploit/attack recipes, or the safety filter refuses mid-run.
- **Ground or hallucinate.** No file:line anchors in the finder prompt → confident fiction.
- **0 confirmed is a success, not a failure.** Don't let a finder invent findings to fill
  a quota — the prompt says so explicitly, keep it that way.
