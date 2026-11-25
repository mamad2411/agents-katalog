---
name: install-poki
description: Install the Poki app on the user's iPhone from a Mac, end to end, when they ask something like "install Poki on my iPhone". Runs bin/install-iphone.mjs from a Poki checkout and tells the user the one sentence it prints at each step only a person can do.
license: AGPL-3.0-only
---

# Install Poki on an iPhone

This installs the standalone Poki app on the user's iPhone through Poki Setup's helper, without its window. It is not the Poki MCP install in the repository's `AGENTS.md`. Works from Claude Code, Codex or any agent that can run a shell command on the user's Mac.

The installer does the work. You start it, relay its person stops, and report its result. Do not run its steps yourself.

## Before you start

**First-time installation requires Wi-Fi.** Ask the user to connect the iPhone to Wi-Fi and keep it connected until initial setup is complete. If it is on cellular data only, wait for the user to confirm Wi-Fi before starting. This applies to both the checkout installer and Poki Setup's bundled command line tool.

1. Find or make a Poki checkout. In a checkout, `bin/install-iphone.mjs` exists. Otherwise run `git clone --branch standalone https://github.com/JosssphZhou/poki.git` and work in that folder.
2. Check: a Mac with macOS 14 or later, Node.js 24 or later, an iPhone on iOS 18 or later, a USB data cable, and the user's Apple Account. A free account works with 7-day signing; it must be renewed before it expires. The iPhone also needs a compatible VPN/proxy app that routes 10.7.0.1 back to the iPhone (for example Karing or Shadowrocket configured as Poki's Setup page directs). Xcode is not required. With Xcode installed, the installer can see when Poki opens and give it the model key even with an older Poki Setup. Without Node.js 24, or on Windows, use "Without Node.js, or on Windows" below instead of the checkout.
3. Ask the user one question: "Should I also give Poki on the iPhone your model API key from this Mac's keychain?" Default is no. On yes, ask which provider (`openai`, `anthropic`, `deepseek`, `gemini` or `openrouter`) and add `--model-key <provider>` below. The installer reads the keychain item `<provider>-api-key` (for example `openai-api-key`; another name with `--model-key-item <item>`). Never read the key yourself and never ask for it in chat.

## Run it

From the checkout, start the installer in the background and read its output as it comes:

```sh
node bin/install-iphone.mjs run --json
```

Each line is one JSON event with an `at` time:

- `{"event":"step","step":"install",...}` starts a step. `done` or `skipped` (with a `reason`) ends it.
- `{"event":"wait","wait":"pair","who":"phone","say":"..."}` is a person stop. Tell the user `say` word for word. `who` is `phone` (tap on the iPhone) or `input` (type into a window on the Mac). The installer sees when it is done and continues.
- `{"event":"note","text":"..."}` is information. Pass it on when it asks something of the user.
- `{"event":"error","code":"...","reason":"...","agent_fix":"...","retrying":true}` is a failure. With `retrying` true, the installer is already trying again.
- `{"event":"result","ok":true,"check":{...}}` is the last line only when the checks passed without manual steps left unverified.
- A result with `ok:false` and `unverified` exits with code 3. Relay every entry's `say`, including instructions from skipped steps. Have the user finish them in Poki and confirm each result. Report what was manually confirmed and what remains unverified; do not call the phone ready just because the app was installed. Older Poki Setup without Xcode can require manual model-key entry and loopback setup.

Several iPhones plugged in: list them with `node bin/install-iphone.mjs phones` and add `--udid <udid>`.

## The steps

The installer runs these in order. Most need nobody.

