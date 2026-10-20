---
name: just-platform-aware-recipes
description: Structure a justfile so Unix and Windows contributors share the same command names while recipes dispatch by OS.
category: devops
version: 1.0.0
version_origin: extracted
tags: [justfile, cross-platform, windows, powershell, bash]
source_type: extracted-from-git
source_url: https://github.com/jamiepine/voicebox.git
source_ref: main
source_commit: 476abe07fc2c1587f4b3e3916134018ebacd143d
source_project: voicebox
confidence: high
imported_at: 2026-04-18T00:00:00Z
---

# Just platform-aware recipes

## When to use
A single repo is actively developed on macOS/Linux and Windows. Contributors on either side should type `just dev`, `just build`, `just check` and get the same behavior, without separate Makefiles or scripts/ wrappers.

## Steps
1. Declare platform-aware paths at the top: `venv_bin := if os() == "windows" { venv / "Scripts" } else { venv / "bin" }`. Do the same for `python`, `pip`. This single indirection keeps every downstream recipe portable.
2. Set the Windows shell to PowerShell once: `set windows-shell := ["powershell", "-NoProfile", "-Command"]`. Without this, Just will try `sh` on Windows and every recipe fails.
3. Use per-OS recipes (`[unix]` and `[windows]`) for anything that materially differs. The recipe name is shared; Just picks the right body based on `os()`.
4. Detect the best Python interpreter at evaluation time: `system_python := if os() == "windows" { "python" } else { \`command -v python3.12 2>/dev/null || command -v python3.13 2>/dev/null || echo python3\` }`. Users hit a helpful message instead of a stack trace when their venv is built on an incompatible Python.
5. On Windows, adjust GPU detection via `Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name` and branch install flags (CUDA vs XPU vs CPU torch) from that output. Don't hard-code an index URL.
6. Use `[private]` recipes (e.g. `_ensure-venv`, `_ensure-sidecar`) as preconditions on public recipes. They fail-fast with a helpful message ("Run: just setup") instead of running a broken environment.
7. For multi-step shell on Unix, use the `#!/usr/bin/env bash` shebang + `set -euo pipefail` inside the recipe body. On Windows, chain statements with `;` + backslash-continuations — PowerShell doesn't have `bash -e` equivalents.

## Counter / Caveats
- Python version detection only works at recipe invocation. If the user `just setup`s with Python 3.14, catch it and print a warning about ML package incompatibility — don't wait for pip to fail 40 minutes later.
- `just kill` on Windows cannot use `pkill`. Use `Get-Process | Where-Object { $_.CommandLine -like '...' }` or similar. Expect commandline filtering to be flaky — many hosts hide commandline to non-admins.
- Avoid mixing `cmd.exe` and PowerShell idioms in a single Windows recipe; pick one shell per recipe.
- Private recipes still show in `just --list` unless marked `[private]`. Prefix with `_` as a safety net when the attribute isn't supported.

Source references: `justfile` (the whole structure, especially `venv_bin`, `[unix]`/`[windows]` recipe pairs, `_ensure-venv`, Windows GPU detection).
