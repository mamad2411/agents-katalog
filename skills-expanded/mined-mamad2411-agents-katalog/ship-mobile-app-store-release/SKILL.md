---
name: ship-mobile-app-store-release
description: Prepares and ships iOS App Store and Google Play releases — code signing (certs/provisioning, upload vs app-signing keystores), marketing-version/build-number bumps, Fastlane/EAS/Gradle build lanes, TestFlight/Play-track uploads, phased rollout, store metadata, and review-rejection remediation.
when_to_use: Cutting a mobile release — fixing signing or keystores, automating builds with Fastlane/EAS/Gradle, uploading to TestFlight or Play tracks, staged/phased rollout, store listing/metadata, or fixing an App Store/Play review rejection. Distinct from deploy-release (server/web deploys), release-notes (changelog prose), and cicd-pipeline-author (the CI workflow that calls these lanes).
---

## When to Use

Reach for this skill when the artifact is a **store binary** (`.ipa`/`.aab`) headed for Apple or Google review, not a server rollout:

- "Set up code signing / fix `No profiles for 'com.x' were found` / rotate an expired cert"
- "Generate or recover an Android keystore; enroll in Play App Signing; upload key vs app-signing key confusion"
- "Bump the version + build number and ship to TestFlight / Play internal track"
- "Wire up Fastlane (`gym`/`pilot`/`supply`) or EAS (`eas build`/`eas submit`) in CI"
- "Do a phased / staged rollout at 1% → 100%, then halt it"
- "Upload screenshots, description, what's-new, age rating"
- "Our build got rejected for Guideline 4.3 / 5.1.1 / IAP — fix and resubmit"

NOT this skill:
- Deploying a server, web app, or container to prod (blue-green, canary pods) → deploy-release
- Writing the human-facing changelog / what's-new *prose* → release-notes (this skill only *places* the text)
- Authoring the CI YAML that runs these lanes (job graph, caching, secrets injection) → cicd-pipeline-author
- Storing the keystore password / App Store Connect API key safely → secrets-management

## Steps

1. **Set versioning first — two independent numbers, never reused.** Marketing version (user-visible) vs build number (uniqueness). Bump the build number on *every* upload even within the same marketing version; stores reject duplicates.

   | Field | iOS (`Info.plist`) | Android (`build.gradle`) | Rule |
   |---|---|---|---|
   | Marketing version | `CFBundleShortVersionString` | `versionName` | SemVer `1.4.0`, free-form |
   | Build number | `CFBundleVersion` | `versionCode` | **Must strictly increase per upload.** iOS: any string with increasing numerics. Android: a single **integer**, monotonic, max 2.1B |

   Default: derive build number from CI run number or commit count (`git rev-list --count HEAD`) so it auto-increments and is reproducible. Use Fastlane `increment_build_number` / `increment_version_code` — never hand-edit and forget.

2. **iOS signing — prefer Fastlane `match`, not Xcode "Automatically manage signing", for CI.** You need a **Distribution certificate** (`.p12`) + an **App Store provisioning profile** bound to the explicit App ID and that cert.

   - `match` stores certs/profiles encrypted in a private git repo (or S3/GCS), so every machine/CI agent shares one cert instead of each minting a new one (Apple caps you at 2–3 distribution certs).
   - Authenticate CI with an **App Store Connect API key** (`.p8` + key id + issuer id) via `app_store_connect_api_key` — not your Apple ID password / 2FA, which breaks unattended.
   - Match entitlements to enabled capabilities: Push → `aps-environment: production` in the **release** entitlements; App Groups, Sign in with Apple, Associated Domains must each be toggled on the App ID *and* present in the profile, or the build is signed but the feature silently fails.
   ```bash
   # one-time, populates the encrypted repo
   bundle exec fastlane match appstore
   # CI: fetch read-only, never regenerate on agents
   bundle exec fastlane match appstore --readonly
   ```

