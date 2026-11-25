---
name: untracked-scratch-triage
description: Triage untracked files that appear in a working tree after a commit operation — classify origin (current-repo work / cross-repo scratch / tool artifact / credential leak), then dispose via delete / local-exclude / shared-ignore / commit.
category: Code Hygiene & Maintenance
---

# Untracked Scratch Triage Skill

> **Skill ID:** `untracked-scratch-triage`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

After completing an atomic commit (or at any audit point), `git status`
often still lists untracked files whose origin is unclear: scratch diff
dumps, tool log files, captured `gh` output, dropped command-output
pipes, or artifacts written by a *different* repo's session into the
*current* repo's working tree.

This skill is the disposition primitive: classify each untracked file by
**content**, **origin**, and **risk**, then choose one of four exits —
**delete**, **local-exclude** (`.git/info/exclude`), **shared-ignore**
(`.gitignore`, committed), or **commit** (it actually belongs here).

It complements rather than overlaps:

- [deleted-files-audit](../deleted-files-audit/SKILL.md) — handles
  *deletions*, not untracked leftovers.
- [gitignore-rules](../gitignore-rules/SKILL.md) — authors ignore
  patterns; this skill *decides* whether a pattern is warranted.
- [git-post-gitignore-untrack](../git-post-gitignore-untrack/SKILL.md)
  — handles tracked files that newly-added ignore rules should drop;
  this skill handles never-tracked files instead.
- [git-atomic-commit-construction](../git-atomic-commit-construction/SKILL.md)
  Step 1f mandates listing untracked files in the inventory; this skill
  is what to invoke when that list contains "what is this?" entries.

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Access | Read access to the working tree |

## When to Apply

Apply when:

- After an atomic commit, `git status` still shows untracked entries.
- A working tree contains files whose origin the user cannot immediately
  explain.
- Bulk untracked files appear (e.g. `*.log`, `*.tmp`, `.gh_*`,
  `nohup.out`, `core.*`).
- A user asks "what about the leftover files?" or "what are these for?".

Do NOT apply when:

