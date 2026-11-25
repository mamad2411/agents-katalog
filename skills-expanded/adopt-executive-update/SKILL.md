---
name: adopt-executive-update
description: Writes a one-page executive update on AI adoption with the bottom line and the decision asked first, what changed in the work with its source and date, a fixed section on what the evidence does not show, concerns raised and what was done, and what the team needs. Use for "run adopt-executive-update", "AI adoption executive update", "one page on AI for leadership", "report AI adoption to executives", "the board wants one number for AI", "AI pilot update for the sponsor", "AI progress report for leadership", "slides on AI adoption results", part of the Claude Guide for AI Adoption Pack by 90n.
---

# AI Adoption Executive Update

## When To Use
Executives want one number for AI and the honest answer is more useful than the number. Use this when there is an evidence review to summarise and a decision you need from leadership. It answers: what changed in the work, how do we know, what do we not know, and what are we asking you to decide?

## When Not To Use
Not when the evidence has not been read yet: a page written straight from raw counts repeats the dashboard, so run AI Adoption Evidence Review first. Not as the record of whether to expand: the options, trade-offs and pause rules belong in AI Rollout Decision, and this page only asks for that decision.

## Inputs
- The evidence review, or its findings with each source and date.
- The concerns raised and what was done about each, without names, and what the team needs from leadership: time, access, a decision on a rule.
- The decision you are asking for, who makes it and by when. Optional: one or two approved use stories.
If you have none of this, I start from what changed in the work in your own words and the decision you want, mark every unsourced line "source to add", and mark the output as a first draft.

## Approach
Bottom line first: the reader gets the conclusion and the request before any background, in line with the "organise and summarise up front" principle of the US General Services Administration's plain language guides. The evidence then follows the five questions of RE-AIM, the evaluation framework published at re-aim.org (reach, effectiveness, adoption, implementation, maintenance), so use is never mistaken for effect. The judgement is to give a busy reader the limits as plainly as the result. The failure this prevents is the update that leads with a large "hours saved" total built from self-reports, gets repeated upward as fact, and leaves the team owning a number nobody can stand behind when it is audited.

## Workflow
1. Ask at most three questions: what decision do you need and from whom by when, which evidence do you have with its source and date, and has a single number been demanded?
2. Write the first two lines: the bottom line, then the decision asked. If you cannot write the bottom line in one sentence, the review is not finished; say so instead of padding.
3. Write what changed in the work, in the order reach, effectiveness, adoption, implementation, maintenance, each line with its source and date and with counts beside percentages. Use only the lines there is evidence for, and leave the others out.
4. Fill the fixed section "What this does not show": for example whether the change lasts, where any saved time went, anything about individuals. A reader who finds this section empty should distrust the page.
5. Summarise the concerns raised and what was done, from the response log, with no names, including the ones still open, then list what the team needs: time, access, a decision on a rule.
6. If a single number is demanded, give the best-evidenced measure with its definition and its limit beside it, never a converted "hours saved" total. Add at most one or two approved stories, each marked as one case.
7. Cut to one page. For the shared version, use Claude Docs (beta) for the page or Claude Slides (beta) for a short deck that exports to PowerPoint or PDF, or any document: a deck is the same six blocks, one per slide.

## Output Format
```markdown
# AI Adoption Executive Update
**Bottom line:** [one sentence: what changed in the work, and how sure we are]
**Decision asked:** [the decision, from whom, by when]. **Period:** [dates] · **Teams in scope:** [teams or roles] · **Prepared by:** [role], [date]
## What changed in the work
| Question | What we see (counts beside percentages) | Source and date |
|---|---|---|
| Reach | [finding at team level] | [source, date] |
| Effectiveness | [finding against the agreed measure and its baseline, side effects included] | [source, date] |
| Adoption | [which teams or settings took it up, which did not] | [source, date] |
| Implementation | [used as agreed, adapted, what it cost in time and support] | [source, date] |
| Maintenance | [still in use after [period], or "too early to say"] | [source, date] |
| One number, if required | [the best-evidenced measure, its definition, and its limit: what it leaves out] | [source, date] |
| One story, optional | [two lines, approved by the teller]. One case, not a rate. | [collected on date] |

## What this does not show
- [For example: whether the change lasts, or where any saved time went]. Nothing here was measured per person.
## Concerns raised and what was done
- [Concern, no names]: [what was done, or "declined because [reason]"]. [Open or closed, next date.]
## What the team needs
- [Time, access, or a decision on a rule, with who can give it]
## Decision
[Named executive or sponsor] decides [the decision asked] by [date]. If the answer is to expand, [name] prepares the rollout decision by [date].
```

## Done When
- The bottom line and the decision asked are the first two lines, the decision names a person and a date, and the page fits on one page.
- Every evidence line has a source and a date, rows with no evidence are removed, not filled, and "What this does not show" has at least one entry.
- Concerns carry no names and include those still open.

## Quality Bar
- Every figure comes from the organisation's own evidence or stays a bracketed placeholder: no benchmark, no outside statistic, no time converted into money, no return on investment.
- Team-level figures only, small groups merged or suppressed, no names in concerns or stories.
- Unwelcome findings sit in the table with the others, not in a footnote. The page asks for a decision; it does not announce one, and nothing is sent on anyone's behalf.
- No saving is claimed that the organisation's own evidence does not show, and the page says what the evidence does not show.

## Next
Run adopt-champions-network (AI Champions Network) to set up the people who keep it going after the update.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
