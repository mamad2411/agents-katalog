---
name: system-wide-tool-management
description: Industrial protocol for detecting, installing, and verifying system-wide
    CLI tools (e.g. jq, curl, git) across macOS, Linux, and Windows. Use whenever a
    system tool is required but may not be installed or available in PATH.
category: Environment-Management
---

# System-Wide Tool Management Skill

This skill defines the industrial protocol for managing **system-wide CLI tools** — tools
that must be available on the OS `PATH` and are not managed by `mise` or any
project-local package manager.

A **system-wide tool** is any binary expected to be globally available (e.g. `jq`, `curl`,
`git`, `grep`, `brew`). This contrasts with project-local tools managed by `mise`, `npm`,
or `pip`.

```text
Layer 1: System Tool Detection & PATH Verification  (base)
└── Layer 2: System Tool Installation               (depends on Layer 1)
    └── Layer 3: Post-Install PATH Verification     (depends on Layer 2)
```

> **Corporate-environment fallback:** On a corporate workstation where `winget` / `scoop`
> / `choco` are disallowed but the organization mounts a shared tool root
> (`<toolbase>`, e.g. a path like `C:\<toolbase>\<package>\<version>\`), Layer 2 of this
> skill is not applicable — the organization itself is the package manager. In that case,
> consult your organization's internal skill library (if one exists) for a
> toolbase-interpreter-discovery skill that enumerates `<toolbase>\<package>\` version
> directories, picks the highest stable version, resolves the executable, and prepends
> its directory to `$env:Path` for the current session; then re-run Layer 1 / Layer 3 of
> this skill against the activated `PATH`. This skill intentionally does NOT link to any
> specific organization's internal library (per
> [`redaction-portability`](../redaction-portability/SKILL.md) §0.1).

***

## 1. Layer 1 — Detection & PATH Verification

Before using any system tool, the agent MUST verify it is installed and reachable on
`PATH`.

### 1.1 Detection Command

```bash
# Generic check — replace `jq` with the tool name
which jq 2>/dev/null && jq --version || echo "NOT_FOUND"
```

- `which jq` — Locates the binary on `PATH`.
- `jq --version` — Confirms it executes correctly (not a broken symlink).
- `echo "NOT_FOUND"` — Sentinel output for scripted detection.

### 1.2 OS Detection

Determine the operating system to select the correct package manager:

```bash
uname -s
# → Darwin  (macOS)
# → Linux   (Linux)
# → MINGW*  (Windows/Git Bash)
```

For Windows, also check:

```bash
winget --version 2>/dev/null || echo "winget_not_found"
```

***

## 2. Layer 2 — System Tool Installation

If the tool is not found, the agent follows a **recursive fallback protocol** for each
package manager (PM) in priority order.

> **User Confirmation Gate (MANDATORY)**: The agent MUST present every proposed command
> and ask `"Shall I run this? (yes / no)"` before executing it. Incorporate any user
> feedback and ask again.
>
> **Tool Identification Gate (MANDATORY)**: When proposing a tool installation, the agent
> MUST provide a link to the tool's official documentation or repository (e.g., GitHub page)
> to ensure the correct tool is picked up. The user will verify this before confirming.

### 2.1 Installation Priority Matrix

| OS | Primary | Fallback 1 | Fallback 2 | Fallback 3 |
| :--- | :--- | :--- | :--- | :--- |
| **macOS** | `brew` | `port` (MacPorts) | — | Manual (ask user) |
| **Linux (Debian/Ubuntu)** | `apt-get` | `snap` | — | Manual (ask user) |
| **Linux (RHEL/Fedora)** | `dnf` | `yum` | — | Manual (ask user) |
| **Linux (Arch)** | `pacman` | `yay` (AUR) | — | Manual (ask user) |
| **Windows** | `scoop` | `winget` | `choco` | Manual (ask user) |

### 2.2 Self-Installable vs OS Built-In Package Managers

Not all package managers can themselves be installed if missing:

| Package Manager | Self-Installable? | Install Method |
| :--- | :--- | :--- |
| `brew` (macOS) | ✅ Yes | Official install script via `curl` |
| `port` (macOS) | ✅ Yes | Download from macports.org |
| `scoop` (Windows) | ✅ Yes | PowerShell one-liner |
| `winget` (Windows) | ✅ Yes | Microsoft App Installer (MSIX) |
| `choco` (Windows) | ✅ Yes | PowerShell one-liner |
| `apt-get` (Linux) | ❌ No | OS built-in; if absent, the OS is incompatible |
| `dnf` / `yum` (Linux) | ❌ No | OS built-in |
| `pacman` (Linux) | ❌ No | OS built-in |
| `snap` (Linux) | ✅ Yes | `sudo apt-get install snapd` |
| `yay` (Arch AUR) | ✅ Yes | Build from AUR |

### 2.3 Universal Recursive Protocol (Applies to Every PM Attempt)

For **each** package manager in the priority order, apply the following decision tree
before moving to the next fallback:

```text
[START] Check if <PM> exists:
  which <pm> && <pm> --version

  ┌─ FOUND ──────────────────────────────────────────────────────────────┐
  │  Propose tool install. Ask user confirmation.                        │
  │  → User YES → install tool → Layer 3 (PATH verify) → DONE           │
  │  → User NO  → skip to next fallback                                  │
  └──────────────────────────────────────────────────────────────────────┘

  ┌─ NOT FOUND ───────────────────────────────────────────────────────────┐
  │  Is <PM> self-installable? (see §2.2)                                │
  │                                                                       │
  │  YES (e.g. brew, scoop, winget):                                     │
  │    Present user TWO options:                                          │
  │      Option A: "Shall I install <PM> itself? (yes / no)"             │
  │        → YES → install <PM> → then install tool → Layer 3 → DONE    │
  │        → NO  → skip to next fallback                                 │
  │      (User may choose option B directly to skip)                     │
  │      Option B: "Skip to next fallback <next-PM>? (yes / no)"         │
  │        → YES → recurse into next PM from [START]                     │
  │                                                                       │
  │  NO (OS built-in, e.g. apt-get not on this system):                 │
  │    This OS flavour is incompatible. Present user ONE option:          │
  │      "apt-get is not available on this system.                        │
  │       Try next fallback <next-PM>? (yes / no)"                       │
  │        → YES → recurse into next PM from [START]                     │
  │        → NO  → halt; document; ask for manual install                │
  └──────────────────────────────────────────────────────────────────────┘

  [ALL PMs EXHAUSTED] → §2.8 Manual Fallback
```

### 2.4 macOS — PM Install Commands

Use when a macOS PM is present but the user selects it, or when proposing PM installation.

**`brew` (primary) — install the tool:**

```bash
# Only after user confirms:
brew install jq
```

**`brew` — self-install (if missing):**

```bash
# Only after user says yes to "Shall I install Homebrew?"
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**`port` (MacPorts fallback) — install the tool:**

```bash
# Only after user confirms:
sudo port install jq
```

**`port` — self-install (if missing):**

> Direct user to: `https://www.macports.org/install.php`. Ask user to install and
> confirm "done" before continuing.

### 2.5 Linux — PM Install Commands

Linux primary PMs (`apt-get`, `dnf`, `pacman`) are OS built-ins and cannot be
self-installed. If they are missing, the OS flavour is incorrect — skip to the fallback.

**`apt-get` (Debian/Ubuntu):**

> **Note on `sudo`**: Notify user before proposing. Ask:
> `"These commands need sudo (elevated). Shall I run them? (yes / no)"`

```bash
# Only after user confirms — no -y; full interactive output:
sudo apt-get update
sudo apt-get install jq
```

**`dnf` (RHEL/Fedora):**

```bash
# Only after user confirms:
sudo dnf install jq
# or, on older systems:
sudo yum install jq
```

**`pacman` (Arch):**

```bash
# Only after user confirms — no --noconfirm; full interactive output:
sudo pacman -Sy jq
```

**`snap` (fallback, self-installable):**

If `snap` itself is missing, offer to install it:

> `"snap is not installed. Shall I install snapd? (yes / no)"`

```bash
# Install snapd first (requires sudo confirmation):
sudo apt-get install snapd
# Then install the tool:
sudo snap install jq
```

**`yay` (Arch AUR fallback, self-installable):**

If `yay` is missing, offer to build it:

> `"yay is not installed. Shall I build it from AUR? (yes / no)"`

```bash
# Build yay from AUR (only after user confirms):
git clone https://aur.archlinux.org/yay.git /tmp/yay-build
cd /tmp/yay-build && makepkg -si
# Then install the tool:
yay -S jq
```

### 2.6 Windows — PM Install Commands

All Windows PMs are self-installable. Apply the recursive protocol from §2.3.

**`scoop` (primary) — install the tool:**

```bash
# Only after user confirms:
scoop install jq
```

**`scoop` — self-install (if missing):**

> `"scoop is not installed. Shall I install it? (yes / no)"`

```powershell
# Only after user confirms (PowerShell):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

**`winget` (fallback) — install the tool:**

```bash
# Only after user confirms — no --silent; full verbose output:
winget install --id stedolan.jq -e
```

**`winget` — self-install (if missing):**

> Direct user to: `https://aka.ms/getwinget` (Microsoft App Installer). Ask user to
> install and confirm "done" before continuing.

**`choco` (fallback 2) — install the tool:**

```bash
# Only after user confirms:
choco install jq
```

**`choco` — self-install (if missing):**

> `"choco is not installed. Shall I install Chocolatey? (yes / no)"`

```powershell
# Only after user confirms (PowerShell, run as Administrator):
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### 2.7 Presenting Options to the User

When a PM is missing and IS self-installable, the agent MUST present both options clearly:

```text
`scoop` is not found on this Windows system.

Option A: Install scoop, then use it to install jq.
  Proposed command:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    scoop install jq

Option B: Skip scoop and try the next fallback (winget).

Which would you prefer? (A / B)
```

### 2.8 Manual Fallback

If all PMs in the priority list are exhausted:

1. Document every PM attempted and the error for each.
2. Present a clear summary to the USER.
3. Provide exact manual install instructions for the detected OS.
4. Wait for user to confirm "done" before proceeding to Layer 3.

```text
All automatic methods failed for `jq`:
  ① scoop  → not installed; user declined to install
  ② winget → not installed; self-install failed
  ③ choco  → not installed; user declined to install

ACTION REQUIRED — install jq manually:
  scoop   : https://scoop.sh → then: scoop install jq
  winget  : https://aka.ms/getwinget → then: winget install --id stedolan.jq -e
  choco   : https://community.chocolatey.org → then: choco install jq
Reply "done" when installed.
```

***

## 3. Layer 3 — Post-Install PATH Verification

After installation, the agent MUST verify the tool is now on `PATH` before using it.

### 3.1 Verification Command

```bash
# Re-check PATH availability after install
which jq && jq --version
```

- If this fails after a successful install, the shell session may need to refresh its
  `PATH` (common after `brew` installs on macOS with Apple Silicon):

  ```bash
  eval "$(/opt/homebrew/bin/brew shellenv)"
  which jq && jq --version
  ```

### 3.2 Shell Reload

On some systems/shells the `PATH` update requires sourcing the profile if the binary is
newly added to a non-standard location (e.g. `/opt/homebrew/bin`):

```bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true
which jq && jq --version
```

***

## 4. Full Worked Example — `jq` Setup

`jq` is required by the [Mise Tool Management Skill](../mise-tool-management/SKILL.md)
to parse PyPI JSON responses.

### 4.1 Detection

```bash
which jq 2>/dev/null && jq --version || echo "NOT_FOUND"
# → NOT_FOUND
```

### 4.2 OS Check

```bash
uname -s
# → Darwin
```

### 4.3 Installation (macOS)

```bash
brew install jq
# → jq is now installed at /opt/homebrew/bin/jq
```

### 4.4 Verification

```bash
which jq && jq --version
# → /opt/homebrew/bin/jq
# → jq-1.7.1
```

***

## 5. Prohibited Actions

The agent is FORBIDDEN from:

- **Executing any install command without explicit user confirmation.** Every proposed
  command MUST be shown to the user with a "(yes / no)" gate before it runs.
- **Running `sudo` silently.** The agent MUST explicitly notify the user that a command
  requires elevated privileges (`sudo`) and wait for approval. Example notice:
  > "This command requires `sudo` (elevated privileges). Shall I run it? (yes / no)"
- **Using auto-accept or silent flags** (`-y`, `--noconfirm`, `--silent`, `-q`,
  `--quiet`). All package manager output MUST be shown in full so the user can review it.
- **Proceeding to use a tool without completing Layer 3** (PATH verification after install).
- **Installing system tools via `pip`, `npm`, or `mise`** — these are for project-local
  tools, not system-wide binaries.
- **Asking the user to install manually before exhausting all fallback package managers**
  per the priority matrix in §2.1.

***

## Related Skills

| Skill | Relationship |
| :--- | :--- |
| [`docker-resource-inventory`](../docker/docker-resource-inventory/SKILL.md) | Consumer — delegates docker CLI install/verify when the binary is absent |
| [`docker-resource-cleanup`](../docker/docker-resource-cleanup/SKILL.md) | Consumer — delegates docker CLI install/verify when the binary is absent |
