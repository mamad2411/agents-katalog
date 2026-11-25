---
name: mcp-tools
description: |
  Control IntelliJ IDEA through MCP server. File operations, editor control, run configs,
  VCS status, debugging, scopes, file colors. Use when working with JetBrains IDEs, running
  tests from IDE, managing project structure, or configuring file scopes.
  Keywords: idea, intellij, jetbrains, ide, mcp, scopes, file colors.
triggers:
  - /idea
  - /idea status
  - /idea files
  - /idea vcs
  - /idea run
  - /idea scopes
  - intellij commands
  - jetbrains integration
  - configure file scopes
  - setup IDEA scopes
  - file colors dark theme
negative_triggers:
  - VS Code operations
  - vim/neovim editing
  - IDE not running or MCP server not connected
version: 1.0.0
author: Christian Kusmanow / Claude
last_updated: 2026-01-31
migrated_from: .claude/skills/idea v2.0.0
---

# Skill: IntelliJ IDEA MCP Integration

Control and interact with JetBrains IntelliJ IDEA directly through the Model Context Protocol (MCP) server.

## Trigger
- `/idea` - Show available IntelliJ IDEA MCP commands and current IDE status
- `/idea [action]` - Execute a specific IDE action

## Arguments
$ARGUMENTS

## Prerequisites

The JetBrains MCP server must be configured and running:

1. **IntelliJ IDEA** must be open with the MCP Server plugin enabled
2. **MCP Server** must be added to Docker MCP Gateway:
   ```
   mcp-find jetbrains
   mcp-config-set jetbrains {"port": <PORT>}
   mcp-add jetbrains
   ```
3. The port can be found in `C:\Users\Chris\AppData\Roaming\Claude\claude_desktop_config.json` under `IJ_MCP_SERVER_PORT`

## Available Tools

### File Operations
| Tool | Description |
|------|-------------|
| `create_new_file_with_text` | Create a new file with specified content |
| `get_file_text_by_path` | Read file contents by relative path |
| `replace_file_text_by_path` | Replace entire file content |
| `replace_specific_text` | Find and replace text in a specific file |
| `find_files_by_name_substring` | Search for files by name pattern |
| `list_files_in_folder` | List files in a directory |
| `list_directory_tree_in_folder` | Get hierarchical project structure |

### Editor Operations
| Tool | Description |
|------|-------------|
| `get_open_in_editor_file_path` | Get path of currently active file |
| `get_open_in_editor_file_text` | Get content of currently active file |
| `get_all_open_file_paths` | List all open file paths |
| `get_all_open_file_texts` | Get content of all open files |
| `get_selected_in_editor_text` | Get currently selected text |
| `replace_selected_text` | Replace selected text |
| `replace_current_file_text` | Replace entire content of active file |
| `open_file_in_editor` | Open a file in the editor |

### Project & VCS
| Tool | Description |
|------|-------------|
| `get_project_modules` | List all project modules with dependencies |
| `get_project_dependencies` | List all project dependencies |
| `get_project_vcs_status` | Get Git/VCS status of files |
| `find_commit_by_message` | Search commits by message |
| `search_in_files_content` | Search text across all project files |

### Run & Debug
| Tool | Description |
|------|-------------|
| `get_run_configurations` | List available run configurations |
| `run_configuration` | Execute a run configuration by name |
| `get_debugger_breakpoints` | List all breakpoints |
| `toggle_debugger_breakpoint` | Add/remove breakpoint at line |

### Terminal & IDE Actions
| Tool | Description |
|------|-------------|
| `execute_terminal_command` | Run command in IDE terminal |
| `execute_action_by_id` | Execute IDE action by ID |
| `list_available_actions` | List all available IDE actions |
| `get_terminal_text` | Get terminal output |
| `get_progress_indicators` | Check running tasks/progress |

### Utility
| Tool | Description |
|------|-------------|
| `wait` | Wait for specified milliseconds |

---

## Scopes & File Colors

IntelliJ IDEA scopes provide powerful file filtering and visual organization capabilities.

### Scope Configuration

Scopes are stored in `.idea/scopes/*.xml` with the following format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<component name="DependencyValidationManager">
  <scope name="Scope Name" pattern="file[ModuleName]:path//*" />
</component>
```

### Scope Pattern Syntax

| Pattern | Description |
|---------|-------------|
| `file[Module]:path//*` | Files in path recursively |
| `file[Module]:path/*` | Files in path (no subdirs) |
| `file:*.ext` | Files by extension |
| `\|\|` | OR operator |
| `&&` | AND operator |
| `!` | NOT operator |
| `$ScopeName` | Reference another scope |

### File Colors Configuration

File colors are configured in `.idea/workspace.xml` under `<component name="FileColors">`:

```xml
<component name="FileColors">
  <fileColor scope="Scope Name" color="hexcode" />
</component>
```

**Dark Theme Color Palette:**
| Purpose | Hex | Description |
|---------|-----|-------------|
| Yellow | `4a4522` | Dark Olive |
| Blue | `2e4a5a` | Dark Nordic |
| Green | `2a4a3a` | Dark Forest |
| Purple | `4a2a4a` | Dark Plum |
| Orange | `5a3a1a` | Dark Amber |
| Gray | `3a3a3a` | Dark Gray |
| Cyan | `1a4a5a` | Dark Teal |

