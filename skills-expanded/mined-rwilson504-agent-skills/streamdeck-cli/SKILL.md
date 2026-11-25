---
name: streamdeck-cli
description: 'Stream Deck CLI (`streamdeck` / `sd`) command reference: create, link, restart, stop, dev, validate, pack/bundle, config. Every flag, every subcommand, with examples. USE FOR: scaffolding a plugin (streamdeck create), linking a plugin folder to Stream Deck, restarting a plugin, stopping a plugin, enabling/disabling dev mode + property-inspector debugger, validating a plugin against the schema, packaging a .streamDeckPlugin installer, .sdignore patterns, configuring package manager (npm/yarn/pnpm/bun), CLI configuration (reduceMotion), schema-update flags for CI.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["streamdeck", "elgato", "cli", "scaffolding", "packaging", "tooling"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/streamdeck", "emoji": "🎛️" } }
---

# Stream Deck CLI — Command Reference

> **Prerequisite:** Read `streamdeck-general` first for installation and
> the overall edit/build/test loop. This skill is the exhaustive flag-by-flag
> reference for every `streamdeck` (alias `sd`) subcommand.

## Purpose

Reference everything the `streamdeck` CLI can do so an agent can stop
guessing flag names. Useful when wiring CI pipelines, writing `npm`
scripts, or troubleshooting an unexpected CLI message.

## Install / verify

```pwsh
npm install -g @elgato/cli@latest
streamdeck -v                # prints CLI version
streamdeck                   # prints top-level help
```

Aliases: `sd` is identical to `streamdeck`. All examples below use
the long form for clarity.

## Top-level commands

| Command | Purpose | Alias |
|---|---|---|
| `create` | Interactive scaffolding wizard for a new plugin | — |
| `link [path]` | Install/symlink a `.sdPlugin/` directory into Stream Deck | — |
| `restart <uuid>` | Stop + start a running plugin | `r` |
| `stop <uuid>` | Stop a running plugin | `s` |
| `dev` | Enable/disable developer mode + PI debugger | — |
| `validate [path]` | Schema-check a plugin | — |
| `pack [path]` | Build a `.streamDeckPlugin` installer | `bundle` |
| `config` | Manage CLI configuration | — |
| `help [command]` | Print help for a specific command | — |

---

## 1. `streamdeck create`

Interactive wizard. No arguments, no flags.

```pwsh
streamdeck create
```

Prompts:

1. **Author name** — free text, becomes `manifest.Author`.
2. **Plugin name** — display name.
3. **Plugin UUID** — reverse-DNS, lowercase `a-z 0-9 . -`. **Permanent
   after publish.**
4. **Description** — short summary.
5. **Open in VS Code?** — convenience.

After completion:

- Scaffolds project directory named after the plugin.
- Runs `npm install` (or yarn/pnpm/bun depending on `config packageManager`).
- Auto-links the new `.sdPlugin/` to Stream Deck.
- Enables `streamdeck dev` mode for the PI debugger.
- Builds once so the plugin appears in Stream Deck immediately.

> 💡 If the wizard fails after creating the folder, you can `cd` into it,
> run `npm install`, then `streamdeck link` manually.

---

## 2. `streamdeck link [path]`

Registers a plugin directory with the local Stream Deck app. Symlinks
under the hood — no file copy, edits reflect immediately.

```pwsh
streamdeck link                              # link current working directory
streamdeck link com.yourhandle.hello-world.sdPlugin
```

**The directory name must equal `<PLUGIN_UUID>.sdPlugin`.** If you renamed
the UUID, also rename the folder.

Use cases:

- After `git clone` of an existing plugin repo, to register it.
- After `streamdeck stop` (followed by edit) to re-register.
- Recovering from a botched `pack`/uninstall.

---

## 3. `streamdeck restart <uuid>` / `streamdeck r <uuid>`

Stops the plugin if running, then starts it. Reloads `manifest.json`,
`imgs/`, `ui/`, and `bin/`.

```pwsh
streamdeck restart com.yourhandle.hello-world
streamdeck r       com.yourhandle.hello-world   # alias
```

Used by the `npm run watch` script under the hood — typically you won't
call this directly during development.

**Common gotcha:** if you renamed the UUID, the old UUID's plugin is
still registered. `streamdeck stop <old>` then re-link with the new UUID.

---

## 4. `streamdeck stop <uuid>` / `streamdeck s <uuid>`

Stops a running plugin and unloads its resources. The plugin remains
installed and can be restarted.

```pwsh
streamdeck stop com.yourhandle.hello-world
streamdeck s    com.yourhandle.hello-world      # alias
```

Useful before attaching a Node debugger with `--inspect-brk` semantics,
or before manually deleting the `.sdPlugin/` directory.

---

## 5. `streamdeck dev`

Toggles developer mode. When **enabled**:

- Property-inspector remote debugger is exposed at <http://localhost:23654/>.
- Plugins receive a Node `--inspect=<port>` flag (or the configured port).
- Stream Deck shows additional diagnostics in its own logs.

```pwsh
streamdeck dev              # enable
streamdeck dev --disable    # disable
```

| Flag | Effect |
|---|---|
| `--disable` | Turn off developer mode. |

`create` enables this automatically. Disable on a shared workstation if
you don't want random programs hitting your localhost debug port.

---

## 6. `streamdeck validate [path]`

Schema-check a plugin's `manifest.json` and project structure. Required
as the first step before `pack`.

