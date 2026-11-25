---
name: use-channels
description: >
  The project's outside conversations — today Telegram. Load it when the owner wants a bot, a
  notification "to my phone", a voice assistant in a messenger, or a way for people to ask the site
  questions from Telegram; and before you install a Telegram library or poll a bot from a route of your
  own. Two things decide everything and neither is visible from the code you can see: Telegram hands
  each update to exactly ONE reader, so a second poller does not add a feature, it silently eats half
  the messages — and that one reader is the channel service on the loopback, which sends, receives,
  transcribes voice and pushes every message into your own /api/telegram/hook. The bot is set up
  inside this project, at /{lang}/architect/telegram.
---

# use-channels

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

The door and the credential are in `use-data`; reached at `/service/channels/*` through `dataFetch`.

---

## 1. 🔒 One reader, and it is not you

Telegram gives each incoming update to whoever asks for it first, and to nobody else. Two pollers means
the messages split between them at random — the bot answers every other question and looks broken in a
way no log explains.

That is why one process owns the bot and everyone else asks IT over the loopback. **Never** install a
Telegram client in this app, never poll `getUpdates`, never register a webhook of your own for the
owner's bot. ✗ that trap already cost this project a day.

## 2. The whole surface — four routes, and all four are CONTROL

| Route | Gives you |
|---|---|
| `GET /status` | `configured` (a token is saved), `reachable` (Telegram recognises it), the bot's name, the linked `chatId`, `enabled` |
| `POST /telegram/config` | saves the token and settings; a NEW token drops the stored chat — it belongs to a different bot |
| `POST /telegram/link/start` | a one-time code plus a `deepLink` (`https://t.me/<bot>?start=<code>`) for the owner to press |
| `GET /telegram/link/poll?code=…` | whether that code has been used yet — the link flow's second half |

`status` is the honest first call: `configured: false` means the owner has not set a bot up, and that
is a **normal state**, not a fault to hide. Show it as "not connected", never as an error.

## 3. Three MORE routes exist — outbound and inbound (corrected 2026-08-25)

🪦 **This section used to say "impossible from your app: there is no outbound route", and that was
FALSE.** It described the service as it stood on 2026-08-23; sending was added afterwards and the text
was never corrected. ✗ Found by a guest agent reading the service's own source while the skill told him
the opposite — **a wrong law is more dangerous than a missing one**, and this one sat exactly where
somebody was building.

Verified in `services/channels/server.js` on 2026-08-25, by line:

| Route | Line | What it does |
|---|---|---|
| `POST /telegram/send` | 596 | sends text. `chatId` may be passed or falls back to the linked one; `422` if no token or no chat, `400` without text, `502` if Telegram refuses — with Telegram's own reason |
| `POST /telegram/sendFile` | 616 | sends bytes as base64. 🔒 **`kind` decides the METHOD**: `audio`→`sendVoice`, `image`→`sendPhoto`, otherwise `sendDocument`. A voice note sent as a photo loses its player; a document sent as a voice note is refused outright |
| `GET /telegram/inbox` | 651 | reads what arrived — `?after=<id>&limit=<n>`, returns `messages` and `lastId` for cursor polling |

🔒 **The token never leaves the service.** Your app hands over text or bytes; the credential stays on
`:3500`. That is the whole reason these routes exist rather than a Telegram client in your slot (§1).

## 3b. The four doors this project already owns (added 2026-09-01, step 77)

The setup screens are inside this repository now, and so are their doors. **Do not write a fifth one**
— call these, or add a section to the entry that already exists.

| Door | What it does |
|---|---|
| `GET /api/architect/channels` | the state: `available` (the service answered at all), then `configured`, `reachable`, `bot`, `chatId`, `enabled`, `tickSeconds` |
| `POST /api/architect/channels/telegram` | `{ token?, enabled?, tickSeconds? }` — straight through to the service, which validates the token format and clamps the schedule |
| `POST/GET /api/architect/channels/telegram/link` | the handshake: start it, then poll `?code=` |
| `GET /api/architect/channels/telegram/inbox` | `?after=&limit=` — what the bot heard, by cursor |

🔒 **All four check `ARCHITECT_LAYER_ROLES` themselves**, and all four are thin on purpose: the rules
live in the service, and a second copy of them here would diverge on the service's first change.
🔒 **`available: false` is a NORMAL state, not a fault** — on the owner's laptop the channel service is
not running at all. Say so in words; never render it as an error.

## 3a. 🔒 What is genuinely NOT there — check before you promise

These are gaps in the product, and a promise made over them is one the platform will not keep.

