---
name: vscode-settings-promotion
description: Automate migration of profile-specific settings to global scope with universal enforcement.
category: VSCode-Configuration
---

# VS Code Settings Promotion Rule (v2)

This skill extracts targeted settings from a profile-specific `settings.json`, promotes them to the global
`settings.json`, and ensures they are added to `workbench.settings.applyToAllProfiles` for universal
enforcement across all profiles.

***

## 1. Protocol & Logic

### 1.1 Promotion Workflow

1. **Identify Targets**: Determine which settings in a profile `settings.json` should be global.
1. **Extraction**: Read the values from the profile file.
1. **Global Injection**: Insert these settings into the global `settings.json`.
1. **Universal Enforcement**: Add the keys to the `workbench.settings.applyToAllProfiles` array in the global file.
1. **Profile Cleanup**: Remove the settings from the profile file to prevent duplicate definitions.
1. **Industrial Synchronization**: If the user maintains a `<private-config-repo>` repository, ensure the source-of-truth
   files are also updated to maintain consistency.

### 1.2 Preservation Rules

- **Formatting**: Maintain the existing indentation of the target files.
- **Backups**: Always create a `.bak` copy of `settings.json` before modification (automated by the script).
- **Deduplication**: Do not add keys to `applyToAllProfiles` if they already exist.
- **Preservation Mandate**: Do not remove existing unrelated settings during the promotion process.

***

## 2. Automation Utility

The promotion process is automated via the industrial-grade Python script located at:
`[promote.py](./scripts/promote.py)`

### 2.1 Usage

Execute the script using the following command structure:

```bash
python3 .agents/skills/vscode-settings-promotion/scripts/promote.py \
  --profile "/path/to/profile/settings.json" \
  --global-settings "/path/to/global/settings.json" \
  --keys "setting.key.one" "setting.key.two"
```

### 2.2 Features

- **Atomic Backups**: Automatically creates `.bak` files for both source and target.
- **Dry Run Mode**: Use `--dry-run` to preview changes without modifying files.
- **Fidelity Check**: Ensures values are moved exactly as they exist in the profile.

***

## 3. Verification Protocol

### 3.1 Syntax Validation

- Ensure both `settings.json` files pass a JSON parser check (`jq .`) after modification.
- Verify `applyToAllProfiles` contains no duplicate entries.

### 3.2 Functional Check

- Verify the settings are removed from the profile-specific file.
- Verify the settings exist in the global file and are correctly listed under `applyToAllProfiles`.

***

## 4. Related Skills

- [VS Code Settings Indent Override](../vscode-settings-indent-override/SKILL.md) — apply per-key
  non-standard indentation overrides after promotion (e.g. 6-space level-2 for `files.associations`,
  8-space `approve`/`matchCommandLine` for `chat.tools.terminal.autoApprove`).
- [VS Code Multi-Scope Setting Write](../vscode-multi-scope-setting-write/SKILL.md) — sibling
  base primitive for the workspace-file (`.code-workspace`) vs folder (`.vscode/settings.json`)
  scope cascade. Use when a setting must persist regardless of whether VS Code opens the
  directory directly or through a workspace file.
