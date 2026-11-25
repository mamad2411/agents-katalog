---
name: git-submodule-commit-details
description: Extract complete commit metadata from a Git submodule by orchestrating the universal git_commit_metadata_extraction primitive, resolving submodule paths, and retrieving registration URLs for parent sync messages.
category: Git & Repository Management
---

# Git Submodule Commit Details Skill

> **Skill ID:** `git-submodule-commit-details`<br>
> **Version:** 2.1.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A specialized skill that prepares commit metadata from a Git submodule for use in parent repository commit messages or audit reports. 

Instead of performing raw extraction itself, this skill orchestrates the **[Git Commit Metadata Extraction](../git-commit-metadata-extraction/SKILL.md)** primitive. It provides the necessary submodule context (path resolution, registration URL) and formats the output into the industrial standard required for submodule syncs.

This skill is called by:

- [`git_submodule_commit_reword`](../git-submodule-commit-reword/SKILL.md)
  — to compose amended commit messages
- [`git_atomic_commit`](../git-atomic-commit-construction/SKILL.md)
  — to compose descriptive submodule sync commit messages

## Prerequisites

| Requirement | Minimum |
| :--- | :--- |
| VCS | Git 2.x+ |
| Shell | Bash 4+ |
| Access | Read access to the submodule repository |

## When to Apply

Apply this skill when:
- Composing a parent-repo commit message that syncs a submodule pointer
- Rewording a submodule addition commit to include full metadata

Do NOT apply when:
- The submodule path is not initialized — run `git submodule update --init` first

---

## Step-by-Step Procedure

### Step 1 — Resolve Submodule Path and Target SHA

#### 1a — Discover the Current Pointer (if not already known)

Use `git ls-tree` to obtain the submodule path and the SHA it currently points to in the parent repository's tree:

```bash
GIT_PAGER=cat git -C <parent-repo-path> ls-tree HEAD <submodule-name>
```

**Output format:**
```
160000 commit <submodule-sha>    <submodule-name>
```

#### 1b — Determine the Chronological Range
If syncing from a previous pointer, the caller MUST provide the previous SHA to determine the range of commits.

#### 1c — Extract Commit Log for the Range
Get the chronological list of commits between old and new SHAs:

```bash
git -C <submodule-path> log <old-sha>..<new-sha> --oneline
```

This enables the format: `Changes (<submodule-name>) [<old-sha>..<new-sha>]:`

---

### Step 2 — Resolve Registration URL

Read `.gitmodules` in the **parent repository** to obtain the remote URL for the submodule:

```bash
GIT_PAGER=cat git -C <parent-repo-path> config \
  --file .gitmodules submodule.<submodule-name>.url
```

---

### Step 3 — Extract Raw Metadata

Execute the **[Git Commit Metadata Extraction](../git-commit-metadata-extraction/SKILL.md)** primitive on the `<submodule-sha>` within the submodule directory. 

*Do not attempt to manually extract data; rely entirely on the primitive to ensure zero-omission extraction and correct file classifications.*

---

### Step 4 — Assemble the Submodule Sync Record

Take the generic structured record produced by the extraction primitive in Step 3 and apply the submodule-specific formatting.

1. Use the `Changes (<submodule-name>):` header for the chronological log.
2. Use the `Metadata (<submodule-name>):` header for the structured fields.
3. Append the registration URL block at the end.

**Required Format:**
```
chore(submodules): sync <submodule-name> with <descriptive-action>

Updates <submodule-name> from <old-sha-short> to <new-sha-short> (<head-commit-title>)

Changes (<submodule-name>) [<old-sha>..<new-sha>]:
- <chronological-commit-list-older-to-newer>

Metadata (<submodule-name>):
Submodule: <submodule-name> -> <submodule-sha>
Submodule commit parent: <parent-sha>
  (merge: <parent1> <parent2>  ← only if merge commit)
Submodule commit msg: <title-line>

<body-paragraphs-if-multiline>

Submodule commit changes:
   | <additions> insertions(<classification>)
   | <additions> insertions, <deletions> deletions(<classification>)
  ...
Submodule commit author: <author-name> <author-email>
Submodule commit author time: <author-date>
Submodule commit committer: <committer-name> <committer-email>
Submodule commit committer time: <committer-date>

Register <submodule-name> submodule pointing to <registration-url>
```

**First Line Guidance:**
- Use format: `chore(submodules): sync <submodule-name> with <action>`
- Include a descriptive action that summarizes the changes (e.g., "with swaps PNL updates", "with build artifact cleanup", "with price data updates")

---

## Output Contract

This skill MUST produce one structured record per submodule SHA requested. The record is consumed verbatim by the caller.

---

## Prohibited Behaviors

The agent **IS BLOCKED** from:
- Attempting to bypass the `git_commit_metadata_extraction` primitive by writing custom extraction bash commands.
- Summarizing or paraphrasing the submodule commit message body.
- Omitting the `.gitmodules` registration URL.

---

## Related Skills

- [`git_commit_metadata_extraction`](../git-commit-metadata-extraction/SKILL.md)
  — The underlying foundational primitive.
- [`git_submodule_commit_reword`](../git-submodule-commit-reword/SKILL.md)
- [`git_atomic_commit`](../git-atomic-commit-construction/SKILL.md)

---

## Traceability

- **Updated to v2.1.0:** Session based on submodule sync commits in oleovista-acers - Added range notation and first line guidance.
- **Refactored in:** Session `502cbc0b-a723-48ab-a7f6-698dff812c9a` to delegate raw extraction to the universal primitive `git_commit_metadata_extraction`.
- **Formatting Authority:** [`git-commit-message-rules.md#5-submodule-sync-commits-parent-repository`](../../../ai-agent-rules/git-commit-message-rules.md#5-submodule-sync-commits-parent-repository)
