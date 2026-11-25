---
name: electron-auto-update
description: >
  This skill should be used when the user wants to ship automatic updates to
  users of an Electron desktop app. Triggers on phrases like "auto-update
  electron", "electron-updater", "ship updates to users", "release pipeline
  electron", "github releases electron", "how do users get updates", "delta
  updates electron", "update channel", "test my update pipeline", "beta
  channel electron", or nervousness about building a release pipeline for the
  first time. Also triggers on "I've never shipped auto-update before" or
  similar anxiety signals.
version: 0.1.0
---

# Electron Auto-Update — The Anxiety-Free Version

## When this skill is loaded

The user is shipping an Electron app and needs a working auto-update pipeline. Often this is their first time building one, and they're scared it's hard. It isn't. It's three moving parts that talk to each other, and once it's wired, releasing a new version is one command.

## Calibrate expectations first

**The thing that's scary isn't auto-update itself — it's the one-time setup of code signing + CI.** Auto-update is just "the app polls a URL; if there's a new version, download it." That part is a library call. The hard parts live in the `electron-code-signing` skill; refer the user there before tackling the update pipeline if signing isn't done.

**After the first release ships, cutting release N+1 is `git tag v1.0.1 && git push --tags`.** That's not marketing — it's the literal workflow. CI does everything else.

## The mental model — three moving parts

1. **Your app** has `electron-updater` embedded. On launch (default) or on a timer (configurable), it polls a **feed URL**.
2. **The feed** is a set of JSON manifests + binary files on a host. `electron-builder` writes the JSON automatically when it publishes. Default host: GitHub Releases.
3. **electron-updater** reads the feed, sees a newer version, downloads the delta (not the full installer — huge savings), verifies the signature, prompts the user to restart.

That's the whole system. Every other question ("what about rollback?", "can I have beta channels?", "what about delta compression?") is a detail on top of those three parts.

## The minimum-viable pipeline (GitHub Releases)

Why GitHub Releases: free, supports public and private repos, zero extra infra, `electron-builder` has a first-class GitHub provider.

### Step 1 — Install electron-updater

```sh
pnpm add electron-updater
```

### Step 2 — Wire it in the main process

In `src/main/main.ts`:

```typescript
import { autoUpdater } from 'electron-updater';
import log from 'electron-log';

// Pipe update logs to electron-log so users can send them for support
autoUpdater.logger = log;
log.transports.file.level = 'info';

app.whenReady().then(() => {
  // ...create window...
  autoUpdater.checkForUpdatesAndNotify();
});
```

That's it for the app side.

### Step 3 — Configure electron-builder publish target

In `electron-builder.yml` (or the `build` field in `package.json`):

```yaml
publish:
  provider: github
  owner: claybowl
  repo: Doer
  private: true   # set false for public repos; affects whether GH_TOKEN is needed at runtime
```

### Step 4 — CI workflow that builds, signs, and publishes on tag push

Short version — full YAML in `references/github-releases-setup.md`. The shape:

- Trigger on `push` to tags matching `v*.*.*`
- Matrix: macos-latest + windows-latest
- Install → build → package → sign → notarize (Mac) → `electron-builder --publish always`

electron-builder handles the GitHub Release upload automatically. No manual steps.

### Step 5 — Cut a release

```sh
npm version patch        # bumps package.json + creates git tag v1.0.1
git push --follow-tags   # pushes commit + tag
```

CI fires. ~15–25 minutes later a new release is live. Users on 1.0.0 get prompted to update to 1.0.1 within seconds of next app launch.

## What users actually experience

**Default behavior:**
- App launches → `electron-updater` polls feed in background → finds 1.0.1 → downloads delta silently while user works → shows a notification "Update available, restart to install" → user restarts → app relaunches as 1.0.1.

**Customizable behavior:**
- Prompt immediately (modal dialog) instead of on-quit
- Defer updates until idle
- Show a progress bar for long downloads
- Staged rollout: 10% of users at first, then 50%, then 100% (requires manual version-selector logic)

See `references/update-ux-patterns.md` (stub — add in v0.2.0 as we learn).

## Testing your pipeline before real users hit it

This is the most-skipped step and the source of most "auto-update doesn't work" tickets.

1. **Build and sign version 1.0.0 via real CI.** Publish the release.
2. **Install 1.0.0 on a clean VM** or a second physical machine. Launch. Confirm it runs cleanly.
3. **Build and publish version 1.0.1 via real CI.** Wait for release to show as "latest" on GitHub.
4. **Launch the installed 1.0.0 app.** Wait ~30–60 seconds for the update check.
5. **Confirm the update prompt appears, download completes, and app restarts as 1.0.1.**

If all five steps pass, your pipeline is real. Skip this test at your peril — subtle mis-config (wrong feed URL, mismatched cert, wrong installer target) only shows up here, not in local `pnpm dev`.

## The five failure modes that actually matter

When auto-update breaks in the wild, it's almost always one of these. See `references/failure-modes.md` for the deep triage guide — and the `/ep-debug-update` command runs the full diagnostic.

1. **Update not detected.** Feed is fine but the app isn't seeing it. Usually: wrong feed URL, new release isn't marked latest, or app's cached last-check time hasn't expired.
2. **Update detected but download fails.** Private repo + missing `GH_TOKEN` at runtime, CORS / CDN issue, corporate firewall.
3. **Install fails / signature mismatch.** Cert rotated between versions; new binary signed with different cert → `electron-updater` refuses. Fix: stable cert, renew never-expires, or handle rotation deliberately.
4. **Version mismatch.** `package.json` version doesn't match the git tag. Tag is `v1.0.1`; package.json says `1.0.0`. Feed is built from package.json, so the feed says 1.0.0; auto-update finds no newer version.
5. **Windows UAC loop / install fails.** Wrong installer target (`msi` instead of `nsis`/`nsis-web`), or unsigned/OV-signed binary triggering SmartScreen.

## Rollback strategy

`electron-updater` does not natively support user-initiated downgrade. Plan for **forward-fix**, not rollback:

- **Primary:** ship 1.0.2 that fixes 1.0.1's bug. Fastest; users get a real fix.
- **Secondary:** unpublish the bad GitHub Release (mark as draft). New installs get the previous "latest" (1.0.0). Users already on 1.0.1 stay on 1.0.1 until 1.0.2 ships. Acceptable for non-critical bugs; risky for data-corruption bugs.
- **Never:** try to force a downgrade. `electron-updater` will fight you, and users will end up with broken installs.

The lesson: **treat every release as if you can't un-ship it.** Run the test-pipeline flow above on every major version.

## What's not in scope for v0.1.0 of this skill

- Custom update servers (Hazel, S3-based, self-hosted). The GitHub Releases path handles 95% of cases. See `references/alternative-hosts.md` (stub — expand when someone actually needs it).
- Staged rollouts. Possible but requires custom feed manipulation. Cross that bridge when you have 10,000+ users.
- Mac App Store distribution. Different update mechanism (Apple manages it). See Apple's docs, not this skill.

## References

- `references/github-releases-setup.md` — full GH Actions workflow YAML
- `references/failure-modes.md` — every known failure mode with diagnostic steps
