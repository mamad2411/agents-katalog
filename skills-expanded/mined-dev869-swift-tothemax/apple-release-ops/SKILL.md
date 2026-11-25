---
name: apple-release-ops
description: >-
  The mechanics of shipping Apple apps. Use for ANY code signing error ("no signing certificate",
  "provisioning profile doesn't include...", "revoked certificate"), provisioning profiles,
  certificates, entitlements, capabilities, TestFlight (groups, expiry, feedback), App Store
  Connect, uploading builds, xcodebuild archive/-exportArchive, exportOptionsPlist, altool/
  notarytool/Transporter, fastlane (match/gym/pilot/deliver), Xcode Cloud, CI/CD for iOS/macOS
  (GitHub Actions, keychains on runners), version and build numbers (agvtool,
  CURRENT_PROJECT_VERSION, MARKETING_VERSION), phased release and halting a rollout, app metadata
  and screenshots, App Store Connect API keys/webhooks, crash reports and crash spikes, and macOS
  notarization/stapling. Trigger on any release, distribution, or signing task — even a single
  cryptic Xcode signing error. NOT for App Review rejection strategy (use app-review-max) or
  privacy policies/legal (use apple-legal-max).
---

# Apple Release Ops

You own the pipeline: signed binary → TestFlight → App Store → monitored release. As of July
2026: Xcode 26.6 (Swift 6.3, iOS 26.5 SDK, requires macOS Tahoe 26.2+). Sibling skills own
review strategy (`app-review-max`) and legal/compliance (`apple-legal-max`) — route there, don't
improvise.

## Signing, demystified

Four artifacts, four jobs. Most "signing hell" is conflating them:

| Artifact | What it is | Where it lives |
|---|---|---|
| **Certificate** | Your identity (public key signed by Apple + your private key) | Keychain. Private key is the part you can lose. |
| **Provisioning profile** | Apple's permission slip: this cert + this app ID + these entitlements (+ these devices, for dev/ad-hoc) | `~/Library/Developer/Xcode/UserData/Provisioning Profiles/` (Xcode 16+; formerly `~/Library/MobileDevice/`) |
| **Entitlements** | Key-value claims baked into the binary at sign time (`.entitlements` file) | Inside the signed binary. Inspect: `codesign -d --entitlements - MyApp.app` |
| **Capability** | App Store Connect / Xcode UI switch that regenerates the app ID config and profiles | Developer portal |

Rules that resolve 90% of confusion:

- Every entitlement your binary claims MUST be allowed by the profile it ships with. Mismatch =
  install/upload failure, not a build failure.
- Distribution profiles have no device list. "Device not registered" is a development/ad-hoc
  problem only.
- **Cloud-managed certificates** (Xcode 13+, default with automatic signing + "Distribute App"):
  Apple holds the distribution private key. Nothing to back up, nothing to expire out from under
  you, works with `xcodebuild -allowProvisioningUpdates`. Prefer them unless your CI can't
  authenticate to Apple.

**Decision: automatic vs manual signing.**
- Solo dev / small team, Xcode or Xcode Cloud builds → **automatic** + cloud-managed certs. Done.
- Self-hosted CI, multiple apps sharing certs, or extensions with exotic entitlements →
  **manual** with profiles checked into a secrets store, or fastlane `match` (git/S3-backed,
  encrypted). Never both: mixed automatic/manual across targets is the #1 source of phantom errors.
- Wrong: fixing CI signing by exporting your personal dev certificate.
  Right: a dedicated distribution cert (or cloud signing via App Store Connect API key) that no
  laptop depends on.

Deep debugging: `references/signing-troubleshooting.md`.

## The canonical CLI release path

Three commands. Everything else (fastlane, Xcode Cloud) is a wrapper around these.

