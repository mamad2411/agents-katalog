---
name: flutter-signing
description: Audit, set up, and rotate Flutter app signing and store credentials — Apple certificates, provisioning profiles, App Store Connect API keys, APNs keys, Android upload keystores, Play App Signing, and Play service accounts. Produces a secret inventory with owner, location and expiry. Usage — /flutter-signing <sub-command> [args]
argument-hint: <audit|setup|rotate> [ios|android|<credential>]
arguments:
  - name: subcommand
    description: "Sub-command: audit, setup, rotate"
  - name: args
    description: "For setup: ios or android. For rotate: upload-key, distribution-cert, asc-api-key, apns-key, play-service-account, keystore-password, app-signing-key"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(git ls-files *)
  - Bash(git log *)
  - Bash(git check-ignore *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(cat *)
  - Bash(date *)
  - Bash(openssl *)
  - Bash(keytool *)
  - Bash(security *)
  - Bash(plutil *)
  - Bash(fastlane *)
---

# Flutter Signing & Store Credentials

Signing credentials are the part of a mobile project with no undo. A lost upload key, a
revoked shared certificate, or a store account tied to a person who left are all recoverable
only through a support ticket, or not at all.

The failure mode in practice is never theft. It is **an expiry nobody owned** — a push
certificate that lapsed on a date not in anyone's calendar, an API key held by one developer.
Every output of this command therefore names an **owner** alongside every credential.

Sub-command is `$ARGUMENTS[0]`. Remaining words are `$ARGUMENTS` minus the first token.

| Sub-command | Purpose |
|---|---|
| `audit` | Inspect this repo and report every credential — owner, location, expiry, what is missing |
| `setup ios` \| `setup android` | Walk the first-time credential setup for one platform |
| `rotate <credential>` | Rotate or replace one credential, with its blast radius stated first |

---

## Rules that apply to every sub-command

**Never instruct the user to commit a secret.** Keystores (`.jks`, `.keystore`), Apple keys
(`.p8`), certificates and their private keys (`.p12`), `key.properties`, and Google service
account JSON never enter the repository — not in a branch, not "temporarily", not encrypted
with a password that is also in the repo. They live in a secret manager and are materialised
on the runner at build time.

**Firebase config files are not secrets and belong in the repo.** `google-services.json`,
`GoogleService-Info.plist` and `firebase_options.dart` contain public client identifiers that
ship inside the app binary anyway — anyone can extract them from the APK. Access is enforced
by Firebase Security Rules and App Check, not by keeping these files hidden. Committing them
is correct; a `.gitignore` rule for them is a mistake that breaks CI builds. Be precise about
this distinction: developers who have been told "never commit Firebase files" are usually
confusing the client config with the *service account* JSON, which genuinely never belongs in
the repo.

**Never print a secret value.** Report a credential's presence, path, fingerprint, key ID and
expiry. Never `cat` a `.p8`, a keystore, a `key.properties`, or a `.env` with real values into
the transcript — the transcript is less protected than the file was.

**Reproducible from secrets, on any machine.** "It signs on my Mac" is not a release process.
Signing must work on a clean runner from stored secrets alone — via `fastlane match` or an
explicit import step in CI.

---

## Decide these first — they are permanent

Raise any of these that is still open before running `setup`. Each one is expensive or
impossible to reverse after the first store submission.

| Decision | Why it is permanent |
|---|---|
| **Bundle ID / package name** | Cannot be changed after publishing. A new ID is a new listing: zero installs, zero reviews, zero ranking, and existing users are not migrated. |
| **Apple enrolment type** | An *individual* enrolment cannot add team members, cannot use App Store Connect roles, and converting to *organization* requires a D-U-N-S number and an Apple-side migration. Choose organization if more than one person will ever touch this. |
| **Account Holder** | One person per Apple team; transferring is an Apple support process. Must be a company-controlled identity. |
| **Flavor suffix scheme** | Each flavor is a distinct bundle ID, App ID, provisioning profile and Firebase app. Fix the scheme now: `com.company.app` for production, `com.company.app.dev` / `.staging` for the rest. Production must not carry a suffix — you cannot remove one later. |

**Store accounts belong to company-controlled role addresses, not a person's Apple ID.**
This is the single most common irreversible mistake in small teams, and it surfaces the week
someone leaves: the Apple ID is personal, the two-factor device leaves with them, the
recovery email is their private one, and the App Store Connect account holder is now
unreachable. Use `developer@company.com` / `play@company.com` — a mailbox the company owns,
with two-factor bound to a shared device or a hardware key held by more than one person, and
the recovery contacts set to other company addresses. If the accounts are already on a
personal Apple ID, transferring them is an Apple support process — start it now, not later.

---

## `/flutter-signing audit`

Inspect the actual repository. Report what exists, what is missing, and what expires. Do not
assume; every line of the output must come from a file that was read or a command that ran.

### Step 1 — Map the project

```bash
ls -d ios android 2>/dev/null
grep -rn "applicationId\|namespace" android/app/build.gradle* | head
grep -rn "PRODUCT_BUNDLE_IDENTIFIER" ios/Runner.xcodeproj/project.pbxproj | sort -u
grep -rn "flavorDimensions\|productFlavors" -A 20 android/app/build.gradle* | head -40
ls ios/*.xcconfig ios/Flutter/*.xcconfig 2>/dev/null
```

Record every bundle ID and package name found. Each flavor multiplies the credential set:
one App ID and one provisioning profile per flavor, one Firebase app per flavor.

### Step 2 — Find credential material on disk

```bash
find . -path ./build -prune -o \
  \( -name '*.jks' -o -name '*.keystore' -o -name '*.p12' -o -name '*.p8' \
     -o -name '*.cer' -o -name '*.mobileprovision' -o -name 'key.properties' \
     -o -name 'Matchfile' -o -name 'Appfile' -o -name 'Fastfile' \) -print 2>/dev/null

ls android/key.properties android/app/*.jks 2>/dev/null
grep -rn "signingConfigs" -A 15 android/app/build.gradle* 2>/dev/null
grep -rln "CODE_SIGN_STYLE\|DEVELOPMENT_TEAM\|PROVISIONING_PROFILE_SPECIFIER" ios/ 2>/dev/null
```

Also read the CI workflow — it names every secret the release actually depends on:

```bash
ls .github/workflows/*.y*ml codemagic.yaml bitrise.yml .gitlab-ci.yml 2>/dev/null
grep -rn "secrets\.\|\$\{\{ *secrets" .github/workflows/ 2>/dev/null
```

A secret referenced by CI but absent from the inventory is a finding, not a gap in the audit.

### Step 3 — Tracked-file check (do not read `.gitignore` for this)

**A `.gitignore` rule has no effect on a file that is already tracked.** Git only consults
ignore rules for *untracked* files. A repo can have `*.jks` in `.gitignore` and a keystore in
every clone, and every tool that reads `.gitignore` will report it as safe. Check the index of
tracked files instead:

```bash
# What git actually tracks, regardless of any ignore rule
git ls-files -- \
  '*.jks' '*.keystore' '*.p12' '*.pfx' '*.p8' '*.pem' '*.key' \
  '*.cer' '*.certSigningRequest' '*.mobileprovision' \
  'android/key.properties' '**/key.properties' \
  '*.env' '.env' '.env.*' '**/.env' '**/.env.*' \
  '**/*service-account*.json' '**/*serviceaccount*.json' '**/*-key.json'
```

Any path returned is a **BLOCKER**. For each one, establish two further facts:

```bash
# Is there an ignore rule that everyone believes is protecting this file?
git check-ignore -v <path>          # a rule here + tracked above = the rule is inert

# Was it ever committed? (present in history = present in every clone and fork)
git log --oneline -1 -- <path>
```

Report the combination explicitly, because it is the one people get wrong:

> `android/app/upload-keystore.jks` is **tracked** (`git ls-files`) *and* matched by
> `.gitignore:12:*.jks`. The ignore rule is inert — it was added after the file was committed.
> `git rm --cached` alone removes it from future commits but **not from history**; anyone with
> a clone or fork still has the key. Treat the key as compromised: rotate it
> (`/flutter-signing rotate upload-key`), then purge history with `git filter-repo`.

Do not run history rewrites or `git rm` as part of an audit. Report and recommend.

Also flag the inverse: `google-services.json` or `GoogleService-Info.plist` listed in
`.gitignore` or absent from `git ls-files`. These *should* be tracked; excluding them breaks
clean-checkout builds and is a symptom of the secret/config confusion above.

### Step 4 — Read expiry from the artifacts, never from memory

```bash
# Apple certificates installed locally
security find-identity -v -p codesigning

# A certificate file's real validity window
openssl x509 -in <cert>.cer -inform DER -noout -subject -enddate -fingerprint

# A provisioning profile's expiry, its App ID and the certificates it is built on
security cms -D -i <profile>.mobileprovision | plutil -p - \
  | grep -E 'ExpirationDate|application-identifier|TeamIdentifier|Name'

# Android keystore: validity, alias, SHA-256 fingerprint (never the password)
keytool -list -v -keystore <path>.jks -alias <alias>
```

| Credential | Typical lifetime | Notes |
|---|---|---|
| Apple distribution certificate | 1–3 years by type | Never assume — read `notAfter`. Shared across the team. |
| Provisioning profile | 1 year, and dies with its certificate | Regenerate after any App ID change |
| App Store Connect API key (`.p8`) | No expiry; revocable | Key ID + Issuer ID are needed with it |
| APNs auth key (`.p8`) | Never expires | One per team, both sandbox and production |
| APNs push certificate | 1 year | The classic unowned expiry — prefer the auth key |
| Android upload key | Whatever validity was set | Play requires validity past 22 Oct 2033 |
| Play app signing key | Permanent, held by Google | Not yours to rotate |
| Play service account key | No expiry unless org policy sets one | Check for a 90-day key-expiry org policy |

Also check the Play `targetSdk` deadline, which blocks *updates* — not just new apps:

```bash
grep -rn "targetSdk\|targetSdkVersion" android/app/build.gradle* android/build.gradle*
```

Compare against Play's current requirement (an annual deadline, historically 31 August with an
extension window to 1 November). If the app is at or below the threshold, that is a WARNING
with a date and an owner — not an INFO.

