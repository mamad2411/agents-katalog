---
name: luma-environment
description: Luma NoRoot Debian/PRoot environment and Android host bridging tools.
---

# Luma NoRoot Environment

Running on Debian/PRoot on Android ARM64; this is neither Termux nor an Android root shell. Even if `id` shows root, it is simulated by PRoot and actual permissions remain Luma's Android app UID. Check `/etc/os-release` for the distribution version.

- `/workspace`: private workspace; `/root`: home directory. Install Linux packages with `apt`, `npm`, or `pnpm`.
- `/sdcard`: Android shared storage (`/storage/emulated/0`), available in new terminals after granting phone file access in Luma. Private directories of other apps are not exposed.

# Android Host Bridging

These tools execute outside PRoot through Luma, using the app UID or an authorized Shizuku session for native Android capabilities:

- `adb-shell <command>`, `adb-shell --status`: run `adb shell` commands on the Android host via Shizuku (e.g., `pm`, `am`, `dumpsys`, `input`, `screencap -p /workspace/shot.png`). On first use when Shizuku is running without permission, Android prompts for authorization.
- `android-run /workspace/program [args]`: run ARM64/Bionic dynamic ELF binaries directly on Android. Run Debian/glibc programs normally instead of using this wrapper.
- `luma-compute-check --cpu`, `--gpu`, `--list`: verify native CPU/Vulkan compute or enumerate GPUs.
- `luma-browser --help`: control the session-bound built-in browser (web interaction, local previews, screenshots). Read `/opt/luma/agent/skills/luma-browser/SKILL.md` before first use.

The native bridge and `adb-shell` automatically map or relay file path arguments under `/workspace`, `/root`, `/tmp`, and `/sdcard`; pass paths directly as seen inside the Debian environment.
