---
name: sdk-bsp-sdk-environment
description: Prepare an Axera SoC SDK Linux host for development. Covers Ubuntu prerequisites, cross-toolchains installation, SDK archive extraction, sdk_unpack.sh source acquisition, and host readiness verification across Axera platforms.
version: 1.0.0
metadata:
  author: Axera BSP Team
  tags: [axera, bsp, sdk, environment, toolchain, ubuntu, sdk_unpack]
  data-classification: public
---

# Axera SDK Environment

## Purpose

Prepare an Axera SoC SDK Linux host environment ready for compilation. Keep host provisioning, toolchain deployment, and source expansion separate from build and compilation commands.

## When to use

Use when:
- Setting up a new Linux/Ubuntu build host;
- Installing, configuring, or repairing SDK cross-compilation toolchains;
- Unpacking a fresh SDK release archive;
- Expanding or repairing Linux/U-Boot/ATF/OP-TEE sources via `sdk_unpack.sh`.

Route `make` compilation and image packaging to `sdk-bsp-sdk-build`.

## Routing

1. If args contains `platform=<id>`, use it directly; otherwise match `routing.yaml` against the workspace.
2. For platforms with `extends`, load the parent `platforms/<parent>.md` first, then overlay the current platform.
3. Report the detected platform (`display` name and source) in one sentence so the user can verify.
4. If no platform matches, execute `fallback: ask`; do not infer unverified platform paths.
5. Load `platforms/<id>.md` for platform-specific toolchains, paths, configuration details, and reference documents via `reference/<id>/_index.md`.

## Instructions

1. **Identify the checkout and host.** Confirm the target platform, SDK archive/directory, host OS version, and network accessibility. Work from the extracted SDK root directory; preserve any existing changes.

2. **Install host prerequisites.** On the Ubuntu baseline, install required build tools and libraries (`make`, `build-essential`, `gcc`, `g++`, 32-bit compatibility libraries `libc6:i386`, `lib32stdc++6`, `lib32z1`, `u-boot-tools`, `device-tree-compiler`, etc.). Configure Python dependencies and ensure `/bin/sh` uses bash-compatible behavior (`dpkg-reconfigure dash` -> No).

3. **Install platform toolchains.** Refer to `platforms/<id>.md` for the exact compiler versions, archive names, and required count. Extract toolchains under `/usr/local` (or the documented path), export each `bin` path in `PATH` (`/etc/profile` or `~/.bashrc`), and verify each compiler with `<toolchain-prefix>-gcc -v`.

4. **Align RTOS/MCU toolchain paths (if applicable).** For platforms with MCU RTOS (such as RT-Thread), inspect the platform config (e.g. `RTT_CONFIGS`) and verify that configuration files (e.g. `rtconfig.py` `EXEC_PATH`) strictly align with the installed toolchain path.

5. **Extract and expand SDK sources.** Extract the SDK release archive. Run `./sdk_unpack.sh` to download and patch upstream kernel and bootloader sources. If offline or download URLs fail, supply matching local source archives using script parameters (e.g. `-k`, `-u`, `-a`, `-o`).

6. **Verify readiness.** Confirm all required compilers respond with `-v`, expected source trees exist after `sdk_unpack.sh`, and `build/` configuration files are present. Avoid running `sdk_clean.sh` carelessly as it removes extracted and patched source trees.

## Safety

- Modifying system paths or `/etc/profile` requires administrative privileges; display target paths before making changes.
- Use the exact compiler versions specified in `platforms/<id>.md`; mismatched toolchains may lead to ABI breakage or boot firmware build failures.
- `sdk_clean.sh` is destructive to expanded source trees; verify backups before executing.
- Keep source archives and SDK patch revisions strictly coupled.

## Reference Documents

For the complete official instructions, refer to `00 - AX SDK 使用说明.doc` in the externally released Axera SDK documentation package (typically located under the release archive's `doc/` or `docs/` directory, providing authoritative details on host environment setup, toolchain installation, SDK expansion, project build, and firmware flashing across platforms).
Platforms and reference mappings:
- [M57 Platform](platforms/m57.md)
- [AX637 Platform](platforms/ax637.md)
- [M57 Reference](reference/m57/_index.md)
- [AX637 Reference](reference/ax637/_index.md)
