---
description: Capture a pasted thread (WhatsApp, Telegram, email body, voice memo transcript) and route it into the brain layer. Say "log this reply", "I got a reply", "they responded", "here is the reply", "log this thread", or run /founder-os:log-reply. Writes one structured entry to brain/log.md per conversation. Proposes (never auto-writes) updates to context/clients.md and context/leads.md.
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep"]
---

# Log reply

Run the log-reply skill at `skills/log-reply/SKILL.md` end to end.

## Procedure

1. If `core/identity.md` does not exist, reply `Founder OS not set up here. Say "set up Founder OS" first.` and stop.
2. If `skills/log-reply/SKILL.md` is missing, reply `log-reply skill not found at skills/log-reply/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.
3. If `brain/log.md` is missing, reply `brain/log.md missing. Say "set up Founder OS" to build it.` and stop.
4. Follow the log-reply skill instructions exactly. The thread body (and source label, if provided) is whatever follows the command, or what the operator pastes when prompted in Step 1.
5. Write the structured entry to `brain/log.md` directly (auto-runnable).
6. Surface proposed updates to `context/clients.md` and `context/leads.md`. Wait for the operator's yes per `rules/approval-gates.md` before any of those edits land.
7. Output the under-120-word confirmation block defined in the skill.

## When to use

- A reply landed and you want it on disk and cross-referenced before you forget the context.
- A long WhatsApp or Telegram thread surfaced new commitments and you want them tracked.
- An email exchange with multiple turns needs to be condensed into one log entry per conversation.
- A voice memo transcript captures a phone call you took.

## When NOT to use

- You ran a meeting and have a transcript. Use `/founder-os:capture-meeting <name>` instead.
- You want to log a free-form thought, not a thread reply. Use `/founder-os:rant` or the brain-log skill directly.
- You want to draft a reply. Use the email-drafter skill.

## Examples

- `/founder-os:log-reply` then paste the WhatsApp export when prompted.
- `/founder-os:log-reply` then paste the email body and label it as `email`.
- "I got a reply from Sam, log this thread" - the natural-language trigger fires the same skill.

## Rules

- Read files before writing. Per `rules/operating-rules.md` and the read-before-destructive-write rule.
- No em dashes or en dashes. Hyphens only with spaces.
- No banned words per `rules/writing-style.md`.
- Do not guess the source format. Ask the operator to label.
- Do not invent commitments the participants did not make. Mirror their words.
- Proposed updates to `context/clients.md` and `context/leads.md` are proposed-only. The skill never auto-writes them. The operator must confirm each one. Per `rules/approval-gates.md`.
- This command works only inside a Founder OS install. If the `brain/` folder is missing, reply: `Founder OS not installed here. Say "set up Founder OS" first.`
