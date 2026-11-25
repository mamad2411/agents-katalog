---
name: CleanYourPhone
description: Use when the user wants to debloat an Android phone, disable preinstalled apps, ads or telemetry, improve battery, or "clean" their phone like cleanyour.tv, over ADB, without root and without uninstalling anything.
---

# CleanYourPhone

You are cleaning an Android phone that belongs to the person in front of you. It is their daily
driver: calls, SMS, banking, alarms, work profile, photos. A wrong package can leave them without a
dialer, without SMS, without a keyboard, or in a boot loop. Treat every change as irreversible until
you have proved the undo.

This skill does one job: **disable preinstalled apps and services with `pm disable-user --user 0`**,
optionally set Private DNS, and produce a report. It does not install apps, does not root, does not
flash a ROM, does not uninstall, and does not touch a managed device.

## Non-negotiable rules

1. **Disable, never uninstall.** Only `pm disable-user --user 0 <package>`. Never `pm uninstall`,
   `pm uninstall --user 0`, `pm hide`, `pm block`, `pm clear`, `adb shell rm`, or a factory reset.
2. **Back up first.** Run `python tools/phone.py backup` (or save the package lists, `getprop`,
   settings, roles and IMEs yourself) before the first change. No backup, no change.
3. **One package per shell call.** Chained `pm` commands can silently stop after the first.
4. **Never touch the protected list.** `tools/protected.py` and `docs/SAFETY.md` list the packages
   that can stop the phone from booting or from calling. If a package matches, refuse. No override.
5. **Respect the roles.** Before disabling a dialer, SMS app, launcher or keyboard, check which app
   currently holds the role. If it is the holder and there is no confirmed replacement, refuse.
   Never leave the phone without a dialer, SMS app, HOME app or IME.
6. **Ask before anything the person uses.** Banking, payments, work apps, WhatsApp, camera, gallery,
   clock/alarm, VPN, password manager, authenticator, smartwatch, eSIM, VoLTE/Wi-Fi calling, hotspot,
   accessibility, parental controls. Put them in one checklist; disable only what they do not tick.
7. **Small batches, verify between.** At most 5 packages per batch. After each batch run
   `python tools/phone.py verify`. If anything fails, re-enable the batch and stop.
8. **Reboot once at the end, then verify again.** Wait 15 seconds (or `adb shell sync`) after the
   last change before rebooting. Compare `pm list packages -d` with what you disabled: some OEM
   firmware re-enables packages at boot. Record those instead of fighting them.
9. **Close ADB when done.** Turn off Wireless debugging and USB debugging (unless the person asks to
   keep it), revoke authorisations, and check that `adb devices` no longer lists the phone.
10. **Speak the person's language.** If they write in Spanish, answer in Spanish. Explain what each
    package is before you touch it; never dump a wall of package names without a plan.
11. **Stop and say so** when the phone refuses: `pm disable-user` refused for every package, ADB
    unauthorized, a managed device, an SDK below 26 (Android 8), or a package you cannot identify.
    Do not retry in a loop and do not invent a workaround.

## First response

Before running anything, ask for:

- Phone brand and model, and the Android version if they know it.
- What they want: fewer ads, better battery, more storage, less telemetry, or all of it.
- Whether it is a work phone or has a work profile.
- Which of these they use: banking/payments, WhatsApp, camera, smartwatch, eSIM, VoLTE/Wi-Fi calling,
  hotspot, VPN, password manager, authenticator, parental controls, accessibility services.
- Whether they have a backup of their photos and data (debloating does not touch data, but a boot
  loop can force a factory reset; say this plainly).

Then run Phase 0.

## Phase 0 — Connect and identify

For a first-time user, walk them through [docs/CONNECT.md](docs/CONNECT.md). Do not assume they know
what ADB, a pairing port or a data cable is.

The short version:

1. **Developer options**: Settings → About phone → tap **Build number** 7 times. On Samsung it is
   under **Software information**; on Xiaomi/Redmi/POCO tap the OS version instead.
