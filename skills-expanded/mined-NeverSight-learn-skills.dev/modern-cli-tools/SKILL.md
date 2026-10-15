---
name: modern-cli-tools
description: Use faster, modern CLI replacements instead of legacy Unix tools, cross-platform (macOS, Linux, Windows). Covers ast-grep, difftastic, sd, ripgrep, fd, fzf, bat, jq, eza, dust, glow, hyperfine. Trigger whenever searching code/text, diffing files, finding files, listing dirs, viewing files, replacing text, checking disk usage, rendering markdown, or benchmarking commands.
---

# Modern CLI Tools

Prefer these over legacy equivalents for speed and better output. All tools are cross-platform (macOS, Linux, Windows) and installable via `brew`, `apt`, `winget`, `scoop`, `cargo`, or the OS package manager of choice.

| Tool | Use for | Syntax | Legacy equivalent |
|---|---|---|---|
| **rg** (ripgrep) | Fast recursive text/regex search | `rg "pattern" [path]` | `grep -r "pattern" .` |
| **fd** | Fast file/dir finding by name | `fd "pattern" [path]` | `find . -name "*pattern*"` |
| **ast-grep** | Structural/syntax-aware code search & rewrite | `ast-grep run -p 'pattern' [path]` or `ast-grep --lang js -p '$A.map($B)'` | `grep`/regex-based code search |
| **difft** (difftastic) | Syntax-aware semantic diff | `difft file1 file2` (or `git config diff.tool difft`) | `diff file1 file2` |
| **sd** | Simple find-and-replace (regex) | `sd "old" "new" file.txt` | `sed` (macOS: `sed -i ''`, Linux: `sed -i`) |
| **fzf** | Interactive fuzzy finder (pipe into it) | `some_command \| fzf` | manual grepping/selecting |
| **bat** | Syntax-highlighted file viewer w/ line numbers | `bat file.txt` | `cat file.txt` |
| **jq** | JSON query/filter/transform | `jq '.key' file.json` | manual parsing / `python -c ...` |
| **eza** | Better `ls` (icons, tree, git status) | `eza -la --icons --tree` | `ls -la` |
| **dust** | Visual disk usage breakdown | `dust [path]` | `du -sh * \| sort -h` (Linux/macOS); no direct Windows equivalent |
| **glow** | Render Markdown in terminal | `glow file.md` | `cat file.md` |
| **hyperfine** | Benchmark command execution time | `hyperfine 'command'` | `time command` (single run, no stats) |

## Agent-safe usage (non-interactive contexts)

Several tools default to interactive/TTY or pager behavior that breaks when invoked programmatically. Use these overrides when capturing output for further processing:

| Tool | Issue | Fix |
|---|---|---|
| **fzf** | Requires a TTY; hangs/fails without one | Avoid in agent contexts, or pre-filter and skip fzf entirely (e.g. use `rg`/`fd` output directly instead of piping to `fzf`) |
| **bat** | Auto-pages and colorizes | `bat --paging=never --color=never -p file.txt` (or `-p`/`--plain` to drop line numbers/headers too) |
| **glow** | Auto-pages | `glow -p file.md` (`-p` disables pager) |
| **eza** | Colorizes by default even when piped in some configs | `eza -la --color=never` |
| **rg** | Colorizes in some shells | `rg --color=never -n "pattern"` (usually auto-detects non-TTY correctly, but force if piping misbehaves) |

## Machine-readable output

For chaining into scripts or further parsing, prefer structured/plain modes:
- `rg --json "pattern"` — structured match output
- `fd -0` — NUL-separated (safe for filenames with spaces), or `-1` for exactly one result
- `jq -c '.key'` — compact single-line JSON
- `ast-grep run -p 'pattern' --json` — structured match output

## Guidance
- Default to these tools for any matching task; fall back to legacy only if the modern tool is unavailable.
- Check availability cross-platform: `command -v <tool>` (macOS/Linux) or `Get-Command <tool>` (Windows PowerShell). Note: `ast-grep`'s binary may be installed as `sg` on some systems — check both names.
- For code-aware search/refactor (not plain text), prefer `ast-grep` over `rg`/`sd`.
- For reviewing diffs of code (not plain text), prefer `difft` over `diff`.
- Chain with `fzf` for interactive human sessions only; in agent/non-interactive contexts, skip `fzf` and filter programmatically instead (e.g. `rg` + `head`, or `fd` with glob filters).
- On Windows, most tools work identically in PowerShell/cmd/WSL; a few legacy-column syntax differences (e.g. `Get-ChildItem` vs `ls`) don't apply since you're using the modern tool directly.
- `dust`'s binary name can collide with unrelated tools of the same name on some systems — verify with `command -v dust` before relying on it in scripts.
