---
name: leeway-secondary-workstation
description: Build, qualify, recover and route a governed Android developer workstation for LeeWay or another authorized LLM/agent using Termux, Desktop Commander Remote MCP, Git/GitHub, Device Bridge, Wireless ADB shell authority and evidence-based failover.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  aliases: LeeWay Developer Android State; Android Developer Workstation
  canonical-device-authority: 4citeB4U/LEEWAY-DEVICE-BRIDGE
  runtime-owner: 4citeB4U/Leeway-Runtime-Fabric
  developer-state-contract: config/android-developer-state-v1.json
  reference-guide: https://github.com/4citeB4U/LEEWAY-DEVICE-BRIDGE/blob/main/docs/ANDROID-SECONDARY-WORKSTATION.md
  evidence: receipts/leeway-developer-android-state-20261001.json
---
<!--
LEEWAY HEADER — DO NOT REMOVE

REGION: LEEWAY.SKILLS.ANDROID
TAG: LEEWAY.SKILLS.ANDROID.DEVELOPER_WORKSTATION

COLOR_ONION_HEX:
NEON=#39FF14
FLUO=#00E5FF
PASTEL=#DDF7FF

ICON_ASCII:
family=lucide
glyph=smartphone-cog

5WH:
WHAT = Governed skill for preparing, qualifying, repairing and operating an Android developer workstation
WHY = Turn an authorized Android phone into a repeatable LeeWay workstation with explicit non-root and ADB-shell authority lanes
WHO = Leeway Industries / Creator-authorized Agent Lee and compatible authorized LLM or agent runtimes
WHERE = skills/leeway-secondary-workstation/SKILL.md and qualified Android hosts
WHEN = On new-phone preparation, workstation recovery, Android permission blockers, ADB/Shizuku setup, or privilege-lane repair
HOW = Inspect -> diagnose -> prepare -> pair -> execute -> validate -> repair -> retest -> verify -> receipt

AGENTS:
ASSESS
AUDIT
EXECUTE
VERIFY

LICENSE:
MIT
-->

# LeeWay Secondary Workstation

## LeeWay Developer Android State

This skill is the canonical LeeWay Android workstation skill.

"LeeWay Developer Android State" is the qualified condition in which an authorized Android phone has a proven normal workstation lane plus, when explicitly enabled and verified, a governed Android ADB-shell lane.

A new phone does not inherit verification from another phone. Every phone must earn its own receipt.

## Purpose

Turn a supported Android phone into a real, independently reachable development/execution node for an authorized online LLM or agent.

The phone does not become Windows and does not gain root by declaration. It becomes a qualified Android/Termux workstation with explicit capabilities, explicit boundaries, persistence evidence, optional Android shell authority, rollback and receipts.

## Authority architecture

### Lane A — ordinary workstation

Online LLM / Agent
-> authenticated Remote MCP
-> Desktop Commander Remote device
-> Android / Termux app UID
-> shell + files + search + Node/npm + Git + HTTPS/OpenSSH
-> GitHub / authorized workplane.

Boundary: `TERMUX_APP_UID_NON_ROOT`.

### Lane B — governed Android shell

Online LLM / Agent
-> Desktop Commander / authorized execution adapter
-> Termux
-> `leeway-priv`
-> authenticated Wireless ADB device
-> Android `uid=2000(shell)`
-> permitted package/settings/activity/service diagnostics and actions.

Boundary: `ANDROID_ADB_SHELL_NON_ROOT`.

The privileged lane MUST prove `uid=2000(shell)` before it is considered live.

### Lane C — Android-native providers

Privileged phone capabilities that require app APIs, user-consent flows, UI automation, hardware access, notifications, accessibility, media capture, Bluetooth, USB/HID or other Android-native surfaces route through LeeWay Device Bridge or another separately authorized provider.

Desktop Commander, ADB shell and Device Bridge are complementary. They MUST NOT be conflated.

### Lane independence law

Lane A, Lane B and Lane C are independently qualified capability lanes inside one LeeWay workstation body.

- Lane B is optional maintenance/diagnostic shell authority. Its absence, timeout or disconnection MUST NOT invalidate a healthy Lane A ordinary workstation or a healthy Lane C Android-native provider.
- Lane C authority originates in the installed authorized Android provider and its Android permission/consent boundary, not in Termux, ADB, Shizuku or USB.
- Termux/Desktop Commander may transport bootstrap or diagnostic requests, but they do not become the authority of Lane C.
- A failed probe in one lane must be classified to that lane only. Do not globalize it into a workstation failure.
- Before repairing a lane, inspect the canonical runtime/provider health and reuse the existing registered adapter/provider/package identity.
- Never create a parallel package, runtime, registry or authority merely to bypass a failed lane.

