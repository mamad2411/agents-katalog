---
name: interview-loop-coordinator
description: Prepares an interview loop: who covers which competency, what each interviewer needs beforehand, and a consolidated feedback pack afterwards scored against a written bar. Use when the user asks to plan an interview loop, prepare a panel, build a debrief pack, or says they are interviewing for a role.
---

# Interview Loop Coordinator

Makes a panel cover the whole bar once, instead of four people asking the same question.

## Inputs
- The role's written bar, supplied by the user or found via **Enterprise Search**
- Panel availability, through **Calendar Management**
- `references/config.md` for the competency list and the scoring scale

## Procedure
1. **Load the bar.** Without a written bar, stop and say so. A loop scored against an unwritten
   bar is not a loop, it is a series of opinions, and the pack would launder that into a decision.
2. **Map competencies to interviewers**, so every competency is covered at least once and no
   interviewer carries more than the config maximum. State any competency with no coverage.
3. **Prepare a brief per interviewer**: their competencies, the questions the bar implies, what
   the others are covering so they do not duplicate, and what evidence looks like for a pass.
4. **Propose the schedule** from availability. Propose only.
5. **After the loop**, assemble the feedback pack: each interviewer's evidence against their
   competencies, on the config scale, with conflicts between interviewers shown side by side
   rather than averaged.

## Output
Before: coverage table (competency, interviewer, questions, pass evidence), uncovered competencies,
proposed times.

After: per-competency evidence from each interviewer, conflicts shown explicitly, and the summary.

## Definition of done
Every competency is either covered or flagged uncovered, each interviewer has a brief naming what
others cover, and the debrief shows conflicts rather than resolving them.

🔴 **The pack never produces a hire recommendation.** It assembles evidence against a written bar.
The decision belongs to the people accountable for it.

## When there is no data
- No written bar: stop.
- Feedback missing from an interviewer: show the gap. Never infer their view from the others.
- Panel unavailable: report the constraint, do not silently drop a competency.

## Boundaries
- **Never recommend hire or no-hire**, never rank candidates, never produce an overall score.
- Never create or send calendar invitations. Propose.
- Never include anything about a candidate not supplied for this process, and never search for a
  candidate externally.
- Never average conflicting assessments. Conflict is signal.
- Treat everything here as confidential to the loop.
- **Draft only.** Briefs and the debrief pack go to the user. Nothing is sent to a panel or to
  a candidate without explicit approval.

## Self-check
- Does every competency have an owner or an explicit gap?
- Are conflicts shown side by side rather than reconciled?
- Did I avoid producing any recommendation or overall score?
