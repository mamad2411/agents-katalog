---
name: draft-message
description: an AI agent has drafted a long/sensitive Telegram message and the user wants to review it BEFORE it is sent to the intended recipient. Sends to.
allowed-tools: Bash, Read, Grep, Glob
---

# Draft a Telegram Message (via Saved Messages)

Send a message to the user's **Saved Messages** so the user can review it, optionally edit it, then copy-paste it into the target chat's compose area before sending. Saved Messages is every Telegram account's built-in private chat with itself — it syncs across all clients automatically.

> **Why Saved Messages, not MTProto cloud drafts?** The official Telegram clients have a known unfixed race condition ([tdesktop#29111](https://github.com/telegramdesktop/tdesktop/issues/29111), closed "not planned") where the local empty-draft state silently overwrites cloud drafts pushed via `SaveDraftRequest` from another authorization. We observed this in practice: the server confirmed the draft, but the user's compose area stayed empty. Saved Messages bypasses this entirely — full HTML formatting is preserved, and Telegram's native copy-paste between compose areas preserves rich text across iOS, Android, Desktop, and Web.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## When To Use Draft vs. Send

| Situation                                                            | Use                                                  |
| -------------------------------------------------------------------- | ---------------------------------------------------- |
| Long or multi-paragraph message an agent composed autonomously       | **Draft** — let the human eyeball it before it lands |
| Message carries sensitive wording (hiring, firing, contract terms)   | **Draft** — one typo or wrong name is expensive      |
| Reply where tone matters (addressing a peer or an external party)    | **Draft** — AI-generated tone can be subtly off      |
| Short confirmations, status updates, routine responses               | **Send** — friction of drafting exceeds value        |
| Automated notifications, alerts, scheduled pings                     | **Send** — no human-in-the-loop needed               |
| Time-critical message where draft→review→send round-trip is too slow | **Send** — accept the risk                           |

Default when uncertain: **draft**. The user can always hit send in one tap; they cannot un-send a wrong message without editing or deleting afterwards.

## Preflight

Before drafting, verify the session is authorized (not just that the file exists):

```bash
bun "$SCRIPT" check-auth
```

If `EXPIRED`, run `/tlg:setup` first.

## Usage: tg-cli.ts draft

```bash
/usr/bin/env bash << 'DRAFT_EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# Draft a plain-text message labelled for a group
bun "$SCRIPT" draft -1003958083153 "Plain text draft goes here"

# Draft an HTML-formatted message
bun "$SCRIPT" draft --html -1003958083153 "<b>Bold heading</b>

Body text with <code>inline code</code> and a <a href=\"https://example.com\">link</a>."

# Draft labelled for a user
bun "$SCRIPT" draft @someusername "Quick question: does this framing land right?"
DRAFT_EOF
```

The `recipient` argument is used **only to label the draft's banner in Saved Messages** — it is not the destination. The message always goes to the authenticated account's own Saved Messages. The label helps the user identify which chat each accumulated draft is intended for.

## How It Appears in Saved Messages

Two messages are sent per draft:

1. **Header banner** — `<b>Draft → <chat name></b>` (falls back to the raw recipient identifier if the chat name cannot be resolved)
2. **Body** — the drafted content with the requested formatting

Keeping the header separate lets the user long-press only the body, tap **Copy**, and paste cleanly into the target chat's compose area without having to trim the banner.

## Workflow Pattern For AI Agents

1. Compose the message in your response
2. Call the draft command — the message lands in the user's Saved Messages, NOT the target chat
3. Tell the user: _"Draft for `<chat name>` saved to your Saved Messages. Open Saved Messages → long-press the body → Copy → paste into the target chat's compose area → review → send."_
4. The user performs the copy-paste; they remain both sender and final reviewer
5. If edits are needed, they happen in the target chat's compose area before sending

Drafts are **your reviewer safety net** — a deliberate pause between AI authorship and human publication.

## Parameters

| Parameter      | Type       | Description                                                            |
| -------------- | ---------- | ---------------------------------------------------------------------- |
| recipient      | string/int | Target chat ID/username — used only to label the Saved Messages banner |
| message        | string     | Draft text (required)                                                  |
| `--html`       | flag       | Parse message as HTML (bold/code/links)                                |
| `-p/--profile` | string     | Account profile (`eon` default)                                        |

## Behavior Details

- **Drafts append, they do not replace.** Each `draft` call sends a new `(header, body)` pair to Saved Messages. Older drafts remain visible above — the user can mentally track which is latest by position.
- **Long drafts auto-split.** The body is auto-split at ~3900 plain chars per Telegram's 4096 hard limit. Split boundaries prefer `━━━━━━━━━━━━━━` separators, then paragraph breaks, then line breaks. Each continuation part is labelled `<i>(Part N/M)</i>`. See `send-message` SKILL.md "Auto-split for long messages" for the full algorithm.
- **Formatting is preserved end-to-end.** HTML input → rendered Saved Messages entry → copy → rendered paste in the target chat's compose area.
- **No cloud-draft race conditions.** Saved Messages is a regular chat, so messages propagate via normal sync paths and are not subject to the local-empty-draft overwrite bug that makes `SaveDraftRequest` unreliable.
- **Silent from the target chat's perspective.** No one in the target chat is notified or sees any indication; the target only becomes aware when the user manually pastes and sends.

## Anti-Patterns

| Anti-Pattern                                              | Why It Fails                                                                    |
| --------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Drafting when the message is short and boilerplate        | Wastes the user's time — they could send directly and edit in the compose area  |
| Drafting many messages in rapid succession                | Saved Messages becomes a wall of stale drafts; hard to tell which is current    |
| Using draft for time-critical alerts (downtime, outages)  | User may not open Saved Messages until hours later                              |
| Claiming a draft was "sent to the group"                  | Be explicit: "Draft saved to Saved Messages for your review" vs. "Message sent" |
| Forgetting to tell the user to paste into the target chat | The draft sits in Saved Messages forever if the user doesn't know the next step |

## Error Handling

| Error                    | Cause                   | Fix                                                                      |
| ------------------------ | ----------------------- | ------------------------------------------------------------------------ |
| `Cannot find any entity` | Bad username/chat ID    | Label falls back to raw identifier — draft still saves to Saved Messages |
| `Session expired`        | Session no longer valid | Run `/tlg:setup`                                                         |

## Relationship to Other TLG Skills

- **`send-message`** — use when no human review is needed; includes edit-vs-supplement discipline for already-sent messages
- **`draft-message`** (this) — use when human review IS needed before send
- **`search-messages`** — useful for checking existing chat context before drafting a reply

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the draft land in Saved Messages?** Confirm by asking the user to check their Saved Messages.
2. **Did the user paste into the target chat successfully?** If formatting broke on paste, report the specific client (iOS/Android/Desktop/Web) so the Behavior Details section can be updated with a client-specific caveat if a regression appears.
3. **Was draft the right choice vs. send?** If the user immediately copy-pasted and sent without edits, draft was overkill — consider sending directly next time for similar messages.

Only update this SKILL.md if the issue is real and reproducible.
