---
name: discover-shims
description: Discover available Scoop shims and identify valuable command-line tools. Use when the user asks about available tools, what commands they can use, or wants to explore their Scoop environment.
---

# Discover Shims Skill

This skill helps you discover and catalog available Scoop shims, identifying valuable command-line tools that can replace default Windows commands.

## When to Use

Trigger this skill when the user asks:
- "What tools are available?"
- "What commands can I use?"
- "What shims do I have?"
- "Explore my Scoop environment"

## Steps

### 1. Scan Available Tools

Run both `scoop shim list` and scan PATH for Scoop-related directories:

```powershell
# Get all shims
scoop shim list

# Get Scoop-related paths from PATH
$scoopPaths = $env:PATH -split ';' | Where-Object { $_ -match 'scoop' } | Where-Object { $_ -match '\\apps\\' }

# List executables in those directories
$scoopPaths | ForEach-Object {
    Get-ChildItem -Path $_ -Filter "*.exe" -ErrorAction SilentlyContinue
} | Select-Object -ExpandProperty Name
```

### 2. Analyze Each Command

For each command (from shim list and PATH), gather information:

```powershell
# Get help information (skip if obviously a GUI program)
<cmd> --help

# Get Scoop package info
scoop info <cmd>

# Get source package (for commands from PATH)
scoop shim info <cmd>
```

**IMPORTANT:** Do NOT run `--help` on obviously GUI programs (e.g., firefox, vscode, notepad++). Running them will launch the application and interrupt the user. Use `scoop info <cmd>` to check the description and homepage instead.

**Note:** `scoop shim info <cmd>` returns the source package name (e.g., `fchash` comes from `fastcopy`). Use the `Source` field for tracking.

### 3. Determine Tool Value and Deduplicate

Based on the help info and Scoop info, determine if each command is:
- ✓ A valuable third-party command-line tool (record it)
- ✗ A programming language itself (skip - e.g., python, node, go, rust)
- ✗ A language's built-in tool (skip - e.g., pip, npm, cargo)
- ✗ A TUI program (skip - not suitable for Agent sessions)
- ✗ A GUI program (skip)
- ✗ An interactive editor (skip)
- ✗ A shell function/alias (skip - e.g., zoxide requires `zoxide init powershell` to create `z` alias, not a standalone shim)

**If tool is unknown:**
- Use `scoop info <cmd>` to get the homepage URL
- Visit the homepage to understand the tool's purpose
- Determine if it's a valuable third-party tool (not a language or built-in tool)

**Deduplication rules:**
- Use command name as unique key
- If same command appears in both shim list and PATH, record only once
- Prefer `scoop shim info` for source tracking (more reliable)
- If package provides multiple commands (e.g., ffmpeg, ffprobe), record each separately
- **IMPORTANT**: Do NOT use text processing tools (grep, awk, etc.) for deduplication. You already have all the information in the command outputs - analyze them directly.

**Enrich each recorded tool:**
- **Replacement target**: Read the `scoop info` Description field. If it mentions "alternative to X", "X clone", or "X replacement", infer that the tool replaces X. If Description is unclear, fall back to `--help` output. If no built-in equivalent exists, describe the capability without a "replaces" clause.
- **Usage examples**: Extract 1-2 common invocation patterns from `--help` output. Prefer the simplest, most frequent use case.
- **Category**: Assign each tool to a functional category based on its purpose (e.g., Text Search, File Finding, File Operations). If no existing category fits, create a new one or use System Utilities.

See the few-shot examples below the format template for guidance on inference patterns.

### 4. Write to Global Memory

**IMPORTANT: If the `<!-- scoop-shims start -->` comment block already exists in your global memory file, you MUST replace the entire block content with the newly discovered tools. Do NOT skip, merge, or leave it unchanged.**

Write discovered tools to your global memory file in a comment block:

```markdown
<!-- scoop-shims start -->
Scoop is a package manager for Windows. These are the command-line tools that have already been installed. Before executing ANY CLI command, check this block FIRST for a suitable tool. These are faster and more capable than PowerShell cmdlets. Only fall back to PowerShell when no match found here:

## Text Search
- rg (ripgrep): replaces grep, recursive regex search, auto-respects .gitignore
  rg "TODO" --glob "*.ts"

## File Finding
- fd: replaces find, simpler syntax, auto-respects .gitignore
  fd "\.tsx$"

## File Viewing
- bat: replaces cat, built-in syntax highlighting and line numbers
  bat src/main.ts

## System Utilities
- lsd: replaces ls, with icons and colors
  lsd -la
<!-- scoop-shims end -->
```

**Format rules:**
- First line: actionable instruction telling the agent to prefer these tools over PowerShell cmdlets
- Group tools under functional category headers (e.g., Text Search, File Finding, File Operations)
- One tool per line
- Format: `- cmd (package): replaces X, description` (if has replacement) or `- cmd (package): description` (if no direct replacement)
- Include 1-2 example commands per tool showing common invocation patterns
- If comment block exists, replace entire block content
  ✗ WRONG: "The block already exists with 12 tools — skipping"
  ✓ CORRECT: Overwrite the entire block with newly discovered tools
- If a tool doesn't fit existing categories, create a new one or place under System Utilities

**Few-shot examples for inferring replacement targets:**

Example 1 — Command name differs from package name:
> Found `fchash` in shim list → `scoop info fchash` fails (not a package name)
> → Use `scoop shim info fchash` → Source: `fastcopy`
> → `scoop info fastcopy` → "FastCopy is the fastest copy/backup software"
> → Inference: file hash tool, no direct built-in replacement
> → Output: `- fchash (fastcopy): compute file hashes`

Example 2 — Description implies replacement:
> `scoop info bat` → "A cat(1) clone with syntax highlighting and Git integration"
> → Inference: "cat clone" → replaces cat
> → Output: `- bat: replaces cat, built-in syntax highlighting and line numbers`

Example 3 — Description and --help are unclear, visit homepage, then skip:
> `scoop info zoxide` → "A smarter cd command" — unclear what it replaces
> → Visit homepage (https://github.com/ajeetdsouza/zoxide) → learn it requires `zoxide init powershell` to create `z` shell function
> → Detection: `z` is not a Scoop shim, it's a shell alias — skip
> → Action: skip (shell function, not a standalone executable)

## Output

After scanning, inform the user:
- How many shims were scanned
- How many valuable tools were identified
- What was written to global memory

## Notes

- This skill does NOT maintain hardcoded lists - let the Agent judge based on help info
- TUI/GUI programs are skipped as they're not suitable for Agent sessions
- The global memory block can be updated anytime by re-running this skill