- The untracked file is a known in-progress edit (the user is mid-task).
- The file is already covered by an existing `.gitignore` rule (it
  wouldn't appear in `git status`).
- The pending change is a *deletion* — use
  [deleted-files-audit](../deleted-files-audit/SKILL.md).

---

## Step-by-Step Procedure

### Step 1 — Enumerate Untracked Files

```powershell
git -C <repo> ls-files --others --exclude-standard
```

```bash
git -C <repo> ls-files --others --exclude-standard
```

> `--others` selects untracked files; `--exclude-standard` honors
> `.gitignore`, `.git/info/exclude`, and global excludes, so output is
> exactly what appears in `git status` as `??`.

### Step 2 — Capture Metadata

For each entry, capture size, mtime, and first ~40 lines:

```powershell
Get-ChildItem <file> | Select-Object Name, Length, LastWriteTime
Get-Content <file> -TotalCount 40
```

```bash
ls -l <file>
head -n 40 <file>
```

> Hex preview (`Format-Hex <file> -Count 256` / `xxd | head`) is the
> fallback for binary files.

### Step 3 — Classify Each File (5-Bucket Rubric)

Place every file in exactly one bucket. Pick the **highest-severity**
match when a file fits more than one.

| Bucket | Diagnostic signal | Default disposition |
|---|---|---|
| **A. Credential / Secret leak** | Contains `ghp_`, `github_pat_`, `BEGIN PRIVATE KEY`, `password=`, `AWS_SECRET_`, JWT, bearer tokens, `.env` with values | **Delete immediately** + warn user. Add pattern to **shared-ignore**. NEVER `git add`. Rotate the secret. |
| **B. Cross-repo scratch** | Content references paths, files, or commits that belong to a *different* repository (e.g., a diff of `ai-agents/.agents/skills/...` found in an unrelated project) | **Delete**. Optionally add a `.git/info/exclude` rule if the user repeatedly redirects output here. |
| **C. Tool / IDE artifact** | Matches a well-known pattern: `*.log`, `*.tmp`, `nohup.out`, `core.*`, `*.swp`, `__pycache__/`, `.DS_Store`, `Thumbs.db`, IDE state files | **Shared-ignore** (`.gitignore`, committed) if the project lacks the pattern; otherwise **delete**. |
| **D. Current-repo work-in-progress** | Content directly relates to a tracked file in this repo; appears intentional | **Commit** (use [git-atomic-commit-construction](../git-atomic-commit-construction/SKILL.md)) or **leave** untouched if explicitly mid-edit. |
| **E. Unknown / undecidable** | Cannot determine origin from content | **Ask user**. Default to local-exclude until classified — never silent-delete. |

### Step 4 — Cross-Repo Detection Heuristics

Bucket B is the most overlooked case. Use any of:

1. **Absolute paths inside the file** that point outside the current
   repo's directory tree.
2. **Diff headers** (`diff --git a/<path> b/<path>`) where `<path>` does
   not exist in `git ls-files` of the current repo.
3. **Commit SHAs** the user can `git -C <other-repo> show <sha>` against
   another known repo but `git -C <this-repo> cat-file -e <sha>^{commit}`
   fails.
4. **Filename prefix** the user typed in another session
   (`.gh_*`, `_diff_*`, `_compare_*`) combined with content unrelated to
   this repo's domain.

Cross-repo scratch is almost always a redirection that landed in the
wrong `cwd`. The data is not lost — it can be regenerated, or it
already exists committed in the source repo.

### Step 5 — Choose the Disposition

Present the user with a verdict table:

| File | Bucket | Proposed disposition | Justification |
|---|---|---|---|
| `.gh_auth_diff.txt` | B | Delete | Diff of `ai-agents` skill file, not this repo |
| `nohup.out` | C | Add `nohup.out` to `.gitignore`, then delete | Tool artifact universally ignored |
| `secrets.env` | A | Delete + warn user + rotate | Contains `GITHUB_TOKEN=ghp_…` |

Then request **explicit authorization** per disposition:

- **Delete** — list exact `Remove-Item` / `rm` commands; never bulk-rm a
  directory without per-file confirmation.
- **Local-exclude** — append the pattern to
  `<repo>/.git/info/exclude` (workspace-private, not committed). Use
  when the noise is *yours* and the team doesn't need the rule.
- **Shared-ignore** — append the pattern to the tracked
  `<repo>/.gitignore`. Follow with a dedicated
  `chore(gitignore): ignore <pattern>` commit per the
  [git-atomic-commit-construction](../git-atomic-commit-construction/SKILL.md)
  Configuration Coupling rule (Step 5). Use when the noise will
  recur for *anyone* on the team.
- **Commit** — hand off to
  [git-atomic-commit-construction](../git-atomic-commit-construction/SKILL.md).

### Step 6 — Execute & Verify

After authorized disposition:

```powershell
git -C <repo> status --short
```

Expect a clean tree (or only the files the user explicitly chose to
leave). Re-run Step 1 to confirm no new entries appeared during
execution.

---

## Disposition Decision Tree

```
Is content a credential / secret?
├── YES → Bucket A → Delete + warn + rotate + shared-ignore the pattern
└── NO
    ├── Does content reference a different repo's files / commits?
    │   ├── YES → Bucket B → Delete (optional local-exclude)
    │   └── NO
    │       ├── Is it a well-known tool / IDE artifact?
    │       │   ├── YES → Bucket C → Shared-ignore (commit) + delete
    │       │   └── NO
    │       │       ├── Does it relate to current tracked work?
    │       │       │   ├── YES → Bucket D → Commit or leave
    │       │       │   └── NO → Bucket E → Ask user
```

---

## Anti-Patterns (Forbidden)

- ❌ `Remove-Item *` / `rm -rf` on the working tree without per-file
  classification — risks deleting Bucket D (real work).
- ❌ `git add .` to "make `git status` quiet" — risks committing Bucket
  A (secrets) or Bucket B (foreign scratch).
- ❌ Silent deletion of any file whose content was not inspected.
- ❌ Adding broad patterns (`*.txt`, `*.log`, `tmp/`) to the shared
  `.gitignore` without checking they don't shadow tracked files. Use
  [git-post-gitignore-untrack](../git-post-gitignore-untrack/SKILL.md)
  if they do.
- ❌ Leaving Bucket-A leaks in the working tree once detected — even
  unstaged secrets are at risk of accidental `git add -A` later.

---

## Worked Example (sanitized)

After committing four coupled files for a new validation constraint,
`git status` still listed:

```
?? .gh_auth_diff.txt
?? .gh_rest_diff.txt
```

Step 2 inspection showed both contained `diff --git a/.agents/skills/…`
headers referencing skill files in a sibling `ai-agents` repository
(not this repo's tree). Classification: **Bucket B (cross-repo scratch)**
— almost certainly the output of a `git diff > file` command issued
from the wrong `cwd` in a prior session, with the original changes
already committed upstream in the source repo.

Disposition options offered:

- (a) delete only,
- (b) delete + `.git/info/exclude` rule for `.gh_*.txt`,
- (c) delete + tracked `.gitignore` rule with its own
  `chore(gitignore)` commit.

User chose (a). Execution: `Remove-Item .gh_auth_diff.txt,
.gh_rest_diff.txt`. Verification: `git status --short` returned empty.

---

## Related Skills

- [git-atomic-commit-construction](../git-atomic-commit-construction/SKILL.md)
  — invoke this skill when its Step 1f inventory contains untracked
  files of unclear origin.
- [deleted-files-audit](../deleted-files-audit/SKILL.md) — the
  symmetric counterpart for *deletions*.
- [gitignore-rules](../gitignore-rules/SKILL.md) — once a Bucket-C
  pattern is identified, this skill authors the rule correctly.
- [git-post-gitignore-untrack](../git-post-gitignore-untrack/SKILL.md)
  — if the ignore rule chosen in Step 5 would shadow an already-tracked
  file.
- [redaction-portability](../redaction-portability/SKILL.md) — Bucket-A
  classification follows the Tier-A identity / credential definitions
  there.

---

## Traceability

- Skill authored: 2026-05-16.
