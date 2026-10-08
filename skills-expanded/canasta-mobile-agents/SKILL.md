# Agent notes

## Layout

- `src/` - shared TypeScript rules engine and AI (Vitest)
- `mobile/` - Expo React Native app
- `server/` - optional multiplayer
- `docs/` - gameplay, design, store listing
- `rules/` - example custom-rules JSON

## Commands

```bash
npm install
npm test
cd mobile && npm install && npx expo start
```

## Rules

- Do not invent stats or features.
- Keep gameplay logic in `src/` so it stays testable.
- Multiplayer is optional (`EXPO_PUBLIC_MULTIPLAYER_ENABLED`). Do not assume it is on.
- This repo is private. Do not treat it as open source.
- Do not commit `.env` files or `docs/internal/*` other than `docs/internal/README.md`.