1. **`setup_app`** Downloads Poki Setup and checks its SHA-256, Developer ID team (`Q64ZL36CJN`) and notarization. Nobody acts.
2. **`bridge`** Starts Poki Setup's helper without a window. Nobody acts.
3. **`channel`** Chooses the release channel, Alpha by default. Nobody acts.
4. **`apple_account`** Signs in with the Apple Account, on the Mac only. Poki Setup keeps the sign-in for renewals. Stops `apple_dialog` and `apple_code_dialog` when this Mac was never signed in.
5. **`phone`** Waits for the iPhone. Stop `phone_plug`.
6. **`install`** Pairs, turns on Developer Mode, signs and installs Poki, gives it its pairing file and disk image. Stops `pair` and `devmode` on a phone that needs them, `pairing_file` rarely.
7. **`open_poki`** The user trusts the developer and opens Poki. Stop `open_poki`, and the installer sees Poki open by itself. Stop `open_poki_tell` only when this Mac cannot read Poki's files. Then the user tells you, and you run `node bin/install-iphone.mjs done open_poki`.
8. **`model_key`** Only with `--model-key`. Gives Poki the key, sealed to a key only that iPhone holds, and waits until Poki says it took it. The first time, macOS may ask on the Mac whether node can use the keychain item; tell the user to click Allow. Poki takes the key while it is in front.
9. **`loopback`** Checks that Poki's local connection (10.7.0.1) answers. Stop `loopback` when it does not, with Poki's own sentence for the VPN app on the phone.
10. **`relay`** Deploys the relay when `CLOUDFLARE_API_TOKEN` is set or Poki Setup keeps a token. Skipped otherwise. Poki and its own chat work without it; agents on other computers need it.
11. **`check`** Self-check: the install record, Developer Mode, pairing, disk image and relay.

Poki turns itself on after this install, and ticks Developer Mode and UI Automation in its Setup once it runs. The iPhone's own switch for UI Automation (Settings > Developer > Enable UI Automation) is still the user's to turn on; Poki's Setup page says so. When Poki first opens it asks for Automation Mode: tell the user to tap Continue and enter the iPhone passcode on iOS's screen. If they cancel, Poki does not ask again until they turn it on again.

## Person stops

