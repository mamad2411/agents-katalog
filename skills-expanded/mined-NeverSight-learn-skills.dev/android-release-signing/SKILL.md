---
name: android-release-signing
description: Verify and fix Android release signing for any Expo/React Native build. Use when Play Console rejects an upload with "signed in debug mode", when a CI-built APK/AAB needs its signer certificate checked, when a release-signing config plugin seems to inject signing wrong, or when jarsigner vs apksigner verification is needed. Not project-specific.
---

# Android release signing

Play Console rejects any APK/AAB signed with the **debug keystore** ("You
uploaded an APK or Android App Bundle that was signed in debug mode"). The
fix is always: sign with the project release keystore, then **prove it on the
artifact itself** — never trust the workflow config alone. A build that
"BUILD SUCCESSFUL" can still produce a debug-signed artifact.

## Steps

### 1. Choose the verifier by artifact type

| Artifact | Verifier | Why |
| --- | --- | --- |
| `.apk` | `apksigner verify --print-certs` | apksigner only reads APKs |
| `.aab` | `jarsigner -verify -certs -verbose` | AAB is a JAR archive — **apksigner throws `ApkFormatException: Missing AndroidManifest.xml` on it** and the workflow fails even though signing is correct |

Completion criterion: you know which verifier matches the artifact and can
explain why the other one fails on it.

### 2. Run the verification

APK (`$ANDROID_HOME` is set on GH runners; locally use the keystore path):

```bash
APKSIGNER=$(ls "$ANDROID_HOME"/build-tools/*/apksigner | sort -V | tail -1)
"$APKSIGNER" verify --print-certs app/build/outputs/apk/release/app-release.apk
```

AAB (jarsigner needs a JDK, which the workflow already sets up):

```bash
jarsigner -verify -certs -verbose app/build/outputs/bundle/release/app-release.aab 2>&1 | grep -E "CN=|jar verified"
```

**Read the result**: the signer cert of the Android debug keystore is
`CN=Android Debug, OU=Android, O=Google Inc, ...`. Any other CN = release
signed. In CI, wrap this in a fail-if-debug check:

```bash
if jarsigner -verify -certs -verbose app/build/outputs/bundle/release/app-release.aab 2>&1 | grep -q "CN=Android Debug"; then
  echo "::error::AAB is signed with the DEBUG keystore — release signing was not applied"
  exit 1
fi
```

Completion criterion: you can state the actual signer CN of the artifact and
whether it is debug or release.

### 3. If it is debug-signed, trace the injection chain

Check in order — the bug is almost always one of these:

1. **Plugin not registered** — the release-signing config plugin must be
   listed in `app.json` → `plugins` (Expo). Prebuild regenerates `android/`
   on every build, so any hand edit to `build.gradle` is lost.
2. **Env vars missing at prebuild time** — the plugin is a **no-op** when
   `ANDROID_KEYSTORE_FILE/PASSWORD/ALIAS/KEY_PASSWORD` are absent. They must
   be set on the `expo prebuild` step, sourced from CI secrets (never write
   the keystore or password into the repo).
3. **String-replace anchor bug** — a plugin that edits `build.gradle` by
   locating `release {` will match the **`signingConfigs.release` block it
   just injected** (the first `release {` in the file) instead of
   `buildTypes.release`. Result: the `debug` buildType gets the release
   config and `release` keeps `signingConfigs.debug` — the exact Play
   Console rejection. Fix: search for `release {` **only inside the
   `buildTypes {` block** (anchor on `buildTypes {` first).
4. **Gradle `file(...)` path resolution** — in `android/app/build.gradle`,
   `file('release.keystore')` resolves relative to the **module dir**
   (`android/app/`), not the repo root. A relative path points at
   `android/app/release.keystore` (missing → build fails, or silently wrong).
   Pass an **absolute path** in CI: `ANDROID_KEYSTORE_FILE:
   ${{ github.workspace }}/release.keystore`.

Completion criterion: you can point at the exact broken link (plugin
registration / env / anchor / path) and have a fix that provably changes the
generated `build.gradle`.

### 4. Prove the fix locally before rebuilding CI

Reproduce the CI exactly with a throwaway keystore:

```bash
CI=1 ANDROID_KEYSTORE_FILE="$PWD/test.keystore" ANDROID_KEYSTORE_PASSWORD=x \
  ANDROID_KEY_ALIAS=x ANDROID_KEY_PASSWORD=x \
  npx expo prebuild --platform android --clean --no-install
grep -A2 "buildTypes" android/app/build.gradle
```

The generated file must show `debug → signingConfigs.debug` **and**
`release → signingConfigs.release`. If not, the fix is wrong — do not push.

Completion criterion: `grep` on the prebuilt `build.gradle` shows the release
buildType pointing at `signingConfigs.release`.

### 5. Rebuild in CI and re-verify

Push / dispatch the workflow, then re-run step 2 on the **new artifact**.
The verify step failing the build is the correct outcome for a bad artifact —
don't disable it to "make CI green".

Completion criterion: the new artifact's signer CN is the release keystore's
CN (not "Android Debug"), confirmed by the CI verify step passing.

## Reference

- **Debug keystore signature**: `CN=Android Debug, OU=Android, O=Google Inc, L=Mountain View, ST=California, C=US`
- **Inspect a local keystore**: `keytool -list -v -keystore <file> -alias <alias> -storepass <pass>` (verify alias/password before blaming CI)
- **Play Console wording → meaning**:
  - "signed in debug mode" → artifact used the debug keystore (plugin anchor / env / path bug, not the build itself)
  - any other upload error → read the full message; usually unrelated to signing
- **Workflow pattern** (any repo with this setup):
  decode the keystore secret (e.g. `ANDROID_KEYSTORE_BASE64`) → `> release.keystore` → pass absolute path + passwords as env to `expo prebuild` → gradle build → verify step → upload.
- The keystore itself must stay **outside the repo** (gitignored) and in CI
  secrets — losing it means losing the ability to update the app.
