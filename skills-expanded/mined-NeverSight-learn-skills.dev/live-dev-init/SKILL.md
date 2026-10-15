---
name: live-dev-init
description: Environment preflight checks and initialization. Probes and installs git, gh, node, vercel, firebase-tools, and gitleaks. Verifies .nvmrc, .gitignore, and Git Flow develop branch setup, and enforces the Secret Vault Policy.
---

# live-dev-init

This skill initializes the development environment and performs preflight checks before any other deployment or configuration tasks are run.

`bash` blocks are POSIX (Git Bash on Windows). Any logic beyond one command/pipe lives in `resources/*.js` (if applicable), never in shell control flow. If your Bash tool is cmd.exe or PowerShell, translate each snippet before running it.

## 1. Preflight (run silently, before planning)

| Check | Probe | On fail |
| --- | --- | --- |
| git, gh | `command -v git`, `command -v gh`, `gh auth status` | run `scripts/install-git-gh-macos.command` \| `scripts/install-git-gh-windows.ps1`. Never improvise install steps. |
| node | `node --version` ≥ `scripts/toolchain/catalog.json:node_lts_major` | `scripts/course-toolchain-macos.command base` \| `scripts/course-toolchain-windows.ps1 -Profile base` |
| vercel, firebase | `npx vercel whoami`, `npx firebase login:list` | `npm install -D vercel@latest firebase-tools` (never `-g`: EACCES). Login must pass before setting up config or deploying. |
| gitleaks | `command -v gitleaks` | install per table below, re-probe, never skip the scan gate |

| OS | Install | Fallback |
| --- | --- | --- |
| macOS | `brew install gitleaks` — brew may NOT exist (course installer uses Xcode CLT + curl, not brew) | curl latest release `gitleaks_*_darwin_$(uname -m).tar.gz` → extract to `~/.local/bin` (mkdir + append to shell profile if absent). No sudo, no `/usr/local/bin`. |
| Windows | `winget install gitleaks.gitleaks` | download `gitleaks_*_windows_x64.zip` → extract `gitleaks.exe` → `%USERPROFILE%\bin` → `setx PATH "%PATH%;%USERPROFILE%\bin"`. `~/.local/bin` and shell profiles do not apply here. |

Then repair project state:

| File / state | Required value | Note |
| --- | --- | --- |
| `.nvmrc` | `catalog.json:node_lts_major` | Sole source of truth. `resources/vercel-preview.yml` reads `node-version-file: '.nvmrc'` — never hardcode a Node major in the yml. |
| `.gitignore` | `.env`, `.env.local`, `.env*.local`, service-account JSON glob | Repair before the first commit ever exists — the vault policy assumes these are ignored. |
| branch | `develop` exists (else propose from `main`); work on `feature/<name>` off `develop` | |

**Secret Vault Policy (hard rule, no override).** Credentials live only in Vercel Env Vars / GitHub Secrets / gitignored `.env.local`. Never hardcode in code, never commit real `.env` values, never print a real secret to chat, logs, or commit messages.
