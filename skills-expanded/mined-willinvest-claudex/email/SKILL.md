---
name: email
description: Broadcast the current brainstorm question plus a short context snapshot to a configured panel by email (SEND-ONLY), so people can read it on their own device during a screen-shared meeting and reply by email or aloud. Use when the user runs /claudex:email, or asks to "email the panel", "send this question to the panel", or "broadcast this to the panel". Reads recipients from ~/.claude/claudex/panel.json. Does not collect replies and does not modify claudex:think.
license: MIT
---

# claudex:email — broadcast a brainstorm question to your panel

**Send-only.** Emails the *current* question + a short context snapshot to a panel defined in
`~/.claude/claudex/panel.json`, so people can read it on their own device during a
screen-shared meeting and respond by email or aloud. It does NOT collect, match, or summarize
replies, and does NOT change `claudex:think`.

Canonical invocation: `/claudex:email [filter]`. Replies land in the connected Gmail account
and are not monitored live.

## Step 1 — Parse panel (true fail-fast)

Read `~/.claude/claudex/panel.json`. If it is missing or does not parse, STOP and tell the
host to create/fix it. Recipients are parsed from `data.panel.members`; the members array is
nested under the top-level `panel` key. Minimal required shape:

```json
{
  "panel": {
    "members": [
      { "name": "Name", "email": "name@example.com", "role": "student", "include": true }
    ]
  }
}
```

If `panel.members` is missing or is not an array, treat it as a panel schema error and STOP
before drafting. This is the only hard stop before drafting — everything else still produces
a draft you can fall back to.

## Step 2 — Resolve recipients

Resolve recipients only from `data.panel.members` plus any validated ad-hoc email tokens.

- **No argument:** every member with `include: true`.
- **Argument contains a token with `@`:** strip surrounding angle brackets, commas,
  semicolons, and whitespace from each such token; lowercase the domain; then validate it
  against a conservative email regex such as `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$`.
  If any `@` token is not a valid email, STOP and list the rejected tokens. Valid ad-hoc
  emails are combined with any other (non-`@`) filter tokens.
- **Other tokens (case-insensitive):**
  - `professor`/`professors` → `role: professor`; `student`/`students` → `role: student`.
  - Name tokens (e.g. `florescu bozdog`) match against `name`. **Multiple tokens are OR** —
    `florescu bozdog` resolves to BOTH people, not one person matching both.
- NEVER select a member with `include: false` unless explicitly named in the argument.
- Each selected member from `panel.members` must have non-empty string `name`, `email`, and
  `role` fields plus a boolean `include` field. If any selected member fails this validation,
  STOP. If any selected member lacks a valid email, show which selected member is invalid.
- Deduplicate the final recipient list by normalized lowercased email before preview, send,
  and log. Show the unique recipient count.
- If zero recipients resolve, STOP and show what matched / was excluded.

## Step 3 — Assemble the draft (always, even if Gmail later turns out unavailable)

**Current-question rule (strict):** ignore the `/claudex:email` invocation text itself and any
confirmation prompts. Use the most recent ASSISTANT-posed brainstorm question shown to the
host plus a 2–4 line summary of the immediate discussion. If there has been a topic shift,
there is no active brainstorm question, or there is any doubt, STOP and ask the host to paste
the exact question. Do not guess.

**Allowlist (authoritative):** the subject, the body, the preview, and the logged question may
contain ONLY the current question text plus the short context snapshot. Include nothing else
from `panel.json` beyond actual recipient addresses (no `meeting.*`, no member
`title`/`expertise`, no member emails outside the final recipient addresses), and no tool
output, hidden reasoning, implementation/planning notes, local file paths, or credentials.
Sanitize the logged question the same way as the email draft.

- **Subject:** `[S.A.G.E.] <short question>` — single line, ≤ 80 chars, no newlines.
- **Body** (plain text, target ≤ ~250 words):
  1. Identification line: *"This is Hao Fu's brainstorm assistant for the S.A.G.E. meeting —
     sending the question we're on so you can follow along."*
  2. **Where we are:** 2–4 line snapshot.
  3. **Question:** the current question + its options if multiple-choice.
  4. Closing: *"Reply here or raise it on the call."*

## Step 4 — Gmail availability check

After the draft exists, confirm a Gmail send tool (e.g. `mcp__gmail__send_email`) is
available, and ensure `~/.claude/claudex/state/` exists (`mkdir -p`). If creating the state
directory fails, continue to preview/send but warn **"logging may fail"**.

If the email cannot be sent for any reason — tool unavailable, send fails, or send hangs —
present the fully-assembled draft (recipients, subject, body) under a **"Manual send fallback"**
heading and STOP.

## Step 5 — Preview & confirm (required)

If a Gmail account/profile identity tool is available, look up and display the actual
connected sender address in the preview. Otherwise show **"the connected Gmail account
(confirm it is the intended sender)"**. The expected account for this setup may be
`agentfao@gmail.com`, but never state it as verified fact without checking.

Show the host: recipients as a list with the unique recipient count + class (e.g. "7 unique
included panel members" or "2 unique professors (Florescu, Bozdog)"); the line **"All
recipients are in To: and will see each other."**; the connected Gmail account wording above;
and the exact subject + full body. Then ask a count-based confirm: **"Send to N <class> from
the connected Gmail account?"** Proceed only on an unambiguous affirmative. If the host's
reply adds conditions (for example, "yes, students only"), re-resolve recipients and
re-preview before sending. Declining aborts with no send and no state write (the dry-run
path).

## Step 6 — Send

Call the Gmail send tool once with all unique recipients in `to`, the subject, and the body.
If the send fails or hangs, follow the **Manual send fallback** rule in Step 4.

## Step 7 — Record

Append one line to `~/.claude/claudex/state/panel-sends.jsonl`. Log recipients as the array of
normalized email addresses, never display text like "7 included members". Set `sentId` from
the send result (`result.id`, else the stringified returned identifier), and include `threadId`
if the send result contains one:

```json
{"ts":"<ISO8601>","sentId":"<result.id or stringified returned identifier>","threadId":"<thread id if returned>","subject":"<subject>","question":"<sanitized question text>","recipients":["a@x","b@y"]}
```

If this append fails AFTER a successful send, report **"Sent but not recorded"** with the
subject and the returned id — not an outright failure.

## Step 8 — Report

Report `Sent` (plain ASCII, no emoji) and the returned id. Remind the host replies arrive in
the connected Gmail account and are not monitored live.

## Hard rules

1. **Send-only.** Never poll, match, or summarize replies here.
2. **Always preview + confirm** before sending to real people.
3. **Never leak:** follow the Step 3 allowlist for subject, body, preview, and log.
4. **Never touch `claudex:think`** or its gate.
