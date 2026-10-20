---
description: Capture a meeting or inbound touch from a named person. Say "capture this", "log this", "I had a call with <name>", "I spoke to <name>", "I got a reply from <name>", "heard back from <name>", "they replied", or "<name> responded" (or run /capture-meeting <name>). Routes a transcript or brain dump into brain/log.md + context/clients.md + open commitments. Also fires on phrases that name a new prospect: "add a client", "add a customer", "new lead", "new prospect" - capture intent without a meeting still updates context/clients.md.
argument-hint: <person or meeting name>
---

# Capture meeting

You just finished a meeting. This command routes the raw input (transcript, file path, or brain dump) into the right Founder OS files so nothing leaks.

Argument: `$ARGUMENTS` (the person or meeting name).

## Procedure (in order)

1. If `$ARGUMENTS` is empty, reply: `Which meeting? Re-run as /capture-meeting <name>.` and stop.

2. Ask the founder, as a single message, nothing else:

   ```
   Capture mode for <name>. Paste one of:
   - Full transcript text
   - A file path to a transcript
   - A brain dump of what happened (voice-to-text is fine)

   Also tell me: is this person already in context/clients.md? (yes / no / unsure)
   ```

3. Wait for the reply. Accept any of the three input forms.

4. Read `context/clients.md`. If the person exists, note their current row. If not, you will create one.

4.5. **Name pass (mandatory on transcript input).** Dictation and meeting recorders mangle proper nouns. Before extracting meaning, read `context/names.md` (the names glossary) if it exists and check every person, company, and product name in the input:
   - A name matching a glossary entry or a listed mishearing: use the canonical spelling.
   - A name matching nothing: keep it as heard, marked `(sp?)`, and ask about all unknowns in one batch before writing to any file. Never guess a fuller identity for an unmatched name, and never overwrite an existing person's record on a near-match - a heard name that is close to two known people is a question, not a pick.
   - Append every correction the founder makes to the glossary's mishearings column.
   Numbers, prices, and dates you are unsure of stay as captured, marked - never silently "fixed".

5. Parse the input for:
   - **Key decisions made** (things settled or ruled out)
   - **Commitments the founder made** (things they owe, verbs like "I'll send / share / do / book")
   - **Commitments the other party made** (things they owe)
   - **Next step** (what happens after this meeting)
   - **Pain surfaced** (what they named as broken)
   - **Signal quality** (did something ICP-worthy surface)

**Private-tag filter (mandatory before any write).** Before persisting anything to a file, scan the source text for `<private>...</private>` blocks (case-insensitive). Remove every matched block (including the tags) from the text before writing. If the entire input is wrapped in `<private>`, write nothing and report "skipped - content was tagged private."

6. Produce four updates:

   **a. Append to `brain/log.md`** (at the top, below the header - newest on top). Format:

   ```
   ### YYYY-MM-DD (meeting capture: <name>) · #acted [S] #xref:context/clients.md

   **Meeting with <name>. Source: <transcript|brain dump>.**

   - Key decisions: <bullets>
   - Founder committed to: <bullets>
   - They committed to: <bullets>
   - Next step: <one line>
   - Pain surfaced: <one line>
   - ICP signal: <one line or "none">

   M/S/D: [S] for the meeting capture.
   ```

   Use `#acted [S]` if the meeting was a prospect/client touch. Use `[D]` if it was infrastructure or internal.

   **b. Update or create row in `context/clients.md`.** Find the existing row OR create one under the right section (Pipeline, Past Clients, etc). Fields: stage, last contact (today), next step, response state if applicable, pain (if surfaced), ICP fit signal. Leave fields blank rather than scaffolding empty strings.

   **c. Commitments.** If the founder committed to anything with a clear deadline or trigger, append each as a bullet to `context/decisions.md` under Pending (format: Context / Options / Stakes / Deadline / Blocking / Notes). If it is not a decision but a task, say: "This is a task, not a decision; add it to priorities.md manually or confirm and I will."

   **d. Flags.** If the founder said something defensive, avoidant, or a pattern that matches anything in `brain/patterns.md`, add one line to `brain/flags.md` with the pattern name.

7. After all writes succeed, report in under 120 words:

   ```
   Meeting captured.
   - brain/log.md: <1 line summary>
   - context/clients.md: <row created|row updated|no change>
   - context/decisions.md: <N commitments logged as Pending, or "none to log">
   - brain/flags.md: <flag added: "<name>" | no flag>
   Next step: <the one-line next step identified above>
   ```

## Rules

- Read files before writing. Never blind-append.
- No em dashes or en dashes. Hyphens only with spaces.
- Do not invent commitments the founder did not make. If unclear, ask.
- Do not publish anything. Internal capture only.
- If a transcript is at a path, read it with the Read tool before routing.
- If it is a voice-to-text brain dump (rambling, tangential), accept the shape and extract intent. Do not ask the founder to be more structured.
- This command works only inside a Founder OS install. If the `brain/` folder is missing, reply: `Founder OS not installed here. Say "set up Founder OS" first.`
