---
name: lawstu-case-brief
version: 1.0.0
description: Brief a judicial opinion yourself — extract facts, issue, holding, and reasoning into a tight case brief you can defend in class.
author: matrixx0070
tags: [law-student, case-brief, irac, reading, socratic]
capabilities: []
---

## When to use

Reach for this when you have an assigned opinion to read and want a brief you actually understand — one you could reconstruct under a cold call. This skill coaches you through briefing your own case; it asks the questions a good study partner would.

**Not for:** having a brief written for you to submit or recite as your own preparation. This guides, it never ghostwrites — you supply the reading, it pressure-tests your grasp. Not for briefing a real matter for a client (that is practice, not study), and not for outlining a whole course (see `lawstu-outline-builder`).

## Method

1. **Read first, brief second.** Read the full opinion before touching structure. Note where you got lost — that is where the exam risk lives.
2. **Pin the procedural posture.** Who sued whom, what was decided below, and what exactly is on appeal. Decision point: if you cannot name the standard of review, re-read.
3. **State the issue as a question** joining the disputed law to the material facts ("Does X apply when Y?"), not a topic label.
4. **Separate holding from dicta.** The holding answers the issue and binds; everything else is persuasion. Mark which is which.
5. **Trace the reasoning.** Reconstruct the court's steps — rule, application, policy — in your own words. Add the dissent's competing rule.
6. **Extract the rule** in one transferable sentence you could apply to a new hypo.

## Example

Issue draft: "Was there a contract?" → tightened to "Does an advertisement constitute an offer when it specifies quantity and a mode of acceptance?" The holding then answers *that* question; the store-restocking language becomes dicta you flag, not memorize.

## Pitfalls

- Copying headnotes or a commercial brief — you learn nothing and the professor's follow-up exposes it.
- Confusing dicta for holding, then over-applying it on the exam.
- Fact-dumping; keep only outcome-determinative facts.
- Skipping the dissent, which is often the next exam's majority.

## Output format

```
Case | Court | Year
Posture: below → on review (standard of review)
Facts: [material only]
Issue: [does X apply when Y?]
Holding: [answer + who wins]
Reasoning: [rule → application → policy]
Dissent: [competing rule]
Rule extracted: [one transferable sentence]
Open question for class:
```

## Reference

- **Case-brief format:** Facts → Procedural Posture → Issue → Holding → Reasoning → Dissent → Rule. Keep to one page.
- **IRAC linkage:** the extracted Rule feeds directly into IRAC practice (`lawstu-irac-practice`).
- **Bar framing:** briefs build the rule statements that become your MBE/essay rule bank later (`lawstu-bar-prep-questions`).
