---
name: telegram
description: Send Telegram notifications to the user. Three use cases — (1) loop-completion messages (short summary + PR links) when an implementation loop (feature-implementation, feature-implementation-agents, feature-implementation-light) finishes, (2) question/blocked messages whenever the loop must ask the user something or is blocked waiting for user input (ambiguous stack, decision needed, rejected step, unavailable agent), and (3) loop-back/iteration messages on EVERY loop-back to a previous step (bugs found, review below gate, CI red, rejected step). The send attempt is MANDATORY in all three cases; only the delivery is best-effort. Also use when the user explicitly asks to be notified on Telegram or to verify the bot setup.
---

# Telegram Notification Skill

One bot, three message types:

1. **Completion** (final step of an implementation loop) — summary + PR links.
2. **Question / blocked** (any time mid-loop) — the loop needs the user's answer before it can continue.
3. **Loop-back / iteration** (every loop-back to a previous step) — short progress alert so the user knows the loop is still working and why it went back.

All three sends are **MANDATORY attempts**: you MUST call `send.sh` before continuing (loop-back) or before waiting (question) or before declaring done (completion). Only the **delivery** is best-effort: a missing config or a failed send NEVER invalidates the completed work and NEVER blocks the loop.

## 1. Credentials

`send.sh` reads credentials in this order:
1. `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` environment variables
2. `~/.config/opencode/.telegram.env` (chmod 600), sourced by the script:

```bash
TELEGRAM_BOT_TOKEN=1234567890:AAEh...   # from @BotFather
TELEGRAM_CHAT_ID=-1004429805612         # channel/group/user chat id
```

**One-time setup**: create a bot with @BotFather (`/newbot`), add it as **administrator** of the target channel with the *Post messages* permission, post one message in the channel, then read the chat id from `curl https://api.telegram.org/bot<TOKEN>/getUpdates` (field `chat.id` — negative for channels). Write both values to `~/.config/opencode/.telegram.env` and verify with `send.sh --test`.

## 2. Sending

```bash
bash /Users/yohan/.config/opencode/skills/telegram/send.sh "<message>"
# setup verification:
bash /Users/yohan/.config/opencode/skills/telegram/send.sh --test
```

Exit 0 = sent (`"ok":true` from the Bot API). Exit 1 = missing credentials or API error. On failure: retry ONCE. Still failing → print a warning and continue (non-blocking).

**Plain text only** — Telegram auto-links URLs. Do NOT use Markdown/HTML parse modes (escaping issues).

## 3. Message composition

### Completion (final step of a loop)

```
✅ Loop terminée : <loop_id>
📋 <one-paragraph summary: what was implemented, on which stack/repo>
🧪 Gates : tests <N> pass · review <S>/10 · QA <bugs|no bugs>
🔗 PR : <PR URL> (one line per PR — ONLY if PRs were created in this loop)
📊 Rapport : <LOOP_DIR>/loop-report.html (only if the file exists)
```

- PR links: include ONLY if the loop included the PR step and PRs were created. No PRs → drop the line (summary only).
- Keep the whole message under ~1000 chars — it is a notification, not a report.

### Question / blocked (mid-loop)

```
❓ OpenCode attend ta réponse (loop <loop_id>)
<the question or the decision needed, 1-2 lines max>
<which session/repo to come back to>
```

Use this whenever the loop is about to stop and wait for user input: ambiguous/mixed stack detection, a user decision or confirmation, a rejected step, or a blocked step that requires the user (e.g. unavailable agent). NOT for progress updates — only when the loop genuinely cannot continue without the user. **Sending it is MANDATORY**: load the `telegram` skill and call `send.sh` BEFORE asking the question in the session. The only best-effort part is the delivery — if the send fails, still ask the question in the session.

### Loop-back / iteration (mid-loop, MANDATORY)

```
🔁 Loop <loop_id> — itération <N> (retour à l'étape <step>)
<one line: why — bugs found / review <S>/10 < gate / CI red / step rejected>
<one line: what is being redone now>
```

Send this on **EVERY loop-back to a previous step**, before redoing the step: bugs found by QA (loop back to implementation), code review below 8/10 or with criticals, failing tests/lint/Sonar/Trivy after a fix pass, CI red on the PR, a step rejected by the user or the gates. One message per loop-back iteration — the user must be able to follow the loop's progress remotely and interrupt it early if it is looping in the wrong direction.

## Agent rules

- **Non-blocking, always.** A notification failure (missing token, network, API error) is a warning, never a gate. Completed work stays valid; a question is still asked in the session even if the Telegram send fails.
- **The send attempt is MANDATORY for all three types.** Completion (once, at the final step), question/blocked (before every wait on the user), and loop-back (before redoing the step, on every iteration). Skipping the attempt because "it's best-effort" is a workflow violation — best-effort applies to delivery only.
- **No secrets in messages.** Never include tokens, API keys, or file contents beyond paths.
- **Plain text, short.** Notifications, not reports. Full details live in the session and in `<LOOP_DIR>/`.
- **One completion message per loop** — send once, at the final step. Question messages: every time the loop waits for the user. Loop-back messages: one per loop-back iteration.
