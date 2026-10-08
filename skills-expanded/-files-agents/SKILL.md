# Agent Guidelines for Dotfiles Repository

## Repository Structure

### Core Directories

- `_scripts/` - Installation and automation scripts
  - `_scripts/unix/` - Unix-like systems (Linux/macOS)
    - `unix/installers/` - Tool installation scripts (install-mise.sh, install-zsh.sh, etc.)
    - `unix/tools/` - Utility scripts (deploy-gitconfig.sh, manage-stow.sh, backup.sh)
    - `unix/checkers/` - Validation scripts (check-dotnet.sh)
    - `unix/lib/` - Shared shell libraries (colors.sh, common.sh, detect.sh, package-managers.sh)
  - `_scripts/windows/` - Windows-specific scripts (PowerShell 7+)
    - `windows/installers/` - Tool installation scripts (Install-Packages.ps1, Install-LazyVim.ps1, etc.)
    - `windows/tools/` - Utility scripts (Invoke-Stow.ps1, Test-StowLocalAppData.ps1)
    - `windows/managers/` - Package manager installers (Install-Choco.ps1, Install-WinGet.ps1, Install-PowerShell.ps1)
    - `windows/lib/` - Shared PowerShell libraries (colors.ps1, common.ps1, detect.ps1, package-managers.ps1)
  - `_scripts/omarchy/` - Omarchy Linux (Arch-based) specialized scripts
    - Injection-based configuration management (non-destructive)
    - Modular architecture (preflight/packages/config/themes/post-install)
  - `_scripts/just/` - Just command runner bootstrap
  - `_scripts/configs/` - Configuration files (YAML)
    - `configs/windows/packages/` - Windows package configs (pro/perso)
    - `configs/unix/packages/` - Unix package configs
- `_docs/` - MkDocs documentation site (public-facing)
- `_specs/` - Technical specifications and development guides (internal)
  - `_specs/just-integration/` - Just integration specs
  - `_specs/guides/` - User and developer guides
  - `_specs/old/` - Archived specifications
- `.just/` - Just recipe modules (modular justfile organization)
- Configuration directories: `nvim/`, `git/`, `zsh/`, `nushell/`, `wezterm/`, etc.

### Important Files

- `justfile` - Main entry point for Just command runner
- `mkdocs.yml` - MkDocs configuration (points to `_docs/`)
- `pyproject.toml` - Python/UV project configuration for MkDocs
- `.gitconfig.template` - Git config template with `#{TOKEN}#` placeholders
- `AGENTS.md` - This file (agent guidelines)

## Build/Test Commands

### Just Command Runner

- **Primary interface**: Use `just` commands for all automation
- Common commands:
  - `just install_full` - Full installation with all tools
  - `just install_minimal` - Minimal installation (core tools only)
  - `just stow` - Symlink dotfiles with GNU Stow
  - `just update` - Update all tools and configs
  - `just doctor` - Run health checks
  - `just verify` - Verify installation
  - `just deploy_gitconfig` - Deploy git config with token replacement
- See `just --list` for all available commands

### Testing

#### Container Testing (Recommended)

**IMPORTANT**: Always test installation scripts in containers, never on the host system.

**Use existing Ubuntu container:**

```bash
# Connect to the running Ubuntu container
docker exec -it a4597fd2-8f64-4bf8-87d1-be16e727de6b bash

# Inside container, clone and test
cd /tmp
git clone /path/to/.files .dotfiles
cd .dotfiles
bash _scripts/install.sh --minimal
```

**Or create a new Ubuntu container:**

```bash
# Create fresh Ubuntu 24.04 container
docker run -it --name dotfiles-test ubuntu:24.04 bash

# Inside container, install git first
apt update && apt install -y git

# Clone and test
cd /tmp
git clone <repo-url> .dotfiles
cd .dotfiles
bash _scripts/install.sh --minimal
```

**Clean up after testing:**

```bash
# Exit container
exit

# Remove test container
docker rm dotfiles-test
```

#### Other Testing

- No traditional build system - this is a dotfiles configuration repository
- Use `pre-commit run --all-files` to run pre-commit hooks (trailing whitespace, secrets detection, YAML validation)
- Test configurations by symlinking and verifying tool functionality
- For Neovim: `nvim --headless -c "checkhealth" -c "qa"` to validate configuration

