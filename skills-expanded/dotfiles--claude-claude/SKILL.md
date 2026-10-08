# Global Claude Code Settings

## SDLC
When working on any software project, read and follow `~/.claude/sdlc.md` — it defines the development methodology (change workflow, git hygiene, planning, testing, code quality, architecture, observability, and AI collaboration principles).

## Modern CLI Tools
This machine has modern CLI tools installed. When using the Bash tool, prefer:
- `fd` over `find` — faster, simpler syntax, respects .gitignore
- `rg` over `grep` — faster recursive search, respects .gitignore
- `bat` over `cat` — syntax highlighting (useful for showing file contents to user)
- `eza` over `ls` — better formatting, icons, git status
- `jq` for any JSON processing
- `fzf` is available for interactive fuzzy selection
- `delta` is configured as git's diff pager
- `tldr` (via tlrc) for quick command references

@RTK.md
