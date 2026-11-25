---
name: app-it-static
description: >-
  Turn a finished or buildable web app into a macOS Dock-launchable .app that
  serves built output instead of a dev server. Use when the user asks for
  app-it-static, a finished site/app launcher, a lightweight Dock app, or a
  dist/build/out bundle clickable from the Dock. Builds once, serves a snapshot
  via static-server.py or file://, and routes live projects to app-it. macOS
  only.
---

# app-it-static - Make a finished build launchable from the Dock

`app-it-static` is the no-dev-server companion to `app-it`: it builds once,
serves the finished output, installs beside live apps in `~/Applications/App It/`,
and keeps the native Swift WebKit window and Dock identity.

## Non-Negotiables

1. Run `templates/inspect-static.sh` first and read the output before editing.
2. Confirm before the first project build. It can write files and take time.
3. Never run `npm run dev`. If the app needs a live dev server, route to
   `app-it` and say why.
4. Serve a snapshot and say so. Source changes need `desktop:rebuild`.
5. Default to `serve_mode: "server"`. Use `file` only after proving the build is
   file:// safe.
6. Copy shipped templates and customize through `scripts/app-it.config.json`.
   Do not re-derive launcher patterns.
7. Verify the built output, app bundle, install path, runtime port, server
   response, quit cleanup, and human-only GUI limits.

## Reference Map

Open only the files needed by the inspection result:

- `references/project-inspection.md` - static-servable tests, build/output
  detection, package managers, monorepos, names, bundle IDs, and tools.
- `references/serve-modes.md` - server vs file decisions and the file:// safety
  checklist.
- `references/generated-files.md` - template roster, shared-template rules,
  allowed target-project files, config JSON, and package scripts.
- `references/verification.md` - smoke tests, app-bundle checks, runtime checks,
  cleanup, and human/deferred buckets.
- `references/report-template.md` - exact final report format plus decision
  history.
- `references/anti-patterns.md` - traps that cause broken static launchers.

## Templates

Templates live next to this file in `templates/`. Copy them into the target
project; do not rewrite them. See `references/generated-files.md` for the full
roster.

Shared templates are byte-identical to `app-it` and guarded by repo validation:
`wrapper.swift`, `native-run-stub.c`, `desktop-icons.sh`,
`desktop-icons-preview.sh`, `desktop-install.sh`, `info-plist-template.xml`, and
`placeholder-icon-gen.sh`. If launcher internals change, edit the `app-it` copy
and re-sync this plugin so marketplace installs stay self-contained.

## Workflow

### 1. Inspect

Run:

```bash
/path/to/plugins/app-it-static/skills/app-it-static/templates/inspect-static.sh
```

Use disk truth: `package.json`, config files, built output, and actual scripts.
Read `references/project-inspection.md` before deciding whether the app is
static-servable, which build command/output dir to use, or whether a monorepo
contains multiple apps.

### 2. Decide

For each user-facing app:

```text
Static build or hand-written index.html exists?
  no  -> route to app-it
  yes -> needs http origin, routing fallback, fetch(), or service worker?
           yes -> server mode (default)
           no  -> file mode candidate
```

When unsure, choose server mode. It costs a tiny Python process and is the safe
default for framework builds.

### 3. Build

Confirm with the user, run the project build once, then copy templates into the
target project and write `scripts/app-it.config.json`. `desktop:build` assembles
the `.app`; it must not run the project build. `desktop:rebuild` is the refresh
path that reruns the build command.

Read `references/generated-files.md` before editing package scripts, generated
docs, config JSON, icons, or install paths.

### 4. Verify

Verification is mandatory. Read `references/verification.md` and run the checks
that apply: built `index.html`, Mach-O `Contents/MacOS/run`, executable
`run.sh`, Mach-O wrapper, plist placeholders gone, `.icns`, installed-path
open, server response, and Cmd+Q cleanup for server mode.

Never claim GUI-only checks passed unless a display actually proves them. Put
window render and Dock icon identity in the human bucket when needed.

### 5. Report

Use `references/report-template.md` for both the chat reply and
`docs/desktop-launcher.app-it-static-report.md`. Include snapshot limitations,
refresh command, verification results, known limits, and decision history.

Stage files only when the local convention or user request asks for it. Do not
commit unless asked.

## Quick Defaults

- Install destination: `~/Applications/App It/`.
- Bundle ID prefix: `com.user.<slug>`.
- Serve mode: `server`, unless file:// safety is proven.
- Vite/CRA/Astro/SvelteKit static/Next export/Angular/Nuxt generate: usually
  server mode.
- Hand-written `index.html` with relative assets and no routing/fetch/service
  worker: file mode candidate.
- Missing `swiftc` or `python3`: stop and say `xcode-select --install`.

## Stop Signs

Stop and explain clearly when the app only works through a live dev server, the
build fails before launcher work, the output dir lacks `index.html`, required
tooling is missing, or the environment cannot verify a claim the report would
need.
