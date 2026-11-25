---
name: esp32-build-and-sdkconfig
description: Use when the build itself is the problem - settings do not take effect, PlatformIO and IDF disagree, a flag is silently overridden, the binary is too big, or the same source builds differently on two machines. Covers sdkconfig, build flags and partition choice.
license: MIT
---

# Build configuration on ESP32

Most "the setting did not apply" bugs are a second, higher-priority definition of
the same setting. The build system has three layers and they override each other
in a fixed order.

## The order that wins

1. `sdkconfig` (generated, do not edit by hand)
2. `sdkconfig.defaults` (yours, applied only when `sdkconfig` is absent)
3. `sdkconfig.<target>` / `sdkconfig.defaults.<target>` (per chip)
4. `-D` flags in `build_flags` / `idf_build_set_flags`

If you change `sdkconfig.defaults` and nothing happens, it is because `sdkconfig`
already exists. Delete it, or change the value in `menuconfig` - the defaults
file is only read on a fresh configuration.

## PlatformIO is not IDF

PlatformIO wraps IDF and adds its own `platformio.ini`. Things that behave
differently:

- `build_flags` are compiler flags, not `CONFIG_` values. `-DCONFIG_FOO=1` does
  not always do what `menuconfig` does, because Kconfig also drives source
  selection at configure time.
- The Arduino core is a component inside IDF in the pioarduino/IDF 5 world; the
  old `framework = arduino` with the precompiled core is a different beast.
- `board_build.partitions` replaces the partition CSV. If it is unset, you get
  the default table, and a 1.2 MB app will not fit in a 1 MB slot.

## The binary is too big

| Lever | Effect |
|---|---|
| `-Os` instead of `-Og`/`-O0` | 15 to 30 % smaller, sometimes faster |
| log level to WARN or ERROR | drops the format strings, tens of kB |
| `CONFIG_COMPILER_OPTIMIZATION_SIZE` | the IDF switch for the above |
| drop unused components | each linked component costs flash even if unused |
| `CONFIG_NEWLIB_NANO_FORMAT` | smaller printf, loses 64-bit float support |

A debug build that fits in a 1 MB slot and a release build that does not is a
partition table decision, not a compiler one.

## Reproducibility

Two machines building the same commit differently is usually:

- different toolchain versions (pin the platform version, not just the framework)
- a stale `sdkconfig` on one of them
- `build/` committed or copied between machines

Pin the platform and framework versions in `platformio.ini`; floating versions
mean a build that worked yesterday fails today for no reason in your code.

| Symptom | Usually |
|---|---|
| setting ignored | `sdkconfig` already exists |
| works in IDF, fails in PlatformIO | different partition table or missing component |
| binary too large after adding a library | log level, or `-Og` in the release env |
| undefined reference to a driver | component not in `REQUIRES` / `build_src_filter` |
| different results on CI and locally | toolchain version not pinned |
