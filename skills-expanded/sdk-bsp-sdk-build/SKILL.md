---
name: sdk-bsp-sdk-build
description: Build Axera SoC SDK images and package AXP download bundles after host environment is prepared. Covers platform discovery (make plist), full AXP builds, standalone component builds, output verification, and build-option configuration across Axera platforms.
version: 1.0.0
metadata:
  author: Axera BSP Team
  tags: [axera, bsp, sdk, build, make, axp, atf, optee, uboot, kernel, rootfs]
  data-classification: public
---

# Axera SDK Build

## Purpose

Compile a selected Axera SoC platform and generate boot/system images or an AXP download bundle. Assume the host has passed `sdk-bsp-sdk-environment` checks.

## When to use

Use when:
- Querying supported board target platforms via `make plist`;
- Compiling full SDK release packages and packaging `.axp` bundles for AXDL;
- Compiling standalone boot/system components (`boot/atf`, `boot/optee`, `boot/uboot`, `kernel/linux`, `rootfs`);
- Configuring build options in `build/platforms/<vendor>/<PLAT>/config.mk`.

Route missing compilers/packages or unexpanded sources to `sdk-bsp-sdk-environment`; route partition/DDR changes to `sdk-bsp-memory-partition`; route flashing to AXDL workflows.

## Routing

1. If args contains `platform=<id>`, use the registered `m57` or `ax637` target. Ask for clarification if the id is unsupported.
2. Otherwise evaluate all `detect` entries in `routing.yaml` against the SDK root. Use the platform only when exactly one platform matches. If multiple platforms match, report the conflicting markers and ask for the SDK/platform before loading platform documents or building. If none matches, execute `fallback: ask`.
3. Identify the SDK using `board-*` or SDK-specific `SafetyIsland/` markers. `build/platforms/axera/` can contain targets for both M57 and AX637; these directories identify available build configurations, not the SDK family or the user's selected `PLAT`.
4. For platforms with `extends`, load the parent `platforms/<parent>.md` first, then overlay the current platform. Report the platform (`display` name and explicit argument or detected path) so the user can verify.
5. Load `platforms/<id>.md` and `reference/<id>/_index.md` for the selected platform. Confirm the user's `PLAT` separately using `make plist`; do not select a target from directory presence alone.

## Instructions

1. **Identify the platform.** In `build/`, run `make plist` to inspect supported targets (`BOARDNAME_FLASHTYPE`). Choose only listed platforms.

2. **Run full build and packaging.** From SDK `build/`, execute:
   ```sh
   make PLAT=<listed_platform> clean all install axp
   ```
   Generates component images under `build/out/<PLAT>/images/` and packages `axera_<PLAT>_<SDK_VERSION>_<timestamp>.axp` in `build/out/`.

3. **Build standalone components (when needed).** From the component directory (`boot/atf`, `boot/optee`, `boot/uboot`, `kernel/linux`, `rootfs`), run:
   ```sh
   make PLAT=<listed_platform> clean all install
   ```
   Outputs are staged to `build/out/<PLAT>/`. Refer to `platforms/<id>.md` for exact defconfigs and DTS paths.

4. **Configure build options.** Tune options in `build/platforms/<vendor>/<PLAT>/config.mk` (e.g. `SUPPORT_OPTEE := FALSE` to disable OP-TEE). Re-run `make PLAT=<PLAT> axp` from `build/` to package changes.

5. **Verify build outputs.** Confirm generated images (`fdl1`, `fdl2`, `u-boot`, `kernel`, `rootfs`, plus `bl31`/`optee` only when `SUPPORT_ATF`/`SUPPORT_OPTEE` are enabled) in `build/out/<PLAT>/images/` and verify the `.axp` package exists and is non-empty.

## Safety

- `clean` removes generated artifacts; confirm the target `PLAT` before executing.
- Successful compilation does not validate partition layout, signatures, or flashing success.
- Do not modify partition JSON or secure boot keys to bypass build errors; route to dedicated skills.

## Reference Documents

For complete official instructions, refer to `00 - AX SDK 使用说明.doc` in the released Axera SDK documentation package.
Platforms and reference mappings:
- [M57 Platform](platforms/m57.md)
- [AX637 Platform](platforms/ax637.md)
- [M57 Reference](reference/m57/_index.md)
- [AX637 Reference](reference/ax637/_index.md)
