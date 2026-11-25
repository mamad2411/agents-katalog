---
name: commit-message-from-changes
description: Reads git status and diff (staged or working tree), analyzes changes, and generates a Conventional Commits-style commit message. Use when the user asks for a commit message, wants to commit their changes, or asks to "create a commit message from my changes."
---

# Commit Message From Changes

Generate a commit message by inspecting the user's git changes. Prefer **staged** changes; if nothing is staged, use the working tree.

## Platform

1. **Detect OS** before running commands. Use one of:
   - **Windows**: `echo $env:OS` (PowerShell) or check user_info for `win32`.
   - **Linux/macOS**: `uname -s` or `echo $OSTYPE` (bash).
2. **Use the appropriate shell and syntax**:
   - **Windows (PowerShell)**: Run git in PowerShell. Use double quotes if you need to pass quoted args; avoid bash-only constructs (e.g. `$(...)` for command substitution — use PowerShell equivalents if needed).
   - **Linux/macOS (bash)**: Run git in bash. Standard git invocations below work as-is.

Git itself is cross-platform; `git status`, `git diff --staged`, and `git diff` behave the same. Use only these portable git invocations so the same workflow works on both platforms.

## Workflow

1. **Gather changes**
   - Run `git status` to see what is staged and what is modified.
   - Run `git diff --staged` for the diff to commit. If empty, run `git diff` and treat that as the change set (and note "no staged changes" in your reply).
   - Optionally run `git diff --staged --stat` or `git diff --stat` for a quick summary.

2. **Analyze**
   - Identify scope: docs, proxmox, docker_compose, core, media, config, etc.
   - Identify type: feature, fix, docs, chore, refactor, style.
   - Build a short list of what changed (files or logical changes).
   - Summarize the intent in one short subject line; put the list of changes in the body.

3. **Output** (use this markdown structure so the message is copy-pastable)
   - **List of changes**: A markdown bullet list summarizing what changed (files and/or edits).
   - **Copy-pastable commit message**: A single fenced code block (no language tag) containing the full commit message including the list of changes in the body. The user should be able to copy the block contents and paste into `git commit -m "..."` or the multi-line editor.
   - Optionally add one short sentence above the block (e.g. "Suggested commit message:").

## Commit message format

Use [Conventional Commits](https://www.conventionalcommits.org/). Include a **list of changes** in the body:

```
<type>(<scope>): <subject>

- Change 1 (e.g. file or summary)
- Change 2
- ...
```

- **type**: `feat` | `fix` | `docs` | `chore` | `refactor` | `style` | `ci`
- **scope**: optional; use repo-appropriate scope (e.g. `docs`, `proxmox`, `core`, `media`, `docker`) when clear.
- **subject**: imperative, lowercase start, no period. ~50 chars.
- **body**: Include a bullet list of changes (files and/or logical edits). Keep lines concise.

## Response format (markdown, copy-pastable)

Structure your reply in markdown as follows:

1. **### List of changes** — A bullet list of what changed (path and short description per item).
2. **### Copy-pastable commit message** — A fenced code block (no language tag) containing only the raw commit message: subject line, blank line, then body with the same bullet list of changes. The user copies the *contents* of this block into `git commit` (e.g. `git commit -F -` and paste, or the commit message editor).

The code block must be plain text only (no markdown inside it) so it can be pasted directly as the commit message.

## Examples

**Staged: edits to `docs/Chapter2c-media.md`**
```
docs(media): expand media VM and stack documentation

- docs/Chapter2c-media.md — add Jellyfin, *arr stack, and NAS mounts sections
```

**Staged: new file in `proxmox/scripts/`**
```
feat(proxmox): add cloud-init script for template customization

- proxmox/scripts/setup-cloud-init.sh — new script
```

**Staged: fix in `docker_compose/core/compose.yml`**
```
fix(core): correct Traefik network name in compose

- docker_compose/core/compose.yml — fix network name
```

**Mixed: only docs changed**
```
docs: update Chapter1 and Chapter2 with hardware and VM notes

- docs/Chapter0-hardware.md — hardware list updates
- docs/Chapter2-vms.md — VM layout notes
```

## Repo-specific scopes

For this homelab repo, scopes often align with layout:

- `docs` — anything under `docs/`
- `proxmox` — `proxmox/` (scripts, snippets, templates)
- `core` | `media` | `monitoring` | `apps` — `docker_compose/<name>/`
- Omit scope if the change spans many areas or is generic (e.g. `chore: update README`).

## Notes

- If there are no changes (empty diff), say so and do not invent a message.
- If the user has only unstaged changes, suggest staging first or offer a message for the current working-tree diff and remind them to stage before committing.
