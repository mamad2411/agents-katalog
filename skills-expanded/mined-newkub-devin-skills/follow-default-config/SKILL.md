---
name: follow-default-config
description: Config convention — keep only overrides; never restate defaults (check via /check-types-definition)
argument-hint: "[config-path]"
related:
  - check-types-definition
  - update-config
  - update-devin-global-skills
  - deep-review-codebase
  - report
---

## Goal

Config files must stay short and easy to read — keep only values that override a tool's defaults; delete any value already equal to the default, so the config never restates what the tool does on its own

## Scope

Apply whenever writing/editing/auditing a config file (`uno.config.ts`, `vite.config.ts`, `biome.jsonc`, `tsconfig.json`, `Cargo.toml` profiles, `.eslintrc`, etc.) — before writing a new key, know whether its value differs from the default

## Execute

### 1. Enumerate Defaults

> Goal: know the real defaults of every option

1. Use `/check-types-definition` — inspect the tool's config type (`defineConfig` param type, `.d.ts`, schema) to get a `Name | Type | Options | Default | Comment` table
2. If the type definition has no default → read the tool's official docs/default source (`/learn-from-web`) — never guess a default
3. Build an `option → default` map for comparison

### 2. Strip Redundant Keys

> Goal: leave only overrides

1. Compare every key in the config against the default map — any key where `value === default` → remove it
2. Keys that differ from the default → keep (these are the config's real intent)
3. Comments that merely restate a default → remove too; comments explaining why an override exists → keep
4. Caution: some tools' defaults vary by env/preset — check `mode`/`env`/`preset` that shift the effective default before removing

### 3. Verify

> Goal: the remaining config behaves exactly as before

1. Run the tool's validate/build command after stripping
2. Behavior must be unchanged — if it changed, you removed a key that differed from the real effective default → revert that key

## Rules

- The default source must be authoritative — use `/check-types-definition` or official docs only; never guess
- Never remove a key that differs from the default, or a key the docs mark "recommended explicit" even when it equals the default
- Never strip a shared/base config if downstream merge logic requires that key
- Report all removed keys + reasons before committing
- When writing config guidance into a skill, the standard is enforced by `update-devin-global-skills` (`## Conventions → Templates` row `config-*`) — every skill that edits config must reference this skill

## Expected Outcome

- Config file keeps only overrides + intent comments — short, and clearly showing what the project actually customizes
- No cargo-culted boilerplate duplicating defaults
- Verification passes — behavior unchanged
