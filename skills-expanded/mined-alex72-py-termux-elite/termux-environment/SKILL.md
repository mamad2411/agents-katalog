---
name: termux-environment
description: Take a small read-only snapshot of a Termux or Android shell (native Termux, proot, another Android shell, or a non-Android system; Android and Termux version, CPU architecture, installed toolchains, free storage and memory) before choosing a package manager, path, or fix. Use when a task depends on what the device is, when asked what is installed or which architecture applies, or at the start of any Termux debugging session. Do NOT use as a ritual before every command, for plain text questions, or to change anything.
license: MIT
compatibility: Termux on Android (Bionic libc, usually aarch64). Where a skill says so, also usable from a proot distro.
metadata:
  risk: "low"
  triggers: "termux environment,android environment,what is installed,which architecture,am i in proot,termux version,android version,is this termux"
---
# Termux Environment

## Purpose
Build a small factual snapshot so later decisions rest on measured facts, not on assumptions about the phone, the shell, or the distro.

## When to use
- A fix depends on Android version, CPU architecture, free space, or installed toolchains.
- It is unclear whether the shell is native Termux, a proot distro, another Android shell, or not Android at all.
- Any other skill in this pack says to capture the environment first.

## When NOT to use
- Plain text questions, or a command whose result does not depend on the device.
- Before every command. Cache the snapshot; refresh only after a package upgrade, entering or leaving proot, or reinstalling Termux.

## Preconditions
Read-only shell only. No root, network, or Termux:API required.

## Decision tree
1. Run `sh scripts/detect-environment.sh`. It prints `key: value` lines and never dumps the environment.
2. Read `environment_class` first; the line beside it, `environment_evidence`, says why. Hints are not proof.
   - `termux-native`: Bionic libc, `pkg`, Termux package names, `$PREFIX` paths. The Termux skills apply as written.
   - `proot`: a distro running under Termux. It has its own package manager and usually glibc; `termux-*` commands and Termux package names belong to the native side. Confirm with `proot-boundaries`.
   - `android-other`: Android properties are readable but there is no Termux prefix (for example an `adb shell` or another terminal app). Do not assume `pkg` or Termux paths; ask.
   - `linux`, `wsl`, `container`, `macos`: not Android. The Termux-specific steps do not apply; use `system_package_manager` and ordinary rules.
   - `unknown`: ask the user. Do not guess.
   Run a command from a Termux skill only when the class is `termux-native`, or the skill says proot is fine.
3. Architecture comes from `architecture`, never from the phone model. `aarch64` is the common case. `armv7l` or `armv8l` means a 32-bit userland, where many prebuilt wheels and binaries do not exist. `x86_64` is an emulator or Chromebook.
4. `android_sdk` selects which Android behavior applies. Report these as version-specific: background clipboard reads are restricted from Android 10; recent releases restrict network interface listing (`ip`, `ifconfig`, `netstat`); Android 12 and later kill excess child processes (see `background-processes`).
5. Hard-coded `/tmp`, `/bin/sh`, or `#!/usr/bin/env` fail on a bare Android layout. Termux uses `$TMPDIR` (`$PREFIX/tmp`) and `$PREFIX/bin/sh`, and `termux-exec` rewrites shebangs. Fix the path or variable, not the system.
6. Under about 1 GiB free storage or available memory: warn before any compile, `pkg upgrade`, or large download.
7. Termux and its plugin apps (Termux:API, Boot, Widget) must come from the same distribution source and signing key, or plugins fail to talk to Termux.

## Example
- Situation: A prebuilt binary will not run and the user says the phone is a recent flagship.
- Without the skill: Guesses arm64 from the phone model and suggests an aarch64 download.
- With the skill: Runs the helper, reads `architecture: armv8l` (a 32-bit userland), explains why aarch64 binaries cannot run, and reports the fact with the line that proves it.

## Safety
Everything here is read-only. `termux-info` prints the device model and the full package list, so share only the lines the task needs. Never print `env` wholesale; it can contain tokens.

## Verification
Every reported fact came from command output in this session. Say `unknown` for anything the script could not read.

## Handoffs
- `proot-boundaries` when native versus proot is unclear or mixed.
- `package-troubleshooting` when no package manager is found or indexes look stale.
- `storage-permissions` when `storage_shared` is absent.
- `python-native-build` when a build needs the toolchain list.

## Report
At most six lines: `environment_class`, architecture, Android API level, Termux version, free storage and memory, and any missing tool that matters for the task.
