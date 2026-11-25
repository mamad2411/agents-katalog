---
name: linkedin-cold-reviver
description: Detect a going-cold lead and fire one completely new angle that lands value whether or not they reply. Use when a thread has gone quiet and a re-ask would only nag.
argument-hint: "[the thread that has gone quiet]"
---

# LinkedIn Cold Reviver

A dying thread does not get revived by chasing. It gets revived by a new gift. This skill spots the cooling, then writes one revival message that is itself a value bomb.

## Inputs
- The thread that has gone quiet (paste the full back-and-forth, with rough dates if you have them): $ARGUMENTS
- The brief (persona pains, offer, voice) loads automatically, so do not re-ask for context it already holds.

## Do this
1. Confirm it is actually cooling. Read the thread. Name the signal: a reply that trailed off, a "let me think", days of silence after warmth. If it is not cold yet, say so and stop.
2. Find a brand-new angle. Do not reopen the old question. Pick a different pain, a different proof, or a different artefact tied to their world. One angle, not three.
3. Build the value bomb. Write the message so the useful thing lands even if they never reply: a teardown, a specific number, a one-page resource, a stolen-with-pride tactic. They keep the value either way.
4. Write the standalone CTA. It must work with zero memory of the prior thread. It names the artefact, states the one-word reply cost ("Reply 'send' and it's yours"), and names the outcome they get from it.

## Output
- The revival message (the value bomb plus the standalone CTA), ready to read.
- A one-line note: why this angle is different from the one that went quiet.
- If they bite, hand the reply to /linkedin-reply-triager. Run /linkedin-humanizer on the draft before it ever sends.

## Rules
- Never just re-ask the old question. A nag is not a revival.
- The value must land even if they bin you. If the message only works on a reply, rewrite it.
- One new angle, not a pile of follow-ups. No "just bumping this", no "did you see my last message".
- Draft only. Claude drafts, you approve, nothing sends without you. Sending happens only through the opt-in CLI/MCP layer wired to your own LinkedIn session or provider key, hard-capped at 20 actions/day for new accounts.
- No em-dashes. No guaranteed-result promises.