### Step 5 — Emit the secret inventory

This table is the deliverable. Every row has an owner; an owner of `—` is itself a finding.

```markdown
# Signing Inventory — <app name>
_Date: <today>_ · _Bundle IDs: <list>_

| Credential | Where it lives | Owner | Expires | Recovery if lost | Status |
|---|---|---|---|---|---|
| App Store Connect API key (.p8) | 1Password `Mobile/ASC` + CI secret `ASC_KEY_P8` | Platform team | Never (revocable) | Revoke in ASC, issue new key | ✅ |
| ASC key ID / issuer ID | CI secrets `ASC_KEY_ID`, `ASC_ISSUER_ID` | Platform team | — | Readable in ASC | ✅ |
| Apple distribution certificate | fastlane match repo (private) | Account Holder | 2027-03-14 | Re-issue; invalidates team profiles | ⚠️ 61 days |
| Provisioning profile (prod) | fastlane match repo | Account Holder | 2026-11-02 | Regenerate from App ID | ⚠️ 60 days |
| APNs auth key (.p8) | 1Password `Mobile/APNs` | Platform team | Never | Revoke + re-issue, update Firebase | ✅ |
| Android upload keystore | 1Password `Mobile/Upload Key` + CI `ANDROID_KEYSTORE_B64` | Platform team | 2052-01-08 | Play support key reset (days) | ✅ |
| Keystore + key passwords | CI secrets `KEYSTORE_PASSWORD`, `KEY_PASSWORD` | Platform team | — | None — lost = key unusable | ✅ |
| Play app signing key | Held by Google | Google | Permanent | N/A — this is the point of enrolling | ✅ |
| Play service account JSON | CI secret `PLAY_SERVICE_ACCOUNT_JSON` | Platform team | No expiry | Create new key in GCP + re-grant in Play Console | ✅ |
| Apple / Play account owner | developer@company.com (role address) | Finance + Platform | — | Apple support transfer | ❌ personal Apple ID |
| Play targetSdk deadline | android/app/build.gradle | — | 2026-08-31 | Ship an update before the date | ❌ no owner |

**Legend:** ✅ present and healthy · ⚠️ expires within 90 days or partially owned · ❌ missing, unowned, or wrong

## Findings

### BLOCKER
1. `android/app/upload-keystore.jks` is tracked in git despite `.gitignore:12`. Rotate + purge history.

### WARNING
2. Distribution certificate expires in 61 days with no calendar entry.
3. `targetSdk 34` — below Play's requirement from <date>. Updates will be rejected after it.

### INFO
4. Push notifications use a per-app push certificate; an APNs auth key would remove an annual expiry.
```

