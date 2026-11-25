---
description: "Send a rich Telegram post to ANOTHER allowlisted chat; not for the current chat reply or plain reports."
---

# rich-post — Telegram rich messages via the bot

Send ONE message that mixes text, inline images, tables, headings, lists,
block quotes, collapsible blocks and formulas. This is `sendRichMessage`
(Bot API 10.1, June 2026), not an album.

## When NOT to use this

A report or an answer for the chat you are talking in is the plain reply of the
turn. The Outbox (`agent/lib/outbox.ts`) already routes a reply that needs
tables, task lists, `<details>` or block formulas into `sendRichMessage`, and
falls back to HTML if Bot API refuses it. Sending the same text with `iva post`
on top of that reply simply delivers it twice. Reach for this skill only when
the destination is a different allowlisted chat, or when the post needs inline
images and the owner asked for it there.

Album (sendMediaGroup) = up to 10 media, ONE caption, no text between images.
Rich message = up to 50 media, text/tables/blocks interleaved in a single
bubble. If the user wants "картинка в середине текста" or "таблица в посте" —
this skill.

## Quick start

`iva post` is the installed CLI command; run it from anywhere.

```bash
iva post --md-file /tmp/post.md
```

- Recipient: by default the message goes to `TELEGRAM_DIGEST_CHAT_ID` from
  `.env`. An explicit `--chat <id>` is accepted ONLY if the id is allowlisted
  (`TELEGRAM_ALLOWED_USER_IDS` + `TELEGRAM_DIGEST_CHAT_ID`) — the recipient of
  a report is the owner's setting, not the model's choice. Anything else is
  refused without sending.
- `--md` / `--md-file` — markdown content (`--md-file -` reads stdin).
- `--dry-run` — OFFLINE check: validates the markdown and image paths, prints
  the result; nothing is uploaded or sent. Always run this first.
- `--allow-upload` — see «Local images» below. Off by default.
- `--silent`, `--thread-id` — optional.
- Token: taken from the installation's `.env`. There is NO `--token` flag
  (argv is visible in the process list) — don't put the token on the command line.

## Local images — read before using

Telegram accepts ONLY public URLs for rich-message media (`attach://` and
multipart upload fail with `RICH_MESSAGE_PHOTO_URL_INVALID`). So a local image
referenced as `![](file:/abs/path "caption")` must first be uploaded to a
public host. The command uses **tmpfiles.org — an anonymous PUBLIC host**:
anyone with the link can open the file while it lives there.

Because of that:

- uploads happen only with the explicit `--allow-upload` flag; without it,
  local images are an error (and `--dry-run` merely lists what WOULD be
  uploaded);
- only real media passes the gate: regular files with an image/video/audio
  extension (jpg/png/gif/webp/mp4/webm/mov/mp3/ogg/m4a), located inside the
  repo or the data dir, with no hidden dot-segment in the path. `.env`, OAuth
  json, logs, vault `.md` and any other text file are refused even with
  `--allow-upload` — a report must not be able to exfiltrate server files;
- never reference private documents as images anyway. If in doubt — don't
  upload; send text instead.

Telegram fetches and caches the media at send time, so the temp URL expiring
afterwards is fine.

## Workflow

1. **Write content** in markdown (see syntax below) to a temp file.
2. **`--dry-run`** to verify layout and image paths (offline).
3. **Send** — to the default digest chat, or an allowlisted `--chat`. For
   images add `--allow-upload` consciously (see above). Confirm with the user
   before posting anywhere beyond the current conversation.

## Markdown syntax (rich_message.markdown)

The same markup as a rich reply — see the `rich-replies` skill for the full
reference (headings, tables, folds, footnotes, formulas, media, collages,
slideshows, maps, buttons). A post supports all of it; `callback_data` buttons
only make sense in a private chat with the bot.

## Limits

- 32768 UTF-8 chars total (incl. emoji alt text + formula source)
- 500 blocks (nested blocks, list items, table rows, quotes, details count)
- 16 levels of nesting
- 50 media attachments total (photos + videos + audio)
- 20 columns per table

## Gotchas (learned)

- Images need a **public URL**. `attach://` and multipart upload → 400
  `RICH_MESSAGE_PHOTO_URL_INVALID`.
- Use `rich_message.markdown` OR `rich_message.html`, exactly one.
- Channels/groups: the bot must be admin with permission to send media (and
  the target still has to be allowlisted).
- The host calls sendRichMessage on normal replies by default (`agent/lib/outbox.ts`,
  `needsRichMessage`), so tables and task lists in an ordinary answer already
  render; with `TELEGRAM_RICH_REPLIES=never` they stay on the HTML path, while
  `iva post` still sends rich. This command exists for the other chat, not for a
  nicer reply.
- `iva post` goes out through the same Outbox and the same outbound gate as every
  other message, so a leaked secret is redacted on the way. That is a safety net,
  not a licence: everything you post must be text you wrote in this turn, not a
  file dump or command output.
- Unlike a turn reply, a post has NO HTML fallback: if Bot API refuses the rich
  message, the command exits non-zero with the API error and nothing is sent. A
  post never lands half-rendered with its images dropped — fix the markdown (or
  the limits above) and run it again. Never report a post as sent on a failed run.

## Example

```bash
cat > /tmp/post.md <<'EOF'
# Заголовок отчёта

Вступительный абзац с **жирным** и [ссылкой](https://example.com).

Таблица:

| Метрика | Значение |
|:--------|--------:|
| Охват | 42k |

> цитата в конце
EOF
iva post --md-file /tmp/post.md --dry-run
iva post --md-file /tmp/post.md
```
