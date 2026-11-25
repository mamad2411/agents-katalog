---
name: reality-check
description: Verification gate for status claims. Nothing gets called sent, replied, scheduled, shipped, merged, deployed, done, or closed until it has been checked against the live thing. Fires automatically before any status list, pipeline summary, weekly recap, standup, or follow-up plan reaches the user, and on demand when they say "/reality-check", "are you sure", "did I actually", "verify that", "check that before you tell me". Applies to outreach, deals, tickets, deploys, and anything a tracker, a note, or earlier in the session claims is done.
---

# /reality-check

Work runs on a picture in your head of where everything stands. When that picture is wrong, you chase someone who already replied, you never follow up with someone who is waiting on you, or you tell your team something shipped that is still sitting in a branch. Each one costs something real.

This is the gate that keeps the picture true.

## The rule

**A tracker is a lead. The live thing is proof.**

Notes, spreadsheets, CRM fields, ticket statuses, memory of last Tuesday, and anything the model said earlier in the session are all leads. They were true when written. They decay within days.

Before any of these words reach the user, open the actual artifact:

| Word | What counts as proof |
|---|---|
| sent | The message in the Sent folder, or the thread itself. Not a draft |
| replied / heard back | The reply, opened and read |
| no response / ghosted | The thread itself, showing nothing after the last outgoing message, and the date |
| scheduled | The event on the calendar |
| shipped / deployed / live | The change visible in production, or the deploy log showing it succeeded |
| merged | The PR showing merged, not approved |
| done / closed | The thing itself in its finished state, not the ticket status |
| followed up | The follow-up message in the thread |

## How to run it

1. **List every checkable claim** you are about to make. Anything with a status word in it.
2. **Open the live source for each one.** The thread, the calendar, the PR, the dashboard, the production page. Not a search result, the thing itself.
3. **Correct what turns out to be wrong,** and say plainly that it changed. "The tracker said sent. The thread shows a draft. It never went out."
4. **Label anything you could not verify.** Say which source you could not reach and why. Do not quietly drop it and do not guess around it.

Then deliver the list.

## Three traps

**Absence is not evidence.** An empty search does not prove nothing was sent. Search hides things: wrong account, archived, a different address, filtered to a label. Open the thread itself, or say "I could not find it, which is not the same as it not existing."

**A send is not a receipt.** Sent proves you sent. It does not prove they read it, and it never proves they will answer. The same goes for a merged PR: merged is not deployed.

**Old is not gone.** Something that went quiet five weeks ago is not automatically dead. Check its current state before writing it off, because "still open, no movement" and "closed" call for completely different moves.

## The honesty floor

- If you did not check it, say you did not check it. In the same sentence as the claim, not in a note at the bottom.
- Never say something is done because it should be done by now.
- Never infer that someone replied, or that something shipped, because time has passed.
- If verifying would take a tool or an account you do not have, say exactly that and tell the user the one thing they can click to settle it.

A short verified list beats a long confident one. Every time.

Pairs with [`no-bullshit`](../no-bullshit/SKILL.md): that one governs factual claims, this one governs status claims.