Rules for the report:

- **Anything absent is a row, not an omission.** A missing App Store Connect API key gets a
  row with Status `❌` and a recovery path, so it appears in the count.
- Severity is driven by consequence: a secret in the repo or an unowned expiry is a BLOCKER or
  WARNING; a stylistic preference is INFO.
- Give expiries as both a date and a days-remaining number. "2026-11-02" gets calendared;
  "60 days" gets acted on.

Write the inventory to `docs/signing-inventory.md` if the user wants it tracked. It contains
locations and expiries — never values — so it is safe to commit.

---

## `/flutter-signing setup ios`

### 1. Confirm the permanent decisions above

Enrolment type, Account Holder, role address, bundle IDs per flavor. Do not continue past an
open one.

### 2. Understand the identity chain before touching Xcode

```
certificate (who you are)  +  App ID (what you ship, and its capabilities)
                           +  devices (development only)
                           ↓
                  provisioning profile  →  signed build
```

**Enabling a capability in Xcode changes the App ID but does not regenerate the profile.** Add
push notifications, App Groups, HealthKit or Sign in with Apple, and the App ID gains an
entitlement the existing profile does not carry. Nothing fails at edit time; the build fails
at the signing step with a message about entitlements or a mismatched profile, often on CI
rather than on the machine that made the change. After any capability change: regenerate the
profile (`fastlane match --force`, or the developer portal), then re-run the build.

