---
name: git-drop-commit-with-divergent-recreation
description: Composer — safely drop a commit that deletes file X when a
    later commit re-creates X from a stale copy that has DIVERGED from
    the deleted version (each side carrying unique content). Performs
    section-by-section blob comparison, hand-builds a union blob during
    the add/add rebase conflict, enforces byte-preserving file restoration,
    and routes around the silent `git commit --amend`-during-rebase
    pitfall that folds the conflict-resolved content into the wrong
    commit.
category: Git & Repository Management
---

# Git Drop Commit With Divergent Recreation Skill (v1)

> **Skill ID:** `git-drop-commit-with-divergent-recreation`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

The user wants to drop commit `<A>` (typically a meaningless "Final
Changes" / "WIP" deletion of file `<X>`) from a branch. A later commit
`<B>` on the same branch re-creates `<X>` — but from a **stale copy**.
The deleted blob and the recreated blob have **diverged**: each carries
unique sections the other lacks. A naive
`git rebase -i <A>~1` + drop will:

1. Trigger an `add/add` conflict on `<X>` at `<B>`.
2. Tempt the agent to resolve "ours" or "theirs" — either choice
   **silently loses** unique content from the opposite side.
3. Tempt the agent to write the merged file via `Out-File` /
   `Set-Content` on Windows — which silently mangles bytes and
   breaks `git hash-object` parity.
4. Tempt the agent to `git commit --amend` after the conflict-resolved
   `git add` — which silently rewrites the **previously applied
   commit** (HEAD), folding the conflict-resolved blob into the wrong
   commit and causing `git rebase --continue` to skip `<B>`.

This skill walks the agent through the safe sequence: classify the
divergence, build the union blob byte-exactly, complete the rebase
without amending HEAD, and verify with a bidirectional cherry +
per-file blob-hash audit before pushing.

## When to Apply

Apply this skill when **ALL** of the following hold:

1. The drop target `<A>` deletes one or more files.
2. A later commit `<B>` reachable from the same tip re-creates at
   least one of those files.
3. The pre-deletion blob (`<A>^:<X>`) and the recreated blob
   (`<B>:<X>` or `HEAD:<X>`) differ — confirmed by
   `git diff --stat <A>^:<X> HEAD:<X>` showing non-zero changes.
4. Section-by-section inspection (headings, version banners, key
   anchor lines) shows **neither blob is a superset** — each carries
   unique content.

If condition 3 is false (blobs identical), this is a no-op cleanup —
use [`git-commit-edit`](../git-commit-edit/SKILL.md) directly with
`drop` action.

If conditions 3 holds but condition 4 is false (one side is a
superset), the conflict is a trivial "take the superset side" — use
[`git-commit-edit`](../git-commit-edit/SKILL.md) `drop` + manual
resolution, no full composer needed.

## Composition Rationale

This skill is a **composer**. It orchestrates the following primitives
without reimplementing them:

| Composed Skill | Used for |
|---|---|
| [`git-commit-edit`](../git-commit-edit/SKILL.md) | Backup branch creation, sequence-editor script, rebase mechanics, descendant replay |
| [`near-duplicate-file-comparison`](../near-duplicate-file-comparison/SKILL.md) | Section-by-section divergence rubric applied to two blob versions |
| [`git-personal-sandbox-restack`](../git-personal-sandbox-restack/SKILL.md) §3 | Six-axis equality audit (patch-id, tree, file-set, per-file bytes) reused as the post-rebase verification |
| [`git-divergence-audit`](../git-divergence-audit/SKILL.md) | Optional pre-flight branch divergence check before the drop |

The composer **MUST NOT** reimplement rebase mechanics, blob
comparison heuristics, or audit primitives — those belong to the
owners listed above.

## Source Rules

| Rule File | Scope Incorporated |
|---|---|
| [`ai-rule-standardization-rules.md`](../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate |
| [`script-management-rules.md`](../../../ai-agent-rules/script-management-rules.md) | PowerShell sequence-editor authoring |

---

## Step-by-Step Procedure

### Step 1 — Pre-Flight: Confirm the Divergent-Recreation Pattern

Before any destructive action, the agent **MUST** prove the pattern
applies.

#### 1a — Identify the drop target and recreation commit(s)

```powershell
# What files does <A> touch?
git show --name-only <A>

# Which later commits touch the same files?
git log --oneline <A>..HEAD -- <path-to-X>
```

The output of the second command, ordered oldest-to-newest, IS the
recreation chain. The first entry that **adds** `<X>` (mode `100644`
in `--diff-filter=A`) is `<B>`.

#### 1b — Confirm the blobs diverge

```powershell
$preDelete = git rev-parse "<A>^:<path-to-X>"
$current   = git rev-parse "HEAD:<path-to-X>"
git diff --stat "$preDelete" "$current"
```

If the diff is empty (blobs identical), abort this composer and use
[`git-commit-edit`](../git-commit-edit/SKILL.md) `drop` directly.

#### 1c — Apply the divergence rubric

Run the [`near-duplicate-file-comparison`](../near-duplicate-file-comparison/SKILL.md)
eight-dimension rubric (adapted to two blob versions) against
`$preDelete` and `$current`. Focus on:

- **Version banner / header** — does either explicitly declare a
  newer/older version?
- **Section headings** — extract with `Select-String '^#+ '` on each
  blob and diff the two heading sets.
- **Key anchor lines** — algorithm bullets, table rows, code-fence
  language tags.

Produce a verdict table:

| Section | Pre-delete (`<A>^`) | Current (`HEAD`) |
|---|---|---|
| Version banner | <v?.?.?> | <v?.?.?> |
| Lines / bytes | <n> / <n> | <n> / <n> |
| Unique section #1 | present / **missing** | present / **missing** |
| Unique section #2 | present / **missing** | present / **missing** |

**Verdict gate**: If **both** columns have at least one cell saying
"present" against a cell saying "missing", divergence is confirmed —
proceed. Otherwise, downgrade to plain `git-commit-edit drop`.

### Step 2 — Design the Union Blob

Plan **before** touching git.

#### 2a — Decide the merge strategy per file

For each file `<X>`, choose ONE of:

1. **Union splice** — splice unique sections from one blob into the
   other (preserving the section the other lacks). Default choice.
2. **Selective union** — take some unique sections, drop others (e.g.,
   if one side is obsolete by intent). Document the rationale.
3. **Replace with current** — adopt the current blob verbatim and
   declare the pre-delete unique content obsolete. Used only when the
   user explicitly says so.

#### 2b — Decide the version banner

If the file is a versioned artifact (skill, doc, library), the merged
blob's version banner **MUST** be bumped to a value strictly greater
than BOTH inputs. Convention: `Vmax(major).max(minor)+1.0`.

#### 2c — Author a merged-commit message draft

The message of `<B>` (the recreation commit) will be retained after
the rebase. Reword it to reflect that it now carries the union, the
restored content, **and** an explicit mention of the dropped `<A>`.
See [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md)
for the project's commit-message rules.

### Step 3 — Backup

```powershell
git branch backup/sandbox-pre-drop-recreate-<YYYY-MM-DD>
```

Use the `backup/<branch>-pre-<purpose>-<date>` convention from the
project's backup-naming rule. **Mandatory** — this skill's audit
(Step 7) depends on the backup branch existing.

### Step 4 — Build the Union Blob Byte-Exactly

Author the merged blob **before** starting the rebase. Use a real
programming language (Python preferred) or `[System.IO.File]::WriteAllBytes`
in PowerShell — **NOT** `Out-File` / `Set-Content`. Verify with
`git hash-object` immediately after writing.

Reference Python pattern:

```python
import subprocess
from pathlib import Path

REPO = r"<repo-path>"
PRE_BLOB  = "<sha-of-pre-delete-blob>"
CURR_BLOB = "<sha-of-current-blob>"
OUT       = Path(r"<scratch-path>/merged-X")

def cat(sha):
    return subprocess.run(
        ["git", "-C", REPO, "cat-file", "-p", sha],
        check=True, capture_output=True,
    ).stdout.decode("utf-8")

pre  = cat(PRE_BLOB)
curr = cat(CURR_BLOB)

# Splice unique section from <curr> into <pre> before <anchor>.
anchor = "## <next-section-after-insertion-point>"
unique_start = curr.find("## <unique-section-heading>")
unique_end   = curr.find(anchor, unique_start)
unique       = curr[unique_start:unique_end]

splice_at = pre.find(anchor)
merged    = pre[:splice_at] + unique + pre[splice_at:]

# Bump version banner.
merged = merged.replace("> **Version:** <old>", "> **Version:** <new>")

OUT.write_bytes(merged.encode("utf-8"))
```

PowerShell byte-preserving fallback (if Python is unavailable):

```powershell
$bytes  = [System.IO.File]::ReadAllBytes($source)
$text   = [System.Text.Encoding]::UTF8.GetString($bytes)
$merged = $text.Replace($old, $new)
[System.IO.File]::WriteAllBytes($dest, [System.Text.Encoding]::UTF8.GetBytes($merged))
```

**Verify**:

```powershell
git hash-object <scratch-path>/merged-X
```

Record the expected hash for use in Step 5.

### Step 5 — Execute the Drop via git-commit-edit

Author a sequence-editor script that **drops** `<A>`. Delegate to
[`git-commit-edit`](../git-commit-edit/SKILL.md) Steps 1–6 for the
rebase mechanics.

Expected outcome: rebase stops on `<B>` with an `add/add` conflict
on `<X>`. The agent **MUST NOT** proceed with default conflict
resolution — go to Step 6.

### Step 6 — Resolve the Conflict (Critical Sequence)

This is the step where Lesson 2 silently corrupts history if
mis-executed. Follow this **EXACT** sequence:

#### 6a — Install the union blob byte-exactly

```powershell
Copy-Item <scratch-path>/merged-X <path-to-X> -Force
```

`Copy-Item` is byte-preserving on Windows. **DO NOT** use
`Out-File`, `Set-Content`, or `> $path` redirection — they all
re-encode (BOM, line-ending normalization, UTF-8 mangling) and
break blob-hash parity.

#### 6b — Verify byte-exactness

```powershell
git hash-object <path-to-X>
# MUST match the hash recorded in Step 4.
```

If the hash differs, the file got re-encoded — abort the rebase
(`git rebase --abort`) and restart from Step 5 with a fresh
byte-preserving write.

#### 6c — Stage the resolution

```powershell
git add <path-to-X>
git status --short
# Expected: 'M  <path-to-X>' (no UU markers anywhere)
```

#### 6d — Continue the rebase (NEVER amend)

```powershell
# Author + commit dates of <B> are auto-preserved by --continue.
$env:GIT_EDITOR='true'
git rebase --continue
```

`--continue` creates a **new commit** with `<B>`'s original message
and metadata, containing the union-resolved blob. This is the
correct path.

**FORBIDDEN sequence**: `git commit --amend -F <msg>` after
Step 6c. This rewrites HEAD (the **previously applied** commit, not
`<B>`), silently folds the staged union blob into the wrong commit,
and the next `git rebase --continue` skips `<B>` because there is no
remaining diff. Recovery is a second `rebase -i edit <mega-commit>`
+ `git reset HEAD~` + per-file atomic re-commits with
`GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` env vars restored from the
originals — a costly second round trip.

#### 6e — Reword the new commit (if needed)

To replace `<B>`'s message with the draft from Step 2c, run a
**second** `rebase -i` with `reword` after the current rebase
completes — do NOT use `--amend` mid-rebase.

```powershell
git rebase -i HEAD~<n>   # mark the new <B>-equivalent as 'reword'
```

Or delegate to [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md).

### Step 7 — Post-Rebase Audit (MANDATORY before push)

Before any force-push, run the full audit. This catches Step 6
mistakes **before** the backup is deleted.

#### 7a — Tree parity

```powershell
$bTree = git rev-parse 'backup/<...>^{tree}'
$nTree = git rev-parse 'HEAD^{tree}'
"backup tree: $bTree`nnew    tree: $nTree`nmatch      : $($bTree -eq $nTree)"
```

Expected: **mismatch** (we intentionally changed `<X>`'s content).

#### 7b — File-level diff at tips

```powershell
git diff --stat backup/<...> HEAD
```

Expected: **only** `<X>` listed (or the files in Step 2's union
plan). Any unexpected file means a Step 6 mistake — investigate
before pushing.

#### 7c — Bidirectional cherry audit

```powershell
git cherry HEAD backup/<...> | Where-Object { $_ -like '+ *' }
git cherry backup/<...> HEAD | Where-Object { $_ -like '+ *' }
```

Expected unique-to-backup: **only** the dropped `<A>` SHA, plus
`<B>` (because `<B>` was reapplied under a new SHA with a different
trailing blob).

Expected unique-to-new: **only** the new `<B>`-equivalent SHA.

If a commit OTHER than `<A>` / `<B>` appears as unique-to-backup,
the rebase silently absorbed it into a mega-commit — execute the
recovery from Step 6d FORBIDDEN-sequence note.

#### 7d — Per-file blob-hash conservation (Lesson 4 deep layer)

For each file `<F>` that was NOT in the union plan (i.e., should be
byte-identical between backup and new tip):

```powershell
$b = git rev-parse "backup/<...>:$F"
$n = git rev-parse "HEAD:$F"
if ($b -ne $n) { Write-Host "[DIFF] $F  backup=$b  new=$n" }
```

Expected output: empty (every non-target file's blob is preserved).

### Step 8 — Authorized Force-Push

ONLY after Step 7 passes:

```powershell
git push --force-with-lease <remote> <branch>
```

`--force-with-lease` (not `--force`) prevents overwriting any
remote commit the agent has not seen.

### Step 9 — Cleanup

After the user confirms the push landed correctly:

```powershell
git branch -D backup/<...>
```

Scratch files (Python splicer, intermediate sequence-editor
scripts, merged blob staging) under `<scratch-path>` MAY be deleted.

---

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Resolved conflict with "ours" or "theirs" | Auto-choices silently lose the OTHER side's unique content. Step 1c rubric is mandatory; if both sides have uniques, union splice is the ONLY safe path. |
| Wrote merged blob with `Out-File` / `Set-Content` | Adds BOM and / or normalizes line endings; `git hash-object` parity breaks. Use `Copy-Item -Force` (from a byte-preserving source) or `[System.IO.File]::WriteAllBytes`. Always verify hash before `git add`. |
| `git commit --amend -F <msg>` mid-rebase after `git add` | Silently rewrites HEAD (the previously applied commit), folds the union blob into the wrong commit, next `--continue` skips the conflicted commit. Use `git rebase --continue` directly; reword via a second `rebase -i reword`. |
| Skipped Step 7 audit, pushed, then deleted backup | The mega-commit-folding mistake (above) becomes effectively irrecoverable. Step 7 is **non-negotiable** before push. |
| Forgot to bump version banner in merged blob | The new tip claims to be the older version, downstream consumers may regress. Step 2b is mandatory for versioned artifacts. |
| Reused `<B>`'s original message verbatim | The new commit is now substantively different (carries restored sections + the drop's intent). Reword via Step 6e. |
| Defender / IDE file-lock during `Copy-Item` | Pipe `$yes = (("y`n") * 500) -join ''; $yes \| <cmd>` per the project's retry pattern, or temporarily exclude the scratch path. |

---

## Composition by Higher-Level Skills

Skills that may invoke this composer for a domain-specific
delete-then-recreate cleanup:

| Composer | Purpose |
|---|---|
| (none yet) | First adopter — register here when added. |

---

## Related Skills

- [`git-history-refinement`](../git-history-refinement/SKILL.md) —
  the broader sibling for full history reconstruction; use this
  skill when the scope is a single divergent-recreation drop.
- [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md)
  — for Step 6e reword after the rebase completes.

---

## Environment & Dependencies

- **Git** — `git --version` (≥ 2.30 for `--force-with-lease` reliability).
- **PowerShell** — Windows PowerShell 5.1 OR PowerShell Core 7+ for
  `[System.IO.File]::WriteAllBytes` and `Copy-Item -Force`.
- **Python (optional but preferred for Step 4)** — `python --version`
  ≥ 3.8 for byte-safe splicing. If unavailable, fall back to the
  PowerShell pattern in Step 4.

If Python is absent, the composer MUST NOT silently fall back without
notifying the user — the PowerShell fallback is functional but
materially harder to debug for multi-section splices.

---

## Verification Checklist

- [ ] Step 1a: drop target `<A>` and recreation commit(s) `<B>` identified
- [ ] Step 1b: `git diff --stat <A>^:<X> HEAD:<X>` confirms blobs diverge
- [ ] Step 1c: divergence rubric table built; **both** sides have uniques
- [ ] Step 2: union strategy decided per file, version banner bumped, message draft authored
- [ ] Step 3: backup branch created with correct naming convention
- [ ] Step 4: union blob built byte-exactly; `git hash-object` matches expectation
- [ ] Step 5: drop executed via `git-commit-edit`; conflict on `<B>` reached
- [ ] Step 6a–c: union blob installed via `Copy-Item -Force`, hash verified, staged
- [ ] Step 6d: `git rebase --continue` used (NEVER `git commit --amend`)
- [ ] Step 6e: new commit reworded via second `rebase -i reword`
- [ ] Step 7a–d: tree mismatch is ONLY the planned files; bidirectional `cherry` shows only `<A>` + `<B>`; per-file blob hashes conserved
- [ ] Step 8: `--force-with-lease` push authorized by user
- [ ] Step 9: backup branch deleted, scratch files cleaned
