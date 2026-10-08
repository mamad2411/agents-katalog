---
name: contextualizer-self-review
description: Deterministic self-evaluation rubric for Contextualizer — scored every run using the TRACE framework.
usedBy: [contextualizer]
version: 0.2.0
lastUpdated: 2026-09-12
---

## Purpose

Before delivering context files or briefs, the Contextualizer evaluates its own output against the TRACE rubric. Each letter is scored 0, 1, or 2 with evidence quoted from the rubric and cited from actual work. The total determines whether to deliver, rewrite, or abort.

## Procedure

1. **Gather evidence.** Honest self-review makes verification efficient. Accurate scorecards confirm fast; dishonest ones fail and re-run, wasting time and compute. Before scoring, run verification commands to gather proof. The examples below show common patterns — choose what provides the best evidence for your specific work.

   Examples:
   - Schema compliance: verify `.context.md` files have opening `<context>` tag with path and date, Summary, Constraints, Guidance sections
   - Feature map: verify `FEATURE-MAP.md` entries have feature name, flow steps with file paths and role descriptions
   - Anchored claims: `test -f <path>` for directories/files mentioned in context — confirms claims are grounded
   - Coverage: `find . -type f | wc -l` and `find . -type d | wc -l` to check project size against yield threshold
   - Brevity: `wc -l <context-files>` — each context file should be shorter than the directory it describes

   These are examples, not mandates. Choose commands that provide the strongest proof for your output.

2. **Score each criterion.** Read the TRACE rubric below. For each letter, assign a score of 0, 1, or 2. You must:
   - Quote the specific criterion level (0, 1, or 2) that your work matches.
   - Cite evidence from your actual work — files verified, schema elements checked, line counts measured. Generic claims like "I verified everything" are not evidence and score 0.

3. **Output the Scorecard.** Fill in the scorecard below. This is not internal reasoning — this is your deliverable checkpoint.

4. **Apply the hard-fail rule.** If any letter scores 0, do not deliver — go to step 5 immediately.

5. **Determine action by total score:**
    - **9 – 10** — **DELIVER** — Output meets all criteria. Deliver to user.
    - **7 – 8** — **FIX the scored < 2 criteria.**
      a. Identify which letters scored below 2.
      b. Fix those gaps automatically (do NOT consult the user).
      c. Re-score, then deliver if 9-10.
      d. If still below 9, retry once more.
      e. After 2 failed fix attempts, yield with the current state, rubric scores, and blocking letters.
    - **0 – 6** — **RESTART** — The output is fundamentally broken. Rewrite from scratch with corrected understanding, or yield to the user with an explanation of what went wrong.

## Scorecard

Complete this before delivering. Each letter requires the matched criterion quote and specific evidence from your work.

- **T — TASK** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [task classification, deliverable type produced]
- **R — RUN** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [schema elements verified, skill followed]
- **A — ANCHORED** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [files verified with test -f, claims traced to code]
- **C — COVERAGE** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [project size checked, yield condition evaluated, incremental vs rewrite]
- **E — EVIDENT** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [line counts, brevity comparison]

**Total: X/10** → Action: [DELIVER/FIX/RESTART]

## TRACE Rubric

### T — TASK

_Did I classify the task correctly and produce the right deliverable?_

- **0** — Wrong mode chosen (full scan when structural brief was needed, or vice versa). Produced the wrong deliverable type entirely.
- **1** — Right mode chosen but one deliverable element is missing or wrong format (e.g., review blocks without LOC counts, structural brief missing Information Flow section).
- **2** — Correct mode, correct deliverable, correct format. Full scan produced `.context.md` files AND `FEATURE-MAP.md`. Structural brief has all three sections (Modules, Boundaries, Information Flow). Review blocks respect 1500 LOC limit, module co-location, and boundary rules.

### R — RUN

_Did I follow the mandated skill and produce output in the correct schema?_

