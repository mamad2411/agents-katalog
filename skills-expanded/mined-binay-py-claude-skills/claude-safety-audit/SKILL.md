---
name: claude-safety-audit
description: Audit a Claude Code setup for the risks that cause leaked keys and wiped machines. Finds secrets saved into permission rules by "Yes, and don't ask again", .claude/settings.local.json or .mcp.json committed to git or still in git history, over-broad allow rules (Bash(*), rm, sudo, git push incl. --force, curl | sh), bypassPermissions mode, and missing deny rules. Can fix them with backups. Use when the user asks if their Claude Code setup is safe, after a scare, before open-sourcing a repo, or when setting up a new machine.
---

# claude-safety-audit

`scripts/audit.mjs` is zero-dependency Node 22+. It is read-only unless `--apply` is passed, and it never prints a full secret (only the first 6 characters).

```
node audit.mjs                          # ~/.claude + every git repo under the current folder (depth 4)
node audit.mjs --root ~/code --root ~/work
node audit.mjs --fix                    # preview fixes
node audit.mjs --fix --apply            # apply them (every touched file is backed up as *.bak-<timestamp>; files inside a git repo are backed up to ~/.claude/backups/ so the copy can't be committed)
```

## What it checks
| Severity | Finding |
|---|---|
| high | A token, key, password, JWT or credentialed URL inside a `permissions.allow` rule. "Yes, and don't ask again" saves the **exact command**, secrets included. |
| high | `settings.local.json` / `.mcp.json` with a secret that git tracks. |
| high | `Bash(*)`, `sudo`, `git push:*` or `git:*` (which include `--force`), `curl … \| sh`, disk tools; `defaultMode: bypassPermissions`; home or root in `additionalDirectories`. |
| medium | Secret files present in git **history**, not in `.gitignore`, `rm`/`Remove-Item` allowed, no deny rules. |
| low/info | The bypass-mode warning hidden, no PreToolUse safety hook, keys in `~/.claude.json`. |

## Fixes it can apply
- Remove allow rules that contain secrets (Claude will ask again next time, which is the point).
- Add deny rules for catastrophic commands to `~/.claude/settings.json`: `rm -rf ~` and `/`, `git push --force`, `git reset --hard`, `git clean -fdx`, `mkfs`, `dd`, `diskpart`, plus `Read(.env)` / `Read(.env.*)` (bare names match at any depth), `~/.ssh` and `~/.aws`. Per the Claude Code permissions docs, `:*` and a trailing ` *` are equivalent, and deny rules apply to every part of a compound command. But Bash rules are not a security boundary (`sh -c` or a full path gets around them), which is why `bash-checkpoint` exists.
- Add `.claude/settings.local.json` to `.gitignore`, and `git rm --cached` it if tracked (the local file stays).

## What you must tell the user
- **A secret that was ever committed and pushed is compromised.** Removing it from the repo does not help: rotate the key at the provider first, then clean history if they want (`git filter-repo` / BFG).
- Deny rules are prefix matches and are a safety net, not a sandbox. Pair them with the `bash-checkpoint` hook (snapshots before destructive commands) and, for risky work, a container.
- Ask before `--apply` on settings the user cares about. Show the `--fix` preview first.
