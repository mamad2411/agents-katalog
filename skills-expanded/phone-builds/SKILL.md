---
name: phone-builds
description: Build an Expo / React Native app for a real phone with the `phone-build` command - an iOS .ipa for the user's iPhone or TestFlight, an Android .apk/.aab - and upload it to TestFlight or Google Play. The month's free EAS cloud builds go first, then the build runs on this machine (Android here, iOS on macbox's macOS VM). Use it for "build it for my phone", "an IPA", "install it on my iPhone", "TestFlight", "a build to share", "an APK". For running and checking the app on simulators, use the simulators skill instead.
---

# Phone builds

UI work is checked on the simulators (the `simulators` skill). A phone build is for what a simulator can't show: the app on the user's own iPhone, a TestFlight build, a store upload.

## How it works

`phone-build` runs EAS builds with the app's `eas.json` profiles and EAS-managed signing, in one of two places:

1. **The EAS cloud, while the month's free builds last.** Expo's Free plan includes a small number of iOS and Android builds a month (15 of each as of 2026). They go through a low-priority queue, which can take an hour or more at peak times. `phone-build` reads the account's usage (`eas account:usage`) before each build.
2. **This machine, once they're used up.** Android builds here (`eas build --local`, with the SDK from `android-sim env`). iOS builds on macbox's macOS VM (Xcode), with `eas build --local` there. This route is free and has no queue, and the signing is the same, because EAS holds the certificates and profiles.

`--local` forces the local route, for example when the build is needed now and the cloud queue is long. `--cloud` forces the cloud.

**iOS needs the paid Apple Developer Program.** Without it EAS can't sign builds for a device (a free Apple ID only allows 7-day sideloads, with no push notifications). Until the user has it and has done the one-time setup below, check iOS on the simulators. Android phone builds need no paid account.

## Commands

Run them from inside the app's checkout:

```bash
phone-build doctor                    # what's ready and what's missing; run it first
phone-build quota                     # free cloud builds used this month, per platform
phone-build init                      # once per app: link it to EAS (eas init) and write eas.json; commit eas.json
phone-build ios [profile]             # build (default profile: preview): cloud while free builds last, else on the Mac
phone-build android [profile]         # the same for Android (local builds run here)
phone-build ios production --local    # force local; --cloud forces the cloud; --no-wait returns with the build's page
phone-build submit ios [file.ipa]     # upload to TestFlight: a local .ipa, or the latest cloud build
phone-build submit android [file.aab] # upload to Google Play's internal track
phone-build device                    # register an iPhone for internal builds: prints a link the user opens on the phone
```

Local builds are written to `$PHONE_BUILD_OUT/<checkout>/` (default `$TMPDIR/phone-build/`), and the command prints the path. Cloud builds print their page on expo.dev, which has the install link and QR code. For anything deeper about eas.json, versions or store metadata, see Expo's EAS documentation (or its `eas-app-stores` skill, if installed).

## Profiles (from `phone-build init`)

| Profile | What it is | How it reaches the phone |
|---|---|---|
| `development` | A development client: the app's native code with Expo's dev menu. It loads the JavaScript from a Metro server, so JS edits arrive without a rebuild. | Internal distribution: the build's install link, on a registered iPhone with Developer Mode on. Metro runs on this machine; a phone away from it needs a tunnel to Metro. |
| `preview` | A standalone internal build with the JavaScript inside. This is the default. | Internal distribution: the install link on a registered iPhone; an `.apk` on Android. |
| `production` | The store build (version numbers increase on their own). | `phone-build submit` → TestFlight / Google Play internal testing. |

A locally built iOS `preview`/`development` `.ipa` has no install link yet. Build it in the cloud, or use `production` and TestFlight.

## The user's one-time setup

Agents can't do these steps. Ask the user for them, and never ask for a password, a code or a key in chat:

1. **Sign in to Expo here, once:** `eas login` in a terminal (eas-cli: `npm install -g eas-cli`).
2. **Buy the Apple Developer Program** membership for their Apple ID (iOS only).
3. **Create an Expo access token** at https://expo.dev/settings/access-tokens, for the builds on the Mac, and store it themselves as a line `EXPO_TOKEN=...` in `~/.config/macbox/expo.env` (`chmod 600`; `PHONE_BUILD_TOKEN_FILE` names another file). `phone-build` sends it to the Mac over SSH's stdin, never on a command line.
4. **Let EAS make the signing, once per app:** in a terminal here, inside the app, run `phone-build setup ios`. They sign in with their Apple ID (password and 2FA). EAS then creates and keeps the distribution certificate and the provisioning profiles; let it also create an App Store Connect API key, for uploads to TestFlight. After this, builds and submits run without them.
5. **Register their iPhone** for internal builds: `phone-build device` prints a link to open on the iPhone. For development builds they also turn on Developer Mode (Settings › Privacy & Security).

Local iOS builds also need `eas-cli` and `fastlane` on the Mac (macbox's guest provisioning can install them). `phone-build doctor` shows which of these are still missing.

## Rules

- **Build for the phone only when the task needs a phone or a store upload.** Free cloud builds are few, and the simulators cover UI checks.
- Uploading to TestFlight is fine when asked. Submitting for App Store review, or releasing to users, needs the user's explicit approval.
- Credentials live in EAS, and the Expo token in the token file. Never put either in a repo, a script, a log or a message.

## When something fails

- **`no eas.json` or no `projectId`:** run `phone-build init`, then commit `eas.json`.
- **`not signed in to Expo here`:** setup step 1.
- **`an Expo access token is needed`:** setup step 3.
- **The iOS build fails on signing or credentials:** setup steps 2 and 4 aren't done yet.
- **The Mac doesn't answer:** run `macbox status`; `macbox up` starts it.
- **A local build failed:** the log is above the error. Errors are usually the app's own (native dependencies, config plugins).
- **A cloud build failed:** its page on expo.dev has the log.
- **The usage can't be read:** `phone-build` builds locally.

## Files

- **The command:** `bin/phone-build` in this skill (linked as `~/.local/bin/phone-build` by `macbox agents install`). Settings come from `~/.config/macbox/macbox.env`: `MACBOX_SSH_HOST` (the Mac), `PHONE_BUILD_OUT`, `PHONE_BUILD_TOKEN_FILE`, `PHONE_BUILD_MODE` (`auto`, `cloud` or `local`).
- **Working files on the Mac:** checkouts are copied to `~/.phone-build/src/<checkout>/`, and builds are written to `~/.phone-build/out/` until they're copied back.
