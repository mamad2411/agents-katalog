---
name: build-sh-test-sh-shell-script-stdlib
description: Each language subdirectory ships build.sh and test.sh with a shared color.sh helper, so CI calls the same scripts that developers run locally.
category: build
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [magika, build]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Build Sh Test Sh Shell Script Stdlib

**Trigger:** Multi-language monorepo where every CI workflow tends to grow ad-hoc inline scripts that drift from local dev commands.

## Steps

- Create a top-level color.sh exposing info(), warn(), error() with ANSI color (gated on TTY).
- Per language subdir, ship build.sh and test.sh that source color.sh.
- Use set -euo pipefail; fail loudly on first error.
- CI workflows call ./rust/build.sh, ./python/test.sh — never inline complex bash blocks.
- Use distinct exit codes (1 = test fail, 2 = build fail) for downstream automation.
- Document supported shells and platforms (bash on macOS/Linux/WSL/Git Bash on Windows).

## Counter / Caveats

- Bash vs sh vs zsh portability bites; explicitly require bash if you use bash-isms.
- Color output assumes ANSI; detect TTY and disable for redirected output.
- Sourcing across directories needs absolute paths or relative-to-script ($(dirname ${BASH_SOURCE[0]})).
- Windows users need WSL or Git Bash; document or provide a PowerShell variant.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `rust/cli/build.sh`
- `rust/test.sh`
- `rust/color.sh`
- `rust/onnx/build.sh`