### Canonical package lineage law

Repairs and updates must modify the existing canonical package/repository identity whenever that identity remains valid.

- 4citeB4U/LEEWAY-DEVICE-BRIDGE remains the Android-native device authority.
- 4citeB4U/LeeWay-Pocket-Agent remains the Pocket client identity.
- 4citeB4U/Leeway-Runtime-Fabric remains the runtime owner/router.
- Experimental builds may exist transiently for verification, but must not become parallel authorities or accumulate as user-visible install choices.
- Preserve one qualified rollback; retire superseded generated package artifacts after the replacement passes Veritas.

## Canonical reusable assets

- `4citeB4U/LEEWAY-DEVICE-BRIDGE/clients/phone-workstation/bootstrap-desktop-commander.sh`
- `4citeB4U/LEEWAY-DEVICE-BRIDGE/clients/phone-workstation/patch-desktop-commander-android.mjs`
- `4citeB4U/LEEWAY-DEVICE-BRIDGE/docs/ANDROID-SECONDARY-WORKSTATION.md`
- `4citeB4U/LEEWAY-DEVICE-BRIDGE/docs/secondary-workstation-node.json`
- `4citeB4U/LEEWAY-DEVICE-BRIDGE/docs/provider-registry.json`
- `skills/leeway-secondary-workstation/scripts/leeway-priv.sh`
- `skills/leeway-secondary-workstation/scripts/android-developer-state-audit.sh`
- `config/android-developer-state-v1.json`
- `receipts/leeway-developer-android-state-20261001.json`

## Reference qualification

A physical Samsung Galaxy Z Fold6 running Android 16 / arm64 was first qualified as a PC-independent and USB-independent Termux/Desktop Commander workstation.

The same reference class was subsequently qualified for a direct Termux -> Wireless ADB -> Android shell lane. Acceptance proof included:

- Android Debug Bridge client in Termux;
- Wireless Debugging enabled;
- one-time Android pairing completed with user-visible pairing consent;
- direct ADB connection to the phone;
- `id` returned `uid=2000(shell)`;
- SELinux context returned `u:r:shell:s0`;
- protected settings became readable through the governed lane;
- the privilege wrapper detected the exact shell identity;
- the wrapper remained fail-closed without that identity;
- destructive commands remained blocked by the wrapper;
- the authenticated device was selected explicitly rather than relying on ambiguous ADB default routing.

This proves the reference phone only.

## Developer-options preparation

### Keep on when building or operating the developer workstation

- Developer options.
- USB debugging when required for the selected ADB workflow.
- Wireless debugging while using the direct Wireless ADB lane.

### Keep off unless a specific diagnostic requires them

- Debug GPU overdraw.
- Show layout bounds.
- Show surface updates.
- Profile HWUI rendering.
- Strict mode visual indicators.
- Pointer location.
- Show taps, unless touch diagnostics are active.
- Force 4x MSAA.
- Override force-dark.
- Disable HW overlays.
- Wait for debugger.
- Don't keep activities / Always finish activities.

Keep Background process limit at the standard/default limit unless a qualified experiment explicitly requires another value.

Do not enable developer toggles merely because they appear powerful. A graphics or UI debugging switch does not increase Android authority.

## Build procedure

### Phase 1 — inspect before mutation

1. Identify Android version, architecture, OEM/build class and current user.
2. Determine whether the host is ordinary app UID, ADB shell or root. Never infer privilege from a UI label.
3. Inventory Termux, ADB, Desktop Commander, Git, Node and existing LeeWay assets.
4. Identify the canonical target, rollback, acceptance test and user-consent gates.
5. Run `android-developer-state-audit.sh` where available.

### Phase 2 — establish the ordinary workstation

1. Install/prepare Termux from an authorized source.
2. Bootstrap Desktop Commander using the canonical Device Bridge assets.
3. Complete provider-owned authentication without exposing passwords, MFA codes, refresh tokens or private credentials.
4. Verify ping, shell, filesystem, search, Node/npm, Git and outbound GitHub/network access.
5. Remove the primary PC from the execution path.
6. Disconnect USB and prove fresh phone-local execution.
7. Verify session recovery.
8. Verify cold-boot reconnect before claiming cold-boot persistence.

### Phase 3 — prepare Android debugging

1. Enable Developer options.
2. Enable USB debugging if required.
3. Enable Wireless debugging for the direct wireless lane.
4. Keep unrelated visual/performance debugging toggles off.
5. Never bypass Android's required user pairing/installation confirmations.

### Phase 4 — optional Shizuku path

Shizuku is an optional Android shell broker and may be useful for apps or terminal integration.

For terminal use:

