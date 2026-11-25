---
name: git-stash-parent-commit
description: Industrial protocol for obtaining the commit hash and subject line that was HEAD when a given Git stash was created.
category: Git & Repository Management
---

# Git Stash Parent Commit Skill (v1)

> **Skill ID:** `git-stash-parent-commit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

This skill provides a reliable, hang‑free way to determine the commit
that was HEAD at the moment a specific Git stash was created. Given a
stash reference (default `stash@{0}`), it outputs the commit hash and
subject line of the stash’s first parent (`<stash>^1`), which represents
the commit that was checked out when `git stash push` was run.

Knowing a stash’s origin commit is useful for:

- Triage decisions (e.g., deciding whether a stash is obsolete or
  belongs to a feature branch)
- Auditing stash provenance before applying or dropping
- Enriching stash inspection tables with contextual information

## When to Apply

Apply this skill when:

- You need to know the commit underlying a stash (e.g., during
  `git stash list` inspection)
- You are writing a skill or script that processes stashes and
  requires the parent commit for logic or display
- You want to avoid running `git show` directly on a stash in an
  agent‑driven terminal (which can invoke a pager and hang)

Do NOT apply when:

- You only need the stash’s diff or stat (use `git stash show -p
  --no-pager` etc.)
- You are in an interactive shell and prefer manual inspection

## Prerequisites

| Requirement | Minimum |
| --- | --- |
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ (or POSIX‑compliant shell for the base logic) |
| File system | Ability to create temporary files (optional, used by the script for error handling) |

## Operational Logic

The skill consists of a single PowerShell script that encapsulates the
core logic. The script:

1. Accepts an optional `-StashRef` parameter (string, default
   `stash@{0}`).
2. Executes `git -C <repo-path> rev-parse --verify "$StashRef^1"` to
   obtain the commit hash of the stash’s first parent.
   - If the stash reference is invalid or the parent does not exist,
     the script writes a clear error message to stderr and exits with
     code 1.
3. If the hash is obtained, runs `git -C <repo-path> show -s
   --format=%H:%s <hash>` to get the full hash and the subject line.
4. Outputs two lines to stdout:
   - Line 1: the commit hash (40‑hex SHA‑1)
   - Line 2: the commit subject (first line of the commit message)
   - Consumers can read the first line for machine‑only use, or both
     lines for human‑readable display.
5. The script uses `--no‑pager` implicitly by invoking `git` via `-C`
   and relying on PowerShell’s native pipeline; it never relies on a
   TTY pager.

### Example usage from PowerShell

```powershell
# Get the parent commit of the latest stash
& "$PSScriptRoot\../../git-stash-parent-commit/scripts/get-stash-parent.ps1"

# Get the parent commit of a named stash
& "$PSScriptRoot\../../git-stash-parent-commit/scripts/get-stash-parent.ps1" -StashRef stash@{1}
```

### Example output

```text
05c1be123064a2d40c2477414f94dfb6f9e41b6e
fix(paper-trading): clear only current tab persistence
```

## SSOT Compliance

This skill consumes — never duplicates — the following authoritative
rules:

- **Scripting language selection** — The provided script is
  PowerShell 7+ (`pwsh`) because its body IS shell glue (≤80 %
  native‑binary invocation in sequence): it primarily invokes `git`
  commands and processes their output, satisfying the Tier‑2 condition
  per [Scripting Language Selection Rules](../../../ai-agent-rules/scripting-language-selection-rules.md).
- **Markdown lint** — All markdown artifacts (this file, `AGENTS.md`)
  MUST be verified with `markdownlint-cli2` per [Markdown Generation
  Rules](../../../ai-agent-rules/markdown-generation-rules.md).
- **No‑embedded‑script mandate** — The script source lives in
  `scripts/get-stash-parent.ps1`; this markdown document only links to
  it.
- **Path portability** — The script resolves its own location via
  `$PSScriptRoot` and uses relative paths to invoke any dependencies
  (none in this case).
- **Redaction & portability** — Before committing, the skill MUST be
  run through the [Redaction & Portability Skill](../redaction-portability/SKILL.md)
  to replace any machine‑specific values with canonical placeholders.

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| --- | --- |
| [`git-stash-triage`](../git-stash-triage/SKILL.md) | Invoked for each stash reference discovered in Phase 0. The triage skill calls `scripts/get-stash-parent.ps1 -StashRef <ref>` to obtain the parent commit hash and subject line, which are then displayed in the verdict table to aid disposition decisions. |

## Anti‑Patterns

| Anti‑pattern | Why it’s wrong | Correct alternative |
| -------------- | ---------------- | --------------------- |
| `git stash show -p stash@{0}` in an agent terminal without `--no-pager` | Invokes a pager that hangs when no TTY is available | Use the script provided by this skill, which never relies on a pager |
| Parsing `git stash list` output with regex to extract commit info | Fragile; output format may change across Git versions | Use the plumbing commands `rev-parse` and `show` as done in the script |
| Assuming `stash@{0}^1` always exists without verification | May fail on corrupted stash or empty repo; leads to uncaught exceptions | The script verifies with `rev-parse --verify` and exits cleanly on error |

## Traceability

- Initial design driven by the conversation where the user requested
  to identify the commit from which a stash was created.
- The script logic is a direct transcription of the commands
  discussed: `git -C <repo> rev-parse --verify stash@{0}^1` followed by
  `git -C <repo> show -s --format=%H:%s <hash>`.

---
<!-- Generated by the Skill Factory (skill-factory v1) -->