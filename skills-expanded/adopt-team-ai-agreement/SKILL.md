---
name: adopt-team-ai-agreement
description: Drafts a session guide and a starting team AI agreement with agreed uses per task, a never-put-in list that starts from the organisation's rules, what checking means per type of work, whose name is on the work and a review date, for the team to write together. Use for "run adopt-team-ai-agreement", "team AI agreement", "team rules for using AI", "AI working agreement", "what is fine to use AI for", "what can we put into AI tools", "help teams agree how they use AI", "some people use AI for everything and some refuse", part of the Claude Guide for AI Adoption Pack by 90n.
---
# Team AI Agreement
## When To Use
Some people use AI for everything, some refuse, and nobody has said out loud what is fine. Use this when you equip several managers and teams and each team needs a session where it writes its own practice. It answers four questions for one team: what we use AI for, what never goes in, what checking means, and whose name is on the work.

## When Not To Use
If people do not know what the organisation allows, run AI Rules Explainer first: this agreement is the team's practice inside those rules and writes no policy. If you still need the wider list of tasks per role, run AI Use Case Map; for the full check behind one type of work, run AI Output Check.

## Inputs
- The organisation's AI rules, or where they live, and who owns them.
- The team's main tasks and how it uses AI today, honestly: what worked, what went wrong, who does not use it and why (no names needed). Plus any usage target from leadership, word for word.
If you have none of this, I start from the team's main tasks and mark the output as a first draft for the team session.

## Approach
The method is working agreements written by the team: set the stage, write the rules together, publish them where the team works, revisit them. The judgment behind it is that rules a team writes get followed and rules handed down get worked around, so Claude drafts a starting version for the session and never a finished agreement on the team's behalf. The failure it prevents: a polished report that nobody reviewed, with a wrong figure in it, sent under the name of someone who cannot say where the figure came from.

## Workflow
1. Ask three questions: which team is this and who runs its session, where are the organisation's AI rules, and is there a usage target (word for word)?
2. Build the session guide. Set the stage without blame: how the team uses AI today, including who does not and why. Sceptics speak early; they usually know where it fails.
3. Draft agreed uses per task from the team's real work: AI helps with, AI does not do, off limits. Mark every line as a proposal the team can strike. Declining to use AI for a task is a position the agreement records, with the reason.
4. Start the never-put-in list from the organisation's rules, each with its clause, then leave room for the team's additions. Where a rule is silent or a legal or data question comes up, the line reads "open, ask [policy owner]": check with a qualified adviser.
5. Set what checking means for each type of work, in one line, and whose name is on it: the person who ships it reviewed it, can explain it and owns it. Responsibility never passes to the tool.
6. Agree where the team shares what works and what failed, where the agreement is published, and a review date the team sets. A usage target is written down as given and discussed as a team. Then hand the draft to the person running the session, status line intact; each team gets its own draft, never a copy of another team's.

## Output Format
```markdown
# Team AI Agreement
Status: DRAFT for the team session, not agreed until the team says so | Team: [team] | Session: [date] | Run by: [manager or facilitator] | Organisation rules: [location, or "none yet"]
## Session guide
| Step | What the team does | Watch for |
|---|---|---|
| Set the stage | [how we use AI today, including who does not and why] | [no blame; sceptics speak early] |
| Write the rules | [edit each section below together] | [any line can be struck or rewritten] |
| Publish and revisit | [where it lives, when we look again] | [how absent colleagues add their view] |

## Agreed uses
| Task | AI helps with | AI does not do | Off limits | Positions recorded |
|---|---|---|---|---|
| [task] | [use] | [limit] | [yes / no / ask first] | [for example, "we do not use AI for this, because [reason]"] |

## Never put in
- [organisation rule, with its clause]
- [team addition, or an open question for [policy owner]: check with a qualified adviser]
## What checking means
| Type of work | What checking means | Whose name is on it |
|---|---|---|
| [type] | [check, in one line] | [the person who ships it: reviewed it, can explain it, owns it] |

## Sharing what works and what failed
Where: [meeting slot or shared space] | Published at: [where the team works]
Usage target, as given: [target or "none"]. Discussed as a team, never tracked per person.
## Decision
[team] agrees the final text in the session on [date]; [name] publishes it where the team works by [date]; the team reviews it on [review date].
```

## Done When
- The draft carries its status line and reaches the person running the session before the session.
- The never-put-in list starts from the organisation's rules, with clauses, and open questions have an owner.
- Every agreed use has a matching line under what checking means, and the team has set a review date.

## Quality Bar
- Uses and limits are specific to the team's tasks, and "whose name is on it" is explicit for every type of work.
- The agreement restates no law and writes no policy; legal and data points go to the policy owner: check with a qualified adviser.
- No list of who uses AI or how much, and no sign-off sheet by name used as compliance tracking.
- The team writes its own agreement; any usage target is discussed as a team and never tracked per person.

## Next
Run adopt-manager-follow-up (Manager Follow-Up Guide) to back up each session with what the manager does before and after.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
