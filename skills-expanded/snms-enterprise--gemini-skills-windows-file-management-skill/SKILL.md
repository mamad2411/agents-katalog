---
name: windows-file-management
description: Use when performing file operations (browse, copy, move, rename, delete) using Windows File Explorer GUI or the Windows FileSystem API via MCP.
---

# Windows File Management

## Overview
Efficiently manage files on Windows using a hybrid approach of direct API calls (for speed) and GUI automation (for complex interactive tasks).

## When to Use
- **FileSystem API**: Use for bulk operations, scriptable tasks, and when precision is required without visual feedback.
- **File Explorer GUI**: Use when you need to interact with specialized shell features (context menus, property dialogs) or when the user explicitly requests visual automation.

## Core Patterns

### 1. Direct FileSystem API (Preferred)
Use the `FileSystem` tool for most tasks. Always use **absolute paths** to avoid ambiguity.

```powershell
# List files in project
FileSystem { mode: "list", path: "C:\\Users\\xxx\\crm-portal" }

# Read file metadata
FileSystem { mode: "info", path: "C:\\Users\\xxx\\crm-portal\\crm.sqlite" }
```

### 2. File Explorer GUI Automation
When using the GUI, follow this sequence: **Launch -> Focus -> Snapshot -> Act**.

#### Navigation & Focus
- **Launch with path**: `mcp_windows-mcp_PowerShell { command: "explorer C:\\path\\to\\folder" }`
- **Switch/Focus**: `mcp_windows-mcp_App { mode: "switch", name: "Eksplorator plików" }`
- **Address Bar**: Use `Shortcut { shortcut: "alt+d" }` then `Type { text: "C:\\new\\path", press_enter: true }`.

#### Common Shortcuts
| Action | Shortcut |
|--------|----------|
| Copy | `ctrl+c` |
| Paste | `ctrl+v` |
| Cut | `ctrl+x` |
| Rename | `f2` |
| New Folder | `ctrl+shift+n` |
| New Window | `ctrl+n` |
| Close Window | `alt+f4` |
| Delete (to Bin) | `delete` |
| Delete (Permanent) | `shift+delete` |

#### Selecting Items
1. **Search**: Use `FileSystem { mode: "search", pattern: "..." }` first to find the file's exact name.
2. **Type-to-find**: Once Explorer is focused, use `Type { text: "filename" }` to highlight the item.
3. **Multi-select**: Use `MultiSelect` with coordinates or labels from `Snapshot`.

## Common Mistakes
- **Relative Paths**: `FileSystem` defaults to the Desktop. Always provide the full `C:\Users\...` path.
- **Z-Order Issues**: Explorer might be hidden behind other windows. Use `App { mode: "switch" }` before taking a `Snapshot`.
- **Language Sensitivity**: Element names (like "Eksplorator plików" vs "File Explorer") depend on the OS locale. Check `Snapshot` labels carefully.

## Red Flags
- Clicking blind without a fresh `Snapshot`.
- Using GUI automation for simple tasks like `copy` or `move` when the `FileSystem` tool can do it in one turn.
- Forgetting to escape backslashes in tool parameters (`C:\\path` not `C:\path`).
