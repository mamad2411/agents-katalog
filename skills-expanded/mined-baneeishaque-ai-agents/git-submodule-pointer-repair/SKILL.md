---
name: git-submodule-pointer-repair
description: Industrial protocol for surgically fixing invalid submodule pointers in parent repository history using the
Synchronization Horizon algorithm.
category: Git & Repository Management
---

# Git Submodule Pointer Repair Skill (v1)

This skill provide surgical, high-fidelity repair of invalid submodule pointers within a parent repository's history. It
implements the **Synchronization Horizon** algorithm to autonomously identify the correct architectural alignment point
between parent mandates and modular history.

***

## 1. Environment & Dependencies

The agent MUST verify the following tools are available before execution:

- **Git**: Mandatory for repository operations.
- **Python 3**: Mandatory for the `repair.py` synchronization engine.

```bash
# Verify environment
which git && git --version
which python3 && python3 --version
```

***

## 2. Operational Logic: The Synchronization Horizon

This algorithm identifies the exact architectural alignment point ($s_p$) where parent repository mandates are satisfied
by submodule history.

### 2.1 Detection & Backtracking (The Discovery)
1. **Identify Target**: Locate submodules with invalid pointers in the input Parent SHA.
2. **Verify Validity**: For every invalid pointer, backtrack in the parent history to find the **Last Known Valid SHA**.
3. **Isolate Intro Commit**: The commit that changed the last known valid SHA to the first invalid SHA is the **Invalid
  Reference Introduction Commit**.

### 2.2 Cumulative Synchronization Scan (Mapping)
1. **Extract Mandates**: Retrieve the commit message of the **Invalid Reference Introduction Commit**.
2. **Successor Analysis**: Identify the successor commits ($s_1, s_2, \dots, s_n$) of the Last Known Valid SHA in the
  submodule repository.
3. **Iterative Alignment**: Analyze the cumulative changes $\{s_1 \dots s_i\}$. 
4. **Identify Boundary $s_p$**: The loop stops at $s_p$ where the cumulative changes correctly and completely satisfy
  the parent's mandates ($s_{p+1}$ MUST be unrelated drift).

### 2.3 Surgical Repair (Execution)
1. **Safety Backup**: MUST create a backup tag before modification (e.g., `backup-pointer-repair-<timestamp>`).
2. **Pointer Swap**: Surgically edit the **Invalid Reference Introduction Commit**, replacing the invalid hash with
  $s_p$.
3. **Propagation**: Propagate the fix across subsequent history using a non-interactive rebase or equivalent
  transformation.

***

## 3. Cleanup Protocol

The safety backup tag MUST be managed with 100% human-in-the-loop fidelity.

1. **Verification**: Confirm `ls-tree` at the sync point reflects $s_p$.
2. **Authorization**: Explicitly ask the user: *"History repair verified. May I delete the safety backup tag
  <tag_name>?"*
3. **Execution**: Delete the tag ONLY upon explicit "yes" confirmation.

***

## 4. Automation Engine

The surgical logic is encapsulated in the industrial Python engine:
[scripts/repair.py](./scripts/repair.py)

```bash
# Example Usage:
python3 .agents/skills/git-submodule-pointer-repair/scripts/repair.py --parent <SHA> --submodule <PATH>
```

***

## 5. Mass Pointer Reconciliation (Full History Rewrite Recovery)

Use this protocol when the **entire submodule history has been rewritten** (e.g., linearized, rebased, pruned), making
**every historical pointer** in the parent repository invalid.

### 5.1 Scope Assessment

```bash
# List ALL parent commits touching the submodule pointer, oldest → newest
git log --reverse --format="%H | %as | %s" -- <submodule-path>
```

Save this list. Each entry has an invalid pointer that needs a verified replacement.

### 5.2 Build the Verified Mapping

For each invalid pointer SHA, find its counterpart in the refined submodule history using **high-fidelity metadata
extraction** (per the `git_commit_metadata_extraction` skill).

#### 5.2.0 Match-Key Selection (CRITICAL)

The match key MUST be chosen based on **how the submodule history was rewritten**:

