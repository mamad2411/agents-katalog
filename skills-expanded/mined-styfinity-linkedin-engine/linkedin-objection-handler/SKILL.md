---
name: linkedin-objection-handler
description: Read pushback from a prospect and write an answer-first reframe that addresses the real concern and advances toward a call. Use when a reply contains an objection (price, timing, trust, fit, "we already do this").
argument-hint: "[the objection + your honest answer to it]"
---

# LinkedIn Objection Handler

An objection is a question wearing a no. This skill answers it directly, reframes to the cost of staying still, and moves the thread one step toward a call.

## Inputs
- The objection as the prospect wrote it, plus your honest answer to it: $ARGUMENTS
- The brief (offer, pains, proof, voice profile) loads automatically.

## Do this
1. Name the real concern underneath the words. Most objections are one of five: price, timing, trust, fit, or "we already do this". Say which one this is and why.
2. Answer it first and directly. No dodging, no pivot before the answer lands. Use the operator's honest answer from the input as the spine.
3. Reframe to the cost of the status quo. What does doing nothing keep costing them, in their own metric (leads, pipeline, hours, missed revenue)?
4. Advance to a call. Offer a small, specific next step (a short call, a look at their numbers). Keep it conditional and low-pressure.
5. Match the tone to the thread's warmth: cold gets shorter and lighter, warm can carry more substance.

## Output
The reframe message, ready to paste, tier-matched to the thread's warmth. Then a one-line note stating the concern you actually addressed (price / timing / trust / fit / already-do-this).

## Rules
- Answer-first, always. Never evade the objection or change the subject before it is handled.
- Never discount to win. Price objections get reframed against the cost of the status quo, not knocked down.
- Advance to a call, do not hard-close in the text. Sending happens later, through the connected CLI/MCP layer, capped at 20 actions/day for new accounts.
- Draft only. Claude drafts, the operator approves, and only then sends.
- No em-dashes. Reads like a peer who respects the prospect's pushback.
- If the reply has run hot and is ready to book, hand it to /linkedin-reply-triager. Run /linkedin-humanizer on the draft before sending.
