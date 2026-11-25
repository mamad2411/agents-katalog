---
name: linkedin-first-dm
description: Write the first DM under 150 characters once a connection is accepted, two variants, value-first and asking for nothing. Use right after a target accepts your request.
argument-hint: "[accepted target + the hook that connected you]"
---

# LinkedIn First DM

The accept is not the win, the conversation is. This skill writes the opener that earns a reply without asking for anything.

## Inputs
- The accepted target and the hook that connected you (a post, a comment thread, a mutual, a shared signal): $ARGUMENTS
- The brief (persona tone, pains, offer) loads automatically.

## Do this
Write two first-DM variants so the operator can pick:
1. Variant A - value-first. Reference the real hook, give one genuine, specific observation about their world, then end on an open question.
2. Variant B - genuinely curious. Lead with curiosity about something specific to them, no observation needed, then end on a different open question.
Both must be UNDER 150 characters. Count every character. Ask for nothing: no call, no offer, no link, no pitch. End each on an open question they would actually want to answer.

## Output
Variant A and Variant B, each labelled with its exact character count. After both, a one-line note: stop-on-reply (do not send a follow-up until they reply).
If the operator wants the message smoothed before sending, run /linkedin-humanizer on the draft. When replies land, hand them to /linkedin-reply-triager.

## Rules
- Under 150 characters, counted and shown. If over, cut and recount.
- No ask, no pitch, no link. Value or curiosity only.
- Every variant ends on an open question about their world.
- No em-dashes, no exclamation marks, no "hope you're well", no "I came across your profile".
- Reads like a text from a peer, references one real, specific hook.
- Draft only. Claude drafts, the operator approves. Nothing is sent without explicit approval, and sending happens only through the connected CLI/MCP layer wired to your own LinkedIn session or a provider key, hard-capped at 20 actions per day for new accounts.