| Submodule rewrite type | Recommended match key | Subject (`%s`) safe to include? |
| --- | --- | --- |
| Cherry-pick / linearize / rebase **without** message edits | `%aI \| %ae \| %s \| sorted-file-list` | ✅ Yes — strongest key |
| **Message-only reword** (e.g., via [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md) or [`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md)) | `%aI \| %ae \| sorted-file-list` (subject EXCLUDED) | ❌ **NO** — reworded subjects will not match; including `%s` produces false negatives |
| Mixed (some commits reworded, some not) | `%aI \| %ae \| sorted-file-list` (subject EXCLUDED) — uniformly | ❌ NO |
| Squash / split (commits collapsed or divided) | This skill is INSUFFICIENT — a 1:1 mapping does not exist; consult the user for manual N:1 / 1:N decisions | N/A |

> **Rule of thumb:** If a [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md),
> [`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md), or
> [`git-commit-edit`](../git-commit-edit/SKILL.md) operation has been run in the rewrite chain — even on a single commit
> — the subject MUST be excluded from the match key.
>
> **Why `%aI` not `%ad`?** `%aI` (strict ISO-8601) is locale-independent and stable across Git versions; `%ad` is
> influenced by `--date=` formatting and locale. Use `%aI` for keys, `%ad` only for human-readable reports.
>
> **Why `sorted-file-list`?** The order returned by `diff-tree --numstat` is implementation-defined; a sort makes the
> key deterministic across Git versions and rewrite tools.

**Match criteria — full reference set (use the subset selected above):**

- `%aI` — Author date (strict ISO-8601, locale-independent)
- `%ae` — Author email
- `%an` — Author name (rarely needed; `%ae` is more stable)
- `%cI` — Committer date (strict ISO-8601)
- `%ce` — Committer email
- `%s` — Subject (**EXCLUDE for reword cases per §5.2.0**)
- `diff-tree --numstat | awk '{print $3}' | sort` — sorted file list

#### 5.2.1 Indexing the New History

```bash
# Reword-tolerant key (subject EXCLUDED): aI | ae | sorted-file-list
git -C <new-submodule-path> log --format="%H%x09%aI%x09%ae" <new-branch> | \
while IFS=$'\t' read sha aiso aem; do
  files=$(git -C <new-submodule-path> diff-tree --no-commit-id -r --numstat "$sha" \
          | awk '{print $3}' | sort | tr '\n' ',' | sed 's/,$//')
  printf "%s\t%s|%s|%s\n" "$sha" "$aiso" "$aem" "$files"
done > /tmp/new_index.tsv
```

> **Flag breakdown:**
>
> - `--format="%H%x09%aI%x09%ae"` — emit SHA, ISO author date, author email, tab-separated.
> - `diff-tree --no-commit-id -r --numstat` — recursive numstat for the commit, suppressing the leading commit-id line.
> - `awk '{print $3}'` — column 3 of `--numstat` is the path.
> - `sort | tr '\n' ',' | sed 's/,$//'` — deterministic CSV file list.

#### 5.2.2 Resolving Old SHAs (Source-of-Truth Selection)

The old (orphaned) SHAs may not exist in the rewritten submodule clone's object store at all. Resolve them from one of
these sources, in priority order:

1. **A pre-rewrite local clone** of the submodule (e.g., `<workspace-old-clone>/<submodule>`) — strongest source; full
  reflog and pre-rewrite refs available.
2. **A backup branch** retained in the rewritten submodule clone (e.g., `backup/pre-bulk-reword-1`) — if the rewriter
  skill's cleanup gate left it in place.
3. **An origin fetch** by SHA: `git -C <submodule-path> fetch origin <old-sha>` — works only while the remote still has
  the dangling commit (typically until the next remote `gc`).

> **Strongly recommended:** Before initiating any rewrite that destroys a branch, keep at least one of the above for the
> duration of the parent-repository pointer-repair session. The promotion gate in
> [`git-branch-promotion`](../git-branch-promotion/SKILL.md) §6.1 codifies this retention horizon.

#### 5.2.3 Per-SHA Lookup

```bash
OLD=<pre-rewrite-submodule-clone>     # e.g., /Users/.../ai-suite-old/ai-agent-rules
NEW=<rewritten-submodule-clone>       # e.g., /Users/.../ai-suite-2/ai-agent-rules

: > /tmp/mapping.tsv
: > /tmp/unmatched.tsv
while read old_sha; do
  aiso=$(git -C "$OLD" log -1 --format=%aI "$old_sha")
  aem=$(git -C "$OLD" log -1 --format=%ae "$old_sha")
  files=$(git -C "$OLD" diff-tree --no-commit-id -r --numstat "$old_sha" \
          | awk '{print $3}' | sort | tr '\n' ',' | sed 's/,$//')
  key="$aiso|$aem|$files"
  matches=$(awk -F'\t' -v k="$key" '$2==k {print $1}' /tmp/new_index.tsv)
  count=$(echo -n "$matches" | grep -c .)
  if [ "$count" = "1" ]; then
    printf "%s\t%s\n" "$old_sha" "$matches" >> /tmp/mapping.tsv
  else
    printf "%s\t%s matches\tkey=%s\n" "$old_sha" "$count" "$key" >> /tmp/unmatched.tsv
  fi
done < /tmp/old_ptrs.txt
```

**Output:** A clean `old_sha\tnew_sha` mapping file, one pair per line.

> **Disambiguation:** If `count > 1` for any row, the file-list alone was insufficient (likely two commits authored at
> the same instant by the same author touching the same files — possible with reorderings). Recover by adding `%cI`
> (committer date) and/or `%ce` (committer email) to the key — these survive a message-only reword.
>
> **Failure:** If `count = 0`, the commit was likely **squashed or split** during the rewrite — see §5.2.0's "Squash /
> split" row.

### 5.3 Verify the Mapping (Extensive Check)

Generate a Markdown verification report comparing all metadata fields side-by-side:

```bash
while read -r line; do
    suite_sha=$(echo "$line" | cut -d'|' -f1 | xargs)
    sub_sha=$(echo "$line" | cut -d'|' -f2 | xargs)
    old_info=$(git -C <submodule-path> log -1 --format="%an <%ae>|%ad|%s" "$sub_sha")
    o_files=$(git -C <submodule-path> diff-tree --no-commit-id -r --numstat "$sub_sha" | awk '{print $3}' | sort | tr '\n' ' ' | xargs)
    match_line=$(grep -F "|$o_adate|$o_title" new_index.txt | head -n 1)
    # Compare: author, date, files — emit ✅ or ❌ per field
done < mapping.txt | tee verification_report.md
```

All mappings MUST show ✅ for Author, Author Date, Committer, Committer Date, Commit Message, and Files before
proceeding.

### 5.4 Backup Before Rewrite

```bash
# Create a timestamped local + remote backup branch
git branch backup/pre-submodule-repair-$(date +%Y%m%d%H%M)
git push origin backup/pre-submodule-repair-<timestamp>
```

### 5.5 Rewrite via git-filter-repo Python API

> **Why `git-filter-repo` not `git replace`?** The old pointer SHAs are unreachable (not present as valid objects in the
> parent's object store), so `git replace` fails with "null type" errors. The `commit_callback` approach via the Python
> API rewrites tree entries directly.

The automation engine for this mass repair is located at:
[scripts/mass_repair.py](./scripts/mass_repair.py)

```bash
cd <parent-repo-path> && python3 scripts/mass_repair.py
```

> **Critical:** Run from inside the parent repository directory. The script must be separate from the submodule path.
>
> **Note on `commit_callback` signature:** When using `--partial`, git-filter-repo passes two arguments: `(commit,
> metadata)`. Using only `(commit)` will raise a `TypeError`.

### 5.6 Final Validation Audit

After the rewrite, verify every pointer is a valid `commit` object in the submodule:

```bash
git log --reverse --format="%H | %as | %s" -- <submodule-path> | \
while IFS=' | ' read -r sha date msg; do
    ptr=$(git ls-tree "$sha" <submodule-path> 2>/dev/null | awk '{print $3}')
    vtype=$(git -C <submodule-subpath> cat-file -t "$ptr" 2>/dev/null)
    if [ "$vtype" != "commit" ]; then
        echo "INVALID: $sha | $date | $ptr | $msg"
    fi
done
echo "Audit complete. Silence = 100% valid."
```

**Zero INVALID lines = safe to push.**

### 5.7 Force-Push

**Do NOT push automatically.** Offer to push and wait for explicit human authorization.

```bash
# Only run after user explicitly says yes
git push --force-with-lease origin main
```

***

## 6. Traceability & Related Conversations

- **Rule Source**: Promotion of **[Git Submodule History Repair
  Rules](../../../ai-agent-rules/git-submodule-history-repair-rules.md)**.
- **Session Log (Single Pointer)**: Industrialized from the 110-commit surgical repair walkthrough.
- **Session Log (Mass Reconciliation)**: Industrialized from session `aab2c817-85cf-41bf-9db6-e200f8b4275e` — 51-pointer
  mass repair after full linearization of `ai-agent-rules` history.

***

## 7. Triggered By (Upstream Composers)

This skill is the **mandatory post-processing step** after any
submodule history rewrite that has been promoted onto the canonical
branch. The chain is always:

```text
<rewriter skill> ▸ git-branch-promotion ▸ git-submodule-pointer-repair §5
```

| Upstream rewriter | Match-key recommendation per §5.2.0 |
| --- | --- |
| [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md) | Reword case — subject EXCLUDED |
| [`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md) | Reword case — subject EXCLUDED |
| [`git-commit-edit`](../git-commit-edit/SKILL.md) (with content edits) | File-list will differ if content changed; use `%aI \| %ae \| %cI \| %ce` (subject AND files EXCLUDED — only viable if author/committer instants are unique) — otherwise manual mapping required |
| [`git-history-refinement`](../git-history-refinement/SKILL.md) | Reword case for the message-only commits; Squash/split case for any consolidated commits |
| [`git-feature-branch-atomic-commit`](../git-feature-branch-atomic-commit/SKILL.md) | Cherry-pick case (subject usually preserved) — strongest key including `%s` |
| [`git-branch-promotion`](../git-branch-promotion/SKILL.md) §7.2 | Delegates to this skill; the promotion gate codifies the pre-rewrite SHA retention horizon (§6.1) needed here |

The upstream skill MUST guarantee that the old (orphaned) submodule
SHAs remain resolvable for the duration of this skill's execution, via
at least one of: a pre-rewrite local clone of the submodule, a
retained backup branch in the rewritten clone, or an origin fetch by
SHA. Initiating cleanup of those sources before this skill's §5.6
audit reports zero `INVALID` is FORBIDDEN.