### 3. Use an App Store Connect API key for CI — never an Apple ID

Users → Integrations → App Store Connect API → generate a key with the **App Manager** role.

Why the API key wins on every CI path:

- **No two-factor prompt.** An Apple ID login from a runner triggers 2FA, which either blocks
  the build or forces a session cookie that has to be refreshed by hand every few weeks.
- **Survives password changes and staff turnover.** It is not bound to a person.
- **Scoped and revocable** — you can revoke this key without disturbing anyone's login.

**The `.p8` downloads exactly once.** Apple does not offer it again. Put it in the secret
manager in the same minute you download it, then delete the local copy. Store the **Key ID**
and **Issuer ID** alongside it — the key is unusable without both.

```bash
# Store all three as CI secrets. The .p8 is base64'd only to survive transport.
base64 -i AuthKey_XXXXXXXXXX.p8 | pbcopy   # paste into the secret manager, then:
rm AuthKey_XXXXXXXXXX.p8                   # never leave it on disk, never add it to git
```

### 4. Distribution certificate — shared, limited, and dangerous to tidy

A team has a small number of distribution certificates and they are shared by everyone.
**Revoking one invalidates every provisioning profile built on it, for everyone** — other apps,
other developers, live CI pipelines, and any in-flight release. Existing App Store builds keep
working, but nothing can be signed again until every affected profile is regenerated.

So: **never revoke a certificate you did not create**, and never revoke one to "clean up"
duplicates. If you need one and the list looks full, ask the Account Holder. Before any
deliberate revocation, tell the user exactly what will break and get explicit confirmation.

