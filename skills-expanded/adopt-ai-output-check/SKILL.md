---
name: adopt-ai-output-check
description: Writes a one-page check a person runs before using AI output for one named type of work, with five passes in order, a stop condition and who signs. Use for "run adopt-ai-output-check", "AI output check", "checklist for checking AI output", "how do we verify what AI wrote", "fact-check AI drafts", "AI review checklist before sending", "a wrong figure went out", "teach people to check AI", part of the Claude Guide for AI Adoption Pack by 90n.
---

# AI Output Check
## When To Use
People were taught to prompt and nobody was taught to check, and a wrong figure has already gone out under someone's name. You want one page a person runs before AI output is used for a specific type of work: a client email, a report with figures, a summary of a document, a policy answer. It answers: what exactly do I check, in what order, and when do I not use the output at all?

## When Not To Use
If you want one card covering the whole task, including when to use AI and what to give it, use AI Job Aid: this skill is only the checking, in depth. If the team has not yet agreed which uses are fine at all, start with Team AI Agreement.

## Inputs
- The type of work, with one or two real examples (sanitised) and where its source material lives.
- What goes wrong when this work is wrong, and who is affected, in your own words.
- Your organisation's never-put-in list, who answers questions about the rules, and who signs this type of work today.
If you have none of this, I start from the type of work described in a few lines and mark the output as a first draft.

## Approach
The check rests on two judgements a person makes when working with AI: how to check, and what you stay responsible for. There is one check per type of work, because the harm differs: a flattened nuance in a summary and a wrong figure in a report need different attention. How deep the check goes is set by the cost of being wrong, which you describe in words. The failure this prevents: the reviewer reads a fluent draft, finds it convincing, and "checked" comes to mean "read it once and it sounded right".

## Workflow
1. Ask at most three questions: which type of work this check is for, what happens and to whom when that work is wrong, and who signs it today.
2. Set the depth from the cost of being wrong, in words (for example "an internal note that is easy to correct" or "a figure a client will act on"). No numeric risk rating; you set what counts as light or full.
3. Write pass 1 and pass 2 for this work. Pass 1: trace each factual claim to a source the person can open. Pass 2: check every number, name, date and quotation against that source. Name where the sources live, or the pass will be skipped.
4. Write pass 3: read for what is missing or flattened. List what this type of work must always contain (a caveat, a second view, an exception), because a gap is harder to see than an error.
5. Write pass 4 and pass 5. Pass 4: confirm nothing on the never-put-in list went in. Pass 5: name who signs; that person can explain the work and owns it.
6. Write the stop condition: what makes the person not use the output at all (a claim with no source, a number that cannot be traced, a rule in doubt) and who to ask.
7. Cut it to one page with each line starting with a verb, and test it on one real output with someone who does the work.

## Output Format
```markdown
# AI Output Check
Type of work: [client email, report with figures, document summary, policy answer] | Check owner: [role] | Review date: [date]
Cost of being wrong, in words: [what happens, to whom] | Depth: [light, standard or full, as you define them]
## The check
| Pass | Do this | For this work | Done |
|---|---|---|---|
| 1 Sources | Trace each factual claim to a source you can open | [where the sources live] | [ ] |
| 2 Figures and names | Check every number, name, date and quotation against that source | [what to compare with] | [ ] |
| 3 Gaps | Read for what is missing or flattened | [what this work must always contain] | [ ] |
| 4 What went in | Confirm nothing on the never-put-in list went in | [the list items that apply here] | [ ] |
| 5 Signature | Name who signs | [role]: can explain it and owns it | [ ] |

## Stop condition
| Stop and do not use the output if | Then | Ask |
|---|---|---|
| [a claim has no source] | [remove it or go back to the source] | [role] |
| [a number cannot be traced] | [do not send] | [role] |
| [a rule is in doubt] | [pause] | [rules owner] |

## What this check does not cover
[Types of work that need their own check; legal, data protection or regulated content, which is a point to check with a qualified adviser]
## Decision
[Process owner for this type of work] approves the check and the stop condition by [date]. [Team lead] decides where the check sits in the workflow by [date]. The person who signs each piece of work runs the check.
```

## Done When
- The check names one type of work and fits on one page.
- The five passes are in order and each is filled in for this work, with the source location named.
- The stop condition says when not to use the output and who to ask; a named role signs; the check has been tried on one real output.

## Quality Bar
- Each line starts with a verb. "Looks right" is never a pass; each claim meets a source the person opens.
- The depth follows the cost of being wrong, described in words; no numeric risk rating.
- The check looks at outputs. It keeps no error log by person and asks nobody who made the mistake.
- A second type of work gets a second check. A person does not skip a pass because the draft reads well.
- A person runs the check and signs the work; responsibility never passes to the tool.

## Next
Run adopt-ai-job-aid (AI Job Aid) to put the check where the work happens.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
