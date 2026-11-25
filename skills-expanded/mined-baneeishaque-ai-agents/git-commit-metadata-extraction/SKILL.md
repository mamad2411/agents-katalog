---
name: git-commit-metadata-extraction
description: A universal primitive for extracting complete commit metadata from any Git commit — parent SHA(s), commit message, file changes with add/modify/delete classification, author, and committer.
category: Git & Repository Management
---

# Git Commit Metadata Extraction Skill

> **Skill ID:** `git_commit_metadata_extraction`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A self-contained universal extraction primitive that retrieves full commit metadata from any Git repository at a given SHA. It produces a structured record containing every field required by industrial commit message formats and analytical audit skills:

- Commit target SHA
- Parent commit(s) — with merge detection
- Full commit message body
- File changes — additions, deletions, and per-file classification (added / modified / deleted)
- Author name, email, and timestamp
- Committer name, email, and timestamp

This skill is a **reusable foundational primitive**. It is called by:

- [`git_submodule_commit_details`](../git-submodule-commit-details/SKILL.md) — to extract the raw data for submodule pointer commits
- [`git_commit_details_audit`](../git-commit-details-audit/SKILL.md) — to gather the raw facts before applying a pedagogical analysis

***

## Environment & Dependencies

The agent MUST autonomously verify the availability of required tools before executing extraction:

- **Git**: Verified via `which git` (Minimum v2.x+).
- **PAGER**: All Git commands MUST be prepended with `GIT_PAGER=cat` to prevent terminal pagers (`less`, `more`) from hanging the agent execution.

***

## When to Apply

Apply this skill when:
- Any consumer skill needs structured, high-fidelity commit data.
- Auditing what a commit contains.

Do NOT apply when:
- The target SHA does not exist locally (the agent must fetch first).

***

## Step-by-Step Procedure

### Step 1 — Extract Core Commit Metadata

Run the following single command against the repository. It retrieves all metadata fields in a deterministic order:

```bash
GIT_PAGER=cat git -C <repo-path> log \
  --format=format:"%P%n%an <%ae>%n%ad%n%cn <%ce>%n%cd%n%B" \
  <commit-sha> -1
```

**Pedagogical Command Breakdown:**
- `GIT_PAGER=cat`: Suppresses interactive pagination.
- `git -C <repo-path>`: Safely targets the repository without requiring a stateful `cd` command.
- `log`: The core Git command to show commit logs.
- `--format=format:"..."`: Uses the "tformat" (terminator format) — every record is terminated, avoiding trailing newline issues.
- `-1`: Limits output to exactly one commit. Without this, it would walk the entire ancestry.

**Pedagogical Breakdown — Format Placeholders:**
| Placeholder | Field | Notes |
| :--- | :--- | :--- |
| `%P` | Parent SHA(s) | Space-separated; two SHAs = merge commit |
| `%an <%ae>` | Author name + email | Human who wrote the change |
| `%ad` | Author date | When the change was authored |
| `%cn <%ce>` | Committer name + email | Who applied the commit (may be CI/automation) |
| `%cd` | Committer date | When the commit was recorded in history |
| `%B` | Full commit message body | Title + blank line + body paragraphs |

**Merge Commit Detection:**
If `%P` returns two SHAs (space-separated), the commit is a merge. Record both parents.

---

### Step 2 — Extract File Changes with Line Counts

```bash
GIT_PAGER=cat git -C <repo-path> diff-tree \
  --no-commit-id -r --numstat <commit-sha>
```

**Pedagogical Command Breakdown:**
- `diff-tree`: Compares the tree of the given commit against its parent.
- `--no-commit-id`: Suppresses the leading commit SHA line, keeping output to exactly one line per changed file.
- `-r`: Recurse into subdirectories so file paths appear fully qualified.
- `--numstat`: Emits tab-separated `<additions>\t<deletions>\t<filepath>` (machine-readable, no ANSI color codes).

**For merge commits** — use the two-parent diff instead:

```bash
GIT_PAGER=cat git -C <repo-path> diff <parent1> <parent2> --stat
```

---

### Step 3 — Classify Each File as Added / Modified / Deleted

For every file returned by Step 2, determine its change type by checking whether it existed in the **parent commit's tree**:

```bash
GIT_PAGER=cat git -C <repo-path> ls-tree -r <parent-sha> \
  | grep <filename>
```

**Pedagogical Command Breakdown:**
- `ls-tree -r`: Lists every tracked file in the parent commit's tree recursively.
- `grep <filename>`: Isolates the specific file entry. If found, it existed in the parent.

**Classification Rules:**
| Condition | Classification |
| :--- | :--- |
| File found in parent tree | `modified` |
| File NOT found in parent tree | `added` |
| File in parent tree but NOT in current commit | `deleted` |

**For merge commits** — compare against `<parent1>` (the base branch).

---

### Step 4 — Assemble the Structured Record

Combine all extracted fields into the canonical output format used by consumer skills:

```
Commit: <commit-sha>
Commit parent: <parent-sha>
  (merge: <parent1> <parent2>  ← only if merge commit)
Commit msg: <title-line>

<body-paragraphs-if-multiline>

Commit changes:
  <filepath> | <additions> insertions(<classification>)
  <filepath> | <additions> insertions, <deletions> deletions(<classification>)
  ...
Commit author: <author-name> <author-email>
Commit author time: <author-date>
Commit committer: <committer-name> <committer-email>
Commit committer time: <committer-date>
```

**Formatting Rules:**
- Consumer skills may substitute "Commit:" with context-specific prefixes (e.g., "Submodule: <submodule-name> -> <commit-sha>").
- Use `(added)`, `(modified)`, or `(deleted)` as the classification suffix — never abbreviate.
- Do NOT summarize the commit body — **Zero Omission** is mandatory.

***

## Output Contract

This skill MUST produce one structured record per SHA requested. The record is consumed verbatim by the caller.

***

## Prohibited Behaviors

The agent **IS BLOCKED** from:
- Summarizing or paraphrasing the commit message body.
- Skipping the file classification step (add / modify / delete).
- Confusing author timestamp with committer timestamp.
- Running `git log` without `-1` and accidentally reading multiple commits.

***

## Traceability

- **Industrialized from:** Session `502cbc0b-a723-48ab-a7f6-698dff812c9a` — Refactoring Git Commit Extraction into a Universal Primitive.
- **Rule source:** [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md)
- **Extracted from:** Initial isolation of `git_submodule_commit_details` to enforce universal primitive architectures.