1. Start Shizuku through Wireless debugging.
2. Complete Android pairing before pressing Start when required.
3. Export the matching `rish` and `rish_shizuku.dex` pair from the running Shizuku app.
4. Replace `PKG` in `rish` with the real terminal package, e.g. `com.termux`.
5. On Android 14+, make the DEX non-writable before `app_process` loads it.
6. Test `rish -c 'id'`.
7. Accept only an actual `uid=2000(shell)` result.

Shizuku "running" does not prove `rish` health. A displayed Shizuku version label does not by itself prove the installed package version. Package visibility from an untrusted app UID may also hide installed packages.

If Shizuku/rish is unhealthy, do not globalize the failure. Use the direct ADB lane when authorized and supported.

### Phase 5 — direct Wireless ADB lane

1. Ensure the Termux ADB client can start its daemon from a writable Termux temp directory. If it attempts `/tmp` and receives permission denied, set `TMPDIR=$PREFIX/tmp`.
2. On Android, open Wireless debugging -> Pair device with pairing code.
3. Treat the six-digit pairing code as an ephemeral secret. Do not persist it in skill source, public receipts or logs.
4. Distinguish the temporary pairing endpoint from the normal Wireless ADB connection endpoint; they are often different ports.
5. Run `adb pair <pairing-host:pairing-port>` and provide the code through the authorized interactive channel.
6. Connect with `adb connect <wireless-adb-host:port>`.
7. Verify the device is in `device` state.
8. Execute `adb -s <serial> shell id`.
9. Require `uid=2000(shell)` and record the SELinux context.
10. Bind future governed commands to the authenticated device serial. If multiple devices are connected and the target is ambiguous, fail closed.

### Phase 6 — governed privilege gate

Install or adapt `scripts/leeway-priv.sh`.

Required behavior:

- normal Termux remains the default execution context;
- privileged Android work enters the wrapper explicitly;
- the wrapper proves `uid=2000(shell)` before executing;
- the wrapper binds to a specific authenticated ADB device;
- no shell identity means BLOCKED, not simulated success;
- destructive command families remain denied by default;
- consequential mutation still requires Creator/user authorization and rollback planning;
- commands and outcomes are logged without credentials, pairing codes or tokens.

## Known failure signatures and repairs

### Colored red/pink/blue overlay across Android UI

Likely cause: Debug GPU overdraw enabled.

Evidence example: `debug.hwui.overdraw=show`.

Repair: turn Debug GPU overdraw off. Do not disable unrelated developer options.

### ADB server cannot open `/tmp/adb.<uid>.log`

Cause: Termux cannot use the host-style `/tmp` path.

Repair: use `TMPDIR=$PREFIX/tmp`, create the directory and restart/retry the Termux ADB client.

### Shizuku start shows `SSLV3_ALERT_CERTIFICATE_UNKNOWN`

Cause: Wireless ADB certificate is not paired/trusted for that Shizuku session.

Repair: complete Shizuku Wireless Debugging pairing first, then start the service.

### Shizuku says running but `rish` fails

Classification: service running != terminal bridge healthy.

Repair order:

1. export a fresh matching `rish` pair;
2. set the terminal package ID correctly;
3. enforce non-writable DEX on Android 14+;
4. retest;
5. if the terminal bridge remains unhealthy, use the independently paired direct ADB lane rather than inventing shell success.

### `pm list packages` appears to say an app is missing from ordinary Termux

Cause may be Android package-visibility restrictions.

Do not infer uninstall from a single app-UID package query. Corroborate with the visible UI, privileged package manager query or another authorized source.

### `pm list packages` under shell reports inaccessible secondary user/profile

Scope the query to the active Android user, e.g. `--user 0`, rather than treating unrelated profile denial as total Package Manager failure.

## Acceptance states

- `PRESENT`
- `INSTALLED`
- `DEVELOPER_OPTIONS_READY`
- `REMOTE_REACHABLE`
- `DIRECT_EXECUTION_VERIFIED`
- `USB_INDEPENDENT_VERIFIED`
- `PC_INDEPENDENT_VERIFIED`
- `SESSION_RECOVERY_VERIFIED`
- `COLD_BOOT_VERIFIED`
- `WIRELESS_ADB_PAIRED`
- `ADB_DEVICE_CONNECTED`
- `ANDROID_SHELL_VERIFIED`
- `GOVERNED_PRIVILEGE_GATE_VERIFIED`
- `DEVELOPER_ANDROID_STATE_VERIFIED`

No lower state implies a higher state.

## Continuous durability gate

Cold-boot reconnect does not prove indefinite background liveness.

Before claiming ALWAYS_ON or 100-percent durability, additionally require:

