# Cursor rules for this repo (loadout)

## Primary goal
Keep this repo **KISS**: minimal, stable, low-maintenance bash automation (starting with Ubuntu 24+).

## Script conventions
- Scripts in `_req/`, `_pre/`, `_tags/<tag>/`, and `_tags/<tag>/optional/` (within any OS layer like `debian/ubuntu/`) are **snippets**.
 - They MUST NOT include boilerplate like `#!/usr/bin/env bash`, `set -euo pipefail`, `source lib/common.sh`, or `ensure_os`.
  - They are executed via `lib/run-script.sh`, which applies strict mode and loads shared helpers.
- Prefer using helpers from `lib/common.sh`:
  - `sudo_run`, `log`, `die`, `fetch_url` (curl/wget agnostic).

## KISS / stability rules
- Prefer `apt-get install -y <pkg>` / `snap install <pkg>` over manual repo/key management.
- Avoid PPAs and custom kernels unless there is a clear, stable, Ubuntu-supported reason.
- Avoid version-specific branching where possible; target Ubuntu 24+.
- Minimize new dependencies and avoid “install both curl and wget”.

## Layer selection rules for agent edits
- When adding/updating software, evaluate layers from lowest to highest specificity (`debian/` -> `debian/ubuntu/` -> version layer).
- Default to adding a baseline in the **lowest compatible layer** when compliance/stability/performance is equal or better.
- If a higher layer has a meaningful compatibility or performance advantage, add an override in that layer too.
- If both Debian and Ubuntu layers exist and Ubuntu is better, add **both** implementations using the **same basename** so Ubuntu overrides Debian automatically.
- Only omit the lower-layer implementation when it is unsupported or unsafe outside the higher layer.

## Optional scripts
- Optional scripts live under `_tags/<tag>/optional/` and are installed only via:
  - `-o/--optional` (for selected tags), `--<tag>-optional`, or `--<tag>--<script>`.