3. **Android signing — separate the upload key from the app-signing key.** Enroll in **Play App Signing**: Google holds the *app-signing key* and re-signs your `.aab`; you sign uploads with an *upload key* you control. Losing the upload key is recoverable (reset via support); losing the app-signing key without Play App Signing is fatal — you can never update the app.

   ```bash
   keytool -genkeypair -v -keystore upload.keystore -alias upload \
     -keyalg RSA -keysize 2048 -validity 9125 -storetype PKCS12   # 25-yr validity
   ```
   - Ship **`.aab`** (App Bundle), not `.apk` — Play requires it for new apps and generates per-device APKs.
   - Keystore password, key password, alias → secrets store / env, never committed (see secrets-management). Gradle reads them from `~/.gradle/gradle.properties` or env, not `build.gradle`.

4. **Automate the build + upload with one lane per store.** Decide the toolchain up front:

   | Stack | Build | Upload | Use when |
   |---|---|---|---|
   | Native iOS | `gym` (`build_app`) → `.ipa` | `pilot` (`upload_to_testflight`) / `deliver` (`upload_to_app_store`) | Bare Xcode project, full control |
   | Native Android | `gradle bundleRelease` → `.aab` | `supply` (`upload_to_play_store`) | Bare Gradle project |
   | Expo / RN managed | `eas build -p ios\|android` | `eas submit -p ios\|android` | Expo-managed; EAS handles signing |

   Default to **Fastlane** for bare native and **EAS** for Expo-managed. Minimal Fastfile lanes:
   ```ruby
   lane :beta do                          # iOS → TestFlight
     match(type: "appstore", readonly: true)
     increment_build_number(xcodeproj: "App.xcodeproj")
     build_app(scheme: "App", export_method: "app-store")
     upload_to_testflight(skip_waiting_for_build_processing: true)
   end
   lane :play_internal do                 # Android → internal track
     gradle(task: "bundle", build_type: "Release")
     upload_to_play_store(track: "internal", aab: "app/build/outputs/bundle/release/app-release.aab")
   end
   ```
   For `supply` you need a **Play Developer API service-account JSON** (`json_key`) with Release Manager permission. For EAS submit, store the same Apple/Google creds in EAS secrets.

5. **Distribute through the right track, then promote — don't ship straight to production.**

   | Store | Tracks (narrow → wide) | Notes |
   |---|---|---|
   | TestFlight | Internal (≤100, no review) → External (review, up to 10k via groups/public link) | Internal testers see builds in minutes; external needs Beta App Review |
   | Play | `internal` → `closed` (alpha/beta) → `open` (beta) → `production` | Promote the *same* build between tracks; don't rebuild |

   Default flow: upload to TestFlight Internal / Play `internal` first, smoke-test, then promote. Gate external/production behind a manual approval.

6. **Roll out in stages with a percentage, never 100% on day one.**
   - **Play:** set `rollout: 0.01` (1%) on the `production` track via `upload_to_play_store(rollout: "0.01")`, then bump `0.01 → 0.05 → 0.2 → 0.5 → 1.0` over days, watching crash-free rate between steps.
   - **iOS:** App Store "Phased Release for Automatic Updates" ramps over 7 days automatically (≈1/2/5/10/20/50/100%). Enable it in App Store Connect or via `deliver`'s phased-release flag; it only covers auto-updaters, manual updaters get it immediately.

7. **Fill store metadata so review doesn't bounce on format.** Required: localized title/description, **what's-new** for this version, keywords (iOS), category, **age/content rating** questionnaire, privacy nutrition label (iOS `App Privacy`) / Play **Data safety** form, and **screenshots at every required device size** (e.g. iOS 6.7" + 6.5"; missing a required size blocks submission). Automate text/screenshot upload with `deliver`/`supply` (`metadata/`, `screenshots/` dirs) so it's version-controlled, not hand-pasted.

8. **Pre-flight against the top rejection reasons before you submit.** Address these in the binary/listing, not after a 1-week review round-trip:

   | Reason | Apple guideline | Fix |
   |---|---|---|
   | Crash / broken on review device | 2.1 | Test on a clean device + the OS in review; provide working demo creds |
   | Hidden/incomplete features ("placeholder") | 2.1 | No dead buttons, no "coming soon"; ship only finished flows |
   | Spam / thin / web-wrapper | 4.3 / 4.2 | Native value beyond a website wrapper |
   | Login wall with no demo account | 5.1.1 / 2.1 | Put **demo username+password** in Review Notes |
   | Sign in with Apple missing | 4.8 | Required if you offer 3rd-party social login |
   | Buying digital goods outside IAP | 3.1.1 | Digital content must use StoreKit IAP, not external payment |
   | Privacy label mismatch | 5.1 | Declared data collection must match actual SDK behavior |

   Play parallels: target the **current required API level** (`targetSdkVersion`), complete Data safety honestly, declare sensitive permissions, no deceptive metadata. Put credentials and any special-access steps in the review notes field.

