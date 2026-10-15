---
name: codex-adapter
description: Use when modifying or testing `packages/codex-plugin` or Codex `/compact` behavior.
user-invocable: false
metadata:
  internal: true
---

- Codex adapter (`packages/codex-plugin`, hint-only: nothing outside a Codex session can run `/compact`). Its sources are TypeScript that plain `node` type-strips, so they must stay erasable - no parameter properties, no enums. Codex rebuilds a hook's PATH from a shell snapshot and may have no `node` on it, so hooks go through `hooks/run.sh`, which is silent when it finds none. Judging is gated to the interactive TUI by the rollout's `originator`. The rollout transcript format is explicitly unstable upstream: `src/rollout.ts` never throws and degrades to the strictest floor. `scripts/validate.mjs` checks the package is loadable exactly as shipped. Snooze/dismiss are a known gap and follow-up: suppressing advice safely needs a reliable current-session identity that Codex gives neither the hook nor the CLI, so the CLI could only mutate the most recently written session record. Windows support is a possible follow-up: this ship is macOS and Linux only because the hooks run through POSIX `sh` and have no `commandWindows` entries.
