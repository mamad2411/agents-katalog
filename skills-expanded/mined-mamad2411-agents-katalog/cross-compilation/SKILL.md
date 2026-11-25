---
name: cross-compilation
domain: embedded
level: technology
description: The mechanical half of targeting a different architecture than the build host — toolchain triples, sysroot, and CMake toolchain files — independent of any specific board or OS image.
tags: [cross-compile, "cross-compilation", "toolchain file", "target triple"]
triggers: [cross-compile, "cross compilation", "toolchain file", "target triple", sysroot]
version: "1.0.0"
requires: []
recommends: []
capabilities: []
conflicts: []
when_to_use: Building software that runs on a different architecture/OS than the machine doing
  the build — the toolchain/sysroot mechanics specifically.
when_not_to_use: A question about runtime behavior on the target after a successful cross-
  compile (see embedded/embedded-linux for that), or a build that isn't actually
  cross-compiling anything.
---

# Skill: cross-compilation

## Purpose

The toolchain-level mechanics of cross-compilation — deliberately separate from
`embedded/embedded-linux`'s runtime/deployment concerns, since a project can cross-compile
without CMake (a raw Makefile + toolchain), or need CMake toolchain guidance without every
embedded-Linux runtime concern applying.

## Method

1. **A target triple (`arch-vendor-os-abi`, e.g. `aarch64-linux-gnu`) identifies the actual
   toolchain to use** — a compiler named `aarch64-linux-gnu-gcc` targets that triple
   specifically; using the host's plain `gcc`/`g++` (even with `-march`/`-mtune` flags) does not
   cross-compile, it just tunes code that still targets the host architecture and ABI.
2. **A sysroot is the target's own headers and libraries, used at build time, not runtime** —
   the cross-compiler needs to link against the target's actual `libc`/system libraries (via
   `--sysroot=<path>`), not the host's; a mismatched or missing sysroot produces link errors
   about undefined symbols that exist on the host but not necessarily in the target's libc
   version, or silent ABI mismatches that only surface at runtime on the target.
3. **A CMake toolchain file must be passed before the first `project()` call runs its compiler
   checks** — via `-DCMAKE_TOOLCHAIN_FILE=<path>` on the initial `cmake` configure, not added
   later; CMake's compiler-identification step happens very early, and a toolchain file applied
   too late (or a fresh build directory not used) leaves stale host-compiler results cached in
   `CMakeCache.txt`. See `software/cmake` for the general toolchain-file mechanism this
   specializes.
4. **Host tools invoked during the build (a code generator, `protoc`, a build-time script) must
   still run on the host, even inside a cross-compiling build** — a toolchain file that
   redirects the C/C++ compiler to the target doesn't redirect every executable CMake might
   invoke; a build-time tool needs to either be a genuinely separate host-native build, or an
   explicitly-excluded exception in the cross-compile configuration.
5. **ABI mismatches between host-built and target-built artifacts are usually silent until
   runtime** — mixing a host-compiled static library into a target build (or vice versa)
   typically still links successfully (same architecture name, wrong ABI/calling convention) and
   fails as a crash or corruption on the actual target device instead of a build error.
6. **"Works when built natively on the target, fails when cross-compiled" is almost always a
   toolchain/sysroot/flag mismatch, not a logic bug** — compare the actual compiler flags,
   defines, and library versions between the two builds before re-reading application code.

## Anti-patterns

- Using the host's own compiler with architecture flags and calling it cross-compilation.
- Applying a CMake toolchain file after the first configure instead of on the initial `cmake`
  invocation with a clean build directory.
- Linking a host-built static/shared library into a cross-compiled target build and only
  discovering the ABI mismatch as a runtime crash.
