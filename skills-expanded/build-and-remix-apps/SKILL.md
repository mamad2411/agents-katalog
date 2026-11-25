---
name: build-and-remix-apps
description: Find live apps in CodeAgent Remix, and build a new app from the user's description — always showing the price and getting an explicit yes before the build starts.
---

# Build and remix apps

Use this when the user wants an app ("build me…", "make an app that…", "I need a tool for…") or asks whether one exists ("is there an app for…", "show me apps that…"), or asks about the apps they made.

## Find apps
1. Call `find_apps` with the user's words as the query. It needs no sign-in and shows cards with each app's poster, author and links.
2. Point the user at the card buttons: *Open in the feed* to use it, *Remix it* to make their own copy. Don't paste every link again in text; one short sentence is enough.
3. Nothing found → say so and offer to build it with `quote_app`.

## Build an app — price first, always
1. Call `quote_app` with a self-contained `description` of the app in the user's words (screens, features, who uses it). Pass `kind` only if the user said "phone app" or "web app".
2. The quote card shows "Working out the price…" while CodeAgent plans the app (about a minute). If you need the result in text, call `get_quote` with the `quote_id`; it returns `pricing`, `ready` or `failed`.
3. When the quote is `ready`, tell the user in one or two lines what will be built and the cost the quote shows in remixes (when `first_app_free` is true it uses none), and ask whether to go ahead. State the cost plainly; never present it as an offer or promotion.
4. Call `create_app` with the `quote_id` **only after the user clearly says yes** (or presses Confirm on the card). Never call it on your own initiative, never to "save time", and never with a quote the user hasn't seen.
5. `create_app` answers at once; the build takes a few minutes and the card shows its progress. If the user asks "is it ready?", call `get_build_status` with the `build_id`.
6. When it is done, give the app's link. Never say an app is ready before `get_build_status` (or the card) says `done`.

## Errors
- `INSUFFICIENT_BALANCE`: say how many remixes it needs and that they can add more in their CodeAgent account; once they have, call `create_app` again with the same `quote_id`. Do not pitch plans or paste purchase links.
- `INVALID_ARGUMENT` with a `next_action`: the quote is still pricing (`get_quote`), expired or already used (`quote_app` again), or the daily quote limit was reached. Repeat the message in plain words and follow the `next_action`.
- A refusal (content not allowed) comes back with its own message: repeat it plainly, don't try to rephrase the request around it.

## Their apps
Call `get_my_apps` for "what apps have I made?" or "what's building?". It lists ready apps and builds in progress with their links.
