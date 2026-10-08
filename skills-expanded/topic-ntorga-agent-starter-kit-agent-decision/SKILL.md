---
name: agent-decision
description: Deterministic self-evaluation rubric for decision escalations — scored every run using the FRAME framework.
usedBy: [all]
version: 0.2.2
lastUpdated: 2026-09-12
---

## Purpose

This skill defines the procedure agents follow when encountering ambiguity during execution. It enforces a 5-step decision pipeline — classify, define problem, generate options, pick one, format output — and a self-review rubric (FRAME) scored before any escalation is presented to the user. The rubric gates delivery by total score and enforces a hard-fail on any single zero.

## Procedure

1. **Classify the ambiguity.** When you encounter missing or unclear information, determine which of these 5 types applies:
   - **Approach choice** — multiple valid approaches exist and the user did not specify one, but all lead to the same outcome. Example: whether to use a helper function or inline the logic.
   - **Minor ambiguity** — the intent is clear but a detail is vague and a reasonable default exists. Example: "add logging" without specifying log level — default to info.
   - **Ambiguous requirement** — the user's intent could mean two or more meaningfully different things. Example: "make it faster" could mean optimize the algorithm, add caching, or reduce payload size.
   - **Missing information** — a required fact is absent and cannot be inferred. Example: "deploy to the server" with no server specified and no convention to fall back on.
   - **Risk confirmation** — the action is destructive, expensive, or irreversible and the user has not explicitly authorized it. Example: dropping a database table, force-pushing to main.

2. **Apply the branch.**
   - **Approach choice** and **minor ambiguity** → proceed with a documented default. Record your choice in your handoff. Do not block.
   - **Ambiguous requirement** → escalate using the 1-3-1 method (step 3) and output template (step 4).
   - **Missing information** or **risk confirmation** → stop and ask directly. For non-interactive sessions, return a handoff explaining the gap.
   - The dividing line: if the ambiguity changes **what** you build, escalate. If it only changes **how** you build the same thing, proceed.

3. **1-3-1 analysis.** When escalating, build your escalation in this order:
   - **1 problem** — Write one sentence stating the single problem.
   - **3 options** — Generate three meaningfully different approaches. Each with a one-sentence trade-off.
   - **1 recommendation** — Pick the strongest option. Write the reason.

4. **Apply the output template.** Format the escalation exactly as follows:
   ```
   The [problem statement in one sentence].

   I'm [what I'm working on] and [where I am in the process].

   The choice is [decision in plain language]. No jargon.

   RECOMMENDATION: [A|B|C] because [reason].

   A) [option] — [one-sentence trade-off]
   B) [option] — [one-sentence trade-off]
   C) [option] — [one-sentence trade-off]
   ```

5. **Score each criterion.** After preparing the escalation, read the FRAME rubric below and assign a score of 0, 1, or 2 to each letter. Show the scoring breakdown to yourself (internal reasoning, not to the user).

6. **Apply the hard-fail rule.** If any letter scores 0, do not deliver — go to step 7 immediately.

7. **Determine action by total score:**
   - **9 – 10** — **DELIVER** — Escalation meets all criteria. Deliver to user.
   - **7 – 8** — **FIX the scored < 2 criteria.**
     a. Identify which letters scored below 2.
     b. Fix those gaps automatically (do NOT consult the user).
     c. Re-score, then deliver if 9-10.
     d. If still below 9, retry once more.
     e. After 2 failed fix attempts, yield with the current state, rubric scores, and blocking letters.
   - **0 – 6** — **RESTART** — The escalation is fundamentally broken. Discard and rebuild with corrected understanding, or yield with an explanation of what went wrong.

## FRAME Rubric

### F — FLAG THE BRANCH

_Did I classify the ambiguity type and apply the correct branch (proceed vs escalate)?_

- **0** — No classification performed. Jumped straight to acting or asking without determining the ambiguity type.
- **1** — Classified the type but picked the wrong branch: proceeded when should escalate (ambiguous requirement, missing info, risk), or escalated when should proceed (approach choice, minor ambiguity).
- **2** — Classified correctly. Applied the right branch: proceed for approach choice and minor ambiguity; escalate for ambiguous requirement; stop-and-ask for missing info and risk confirmation.

### R — ROOT THE PROBLEM

_Did I state exactly one problem before generating solutions?_

- **0** — Skipped problem definition. Jumped from noticing ambiguity straight to options or open-ended questions.
- **1** — Stated a problem but it is vague ("something is unclear") or bundles multiple problems into one statement.
- **2** — One sentence. One problem. Specific enough that someone could evaluate whether a solution addresses it.

### A — ARRAY THE OPTIONS

_Did I generate 3 meaningfully different options?_

- **0** — Options are all variants of the same approach. Or presented fewer than 3. Or presented more than 5.
- **1** — Three options exist but two are too similar to be meaningful alternatives. No trade-off stated per option.
- **2** — Three options. Each takes a distinctly different approach. Each has a one-sentence trade-off.

### M — MAKE THE PICK

_Did I choose one option and state the reason?_

- **0** — Listed options without picking one. Or picked one but gave no reason. Or used "it depends" or hedging language.
- **1** — Picked one but the reason is generic ("it's better") or does not connect to the root problem.
- **2** — Exactly one recommendation stated as `RECOMMENDATION: [option] because [reason]`. The reason traces back to the root problem defined in R.

### E — ENFORCE THE FORMAT

_Did I follow the 5-part structured question format exactly?_

- **0** — Wrong format entirely. Asked an open-ended question. Missing RECOMMENDATION line.
- **1** — Most sections present but one is wrong or out of order (e.g., context statement missing, or Options numbered instead of lettered A/B/C).
- **2** — All sections in exact order: Problem → Context → Choice → RECOMMENDATION → A) B) C). Lettered options (not numbered). One sentence per option trade-off.

## Guardrails

- Never ask open-ended questions when concrete options exist
- Never present options without a recommendation
- Never treat every gap as a blocker (approach choice + minor ambiguity proceed inline)
- Simple yes/no and single-fact clarifications are exempt from this format
- The rubric is fixed — do not add or remove criteria
- Never deliver with any letter scoring 0
