---
name: versioning
description: How app version bumping interacts with OTA runtimeVersion fingerprints, and how to bump versions safely. Use when choosing a runtimeVersion policy, when an OTA silently stops reaching devices after a version bump, when setting up automated version/build-number bumping for an Expo app, or when a store rejects a submission for a duplicate/already-used version (e.g. iOS "version already submitted" while Android accepted the same build).
---

# Versioning & the OTA fingerprint

This skill is about the **collision between marketing-version bumps and the OTA fingerprint**.
For the full OTA pipeline (manifest server, upload script, iOS patches, retention) see the
**ota** skill — this one covers only the versioning half and how to keep it OTA-safe.

## The core model — `runtimeVersion: { policy: 'fingerprint' }`

With the `fingerprint` policy, `runtimeVersion` is **not** a version string — it's a per-platform
**hash of the native layer**. An OTA is tagged with the fingerprint of the code it was exported
from, and it only reaches a binary whose **embedded fingerprint exactly matches**. A mismatch =
the OTA *silently never applies* (no error; the app keeps its old bundle).

The fingerprint hashes the native inputs: native modules/deps (`package.json`/`yarn.lock`),
config plugins, entitlements, native dirs, `expo-build-properties`, `yarn patch` patches,
`firebase.json`, config-affecting env vars baked at build — **and, by default, certain
`app.config` fields: `version`, `android.versionCode`, `ios.buildNumber`** (the fingerprint
source named `ExpoConfigVersions`).

**Why this is the safe default:** a real native change (new native module, a permission, an SDK
bump) changes the hash automatically, so an incompatible JS bundle can *never* reach a binary
that lacks the native capability it needs. You get that guarantee for free — no manual runtime
bookkeeping.

## The trap: marketing version is coupled to the fingerprint

Because `version`/`versionCode`/`buildNumber` are in the fingerprint by default, and a typical
`app.config.ts` does:

```ts
version: config.version,   // version flows package.json → resolved Expo config
```

**bumping the marketing version silently changes the fingerprint — with zero native changes.**
Every already-installed binary is on the OLD fingerprint. Any OTA you export *after* the bump is
tagged with the NEW hash, which **no installed binary carries** → it reaches nobody, silently.

| Symptom | Cause | Fix |
| --- | --- | --- |
| "I pushed an OTA and nobody got it" (right after a version bump) | The version bump moved the fingerprint; OTAs now target a hash no shipped binary has | Decouple version from the fingerprint (below) |
| "OTA worked, then stopped reaching devices after a release" | Same — the release bumped `version`/`buildNumber`, which are fingerprint inputs | Same |

This is the version-specific twin of the `.gitignore` footgun documented in the **ota** skill:
a non-native edit drifts the hash and strands every installed build.

## The fix: decouple version from the fingerprint

Add a **`fingerprint.config.js`** at the project root and skip the version sources:

```js
/** @type {import('@expo/fingerprint').Config} */
module.exports = {
  sourceSkips: ['PackageJsonScriptsAll', 'ExpoConfigVersions'],
};
```

- **`ExpoConfigVersions`** drops `version` / `android.versionCode` / `ios.buildNumber` from the
  hash. After this, marketing/build-number bumps are OTA-compatible.
- **`PackageJsonScriptsAll`** additionally drops `package.json` `scripts` (editing an npm script
  otherwise drifts the hash — see the ota skill). Only skip scripts if none affect the native
  build (no prebuild/postinstall that touches native).

After this, **only real native changes move the fingerprint.** Version bumps become cosmetic and
OTA-safe.

> **CRITICAL — a fingerprint-config change ships with a new full build.** Changing
> `sourceSkips` (or `.fingerprintignore`) changes the fingerprint **baseline**, so it takes effect
> only on the **NEXT native build**. Binaries already installed keep their old hash until rebuilt.
> The binary and its OTAs adopt the new stable hash together — never introduce a `sourceSkips`
> change as a standalone OTA. Decide the full skip set *before* that build so you don't need
> another rebuild to add more. Then verify the build's CI `Resolved runtime version` equals
> `expo-updates fingerprint:generate`'s hash (both must honor the same config).

