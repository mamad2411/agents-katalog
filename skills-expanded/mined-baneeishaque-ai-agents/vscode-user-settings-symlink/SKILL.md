---
name: vscode-user-settings-symlink
description: Protocol for relocating VS Code Insiders User folder to a private config repo and creating a direct symlink without intermediate subdirectories.
category: VSCode-Configuration
---

# VS Code User Settings Symlink Protocol

This skill automates the relocation of the VS Code Insiders User settings folder from the macOS Application Support directory to a portable `<private-config-repo>` location, with a direct symlink for seamless IDE functionality.

## 1. Protocol & Logic

### 1.1 Source & Destination Definition

- **Source Symlink Path**: `/Users/dk/Library/Application Support/Code - Insiders/User`
- **Target Destination**: `~/<private-config-repo>/vscode-insiders-configuration/visual-studio-code-user-settings`
- **Symlink Target**: The symlink MUST point DIRECTLY to the destination (no intermediate "User" subfolder)
- **Platform**: macOS (zsh shell)

### 1.2 Relocation Workflow

1. **Source Verification**: Verify the original source folder exists at `~/Library/Application Support/Code - Insiders/User`
2. **Destination Preparation**: Create the destination directory if it does not exist
3. **Content Migration**: If the destination contains a nested `User` subfolder:
   - Move all contents from `destination/User/*` to `destination/`
   - Remove empty `User` subfolder
4. **Symlink Recreation**:
   - Remove the existing symlink at source
   - Create a new symlink pointing directly to the destination (not `/destination/User`)
5. **Verification**: Confirm the symlink resolves correctly

### 1.3 Path Standards

- The destination MUST contain VS Code settings files directly (e.g., `settings.json`, `keybindings.json`, `snippets/`, `extensions/`)
- There MUST NOT be a nested `User` folder inside the destination
- The symlink MUST point to the destination folder directly

***

## 2. Commands & Implementation

### 2.1 Verification Commands

```bash
ls -la "/Users/dk/Library/Application Support/Code - Insiders/User"
ls -la ~/<private-config-repo>/vscode-insiders-configuration/visual-studio-code-user-settings/
```

### 2.2 Migration Commands

```bash
# Step 1: Verify source exists
ls -la "/Users/dk/Library/Application Support/Code - Insiders/User"

# Step 2: Create destination if needed
mkdir -p ~/<private-config-repo>/vscode-insiders-configuration/visual-studio-code-user-settings

# Step 3: Move nested User contents up (if exists)
mv /path/to/destination/User/* /path/to/destination/
rmdir /path/to/destination/User

# Step 4: Remove old symlink and recreate pointing to destination
rm "/Users/dk/Library/Application Support/Code - Insiders/User"
ln -s ~/<private-config-repo>/vscode-insiders-configuration/visual-studio-code-user-settings "/Users/dk/Library/Application Support/Code - Insiders/User"

# Step 5: Verify symlink resolves
ls -la "/Users/dk/Library/Application Support/Code - Insiders/User"
```

### 2.3 Symlink Validation

The symlink output MUST show:

```
lrwxr-xr-x@ ... -> ~/<private-config-repo>/vscode-insiders-configuration/visual-studio-code-user-settings
```

The symlink MUST NOT contain `/User` at the end of the target path.

***

## 3. Verification Protocol

### 3.1 Structural Check

- [ ] Destination folder exists at the defined path
- [ ] Destination contains VS Code settings files directly (no nested User folder)
- [ ] Symlink exists at source path
- [ ] Symlink points directly to destination (no intermediate User)

### 3.2 Functional Check

- [ ] VS Code Insiders opens without errors
- [ ] Settings are loaded correctly from the new location
- [ ] Extensions and snippets are accessible

***

## 4. Related Skills

- [`tool-config-directory-symlink`](../tool-config-directory-symlink/SKILL.md)
  — Base skill for migrating tool configuration directories into a companion
  repo. This skill is a concrete example of that pattern for VS Code Insiders.
- [`opencode-config-preserve`](../opencode-config-preserve/SKILL.md) — Analogous config preservation for OpenCode CLI/IDE.

## 5. Traceability

- Created: 2026-04-24
- Context: Relocation of VS Code Insiders User settings for portability across machines
