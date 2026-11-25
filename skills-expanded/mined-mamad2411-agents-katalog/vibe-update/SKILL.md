---
name: vibe-update
description: Update vibe and its plugins to the latest version
---

# Vibe Update Skill

Updates vibe marketplace, plugins, permissions, and MCP server configurations to the latest version.

## Instructions

1. **Run the update command:**
   ```bash
   vibe update
   ```

2. **What vibe update does:**
   - Downloads the latest vibe release from GitHub
   - Updates the marketplace at `~/.vibe/marketplace`
   - Syncs permissions to `~/.claude/settings.json`
   - Syncs MCP server configurations
   - Reinstalls all currently installed plugins to pick up changes
   - Updates the vibe CLI itself (requires sudo)

3. **After the update completes:**
   - Inform the user that Claude Code should be restarted to apply changes
   - If the CLI update failed due to sudo, mention they can manually run:
     ```bash
     sudo cp ~/.vibe/marketplace/vibe.sh /usr/local/bin/vibe
     ```

4. **To check current status:**
   - Run `vibe status` to see installed plugins and configuration state
