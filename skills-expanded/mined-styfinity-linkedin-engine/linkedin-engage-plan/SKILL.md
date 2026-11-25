---
name: linkedin-engage-plan
description: Design a multi-touch warming sequence for one target so they recognise you before you ever message them. Use when you have a specific person worth warming up before any pitch.
argument-hint: "[target + how warm they already are]"
---

# LinkedIn Engage Plan

Warming is recognition before the message. This skill lays out a conditional, stop-on-reply arc that earns familiarity first, so the eventual DM lands on a name they already know, never a cold pitch.

## Inputs
- The target (name, role, company) and how warm they already are (never seen you, follow each other, you've commented before, a mutual connection): $ARGUMENTS
- The brief (persona, pains, offer, voice) loads automatically.

## Do this
1. Read the starting warmth. Skip steps they're already past. A target who follows you starts further along than a stranger.
2. Lay out a day-by-day arc, each step conditional on the prior one landing and on no reply yet:
   - Day 1: react to a recent, relevant post of theirs. Specific, not the latest by default.
   - Day 2: leave a real value-add comment on their content. Hand the draft to /linkedin-comment-warmer.
   - Day 3: send a connection note that references the prior touch. Hand to /linkedin-connection-note.
   - Day 4+ (only after the connection is accepted): a first DM. Hand to /linkedin-first-dm only once the connection is accepted.
3. Set the stop conditions plainly: the moment they reply or engage back, stop the arc and move to a real conversation.
4. Note the gates: each step waits on the prior one. No connection note before a comment has landed; no DM before the connection is accepted.

## Output
A day-by-day arc table: day, action, the skill to run for that step, and the stop/advance condition. End with the single next touch to make today and what has to be true before the step after it.

## Rules
- Warm before you message. Recognition first, pitch never in the arc itself.
- Stop the moment they reply. Every step is conditional on no reply yet.
- This skill drafts and plans only. Nothing here sends automatically.
- Any sending happens through the connected CLI/MCP layer wired to your own LinkedIn session, drafts shown first, explicit approval required, hard-capped at 20 actions per day for new accounts.
- No em-dashes. No guaranteed-result or fast-growth promises.
