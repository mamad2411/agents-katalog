---
name: migrate-to-addfox
version: 0.1.1
description: Migrate existing browser extensions from WXT, Plasmo, Extension.js/CRXJS, or vanilla setups to Addfox with incremental validation.
metadata:
  tags: addfox, migration, wxt, plasmo, extension-js, crxjs, browser-extension
---

# Migrate to Addfox

Use this skill when moving an existing extension codebase to Addfox.

## When to use

- Migrating from `wxt.config.ts` to `addfox.config.ts`
- Migrating from Plasmo `contents/`, `popup.tsx`, `options.tsx`
- Migrating from Vite + custom manifest workflows
- Porting entry layout into Addfox `app/` reserved folders

## Migration workflow

1. Keep behavior first, refactor later.
2. Create `addfox.config.ts` with minimal working manifest.
3. Map source entries to `app/background`, `app/content`, `app/popup`, `app/options`.
4. Run `addfox build` after each major step.
5. Validate extension loading in browser before optimization.

## Entry mapping (quick view)

| Source | Target in Addfox |
|---|---|
| background entry | `app/background/index.ts` |
| content script | `app/content/index.ts` |
| popup page | `app/popup/index.tsx` |
| options page | `app/options/index.tsx` |

## Follow-up skills

- `addfox-best-practices` for ongoing architecture and config decisions
- `addfox-debugging` for build/runtime failures after migration
- `addfox-testing` for regression test setup
