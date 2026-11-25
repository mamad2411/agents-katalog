---
name: pdes-portfolio-case-study
description: Writes a Portfolio Case Study that tells one project through three to five decisions with the options you had and the trade-off you chose, your own role and who decided what, what real users did in testing, outcomes from real data, what you would do differently and a confidentiality check before anything is published. Use for "run pdes-portfolio-case-study", "portfolio case study", "ux case study", "write up a project for my portfolio", "my case study reads like everyone else's", "show my design decisions", "ux portfolio project", "case study from my design work", part of the Claude for Product Designers Pack by 90n.
---

# Portfolio Case Study

## When To Use
Your portfolio shows twenty polished frames and a line that says "the team loved it", and it reads like every other generated case study. Run it when a project is finished enough to have decisions behind it and, ideally, results. It answers: what did I decide, what did it cost, and what happened?

## When Not To Use
If the reader is inside your team and the point is what the work delivered, use Design Impact Write-Up; that one is internal and about results, this one is public and about your decisions and role. If the project has no decisions on record yet, a few entries in the Design Decision Log come first.

## Inputs
- One project: the brief, your rationale notes or decision records, the screens, what happened in real test sessions and outcome data with its source
- Your own role, who else worked on it (by role), and what you are allowed to show outside the organisation
If you have none of this, I start from your own account of one project and mark the output as a first draft.

## Approach
The spine is the four-part story the UX Design Institute describes in its article on what hiring managers look for in a UX portfolio (2022): Problem, Approach, Process, Result, with your specific role stated and the whole thing short enough to skim. The public product designer ladder in the GitLab Handbook asks for research that checks user needs and an evidence-based view that informs product decisions. Telling the Process through three to five decisions is this skill's own choice. It prevents the fluent case study that describes a process anyone could have followed and falls apart at the first "why?".

## Workflow
1. Ask three questions: which project and what was your own part in it, what real testing and outcome data exist, and what are you allowed to share?
2. Problem: what it was, why it mattered, your specific role, and a plain statement if you worked in a team. Add who decided what, by role. "I" for what you did, "we" for what the team did.
3. Approach: how you investigated, and only what took place. Research you did not run is not described as yours.
4. Process, as three to five decisions. For each: the options you had, what you chose, what it gave up, and the obstacle if there was one. A decision with no losing option is a description, so cut it or find the option.
5. What real users did: only from sessions that happened, as "n of N" from your notes. If no test ran, the section says "not tested with users" and stays in.
6. Result: outcomes from real data with the source and what else moved in the same period; a missing number reads `[not measured]`. Then what you would do differently, as a specific change.
7. Choose screens, one per decision at most, then cut to skim length. Last, the confidentiality check that you run yourself before publishing: employer and client names, unreleased work, data, colleagues, participants. Lay it out in any chat, in Claude Docs or in Claude Design.

## Output Format
```markdown
# Portfolio Case Study
**Project:** [name, generalised if confidential] | **My role:** [role, solo or in a team of roles] | **Period:** [dates] | **Cleared to share:** [yes, by which role / pending]
## Problem
[What it was, why it mattered, who decided what (by role).]
## Approach
[How I investigated. Only what happened.]
## Decisions
| # | Decision | Options I had | What I chose and why | What it gave up | Screen (one at most) |
|---|---|---|---|---|---|
| [1] | [decision] | [options] | [choice, reason] | [trade-off] | [screen ref or none] |
## What real users did
| Task or question | What happened ("n of N") | Source (session notes, date) |
|---|---|---|
| [task] | [observation, or not tested with users] | [source] |
## Result
| Outcome | Data | Source | What else moved it |
|---|---|---|---|
| [outcome] | [value or [not measured]] | [source] | [other changes] |
**What I would do differently:** [specific change]
## Confidentiality check
- Employer and client names: [action] | Unreleased work: [action] | Data: [action] | Colleagues and participants: [action] (remove, generalise, or cleared by which role)
## Decision
[Designer] decides by [date] what is published, once [the role that can clear it] has confirmed what may be shared.
```

## Done When
- Three to five decisions each show the options, the choice and what it gave up
- Your role is stated, nothing done by others reads as yours, and every outcome has a source or reads `[not measured]`
- The confidentiality check is filled in before anything is published

## Quality Bar
- Colleagues appear by role and are never judged; no participant can be identified
- No employer or client name unless you confirm it may be shared; if a contract limits what you can show, check with a qualified adviser
- "What I would do differently" names a real change, never a compliment in disguise
- Claude writes only what happened and what your data shows; a test that did not run and a number nobody measured do not appear.

## Next
Run pdes-design-decision-log (Design Decision Log) so the next case study has its decisions on record.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
