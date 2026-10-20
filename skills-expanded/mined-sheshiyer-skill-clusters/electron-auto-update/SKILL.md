---
name: electron-auto-update
description: "Ship updates to installed Electron apps — autoUpdater / electron-updater, update feeds (S3/GitHub/generic), signed differential updates, and staged rollouts with rollback. USE WHEN adding or debugging auto-update, choosing an update server, or handling update events safely. Updates must be signed."
cluster: electron
version: 1.0.0
origin: "skill-clusters (original)"
---

# Electron Auto-Update

Delivering new versions after install. Two layers: Electron's built-in **`autoUpdater`** (uses
Squirrel on macOS/Windows) and **`electron-updater`** (from electron-builder — feeds, deltas,
more control). Most electron-builder apps use `electron-updater`.

## The flow

1. CI publishes signed artifacts + a manifest (`latest.yml`/`latest-mac.yml`) to a **feed**
   (GitHub Releases, S3, or a generic HTTPS server).
2. The app checks the feed (`autoUpdater.checkForUpdates()` / `electron-updater`), downloads in the
   background, and installs on quit (or on user confirm).
3. Signature is **verified** before applying — updates inherit the same signing as the installer
   (`electron-builder-packaging`); an unsigned/forged update must be rejected.

## Handle the events (don't silently swap binaries)

```js
autoUpdater.on('update-available', /* notify */);
autoUpdater.on('download-progress', /* show progress */);
autoUpdater.on('update-downloaded', () => promptThenQuitAndInstall());
autoUpdater.on('error', /* log + surface, don't crash */);
```

## Rules

- **Updates must be signed/verified** — the update channel is a code-execution channel; treat it like one.
- Serve the feed over **HTTPS**; pin the host; never an unauthenticated HTTP feed.
- **Stage rollouts** (a percentage) and keep the previous version available for **rollback**.
- macOS auto-update **requires** signing + notarization; Windows requires a signed installer + matching feed.
- Let the user defer; install on quit by default — don't yank the app out from under work.

## Guardrails

- Signed, HTTPS-only, verified-before-apply updates — no exceptions.
- Staged rollout + rollback path; surface errors instead of failing silently.
- Reuse the packaging signing identity (`electron-builder-packaging`).
