---
name: linkedin-connection-note
description: Write two LinkedIn connection notes under 200 characters, each opening on one real specific hook so the request is easy to accept. Use when sending a connection request to a named prospect.
argument-hint: "[target profile + how you found them / the real hook]"
---

# LinkedIn Connection Note

A connection note is not a pitch. It earns the accept by referencing one real, specific detail. This skill writes two short variants so the operator can pick.

## Inputs
- The target profile (name, role, company) and how you found them, plus the one real hook (a post they wrote, a comment, a mutual, a signal): $ARGUMENTS
- The brief (persona tone, pains, voice) loads automatically.

## Do this
1. Pull the single most specific real hook from the input. If there is no real hook, say so and ask for one. Do not invent it.
2. Write Variant A: a connection note that opens on that exact detail. Under 200 characters. No pitch.
3. Write Variant B: a different angle on the same hook, or a second real detail. Under 200 characters. No pitch.
4. Count the characters in each. If either is over 200, cut it down and recount.

## Output
Variant A and Variant B, each on its own line, with the exact character count in brackets after it (for example: [184 chars]). One line below: each is draft only, pick one, then approve before it goes out.

## Rules
- Under 200 characters, counted and shown. No exceptions.
- No pitch, no ask, no offer. The note buys the accept, nothing more.
- No "I came across your profile", no "hope you're well", no exclamation marks.
- No em-dashes. Use a comma, a period, or " - ".
- Reads like one peer messaging another about a real thing they noticed.
- Draft only. Claude drafts, the operator approves and sends.
- Sending happens only through the connected opt-in CLI/MCP layer wired to your own LinkedIn session or provider key, and is hard-capped at 20 actions per day on new accounts. This skill never sends.