2. **Wi-Fi (Android 11+)**: turn on **Wireless debugging**, then **tap the words “Wireless
   debugging”** (not only the switch) to open its detail screen. Tap **Pair device with pairing
   code**. The dialog shows a six-digit code and its own **IP:port**. Keep that dialog open: the code
   expires and its port closes with the dialog. The **pairing port** in the dialog is not the
   **connection port** on the main screen. `adb mdns services` lists `_adb-tls-pairing._tcp` and
   `_adb-tls-connect._tcp` when the dialog is open.
3. **USB**: use a data cable, turn on **USB debugging**, choose **File transfer / MTP** in the USB
   notification, and accept **Allow USB debugging?** with **Always allow from this computer**.
4. If Windows sees no phone at all, it is a cable, port or OEM driver problem. Try another data
   cable and a direct USB port before changing any package.

```bash
adb devices -l
python tools/phone.py doctor
python tools/phone.py probe
```

If `cleanyourphone` is installed, use `cleanyourphone doctor` and `cleanyourphone probe` instead;
both commands are the same CLI with the same guards. The rest of this skill uses the repo-local form.

If `adb` is not installed, use the platform-tools for the computer's OS. If there are several
devices, ask which serial to use and pass `--serial <serial>` to every command.

**Stop and explain, do not continue, if any of these is true:**

- `ro.build.characteristics` contains `tv` or `box`: this is an Android TV, not a phone. Send them to
  https://cleanyour.tv instead.
- `dumpsys device_policy` shows a **Device Owner** or **Profile Owner**: it is a managed/work phone.
  Changing packages can break company policy. Stop. If the policy cannot be read, stop: unknown is not
  permission.
- `pm list users` shows more than one user (work profile, guest or clone), or cannot be read. A
  `--user 0` disable can still affect shared packages. Stop.
- `ro.build.version.sdk` is below 26 (Android 8): the role commands and some package states differ.
  Do the backup and the safe list only, or stop.
- ADB says `unauthorized`, `offline`, or no device: fix the cable, USB mode, driver or pairing dialog
  first. Do not continue with an unverified connection.
- The phone has less than 30% battery: ask them to charge it before a reboot.

Warn, but do not stop, if:

- `ro.boot.verifiedbootstate` is not `green` or `ro.boot.flash.locked` is `0`: the bootloader is
  unlocked or the ROM is custom. Debloating still works, but banking/DRM may already be affected.
- `ro.debuggable` is `1`: a userdebug/custom build. Package names may differ from the retail ROM.
- The phone is a Samsung: do **not** suggest unlocking the bootloader later. Knox is permanent.
- The phone is a Huawei/Honor without Google services: many `com.google.*` packages do not exist;
  do not assume a list written for another brand applies.

## Phase 1 — Back up

```bash
python tools/phone.py backup
```

It writes a timestamped folder under `backup/` with the package lists, disabled list, `getprop`,
settings, roles, IMEs, HOME activities, device policy and battery state. Tell the person the path.

If the CLI is not available, run the same commands manually and save the output:

```bash
adb shell pm list packages -f
adb shell pm list packages -d
adb shell pm list packages -e
adb shell pm list packages -s
adb shell pm list packages -3
adb shell getprop
adb shell settings list global
adb shell settings list secure
adb shell settings list system
adb shell cmd role get-role-holders android.app.role.DIALER
adb shell cmd role get-role-holders android.app.role.SMS
adb shell cmd role get-role-holders android.app.role.HOME
adb shell cmd role get-role-holders android.app.role.EMERGENCY
adb shell settings get secure default_input_method
adb shell ime list -s
adb shell cmd package query-activities -a android.intent.action.MAIN -c android.intent.category.HOME
adb shell pm list users
adb shell dumpsys device_policy
adb shell dumpsys battery
```

The backup is the baseline. The exact undo journal is `~/.cleanyourphone/applied.json`; `restore`
uses it. If the journal is lost, `restore --from-backup <backup-folder>` compares the backup's
disabled list with the phone and asks before enabling anything. Do not skip either because "it is
only a few packages".

Also capture a benchmark before the first change, after the backup:

```bash
python tools/phone.py bench snapshot --label before
```