- Android/OEM background restrictions reviewed and the workstation host exempted where appropriate;
- Remote MCP control plane isolated from heavy media, TTS, model, build or other long-running child workloads;
- no orphaned child processes accumulating in the control-plane runtime;
- durable foreground-service or equivalent Android-supported keepalive strategy where required;
- sustained liveness soak testing under representative workload;
- recovery verified after process pressure, screen-off/Doze conditions, ordinary app switching and network changes.

Wireless ADB connection ports can change after Wireless Debugging restarts. Persistent pairing does not imply a permanently fixed connection endpoint.

## Control boundary

### Verified ordinary workstation control

Within the Termux/Android app boundary, a qualified Remote MCP client can perform direct ping/health, shell execution, Termux-accessible file read/write/edit/list, content search, Node.js/npm, Git, HTTPS/curl, OpenSSH tooling, repository operations, local build/test work that fits the phone, session recovery and boot reconnect.

### Verified ADB-shell control

When `uid=2000(shell)` is freshly proven, the governed lane may perform operations available to Android's shell user, including many package, settings, activity/service and diagnostic commands.

ADB shell is not root. It does not grant unrestricted access to protected app-private data, OEM/signature permissions, credentials, secure hardware or arbitrary kernel/system partitions.

### Separately authorized capabilities

Notifications, unrestricted camera/microphone, Bluetooth/USB/HID, screen observation, tap/swipe/type, accessibility and other Android-native surfaces require separately authorized and verified providers.

## Device Manager registration

Register the ordinary workstation provider as:

- provider: `desktop-commander-android-workstation`
- node: `leeway-phone-workstation`
- boundary: `TERMUX_APP_UID_NON_ROOT`

Optional privileged provider:

- provider: `leeway-android-adb-shell`
- node: qualified target phone
- boundary: `ANDROID_ADB_SHELL_NON_ROOT`
- acceptance: exact `uid=2000(shell)` proof
- routing: explicit authenticated device serial

Logical workstation capabilities:

- `workstation.remote.ping`
- `workstation.shell.execute`
- `workstation.files.read`
- `workstation.files.write`
- `workstation.search`
- `workstation.git.local`
- `workstation.github.network`
- `workstation.session.recover`
- `workstation.boot.reconnect`
- `android.adb.pair`
- `android.adb.connect`
- `android.shell.execute`
- `android.settings.read`
- `android.package.inspect`

Mutation capabilities are not automatically authorized merely because shell authority exists.

## Failover rule

A work item requests logical capabilities, never a specific PC, IP address or phone model. Resolve requirements against the device/node registry, user authorization, live health and supported capabilities.

Preferred privileged routing:

1. already verified authorized Android-native provider when the operation requires it;
2. healthy `rish` when specifically required;
3. direct authenticated ADB shell;
4. ordinary Termux for non-privileged work;
5. BLOCKED with exact dependency if no authorized route exists.

Never silently broaden authority to "make it work."

## Developer portability rule

`DISCOVER -> INSPECT -> INSTALL -> CONFIGURE -> PAIR -> DIRECT EXECUTION -> REMOVE PC -> REMOVE USB -> RECOVERY -> COLD BOOT -> ADB SHELL PROOF -> GOVERNED GATE -> VERITAS -> RECEIPT -> VERIFIED`

Android vendor, Android version, Termux distribution, ADB client, Shizuku and Desktop Commander versions may change behavior. Re-run qualification after material upgrades.

## Proof law

`installed != running`
`running != healthy`
`paired != connected`
`connected != executable`
`rish present != rish healthy`
`Shizuku running != shell command verified`
`Termux command success != Android shell authority`
`uid=2000(shell) != root`
`configured != proven`
`first success != completion`

## Evidence requirements

A receipt should include:

- phone class/model and Android version without unnecessary unique identifiers;
- architecture and relevant tool versions;
- ordinary Termux boundary;
- Remote MCP direct ping and execution evidence when workstation qualification is claimed;
- PC/USB independence, recovery and cold boot when those claims are made;
- ADB pair/connect state when privileged lane is claimed;
- exact `id` output proving `uid=2000(shell)`;
- SELinux context;
- active Android user where relevant;
- governed wrapper identity/hash and rollback reference;
- negative/destructive-command test;
- unresolved limitations and provider boundaries.

Never publish pairing codes, Remote MCP tokens, refresh tokens, Google account identifiers, private keys or other credentials.

## Completion rule

For ordinary workstation qualification, require `SECONDARY_WORKSTATION_VERIFIED`.

For the full developer state, require `DEVELOPER_ANDROID_STATE_VERIFIED`, including a live governed privilege lane or an explicit record that privileged shell was not requested.

First success is not completion.
