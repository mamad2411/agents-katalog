---
name: watch-ts
description: Start the background TypeScript watcher (tsc -b --watch) for this session — streams type errors into the chat as they appear. Invoke when actively editing TS and wanting CI-stricter type errors surfaced live; the watcher is opt-in because a monorepo tsc -b --watch is resource-heavy.
---

The `tsc-watch` background monitor is registered lazily against this skill: invoking
`/watch-ts` is what starts it. Nothing else to do — confirm to the user that the watcher
is now running and that TypeScript build errors will stream into the conversation.

If the current directory has no `tsconfig.json` / `tsconfig.base.json` (iOS, Android,
infra repos), tell the user the watcher has nothing to watch here and will stay idle.
