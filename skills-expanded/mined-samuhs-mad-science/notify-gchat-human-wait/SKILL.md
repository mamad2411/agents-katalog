---
name: notify-gchat-human-wait
description: "Send a Google Chat card through the webhook set in .env (GCHAT_WEBHOOK_URL) when the agent is waiting for human input, with the open question and the project name. Use to get pinged during long agent sessions, or when the user asks for Google Chat notifications."
---

# Send Google Chat notification — human waiting

Sends a text card to the Google Chat space configured in the repository when
work is blocked waiting for a human response, so the user notices without
returning to the terminal.

## When to use — decided by the repository policy

This skill only implements **how** to notify. The **when** (which skills and
conditions trigger it) is defined in the repository's `CLAUDE.md`, in the
section describing flow skills. If a flow skill is in progress and the turn is
waiting for human input, call this skill to notify. Otherwise, do not call it.

Do not notify for waiting on processing, script execution, or system actions —
only when a **human** needs to respond.

## How to call

From the repository root (where `.env` lives), run — `<skill-dir>` is the
directory containing this `SKILL.md` (it differs per agent and install method):

```bash
bash <skill-dir>/scripts/notify-gchat.sh \
  "the question awaiting a response" ["project name"] ["waiting"|"done"]
```

- Argument 2 is optional: without it, the script uses the `basename` of the
  repository root (the project folder name).
- Argument 3 is optional and selects the card header: `waiting` (default) for a
  question awaiting a human, `done` for a finished stage/experiment.

The bash script is a **thin wrapper**: it only reads `GCHAT_WEBHOOK_URL` from
`.env` and delegates to `scripts/notify_gchat.py`, which builds the payload.
Formatting lives in Python — not in bash — because the card is a `cardsV2`
payload (header + sections) and plain `text` payloads render as one
unformatted blob in Google Chat.

Tests for the payload builder (including the escaping regression):

```bash
python3 -m pytest <skill-dir>/scripts/tests -q
```

The message body is written in the card's **own markup — not HTML**:

| Markup | Renders as |
|---|---|
| `<b>…</b>` | bold |
| `<i>…</i>` | italics |
| `<u>…</u>` | underline |
| `<s>…</s>` | strikethrough |
| `<font color="#RRGGBB">…</font>` | colored text |
| `<a href="https://…">…</a>` | hyperlink (`http`/`https` only) |
| `<br>` | line break (a newline in the body becomes `<br>` on its own) |
| `<code>…</code>`, `<pre>…</pre>` | monospace |
| `• ` at line start | list item |

Two rules that matter:

- **Do not HTML-escape the body.** Write `<b>`, not `&lt;b&gt;` — Google Chat
  cards do not decode HTML entities, so an escaped tag is displayed literally.
  This is the bug the sanitizer was introduced to fix.
- **Anything outside the table is neutralized, never rendered as markup.** The
  script sanitizes the body (and escapes the project name/timestamp, which are
  data): supported tags are normalized, malformed ones are dropped. `&` is left
  alone, so `R&D` stays `R&D`.

Reference: [Format messages — Google Chat](https://developers.google.com/workspace/chat/format-messages).

Examples:

```bash
bash <skill-dir>/scripts/notify-gchat.sh \
  "Which ranking approach should I use for experiment E13?"
```

```bash
bash <skill-dir>/scripts/notify-gchat.sh \
  "Stage 1 completed.

<b>F1-macro:</b> 0.3233 ± 0.1150 (n=100)" "iris_dataset" "done"
```

The script always exits `0` (fail-silent): if the webhook is not configured or
the network fails, it logs a warning to stderr and **does not block** the work.

## Configuration (done by the user, once per repo)

The webhook URL lives in `.env` (not versioned). For repos following this pattern:

```bash
cp .env.example .env
# edit .env and add/complete the line:
#   GCHAT_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/<SPACE>/messages?key=<KEY>&token=<TOKEN>
```

The webhook is a **secret**: never print, log, or commit its value. It can post
messages to the space — treat it as a password.

## Safety rules

- **Never** include credentials, `.env`, tokens, or PII in the notification body.
- **Never** print the content (or value) of `GCHAT_WEBHOOK_URL` in any output.
- The message is truncated to 4000 characters to respect the Google Chat limit.