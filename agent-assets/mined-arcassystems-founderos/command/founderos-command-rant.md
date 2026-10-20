---
description: Capture a raw rant immediately, then offer to route it. Say "I want to rant" or "let me dump something" (or run /founder-os:rant). The rant goes to brain/rants/ first; routing is optional after.
---

# Rant

The user just dropped a rant. Voice-to-text, long, tangential, conversational. The volume is the thinking.

**Capture first, qualify second.** The previous flow asked a qualifying question before writing - if the user walked away or sent an unrelated message, the rant was lost. That cost is unacceptable. The new flow writes the rant to disk immediately, then offers to route it.

## Procedure (in order)

### Step 1: Capture immediately

1. Read the user's rant text (whatever followed `/rant` or the natural-language trigger like "I want to rant" / "let me dump something").
2. Determine today's date in the user's timezone. Look up timezone from `core/identity.md`. If not set, default to local system time.
3. Determine the rants file path: `brain/rants/<YYYY-MM-DD>.md`.
4. If the file does not exist, create it with this header:

   ```markdown
   # Rants - <YYYY-MM-DD>
   ```

5. **Private-tag filter (mandatory before any write).** Scan the source text for `<private>...</private>` blocks (case-insensitive). Remove every matched block (including the tags) from the text before writing. If the entire input is wrapped in `<private>`, write nothing and report "skipped - content was tagged private."

6. Prepend a new entry to the file (newest on top, after the header):

   ```markdown
   ---
   captured: <ISO 8601 timestamp with timezone offset>
   processed: false
   mode: unknown
   ---

   <verbatim rant text>

   ---
   ```

7. Confirm in one line: `Captured to brain/rants/<YYYY-MM-DD>.md. <N> rants today, M unprocessed.` Do not summarise the rant content.

### Step 2: Offer routing (optional)

On a second line, ask:

> Want to act on it now? Say `decision`, `draft`, `plan`, or `log` - or ignore this and /dream will pick it up later.

The user may answer or may not. Either is fine. The rant is already on disk.

### Step 3: If the user routes, act

If the user replies with one of the route words (or natural language that maps to one), update the rant entry's `mode:` field in `brain/rants/<YYYY-MM-DD>.md` to the chosen route, then invoke the matching skill:

- `decision` -> invoke `decision-framework` with the rant as the decision context. Set `mode: decision`.
- `draft` -> choose the writing skill from the rant content: `linkedin-post` for post or content, `email-drafter` for email or follow-up, `proposal-writer` for proposal or scope, `client-update` for client status. If unclear, default to `email-drafter` when the rant names a lead or client follow-up; otherwise default to `linkedin-post`. Set `mode: draft`.
- `plan` -> invoke `priority-triage` if the rant is about what to do next, or `forcing-questions` if it is about starting a new initiative. Set `mode: plan`.
- `log` -> invoke `brain-log` to also write a referenced entry to `brain/log.md`. Set `mode: log`.
- `just capture` / unclear / unrelated reply -> leave `mode: unknown`. The rant stays in `brain/rants/` for `/dream` to process later.

## Rules

- Do not edit the rant text. Spelling errors, run-on sentences, voice-to-text artifacts stay.
- The capture write happens FIRST and unconditionally (subject to private-tag filter). Routing happens AFTER.
- Do not interview the user. The single follow-up question in Step 2 is the entire routing surface.
- Do not exceed two lines of output before the user replies. One confirmation line, one routing offer.
- If the user replies in plain English that does not match a route word, infer the route from the content. If still unclear, treat as "just capture" and stop.
