# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an Obsidian vault used for personal knowledge management. Obsidian is a markdown-based note-taking application that stores notes as plain text files.

## Installed Plugins

### Terminal Plugin

The vault has the "Terminal for Obsidian" plugin installed, which integrates terminals into Obsidian.

**Plugin Configuration:**
- Plugin data: `.obsidian/plugins/terminal/data.json`
- Default integrated terminal (Windows): `cmd.exe`
- Default external terminal (Windows): `cmd.exe`
- Terminal history restoration is disabled by default
- Python executable: `python3` (required for terminal resizing features)

**Terminal Profiles Available:**
- Windows integrated/external (cmd.exe)
- Linux integrated (sh) / external (xterm)
- macOS integrated (zsh) / external (Terminal.app)
- Developer Console profile

## Vault Structure

**Core Directories:**
- `.obsidian/` - Obsidian configuration and workspace data
  - `plugins/` - Installed community plugins
  - `workspace.json` - Current workspace layout
  - `app.json`, `appearance.json` - App settings
  - `core-plugins.json`, `community-plugins.json` - Plugin configurations

**Content Files:**
- `환영합니다!.md` - Welcome note (Korean)
- `무제.base` - Base file with table view configuration

## Working with Obsidian Vaults

When modifying files in this vault:

1. **Markdown Files**: All notes are stored as `.md` files with standard markdown syntax. Obsidian uses `[[wikilinks]]` for internal linking.

2. **Configuration Files**: The `.obsidian/` directory contains JSON configuration files. These should be edited carefully as invalid JSON will break the vault.

3. **Workspace State**: `.obsidian/workspace.json` contains the current layout of open files, tabs, and panes. This file is automatically updated by Obsidian.

4. **Plugin Data**: Each plugin stores its settings in `.obsidian/plugins/<plugin-name>/data.json`

## Language

This vault appears to use Korean as the primary language, as evidenced by:
- Korean welcome note (`환영합니다!.md`)
- Korean UI labels in workspace configuration
- Terminal plugin showing Korean interface text

## Common Tasks

**Terminal Operations:**
Since the Terminal plugin is installed, you can reference terminal commands that would be available through the plugin's integrated terminal feature.

**Note Management:**
When creating or editing markdown notes, maintain compatibility with Obsidian's markdown flavor, which supports:
- WikiLinks: `[[Note Name]]`
- Block references: `[[Note Name#^block-id]]`
- Embedded notes: `![[Note Name]]`
- Frontmatter (YAML) metadata at the top of files