### Documentation

- `uv venv` - Create virtual environment for MkDocs
- `uv sync` - Install MkDocs dependencies
- `source .venv/bin/activate && mkdocs serve` - Start local docs server
- `mkdocs build` - Build static documentation site

## Code Style Guidelines

### Shell Scripts (Bash/Zsh)

- Use `#!/usr/bin/env sh` for portability or `#!/usr/bin/env bash` when bash-specific features needed
- Follow POSIX shell conventions where possible
- Use lowercase variables with underscores: `monitor_data`, `focused_name`
- Quote variables to prevent word splitting: `"$variable"`
- Use `jq` for JSON parsing in scripts

### Configuration Files

- Use 2-space indentation for YAML files
- Use 4-space indentation for shell scripts
- Follow existing naming conventions: kebab-case for config files, snake_case for variables
- Comment configuration sections clearly with `# =====` style headers
- Group related configurations together (e.g., git aliases, kubernetes aliases)

### Markdown Files

**IMPORTANT**: This repository uses `markdownlint` via pre-commit hooks. All markdown files must pass linting before commit.

**Common markdownlint rules to follow:**

- **MD022**: Add blank lines before and after headings

  ````markdown
  Some text here.

  ## Heading

  More text here.
  ````

- **MD031**: Add blank lines before and after fenced code blocks

  ````markdown
  Some text here.

  ```bash
  code here
  ```

  More text here.
  ````

- **MD032**: Add blank lines before and after lists

  ````markdown
  Some text here.

  - List item 1
  - List item 2

  More text here.
  ````

- **MD040**: Specify language for all fenced code blocks

  ````markdown
  # ✅ Good
  ```bash
  echo "hello"
  ```

  ```text
  Plain text output
  ```

  # ❌ Bad
  ```
  no language specified
  ```
  ````

- **MD034**: Wrap bare URLs in angle brackets

  ````markdown
  # ✅ Good
  Visit <https://example.com> for details

  # ❌ Bad
  Visit https://example.com for details
  ````

**When creating new markdown files:**

1. Always specify language for code blocks (use `text` for non-code content like output or plain text)
2. Add blank lines around all headings, lists, and code blocks
3. Wrap standalone URLs in `<>` angle brackets
4. Avoid inline HTML unless absolutely necessary

**Testing markdown files:**

```bash
# Run markdownlint on all markdown files
pre-commit run markdownlint --all-files

# Run all pre-commit hooks
pre-commit run --all-files
```

### Aliases and Functions

- Prefix tool replacements clearly: `alias ls='eza --icons'`
- Use single letters for frequently used commands: `alias g='git'`, `alias k='kubecolor'`
- Keep muscle memory typos as aliases: `alias kubeclt='kubecolor'`
- Group aliases by functionality with clear section headers

### Error Handling

- Use conditional checks for OS-specific configurations: `if [[ "$OSTYPE" == "darwin"* ]]`
- Validate tool availability before creating aliases
- Provide fallbacks for missing dependencies where appropriate

## PowerShell Scripts

### Target Version

- **IMPORTANT**: All PowerShell scripts target **PowerShell 7+** (not Windows PowerShell 5.1)
- Use `#Requires -Version 7.0` at the top of scripts when using PS7-specific features
- PowerShell 7 is cross-platform (Windows, Linux, macOS)

### Code Style

- Use 4-space indentation
- Use PascalCase for function names: `Get-SystemInfo`, `Install-Package`
- Use camelCase for variables: `$packageName`, `$targetDir`
- Use approved verbs for functions: `Get-`, `Set-`, `New-`, `Remove-`, `Install-`, `Test-`
- Add proper comment-based help (`.SYNOPSIS`, `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE`)

### Helper Functions - CRITICAL RULES

**NEVER use empty strings with Write-Info, Write-Success, Write-Warning, or Write-Error:**

```powershell
# ❌ WRONG - Will cause parameter binding error
Write-Info ""
Write-Success ""
Write-Warning ""

# ✅ CORRECT - Use Write-Host for blank lines
Write-Host ""
```