### If `$ARGUMENTS` is "scopes":

1. List existing scopes from `.idea/scopes/`
2. Show current file colors from `.idea/workspace.xml`
3. Suggest scope improvements based on project structure

### If `$ARGUMENTS` is "scopes setup" or "scopes create":

1. Analyze project structure (folder hierarchy)
2. Create logical scope groupings
3. Generate scope XML files in `.idea/scopes/`
4. Configure file colors in workspace.xml
5. Use dark theme colors by default

### If `$ARGUMENTS` is "scopes colors":

1. Read current file colors from workspace.xml
2. Display color assignments
3. Suggest adjustments for dark/light themes

## Command Handling

### If `$ARGUMENTS` is empty or "status":
1. Check if JetBrains MCP server is connected
2. If not connected, attempt to connect using `mcp-find`, `mcp-config-set`, and `mcp-add`
3. Show current IDE status:
   - Currently open file
   - All open files
   - Project VCS status
   - Running progress indicators

### If `$ARGUMENTS` is "files":
List all open files in the editor using `get_all_open_file_paths`.

### If `$ARGUMENTS` is "tree" or "structure":
Show project directory tree using `list_directory_tree_in_folder` with path "/" and maxDepth 3.

### If `$ARGUMENTS` is "vcs" or "git":
Show VCS status using `get_project_vcs_status`.

### If `$ARGUMENTS` is "runs" or "configurations":
List run configurations using `get_run_configurations`.

### If `$ARGUMENTS` is "breakpoints":
List all breakpoints using `get_debugger_breakpoints`.

### If `$ARGUMENTS` is "modules":
List project modules using `get_project_modules`.

### If `$ARGUMENTS` is "deps" or "dependencies":
List project dependencies using `get_project_dependencies`.

### If `$ARGUMENTS` is "terminal":
Get terminal output using `get_terminal_text`.

### If `$ARGUMENTS` is "actions":
List available IDE actions using `list_available_actions`.

### If `$ARGUMENTS` starts with "open ":
Open the specified file using `open_file_in_editor`.

### If `$ARGUMENTS` starts with "run ":
Execute the specified run configuration using `run_configuration`.

### If `$ARGUMENTS` starts with "search ":
Search in files using `search_in_files_content` with the query.

### If `$ARGUMENTS` starts with "find ":
Find files by name using `find_files_by_name_substring`.

### If `$ARGUMENTS` starts with "exec " or "action ":
Execute IDE action by ID using `execute_action_by_id`.

### If `$ARGUMENTS` starts with "cmd " or "terminal ":
Execute terminal command using `execute_terminal_command`.

### If `$ARGUMENTS` is "current" or "active":
Show the currently active file path and content using `get_open_in_editor_file_path` and `get_open_in_editor_file_text`.

### If `$ARGUMENTS` is "selected" or "selection":
Get selected text using `get_selected_in_editor_text`.

### If `$ARGUMENTS` is "help":
Display this skill documentation with all available commands.

## Usage Guidelines

1. **Always ensure IntelliJ IDEA is running** before attempting to use these commands
2. **File paths are relative to project root** unless specified as absolute
3. **Use `get_project_vcs_status`** before making changes to understand current state
4. **Prefer `replace_specific_text`** over `replace_file_text_by_path` for targeted edits
5. **Check `get_progress_indicators`** if IDE seems busy or unresponsive
6. **Use `wait`** when chaining commands that need IDE to process (e.g., after running a configuration)

## Example Usage

```
/idea                    # Show IDE status and open files
/idea files              # List all open files
/idea tree               # Show project structure
/idea vcs                # Show Git status
/idea open src/main.ts   # Open a specific file
/idea run "Debug App"    # Run a configuration
/idea search TODO        # Search for TODO in all files
/idea find config        # Find files with "config" in name
/idea terminal npm test  # Run npm test in terminal
/idea current            # Show current file content
/idea help               # Show this help
```

## Error Handling

If the MCP server is not connected:
1. Use `mcp__MCP_DOCKER__mcp-find` with query "jetbrains" to verify availability
2. Use `mcp__MCP_DOCKER__mcp-config-set` to set the port configuration
3. Use `mcp__MCP_DOCKER__mcp-add` to activate the server

Common issues:
- **Port mismatch**: Check `IJ_MCP_SERVER_PORT` in claude_desktop_config.json
- **IDE not running**: Start IntelliJ IDEA and ensure MCP Server plugin is enabled
- **Plugin disabled**: Go to Settings > Plugins > MCP Server and enable it

## References

- [Scopes Guide](references/scopes-guide.md) - Complete guide to IDEA scopes and file colors

---

## Metadata

```yaml
author: Christian Kusmanow / Claude
version: 1.0.0
last_updated: "2026-01-31"
migrated_from: .claude/skills/idea v2.0.0
change_surface: references/ (scopes guide, tool updates)
```
