---
name: vscode-nginx-filetype-config
description: Configure VSCode at multiple tiers (application, profile, workspace, code-workspace) to recognize nginx directory files as NGINX language type with syntax highlighting.
category: VSCode-Configuration
---

# VSCode NGINX File Type Configuration Skill (v3 - Multi-Tier with Code-Workspace)

This skill enables proper syntax highlighting and language-aware editing for NGINX configuration files in VSCode by configuring file type associations across all VSCode configuration tiers.

***

## 1. Overview

NGINX configuration files often lack standard extensions (e.g., `nginx.conf`, `fastcgi.conf`, `proxy_params`, `mime.types`). By default, VSCode cannot automatically identify these as NGINX files, resulting in lack of syntax highlighting and code intelligence.

This skill configures VSCode to recognize all files within a project's `nginx/` directory as NGINX language type across four configuration tiers:

- **Application Settings** (User-wide, macOS: `~/Library/Application Support/Code/User/settings.json`)
- **Profile Settings** (Profile-specific overrides, if profiles are enabled)
- **Workspace Settings** (Project-level, `.vscode/settings.json`)
- **Code-Workspace Settings** (Multi-root workspace definition, `*.code-workspace` files)

This multi-tier configuration enables:

- Syntax highlighting for NGINX directives
- Code completion (if NGINX extensions are installed)
- Proper indentation and formatting
- Language-aware navigation
- Portable, team-shareable workspace configuration

***

## 2. VSCode Configuration Hierarchy

VSCode settings follow a priority hierarchy (highest to lowest):

1. **Code-Workspace Settings** (`*.code-workspace` files) — Multi-root workspace overrides, **highest priority**
2. **Workspace Settings** (`.vscode/settings.json`) — Project-specific, committed to repository
3. **Profile Settings** (`profiles/<profile-name>/settings.json`) — Profile-specific overrides
4. **Application Settings** (User settings directory, OS-specific) — User-wide defaults, **lowest priority**

**Recommendation**: Define the NGINX association at the **Application** level for consistency across all projects, then override in **Workspace** or **Code-Workspace** for project-specific tuning.

***

## 3. Environment & Dependencies

### 3.1 Pre-requisites

- **VSCode**: Version 1.60+ (supports `.vscode/settings.json`)
- **VSCode User Directory**: Must be accessible (OS-specific paths)
  - **macOS**: `~/Library/Application Support/Code/User/`
  - **Linux**: `~/.config/Code/User/`
  - **Windows**: `%APPDATA%\Code\User\`
- **NGINX Extension (Optional)**: For enhanced features, install one of:
  - [NGINX IntelliSense](https://marketplace.visualstudio.com/items?itemName=hangxingliu.vscode-nginx-conf)
  - [NGINX Configuration](https://marketplace.visualstudio.com/items?itemName=ahmadalli.vscode-nginx-conf)

### 3.2 Verification

```bash
# Verify VSCode is installed and accessible
which code

# Confirm VSCode version is 1.60+
code --version

# Verify application settings directory exists (macOS)
ls ~/Library/Application\ Support/Code/User/

# Or for Linux
ls ~/.config/Code/User/

