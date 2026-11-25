---
name: linkedin-signal-stack
description: Pull five-plus real, checkable signals on one target and stack them into a 3-line signal brief a message can be built on. Use before writing any outreach so the message reads like 30 minutes of homework.
argument-hint: "[a target: profile or company]"
---

# LinkedIn Signal Stack

The lift in outreach is not the message, it is the signal stack underneath it. This skill does the homework: five-plus real signals per target, distilled to the one sharpest thing to open on.

## Inputs
- A target (profile and/or company) to research: $ARGUMENTS
- The brief (ICP, voice, offer, pains) loads automatically, so the signals are filtered for what matters to this operator.

## Do this
1. Gather signals that matter on this one target. Aim for five or more from across:
   - Recent funding, raise, or revenue milestone.
   - An exec move or a new hire (especially in growth, sales, or rev ops).
   - A phrase or priority lifted straight from a current job description they have open.
   - Their last post (the hook, the claim, the question they raised).
   - Any company news from the last 14 days (launch, press, partnership, hiring spike).
2. Verify each one. If a signal cannot be checked against a real, dated source, leave it out. No guessing, no inference dressed as fact.
3. Stack them into a 3-line signal brief: what is going on, why it is happening now, and the angle it opens.
4. Pick the single sharpest signal: the one a peer would notice and the target would feel seen by.

## Output
A signal brief per target, labelled clearly: the five-plus verified signals (each with its source), then the 3-line brief, then "Open on:" with the single sharpest signal. Hand this to a message-writing skill like /linkedin-first-dm or /linkedin-connection-note.

## Rules
- Only real, checkable signals. Every one carries its source. If it cannot be verified, it does not go in.
- Drafts research only. Pulling signals live (profiles, posts, company pages) needs the connected CLI/MCP layer wired to the operator's own session or a provider key; nothing is scraped by default.
- The operator approves what gets used. This skill never sends.
- No em-dashes. No filler. Operator-grade signals only.
