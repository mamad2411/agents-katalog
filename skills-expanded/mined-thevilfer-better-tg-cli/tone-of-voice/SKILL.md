---
name: tone-of-voice
description: Writes Telegram messages in the user's own voice when they ask to write to someone without giving the exact text.
---

# Tone of Voice

Drafts messages that sound like the user.

## Compose

1. Read the style: `telegram plugin data get tone-of-voice style`.
2. Read the context: `telegram read <chat> -n 10`.
3. Write a draft in that style and show it to the user before sending.

```md
## Not a heading
```

## Notes

The user's exact text is always sent as is.