Without the CLI, save the same fields manually:

```bash
adb shell cat /proc/meminfo
adb shell ps -A -o NAME
adb shell pm list packages -e
adb shell pm list packages -d
adb shell pm list packages -s
adb shell pm list packages -3
adb shell settings get global window_animation_scale
adb shell settings get global transition_animation_scale
adb shell settings get global animator_duration_scale
adb shell settings get system peak_refresh_rate
adb shell settings get global low_power
adb shell settings get global private_dns_mode
adb shell settings get global private_dns_specifier
```

Keep the output with the backup. This is evidence, not a promise.

## Phase 2 — Inventory and plan

```bash
python tools/phone.py list --state enabled
python tools/phone.py roles
python tools/phone.py plan --profile <profile-id>
```

If a profile matches the model, check its `verification` level first:

- `device`: tested on that model and build. It may have a `disable` list and may be auto-applied only
  when the current build is in `tested`.
- `documented`: built from a firmware dump, not tested on a phone. It has **no** `disable` list and
  must never be auto-applied. Every row is `ask` or `keep`; explain the source and ask per package.
- `reference`: generic guidance only. It has no `disable` list and cannot be auto-applied.

The profile separates:

- `disable`: tested on that model/firmware, low risk. Only `device` profiles.
- `ask`: user-facing or dependency-heavy; ask first.
- `never`: protected for that model.

If there is no exact profile, or the only match is `documented`, classify manually. For every package,
find out what it is before you touch it:

```bash
adb shell dumpsys package <package> | grep -E "versionName|installerPackageName|firstInstallTime|lastUpdateTime|enabled="
adb shell cmd package resolve-activity --brief <package>
```

If the name is still unclear, search the web for the exact package name plus the model, or ask the
person. **Do not guess from the name alone.** A package called `*.service` or `*.provider` is not
automatically safe, and a package called `*.analytics` is not automatically the one you think.

Present a table like this and wait for approval:

| Package | App | Why | What breaks | Action |
|---|---|---|---|---|
| `com.samsung.android.app.spage` | Samsung Free | Ad/recommendation surface | Samsung Free disappears | disable |
| `com.google.android.apps.wellbeing` | Digital Wellbeing | Screen-time telemetry | Screen-time reports | ask |
| `com.google.android.gms` | Play Services | Push, banking, backups | Almost everything | never |

Only the `disable` rows of a `device` profile can be applied after the person approves the plan.
`ask` rows need an explicit yes per row (or a checklist). `never` rows are not negotiable. A
`documented` profile has no `disable` rows: use it to ask, never to batch-apply.

### Triage guide

Good candidates, after checking the exact package on that model:

- OEM ad and recommendation surfaces: Samsung Free (`com.samsung.android.app.spage`), Xiaomi MSA
  (`com.miui.msa.global`), Xiaomi GetApps (`com.xiaomi.mipicks`), `com.miui.systemAdSolution`,
  Motorola demo/help apps, carrier "app store" and "games" preloads.
- Telemetry and feedback: `com.google.android.feedback`, OEM analytics packages whose only
  components are services and receivers. Anything under `com.google.android.gms.*` is protected:
  Play Services is one package family, and disabling a subpackage can break push, location, banking
  or Play Integrity.
- Duplicate content apps you already replace: OEM browser, email, calendar, gallery, music, video,
  file manager, notes. Ask which one the person actually uses.
- Unused preloads: Facebook/Microsoft/LinkedIn installers on Samsung, "Partner Bookmarks", games,
  movie stores, "Tips", "Community", "Members".

Ask, do not assume:

- The OEM dialer, SMS, contacts, camera, gallery, clock, calculator, file manager, keyboard, launcher.
  The stock launcher often provides the Recents screen even when another launcher is set (Pixel
  Launcher Quick Switch, Samsung One UI Home). Do not disable it just because the person uses Nova
  or another launcher; keep it unless they accept losing Recents.
