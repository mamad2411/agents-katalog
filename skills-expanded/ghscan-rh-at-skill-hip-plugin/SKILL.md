---
skill: plugin-creator
name: Plugin Creator (Codex)
perks: [scaffold, marketplace]
---

# plugin-creator — Plugin Creator (Codex)

Scaffold a Codex plugin directory with a required `.codex-plugin/plugin.json` (local-only),
or register that plugin in the repo-root `.agents/plugins/marketplace.json` (destructive — mutates a shared registry).

## What to look out for
Each tool emits one line of structured JSON (the audit + debug log) and writes its
artifacts under `record_store`. LOGS TO CHECK: that line + the named report + the executor run-ledger.
Plugin names are normalized to lower-case hyphen-case (`My Plugin` → `my-plugin`) and must be <= 64 chars.

## Perks
| perk | tool | nature |
|---|---|---|
| `scaffold` | `scaffold_plugin` | local-only / safe (creates `<plugin>/.codex-plugin/plugin.json` + optional `skills/ hooks/ scripts/ assets/ .mcp.json .app.json`) |
| `marketplace` | `register_marketplace` | destructive — creates/updates an entry in the shared repo-root `marketplace.json` (`--force` overwrites) |

The `scaffold` perk only writes inside a new plugin folder under `PLUGIN_PARENT`; it never touches the shared
registry. The `marketplace` perk mutates `<root>/.agents/plugins/marketplace.json` — a shared file whose entries
gate Codex UI availability and ordering — and is therefore declared `destructive: true`; the executor gates it accordingly.

## How to use it
Pick a perk (`scaffold` or `marketplace`), copy `ledger.json` → `task-ledger.json`, fill its vars + `record_store`,
then validate → compose → compile → oversight → executor.

> Localized from [openai/skills](https://github.com/openai/skills) `plugin-creator` — Apache-2.0 (see LICENSE.txt).
