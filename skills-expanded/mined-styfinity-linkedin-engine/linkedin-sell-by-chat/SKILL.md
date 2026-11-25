---
name: linkedin-sell-by-chat
description: Draft the single next message in the 6-stage warm-to-booked chat framework, gating the offer behind a confirmed problem and the calendar link behind a yes. Use when you have a live LinkedIn conversation and need to know what to say next.
argument-hint: "[paste the thread so far]"
---

# LinkedIn Sell By Chat

The hero outreach skill. Selling on LinkedIn is a six-stage conversation, not a pitch. This skill reads where the thread actually is and drafts only the next message, so you never run ahead of the buyer.

## Inputs
- The conversation so far, pasted in full, plus the offer: $ARGUMENTS
- The brief (offer, pains, voice profile) loads automatically.

## Do this
1. Read the thread and identify which of the six stages it is at right now. The six stages:
   1. Open on their world, not your offer. A genuine, specific opener about them.
   2. One real insight that earns the reply. Useful on its own, no ask attached.
   3. Qualify the problem, message one: confirm the problem actually exists for them.
   4. Qualify the problem, message two: confirm the problem actually hurts.
   5. Introduce the offer, ONLY after they have confirmed the problem exists.
   6. Send the calendar link, ONLY after they say yes to a call.
2. Draft only the next single message for the stage they are at. One message, not a sequence.
3. Never skip a stage. Never pitch before the problem is confirmed (stages 3 and 4). Never send the link before a clear yes (stage 6).
4. If the thread is ambiguous, name the most likely stage, say why, and draft for that one.

## Output
- The next message, ready to copy.
- The stage it belongs to (1 to 6).
- What a yes vs a no looks like at this stage, so the user knows whether to advance or hold.

## Rules
- One message at a time. Never draft ahead of the buyer.
- Gate the offer behind problem-confirmation, and the link behind an explicit yes.
- Once they say yes, stop selling and book. Hand to /linkedin-booking-closer.
- Run /linkedin-humanizer on the draft if it reads stiff.
- Draft only. Claude drafts, the operator approves and sends. Sending happens only through the connected CLI/MCP layer, wired to your own LinkedIn session or provider key, hard-capped at 20 actions per day for new accounts.
- No em-dashes. No guaranteed-result or "10x in a week" promises.
