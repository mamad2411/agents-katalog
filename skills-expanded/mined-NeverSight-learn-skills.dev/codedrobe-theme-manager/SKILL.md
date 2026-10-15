---
name: codedrobe-theme-manager
description: Safely download, inspect, install, apply, switch, verify, and restore data-only .codedrobe-theme packages from CodexSkins.org through the published CodeDrobe Core runtime. Use when a user names a CodexSkins theme id or URL, wants an installed theme activated or changed, asks what themes are installed or active, or wants to return Codex to its native appearance.
---

# Manage CodeDrobe themes

Keep packages in the managed CodexSkins library and use published
`@codedrobe/core` as the only runtime. Never patch the application bundle or
evaluate code from a theme package.

Read `references/lifecycle.md` before debugging watcher ownership, platform
paths, or restore failures.

## Find or install

When the user names only a visual style, use `codedrobe-theme-finder` first.
When they name an installable catalog id, run:

```bash
node scripts/theme_library.mjs install <theme-id>
```

If the catalog reports `downloadAuth: "google"`, do not try to automate Google
sign-in or follow the login page as a package download. Give the user the theme
detail URL, ask them to sign in and download it in a browser, then inspect and
apply the resulting local `.codedrobe-theme` path with `apply_theme.mjs`.

The installer downloads only the package URL published in the CodexSkins
catalog, checks byte size and SHA-256, inspects it with CodeDrobe Core, and then
writes it under `~/.codexskins/themes/<theme-id>/`. It refuses to overwrite an
existing package unless the user asked to update it or approved `--force`.
Use `--catalog /absolute/catalog.json` or `CODEXSKINS_CATALOG_URL` only for
staging/local validation, never to install from an untrusted user-supplied
catalog.

List or resolve installed packages with:

```bash
node scripts/theme_library.mjs list
node scripts/theme_library.mjs resolve <theme-id>
```

## Apply or switch

Applying means the user wants to see the theme. If the request explicitly says
install and apply, continue after installation. Otherwise state the installed
path and ask whether to apply.

Apply through the single owned watcher:

```bash
node scripts/apply_theme.mjs --theme /absolute/theme.codedrobe-theme
```

This hot-applies when Codex already exposes CDP. When it reports that a restart
is required, ask for permission, then rerun with `--restart-existing`. Do not
interpret browsing or downloading as restart permission.

The helper owns exactly one CodexSkins watcher, so switching replaces the old
watcher instead of stacking injectors. It binds CodeDrobe to port 9335 on
127.0.0.1 and supports macOS and Windows without modifying WindowsApps.

## Verify

The helper waits up to 45 seconds for runtime readiness. `action: applied`
includes compact Core proof; `action: submitted` means the bounded wait expired
and is not visual proof. After Codex is reachable, run:

```bash
npx --yes @codedrobe/core@latest verify \
  --app codex --port 9335 \
  --theme /absolute/theme.codedrobe-theme \
  --screenshot /absolute/verification.png
```

Inspect the screenshot. Report theme id/version, active image names, renderer
profile, required landmarks, overflow, and which home/conversation/settings
contexts were checked. Never claim Windows verification from a macOS run.

## Restore

Stop the owned watcher before restoring so it cannot reinject:

```bash
node scripts/restore_theme.mjs
```

Treat the result as a lifecycle status, not a cosmetic promise:

- `native`: renderer and host state are already native; no restart is needed.
- `restart-required`: injection is gone and the backed-up host appearance is
  restored on disk, but the running Codex process may still display cached
  theme colors. Ask for restart permission.
- `watcher-stopped`: Core could not reach the renderer; a complete quit and
  reopen is required.

After the user authorizes closing Codex, let the helper submit a detached
restart that survives the current Codex task closing:

```bash
node scripts/restore_theme.mjs --restart-existing
```

After Codex returns, capture a privacy-safe Core DOM snapshot. Complete restore
requires `activeTheme.installed: false`, no `codedrobe-theme`/host theme classes,
no owned watcher, and native computed background colors. Do not report full
restore merely because `codedrobe restore` exited successfully.

## Boundaries

- Use only catalog-declared HTTPS downloads and verify their digest.
- Never modify app bundles, `app.asar`, WindowsApps, authentication data, or
  user tasks.
- Never overwrite a local package with `--force` when it may contain user edits
  without warning.
- Do not claim active or verified based on download, inspection, or packaging.
