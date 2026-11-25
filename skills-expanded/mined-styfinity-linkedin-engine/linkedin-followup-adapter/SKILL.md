---
name: linkedin-followup-adapter
description: Write the next follow-up from where the conversation actually is, off the real state of the thread rather than a fixed timer. Use when a prospect has gone quiet and the next touch needs a new angle.
argument-hint: "[the thread so far + what actually happened last]"
---

# LinkedIn Follow-up Adapter

A follow-up is a new move, not a reminder. This skill reads the real state of the conversation and writes the next message off THAT, adding a fresh piece of value every time.

## Inputs
- The thread so far and what actually happened on the last touch (they replied and went quiet, they opened a loop, they raised an objection, they ghosted after a yes): $ARGUMENTS
- The brief (persona tone, pains, offer) loads automatically.

## Do this
1. Read where the conversation actually is. Name the real state in one line: warm-but-busy, half-objection, interest-without-action, or genuine silence. Write off that, not a calendar.
2. Pick a new angle, different from the last touch. If the last message asked a question, this one gives. If the last gave value, this one references a signal or a result.
3. Add one new piece of value: a relevant observation, a useful resource, a specific result a client or operator saw, a single sharp question. Never restate the prior ask.
4. Write the message short and human. Reads like a peer continuing a real thread.
5. If their reply signals heat, hand it to /linkedin-reply-triager instead of sending another nudge. Run /linkedin-humanizer on the draft before it ships.

## Output
- The next message, labelled clearly.
- The angle it takes and the conversation state it answers, one line.
- When to send it, expressed relative to the last touch, not a fixed date.

## Rules
- State-driven, never timer-driven. The thread tells you when and what, not the clock.
- New angle and new value on every touch. If you cannot add value, do not send.
- Banned phrase: "just following up" (and its cousins "bumping this", "circling back", "checking in").
- No em-dashes. No "hope you're well".
- Draft only. Claude drafts, the operator approves. Sending runs through the connected CLI/MCP layer on the operator's own session or provider key, shows the draft first, and is capped at 20 actions per day for new accounts.