🪦 **TWO ROWS OF THIS TABLE WERE FALSE AND ARE REMOVED (2026-09-01, step 77-6).** They said there is
**no push into your project** and that **a voice note is dropped silently**. Both were checked against
`services/channels/server.js` line by line while writing the bot's own description page, and both are
the opposite of what the code does:

| What this file used to claim | What the service actually does |
|---|---|
| "no push into your project: no webhook, no queue" | `:376` — the service calls **your own door**, `POST /api/telegram/hook` (`:59`), with a shared secret (`:382`), the moment a message lands. While that wiring is in place `mode` defaults to `app`: **your project answers, the service does not** |
| "the voice note is dropped silently" | `:179` `voiceToText()` fetches the file and transcribes it; from then on it is indistinguishable from typing. `/status` reports `voice` (`:494`), which is `false` only when no OpenAI key is present |

🔒 **THIS IS THE SECOND TIME THIS EXACT SECTION LIED, AND THAT IS THE LESSON.** It already carries a
🪦 from 2026-08-25 for the same kind of error. A capability list written by hand goes stale the day the
platform ships something, and nothing wakes it up — so **read the service before you promise anything
from this table**, and treat every row as a claim with an address, not as a law.

✗ **A stale law is more dangerous than a missing one.** Both removed rows would have made you either
build a workaround for something that already works, or tell the owner the product cannot do what it
has been doing for weeks.

| The owner asks for | Today |
|---|---|
| "each of my clients gets their own chat" | **one LINKED chat, the owner's.** Other people can write to the bot and their messages do reach your project through the hook, but `chatId` in the config is a single field and stays the default recipient; nothing collects a list of other people |
| "mass mailing to my customer base" | **not this service.** One bot, one linked chat, one messenger. A loyalty service messaging thousands is a different product and usually an external gateway |
| "say it in our language" | the bot's own replies are English strings **inside the service**; your app cannot translate them |

**When one of these is asked for, the honest answer is not "I will build it".** Name exactly which is
missing, say it is a change in the channel service — platform, not your slot — and hand it over the way
`CLAUDE.md` describes. Then build everything around it that does not depend on it.

## 4. 🔒 Linking is a handshake, and the human moves first

The code is issued, the owner opens the deep link and presses Start in Telegram, and only then does the
chat id exist. Your page polls until it appears, with a visible "waiting" state — and the code expires,
so a page that waits forever is wrong.

🪦 **"YOU NEVER ASK A PERSON FOR A BOT TOKEN IN THE PRODUCT'S OWN FORM" — REPEALED 2026-09-01 (step
77).** That line stood here, and it was right while it stood: there was no place in the project built
to hold a credential, so the panel was the only honest answer.

🔒 **THE NEW CONDITION, AND IT IS A CONDITION, NOT A PERMISSION.** The token is now typed at
`/{lang}/architect/telegram?section=settings` — the architect layer, behind `ARCHITECT_LAYER_ROLES`,
which the door checks itself and not only the page. It leaves the browser by XHR and **passes straight
through to the channel service**: it is never written into a file of this repository, never logged,
never returned in a response. `/status` answers `configured: true|false` and never the value, so there
is nothing to mask and nothing to leak.

**What is still forbidden, and this half did not change:** a token field on a PUBLIC page, in a product
form, or behind any weaker gate than the architect layer; storing it in `APP-CONFIG`, `.env.local` or a
table of your own; printing it while debugging. A credential asked for in a place that was not built to
hold one is exactly the defect the old rule was protecting against — the place was built, the defect
was not repealed.

## 5. What the bot already is

A **mouth for the knowledge base**: a question in Telegram is passed to the graph (`use-agentic-rag`)
and the answer is repeated back. When the base is switched off or empty it says so plainly rather than
inventing an answer.

So "let people ask our documents from Telegram" is mostly a matter of loading the documents, not of
writing a bot — and improving the ANSWERS means working on the knowledge base, not on the channel.

## 6. The shape is channel-agnostic on purpose

The service is written so that WhatsApp, email or a web widget become a second entry in the same config
rather than a second service. Another channel is a platform change — name it and hand it over
(`use-data` §5); do not grow a parallel messenger inside the app.

## 7. Before you call it done

1. `status` was read first, and the "not connected" path exists in the product, in the user's language.
2. Nothing in this app polls Telegram or holds the bot token.
3. The linking page shows waiting, success and expiry — the human is the slow part of that handshake.
4. Anything from §3 that the owner wanted was named out loud as missing, not quietly worked around.
5. If the answers are poor, you said so about the knowledge base — the channel only carries them.
