---
name: fac-session-feedback-form
description: Writes a session feedback form of four to six questions with answer options that describe a concrete state, two open prompts and an aggregate summary template that rates the session, never the trainer or a participant. Use for "run fac-session-feedback-form", "training feedback form", "better smile sheet", "end of session survey", "workshop feedback questions", "post training evaluation form", "happy sheet questions", "the form says everyone loved it", part of the Claude for Trainers and Facilitators Pack by 90n.
---

# Session Feedback Form

## When To Use
The form says everyone loved it and tells you nothing to change. Use this before a session to build the form you hand out at the close, and the summary you fill in afterwards. It answers one question: did people get something they can and will use, and what stands in the way?

## When Not To Use
A form filled in on the day cannot show learning or use at work, so do not ask it to. Before the session, when the questions are for the design, run Pre-Session Survey. For what you and your co-trainers saw from the front, run Facilitator Retro.

## Inputs
- What people should be able to do or use after the session, in one or two sentences
- Your current form, if there is one, and how it reaches people (paper, or a link from your survey tool)
- The minimum group size below which results are not reported
If you have none of this, I start from the session title and what you remember of its aim, and mark the output as a first draft.

## Approach
LTEM, the evaluation model from Work-Learning Research, sets out eight tiers and is blunt that its lower tiers, learner perceptions among them, cannot validate learning on their own. So the form stops asking whether people enjoyed the day and asks about what points to use: relevance, real practice, readiness, support, obstacles. The failure it prevents is the form full of "the trainer was engaging" items, which reads as a verdict on a colleague and leaves the session exactly as it was.

## Workflow
1. Ask three questions: what should people be able to do after this session, which parts of the session are you free to change, and what is the minimum group size for reporting?
2. Audit the current form, if there is one. Mark each item: rates the trainer (remove), measures satisfaction (keep one at most), or points to use (keep and sharpen). Show the verdicts so you can overrule them.
3. Write four to six closed items, one each on relevance to the work, whether people practised the real thing, readiness to use it, the support they expect back at work, and what could get in the way. An item that could not lead to a change you are free to make is cut.
4. Give every item answer options that describe a concrete state ("I could do this now without help", "I would need more practice first"). No "agree" or "strongly agree", and no number scale: a number invites an average, and an average hides the people who are stuck.
5. Add the two open prompts and the line at the top of the form: anonymous by default, the answers help fix the session and say nothing about any person.
6. Build the summary template: counts per option, themes from comments, groups under your minimum suppressed, no quote that identifies someone, one change to make per item, and the limits written on the page.
7. Hand over the cold read for you to run before it ships: answer the form yourself as a participant in your last session, and strike any item where no answer would change what you do.

## Output Format
```markdown
# Session Feedback Form
Session: [name] | Date: [date] | Anonymous by default. Your answers help fix the session and say nothing about any person.
Audit of the current form: [item] is [rates the trainer: remove / satisfaction: keep one at most / points to use: sharpen to ...]
## Questions
| # | Question | About | Answer options (concrete states) |
|---|---|---|---|
| 1 | How close was this session to the work you do? | Relevance | [state A] / [state B] / [state C] |
| 2 | How much did you practise [the real task]? | Practice | [state A] / [state B] / [state C] |
| 3 | How ready are you to [objective] at work? | Readiness | [I could do this now without help] / [I would need more practice first] / [state C] |
| 4 | What support do you expect when you try it? | Support | [state A] / [state B] / [state C] |
| 5 | How likely is something to get in the way? | Obstacles | [state A] / [state B] / [state C] |
## Open prompts
1. What could stop you using this in the next [period]? 2. What should be cut, and what should be added?
## Summary (filled in after the session)
Responses: [count] of [participants]. Groups under [minimum group size] are not reported. Limit: a form filled in on the day cannot show learning or use at work.
| Question | Count per option | Themes from comments | Change to make |
|---|---|---|---|
| [#] | [counts, or "suppressed"] | [theme] | [change to the session] |
## Decision
[Trainer name] decides by [date] which changes go into the next run, and [name] confirms who may see the summary.
```

## Done When
- No item rates the trainer or asks about a named person
- Every closed item has options that describe a concrete state, with no agreement scale and no numbers
- The summary reports counts and themes only, with your suppression threshold and the limit of the form written on it
- You have run the cold read, and every item left points to a change you could make

## Quality Bar
- Fewer items answered honestly beat a long form finished at the door; one satisfaction item at most
- Comments are summarised as themes; a quote that could identify someone is left out
- How answers are stored and who may read them is a privacy point: check with a qualified adviser
- The form rates the session, never the trainer or a participant; results are read in aggregate with small groups suppressed.

## Next
Run fac-facilitator-retro (Facilitator Retro) to add what the team saw to what participants said.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).