## Why NOT `policy: 'appVersion'`

`appVersion` ties `runtimeVersion` to the version string, giving **release-cohort isolation**
(each version is its own OTA lineage). It's a common alternative, but it's **less safe** than
fingerprint:

- **It doesn't automate the crash guard.** If you make a native change and *forget* to bump the
  version, the OTA reaches the old-native binary and **crashes** (JS expects a native module the
  binary lacks). `fingerprint` closes this hole automatically — a native change moves the hash, so
  the OTA can't land on an incompatible binary.
- **It forces a rebuild for every version bump to ship OTAs** — because the runtime is the version
  string, an OTA for 1.3.0 needs a 1.3.0 binary in the field.

**Recommendation:** use `fingerprint` + `ExpoConfigVersions` skip. Only choose `appVersion` if the
team specifically wants version-based release cohorts and accepts those two costs.

## Version bumping is now cosmetic / store-facing — automate it lightly

Once decoupled, versions are for the stores and humans, not for OTA routing. Two independent
knobs:

### Build numbers (`versionCode` / `buildNumber`) — fully automated by EAS

Never touch these by hand. Let EAS own them remotely:

```jsonc
// eas.json
{
  "cli": { "version": ">= 16.0.0", "appVersionSource": "remote" },
  "build": {
    "stg": { "autoIncrement": true },
    "prd": { "autoIncrement": true }
  }
}
```

`appVersionSource: "remote"` stores the counters on EAS; `autoIncrement: true` on each store
profile bumps them per build. You never edit `versionCode`/`buildNumber` in config again.

### Marketing version (`1.x.y`) — resolve it IN the release workflow

A **conventional-commits resolver** picks the level from the commit subjects since the last
release (`scripts/next-version.mjs` in the templates):

- `feat:` → **minor**
- `fix:` / `perf:` → **patch**
- `!` or `BREAKING CHANGE` → **major**
- anything else (`chore`/`docs`/`ci`/…) → **no bump**

**Do not leave the bump as a separate manual step next to a self-triggering store build.**
That combination is not merely forgettable — it fails *asymmetrically*, which is what makes it
so easy to ship:

| Store | Gates on | A stale marketing version… |
| --- | --- | --- |
| **Google Play** | `versionCode` (auto-incremented by EAS) | **accepted** — nothing complains |
| **App Store** | `CFBundleShortVersionString` (must be unique per submission) | **rejected at submission** — after a full build |

So the release *looks* fine (Android went out), and iOS fails at the very last step, ~40 minutes
of build later. Every release, until someone remembers. Resolve the version inside the prd store
workflow so there is nothing to remember — see `templates/.github/workflows/expo-store-deploy-prd.yml`
(`resolve-version` job).

**Keep the bump COMMIT on the staging branch.** Auto-committing to `main` fights a stg-first /
no-squash merge flow and produces version conflicts on every merge. The workable split is:

