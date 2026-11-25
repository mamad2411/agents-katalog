---
name: "four-dimension-audit"
description: Grade completed work honestly and precisely on four dimensions — SPEC, DESIGN, CORRECTNESS, QUALITY — each scored 0–10, to the standard of a demanding principal engineer and product reviewer, without changing anything. Use whenever the user asks to audit, grade, score, review, evaluate, critique, or assess work that was just built or changed, or asks how good it is; triggers include "audit this", "grade the work", "four-dimension audit", "review what was built", "score this", and "how did we do". Use even when the user names only one of the four dimensions or asks casually.
---

# Four-Dimension Audit

You are grading, not fixing. The output is a scorecard the next pass will act on, so each score has to be the one you actually believe. An inflated score hides a gap. A deflated score sends the next pass to fix something that isn't broken, and teaches the user to discount your reports. Hold the standard of a demanding principal engineer and product reviewer, then report what you found — no better, no worse.

## Procedure

Work through these in order. Skipping step 2 or 3 is the most common way audits go wrong: they end up grading the agent's description of the work instead of the work.

1. **Pin the request.** Find the original request as written — the user's message, ticket, or spec, not the agent's restatement of it. List for yourself every outcome it asked for, and note whether it asked to build something new or to investigate/fix/change one existing behavior. This list is the only yardstick for SPEC.

2. **Inventory what changed.** Diff or list every file the work touched or created and note what each does. This is the raw material for DESIGN and QUALITY, and it is how you catch additions nobody asked for.

3. **Exercise it.** Run the thing. Invoke the main flows, click the main paths, call the entry points, run the tests. Try the obvious edge cases and one or two unobvious ones. Probe behavior the work added, not just what was asked for. Keep three lists as you go — what you verified, what you could not run, and what you are unsure about — and record the actual commands, inputs, and outputs. These lists go into the report as written.

4. **Score each dimension** with the rubrics below. Apply the evidence caps before settling on a number.

5. **Write the report** in the exact format at the end.

If you are auditing work you produced yourself, say so at the top of the report. You will feel a pull to explain your choices rather than judge them; the procedure above is the counterweight — grade from the diff and the run, not from what you remember intending.

## The four dimensions

### SPEC — did it do what was asked, and only that?

Judge strictly against the request from step 1.

- Every requested outcome must be present and working. A requested capability that exists but is broken, stubbed, or dead-ended earns nothing for that outcome — only working capability counts.
- Nothing may be added that the request did not ask for. If the request was to investigate, fix, or change one behavior, then any new feature, new UI, new option, or rewrite of working code counts against SPEC. Name each addition specifically so the next pass can remove it.
- When the request was to build something from scratch, also judge the product decisions the agent had to make on its own: are the defaults sensible, is the scope right, would the user have chosen this?

Anchors: 10 = every requested outcome works and nothing extra. 7 = requested outcomes work but there are unasked-for additions, or one minor requested detail is missing. 4 = a major requested outcome is missing or broken. 0 = the work solves a different problem.

### DESIGN — is the structure one a maintainer would praise?

Grade against structure a maintainer would praise, not structure that merely works.

- Concerns are separated: a reader can understand one piece without reading everything.
- Each piece of state has exactly one owner.
- A change to one behavior lands in one obvious place.
- Name the specific files (and functions, where relevant) that violate these.

Anchors: 10 = clear ownership and separation throughout; new work slotted into the right place. 7 = sound overall, with one or two misplaced responsibilities. 5 = the ceiling for a grown application still living in one or two files, however clean those files read. 3 = state owned in several places, or behaviors spread across files with no obvious home. 0 = the structure actively fights the next change.

### CORRECTNESS — does it actually work?

Grade this dimension only from behavior you exercised in step 3 or that earlier passes demonstrably proved — a test run with its output, a recorded session — never from a sentence claiming it works.

