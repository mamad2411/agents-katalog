---
name: review
description: "Use when finishing a task or task slice, before a merge or PR, or after a major change — and when reviewing a spec, plan, or structure/boundary decision as its own object. Routes each review object to a dedicated rubric reference."
---

# Review

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

Pressure-check the work product against what was agreed — before the next task or before **commit-and-push**. The reviewable object is not always a code diff: a **spec** (`write-spec`), a **plan** (`write-plan`), or a **structure decision** (`solid`) each gets its own review with its own falsification method.

**Core principle: review the artifact, not your remembered intentions.**

**Announce:** "Using review to review a <spec|plan|solid|code> …"

## When to Use

- After each plan task (when executing a **write-plan**)
- After a major feature slice
- Before opening/updating a PR/MR
- When a spec / plan / structure decision is finished and you want it pressure-checked before downstream work locks onto it
- When stuck (fresh pass over assumptions)

**When NOT to use:** empty diff; user waived review explicitly.

## The Iron Law

```
1. Critical and Important findings BLOCK progress until fixed or explicitly deferred by the human with reason. The **transition gate** at each skill's Hand-off is where that deferral happens — review surfaces findings, the human decides proceed / fix / adjust at the gate.
2. EVERY review carries a claim→case table — the design-level analog of a test suite. No claim→case table, no LGTM.
3. EVERY review checks the artifact against its DIRECT upstream (child must faithfully narrow the parent).
4. NEVER claim "LGTM" without reading the actual artifact (diff, tests, spec text, plan tasks, boundary decisions).
5. Findings are written in the user's conversational language, plain words, no metaphor-for-decoration; each finding says the scene, what someone hits, and where in the artifact.
```

## Dispatch

Identify the review object, open its reference, and run only that rubric.

| Review object | When | Reference | claim→case table built from |
|---------------|------|-----------|--------------------|
| **code** | A diff / implementation slice | `references/code.md` | claims in the diff (behavior + test expectations) |
| **spec** | A design/spec doc (`write-spec` output) | `references/spec.md` | claims in the spec (scenarios, In/Out, mechanisms, acceptance) |
| **plan** | An implementation plan (`write-plan` output) | `references/plan.md` | claims in the plan (per-task testability, traceability) |
| **solid** | A structure/boundary decision | `references/solid.md` | structural claims (unit purpose, dependency arrows, no theater) |

Mixed object (e.g. a PR that ships a spec + its first implementation)? Run the reference for each object, one claim→case table per object, one report.

## Workflow

1. **Gather context** (not session vibes):
   - Identify the object type → open the matching reference
   - The artifact itself + its **direct upstream** (spec when reviewing plan, plan when reviewing code, grill decisions when reviewing spec, spec boundaries when reviewing solid)
   - For code: `git diff` / `BASE...HEAD`
2. **Run the reference rubric** — claim→case table is mandatory output (see below). Prefer a fresh subagent/reviewer when available; otherwise self-review with the same rubric.
3. **Report** by severity: Critical / Important / Minor — every finding in plain language, three-part (scene → what someone hits → where in the artifact).
4. **Act**: fix Critical + Important; note Minor; push back on wrong findings with evidence.
5. **Re-verify** — if fixes landed, re-run the relevant part of the claim→case table; for code re-run tests (**debug** verification gate / **tdd**).
6. **Hand off** to **commit-and-push** when shipping.

## The claim→case table (mandatory)

**A claim that is not falsified is not reviewed.** Like a test suite, the claim→case table makes each falsifiable claim in the artifact a row, injects scenarios, and assigns a verdict.

For each row:

- **Claim:** one falsifiable assertion from the artifact (a spec acceptance item, a plan task's "the test verifies Z", a solid "domain does not depend on IO", a code behavior).
- **Scenarios injected** (minimum two; add more until the row stops surprising you):
  - happy path
  - at least one **boundary** (empty, zero, max, just-out-of-range, first/last element, deadline, quota…)
  - at least one **extreme** (100× load, missing upstream, permission denied, network drop, corrupt input, angry user, midnight rollover…)
  - a **real case** if you have one — a past incident, a user complaint, a regression that already happened. Inject the real case verbatim; the artifact must survive it.
- **Verdict:** PASS / WATCH / BLOCK.
  - PASS — holds under injected scenarios.
  - WATCH — holds on happy path but a boundary/extreme/real scenario is unaddressed, unstated, or ambiguous.
  - BLOCK — a scenario directly contradicts the artifact (silent scope add, untraceable task, boundary no one owns, acceptance not demoable).

**Output shape — a fixed section in every report:**

```markdown
### claim→case table
| Claim | Scenarios injected | Verdict |
|-------|--------------------|---------|
| …     | happy; boundary; extreme; real case   | PASS/WATCH/BLOCK |
```

Full table for a small artifact; for a large one, write every WATCH/BLOCK row + one line "remaining rows swept, no anomalies" — never drop a row without an explicit sweep note.

**Real-case injection:** when a real case exists (you have the incident text, a failing repro, a user's exact words), it takes priority over invented scenarios — the artifact must be run through it first.

## Report shape

```markdown
## Review
**Object:** spec | plan | solid | code (BASE...HEAD or paths)
**Upstream checked:** <path or "none — WATCH noted">
**Verdict:** proceed | blocked

### Strengths
- …

### Critical
- …

### Important
- …

### Minor
- …

### claim→case table
| Claim | Scenarios injected | Verdict |
|-------|--------------------|---------|
```

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "It's a small change" | Small changes break prod too. Run the rubric anyway. |
| "Tests pass = good" | Tests can be theater. Check the claim→case table covers the claims. |
| "It's just a plan/spec, nothing to test" | Plans/specs have falsifiable claims — that is what the claim→case table is for. |
| "The user is technical, no need for plain words" | Findings must survive being read by the next person who was NOT in the room. Plain words are for them. |
| "I'll review in the PR UI later" | Catch now; later compounds. |
| "Reviewer is wrong so ignore" | Push back with evidence — don't ghost Critical. |

## Red Flags

- Shipping without opening the artifact (diff, spec text, plan tasks, boundary decisions)
- "LGTM" with no claim→case table pass
- Proceeding with open Critical/Important
- Reviewing only the object, never its direct upstream
- Findings written in jargon only, with no scene / no "who gets hit"

## Checklist

- [ ] Object identified; matching reference open
- [ ] Artifact + direct upstream in hand (upstream missing → WATCH finding)
- [ ] claim→case table filled; every claim falsified or swept
- [ ] Findings plain-word three-part (scene → what someone hits → where); no decorative metaphor
- [ ] Severities assigned; blockers fixed or waived by human
- [ ] Verification re-run if fixes landed
- [ ] Ready for commit-and-push when shipping

## Hand-off

**Transition gate** — the review report is done; before shipping, ask the user (one AskUserQuestion; never auto-ship a report with open blockers):

```
A) Recommended: Proceed → commit-and-push (clean, or Critical/Important fixed or waived with reason)
B) Fix open Critical/Important first — back to debug / tdd, then return to this gate
C) Adjust — re-review a narrower object / different slice, then return to this gate
D) Something else (I will type it)
```

- Code findings → **debug** / **tdd**
- Structure issues → **solid**
- Spec/plan product ambiguity re-opened → **grill**
- Ship → **commit-and-push**
