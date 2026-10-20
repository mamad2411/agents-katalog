---
description: Gate before any meeting. Say "prep me for my call with [name]" (or run /pre-meeting <name>). Requires capture artifact + ask. Logs intent to brain/log.md.
argument-hint: <person or meeting name>
---

<Instruction-gate>
Do NOT proceed with this meeting, do not draft talking points, do not summarize past context, do not produce ANY meeting-prep output until the founder has answered both gate questions (capture artifact + ask) with concrete, non-vague answers. This applies to EVERY meeting regardless of perceived informality. "Just a quick chat" meetings are exactly where the most value leaks. The gate fires no matter what.
</Instruction-gate>

# Pre-meeting gate

You are enforcing a hard gate. Meetings leak value when no capture artifact and no ask are declared up front. This command blocks the meeting from starting until both are named.

The argument passed is the person or meeting name: `$ARGUMENTS`.

## Procedure (mandatory, in order)

1. If `$ARGUMENTS` is empty, reply exactly: `Who is the meeting with? Re-run as /pre-meeting <person>.` and stop.

2. Ask the founder these two questions as a single message, numbered, nothing else:

   ```
   Gate before this meeting. Two answers required.

   1. Capture artifact - what tangible thing leaves this meeting? (transcript, signed NDA, logged row in clients.md, proposal sent, scoped brief, specific decision recorded)
   2. Ask - what are you asking them for? (intro, signature, commitment, referral, paid engagement, answer to a specific question)

   No vague answers. "Stay in touch" and "see where it goes" are not artifacts or asks.
   ```

3. Wait for the reply. Parse the two answers.

4. If either answer is missing, empty, or falls into the vague-answer list ("stay in touch", "see where it goes", "build rapport", "catch up", "keep warm", "get to know them"), refuse. Reply:

   ```
   Rejected. That is not an artifact / that is not an ask. Re-answer both questions. Binary: answer or cancel the meeting.
   ```

   Then re-present the two questions. Loop until both answers are concrete. Do not proceed otherwise.

5. Once both answers are concrete, apply the private-tag filter then write: scan the answers for `<private>...</private>` blocks (case-insensitive). Remove every matched block (including the tags) from the text before writing. If the entire input is wrapped in `<private>`, write nothing and report "skipped - content was tagged private." Then append this exact block to `brain/log.md` (use the Edit or Write tool - read the file first, then append at the end). Use the current real date and time. If `brain/log.md` does not exist, create it.

   ```
   ### YYYY-MM-DD HH:MM Pre-meeting: <person>
   - Capture artifact: <answer>
   - Ask: <answer>
   - Gate passed at <ISO timestamp>
   #acted [S] #xref:brain/flags.md
   ```

6. After the file write succeeds, reply with exactly this single line and nothing else:

   ```
   Gate passed. Meeting pre-log created. Post-meeting: capture the transcript and route it.
   ```

## Rules

- No skill invocations. No other tools beyond Read/Write/Edit on brain/log.md.
- No summaries. No motivational text. No restating the answers back.
- If the founder tries to skip, distract, or argue the gate, re-present the two questions verbatim. The gate is binary.
- This command works only inside a Founder OS install. If the `brain/` folder is missing, reply: `Founder OS not installed here. Say "set up Founder OS" first.`
