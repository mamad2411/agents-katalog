---
name: moe-dogfood
description: Use when installing, reinstalling, upgrading, uninstalling, or dogfooding this repo's Moe plugins in a live Claude Code session, when adding or retiring a plugin, or when a dogfood install misbehaves — hooks failing with MODULE_NOT_FOUND at node:internal/modules/cjs/loader, "Plugin directory does not exist", a dead moe-memory MCP server, or skills that did not change after an edit.
---

# Dogfooding Moe into Claude Code

## How Moe actually installs — read this first

Moe is **not** sideloaded by copying `plugins/` into a directory. It installs
through a real marketplace, and getting this wrong is the source of every
dogfood mishap:

- **Marketplace**: the GitHub repo `https://github.com/zak-keown/moe.git`,
  registered under the name `moe`. `claude plugin marketplace add <url>` clones
  it to `<config-dir>/plugins/marketplaces/moe`; `claude plugin marketplace
  update moe` re-pulls it.
- **Plugins**: each plugin's `source` in the marketplace's
  `.claude-plugin/marketplace.json` is a **published npm package** —
  `@bubstack/moe-core` (plugin `moe`), `@bubstack/moe-backstory`,
  `@bubstack/moe-memory`, `@bubstack/moe-glass`, `@bubstack/moe-crew`,
  `@bubstack/moe-statusline`. These are on the public npm registry
  (`npm view @bubstack/moe-memory version`). `claude plugin install <name>@moe`
  npm-installs the package into `<config-dir>/plugins/npm-cache/node_modules/`
  and unpacks the active version to
  `<config-dir>/plugins/cache/moe/<plugin>/<version>/`.
- **Every plugin is self-contained.** Because each is a published npm package,
  it ships its own compiled runtime and vendored deps (moe-memory carries its
  onnxruntime/tokenizer runtime; moe-crew carries its `dist`). There is nothing
  to hand-copy and nothing to repoint. If you find yourself editing a staged
  `hooks.json` or copying a `dist/` into place, you are on the wrong path — stop.

The command generator is `bin/moe-install` (published as the `moe` CLI). It is
multi-harness and **dry-run by default**: nothing changes without `--apply`.

## Install or reinstall (Claude Code)

```bash
node bin/moe-install --harness claude-code            # print the plan (dry-run)
node bin/moe-install --harness claude-code --apply    # execute it
```

The plan it prints, verbatim:

```
claude plugin marketplace add https://github.com/zak-keown/moe.git
claude plugin install moe@moe
claude plugin install moe-backstory@moe
claude plugin install moe-memory@moe
claude plugin install moe-glass@moe
claude plugin install moe-crew@moe
claude plugin install moe-statusline@moe
```

Then **restart the session** — a running one holds the hook registry it loaded
at startup.

To keep dogfooding out of your primary `~/.claude`, install into a separate
config directory with `--config-dir <path>` or `CLAUDE_CONFIG_DIR` (e.g.
`~/.claude-alt`). Which plugins install is governed by the active profile
(`core` / `standard` / `full`); the active one is in `<config-dir>/.moe-profile`,
and `moe --help` lists the selectors.

## Dogfooding working-tree changes: the github/npm refresh

The marketplace serves **published** versions. Your working tree is not live
until it is published — there is no local-directory shortcut in this design
(a Claude-Code-only local marketplace would not work for the other seven
harnesses; see CLAUDE.md).

1. Land the change and cut a release. `publish.yml` (on a `v*` tag) OIDC-publishes
   the `@bubstack/moe-*` packages to npm, and `zak-keown/moe` main carries the
   matching `.claude-plugin/marketplace.json`. Regenerate that manifest with
   `pnpm mint`; never hand-edit it (AGENTS.md, repo law 1).
2. `claude plugin marketplace update moe` — re-pull the manifest.
3. Update the plugins: `node bin/moe-install --harness claude-code --upgrade`
   prints the manual plan (open Claude Code's `/plugins` and update `moe@moe`,
   `moe-backstory@moe`, … each), or reinstall them.
4. **Restart the session.**

So this refresh dogfoods a *released* version. Iterating on unpublished code
through it means publishing a version per iteration — a real cost worth naming
before you start.

## Diagnosing a broken install

| Symptom | Cause | Fix |
|---|---|---|
| A hook fails, `cjs/loader` MODULE_NOT_FOUND, no plugin named | a plugin's installed runtime is missing/broken, or a half-finished install | reinstall that plugin; confirm the version dir under `<config-dir>/plugins/cache/moe/<plugin>/<version>/` |
| `Plugin directory does not exist: .../<name>` | plugin uninstalled or removed while a session held it | restart; if it persists, check `enabledPlugins` in `<config-dir>/settings.json` |
| moe-memory MCP dead / search returns nothing, no error | the server failed to start (read its log) or the npm package never resolved into `npm-cache/` | reinstall `moe-memory@moe`; restart |
| Skill edits do not take effect | you edited the repo, but the install serves the published cache, not your tree | publish + refresh (above), then restart |
| Retired plugin still loads | still in `enabledPlugins` | `claude plugin uninstall <name>@moe`, then restart |

Two persisted files are the truth, and they disagree with a stale session:

- `<config-dir>/plugins/installed_plugins.json` and
  `<config-dir>/plugins/known_marketplaces.json` record what is installed and
  where the `moe` marketplace resolves from (its `installLocation` may sit under
  a different config home than the one you are reading).
- `<config-dir>/settings.json` `enabledPlugins` is what the harness will load.
  When it disagrees with what the session does, the session is stale — restart.

`<config-dir>/plugins/cache/moe/` is **versioned** (`<plugin>/<version>/`), and
its timestamps mislead: an untouched cache dir tells you nothing about which
version is live. Trust `installed_plugins.json`, not `ls`.

## Retiring a plugin

Order matters. `claude plugin uninstall <name>@moe` **first**, while the session
still holds it — uninstalling after the marketplace has dropped the plugin
leaves the session firing its hooks at a directory that is gone, reporting
`Plugin directory does not exist` on every event until you restart. Then
`claude plugin marketplace update moe` and restart.

## Other harnesses

`bin/moe-install` installs for eight harnesses — `claude-code, cursor, codex,
kimi, opencode, pi, agent-plugins-1.0, copilot`. This skill shows the
`claude-code` adapter; for any other, `node bin/moe-install --harness <id>`
(still dry-run until `--apply`). Any change to how install works has to hold for
all eight (CLAUDE.md), which is exactly why the install path is a shared
marketplace and not a Claude-Code-specific copy step.
