---
name: consult-the-expert
description: Drafts a casual, context-rich message to consult a more experienced developer about a technical problem, decision, or blocker. Use when the user wants help framing a question for a senior teammate, mentor, or domain expert who has zero context on the project being worked on.
metadata:
  author: https://github.com/Jei-sKappa
  version: 1.1.0
---

# Consult the Expert

Transform a raw problem description into a ready-to-send message that gives a zero-context expert enough background to actually help — without burying them in noise.

## When to use

The user is stuck on a technical problem, weighing a decision, or hitting a blocker, and wants to ping someone more experienced for input. The recipient is a peer or senior — not a stranger, not a support channel — so the message stays direct and conversational.

## Tone

- Casual, direct, peer-to-peer — assume they saw each other earlier today
- No greetings, sign-offs, or email-style formality
- Natural openers are fine and often clearest: "I have a problem with…", "I'm stuck on…", "I'm facing an issue where…"

## Structure (in this order)

1. **What the project is** — one or two sentences so the rest of the message makes sense
2. **The relevant component or area** — where in the project the issue lives
3. **The problem itself** — what's happening, what's expected, or what decision is being weighed
4. **What's been tried or considered** — including others' suggestions and the user's current leaning, with reasoning
5. **The specific ask** — a clear question, not a vague "thoughts?"

## Guidelines

- Prioritize clarity and completeness over brevity. Length is whatever the content needs — no padding, no aggressive trimming. An expert with zero project context needs real context to give useful input.
- Don't lead with the question before establishing what the project is — that's disorienting.
- Strip background that isn't load-bearing; keep anything the reader needs to follow the reasoning.
- Show respect for the expert's time by demonstrating the user has already thought about it — what they tried, what they ruled out, where they're leaning.
- Include a short `Stack:` line (one line, comma-separated) only if the problem is stack-specific. Skip it for abstract, architectural, or language-agnostic problems where it would just be noise.

## Output format

- A ready-to-send message (chat/DM style)
- Plain prose, short paragraphs, no headers, no bullet lists in the message itself
- No artificial length cap — let the content determine the length

## Workflow

1. Read the user's problem description.
2. Draft the message following the structure and guidelines above.
3. Pipe it straight into the clipboard script via stdin — no temp file:

   ```bash
   python3 scripts/copy-to-clipboard.py <<'__consult-the-expert-skill_EOF__'
   <drafted message here>
   __consult-the-expert-skill_EOF__
   ```

   Use a quoted heredoc (`<<'__consult-the-expert-skill_EOF__'`) so backticks, `$`, and other shell metacharacters in the message are preserved verbatim. The sentinel is deliberately unusual so it won't appear at the start of a line inside the message and prematurely close the heredoc.
4. Show the drafted message inline in chat so the user can review, and confirm the clipboard now holds it.

## When context is thin

Don't fabricate project details, stack choices, error messages, or attempted fixes. If the user hasn't given enough to ask a clear question, list the missing pieces back to them as bullets and wait for answers before drafting.
