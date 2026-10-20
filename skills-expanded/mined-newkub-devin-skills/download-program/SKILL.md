---
name: download-program
description: Find and install programs on the machine via the right package manager, or open the download page
argument-hint: "[program-name]"
related:
  - update-all-program-in-computer
  - use-pwsh-shell
  - search
  - follow-best-practice
  - enhance-prompt
  - run-program
---

## Goal

Help find and install programs on the machine, choosing the suitable package manager via `workflows/package-manager` and falling back to the download page when nothing is found

## Scope

- Works on any OS; `workflows/package-manager` selects the package manager per OS
- Supports `mise`, `scoop`, `winget` on Windows and `mise`, `brew`, `apt`, `pacman`, `yum`, `dnf` on Unix
- If no package manager has the program → open the main download page for the user to install manually
- No guarantee that every program can be installed automatically

## Execute

### 1. Identify Program

> Goal: Identify the program to install

1. Take `program-name` from the argument or the user
2. If the name is ambiguous → use `/enhance-prompt` or `/ask-me`
3. Normalize the name (lowercase, drop the version unless specified)
4. Use `/follow-best-practice` to check the program's official name or alias

### 2. Check Already Installed

> Goal: Avoid reinstalling something already present

1. Run `Get-Command <program>` in PowerShell or `which <program>` on Unix
2. If found → record the path and version (`<program> --version`)
3. Report that it is already installed, with version and path
4. If not yet installed → go to the next step

### 3. Select Package Manager

> Goal: Get the suitable package-manager order

1. Follow `## Merged Details → package-manager` with `<program-name> install`
2. Record the package-manager order received, e.g. `[mise, scoop, winget]`
3. Record the install command template for each package manager
4. If the workflow finds no package manager with the program → jump to the fallback

### 4. Install Through Recommended Package Manager

> Goal: Install the program following the received order

1. For each package manager in the order:
   - Check that the package manager is installed (`Get-Command <manager>`)
   - If missing → use `/download-program <manager>` to install that package manager, or skip to the next one
   - Search for the program in the package manager (see commands below)
   - If found → install with the correct command
   - Verify with `Get-Command <program>` after installing
   - If successful → report the package manager, path, and version
2. If every package manager fails → go to the fallback

#### Install Commands by Manager

- `mise`: `mise search <program>` then `mise use -g <program>`
- `scoop`: `scoop search <program>` then `scoop install <program>`
- `winget`: `winget search <program>` then `winget install --id <package-id> --accept-package-agreements --accept-source-agreements`
- `brew`: `brew search <program>` then `brew install <program>`
- `apt`: `apt-cache search <program>` then `sudo apt install <program>`
- `pacman`: `pacman -Ss <program>` then `sudo pacman -S <program>`
- `yum`/`dnf`: `yum search <program>` then `sudo yum install <program>`

### 5. Fallback to Manual Download

> Goal: Open the download page for the user to install manually when package managers are exhausted

1. Use `/search-files-patterns` or `/search-github-star` to find the program's main download page
2. If a GitHub repo is found → open `https://github.com/<owner>/<repo>/releases`
3. If the official website is found → use `/open-web` to open the download page
4. If nothing is found → search the web with `google` or `duckduckgo` and open the first result
5. Report the opened URL along with the general installation steps
6. Stop and wait for the user to proceed manually

## Rules

### 1. Delegate Package Manager Selection

- Always use `workflows/package-manager` to select the package manager
- Do not hardcode the package-manager order in the skill
- If the OS changes, let the workflow handle it

### 2. OS Awareness

- Supports Windows, macOS, Linux
- Use `Get-Command` on PowerShell, `which` on Unix
- Use package-manager commands for the detected OS

### 3. No Untrusted Sources

- Never install from untrusted sources
- When unsure, open the official website or GitHub release instead of auto-installing
- Never run an install script from a URL without verifying its checksum or signature

### 4. Idempotent

