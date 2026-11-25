---
name: lore-plugins
description: Manages the LoreAI OpenCode plugin and gateway on this machine — install, update, upgrade, diagnose, and (when asked) the V1-to-V2 port of @loreai/opencode, which as of 0.40.0 still targets the V1 plugin API and does not run in V2. Use when the user asks you to adjust, fix, port, or check the loreai plugin; not for explaining what components do, and not for lore recall/history queries.
spec_hash: 4007f2a4d5fd
---

# Lore Plugins

Manage the LoreAI OpenCode plugin and its immediate ecosystem on this machine.
Use `lore-plugins-reference` for facts (packages, paths, port, component map)
and cite it rather than restating it. This skill owns the actions.

## Workflow

1. **Detect the API shape first.** Before any install or update, confirm
   whether the plugin targets V1 or V2. `@loreai/opencode` 0.40.0 imports
   `@opencode-ai/plugin` and exports the V1 function — it is V1-shape and will
   not run in OpenCode V2. State this result; do not trust the README's
   "OpenCode plugin" framing to mean V2.

1. **Respect the wiring.** The plugin is wired through the loreai topic's
   `dotfiles/apps/loreai/files/opencode/lore-plugin.jsonc`, pulled into the
   deployed `~/.config/opencode/opencode.jsonc` behind a stat-guard include.
   Plugin entries never go in `.chezmoidata/opencode.yaml`.

1. **Classify any load failure, then fix.** When the plugin is not loading (or
   `opencode api get /api/plugin` is empty or errors), grep
   `~/.local/share/opencode/log/opencode.log` and classify:

   - **install-cause** — `NpmInstallFailedError` / `LockTimeoutError` →
     `opencode plugin add @loreai/opencode` then `opencode service restart`.
   - **loader-cause** — `Plugin must export` → upstream BYK/loreai release or
     the V2 port below.
     A malformed or empty response is *not loaded* — never treat it as success.

1. **Port to V2 when asked.** Work against your `bengineerdavis/loreai` fork.
   Read `packages/opencode/src/index.ts` and `internal.ts`, then produce (or
   check) a V2 port: `Plugin.define` from `@opencode/plugin`, translating the
   V1 function + `config` hook into V2 registration (transforms/tools/hooks)
   while preserving routing and context injection. Report the change surface;
   do not commit.

## Example: classifying a load failure

When `opencode api get /api/plugin` returns an empty list and the log shows
`NpmInstallFailedError`, the cause is install-class, not loader-class — run
`opencode plugin add @loreai/opencode` and restart the service. If instead the
log shows `Plugin must export`, the installed plugin is V1-shape and the fix is
the V2 port, not a reinstall.

## Never

- Never install or upgrade the plugin outside the loreai topic (e.g. `npx -y @loreai/opencode@latest` or editing the deployed config directly); version
  and wiring follow the topic and the mise pin.
- Never whisper a broken plugin as a debug note — raise it with the classified
  cause.
- Never run `git add`, `git commit`, `git push`, or `dotagents install` for
  skills you authored — those are the user's gate, printed not executed.