```bash
# 1. Archive (build once, distribute many)
xcodebuild archive \
  -project MyApp.xcodeproj -scheme MyApp \
  -destination 'generic/platform=iOS' \
  -archivePath build/MyApp.xcarchive \
  -allowProvisioningUpdates \
  -authenticationKeyID "$ASC_KEY_ID" \
  -authenticationKeyIssuerID "$ASC_ISSUER_ID" \
  -authenticationKeyPath "$PWD/AuthKey_$ASC_KEY_ID.p8"

# 2. Export + upload in one step (destination: upload does the upload for you)
xcodebuild -exportArchive \
  -archivePath build/MyApp.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath build/export \
  -allowProvisioningUpdates \
  -authenticationKeyID "$ASC_KEY_ID" \
  -authenticationKeyIssuerID "$ASC_ISSUER_ID" \
  -authenticationKeyPath "$PWD/AuthKey_$ASC_KEY_ID.p8"
```

`ExportOptions.plist` — the method name changed; `app-store` is deprecated:

```xml
<dict>
    <key>method</key><string>app-store-connect</string>   <!-- NOT "app-store" -->
    <key>destination</key><string>upload</string>          <!-- or "export" for an .ipa -->
    <key>manageAppVersionAndBuildNumber</key><true/>
    <key>signingStyle</key><string>automatic</string>
</dict>
```

**Uploading a pre-built .ipa/.pkg** (if you exported instead of uploading):
- `altool` upload is **deprecated**. Do not write new automation on it.
- Use Transporter CLI (`xcrun iTMSTransporter` or Transporter.app) with the same ASC API JWT, or
- Use the **Build Upload API** (App Store Connect API, WWDC25+): create a `buildUploads`
  resource, PUT the asset parts, commit — pure REST, works from any language/runner, structured
  error messages. Prefer this for new tooling.

**Auth everywhere with an App Store Connect API key** (Users and Access → Integrations → Team
Keys, role App Manager). One `.p8` powers xcodebuild, notarytool, fastlane, and raw API calls.
Never use Apple ID + app-specific passwords in new CI — 2FA prompts will break it.

**macOS outside the App Store — notarize or Gatekeeper blocks you:**

```bash
xcrun notarytool store-credentials ci-profile \
  --key AuthKey_XXX.p8 --key-id "$ASC_KEY_ID" --issuer "$ASC_ISSUER_ID"
xcrun notarytool submit MyApp.dmg --keychain-profile ci-profile --wait
xcrun stapler staple MyApp.dmg          # staple the ticket for offline validation
xcrun notarytool log <submission-id> --keychain-profile ci-profile  # on failure
```

Sign with Developer ID Application cert, hardened runtime on (`--options runtime`), before
submitting. Mac App Store builds skip notarization (App Review covers it).

## TestFlight strategy

- **Internal groups** (up to 100 ASC users, 30 devices each): no Beta App Review, builds appear
  in minutes. Enable "automatic distribution" on the group so every upload reaches the team.
  This is your smoke-test tier — every CI build goes here.
- **External groups** (up to 10,000 testers, email or public link): first build of each version
  needs Beta App Review (usually <24h; re-submissions of the same version train are instant).
  Gate by group: `nightly` public-link group ≠ `beta` invited group.
- **Builds expire 90 days after upload.** No extensions. Schedule at least a monthly upload for
  any live beta, or testers go dark.
- **Feedback**: screenshots + crash feedback flow into ASC → TestFlight → Feedback, and are now
  retrievable via the **Feedback API**; configure **webhooks** (ASC API) for build-processing and
  beta-state events instead of polling.
- Wrong: testing a release candidate only via external group and waiting on Beta App Review.
  Right: internal group for the RC same-hour, external for the soak.

## Version & build number discipline

Two numbers, two audiences:
- `MARKETING_VERSION` (CFBundleShortVersionString) — humans. Semver-ish, e.g. `2.4.0`.
- `CURRENT_PROJECT_VERSION` (CFBundleVersion) — App Store Connect. Must be **unique per upload**
  within a version train, and monotonically increasing.

Rules:
- Set `GENERATE_INFOPLIST_FILE`-era targets to read both from build settings; never hand-edit
  Info.plist. `agvtool` still works (`agvtool next-version -all`, `agvtool new-marketing-version
  2.4.0`) but mutates the pbxproj — in CI prefer an override at build time:
  `xcodebuild ... CURRENT_PROJECT_VERSION=$GITHUB_RUN_NUMBER` (or commit count:
  `git rev-list --count HEAD`).
