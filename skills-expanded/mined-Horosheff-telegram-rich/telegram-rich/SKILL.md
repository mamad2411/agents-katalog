---
name: telegram-rich
disable-model-invocation: true
description: >
  Format and (only on command) send a Telegram rich post via Bot API:
  long text, inline photos/video, collage, slideshow. No default channel.
  Token stays in the user's .env.
---

# Telegram Rich

Turn a ready draft into Telegram Bot API **10.1 / 10.2** rich message shape. Do not invent the article. Do not bake in a channel or a bot token.

## Methods

| Job | Method | Not this |
|-----|--------|----------|
| Long post, media inside the text, headings, table, in-post carousel | `sendRichMessage` | old `sendMessage` |
| Short note, up to 4096 chars, no article layout | `sendMessage` | rich |
| Classic swipe album, 2–10 files, no article around them | `sendMediaGroup` | `<tg-slideshow>` |

Default for a long post: **rich only**.

## Limits (rich)

- Text: 32_768 characters
- Blocks: 500
- Media files in one post: 50
- Nesting: 16
- Table columns: 20

## Payload

Put JSON next to the draft. Example shape:

```json
{
  "chat_id": "@your_channel",
  "method": "sendRichMessage",
  "disable_notification": false,
  "protect_content": false,
  "markdown": "",
  "media": [
    {"id": "cover", "type": "photo", "path": "media/cover.jpg"}
  ],
  "inline_keyboard": [
    [{"text": "Site", "url": "https://example.com"}]
  ]
}
```

`chat_id` must come from the user, their `.env` (`TELEGRAM_CHAT_ID`), or the payload. **Never** invent a channel. **Never** ship a real id in the repo.

Media `id`: 1–64 chars, `A-Za-z0-9_-`. In markdown: `![](tg://photo?id=cover)`.

## Rich markdown

Media is its **own paragraph**, not inside a sentence.

Allowed: `#`–`######`, paragraphs, `---`, `**bold**`, `*italic*`, `~~strike~~`, `==mark==`, `||spoiler||`, lists, task lists, `>`, tables, code, footnotes, `![](url "caption")`, `<tg-collage>`, `<tg-slideshow>`, `<details>`.

See `reference.md`.

## Script

```text
python scripts/publish.py --payload post.telegram.json --dry-run
python scripts/publish.py --payload post.telegram.json --send
```

After install the script lives at:

`%USERPROFILE%\.cursor\plugins\local\telegram-rich\scripts\publish.py`

`--send` only after the user said to publish. Token: `TELEGRAM_BOT_TOKEN` in `.env` or the environment. If missing, say so — do not ask them to paste the token into chat.

## Forbidden

- Hardcoded channels, bots, apps, or keys
- Logging the token
- Sending on the ideas / draft stage
- Replacing rich with an album “to keep it simple”
- Calling Instagram-carousel pipelines