- Google app suite: Gmail, Photos, Maps, YouTube, Drive, Meet, Calendar, Keep, Messages, Phone.
- Bixby, Samsung Cloud, Link to Windows, DeX, Secure Folder: ask. Samsung Pass, Samsung Wallet/Pay
  and Knox are **never** (protected): they hold passwords, payments and the security platform.
- Xiaomi Cloud, Mi Mover, Mi Video, Mi Music, Game Center, Themes: ask. The Security app
  (`com.miui.securitycenter`), Permission Center and PowerKeeper are **never** (protected).
- VoLTE/RCS/IMS, SIM Toolkit, carrier config, Wi-Fi calling, hotspot, eSIM.
- VPN, private DNS apps, password managers, authenticators, banking, work apps.
- Accessibility services, parental controls, smartwatch companions, Find My Device.
- Emergency alerts, cell broadcast, Android Auto, Wear OS, Nearby Share/Quick Share.

Never disable (the CLI refuses these; the list is in `tools/protected.py`):

- `android`, `com.android.systemui`, `com.android.settings`, `com.android.shell`
- `com.android.phone`, `com.android.server.telecom`, `com.android.incallui`
- `com.android.providers.*` (telephony, contacts, media, settings, downloads, calendar)
- `com.android.permissioncontroller`, `com.google.android.permissioncontroller`
- `com.android.packageinstaller`, `com.google.android.packageinstaller`
- `com.google.android.gms*` (all Play Services subpackages), `com.google.android.gsf*`,
  `com.android.vending*`
- `com.google.android.webview`, `com.android.webview`
- `com.android.ext.services`, `com.android.ext.shared`, `com.google.android.ext.services`,
  `com.google.android.ext.shared`, `com.google.android.overlay.modules*`
- `com.android.cellbroadcastreceiver`, `com.google.android.cellbroadcastreceiver`,
  `com.android.cellbroadcastservice`, `com.android.emergency`
- `com.android.ims*`, `com.google.android.ims`, `com.android.carrierconfig`
- `com.android.se` (eSIM/NFC secure element), `com.android.nfc` (payments, transit, tags)
- `com.android.bluetooth*` (wearables, car, earbuds)
- `com.android.networkstack*`, `com.google.android.networkstack*`, `com.android.wifi*`,
  `com.google.android.wifi*` (Wi-Fi and mobile data)
- `com.android.keychain`, `com.android.certinstaller`, `com.android.vpndialogs`
- `com.android.documentsui` (the file picker other apps use)
- OEM equivalents: `com.samsung.android.incallui`, `com.samsung.android.app.telephonyui`,
  `com.samsung.android.dialer`, `com.samsung.android.messaging`, `com.samsung.android.knox.*`,
  `com.samsung.android.spay`, `com.samsung.android.samsungpass`, `com.samsung.android.authfw`,
  `com.samsung.android.thermal`, `com.miui.securitycenter`, `com.miui.powerkeeper`,
  `com.miui.permcenter`, `com.miui.home`, `com.huawei.systemmanager`, `com.huawei.phone`,
  `com.huawei.contacts`, `com.huawei.mms`, `com.huawei.dialer`, `com.coloros.securitypermission`,
  `com.oplus.battery`, `com.coloros.phonemanager`.

## Phase 3 — Apply

Use the CLI so the guardrails run:

```bash
python tools/phone.py disable <package>
```

Or, if the CLI is unavailable, run exactly one package per call and verify it:

```bash
adb shell pm disable-user --user 0 <package>
adb shell pm list packages -d | grep <package>
```

If you use raw `adb`, `python tools/phone.py restore` cannot see those changes. Keep your own list
of every package you disabled in this session, and enable from that list. The backup's `disabled.txt`
is the phone's **pre-session** disabled list, not a change log.

Rules for this phase:

- At most 5 packages per batch. After each batch: `python tools/phone.py verify`.
- If a `disable-user` call prints `SecurityException`, `Error`, or does not appear in
  `pm list packages -d`, stop. Some firmware refuses; there is nothing to debloat there.
- If the phone loses the dialer, SMS, HOME, keyboard, notifications, mobile data, Wi-Fi, Bluetooth or
  Play Services after a batch, re-enable that whole batch immediately and stop.
