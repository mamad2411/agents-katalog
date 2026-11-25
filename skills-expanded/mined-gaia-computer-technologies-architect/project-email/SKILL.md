---
name: project-email
description: Drafts and replies to project correspondence (client, consultant, contractor, planning officer, design team) in the practice's own tone, keeping a clear written record of instructions, decisions, and information requested. Use when the architect wants to "draft an email", "reply to this", "chase the engineer", "push back politely", "confirm in writing", or turn a messy thread into a clear message. Flags any sentence that would commit the practice to scope, fee, programme, or a contractual position before it is sent. Hands formal contract letters to contract-admin-letter, construction queries to rfi, and difficult client conversations to client-pushback.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Project Email

Most of an architect's week is correspondence, and most project disputes are about what an email did or did not say. Write emails that are short, unambiguous, and safe to be read back later by someone who wants to hold you to them.

## When to use

- Drafting a new message to a client, consultant, contractor, supplier, or planning officer.
- Replying to a thread: answering questions, chasing information, confirming a decision.
- Confirming in writing something agreed verbally or in a meeting.
- Turning a long, tangled thread into one message that states where things stand.

## Input

- The thread or the point to make. Paste the thread so nothing is answered out of context.
- Who it is to, and the relationship (client, appointed consultant, contractor under a building contract, statutory body).
- What the architect wants to happen as a result: a decision, information, a date, an acknowledgement.
- The practice's tone: a sample email or two is better than a description. Default: plain, warm, professional, no filler.
- Any constraint: appointment scope, fee basis, current stage, contract form. If unknown and relevant, flag it.

## Process

1. **Find the ask.** One email, one main purpose. State it in the first two lines. If the thread has three unrelated issues, suggest three emails or numbered points.
2. **Answer what was asked.** List every question in the incoming message and make sure each is answered, deferred with a date, or declined. Missed questions are the commonest failure.
3. **Make requests specific.** What, from whom, by when, in what format. "Please send the updated structural GA in DWG and PDF by Friday 14 March so we can coordinate before the Stage 3 issue."
4. **Record, don't recall.** When confirming something, state it as a fact with a date: "As agreed at the design team meeting on 4 March (minute 3.2), ..." Reference drawings by number and revision.
5. **Run the commitment check.** Before output, scan the draft for anything that commits the practice to:
   - **Scope** — agreeing to do work outside the appointment ("we'll also look at the landscape").
   - **Fee** — implying work is included, or quoting a figure.
   - **Programme** — promising a date the architect does not control.
   - **Design responsibility** — accepting or passing responsibility for an element.
   - **Contractual position** — admitting delay, accepting a claim, instructing a contractor informally.
   Flag each one in a note above the draft with a safer alternative. Never silently soften or delete the architect's own words; offer the alternative.
6. **Match the tone.** Shorter is more professional. No "I hope this email finds you well", no "just circling back", no exclamation marks unless the practice uses them.
7. **Subject line.** Project code or name, topic, and action: "[P123] Kitchen layout — decision needed by 14 Mar".

## Domain knowledge

- **Informal instructions to a contractor are risky.** On most building contracts only the named contract administrator (architect, employer's agent, project manager) can instruct, and instructions often must be in writing in a set form. If an email reads like an instruction to a contractor, flag it and hand to `contract-admin-letter`.
- **Client emails are often the record of the brief.** Confirm changes to brief, budget, or programme back to the client in writing, so the change is dated.
- **Consultants work to their own appointments.** Asking an engineer for "a quick check" may be outside their scope; say what you need and ask them to confirm it is covered.
- **Planning officers and statutory bodies:** factual, courteous, referenced to the application number; no argument by email that belongs in a formal submission.
- **"Without prejudice"** has specific legal meaning in some jurisdictions; never add it unless the architect asks and understands it.

## Output format

```
COMMITMENT CHECK
- [quoted phrase] → commits to [scope/fee/programme/responsibility/contract]. Safer: "[alternative]"
(or: No commitments found.)

UNANSWERED FROM THE THREAD
- [question that the draft does not yet answer] (or: None.)

SUBJECT: [ ]

[Email body]

[Sign-off as the practice signs]
```

Keep the body short: most project emails fit in under 150 words. If it needs to be longer, use numbered points.

## What you don't do

- Don't send anything. You draft; the architect sends.
- Don't invent facts, dates, drawing numbers, or what someone said. Use placeholders like [date] and list them.
- Don't make or accept contractual positions on the architect's behalf. Flag them.
- Don't give legal advice or interpret the appointment or contract. Suggest checking it.
- Don't pad with pleasantries, and don't use emojis.
