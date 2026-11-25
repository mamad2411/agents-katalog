---
name: where-is
description: Resolve a project, repo or directory name to its absolute path on this machine, ranked by how often it actually gets used (zoxide), with a filesystem fallback and a short orientation blurb. Works from any directory. Use when the user asks "where is X", "what's the path to X", "point at my X repo", "cd to X", "open X", or otherwise names another project and you need its real path before reading or writing anything in it.
---

# where-is

One script does the whole resolution ladder. Run it, do not reimplement it.

```bash
~/dotfiles/.claude/skills/where-is/scripts/where-is.sh <name>               # path + orientation
~/dotfiles/.claude/skills/where-is/scripts/where-is.sh <name> --path-only   # path only
```

That is the canonical path. Both `~/.claude/skills/` and `~/.agents/skills/` symlink to it, so it resolves identically for Claude Code and Codex.

Reach for `--path-only` when the path is a string you are about to interpolate (handing a directory to another agent, building a command, `--add-dir`). Use the default when you are about to read or write in that repo, so you know what it is before you touch it.

## Reading the output

| Field | Meaning |
|---|---|
| `PATH:` | The resolved absolute path. This is the answer. |
| `GIT:` | Branch and origin, when it is a repo. |
| `ORIENTATION:` | First 30 lines (2000 byte cap) of `AGENTS.md`, else `CLAUDE.md`, else `README.md`. |
| `MANIFEST:` / `TOP LEVEL:` | Fallback when none of those exist. |

Roughly half of these directories have no agent file, so the manifest fallback is the normal path, not a failure.

## Exit codes

- **0** resolved.
- **2** ambiguous. The script lists the candidates and deliberately reads no orientation file. Show the candidates and ask which one. Never pick for the user.
- **1** not found. Not in zoxide, not under the search roots.

## Rules

- **Never invent a path.** On exit 1, say it was not found. A plausible-looking `~/dev/personal/<name>` that does not exist is worse than no answer, because the next tool call fails somewhere else.
- **Never fall back to guessing on exit 2.** Ambiguity is information; hand it to the user.
- zoxide only knows directories reached from a terminal. A repo that exists but was never `cd`'d into resolves through the `fd` fallback, one rank lower in confidence, and the script says which source it used.
