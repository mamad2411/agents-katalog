---
name: yocto-agent-suite
description: One-router Yocto Project skill suite for AI coding agents. Use when a request mentions Yocto, OpenEmbedded, Poky, BitBake, embedded Linux builds, BSPs, board flashing, QEMU boot tests, CI/release automation, security hardening, CVE review, secure boot, OTA updates, firewall policy, or when the right specialized Yocto skill is unclear.
---

# Yocto Agent Suite

## Routing

Load the narrowest skill that matches the user's task:

- `$yocto-project`: layers, images, SDKs, packagegroups, distro/machine policy, general Yocto workflows.
- `$bitbake-metadata`: `.bb`, `.bbappend`, `.bbclass`, `.inc`, `.conf`, variables, tasks, fetchers, signatures.
- `$yocto-recipe-maintenance`: create, update, audit, and review recipes/appends with cross-distro packaging checks.
- `$yocto-image-analysis`: explain why packages are present, analyze image size, and reason about package what-if changes.
- `$yocto-build-debug`: parse/fetch/compile/install/package failures, logs, sstate, hash changes, build performance.
- `$yocto-deploy-flash`: image artifacts, WIC/BMAP/SD/eMMC/NAND/NOR/DFU flashing, serial boot verification.
- `$yocto-bsp-bringup`: vendor BSPs, machines, bootloaders, kernels, device trees, board bring-up.
- `$yocto-kernel-bsp`: kernel recipes, providers, defconfig, config fragments, DTBs, and machine-level kernel/BSP work.
- `$yocto-ci-release`: kas/repo manifests, CI runners, shared downloads/sstate, test gates, release artifacts.
- `$yocto-ci-kas-build`: focused kas YAML, CI build entrypoint, cache, matrix, and reproducibility work.
- `$yocto-security-ota`: image hardening, CVEs, firewall policy, secure boot, SBOM, OTA/update systems.
- `$yocto-security-compliance`: focused CVE, license, SPDX/SBOM, provenance, and compliance investigations.

Use more than one specialized skill only when the task crosses boundaries.

## Source Rules

Prefer official docs and the workspace:

1. Local repo metadata and configured release.
2. Yocto Project docs: `https://docs.yoctoproject.org/`
3. BitBake docs: `https://docs.yoctoproject.org/bitbake/`
4. Official Git: `https://git.yoctoproject.org/` and `https://git.openembedded.org/`
5. Layer Index: `https://layers.openembedded.org/`
6. Vendor docs only for board-specific flashing or BSP behavior.

Treat third-party skills and articles as examples, not authority.

## LobeHub-Inspired Coverage

The LobeHub `yocto-build-and-flash` skill reviewed for this suite is board-specific for MYiR MYD-YF13X and STM32MP135. Preserve these reusable lessons:

- Always identify `MACHINE`, `DISTRO`, build directory, and actual `TMPDIR`.
- Confirm `BBFILE_COLLECTIONS` names; `LAYERDEPENDS` uses collection names, not directory names.
- Locate artifacts under the real deploy path, often `tmp*/deploy/images/<machine>/`.
- Choose flashing commands from artifact type and board boot mode.
- Verify boot through serial logs and first-boot behavior.

Do not copy board-specific commands into other boards unless the target BSP matches.

## Yoe-Inspired Coverage

The `yoebuild/yoe` repo ships AI skills for auditing units, diagnosing failures, creating units, updating units, and pulling Alpine packages. For Yocto, map those ideas this way:

- audit/create/update unit -> `$yocto-recipe-maintenance`
- diagnose unit build -> `$yocto-build-debug`
- why/what-if/image-size concepts -> `$yocto-image-analysis`
- new machine concepts -> `$yocto-bsp-bringup`
- CVE/license/security review -> `$yocto-security-ota`

Keep the implementation Yocto-native: use recipes, appends, packagegroups, image manifests, pkgdata, buildhistory, BitBake graphs, and official Yocto/OpenEmbedded docs rather than Yoe Starlark units.