9. **After release, watch crash-free rate and keep the halt path one command away.** Monitor crash-free *sessions* (target **≥ 99.5%**) and ANR rate in Crashlytics / Play vitals during ramp. If it regresses below threshold: **Play** → halt rollout in Console or `upload_to_play_store(rollout:)` won't un-ship, so use **"Halt rollout"** (stops further % but doesn't pull installed users) then ship a fixed build. **iOS** → "Pause Phased Release" in App Store Connect; to actually pull a broken build you must **expedite a new build through review** (Apple has no instant rollback). Plan a hotfix lane, not a rollback button.

## Common Errors

- **Reusing a build number.** `ERROR ITMS-90186 / "Version already exists"` (iOS) or `Version code N has already been used` (Play). Always increment per upload, even for the same marketing version.
- **Each CI agent minting its own distribution cert.** Hits Apple's 2–3 cert cap, then nothing can sign. Use `match --readonly` so agents fetch one shared cert.
- **Apple ID + password (not API key) in CI.** Breaks on 2FA prompts. Use an App Store Connect API key (`.p8`).
- **Committing the keystore or its passwords.** Anyone with the repo can sign as you. Keystore + passwords go to a secrets store; `.gradle` properties out of VCS.
- **Treating the upload key as the app-signing key.** With Play App Signing, Google re-signs; the key in your keystore is only the *upload* key. Don't panic-rotate the wrong one — resetting the upload key is a support flow, not a config change.
- **Shipping `.apk` to a new Play app.** Rejected — new apps require `.aab`. Use `bundleRelease`, not `assembleRelease`.
- **Entitlement enabled in Xcode but not on the App ID / profile.** Signs fine, feature dead at runtime (push silently drops, App Group reads empty). Toggle the capability on the App ID and regenerate the profile.
- **`aps-environment: development` in a store build.** Push notifications work in debug, fail in production. Release entitlements must use `production`.
- **Missing a required screenshot size.** Submission blocked with no obvious cause. Supply every required device dimension for the platform.
- **100% rollout on day one.** A crash hits every user at once with no staged escape. Start at 1% and ramp.
- **Expecting an instant rollback.** Neither store has one. iOS needs an expedited re-review; Play halt only stops *new* installs. Always keep a hotfix lane ready.
- **Login-walled app with no demo credentials.** Auto-reject under 5.1.1/2.1. Reviewer can't get past the login. Put working creds in Review Notes.

## Verify

1. **Versioning:** the build number is strictly greater than the last accepted upload (check App Store Connect / Play Console history); marketing version is correct.
2. **iOS signing:** `codesign -dvv <App>.app` shows the **Distribution** cert and the explicit App ID; the embedded profile is the App Store profile and not expired (`security cms -D -i embedded.mobileprovision`).
3. **Android signing:** `jarsigner -verify -verbose app-release.aab` (or `apksigner verify` on a built APK) passes with the **upload** key; the app is enrolled in Play App Signing.
4. **Entitlements:** `codesign -d --entitlements - <App>.app` lists every capability the app uses, with `aps-environment: production` for a store build.
5. **Upload landed:** the build appears in TestFlight Internal / the target Play track and finishes processing without an email rejection (ITMS-* / Play pre-launch report clean).
6. **Metadata complete:** what's-new, all required screenshot sizes, age/content rating, and the privacy/Data-safety form are filled — the submit button is enabled with no blocking warnings.
7. **Rollout staged:** production is at the intended start percentage (e.g. 1%), not 100%, and the phased/staged toggle is on.
8. **Post-release watch:** crash-free sessions and ANR are visible on a dashboard, and you've confirmed the halt/pause control works (locate it, don't trigger it).

Done = a binary with a unique, increasing build number is correctly signed (distribution cert + production entitlements / upload key + Play App Signing), uploaded to the intended track with complete metadata, rolling out at a staged percentage, and the crash-free monitor + halt path are both confirmed available.