- **derive** the version from the branch being built (`main` — that's what ships), then
- **push the bump commit to `stg`**, where it reaches `main` on the next normal merge.

That works because **`eas build --local` builds the WORKING TREE, not a git commit** — the build
job just writes `package.json` in place before building, so the binary carries the new version
without the commit ever touching `main`. This is the detail that makes "automate the bump" and
"CI never commits to main" compatible; without it you have to pick one.

**Record the bump BEFORE building, not after.** A version you couldn't record is one you'll
recompute and resubmit next time — the exact rejection the automation exists to prevent. Fail the
release on a failed push rather than shipping a version nothing tracks.

Give the workflow a **`version` input** (force an exact `X.Y.Z`, for releases the commit history
can't express) and a **`skip_version_bump`** toggle (re-cut a version the stores never accepted —
e.g. rebuilding one platform to match the other's in-flight submission).

#### Two traps in the CI wiring

**A cancelled `needs` job does not fail the guard.** `if: always() && !failure() && !cancelled()`
is the usual way to tolerate a *skipped* `detect-platform` on `workflow_dispatch` — but a
**cancelled** dependency (runner starvation cancels jobs before they record a single step) is
neither a workflow failure nor a workflow cancellation, so the deploy job runs anyway with an
empty version output, which the build reads as *"use package.json as-is"* → the stale version
ships. Require success explicitly:

```yaml
if: ${{ always() && !failure() && !cancelled() && needs.resolve-version.result == 'success' }}
```

**`git push --follow-tags` only pushes ANNOTATED tags.** A release step doing `git tag "v$NEXT"`
(lightweight) + `git push --follow-tags` silently pushes no tag at all — `git ls-remote --tags`
stays empty for months. The resolver prefers the newest `v*` tag as its scan base and quietly
falls back to "the commit that last set this version", which is only correct while history stays
linear. Use `git tag -a "v$NEXT" -m "v$NEXT"`.

## Debugging playbook — "OTA not reaching a device"

1. **Read the device's ACTUAL fingerprint, don't guess it.** If you self-host the manifest (ota
   skill), log every device check-in — `expo-platform`, the `expo-runtime-version` header, and
   `expo-current-update-id` — to a table. That header **is** the fingerprint the shipped binary
   embeds; compare it against the published update's `runtime_version`.
2. **Don't trust a locally-computed fingerprint.** Local (macOS) vs CI (Linux) computation can
   differ from what a store-built binary actually embedded. The device's real header is ground
   truth; a local hash is a hypothesis.
3. **Compute per platform under the SAME env as the build.** Config-affecting env vars change the
   hash:
   ```bash
   doppler run --project mobile --config stg -- \
     node_modules/.bin/expo-updates fingerprint:generate --platform ios
   # → {"sources":[...],"hash":"489751…"}   ← hash is the runtimeVersion
   ```
4. **To OTA a device stranded on an OLD baseline** (e.g. a build made *before* you added the
   `fingerprint.config.js` decouple, or before a version bump): reproduce that binary's fingerprint
   at compute time. Temporarily **revert both** the version bump **and** the `fingerprint.config.js`
   / `.fingerprintignore` change in the working tree, then export/push the OTA — it'll be tagged
   with the hash that stranded binary actually carries. (The permanent fix is a fresh build; this
   is the one-time rescue.)
5. **stg and prd are separate fingerprint lineages.** Different config (e.g. `EXPO_UPDATE_URL`) →
   different hashes, so a staging fingerprint issue never touches production and vice-versa. Always
   verify against the same environment the device was built in.

## Quick checklist for a new project

- [ ] `runtimeVersion: { policy: 'fingerprint' }` in `app.config.ts`
- [ ] `fingerprint.config.js` with `sourceSkips: ['PackageJsonScriptsAll', 'ExpoConfigVersions']`
- [ ] `.fingerprintignore` for non-native *file* sources (e.g. `.gitignore`) — see ota skill
- [ ] `eas.json`: `cli.appVersionSource: "remote"` + `autoIncrement: true` on store profiles
- [ ] `scripts/next-version.mjs` + a `resolve-version` job **inside** the prd store workflow —
      never a manual bump sitting next to an automatic build (iOS rejects, Android doesn't)
- [ ] The bump commit lands on **stg**, not `main`; the build stamps the working tree
- [ ] `needs.<resolver>.result == 'success'` on the deploy job — `!cancelled()` does not cover a
      cancelled dependency
- [ ] Release tags are **annotated** (`git tag -a`), or `--follow-tags` pushes nothing
- [ ] Ship the fingerprint-config + version decouple **with a full build**, then verify the build's
      CI `Resolved runtime version` matches `fingerprint:generate`
