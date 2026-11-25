---
name: lawstu-cold-start-interview
version: 1.0.0
description: Onboarding interview for a new law student — capture school, year, courses, professors, and goals to tailor every other lawstu skill.
author: matrixx0070
tags: [law-student, onboarding, intake, personalization, setup]
capabilities: []
---

## When to use

Reach for this the first time you use the law-student toolkit, or at the start of a new semester. The skill interviews you to build a study profile — your year, courses, professors' teaching styles, exam formats, strengths, and goals — so the other lawstu skills stop asking the same context every time.

**Not for:** ongoing tweaks to how a skill behaves after setup (see `lawstu-customize`), or interview prep for a job or externship (this is an *intake* interview about your studies). It gathers context; it does no studying and produces nothing you submit.

## Method

1. **Establish the basics.** School, year (1L/2L/3L or bar candidate), jurisdiction of interest. Decision point: bar candidates route toward `lawstu-bar-prep-questions` framing from the start.
2. **Enumerate courses.** For each: professor, casebook, credit weight, and exam format (issue-spotter, policy essay, take-home, multiple choice).
3. **Probe teaching style.** Cold-call frequency, Socratic intensity, whether past exams are released, stated grading emphasis.
4. **Self-assess.** Rate confidence per course and name the two doctrines that scare you most. Decision point: sub-3 confidence flags a course for extra study-plan weight.
5. **Set goals and constraints.** Target grades/pass, realistic weekly hours, competing commitments.
6. **Emit a profile** the other skills consume, and recommend the first three to run.

## Example

Intake reveals: 1L, Contracts professor cold-calls daily and never releases exams; Torts is a policy-essay format. Profile flags daily `lawstu-cold-call-prep` for Contracts and steers Torts prep toward `lawstu-exam-forecast` policy simulation. You leave setup with a concrete first week, not a blank page.

## Pitfalls

- Rushing the interview and giving vague answers — every downstream skill inherits the gaps.
- Omitting exam format, the single most useful field for tailoring practice.
- Inflating confidence ratings; honest self-assessment drives smarter allocation.
- Treating the profile as permanent — re-run each semester.

## Output format

```
STUDENT PROFILE
School | year | jurisdiction
Courses:
  name | professor | exam format | credits | confidence /5
Teaching style: cold-call freq | Socratic | past exams? | grading emphasis
Fear list: [2 doctrines]
Goals | weekly hours | constraints
Recommended first skills: [3]
```

## Reference

- **Routing:** the profile seeds `lawstu-study-plan`, `lawstu-exam-forecast`, and `lawstu-session`.
- **Bar framing:** a bar-candidate profile front-loads MBE/MEE prep (`lawstu-bar-prep-questions`).
- **IRAC / case-brief** defaults are chosen per exam format captured here.