- Check first whether the program is already installed
- If installed, report version and path, then stop
- Never reinstall unnecessarily

### 5. Output

- Report the package manager used to install
- Report version and path after installing
- If the download page was opened, report the URL with general install steps

- Use /use-pwsh-shell if needed
- Use /run-program if needed

- Use /update-all-program-in-computer if needed

## Merged Details

### package-manager

##### Goal

Choose the suitable package manager for installing, listing, or uninstalling programs on the current OS —

##### Scope

- Check the OS and the installed package managers
- Suitability order on Windows: `mise` → `scoop` → `winget`
- Supports macOS: `mise` → `brew` (and `port` if present)
- Supports Linux: `mise` → `apt` → `pacman` → `yum` → `dnf`
- Used by parent and siblings: `download-program`, `list-program-in-computer`, `uninstall-program-in-computer`, `update-all-program-in-computer`

##### Execute

###### 1. Detect OS

> Goal: Determine the current OS

1. On PowerShell: use `[System.Runtime.InteropServices.RuntimeInformation]::OSDescription`
2. If `Microsoft Windows` is found → use Windows package managers
3. If `Darwin` is found → use macOS package managers
4. If `Linux` is found → use Linux package managers
5. Record the OS for choosing the package manager

###### 2. Check Available Package Managers

> Goal: Know which package managers are ready to use

1. Windows: `Get-Command mise/scoop/winget -ErrorAction SilentlyContinue`
2. macOS: `Get-Command mise/brew -ErrorAction SilentlyContinue`
3. Linux: `Get-Command mise/apt/pacman/yum/dnf -ErrorAction SilentlyContinue`
4. Record the list of ready-to-use package managers

###### 3. Determine Best Package Manager For Action

> Goal: Select the package manager per action

1. `install`: dev tool / versioned tool → try `mise` first, then follow the OS order (Windows: `scoop` → `winget`, macOS: `brew`, Linux: native)
2. `list`: query every available package manager and merge the results
3. `uninstall`: first find the package manager that installed this program, via `list-program-in-computer` or each manager's `list` — if not found → notify the user

###### 4. Search Program In Package Manager

> Goal: Confirm the package manager has the program

1. `mise`: `mise search <program>` or `mise list-all <program>`
2. `scoop`: `scoop search <program>`
3. `winget`: `winget search <program>`
4. `brew`: `brew search <program>`
5. `apt`: `apt-cache search <program>`; `pacman`: `pacman -Ss <program>`; `yum`/`dnf`: `yum search <program>`
6. If the first package manager does not have it → try the next one in order

###### 5. Return Recommendation

> Goal: Deliver a clear recommendation

1. State the package manager to use + the command for the action (install/list/uninstall)
2. If no package manager has the program → recommend the `download-program` fallback or `/open-web`

##### Rules

###### 1. OS-Specific Order

- Windows: `mise` → `scoop` → `winget`; macOS: `mise` → `brew`; Linux: `mise` → native
- Never set an order that does not fit the OS

###### 2. No Hidden Install Of Package Manager

- If a package manager is not yet installed → notify the user or install it via `download-program`
- Never install a package manager unannounced

###### 3. Action-Aware

- `install`: prefer managers with good version handling; `list`: query all of them; `uninstall`: find the real source before removing

###### 4. Idempotent

- If the program is already installed, let `download-program` or `uninstall-program-in-computer` check first — no duplicate installs/removals

###### 5. Output

- Show the OS, chosen package manager, command, and a brief rationale + fallback if nothing is found

- Use /use-pwsh-shell if needed
- Use /run-install if needed

##### Expected Outcome

- Get the package manager suited to the OS and action, with the correct command
- Never install a package manager or program without permission

## Expected Outcome

- The program is installed through the suitable package manager when found
- If installation fails, the main download page is opened for the user to install manually
- No duplicate installation when the program is already present
- A complete report of the method used, version, path, or URL opened