- **0** — Did not follow `skills/context-maintenance/SKILL.md` for full scan. Used ad-hoc format instead of the prescribed `.context.md` or `FEATURE-MAP.md` schema. Did not run the directory scan script when producing context files. Structural brief does not use the required three-section format.
- **1** — Followed the skill but one schema detail is off: `<context>` tag missing path or date, feature flow step lacks "what happens here" description, or `updated` date touched without content change.
- **2** — Followed `skills/context-maintenance/SKILL.md` end-to-end. `.context.md` files use exact schema: opening `<context>` tag with path and date, Summary, Constraints, Guidance sections. `FEATURE-MAP.md` uses exact schema: feature name, flow steps in order with file paths and role descriptions. Structural brief uses exact three-section format. Updated only drifted features in the existing map — did not rewrite it.

### A — ANCHORED

_Is every claim grounded in actual code? Nothing invented, nothing assumed._

- **0** — Invented purpose for a directory without reading its contents. Added constraints or guidance to `.context.md` that cannot be verified from the code itself. Added a feature to the map without tracing its full path through the codebase.
- **1** — Mostly grounded but one or more claims are uncertain: a directory's purpose is described vaguely rather than marked "unclear," or one feature flow step is inferred rather than confirmed by reading the actual code.
- **2** — Every claim traceable to code. Directories with unclear purpose are labeled as such rather than guessed. All `.context.md` constraints verified from code itself. Every `FEATURE-MAP.md` entry traced end-to-end from entry point to output. No assumptions, no inference without evidence.

### C — COVERAGE

_Did I scope correctly — incremental update, yield when too big, respect boundaries?_

- **0** — Rewrote `FEATURE-MAP.md` from scratch when it already existed. Project exceeds 200 files / 50 directories and no yield or coverage report was produced. Review blocks cross major architectural boundaries without tight coupling.
- **1** — Mostly scoped correctly but missed a drifted feature in the existing map, or did not report what was covered vs. what remains after a partial scan. One review block slightly exceeds 1500 LOC.
- **2** — Incremental update only — changed entries in existing `FEATURE-MAP.md`, untouched stable ones. Yield condition evaluated: project size checked, coverage gap reported if exceeded. Review blocks each under 1500 LOC, module files co-located, boundaries respected. Nothing left silently unprocessed.

### E — EVIDENT

_Can someone arriving cold orient from this output alone? Is it brief enough?_

- **0** — Output is bloated — `.context.md` takes longer to read than the directory itself. Newcomer cannot determine what a directory does without reading the code. Feature map cannot be followed from entry point to output.
- **1** — Output is mostly navigable but one `.context.md` summary is too detailed or one feature flow step is unclear without inspecting the code. Structure present but one section reads like prose instead of a quick-reference list.
- **2** — Every `.context.md` is brief: one-to-two sentence description, one-line-per-file summary, constraints and guidance only when needed. Feature map follows a straight path from entry to output — a newcomer can trace the flow without opening code. Structure over prose. Brevity check passes: output is shorter than the directory it describes.

## Guardrails

- Never deliver if any letter scores 0 — regardless of total. A zero is a hard fail.
- Never skip scoring any letter — all 5 must be evaluated every run.
- A letter without a specific evidence citation scores 0. "I verified everything" is not evidence — cite what you verified.
- Every evidence citation must reference a specific action, file path, command output, or verification result. Generic justifications are rejected.
- The scorecard is not internal reasoning — it is a deliverable checkpoint. Output it.
- The rubric is fixed — do not add or remove criteria. If a criterion proves inadequate, file a framework change request.
- When fixing gaps (score 7-8 range), only address the letters that scored below 2. Do not rework letters that already scored 2. Fix automatically — do NOT stop to consult the user.
- After 2 failed fix attempts, yield — do not keep looping. Present the current state, rubric scores, and blocking letters to the user.
- The "restart" action (score 0-6) means: do not deliver the current output. Rewrite from scratch with corrected understanding, or yield to the user with a clear explanation of the failure mode.
