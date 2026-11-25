---
name: file-organizer
description: Use when user wants to organize files, move files, clean up downloads, categorize files, add tags, rename files, or detect duplicates - provides file organization with YAML-based rules
allowed-tools: Bash, Glob, Read, AskUserQuestion
---

# File Organizer

Helps you organize file systems with YAML-based rules for automated operations.

## Features

- **File Moving**: Move files by type/source/pattern to designated directories
- **File Renaming**: Remove garbled characters, unify formats, standardize naming
- **Mac Tags**: Add color tags and custom text labels to files
- **Duplicate Detection**: Find duplicate files by content/name and process by rules
- **AI Insights**: Analyze directories and intelligently recommend organization rules

## Mac Tag Commands

Use the `tag` command-line tool for tag operations.

### Tag Colors

| Color   |
|---------|
| gray    |
| green   |
| purple  |
| blue    |
| yellow  |
| red     |
| orange  |

### Usage

```bash
# Add tag (color + text)
# Format: tag --add "label"$'\n'"color_code" file
# Color codes: 1=gray, 2=green, 3=purple, 4=blue, 5=yellow, 6=red, 7=orange

# Example: Red "To Delete" tag
tag --add "To Delete"$'\n'"6" /Users/alien/Downloads/README.md

# Example: Blue "Invoice" tag
tag --add "Invoice"$'\n'"4" file.pdf

# List tags on a file
tag --list file

# List all used tags
tag --usage
```

### Using in Skills

When executing tag operations, use the `tag` command:

```bash
tag --add "label"$'\n'"color_code" <file_path>
```

## Trigger Methods

### Auto Trigger

Automatically triggers when you say:
- "整理下载目录" (organize downloads)
- "整理桌面" (organize desktop)
- "移动文件" (move files)
- "清理重复文件" (clean duplicates)
- "给文件打标签" (tag files)
- "分析一下我的下载目录" (analyze my downloads)

### Manual Invocation

- `/file-organizer` - Manual skill invocation

## First-Time Usage Flow

```
1. Skill starts → 2. Check rules → 3. Rules exist? Execute : Guide to create → 4. Preview → 5. Confirm execution
```

### Rule Detection

The skill automatically checks `~/.file-organizer/rules/` for valid rules on startup.

### No Rules Guidance

If no rules exist, the skill will:
1. Ask which directory you want to organize
2. Use AI to analyze directory contents
3. Provide rule suggestions
4. Save rules and execute after your confirmation

## Environment Requirements

- Python 3.8+
- macOS
- `tag` command-line tool (required for Mac Tag functionality)

### Installing tag Command

```bash
brew install tag
```

Pre-first-use check:

### Initial Setup

Before first use, check if tag command is installed:

```bash
which tag || brew install tag
```

The skill will automatically create config directories:
- `~/.file-organizer/rules/` - Rule files
- `~/.file-organizer/logs/` - Operation logs
- `~/.file-organizer/config.yaml` - Configuration file

## Configuration File

Location: `~/.file-organizer/config.yaml`

```yaml
# Preview mode (true=preview, false=execute)
dry_run: true

# Scan directories
scan_paths:
  - ~/Downloads
  - ~/Documents
  - ~/Desktop

# Log level
log_level: info
```

## Rule Syntax

### move.yaml - Move Rules

```yaml
rules:
  - name: "WeChat PDF Organization"
    condition:
      path: "~/Downloads"
      extension: ["pdf", "doc", "docx"]
      pattern: "WeChat|微信"
    action:
      move: "~/Documents/WeChat"
      create_if_missing: true
      tag:
        color: "blue"
        label: "WeChat"
```

**condition options**:
- `path`: Source directory path (supports ~ shorthand)
- `extension`: Array of file extensions, e.g., `["xlsx", "xls"]`
- `pattern`: Regex or keyword pattern for filename matching
- `size_gt`: Greater than specified size, e.g., `100MB`

**action options**:
- `move`: Target directory path
- `create_if_missing`: Whether to create target directory
- `tag.color`: Mac tag color (gray, red, orange, yellow, green, blue, purple)
- `tag.label`: Tag text label

### rename.yaml - Rename Rules

```yaml
rules:
  - name: "Remove duplicate parentheses"
    condition:
      pattern: "（(\\d+)）|\\((\\d+)\\)"
    action:
      replace: "-"
      prefix: ""
      suffix: ""
      separator: "-"
```

### tag.yaml - Tag Rules

```yaml
rules:
  - name: "Large file tag"
    condition:
      size_gt: 100MB
    action:
      tag:
        color: "red"
        label: "Large File"
```

### duplicate.yaml - Duplicate Detection Rules

```yaml
rules:
  - name: "Duplicate handling"
    check_by: "content"  # content or name
    action:
      keep: "newest"  # newest, oldest, first
      tag_duplicates: true
      duplicate_label: "Duplicate"
```

## Usage Examples

### Organize Downloads
```
"帮我整理下载目录" (Help me organize downloads)
→ Scan ~/Downloads
→ Apply rules, show preview
→ You say "执行" (execute) → Execute operations
```

### AI Analysis & Suggestions
```
"分析一下我的下载目录有什么" (Analyze what's in my downloads)
→ AI analyzes directory contents
→ Provides rule suggestions
→ Save and execute after your confirmation
```

### Move Specific Files
```
"把微信的 PDF 移到 Documents" (Move WeChat PDFs to Documents)
→ Scan ~/Downloads
→ Match PDF + WeChat
→ Preview operations
→ Execute
```

### Remove Duplicate Naming
```
"重命名所有包含 (1) 的文件" (Rename all files containing (1))
→ Scan matching files
→ Preview rename results
→ Execute
```

### Check Duplicate Files
```
"检查下载目录的重复文件" (Check duplicates in downloads)
→ Detect by content/name
→ Show duplicate file list
→ You choose which to keep
```

## Execution Modes

### Preview Mode (Default)
1. Scan source directory
2. Apply rules
3. Show operation summary
4. Wait for you to say "执行" (execute) or "确认" (confirm)

### Execution Mode
After you say "执行", "确认":
1. Execute operations one by one
2. Show execution results
3. Log to file

## Troubleshooting

### Issue: Skill not responding
- Check if match rules are correctly configured in SKILL.md
- Try manual invocation with `/file-organizer`

### Issue: Rules not working
- Check YAML syntax is correct
- Confirm rule files are in `~/.file-organizer/rules/` directory
- Use `--verbose` for detailed information

### Issue: Tag functionality not working
- Confirm running on macOS
- Check if AppleScript is available

### Issue: Move operations failing
- Check if target directory has write permissions
- Confirm sufficient disk space
