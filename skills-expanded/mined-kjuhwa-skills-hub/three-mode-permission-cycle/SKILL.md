---
name: three-mode-permission-cycle
description: Three-mode permission state (safe / ask / allow-all) cycled with SHIFT+TAB, with canonical UI names (explore/ask/execute), dual lookup, legacy aliases, and cross-process persistence.
category: agent-sdk
version: 1.0.0
version_origin: extracted
tags: [permissions, modes, agent-safety, ux]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/agent/mode-types.ts
imported_at: 2026-04-18T00:00:00Z
---

# Three-mode permission cycle

## When to use
- Agent that can read + write files / run commands, and the user wants quick escalation/de-escalation.
- Need a single keybinding (SHIFT+TAB) that rotates through safety levels, Vim-style.
- Want internal storage names to stay stable while UI copy evolves.

## How it works
1. **Two name spaces** for every mode - internal (`safe`, `ask`, `allow-all`) and canonical UI (`explore`, `ask`, `execute`). Map via bidirectional `Record`s.
2. A `PERMISSION_MODE_ORDER` array defines cycle order: `['safe', 'ask', 'allow-all']`. `cyclePermissionMode(cur)` returns the next.
3. `parsePermissionMode(str)` is the single ingest point - accepts both name spaces plus legacy aliases (`ask-to-edit`, `ask_to_edit`, `ask to edit`). Returns `null` for unknown.
4. Store only the internal mode on disk (session header, workspace config). Always format through `toCanonicalPermissionMode(mode)` for UI / logs.
5. Permission mode changes are an **event** (`PermissionModeChange`) fired on the automation bus - lets automations react ("when mode drops to safe, cancel in-flight tool calls").
6. Each mode drives a `PERMISSION_MODE_CONFIG[mode]` record: `description`, allowed tool prefixes, UI color, indicator icon - keep all mode-specific behaviour in that one table.

## Example
```ts
export type PermissionMode = 'safe' | 'ask' | 'allow-all';
export type PermissionModeCanonical = 'explore' | 'ask' | 'execute';

const TO_CANONICAL: Record<PermissionMode, PermissionModeCanonical> = {
  safe: 'explore', ask: 'ask', 'allow-all': 'execute',
};
const ORDER: PermissionMode[] = ['safe', 'ask', 'allow-all'];

export function cyclePermissionMode(cur: PermissionMode): PermissionMode {
  return ORDER[(ORDER.indexOf(cur) + 1) % ORDER.length];
}

export function parsePermissionMode(s: string): PermissionMode | null {
  const n = s.trim().toLowerCase();
  if (['safe','explore'].includes(n)) return 'safe';
  if (['ask','ask-to-edit','ask_to_edit','ask to edit'].includes(n)) return 'ask';
  if (['allow-all','execute'].includes(n)) return 'allow-all';
  return null;
}
```

## Gotchas
- Never let UI strings leak into storage - rename "Auto" to "Execute" freely, but `allow-all` on disk stays `allow-all` forever.
- Legacy alias parsing saves you from data migration pain when you rename modes.
- Cycle order is user-visible; if you add a fourth mode, inserting it in the middle changes everyone's muscle memory. Prefer appending or use chord keys for rare modes.
- Fire the mode-change event BEFORE you apply the new mode in tool callbacks, so automations (e.g. cancel-in-flight) see the old state.
