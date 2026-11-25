---
name: isd-source-content-triage
description: Sorts an expert's raw material into a dated source inventory, a list of conflicts and unsourced passages for the expert to rule on, a practise, remember, look up, cut table and a cut list the expert can accept. Use for "run isd-source-content-triage", "the expert sent a 147-slide deck", "two manuals that disagree", "which version is current", "nobody can date this page", "what can we leave out of the course", "the SME wants everything in", "this page looks AI-written", "build the approved source list", part of the Claude for Instructional Designers Pack by 90n.
---

# Source Content Triage

## When To Use
The source is a 147-slide deck, two manuals that disagree, and a page nobody can date. Use this after the actions are agreed and before a single screen is drafted. It answers two questions in order: which of this material may count as a source at all, and what does the learner practise, remember, look up, or never see?

## When Not To Use
If the know-how you need is written nowhere in the pile, run SME Interview Script to get it from the expert. If you already hold a draft course and want its facts traced, that is AI Content Accuracy Check, which uses the approved list this skill produces.

## Inputs
- Everything the expert sent, attached as files (a Project helps when there are many), with whatever you know about dates and owners
- The actions the course serves, from your action map or a task list, and where cut content can live
If you have none of this, I start from a table of contents and three actions you name, and mark the output as a first draft.

## Approach
Cognitive load theory (Sweller, van Merriënboer and Paas, 2019, Educational Psychology Review) describes a limited working memory that everything on the screen competes for; action mapping, on its originator's public page, adds the cut rule of minimum information per practice. Sorting comes second here, on purpose. The failure this prevents is the course that teaches last year's limit with great clarity, because the superseded manual was the better written one and nobody asked which was current.

## Workflow
1. Ask up to three questions: which actions the course serves, who owns each source by role, and where cut content can live (a reference page, a job aid).
2. Take the inventory before any sorting: every file and section with its date, owner, version and status (current, undated, superseded, conflicts with). An undated or ownerless item is not an approved source until someone claims it; you chase the owner, I only list the gap.
3. Set the conflicts side by side. Where two sources disagree on a fact, both versions appear with their place and date for the expert to rule on. I never pick the winner, and the newer date is not a ruling.
4. Mark passages with no traceable origin, including text the expert says an AI drafted, as "to confirm". They stay out of the approved set until the expert confirms each claim, one by one.
5. Sort each remaining item against the actions: practise (the learner does it), remember (needed in the head during the task), look up (a job aid), cut. An item linked to no action is cut. Then test every "remember" item: if the person can look it up mid-task, it moves to look up.
6. Write the cut list in the expert's terms ("accurate, and it lives in the reference page"), each cut with a parking place, so nothing true is lost and nobody's work is called unnecessary.
7. Close with the approved source list: only items that are dated, owned, current and free of open conflicts. You decide what is ready to go to the expert; the accuracy check will trace the draft against this list later.

## Output Format
```markdown
# Source Content Triage
## Source inventory
| Item (file, section) | Date | Owner (role) | Version | Status (current / undated / superseded / conflicts with) |
|---|---|---|---|---|
| [Item] | [Date or undated] | [Role or none] | [Version] | [Status] |
## Conflicts and passages to confirm
| Type (conflict / no origin / AI-drafted) | Version A, place, date | Version B, place, date | Expert's ruling |
|---|---|---|---|
| [Type] | [Text as written, place, date] | [Text as written, place, date, or none] | [open] |
## Triage table
| Content item | Linked action | Bin (practise / remember / look up / cut) | In the head during the task? | Note |
|---|---|---|---|---|
| [Item] | [Action, or none] | [Bin] | [yes / no] | [Note] |
## Cut list
| Item cut | Reason in the expert's terms | Parking place | Accepted by the expert |
|---|---|---|---|
| [Item] | [Accurate, and it lives in [place]] | [Reference page / job aid] | [yes / contested] |
## Approved source list
[Item, version, date, owner by role] | Left out until claimed or confirmed: [items]
## Decision
[Expert name, role] rules on every conflict, every passage to confirm and every cut by [date]; [designer name] records the rulings and issues the approved source list. Anything still unclaimed on that date stays out.
```

## Done When
- Every item sent has a row in the inventory with a date, an owner and a status, or is marked as missing one
- Every conflict shows both versions with place and date, and no ruling is filled in for the expert
- Every item is linked to an action or sits in the cut list with a reason and a parking place
- The approved source list contains nothing undated, ownerless or still to confirm

## Quality Bar
- Facts are flagged for the expert, never corrected, and a gap is written `[to confirm with the expert]`
- Practise items are written as things the learner does, never as topics to present
- Look-up items are only named here; the aid itself is built in Job Aid Template
- The inventory names content owners by role and never rates the quality of an expert
- Claude sorts and flags; the expert rules on every conflict and every cut, and an undated page is never treated as a source.

## Next
Run isd-review-plan (Review and Sign-Off Plan) to agree who signs what before anything is built.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