**Why**: Our custom helper functions in `_scripts/lib/pwsh/colors.ps1` require non-empty message parameters. PowerShell 7 strictly enforces this.

**Helper Functions Available**:

- `Write-Header $message` - Section headers with color
- `Write-Info $message` - Informational messages
- `Write-Success $message` - Success messages
- `Write-Warning $message` - Warning messages (alias: `Write-Warn`)
- `Write-Error $message` - Error messages (alias: `Write-ErrorMsg`)
- `Write-Step $message` - Step indicators

**For blank lines**: Always use `Write-Host ""`

### File Encoding

- Use UTF-8 with BOM for scripts that need to run in Windows PowerShell 5.1
- Use UTF-8 without BOM for PowerShell 7+ only scripts
- Ensure YAML config files use UTF-8 without BOM

### Error Handling

```powershell
# Set strict error handling
$ErrorActionPreference = 'Stop'

# Use try/catch for error handling
try {
    # Code that might fail
}
catch {
    Write-Error "Failed: $_"
    exit 1
}
```

### Path Handling

```powershell
# Use Join-Path instead of string concatenation
$configPath = Join-Path $env:LOCALAPPDATA "nvim"

# Use Test-Path before accessing files
if (Test-Path $configPath) {
    # Safe to use
}

# Use Split-Path for path manipulation
$parentDir = Split-Path $filePath -Parent
$fileName = Split-Path $filePath -Leaf
```

### Cross-Platform Considerations

```powershell
# Detect Windows vs Linux/macOS
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    # Windows-specific code
}
elseif ($IsLinux) {
    # Linux-specific code
}
elseif ($IsMacOS) {
    # macOS-specific code
}
```

## Platform Detection

### Detection Strategy

**Entry Points**: Detect Windows vs Unix at the main script level

- **Windows**: `install.ps1` (PowerShell 7+)
- **Unix**: `install.sh` (Bash/Zsh) - handles both Linux and macOS

**Unix Scripts**: Detect specific OS internally when needed

### Unix Shell Detection

```bash
# Source Unix libraries for detection functions
source "$DOTFILES_ROOT/_scripts/unix/lib/init.sh"

# Detect OS type
OS=$(detect_os)  # Returns: macos, linux, or unknown
if [[ "$OS" == "macos" ]]; then
    # macOS-specific code (e.g., Homebrew)
elif [[ "$OS" == "linux" ]]; then
    DISTRO=$(get_distro)  # Returns: ubuntu, debian, fedora, arch, etc.
    case "$DISTRO" in
        ubuntu|debian)
            # Debian-based: use apt
            ;;
        fedora|rhel)
            # RedHat-based: use dnf/yum
            ;;
        arch)
            # Arch-based: use pacman
            ;;
    esac
fi

# Package manager abstraction
PM=$(get_package_manager)  # Returns: brew, apt, dnf, yum, pacman, etc.
install_package git  # Automatically uses correct PM
```

### Windows Detection

PowerShell built-in variables and library functions:

```powershell
# Built-in variables (PowerShell 7+)
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    # Windows code
}

# Library functions (source from _scripts/windows/lib/detect.ps1)
$winVersion = Get-WindowsVersion
if (Test-IsWindows11) {
    # Windows 11-specific code
}

if (Test-IsAdmin) {
    # Admin-required operations
}
```

### Unix Shell Libraries

**Location**: `_scripts/unix/lib/`

#### `init.sh` - Library Loader

```bash
# Source all Unix libraries at once
source "$DOTFILES_ROOT/_scripts/unix/lib/init.sh"
```

#### `colors.sh` - Logging Functions

- `log_info $message` - Informational messages (green)
- `log_success $message` - Success messages (green with checkmark)
- `log_error $message` - Error messages (red)
- `log_warning $message` - Warning messages (yellow)
- `log_header $message` - Section headers (magenta)
- `log_step $message` - Sub-steps (blue)

#### `common.sh` - Utility Functions

