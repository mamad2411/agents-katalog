---
name: build-ai-prototype-check
description: Checks where the inputs of an AI feature inside a prototype came from and writes an AI Prototype Input Check with every hand-picked input listed, a masked share of real cases drawn at random, runs per input, picked and random results reported apart and what one good run cannot show. Use for "run build-ai-prototype-check", "the AI part worked on my three examples", "is my AI demo cherry-picked", "test the AI feature on random inputs", "how many times should I run each input", "what does one good run prove", "check the AI feature before the demo", part of the Claude for Product Builders Pack by 90n.
---

# AI Prototype Input Check

## When To Use
The AI part worked beautifully on the three examples you chose. Run this before anyone else sees it, or straight after a demo that went suspiciously well. It answers: where did the inputs come from, how many times did each one run, and what would the same feature do on a case nobody picked?

## When Not To Use
If the prototype has no AI feature inside, skip this. If you need the belief about users and its pass line, that is Prototype Test Card; for the full list of what stands between a prototype and production, use Prototype vs Production Note.

## Inputs
- What the AI feature does, and the inputs it has been tried on so far
- Who chose those inputs, and why
- The pool of real cases it could draw from, described, with any sample masked
If you have none of this, I start from a one-line description of the feature and mark the output as a first draft.

## Approach
The method starts from the Test Card (Strategyzer, strategyzer.com/library/validate-your-ideas-with-the-test-card): what must be true, how you test it, what you measure, what success looks like. For a system that does not answer the same way twice, a practitioner convention adds two things: a check on who chose the inputs, and repeat runs. The inputs you pick are the ones you already suspect will work. The failure it prevents: three chosen examples, one good run in a meeting, and "it works" becoming a date in someone's plan.

## Workflow
1. Ask up to three questions: what does the AI feature do and for whom, which inputs has it run on and who chose them, and who sets the pass line?
2. Write the belief as the card asks: "[the AI feature] can [task] on [kind of input] well enough that [user] will [behaviour]". If it holds "and", it is two beliefs and two checks.
3. List every input someone chose by hand, with who chose it and why. No judgement in the list; it is a record of where each case came from.
4. Require a share drawn at random from real cases. You set the number. The cases are masked before use, and whether real cases may be used at all is approved by a named person first; on that question, check with a qualified adviser.
5. Set the runs per input; you choose the number. One run of a system that varies is a demo, not a rate. Agree one observable measure before the runs (passes the agreed check, edits needed), and have the pass line set and dated first. I never propose a pass line once results exist.
6. Report picked and random results in separate tables, as "[n] of [N]", never blended. Then list what one good run cannot show: variation between runs, input nobody picked, hostile input, cost at volume.

## Output Format
```markdown
# AI Prototype Input Check
Prototype: [name] | AI feature: [what it does] | Check written: [date]
## Belief and pass line
| Item | Entry |
|---|---|
| What must be true | [the AI feature] can [task] on [kind of input] well enough that [user] will [behaviour] |
| Measure and runs | [one observable measure]; [number set by the builder] runs per input |
| Pass line | [threshold], set by [role] on [date], before any run |
## Picked inputs
| Input (masked) | Chosen by (role) | Why it was chosen | Passed |
|---|---|---|---|
| [input] | [role] | [reason] | [n] of [N] runs, or not yet run |
## Random inputs
| Input (masked) | Drawn from | Use approved by (role) | Passed |
|---|---|---|---|
| [input] | [pool, drawn at random] | [role, date] | [n] of [N] runs, or not yet run |
## Against the pass line
Picked set: [n] of [N], [met / not met / not yet run]. Random set: [n] of [N], [met / not met / not yet run]. The two are never added together.
## What one good run cannot show
Variation between runs: [reason]. Input nobody picked: [reason]. Hostile input: [reason]. Cost at volume: [reason].
## Decision
[Named person, by role] reads the random set against the pass line dated [date] and decides by [date] whether the AI feature goes in front of testers, is changed, or is shown as faked.
```

## Done When
- Every input is in one of the two tables, with where it came from
- The pass line carries a date earlier than the first run, and picked and random results are never added together
- All four "cannot show" areas have a line

## Quality Bar
- No result is predicted or filled in before it is run. "Not yet run" is a valid entry.
- Random real cases are masked; no person can be identified from an input or an output in the record.
- The check rates the feature's outputs, never the people whose cases were drawn or the person who picked the examples.
- A good run on picked inputs is a demo; a named person sets the pass line before the runs. On using real cases, check with a qualified adviser.

## Next
Run build-secrets-check (Secrets and Keys Check), since an AI feature usually means a key.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