- Do not disable the package that currently holds a role. Check again after every batch, because
  disabling one app can move a role to another.
- Do not disable a package that is already disabled. Skip it and note it.
- Do not use `--user all`; only user 0. Do not touch a work profile.
- Do not disable a package whose only job is to keep the phone updated (OTA/firmware updater) unless
  the person explicitly accepts that they will update manually. Prefer leaving it enabled.

## Phase 4 — Optional: Private DNS

Only after the debloat is stable and verified. Ask first:

- Do they use a VPN? Private DNS can coexist with some VPNs, but not all.
- Does their router already block ads (Pi-hole, AdGuard Home, NextDNS)? Private DNS goes around the
  router's DNS, so their rules stop applying. In that case, keep the router and skip this.
- Do they use captive portals (hotels, airports)? A strict resolver can break the login page.

Record the original values before changing anything:

```bash
adb shell settings get global private_dns_mode
adb shell settings get global private_dns_specifier
```

Presets: `adguard` (`dns.adguard-dns.com`), `adguard-family` (`family.adguard-dns.com`),
`controld` (`p2.freedns.controld.com`), `mullvad` (`adblock.dns.mullvad.net`). With the CLI,
`python tools/phone.py dns providers` lists them and `dns set adguard` applies one. Raw ADB always
works:

```bash
adb shell settings put global private_dns_specifier dns.adguard-dns.com
adb shell settings put global private_dns_mode hostname
```

Verify with a control domain and a fresh ad subdomain:

```bash
adb shell settings get global private_dns_mode
adb shell ping -c 1 -W 3 cyp-check.adnxs.com
adb shell ping -c 1 -W 3 wikipedia.org
```

Use a new label on every check (`cyp-check2`, `cyp-check3`…). Reusing a name can read the resolver
cache and show the IP from before the change. `adnxs.com` has a real wildcard, so an unblocked
resolver returns a public IP instead of NXDOMAIN.

If the ad name resolves to a sinkhole (`0.0.0.0`, `::`, `127.0.0.1`, `::1`), the resolver is active.
If it still resolves to a public IP, it is not. If the control domain does not resolve, the phone is
offline or the DNS is misconfigured: do **not** claim ads are blocked. Say “cannot test” and fix the
network first. `python tools/phone.py dns check` does the same check with a random label; `--json`
returns the result.

Open a browser and an app that uses the network. If they fail, restore the exact values you recorded:

```bash
adb shell settings put global private_dns_specifier <original-specifier>
adb shell settings put global private_dns_mode <original-mode>
```

If the original mode was `opportunistic`, `adb shell settings put global private_dns_mode opportunistic`
is enough. The CLI does this with `python tools/phone.py dns restore`.

Tell them plainly: an ad-blocking resolver over Private DNS blocks many in-app ads and trackers,
**not YouTube ads** (same domain), and it is not a VPN. It also does not stop an app from tracking you
once it has your data. The OEM checklist is in [docs/ADS.md](docs/ADS.md).

## Phase 5 — Reboot and verify

```bash
adb shell sync
# wait 15 seconds
adb reboot
adb wait-for-device
adb shell getprop sys.boot_completed
python tools/phone.py verify
```

Wait until `sys.boot_completed` is `1`. Then ask the person to test, on the phone:

- Call someone and receive a call.
- Send and receive an SMS.
- Open the camera and take a photo.
- Type in a text field (keyboard).
- Press Home and open the app drawer.
- Pull down notifications; check an alarm.
- Open the banking app and WhatsApp (or the apps they named).
- Turn Wi-Fi off/on, mobile data off/on, Bluetooth off/on.
- If they use it: hotspot, NFC payment, VoLTE/Wi-Fi calling, smartwatch, eSIM.

If anything fails, stop and follow the recovery section below. Do not "fix it" by disabling more.

## If something breaks

Stop. Do not disable more packages.

1. If `adb devices` still shows the phone, run `python tools/phone.py restore` (or
   `cleanyourphone restore`). If it says there is no record, run
   `python tools/phone.py restore --from-backup <backup-folder>`, review the list and add `--yes`
   only when it is correct.