- `has_command $cmd` - Check if command exists
- `retry $max_attempts $command` - Retry failed operations
- `backup_file $file [$backup_dir]` - Create timestamped file backup
- `confirm_prompt $message [$default]` - Ask for user confirmation
- `safe_mkdir $path` - Create directories with error checking
- `check_internet [$host]` - Check internet connectivity
- `get_dotfiles_root $levels_up` - Get absolute path to repo root

#### `detect.sh` - OS Detection

- `detect_os` - Get OS type (macos/linux/unknown)
- `get_distro` - Get Linux distribution ID
- `is_macos` - Check if macOS (boolean)
- `is_linux` - Check if Linux (boolean)
- `get_package_manager` - Detect available PM (brew/apt/dnf/yum/pacman)
- `is_root` - Check if running as root
- `get_home_dir` - Get correct user home directory
- `ensure_home_correct` - Fix stale HOME environment variable

#### `package-managers.sh` - Package Manager Abstraction

- `install_package $name [$pm]` - Install using available PM
- `check_package_installed $name [$pm]` - Check if package installed
- `update_packages [$pm]` - Update all packages
- `install_with_brew $name` - Install with Homebrew
- `install_with_apt $name` - Install with apt
- `install_with_dnf $name` - Install with dnf
- `install_with_yum $name` - Install with yum
- `install_with_pacman $name` - Install with pacman

## Nushell Configuration

### Module Structure

- **Modular layout**: Nushell config is organized into modules under `nushell/.config/nushell/`
  - `core/hooks.nu` - Shell hooks
  - `ui/menus.nu`, `ui/theme.nu`, `ui/keybindings.nu` - UI components
  - `aliases/git-aliases.nu` - Git aliases
  - `integrations/external-tools.nu` - Tool initialization (zoxide, starship, direnv)

### Important Constraints

- **No `&&` operator**: Nushell doesn't support `&&` - use `;` to chain commands
- **No variable string interpolation in `source`**: Cannot use `source $"..."` with variables
  - For Windows paths, use bare literals with tokens: `source C:/Users/#{USERNAME}#/.cache/...`
  - Tokens get replaced at deploy time by `replacetokens` CLI
- **Module exports**: Export functions with unique names to avoid collisions (e.g., `export def get_menus []` instead of `export def menus []`)
- **Direnv integration**: Implemented via `env_change.PWD` hook per official nushell cookbook

## Token Replacement System

### Overview

Template files use `#{TOKEN}#` syntax that gets replaced at deploy time with actual values.

### Common Tokens

- `#{USER_FULLNAME}#` - User's full name for git config
- `#{USER_EMAIL}#` - User's email for git config
- `#{USERNAME}#` - System username (for Windows paths)

### Usage in Files

**Git config template** (`git/.gitconfig.template`):

```gitconfig
[user]
    name = #{USER_FULLNAME}#
    email = #{USER_EMAIL}#
```

**Nushell external tools** (`nushell/.config/nushell/integrations/external-tools.nu`):

```nu
# Windows branch - use bare literal paths with tokens
source C:/Users/#{USERNAME}#/.cache/starship/init.nu
```

### Token Replacement Tool

- **CLI**: `replacetokens` (installed via npm)
- **Pattern**: `#{TOKEN}#` (default pattern)
- **Configuration**: In `Taskfile.yml` under `replacetokens` task
  - Sources: `nushell/.config/nushell/**/*.nu`
  - Environment variables provided via `env:` section

## Installation Scripts - Critical Patterns

### HOME Environment Variable Sanitization

**Problem**: When using `su` without `-`, `$HOME` can point to the wrong directory (e.g., `/home/ubuntu/` instead of `/home/yaya1/`)

**Solution**: Add this at the top of all entry-point scripts:

```bash
# Correct HOME if it's stale (happens with 'su' without '-')
REAL_HOME=$(getent passwd "$(whoami)" | cut -d: -f6)
if [[ "$HOME" != "$REAL_HOME" ]]; then
    export HOME="$REAL_HOME"
fi
```

**Applied to**:

- `_scripts/install.sh`
- `_scripts/just/bootstrap.sh`
- `_scripts/unix/tools/deploy-gitconfig.sh`

### Path Resolution in Scripts

Scripts must resolve `DOTFILES_ROOT` relative to their location:

```bash
# Example: Script is 3 levels deep (_scripts/unix/tools/script.sh)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOTFILES_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
```

**Count carefully**:

- `_scripts/install.sh` → 1 level deep → `..`
- `_scripts/just/bootstrap.sh` → 2 levels deep → `../..`
- `_scripts/unix/installers/*.sh` → 3 levels deep → `../../..`
- `_scripts/unix/tools/*.sh` → 3 levels deep → `../../..`
- `_scripts/windows/installers/*.ps1` → 3 levels deep → `../../..`
- `_scripts/windows/tools/*.ps1` → 3 levels deep → `../../..`

### File Existence Checks

**Use `-f` instead of `-x` for script checks**:

```bash
# ❌ WRONG - git clone doesn't preserve execute permissions
if [[ -x "$script_path" ]]; then
    "$script_path"
fi

# ✅ CORRECT - check if file exists, then invoke with bash
if [[ -f "$script_path" ]]; then
    bash "$script_path"
fi
```

### Mise Environment Variables

**Correct variables** (as of mise v2024+):

```bash
export MISE_DATA_DIR="$HOME/.local/share/mise"
export MISE_CACHE_DIR="$HOME/.cache/mise"
```

**Incorrect** (old):

```bash
# ❌ Don't use MISE_HOME - deprecated
export MISE_HOME="$HOME/.local/share/mise"
```

**Apply in**:

- `_scripts/install.sh` (3 places: `install_mise`, `install_package`, `install_mise_tools`)
- `_scripts/unix/installers/install-mise.sh` (in shell config blocks)

### Bootstrap Order

**Linux** (`_scripts/just/bootstrap.sh`):

1. `apt` (system package manager)
2. `script` (runs install.sh)

**macOS**:

1. `brew` (Homebrew)
2. `script` (runs install.sh)

**Removed from default**:

- `mise` - not a default package manager
- `cargo` - not a default package manager

### Git Config Deployment

**Script**: `_scripts/unix/tools/deploy-gitconfig.sh`

**Behavior**:

1. Reads `git/.gitconfig.template`
2. Prompts for `USER_FULLNAME` and `USER_EMAIL` (or uses env vars)
3. Uses existing values from `~/.gitconfig` as defaults if file exists
4. Replaces tokens with actual values
5. **Copies** (not symlinks) result to `~/.gitconfig`

**Invocation**:

- Automatic: During `just install_full` (via `_scripts/install.sh`)
- Manual: `just deploy_gitconfig`

## Just Command Runner Integration

### Color Variables

Use Unicode escape sequences in Just recipes (requires Just 1.14.0+):

```just
# ✅ CORRECT (Just 1.14.0+, October 2023)
reset := "\u{1b}[0m"
bold := "\u{1b}[1m"
red := "\u{1b}[31m"

# ❌ WRONG - Invalid in Just
reset := "\033[0m"
```

**Installation Note**: The `_scripts/just/install-just.sh` script downloads the **latest binary** from GitHub releases to ensure modern Just features work. On Linux, it prefers the binary over apt (which may have outdated versions like 1.21.0).

**Installation order**:

- **macOS**: brew → binary → script
- **Linux**: binary → apt → script

### Recipe Organization

- **Main recipes**: Shown in default `just` command (defined in `justfile`)
- **All recipes**: Available via `just --list`
- **Module structure**: Recipes organized in `.just/*.just` files
  - `.just/_helpers.just` - Shared variables and helper recipes
  - `.just/install.just` - Installation recipes
  - `.just/windows.just` - Windows-specific recipes
  - `.just/tools.just` - Tool management recipes

### Script Invocation

```just
# Use bash to invoke scripts (adds HOME guard automatically)
install_full:
    bash {{scripts_dir}}/install.sh --full
```

## Git Configuration

### Template System

**File**: `git/.gitconfig.template`

**Contains**:

- Token placeholders: `#{USER_FULLNAME}#`, `#{USER_EMAIL}#`
- Git aliases and settings
- Conditional includes for OS-specific configs

**Deployment**:

- Tokens replaced with actual values
- Result copied (not symlinked) to `~/.gitconfig`
- This allows git to modify the file without affecting the template