### 5. Push — prefer the APNs auth key

Create one **APNs auth key** (`.p8`) for the team: it covers every app in the team, works for
both sandbox and production, and **never expires**. Per-app push certificates expire annually,
on a date nobody has calendared, and the symptom is silent — notifications simply stop being
delivered to production users. This `.p8` also downloads only once.

Upload the key (plus Key ID and Team ID) to Firebase Console → Cloud Messaging if using FCM.

### 6. Make signing reproducible

Either `fastlane match` (certificates and profiles in an encrypted private repo, one command
to import on any runner) or an explicit import step in CI that installs the `.p12` and profile
from secrets into a temporary keychain. Set `CODE_SIGN_STYLE = Manual` for release builds so
the runner cannot silently pick a different identity from Xcode automatic signing.

### 7. Verify

```bash
flutter build ipa --release --export-method app-store
security cms -D -i <profile>.mobileprovision | plutil -p - | grep ExpirationDate
```

Then run `/flutter-signing audit` and confirm every iOS row is `✅` with a named owner.

---

## `/flutter-signing setup android`

### 1. Enrol in Play App Signing

Two keys, and the distinction is the whole point:

| Key | Held by | Rotatable | If lost |
|---|---|---|---|
| **Upload key** | You | Yes | Play support resets it — days, not a dead app |
| **App signing key** | Google | No (Google re-signs every release with it) | Not your problem — Google holds it |

Enrolling converts *unrecoverable key loss* — an app that can never be updated again, by anyone,
for the rest of its life — into **a support ticket**. Enrol. There is no scenario where holding
the only copy of the app signing key yourself is the better trade.

### 2. Generate the upload key

```bash
keytool -genkeypair -v \
  -keystore upload-keystore.jks \
  -alias upload \
  -keyalg RSA -keysize 2048 \
  -validity 10000              # ~27 years; Play requires validity past 2033-10-22
```

Then, in order, in one sitting:

1. Store the keystore file **and** both passwords in the team secret manager — the passwords
   are not recoverable and a keystore without them is scrap metal.
2. Add the base64 of the keystore plus both passwords as CI secrets
   (`ANDROID_KEYSTORE_B64`, `KEYSTORE_PASSWORD`, `KEY_PASSWORD`, `KEY_ALIAS`).
3. Record the SHA-256 fingerprint (`keytool -list -v`) in the inventory — you will need it for
   Firebase, App Links and Play uploads.
4. Confirm the keystore is **not** in the repo: `git ls-files -- '*.jks' '*.keystore'` must be
   empty.

### 3. Wire signing without secrets in the repo

`android/key.properties` is generated at build time and is never tracked:

```properties
storeFile=/path/on/runner/upload-keystore.jks
storePassword=${KEYSTORE_PASSWORD}
keyPassword=${KEY_PASSWORD}
keyAlias=upload
```

`android/app/build.gradle` reads it if present and fails loudly if a release build finds no
signing config — a release that silently falls back to the debug key is rejected by Play at
upload, after the whole pipeline has run.

Confirm both: `key.properties` in `.gitignore`, *and* `git ls-files -- '**/key.properties'`
empty. The second check is the one that matters.

### 4. Firebase config files stay in the repo

`android/app/google-services.json` and `ios/Runner/GoogleService-Info.plist` are committed.
They are client configuration, not credentials. Excluding them breaks clean-checkout CI builds
and buys no security, since the same values are extractable from any shipped APK. Add each
flavor's SHA-256 fingerprint to the Firebase project so App Check and Google Sign-In work per
flavor.

### 5. CI service account — created in Google Cloud, granted in the Play Console

This is a two-system setup and the second half is the step teams miss:

1. **Google Cloud Console** → the project linked to your Play developer account → IAM & Admin
   → Service Accounts → create one → Keys → add key → JSON. The JSON downloads once.
2. **Play Console** → Users and permissions → invite the service account's email → grant app
   access and the release permissions it needs.