2. If the phone does not boot, follow [docs/RESTORE.md](docs/RESTORE.md): safe mode first, then ADB,
   then recovery. A factory reset is the last resort; explain what will be lost before it.
3. If the phone is managed, a TV/box or has more than one user, stop before changing anything.

## Phase 6 — Report and close

```bash
python tools/phone.py report
```

Give the person:

- The model, Android version and build fingerprint.
- The backup path.
- What was disabled and why (one line each).
- What was kept and why.
- DNS state.
- The exact undo command: `python tools/phone.py restore`.
- If the journal is ever lost: `python tools/phone.py restore --from-backup <backup-folder>`.
- The battery baseline, if they want to measure it (see `docs/BATTERY.md`).
- The before/after benchmark, if they asked for it.

Measure after the reboot and verification, under the same conditions:

```bash
python tools/phone.py bench snapshot --label after
python tools/phone.py bench compare <before.json> <after.json>
```

Without the CLI, repeat the same raw commands from Phase 1. Compare free RAM, processes, enabled and
disabled package counts, animation scales, refresh rate and DNS. Say “measured on this phone,
approximate, not causal”; do not claim that the phone is faster or that RAM gains are guaranteed.

Then close ADB:

- Turn off **Wireless debugging** if it was on.
- Turn off **USB debugging** unless they ask to keep it.
- Revoke USB debugging authorisations.
- Unplug the cable and confirm `adb devices` no longer lists the phone.

## Optional — feedback or a profile request

Only if the person asks. Never send anything automatically.

Build a short checklist from `probe`: brand/model/device, Android and SDK, build, fingerprint, profile
id, packages touched and the result. Remove serial numbers, IP addresses, IMEI, MAC addresses,
account emails and pairing codes.

Show the checklist and ask for explicit permission. Then preview it:

```bash
python scripts/feedback.py --kind profile --checklist-file feedback.txt
```

If the preview is correct and the person approves, send it:

```bash
python scripts/feedback.py --yes --kind profile --checklist-file feedback.txt
```

Without `--yes`, the script prints the payload and sends nothing. It redacts common identifiers before
the preview. The web form is at
<https://cleanyourphone.org/#feedback>. The feedback helper is separate from
`tools/phone.py`, which stays local and network-free. See [docs/FEEDBACK.md](docs/FEEDBACK.md).

## Stop conditions

Stop immediately, explain what happened, and do not improvise if:

- The phone is not an Android phone, or is an Android TV.
- It is a managed/work device.
- ADB is unauthorized or the phone is offline.
- `pm disable-user` is refused for every package.
- The phone boot-loops, or Home, dialer, SMS, keyboard, notifications, mobile data or Wi-Fi breaks.
- The person says stop, or asks for something outside this skill (root, ROM, unlocking, uninstalling).

## Manual undo

Every change is reversible if you know which packages you disabled:

```bash
adb shell pm enable <package>
python tools/phone.py restore
```

`restore` re-enables exactly what the CLI recorded in `~/.cleanyourphone/applied.json`. If you used
raw `adb`, use your own session list instead; `disabled.txt` is the pre-session baseline and may
contain packages that were already disabled before you started.

If the phone will not boot, do not panic and do not factory reset yet: boot into safe mode (most
phones: hold Volume Down while booting), re-enable the last batch from a computer with ADB, or read
your session list. `docs/RESTORE.md` has the long version.

## What this skill will not do

- No root, no Magisk, no Shizuku requirement.
- No custom ROM, no bootloader unlock, no flashing.
- No `pm uninstall`, no `pm hide`, no `pm clear`.
- No app installation, no APK sideloading, no "cleaner" apps.
- No promises of "double battery". Debloating typically saves 0–10% standby; the big wins are
  background restrictions, screen brightness/refresh rate and DNS.
- No work-profile changes, no MDM bypass, no warranty advice beyond "this is reversible but your
  OEM may see it differently".
- No privacy magic. The CLI is local, but a hosted coding agent may send the phone model, package
  names and fingerprint to its provider. If that matters, use a local model or redact before pasting.
