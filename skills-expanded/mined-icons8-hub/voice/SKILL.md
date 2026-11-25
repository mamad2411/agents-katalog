---
name: voice
description: How to write text that goes out in the owner's name (a chat, mail, a comment). Use when you draft or send a message to a person as the owner, they ask to write "as I would", or they tell you to remember or forget a point of how you write for them.
---
# Writing in the owner's name
- Before drafting, read the latest messages of that chat: a required step. Load the chat tool's schema if it is not
  loaded (Teams: `list-chat-messages`, no field filters; Telegram: the dialog history). Take them into account: no
  second greeting inside a live conversation, do not re-ask what was answered.
- The owner's words — in their own wording, not retold. Their style is in `$HUB_STATE_DIR/owner-voice.md`, if it exists;
  no file — neutral, short, in the language of the chat.
- Add a line to that file only when the owner says "remember" or "always" about the style, with their words; a correction
  of one message ("shorter here") is not a line. "Forget X" — delete that line. At most 20 lines.
- The hub skill's rules stay: the addressee from `hub contacts find`, the owner's yes for outside sending, `hub wait` after.