| `wait` | What you do |
|---|---|
| `apple_dialog` | Tell the user `say`. A Poki Setup window on the Mac asks for the Apple Account email, then the password (hidden). If they close it, the installer stops with `apple_credentials_missing`; run it again when they are ready. |
| `apple_code_dialog` | Tell the user `say`. Another window asks for the 6-digit code (hidden). Never ask for the code in chat. |
| `apple_password` | Only without windows (`POKI_INSTALL_DIALOGS=0`, or a session with no screen such as SSH). Give the user the command in `say`. They run it in their own Terminal, where macOS asks for the password without showing it. Never type it for them. |
| `apple_code` | Only without windows. Give the user the command in `say` exactly as printed (it has this checkout's absolute path). They type the code at its hidden prompt. The installer takes no code as an argument. |
| `phone_plug` | Tell the user `say`. |
| `pair` | Tell the user `say`. A phone already paired with this Mac gets only a `note`. |
| `devmode` | Tell the user `say`. The phone restarts; the installer waits for it. |
| `pairing_file` | Tell the user `say`. Rare: Poki Setup could not write the pairing file into Poki. |
| `open_poki` | Tell the user `say`. The installer sees Poki open. If the user says Poki is open and the installer has not moved on within a minute (an older Poki writes no hello), run `node bin/install-iphone.mjs done open_poki`. |
| `open_poki_tell` | Tell the user `say`. When they say Poki is open, run `node bin/install-iphone.mjs done open_poki`. |
| `loopback` | Tell the user `say`. It names their VPN app and the one thing to set. The installer sees when it answers. |

A person stop waits 15 minutes, then the installer exits with code 3 and `{"event":"result","ok":false,"waiting":"..."}`. Run the same command again when the user is ready; it rechecks the steps and reuses an unexpired install. If Poki says it is no longer available or signing has expired, run `node bin/install-iphone.mjs run --reinstall` with the same options. The installer renews expired records automatically; `--reinstall` also covers a revoked signature whose recorded expiry is still in the future.

## When a step fails

The installer exits with code 2. The last `error` event has `code`, `reason` and `agent_fix`. Do what `agent_fix` says and run again. Ask the user only for what the `person` field names.

| Code | Meaning | What you do |
|---|---|---|
| `setup_download_failed` | GitHub did not serve a release asset or its metadata. | Each request makes at most 3 attempts. Asset requests switch to the release asset API after a 5xx or connection failure. Report the failed URL/status and rerun later if both routes fail. |
| `setup_checksum_mismatch` | The DMG does not match `SHA256SUMS-desktop.txt`. | Fetched again once. Then stop and report. Never open the file. |
| `setup_signature_invalid` | Poki Setup is not signed by team `Q64ZL36CJN` or not notarized. | Stop. Do not run it. Report it. |
| `setup_app_missing` | `phones` or `diagnose` cannot find Poki Setup.app. | Run `run`, which installs it, or pass `--app-dir` or `--bridge`. |
| `bridge_start_failed` | Poki Setup's helper did not start. | Delete `~/Applications/Poki Setup.app` if the installer put it there, and run again. |
| `usbmuxd_unreachable` | macOS does not list the iPhone (issue #6). | Ask the user to plug it in again, unlocked. Then run `diagnose`. |
| `several_phones` | More than one iPhone is plugged in. | Run again with `--udid`. |
| `phone_locked` | The iPhone is locked. | Ask the user to unlock it. Retried by itself. |
| `trust_not_answered` | Nobody tapped Trust in time, or someone tapped Don't Trust. | Ask the user to tap Trust. Retried by itself. |
| `developer_mode_off` | Developer Mode is still off. | Ask the user to turn it on. Retried by itself. |
| `apple_credentials_missing` | Nothing to reuse, and the user closed the Poki Setup window. | Ask whether to sign in now, then run again. |
| `apple_sign_in_rejected` | Apple refused the email or password. | The window opens again by itself. |
| `apple_code_wrong` | Apple refused the code. | The window asks again; without windows, the user runs the `code` command again with the newest code. |
| `apple_server_busy` | Apple or the anisette server answered with an error. | Retried by itself on another server. |
| `apple_account_limit` | A free-account limit: 10 App IDs a week, 3 apps, or one certificate already held by AltStore, SideStore or Xcode. | Stop. Tell the user which limit Apple named. The way out is their decision. |
| `network` | A request failed, also while signing in. | Retried by itself with what the user already typed. Then report. |
| `sign_failed` | Signing failed. | Stop and run `diagnose`. |
| `ddi_refused` | Apple rejected the developer disk image with STATUS=94 or a signing-server refusal. The image may be too old for the phone's iOS. | Relay the detected Xcode and iOS versions from the error. Update Xcode to support that iOS version (iOS 27 requires Xcode 27), open Xcode once, and wait for its components to finish installing. Rerun the same command. Poki does not need to be reinstalled. If `prepare-device` used `--image`, replace that image with the updated Xcode image. |
| `install_failed` | iOS refused the install. | Retried once. Then run `diagnose`. |
| `relay_failed` | The relay deploy or check failed. Poki still works on the phone. | Report it. The user can deploy from Poki Setup's Relay page. |
| `check_failed` | Installed, but the self-check found something not ready. | Read the `check` fields, fix what the matching code says, run again. |
| `model_key_missing` | `--model-key` was given, but the keychain item is missing or empty. | Tell the user the item name. They add it in their own Terminal (`security add-generic-password -U -s <item> -a "$USER" -w`) or type the key in Poki: Agents > Accounts and Models. |
| `model_key_not_taken` | Poki did not take the sealed key in time. | Ask the user to bring Poki to the front, then run again. |
| `node_too_old` | Node.js is older than 24. | Install Node.js 24 or later, or follow "Without Node.js, or on Windows" below. |
| `unknown` | Not recognised. | Run `diagnose` and `issue`. |

## Download and upgrade recovery

When Poki Setup reports an HTTP error during installation, the installer downloads the selected release's external IPA, SHA256SUMS and Poki-signing.zip into a fresh folder. It checks the IPA's SHA-256, then passes the local IPA to the helper; the helper reads the signing zip beside it. Current releases do not list the signing zip in SHA256SUMS, so its integrity is provided by HTTPS, not a published checksum. If a release lists its checksum, the installer checks it too. Local installation records use a `local:` tag. No desktop update is required for this fallback.

If both download routes fail, do not skip checksum checks or substitute another release's signing zip. A manual recovery can use `gh release download <selected-tag> --repo JosssphZhou/poki --pattern '<selected-IPA-name>' --pattern SHA256SUMS --pattern Poki-signing.zip --dir <new-empty-folder>`. Check the IPA against that release's SHA256SUMS before using Poki Setup's local IPA install. This is a manual fallback, not an installer success.

Before an upgrade, ask the user to save their work and close the old Poki. If installation stalls, retry with the phone unlocked and the old app closed. Do not delete Poki or revoke certificates without explaining the data/signing impact and getting permission. An unavailable old app is not proof that its data is lost.

## Without Node.js, or on Windows

Poki Setup 0.2.2 and later carry their own command line tool, which needs no checkout and no Node.js: `"/Applications/Poki Setup.app/Contents/MacOS/poki-setup"` on a Mac (or under `~/Applications`), `"$env:LOCALAPPDATA\Poki Setup\poki-setup.exe"` on Windows. When Node.js 24 is missing (`node_too_old`) or the computer runs Windows, ask the user to install Poki Setup from https://github.com/JosssphZhou/poki/releases#release-ios-alpha-latest and open it once, then run `"<tool>" prompt` and follow what it prints. In short: `"<tool>" next --json` lists what is done and what is next, with `who`, `command` and `say` for each step; exit code 2 means a person has to act and 3 that Apple's sign-in code is needed. The person signs in by running `"<tool>" login <email> --keep-password` in their own terminal.

## Read Poki's records on the Mac

`node bin/install-iphone.mjs records` reads Poki's chats, voice conversations and log off the iPhone over USB and writes them as one text file in time order, by default in `~/Library/Application Support/PokiInstall/records/`. It only copies from Poki's app container (`devicectl device copy from`) and changes nothing on the phone. It prints only the file's path, not the conversations. Keys, pairing records and relay addresses are removed. Use `--udid` when several iPhones are plugged in, `--out <file>` to choose the file, and `--bundle <id>` when iOS does not list Poki by name. The file holds the owner's own messages: show it only to them.

## When you cannot fix it

1. Run `node bin/install-iphone.mjs diagnose`. It prints a JSON bundle with versions, each step's result, what usbmuxd, USB, `devicectl` and Bonjour see, and Poki Setup's last log lines, with identifiers, names, keys, tokens and addresses removed. Show it to the user.
2. Run `node bin/install-iphone.mjs issue`. It writes an English issue draft and prints the `gh issue create` command. It never submits.
3. Show the user the whole draft. Run the printed command only after they say yes. Never submit without that yes.

## Secrets

- The Apple Account password and code go into Poki Setup windows the user types into, never into chat or a command line. `POKI_APPLE_ID` and `POKI_SETUP_PASSWORD` are for the user's own shell, not for you.
- The model key leaves the keychain only into the installer's memory, is sealed to the iPhone's key, and is never printed, logged or put on a command line.
- Do not print, log or paste the user's password, tokens, model keys or iPhone passcode.

`node bin/install-iphone.mjs run --dry-run` checks the real Poki Setup and simulates the iPhone and the Apple Account. `node bin/install-iphone.mjs --version` names the installer; say it when you report a problem. On Windows, see "Without Node.js, or on Windows" above.
