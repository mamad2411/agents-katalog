---
name: adopt-concern-response-log
description: Builds a log of the concerns raised about AI, with the substance of each checked on its merits, what changed and what did not and why, an owner and date for each commitment, and a shareable update with identifying details removed. Use for "run adopt-concern-response-log", "what happened to the concerns people raised", "close the loop on AI concerns", "you said we did log for AI", "respond to an anonymous AI concern", "track commitments from the AI feedback session", "update the team on their AI concerns", part of the Claude Guide for AI Adoption Pack by 90n.
---

# Concern Response Log

## When To Use
Concerns were collected in a session and nobody ever heard what happened to them. Use this when you hold a list of things people raised about AI, by any route, and owe them an answer. It answers: was each concern right, what did we do about it, and who has been told?

## When Not To Use
Do not use it for a serious allegation about a person: that goes to the appropriate human process, with restricted handling, and not into a shared log. For the recurring question about jobs, run AI and Jobs Answer. For input gathered as part of the rollout consultation, the ledger in Team Involvement Plan is the right place.

## Inputs
- The concerns as raised, with names and identifying details removed before you paste them.
- What was checked, what was decided and why, in the decision owner's own reasoning.
- Commitments already made, with owners and dates where they exist, who the update is for, and how small the teams are.
If you have none of this, I start from the raw list of concerns and mark the output as a first draft.

## Approach
The method is a plain ledger with no owner: heard, changed, declined, and why. It runs in two passes, in this order: check the claim on its merits, then follow through. A concern is neither stronger nor weaker because it arrived anonymously, bluntly or drafted with AI help. The failure this prevents: a pointed, unsigned note lands, the first hour goes on working out who wrote it, and the team learns that the question asked about a concern is "who" and never "is it true".

## Workflow
1. Ask up to three questions: what was raised and through which routes, what has been checked and decided so far, and who the update is for.
2. Write one row per concern: the substantive claim and its consequence for the work. Keep supplied evidence, unsupported assertions and unknowns in separate cells, so a strong claim is not sunk by a weak sentence beside it.
3. Check each claim on its merits. What needs verifying, and what would change the decision owner's position? I do not try to identify an author from style, logs or metadata. If asked to, I decline that part in one sentence and continue with the substance.
4. Record what changed, what stays the same and why, in the reasoning actually supplied. If the evidence was not enough, the row says what is unknown and how it will be checked. No kinder explanation is invented, and a decision made is not written up as a disagreement resolved.
5. Give each commitment an action, an owner, a date and an observable sign of completion. Owners and dates I suggest are marked "proposed" until agreed. An overdue commitment is shown as overdue with a revised date: a second listening exercise does not replace a promise already made.
6. Draft the shareable update with identifying details removed, and a route for correction or further evidence. Where a small team could work out who raised what, the update moves to a broader summary.
7. Set the check-in: did the original work issue improve, and was the response useful? More comments or more AI use are not proof of anything.

## Output Format
```markdown
# Concern Response Log
Covers: [session or period] | Decision owner: [role] | Log kept by: [role] | Last updated: [date]
## Concerns and what was found
| Ref | Claim and consequence for the work | Supplied evidence | Unsupported or unknown | What was checked | Finding |
|---|---|---|---|---|---|
| [C1] | [claim] | [evidence] | [assertion or gap] | [check, by which role] | [supported / partly / not supported / not yet known] |

## Response
| Ref | What changed | What stays the same, and why | Status |
|---|---|---|---|
| [C1] | [change, or none] | [actual reasoning] | [decided / interim / open] |

## Commitments
| Ref | Action | Owner | Date | Sign it is done | State |
|---|---|---|---|---|---|
| [C1] | [action] | [role; proposed or agreed] | [date; proposed or agreed] | [what anyone could observe] | [open / done / overdue, revised to date] |

## Update to share
[Short text for the team: what we heard, what changed, what did not and why, what happens next. No names, no detail that points to a person. How to correct us or add evidence: [route].]
Check-in: on [date], [role] asks whether the work issue improved and whether the response was useful.
## Decision
[Decision owner] confirms the findings, owners and dates by [date], and decides when and where the update is shared.
```

## Done When
- Every concern raised has a row, including the ones that were declined.
- Each finding rests on what was checked, not on how or by whom the concern arrived.
- Every commitment has an owner, a date and a sign of completion, with proposals marked as proposals.
- The shareable update contains no name and no identifying detail, and a check-in date is set.

## Quality Bar
- "Declined" always comes with the real reason, stated respectfully.
- No credibility ranking of who raised what, and no judgement of anyone's tone.
- An undecided concern gets an interim update, and nothing is marked done without evidence that it was done.
- The substance is checked and the author is never hunted; a named owner answers each concern.

## Next
Run adopt-ai-value-measures (AI Value Measures) to agree what "it worked" will mean before the pilot.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
