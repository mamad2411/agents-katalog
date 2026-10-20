---
name: embedded-linux
domain: embedded
level: domain
description: Reusable embedded-Linux patterns — sysroot, target filesystem, shared-library dependency inspection, runtime loader paths, deployment, and resource constraints — independent of any specific board.
tags: [embedded, "embedded linux", "arm linux", aarch64, sysroot, systemd]
triggers: [aarch64, sysroot, "embedded linux", "arm linux", "target filesystem", ldd, readelf, systemd]
version: "1.0.0"
requires: []
recommends: []
capabilities: []
conflicts: []
when_to_use: A Linux-based embedded/single-board target (ARM/aarch64 or otherwise) —
  deployment, dependency, or resource-constraint questions independent of the toolchain
  mechanics themselves.
when_not_to_use: A bare-metal (no-OS) embedded target, or a question that's really about the
  cross-compilation toolchain itself (see embedded/cross-compilation for that half).
---

# Skill: embedded-linux

## Purpose

The recurring, board-independent facts about developing for a Linux-based embedded/single-board
target — deliberately not board-specific (no per-board skill exists yet; keep board details in
project context until a board proves worthy of its own skill).

## Method

1. **A target filesystem is usually much smaller and more locked-down than a desktop
   distribution** — assume no package manager, no compiler, and a read-only or size-constrained
   root filesystem unless proven otherwise; a fix that works by "just install X" on a desktop
   often has no equivalent on the target.
2. **`ldd`/`readelf -d` reveal a binary's actual runtime shared-library dependencies** — before
   assuming a "cannot execute binary file" or "error while loading shared libraries" failure is
   a build problem, check whether the target's filesystem actually has the required `.so`
   versions (and the right ABI — see cross-compilation below) at the paths the binary expects.
3. **The runtime dynamic loader's search path (`/etc/ld.so.conf`, `LD_LIBRARY_PATH`, or an
   RPATH/RUNPATH baked into the binary at link time) determines which shared library actually
   loads at runtime** — a library present on the filesystem but not on the loader's search path
   still fails to load; `ldd` on the target (not the host) shows what actually resolves.
4. **Resource constraints are real design constraints, not just performance tuning** — limited
   RAM/flash/CPU on many embedded-Linux targets means a technique that's fine on a desktop
   (loading a whole file into memory, a large in-memory cache, verbose logging by default) can
   OOM-kill the process or wear out flash storage; treat memory/storage budgets as a hard
   requirement to check, not an afterthought.
5. **Deployment is usually SSH/SCP-based (or an image-flashing step), not a package manager
   install** — know which one applies to the target before assuming a deployment step; a target
   without network access at all needs a physical/serial deployment path instead.
6. **`systemd` (where present) determines what "the service isn't running" actually means** —
   `systemctl status <unit>` and `journalctl -u <unit>` are the first place to look before
   assuming application-level code is at fault; see `it/linux` for the general Linux
   troubleshooting method this specializes.
7. **Serial console and GPIO access usually require specific group membership or udev rules**
   on the target — a "permission denied" opening `/dev/ttyUSB0` or a GPIO sysfs path is very
   often a udev/group configuration gap on that specific image, not a code bug.
8. **Remote debugging (gdbserver, a remote toolchain-aware debugger) needs matching debug
   symbols built for the target's actual architecture/ABI** — debug info built for the host
   architecture is useless against a target binary; confirm the debug build was actually cross-
   compiled, not accidentally built for the host.

## Anti-patterns

- Assuming a technique that works on a desktop Linux distribution (arbitrary package installs,
  unconstrained memory use) transfers directly to a resource-constrained target.
- Debugging a "shared library not found" error as an application bug before checking `ldd`
  against the target's actual filesystem and loader search path.
- Assuming a permission error on a serial/GPIO device is a code bug rather than a udev/group
  configuration gap on that image.