```pwsh
streamdeck validate                                       # cwd
streamdeck validate com.yourhandle.hello-world.sdPlugin   # explicit path
streamdeck validate --force-update-check
streamdeck validate --no-update-check                     # CI mode
```

| Flag | Effect |
|---|---|
| `--force-update-check` | Refresh cached schemas immediately. |
| `--no-update-check` | Skip the schema-version check. Use in CI to avoid network calls. |

Checks:

- Manifest is valid against
  <https://schemas.elgato.com/streamdeck/plugins/manifest.json>.
- Required files exist (`CodePath`, action `Image`s, PI HTML).
- File extensions are correct (e.g. `Icon` must be extension-less in the
  field; the file on disk needs `.png`/`.svg`).
- UUIDs are reverse-DNS and properly nested under the plugin UUID.

Non-zero exit on any error. Use it as a pre-commit / pre-push hook.

---

## 7. `streamdeck pack [path]` / `streamdeck bundle [path]`

Builds the `.streamDeckPlugin` installer file users will double-click to
install. Internally: `validate` → strip files matched by `.sdignore` →
zip into `.streamDeckPlugin`.

```pwsh
streamdeck pack com.yourhandle.hello-world.sdPlugin/ --output dist/
streamdeck pack --version 0.8.2.12
streamdeck pack --dry-run
streamdeck pack --force --output dist/                    # overwrite
```

| Flag | Effect |
|---|---|
| `--dry-run` | Print what would be packed without writing the file. |
| `-f`, `--force` | Overwrite an existing `.streamDeckPlugin` at the output path. |
| `-o`, `--output <path>` | Output directory. Default is cwd. |
| `--version <version>` | Override `manifest.Version`. Must be in `MAJOR.MINOR.PATCH.BUILD` format. |
| `--force-update-check` | Refresh schemas before validating. |
| `--no-update-check` | Skip schema refresh (CI). |

### `.sdignore`

Same syntax as `.gitignore`, applied at pack time. Default exclusions:

```
.git/
/.env*
*.log
*.js.map
```

Common additions:

```gitignore
# Source — only ship compiled bin/
src/
*.test.*
__tests__/
# Dev-only docs
README.md
CONTRIBUTING.md
.vscode/
```

> Do NOT exclude `bin/`, `imgs/`, `ui/`, or `manifest.json` — those are
> what the user actually needs.

---

## 8. `streamdeck config`

Manages CLI-wide configuration (stored in your home directory, not the
project). Useful when you want all `streamdeck create` runs to use yarn,
or to silence the gif-style ASCII recordings.

```pwsh
streamdeck config list                              # show current
streamdeck config set packageManager=yarn
streamdeck config set reduceMotion=true
streamdeck config unset packageManager              # back to default
streamdeck config reset                             # back to all defaults
```

| Sub-command | Description |
|---|---|
| `set <key=value...>` | Set one or more keys. Multiple in one invocation OK. |
| `unset <key...>` | Remove a key (revert to default). |
| `reset` | Clear all custom config. |
| `list` | Print current effective config. |

| Key | Type | Default | Notes |
|---|---|---|---|
| `packageManager` | `npm` / `yarn` / `pnpm` / `bun` | `npm` | What `create` runs to install deps. |
| `reduceMotion` | boolean | `false` | Disables animated CLI output. |

---

## 9. Useful `package.json` scripts

The scaffold gives you `build` and `watch`. Recommended additions:

```json
{
  "scripts": {
    "build":        "rollup -c",
    "watch":        "rollup -c -w --watch.onEnd=\"streamdeck restart com.yourhandle.hello-world\"",
    "validate":     "streamdeck validate com.yourhandle.hello-world.sdPlugin --no-update-check",
    "pack":         "streamdeck pack com.yourhandle.hello-world.sdPlugin --output dist --force --no-update-check",
    "pack:dry":     "streamdeck pack com.yourhandle.hello-world.sdPlugin --dry-run --no-update-check",
    "lint":         "eslint . --max-warnings 0 && prettier . --check",
    "format":       "eslint . --fix && prettier . --write",
    "release":      "npm run lint && npm run validate && npm run build && npm run pack"
  }
}
```

---

## 10. Quick troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `streamdeck: command not found` | CLI not on `PATH` | `npm install -g @elgato/cli@latest`, restart shell |
| Plugin doesn't appear after `link` | Stream Deck app was launched with elevated privileges | Restart Stream Deck normally |
| `watch` rebuilds but plugin doesn't update | `manifest.json` has no change → watch only triggers on `src/` | Touch the manifest or `streamdeck restart <uuid>` |
| `restart`: `plugin <uuid> not found` | UUID mismatch between folder, manifest, command | All three must match; check folder is `<uuid>.sdPlugin/` |
| `validate` complains about extension on `Icon` | Extension was included in the manifest field | Remove the `.png`/`.svg` from the value — only the file on disk has it |
| `pack` produces a tiny `.streamDeckPlugin` | `.sdignore` is too aggressive — `bin/` got excluded | Remove `bin/` (and other required dirs) from `.sdignore` |
| PI debugger at `localhost:23654/` is empty | PI not visible OR `streamdeck dev` is disabled | Open the action in Stream Deck so the PI renders; verify `streamdeck dev` (no `--disable`) |

---

## See Also

- Official CLI intro: <https://docs.elgato.com/streamdeck/cli/intro>
- Per-command docs: `https://docs.elgato.com/streamdeck/cli/commands/<name>`
- Sibling skills: `streamdeck-general` (workflow), `streamdeck-publishing`
  (uses `pack` for marketplace submission)