Step 1 alone produces a service account that authenticates successfully and then fails every
API call with a permission error, which reads like a broken key rather than a missing grant.
**Permissions are granted in the Play Console, not in Google Cloud IAM.** Grant only the apps
and permissions the pipeline needs — releases to the tracks you use, not account-wide admin.

Store the JSON as a CI secret. It never enters the repo.

### 6. Calendar the `targetSdk` deadline

Play enforces an annual minimum `targetSdk` and blocks *updates* to existing apps once it
passes — so a lapse is discovered at the worst moment, when a fix needs to ship. Put the date
in a shared calendar with a named owner and a reminder a month out, and record it as a row in
the inventory.

### 7. Verify

```bash
flutter build appbundle --release
# Confirm the release used the upload key, not the debug key:
keytool -printcert -jarfile build/app/outputs/bundle/release/app-release.aab
```

---

## `/flutter-signing rotate <credential>`

Rotation is where blast radius matters. **State what breaks, and for whom, before doing
anything.** Ask for explicit confirmation on anything in the "team-wide" column.

| `<credential>` | Blast radius | Path |
|---|---|---|
| `upload-key` | Your uploads only | Generate a new keystore, then Play Console → Setup → App signing → request upload key reset. Google keeps re-signing with the unchanged app signing key, so **users are unaffected**. |
| `app-signing-key` | **Not rotatable by you** | Google holds it. If it must change, Play Console → App signing → key upgrade, which applies to new installs only; old installs keep the old key. Rarely correct. |
| `distribution-cert` | **Team-wide** | Revoking invalidates every profile built on it, for every app and every developer on the team. Create the new certificate *first*, regenerate all profiles, verify a build, and only then revoke — with the Account Holder's agreement. |
| `asc-api-key` | CI only | Generate the new key, update `ASC_KEY_P8` / `ASC_KEY_ID` / `ASC_ISSUER_ID`, run one pipeline green, then revoke the old key. The new `.p8` downloads once. |
| `apns-key` | All apps in the team using it | Create the new key, update Firebase / your push provider, verify a real delivery to a device, then revoke the old one. Revoking first means silently undelivered notifications. |
| `play-service-account` | CI only | New key in Google Cloud → update the CI secret → **re-check the Play Console grant, which does not follow a new key if you also created a new service account** → run one release green → delete the old key. |
| `keystore-password` | Your uploads only | `keytool -storepasswd` / `-keypasswd`, update the CI secrets in the same change. Test a release build before merging — a mismatched password fails at signing, at the end of the pipeline. |

Rotation steps in every case:

1. Say what breaks and who else is affected. Get confirmation for anything team-wide.
2. Create the replacement and store it in the secret manager **before** revoking anything.
3. Update every consumer: CI secrets, `fastlane match`, Firebase, the local `.env.example`
   documentation (names only, never values).
4. Run one full release pipeline green on the new credential.
5. Only then revoke the old credential.
6. Update `docs/signing-inventory.md` — new expiry, new owner, date rotated.

**If a credential is being rotated because it leaked** (found tracked in git, pasted in a
ticket, in a transcript), invert step 5: revoke immediately, then rebuild. And remember that
deleting the file does not remove it from history — every clone and fork still has it, so
rotation, not deletion, is the fix.

---

## Never do this

- Commit a keystore, a `.p12`, a `.p8`, `key.properties`, or a service-account JSON — in any
  branch, in any form, however temporarily.
- Trust `.gitignore` as evidence that a file is not in the repo. Check `git ls-files`.
- Add `google-services.json` or `GoogleService-Info.plist` to `.gitignore` — they belong in
  the repo.
- Use an Apple ID and password for CI when an App Store Connect API key exists.
- Revoke a distribution certificate you did not create, or one you have not confirmed is
  unused by the rest of the team.
- Ship push with a per-app certificate when an APNs auth key would remove the expiry entirely.
- Hold the only copy of an Android app signing key instead of enrolling in Play App Signing.
- Keep store accounts on a personal Apple ID.
- Print a secret value into the transcript while auditing it.