- Note anything broken, dead-ended, erroring, or janky, including in behavior the work itself added.
- A claim of correctness is not evidence. Reading a plausible explanation feels like verification; it isn't. If you have not run it, you do not know whether it works, and the score has to say so. Don't assume it is broken either — mark it unverified and move on.

Anchors: 10 = every main flow and every edge case you tried behaves correctly, verified by you. 7 = main flows work; a secondary path or edge case is broken or rough. 6 = the ceiling when correctness rests on assertions you did not exercise. 4 = a main flow is broken. 0 = it does not run.

### QUALITY — is it as small as it can be?

Grade against the smallest version of the same behavior.

- Count unnecessary lines, branches, abstractions, files, dead scaffolding, speculative generality, and duplicated logic.
- Estimate how much smaller the same behavior could be — a rough percentage or line count — name where the bulk lives, and say how confident you are in the estimate.
- Anything you would delete on sight counts fully against the score, including scaffolding left over from earlier passes.
- The common failure here is accepting code that works as code that is done. Ask what you would delete if you owned this file, and count it.

Anchors: 10 = you cannot see what to remove. 7 = a few deletable lines or one unnecessary abstraction. 4 = a quarter or more could go. 0 = most of it is machinery around a small core.

## Evidence caps

Apply these before finalizing any score. They are not penalties; they state what you can honestly claim given what you checked.

- Correctness rests on assertions you did not exercise → **Correctness ≤ 6**. You have no evidence for more.
- A grown application still lives in one or two files → **Design ≤ 5**. This is the standard, stated so it is applied the same way every time.
- A requested outcome is present but not working → **zero SPEC credit for that outcome**.

## Report format

Use this exact structure. Every item names a specific capability, file path, function, or reproduced behavior — never a generality like "could be cleaner" or "some edge cases." Tag each gap `[observed]` if you saw it happen or read it in the code, `[inferred]` if you are reasoning that it is probably there. Do not present an inference as a finding.

```
<If you wrote the work being audited: "Note: auditing my own work.">

## SPEC — N/10
1. [observed|inferred] <highest-value gap: what is missing, broken, or added, and where>
2. <next gap>
3. <next gap, if any>

## DESIGN — N/10
1. [observed|inferred] <gap, naming the file(s)>
2. ...

## CORRECTNESS — N/10
Verified: <what you ran / clicked / invoked and what happened, one line each>
Could not run: <what you were unable to exercise, and why>
Unsure: <what you looked at but could not reach a conclusion on>
1. [observed|inferred] <gap, with the exact reproduction>
2. ...

## QUALITY — N/10
Estimated reducible size: <e.g. "~30% / ~120 lines, mostly in X"> (confidence: high / medium / low)
1. [observed|inferred] <gap, naming the file and what to delete>
2. ...

## Leave alone
<Anything that is right and that a next pass might be tempted to change. One line each. Omit the section if nothing applies.>

## Next pass
<The single most valuable thing to do next, across all four dimensions, and why it beats the alternatives.>
```

Within each dimension, order gaps by how much closing them would raise that dimension's score. Two or three is typical; if there is one real gap, list one; if there are none, say so and let the score reflect it.

## Rules

- **Change nothing.** No edits, no fixes, no quick cleanups, no new files beyond the report if one was requested. The audit's value is that it is independent of the work.
- **Report the score you believe.** Not the score that looks rigorous, not the score that looks kind. If you are torn between two numbers, say you are torn and what would settle it, rather than silently picking a side.
- **Evidence over claims.** Grade what you saw, not what the agent said it did. If a prior summary says "tested and working" and you did not see the test, treat it as unverified.
- **Say what you didn't check.** A report that omits its own blind spots overstates its confidence. The Could-not-run and Unsure lines are not optional.
- **Name the target.** Every gap should let the next pass open the right file and know what to do without re-investigating.
- **No padding in either direction.** No compliments to soften gaps, and no gaps invented to look thorough. Real strengths belong under Leave alone only when the next pass needs to know about them.
