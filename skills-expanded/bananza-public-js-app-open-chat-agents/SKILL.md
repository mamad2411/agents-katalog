# AGENTS.md for public/js/app/open-chat

## Purpose
- This folder contains the open-chat, message history, pagination, scroll restore, read receipt, and media playback runtime for the main app.
- Scripts load before `public/js/app.js` and expose factories through `window.BananzaApp.openChat`.

## Runtime Contract
- Modules publish under `window.BananzaApp.openChat`.
- Message rendering is invoked only through callbacks/actions from `app.js`.
- Do not create message rows or move message DOM rendering internals here.
- Do not move composer/send flow, reactions, media viewer, AI admin, folders, or chat-list logic into this folder.
- Do not create a second independent chat/message state. Use injected getters/setters and controllers as the single source of truth.
- Use plain browser JavaScript. No ES modules, imports, exports, or bundler-only code.

## Boundaries
- `pages.js` owns message page normalization, API page fetches, cache coordination, and asset warming.
- `read-receipts.js` owns member last-read state and read reconciliation.
- `scroll.js` owns scroll anchors, near-bottom checks, bottom button sync, and the scroll date indicator.
- `media-playback.js` owns playback resume/completed state and bridge-compatible helpers.
- `controller.js` owns open-chat orchestration, top/bottom pagination flags, current chat catch-up, and background message sync.