# Or for Windows
ls "%APPDATA%/Code/User/"
```

If any command fails, the user MUST install or configure VSCode in their environment.

***

## 4. Configuration Locations by Tier

### 4.1 Application Settings (User-wide)

**macOS**:
```
~/Library/Application Support/Code/User/settings.json
```

**Linux**:
```
~/.config/Code/User/settings.json
```

**Windows**:
```
%APPDATA%\Code\User\settings.json
```

**Purpose**: Global NGINX file association. Applied to ALL VSCode instances on this machine. Useful for establishing a user-wide standard.

### 4.2 Profile Settings (Profile-specific)

Located in:
- **macOS**: `~/Library/Application Support/Code/User/profiles/<profile-name>/settings.json`
- **Linux**: `~/.config/Code/User/profiles/<profile-name>/settings.json`
- **Windows**: `%APPDATA%\Code\User\profiles\<profile-name>\settings.json`

**Purpose**: Profile-specific overrides. Only applied when the profile is active. Allows different projects/teams to have distinct configurations.

**Note**: Profiles must be enabled in VSCode settings first.

### 4.3 Workspace Settings (Project-specific)

Located in:
```
<repository-root>/.vscode/settings.json
```

**Purpose**: Project-level configuration. Committed to the repository for team-wide benefit. Overrides both Application and Profile settings.

***

## 5. File Type Association Rule

The core configuration uses VSCode's `files.associations` setting with glob patterns:

```json
{
  "files.associations": {
    "nginx/**": "nginx"
  }
}
```

**Explanation**:
- **Key**: `"nginx/**"` — Glob pattern matching all files in the `nginx/` directory and subdirectories
- **Value**: `"nginx"` — VSCode's built-in language identifier for NGINX configuration

### 5.1 Supported File Patterns

This configuration automatically covers all files within `nginx/`:

- `nginx.conf` — Main NGINX configuration
- `fastcgi.conf` — FastCGI parameters
- `fastcgi_params` — Additional FastCGI parameters
- `proxy_params` — Proxy directive templates
- `scgi_params` — SCGI gateway parameters
- `uwsgi_params` — uWSGI gateway parameters
- `mime.types` — MIME type definitions
- `koi-utf`, `koi-win`, `win-utf` — Character encoding definitions
- `sites-available/*` — Site configurations (subdirectories)
- `sites-enabled/*` — Enabled site symlinks (subdirectories)
- `snippets/*` — Reusable NGINX snippets (subdirectories)
- Any additional files added to the `nginx/` directory

***

## 4.4 Code-Workspace Settings (Multi-root workspace)

Located in:
```
<repository-root>/*.code-workspace
```

**Example**: `myproject.code-workspace`

**Purpose**: Multi-root workspace configuration. These files define workspace structure and settings that override `.vscode/settings.json`. Used when a workspace spans multiple root folders or when settings are managed via workspace file instead of `.vscode/` directory.

**Structure** (JSON file with `settings` key):
```json
{
  "folders": [
    {
      "path": ".",
      "name": "Project Root"
    },
    {
      "path": "nginx",
      "name": "NGINX Config"
    }
  ],
  "settings": {
    "files.associations": {
      "nginx/**": "nginx"
    }
  }
}
```

**Priority Note**: Settings in `.code-workspace` **override** `.vscode/settings.json`. If using `.code-workspace` files, that's where the NGINX association should be configured.

***

## 6. Implementation Protocol

### 6.1 Tier 1: Application Settings (User-wide)

**Purpose**: Configure NGINX file type recognition globally for all VSCode projects.

**Steps**:

1. **Locate User Settings Directory**:
   ```bash
   # macOS
   CODE_USER_DIR=~/Library/Application\ Support/Code/User
   
   # Linux
   CODE_USER_DIR=~/.config/Code/User
   
   # Windows (PowerShell)
   $CODE_USER_DIR = "$env:APPDATA\Code\User"
   ```

2. **Create or Merge `settings.json`**:
   ```bash
   # If directory doesn't exist, create it
   mkdir -p "$CODE_USER_DIR"
   
   # If settings.json doesn't exist, create with minimal config
   if [ ! -f "$CODE_USER_DIR/settings.json" ]; then
     echo '{}' > "$CODE_USER_DIR/settings.json"
   fi
   ```

3. **Merge NGINX Association**:
   - Read the existing `settings.json` as JSON
   - Merge the `files.associations` entry without overwriting existing entries:
     ```json
     {
       "files.associations": {
         "nginx/**": "nginx"
       }
     }
     ```
   - Write the merged JSON back with proper formatting

4. **Restart VSCode**:
   Close and reopen VSCode to apply application-level settings.

### 6.2 Tier 2: Profile Settings (Profile-specific)

**Purpose**: Configure NGINX file type for a specific VSCode profile.

**Prerequisites**: The profile must exist in VSCode. Create via `Cmd+Shift+P` → "Profiles: Create Profile".

**Steps**:

1. **Locate Profile Directory**:
   ```bash
   # macOS
   PROFILE_DIR=~/Library/Application\ Support/Code/User/profiles/<profile-name>
   
   # Linux
   PROFILE_DIR=~/.config/Code/User/profiles/<profile-name>
   
   # Windows
   $PROFILE_DIR = "$env:APPDATA\Code\User\profiles\<profile-name>"
   ```

2. **Create or Merge Profile `settings.json`**:
   ```bash
   mkdir -p "$PROFILE_DIR"
   
   if [ ! -f "$PROFILE_DIR/settings.json" ]; then
     echo '{}' > "$PROFILE_DIR/settings.json"
   fi
   ```

3. **Merge NGINX Association** (same logic as Tier 1):
   - Read existing profile settings
   - Merge NGINX association without overwrites
   - Write back with proper formatting

4. **Activate Profile and Restart**:
   - Switch to the profile in VSCode
   - Reload VSCode to apply settings

### 6.3 Tier 3: Workspace Settings (Project-specific)

**Purpose**: Configure NGINX file type for a specific project repository.

**Steps**:

1. **Create `.vscode/` Directory**:
   ```bash
   mkdir -p .vscode
   ```

2. **Create or Merge Workspace `settings.json`**:
   ```bash
   if [ ! -f .vscode/settings.json ]; then
     echo '{}' > .vscode/settings.json
   fi
   ```

3. **Merge NGINX Association** (same atomic merge logic):
   - Read existing workspace settings
   - Merge NGINX association without overwrites
   - Write back with proper formatting

4. **Commit to Repository**:
   ```bash
   git add .vscode/settings.json
   git commit -m "feat: configure NGINX file type for workspace

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   ```

5. **Reload VSCode**:
   - Workspace settings take effect immediately upon reload
   - All team members with the workspace will inherit the configuration

### 6.4 Tier 4: Code-Workspace Settings (Multi-root workspace)

**Purpose**: Configure NGINX file type in a multi-root workspace file.

**When to Use**: When the project uses `.code-workspace` files to define multi-root workspaces or manage settings centrally via workspace file instead of `.vscode/` directory.

**Important**: Settings in `.code-workspace` files **override** `.vscode/settings.json`. If the repository uses `.code-workspace`, configure there.

**Steps**:

1. **Locate or Create `.code-workspace` File**:
   ```bash
   # List existing workspace files
   find . -maxdepth 1 -name "*.code-workspace"
   
   # If none exist, create one (example: myproject.code-workspace)
   cat > myproject.code-workspace << 'EOF'
   {
     "folders": [
       {
         "path": ".",
         "name": "Project Root"
       }
     ],
     "settings": {
       "files.associations": {
         "nginx/**": "nginx"
       }
     }
   }
   EOF
   ```

2. **If `.code-workspace` Already Exists**:
   - Read the file as JSON
   - Ensure `settings` key exists
   - Ensure `files.associations` exists in `settings`
   - Merge NGINX association without overwriting existing entries
   - Write back with proper formatting

3. **Merge NGINX Association** (atomic logic):
   ```json
   {
     "folders": [...],
     "settings": {
       "files.associations": {
         "nginx/**": "nginx"
       },
       "other-settings": "..."
     }
   }
   ```

4. **Commit to Repository**:
   ```bash
   git add *.code-workspace
   git commit -m "feat: configure NGINX file type in workspace file

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   ```

5. **Open Workspace**:
   - In VSCode: `File → Open Workspace from File`
   - Select the `.code-workspace` file
   - Reload if needed

***

## 7. Preservation & Merge Rules

### 7.1 Atomic Merge Logic

When merging into existing settings at any tier:

1. **Read** the existing file as JSON
2. **Check** if `files.associations` key exists:
   - If **exists**: Merge the new `"nginx/**": "nginx"` entry without overwriting other file associations
   - If **missing**: Create the `files.associations` object with the NGINX entry
3. **Write** the merged JSON back to the file with proper formatting (2-space indentation)
4. **Verify** the output is valid JSON

### 7.2 Conflict Resolution

- **Do NOT** remove or overwrite existing file associations for other languages
- **Do NOT** modify other settings in the file (e.g., `editor.fontSize`, `python.linting`)
- **Do NOT** remove or modify `folders` array in `.code-workspace` files
- **Idempotency**: Running this skill multiple times MUST produce the same result (no duplicate entries)
- **Hierarchy Respect**: Code-Workspace > Workspace > Profile > Application

### 7.3 Backups (Optional but Recommended)

Before modifying any settings file:

```bash
# Create backup
cp settings.json settings.json.bak

# After successful merge, optionally clean up
rm settings.json.bak
```

***

## 8. Verification Protocol

### 8.1 Configuration Validation

```bash
# For application settings (macOS example)
jq '.files.associations."nginx/**"' ~/Library/Application\ Support/Code/User/settings.json

# For profile settings (macOS example)
jq '.files.associations."nginx/**"' ~/Library/Application\ Support/Code/User/profiles/<profile-name>/settings.json

# For workspace settings
jq '.files.associations."nginx/**"' .vscode/settings.json

# For code-workspace settings
jq '.settings.files.associations."nginx/**"' myproject.code-workspace
```

Expected output at any tier: `"nginx"`

### 8.2 VSCode Functional Check

1. Open VSCode and load the workspace
2. Open any file from the `nginx/` directory (e.g., `nginx/nginx.conf`)
3. Verify the **Language Mode** indicator (bottom-right) displays `nginx`
4. Confirm syntax highlighting is applied to NGINX keywords (e.g., `server`, `location`, `proxy_pass` should be styled)

### 8.3 Hierarchy Verification

To verify that settings are correctly prioritized:

1. **Define the same setting at multiple tiers with different values** (for testing only)
2. **Open an NGINX file** and confirm the workspace setting takes precedence
3. **Disable workspace setting** and verify profile setting activates
4. **Disable profile setting** and verify application setting activates

### 8.4 Extension Integration (Optional)

If an NGINX extension is installed:

- Open an NGINX file and verify hover tooltips appear on directives
- Verify code completion works (type `proxy_` and observe completions)
- Check that problem diagnostics are reported for invalid syntax

***

## 9. Automation & Scripts

A Python utility is available to automate the merge process across all tiers without manual JSON editing:

**Location**: `./scripts/vscode-nginx-config.py`

### 9.1 Usage

```bash
# Configure workspace settings (default)
python3 ./scripts/vscode-nginx-config.py --workspace-root /path/to/project

# Configure application settings (user-wide)
python3 ./scripts/vscode-nginx-config.py --tier application

# Configure profile settings
python3 ./scripts/vscode-nginx-config.py --tier profile --profile-name my-profile

# Configure code-workspace file
python3 ./scripts/vscode-nginx-config.py --tier code-workspace --workspace-file myproject.code-workspace

# Preview changes without modifying
python3 ./scripts/vscode-nginx-config.py --tier workspace --dry-run
```

### 9.2 Flags

- `--tier {application|profile|workspace|code-workspace}`: Which tier to configure (default: workspace)
- `--workspace-root PATH`: Repository root (default: current directory)
- `--profile-name NAME`: Profile name for profile tier (required if `--tier profile`)
- `--workspace-file PATH`: Path to `.code-workspace` file (required if `--tier code-workspace`)
- `--dry-run`: Preview changes without modifying files

### 9.3 What the Script Does

1. **Discovers** the appropriate settings directory (based on tier and OS)
2. **Creates** directories if needed
3. **Reads** existing settings (creates empty JSON if missing)
4. **Merges** the NGINX file association atomically (preserves existing entries)
5. **Validates** the output JSON syntax
6. **Reports** success or failure with atomic backups

***

## 10. Related Conversations & Traceability

This skill was developed to address NGINX file type configuration in:
- **Repository**: `/Users/dk/lab-data/oleovista-acers`
- **Use Case**: Enabling VSCode syntax highlighting for all NGINX configuration files across all configuration tiers
- **Scope**: Multi-tier, portable VSCode configuration with support for standard folders, profiles, and multi-root workspaces

***

## 11. Notes & Considerations

### 11.1 Multi-Repository Portability

This skill is designed to be **project-portable**:

- **Workspace & Code-Workspace**: Should be committed to the repository so all developers benefit from NGINX file type configuration
- **Application & Profile**: User-specific configurations, not shared across repositories

### 11.2 VSCode Extension Recommendations

While NGINX syntax highlighting is available without extensions, installing an NGINX extension provides:
- **IntelliSense**: Code completion for directives and variables
- **Diagnostics**: Real-time validation of NGINX syntax
- **Hover Documentation**: Quick reference for directive parameters

Recommended extension: [NGINX IntelliSense](https://marketplace.visualstudio.com/items?itemName=hangxingliu.vscode-nginx-conf)

### 11.3 Configuration Precedence

When multiple tiers define the same setting (highest to lowest):

1. **Code-Workspace** (highest) — Multi-root workspace overrides all
2. **Workspace** — Project-specific `.vscode/settings.json`
3. **Profile** — Active profile overrides application
4. **Application** (lowest) — User-wide defaults

This allows for flexible, layered configuration strategies. Settings at higher tiers always win.

### 11.4 When to Use Each Tier

| Tier | Use Case | Example |
|------|----------|---------|
| **Application** | All your VSCode projects | Developer wants NGINX syntax across all work |
| **Profile** | Specific workflow | "DevOps" profile with all infra-specific settings |
| **Workspace** | Team projects | Repository-level config shared with team |
| **Code-Workspace** | Multi-root workspace | Project with multiple independent folders |

### 11.5 Edge Cases

- **Subdirectories**: The glob pattern `nginx/**` matches all levels (e.g., `nginx/sites-available/example.com`)
- **Files Without Extensions**: NGINX config files without extensions (e.g., `proxy_params`) are correctly matched
- **Character Encoding Files**: Files like `koi-utf` and `win-utf` are included by the glob pattern
- **Multiple Profiles**: Configuration is independent per profile; no conflicts between profiles
- **Settings Sync**: If VSCode Settings Sync is enabled, application settings are synchronized; workspace/profile/code-workspace settings remain local
- **Multi-root Workspaces**: Code-workspace settings apply to all folders in the workspace
- **Workspace File Location**: `.code-workspace` file can reside anywhere; typical locations are repository root or parent directories

***

## 12. Failure Recovery

If NGINX file type is not recognized after configuration:

1. **Verify Configuration Was Applied**:
   ```bash
   # Check all three tiers for the setting
   jq '.files.associations."nginx/**"' ~/Library/Application\ Support/Code/User/settings.json
   jq '.files.associations."nginx/**"' ~/Library/Application\ Support/Code/User/profiles/<profile>/settings.json
   jq '.files.associations."nginx/**"' .vscode/settings.json
   ```

2. **Reload VSCode**:
   ```
   Cmd+Shift+P → "Developer: Reload Window"
   ```

3. **Clear VSCode Cache** (if reload doesn't work):
   ```bash
   # macOS
   rm -rf ~/Library/Application\ Support/Code/
   
   # Linux
   rm -rf ~/.config/Code/
   
   # Windows
   rmdir /S "%APPDATA%\Code\"
   ```

4. **Manually Set Language Mode**:
   - Open an NGINX file
   - Click the language mode in the bottom-right status bar
   - Select `nginx` from the dropdown
   - Right-click and select "Configure File Association for .conf" (or applicable extension)

5. **Verify Extension Integration**:
   - If an NGINX extension is installed, verify it's enabled
   - Check for conflicting extensions that might override the language mode