- Or let Apple do it: `manageAppVersionAndBuildNumber` in ExportOptions bumps the build number
  to max(existing)+1 at upload. Fine for solo apps; avoid when build number must match a git ref.
- Every target/extension in the app must share identical version + build numbers or validation
  fails (ITMS-90473 and friends).
- Wrong: timestamp build numbers like `202607011230` — they overflow comparisons and you can
  never insert a build "before" one. Right: small monotonically increasing integer.

## Release strategy

- **Phased release** (App Store version option, iOS/macOS): auto-update users get it over 7 days
  — 1%, 2%, 5%, 10%, 20%, 50%, 100% by day. Manual App Store downloads always get the new
  version immediately, so phased ≠ hidden.
- You can **pause** a phased release for up to 30 days, or "Release to All Users" early. You
  can NOT halt distribution entirely except by **Remove from Sale** (nuclear) or shipping a fix.
- **There is no rollback.** Once approved-and-released, the only way forward is a new build.
  Keep a hotfix branch cut from the release tag; use expedited review (route strategy questions
  to `app-review-max`) for critical fixes.
- **Forced update pattern**: ship a remote-config minimum-version check from v1 (server returns
  `min_supported_build`; app blocks with an "Update" button to the App Store URL). You cannot
  force-update clients that predate the check — ship it before you need it.
- Use **Developer ID / direct distribution** (macOS) when you need same-day fixes with no review.

## Incident triage: crash spike after release

In order — fastest signal first:

1. **Pause the phased release** (ASC → App Store → version → Pause). Buys time; stops auto-update
   spread. Do this before diagnosing if the spike is real.
2. Xcode Organizer → Crashes (or ASC → Analytics → Metrics → Crashes): is the spike one
   signature or diffuse? One signature + new OS version = OS-specific regression; diffuse =
   likely bad build/misconfigured backend.
3. Check the crashed thread's frames are symbolicated — if not, you didn't upload dSYMs
   (archive keeps them at `MyApp.xcarchive/dSYMs/`; crash reporters need them uploaded per-build).
4. Cross-check MetricKit (`MXCrashDiagnostic`) / third-party reporter for the same window —
   Organizer data lags hours; your own pipeline is near-real-time.
5. Correlate with the diff: `git log lastTag..thisTag -- <subsystem from crash frames>`.
6. Decide: fix-forward build (same version train, bump build number, expedited review) vs.
   server-side kill-switch/remote-config disable of the offending feature. Prefer the
   kill-switch you shipped in advance.
7. If the bad version must stop spreading and no fix is ready: Remove from Sale, understanding
   existing users keep the app.

## References

Read the matching file before deep work — they carry the exact commands and current specs:

- `references/ci-recipes.md` — GitHub Actions pipeline (keychain setup, ASC key auth, SPM
  caching, macOS runner realities), Xcode Cloud decision guide, fastlane equivalents.
- `references/signing-troubleshooting.md` — decision tree for every classic signing error,
  `codesign`/`security` forensics, CI keychain pathologies.
- `references/store-presence.md` — metadata field limits, 2026 screenshot specs, privacy label
  upkeep, phased release + review windows, replying to reviews via API, crash/metric triage.

## Companions & orchestration

Part of the swift-tothemax plugin — `apple-dev-conductor` routes multi-facet tasks. Siblings: `app-review-max` is the gate before every submission this skill uploads; `apple-legal-max` supplies the privacy/label inputs entered in App Store Connect.
Ecosystem companions (delegate if installed): `xcode-build-fixer` and its siblings for build failures and build-time optimization; `asc-metadata-sync` and the rudrankriyam ASC CLI suite for scripted metadata/localization ops; `xcode-project-setup` (firebase) when Firebase is in play. Command syntax here is verified against Xcode 26.6 — prefer it over older companion invocations.
