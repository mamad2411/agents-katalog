---
name: lawstu-irac-practice
version: 1.0.0
description: Drill IRAC on hypotheticals — you write each element, the skill critiques structure, rule accuracy, and application depth.
author: matrixx0070
tags: [law-student, irac, exam-writing, hypotheticals, feedback]
capabilities: []
---

## When to use

Reach for this when you can recite the black-letter law but freeze turning it into exam prose. You write the Issue, Rule, Application, and Conclusion for a hypo; the skill grades your structure and tells you where an examiner would dock points.

**Not for:** producing a model answer you copy onto a graded exam or take-home. This is a coaching drill — it critiques *your* IRAC, it does not write the answer for you. That line is the point: an answer written by anyone but you teaches nothing and violates academic integrity. Not for briefing cases (see `lawstu-case-brief`).

## Method

1. **Read the call of the question first.** It scopes which issues count. Decision point: if you cannot restate what is being asked, stop and re-read the facts.
2. **Spot every issue**, majors and minors, before writing. Missed issues are the largest point loss.
3. **Write the Rule from memory** — elements broken out, exceptions flagged. The skill checks accuracy against black-letter law and names gaps; it will not hand you the rule verbatim before you attempt it.
4. **Apply fact-to-element.** For each element, tie a specific fact and argue both sides where facts are contested. This is where 70% of the points live.
5. **Conclude decisively** per issue, even when it is close.
6. **Self-score, then compare** against the rubric the skill returns.

## Example

Hypo tests negligence. Weak Application: "The driver was careless, so he breached." Coached rewrite: "A reasonable driver would slow in fog (standard); here the driver maintained 60 mph in near-zero visibility (fact); that gap shows breach — though the defense argues the posted limit was 65, which a factfinder may weigh." Same conclusion, far more earned points.

## Pitfalls

- Rule-dumping with no application — the classic B answer.
- One-sided application on facts the drafter made deliberately ambiguous.
- Merging issues into one blob; grade one issue at a time.
- Burying the conclusion or hedging every call.

## Output format

```
Hypo + call of the question
Your IRAC (per issue):
  I: [issue as question]
  R: [rule with elements]
  A: [fact ↔ element, both sides]
  C: [decision]
Coaching:
  issues missed | rule accuracy | application depth | rubric score /10
Next rep:
```

## Reference

- **IRAC structure:** Issue (legal question) → Rule (elements + exceptions) → Application (facts to each element, both sides) → Conclusion. Variants: CREAC (Conclusion first) for memos, FIRAC (Facts front-loaded) for briefs.
- **Bar-exam framing:** MEE/essay graders reward issue-spotting breadth and two-sided application — the same muscles this drill builds (`lawstu-bar-prep-questions`).
