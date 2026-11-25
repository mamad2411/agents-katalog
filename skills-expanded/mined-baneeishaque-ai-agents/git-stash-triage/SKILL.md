---
name: git-stash-triage
description: Industrial protocol for classifying, disposing, and (when appropriate) promoting pre-existing Git stashes to atomic commits or personal-sandbox branches — covers hang-free inspection, content-based classification, apply-not-pop verification, and rule-driven disposition.
category: Git & Repository Management
---

# Git Stash Triage Skill (v1)

> **Skill ID:** `git-stash-triage`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Composition Rationale

This skill is a composer: it does NOT re-implement the logic for obtaining a stash’s parent commit; instead, it consumes
the [`git-stash-parent-commit`](../git-stash-parent-commit/SKILL.md) base skill to obtain the commit hash and subject
line that was HEAD when each stash was created.

1. **[`git-stash-parent-commit`](../git-stash-parent-commit/SKILL.md)** — invoked for each stash reference discovered in
Phase 0. The skill calls `scripts/get-stash-parent.ps1 -StashRef <ref>` to obtain the parent commit hash and subject
line, which are then displayed in the verdict table to aid disposition decisions.

The composer's domain‑specific value‑add over using the base skill alone: it integrates the origin‑commit data into the
stash‑triage workflow, allowing the user to see *where* a stash came from when deciding whether to drop, apply, or split
it.

Bidirectional discoverability: the base skill lists this composer in its `## Composition by Higher-Level Skills` table.

## Description

You discover one or more pre-existing entries in `git stash list` — created in
a prior session, by another tool, or by yourself before context-switching.
You need a disciplined protocol to:

1. **Inspect** stash contents without hanging the terminal (the pager trap).
2. **Classify** each stash by content into one of four disposition buckets.
3. **Decide** the correct disposition with the user (no auto-destruction).
4. **Execute** the disposition safely — apply-not-pop for whole-stash
   execution (§4b/§4c), or per-file granular triage (§4d) when the user
   requests fine-grained control or `git stash apply` fails.
5. **Drop** only after the disposition is materialized and verified.

This skill is the read-then-decide complement to
[`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
§9 (which covers stash-as-shelf during commit reconstruction). This skill
covers stashes you did NOT just create.

## When to Apply

Apply this skill when:

- `git stash list` returns ≥ 1 entry whose origin is unclear or stale.
- A workspace switch / repo audit / pre-rebase check surfaces stashes that
  must be disposed of (not silently carried forward).
- Restoring an old WIP and promoting it to a real commit / branch is on the
  table.

Do NOT apply when:

- You just created the stash 5 seconds ago as a temporary shelf during the
  same atomic-commit flow — use the inline `git stash pop` step in
  [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
  §9.
- The stash is known to belong to a feature you are about to resume — just
  `git stash pop` (no triage needed).

## Prerequisites

| Requirement | Minimum |
| --- | --- |
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or POSIX shell |
| Disposition authority | User authorization required for every destructive step (drop) |

## Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| `bash` | Required by `scripts/blob-hash-check.bash` — verify with `which bash` |
| Git 2.x+ | All operations require a valid Git repository |

Verify the blob-hash script is present:

```bash
ls -la .agents/skills/git-stash-triage/scripts/blob-hash-check.bash
```

## Script Inventory

| Script | Language | When to use |
| --- | --- | --- |
| [`scripts/blob-hash-check.bash`](scripts/blob-hash-check.bash) | Bash | Compare per-file blob hashes between a stash and HEAD (or any ref) for fast supersession triage. Default. |

---

## Operational Logic

### Phase 0 — Discover

Stashes are local refs (`refs/stash` plus reflog entries). They never push
with branches, so they are at risk if the clone is lost.

```powershell
git -C <repo-path> stash list
git -C <repo-path> show-ref | Select-String stash       # confirms refs/stash
git -C <repo-path> reflog stash                         # full history including dropped-but-not-pruned
```

For each stash reference returned by `git stash list`, the skill invokes the [`git-stash-parent-commit`](../git-stash-
parent-commit/SKILL.md) base skill to obtain the commit hash and subject line that was HEAD when the stash was created.
This information is stored for later display in the verdict table.

Additionally, capture the stash's own creation timestamp for chronological
analysis in Phase 2:

```bash
git log -1 --format=%ai stash@{N}
```

Store the timestamp alongside the parent-commit data for later display and
timeline comparison against related commit timestamps.

If `git stash list` returns no output AND `show-ref | Select-String stash`
also returns no output, there are no stashes — exit the skill.

> [!IMPORTANT]
> If a UI client (VS Code Source Control, IntelliJ, GitKraken) shows
> stashes that `git stash list` does not, check for **secondary worktrees**
> (`git worktree list`) — each worktree has independent stash refs not
> visible from sibling worktrees.

### Phase 1 — Inspect Without Hanging

`git stash show -p` and `git stash show --stat` invoke a pager by default.
In agent-driven terminals (no TTY, or a TTY that the agent cannot interact
with), this **hangs the entire VS Code window** until manually killed.

**Hang-free inspection protocol** — always use `--no-pager` AND dump to a
file:

```powershell
$repo = '<repo-path>'
# --stat first (fast overview)
git -C $repo --no-pager stash show --stat 'stash@{N}' | Out-File "$repo\.stash_stat.txt" -Encoding utf8
# Full patch (may be large)
git -C $repo --no-pager stash show -p    'stash@{N}' | Out-File "$repo\.stash_patch.txt" -Encoding utf8
```

To inspect changes scoped to a single pathspec, use `git diff` between the
stash and its parent (since `git stash show` does not accept pathspec):

```powershell
git -C $repo --no-pager diff 'stash@{N}^' 'stash@{N}' -- '*.launch' `
  | Out-File "$repo\.stash_diff.txt" -Encoding utf8
```

Read the dump files via your editor's `read_file` tool — never paginate in
the terminal.

> [!CAUTION]
> Use `.stash_*.txt` filenames so the dumps are easy to spot in
> `git status` and explicitly delete in Phase 5. NEVER commit these files.
> Add them to `.git/info/exclude` if you intend to inspect repeatedly.

### Phase 2 — Classify

For each stash, classify its content into one of four buckets:

| Bucket | Content fingerprint | Default disposition |
| --- | --- | --- |
| **A — Obsolete/duplicate** | Changes are already merged, already on disk, or superseded by newer commits | DROP (after user confirms) |
| **B — Active feature WIP** | Source-code changes belonging to a known feature branch / Jira ticket | APPLY to that feature branch + atomic commit |
| **C — Personal sandbox** | IDE artifacts, machine-specific configs, build outputs, runtime-location tweaks — not for team origin | APPLY to personal-sandbox branch (delegate to [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md)) |
| **D — Unknown / mixed** | Unclear provenance OR mixes buckets B and C | SPLIT — apply, hunk-stage by classification, multiple atomic commits |

**Classification heuristics:**

- Paths under `.idea/`, `.vscode/`, `.metadata/`, `.settings/`, generated
  Ant `build.xml`, `javaCompiler*.args`, `*.iml`, `Thumbs.db`, IDE
  workspace files → Bucket C.
- Paths under `src/`, `lib/`, `test/`, application source → Bucket B
  (correlate with active feature branch via Jira ID in branch name).
- Both → Bucket D.
- Empty stash, or stash whose diff is now a no-op against current HEAD
  (`git diff <stash> HEAD` is empty) → Bucket A.

#### Fast Supersession Check via Blob Hash Comparison

For faster Bucket A confirmation without full patch inspection, use the
[`scripts/blob-hash-check.bash`](scripts/blob-hash-check.bash) script to
compare blob hashes between the stash and HEAD on a per-file basis:

```bash
.agents/skills/git-stash-triage/scripts/blob-hash-check.bash \
  --repo <path> --stash-n <N> [--ref-b HEAD]
```

The script emits one line per differing file:

| Line pattern | Meaning |
| --- | --- |
| `IDENTICAL      <path>` | Blob hash matches HEAD — no unique stash content |
| `DIFFERENT      <path>` | Blob hash differs — needs deeper analysis |
| `not in stash   <path>` | File exists in HEAD but not in the stash |
| `not in HEAD    <path>` | File exists in stash but not in HEAD (untracked at stash time) |

- **All files IDENTICAL** → proven Bucket A. The stash contains zero unique
  content. Exit code 0.
- **Any file DIFFERENT** → the differing files need deeper analysis. Exit
  code 1. Determine whether the differences represent content that was
  deliberately refined (superseded → Bucket A) or content that was lost
  (salvageable → consider §4d selective restoration).

**Chronological timeline analysis** — when blobs differ, compare the stash
creation timestamp (captured in Phase 0) against the timestamps of commits
that touched the same files:

```bash
git -C <repo> log -1 --format="%ai %s" stash@{N}    # stash creation time
git -C <repo> log -1 --format="%ai %s" -- <file>     # last commit touching file
```

Scenarios:

| Timeline pattern | Likely classification | Rationale |
| --- | --- | --- |
| Stash created BEFORE a commit that modified the same file | Bucket A (superseded draft) | The stash captured working-copy draft content that was intentionally refined and committed later. The stash blob differs because the commit distilled the draft into a cleaner form — the stash was a transient shelf, not lost work. |
| Stash created AFTER the last commit touching the file, and blob differs | Potentially Bucket B/D (salvageable) | The stash content represents work-in-progress that was started but never committed. If the file tracks source code, prompt the user to apply. |
| Stash created BEFORE the commit, but stash content is MORE detailed than commit (added lines absent in HEAD) | Assess per file — see §4d for extraction | The stash may contain draft annotations, debug code, or long-form documentation that the commit intentionally trimmed. Present the stash version to the user for selective extraction. |

This comparison is a lightweight alternative to the full
[`git-ref-content-audit`](../git-ref-content-audit/SKILL.md) audit in §4a.
Use the full audit when you need a formal proven-superseded verdict
(especially for safety stashes created by
[`git-pre-execution-safety-stash`](../git-pre-execution-safety-stash/SKILL.md)).
Use the blob-hash shortcut for quick triage of many stashes.

### Phase 3 — Decide (User Authorization Gate)

Present the classification to the user as a verdict table:

```text
stash@{0}  Bucket C  <hash> <subject>  46 files +17,155  PDE build artifacts + 2 launch tweaks
stash@{1}  Bucket A  <hash> <subject>  3 files +12       Already-committed README changes
stash@{2}  Bucket B  <hash> <subject>  5 files +130      WIP on SWIT-12345 feature/foo
```

For each row, propose the default disposition and request the user's
explicit `go` / `start` / numbered choice. NEVER auto-execute drops.

> [!WARNING]
> `git stash drop` / `git stash pop` / `git stash clear` are destructive.
> Stashes are NOT in the reflog after being dropped (reflog entries are
> garbage-collected). Lost stash content is unrecoverable without
> `git fsck --lost-found` heroics and may not be found at all. Always
> require explicit user authorization per stash.

### Phase 4 — Execute Disposition

Choose the execution path based on the disposition decided in Phase 3:

- **§4a (Bucket A)**: Drop the stash (after supersession verification).
- **§4b (Bucket B/C)**: Apply all, then commit.
- **§4c (Bucket D)**: Apply all, hunk-stage, multiple commits.
- **§4d (Selective File Restoration)**: Walk through each changed file
  individually — analyze, present findings, get user decision per file.
  Use when `git stash apply` failed, the user requests per-file
  granularity, or the stash contains mixed file types needing individual
  per-type treatment.

#### 4a — Bucket A (Drop)

> **Stronger pre-drop verification (recommended for safety stashes)**:
> before invoking `stash drop`, run the
> [`git-ref-content-audit`](../git-ref-content-audit/SKILL.md) per-file
> blob-equality audit to prove every file the stash captures (including its
> untracked tree at `<stash>^3`) is byte-identical or knowingly-refined in
> the disposition target (usually `HEAD`). A `✅ FULLY SUPERSEDED` verdict
> upgrades Bucket A from "applied content already in tree" to "every
> stashed blob proven equal at HEAD".
>
> ```bash
> python3 .agents/skills/git-ref-content-audit/scripts/audit-ref-content.py \
>     --repo $repo --stash N --ref-b HEAD --show-diffs
> ```

```powershell
git -C $repo stash drop 'stash@{N}'
git -C $repo stash list   # verify N decremented or list empty
```

#### 4b — Bucket B or C (Apply → Commit → Drop)

ALWAYS use `apply` not `pop`. `pop` drops the stash atomically with the
apply — if the apply succeeds but the subsequent commit fails (conflicts,
hook rejection, mis-staged hunks), you have neither the stash nor the
commit. `apply` preserves the stash until you have verified the commit.

```powershell
# 1. (Pre-flight) Make sure the working tree is clean
git -C $repo status --short

# 2. (Optional) Switch to or create the destination branch
git -C $repo checkout <feature-branch>            # Bucket B
# OR
git -C $repo checkout -b personal/<purpose>       # Bucket C — see git-personal-sandbox-remote skill

# 3. Apply (NOT pop)
git -C $repo stash apply 'stash@{N}'

# 4. Inspect the working tree against the planned classification
git -C $repo status --short
git -C $repo diff --stat

# 5. Stage and commit atomically per git-atomic-commit-construction skill
git -C $repo add <paths>
git -C $repo commit -F <message-file>             # see SSOT mandate below

# 6. Verify the commit
git -C $repo log -1 --format='%H %s'
git -C $repo diff HEAD~1 HEAD --stat

# 7. ONLY after the commit is verified, drop the stash
git -C $repo stash drop 'stash@{N}'
```

> [!IMPORTANT]
> **Commit message authoring** — use the BOM-free, variable-expansion-safe
> pattern when authoring the message via PowerShell:
>
> ```powershell
> $msg = @'
> chore(scope): subject line
>
> Body paragraph...
> Use ${var} forms — single-quoted here-string PREVENTS expansion.
> '@
> $utf8NoBom = [Text.UTF8Encoding]::new($false)
> [IO.File]::WriteAllText("$repo\.git\COMMIT_EDITMSG_NEW", $msg, $utf8NoBom)
> ```
>
> NEVER use `Out-File -Encoding utf8` (writes BOM, leaks into commit subject
> as `∩╗┐` glyphs). NEVER use double-quoted here-strings (`@"..."@`) — they
> expand `$variable` and `${variable}` references mid-message, corrupting
> sentences like `location=${workspace_loc}/...`.

#### 4c — Bucket D (Split — Apply → Hunk-Stage → Multiple Commits)

Same as 4b but instead of staging whole files, use interactive add to
separate hunks per classification bucket:

```powershell
git -C $repo stash apply 'stash@{N}'
git -C $repo add -p              # hunk-by-hunk: stage only Bucket B hunks
git -C $repo commit -F <feature-msg>
git -C $repo add -p              # second pass: stage only Bucket C hunks
git -C $repo commit -F <sandbox-msg>
git -C $repo status --short      # MUST be clean
git -C $repo stash drop 'stash@{N}'
```

Each commit MUST follow
[`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md).

#### 4d — Selective File Restoration (Per-File Triage)

Use this subsection instead of §4a–§4c when:

- `git stash apply` failed (divergent editor — see
  [`git-pre-execution-safety-stash`](../git-pre-execution-safety-stash/SKILL.md)
  §1g for the safety-stash path; this subsection covers ALL stashes).
- The user explicitly requests per-file granularity.
- The stash contains mixed file types requiring individual treatment
  per file type (user config vs auto-generated IDE state vs binary cache).

**Core principle — analysis-first, action-on-command**: For each changed
file, the agent analyzes (stash vs HEAD; or stash vs on-disk when the HEAD
version is gitignored), presents findings, recommends an action, and
**waits for the user to decide**. No action is pre-determined for any
file type.

---

##### Step 1 — List changed files

```bash
git -C <repo> diff stash@{N} HEAD --name-status
```

This lists every file that differs between the stash and HEAD, prefixed with
`A` (Added), `M` (Modified), or `D` (Deleted). `A` files do not exist in HEAD
— they must be located in the stash's index tree (`stash@{N}^2`) or untracked
tree (`stash@{N}^3`).

---

##### Step 2 — Per-file analysis loop

For each file in the `--name-status` output:

1. **Determine the reference versions**:
   - **If file exists in HEAD (M)**: compare `git diff stash@{N} HEAD -- <file>`.
   - **If file exists only in stash (A)**: determine source tree:
     - Check stash^2 (index): `git ls-tree stash@{N}^2 | grep <path>`
     - Check stash^3 (untracked): `git ls-tree stash@{N}^3 | grep <path>`
   - **If HEAD version is gitignored**: compare stash version vs on-disk file
     (`diff <(git show stash@{N}:<path>) <path>`) — the HEAD commit does not
     track it, but the file lives in the working tree.

2. **Classify the file type** and apply the appropriate analysis pattern:

    | File type | Analysis pattern | Typical recommendation |
    | --- | --- | --- |
   | `settings.json` (VS Code user settings) | Compare keys line-by-line: stash-only keys, HEAD-only keys, common-modified keys | Merge stash-only keys into HEAD (user decides) |
   | `extensions.json` (VS Code auto-generated) | Verify HEAD version is current; skip if auto-regenerated | Skip — auto-generated IDE state |
   | `state.vscdb` (SQLite binary — VS Code state) | Delegate to [`vscode-state-vscdb-merge`](../vscode-state-vscdb-merge/SKILL.md) `--json` for key-level comparison. Present stash-only/HEAD-only/common-modified key counts | Merge stash-only keys if stash has unique keys (user authorizes) |
   | `claude/*.json`, `claude/.last-cleanup` (Claude config) | Compare content; check if stash has newer/updated values | Restore from stash if newer |
   | `claude/projects/*.jsonl` (gitignored, on-disk) | Compare on-disk hash vs stash hash (`git hash-object <file>` vs `git rev-parse stash@{N}:<path>`) | No action needed if hashes match; user decides if they differ |
   | `.gitignore`, `.gitattributes` | Show diff | User decides |
   | Other text files | Show diff | User decides |
   | Other binary files (non-SQLite) | Show only stat (size, hash) | User decides |

3. **Present findings**:
   - Diff output (or key-level comparison for state.vscdb)
   - Source (stash@{N} tracked / stash@{N}^2 index / stash@{N}^3 untracked)
   - File type category with implications
   - Recommended action

4. **Wait for user decision**. Options:
   - **restore**: overwrite working tree with stash version (`git checkout
     stash@{N} -- <file>` for tracked, `git show stash@{N}^3:<path> > <path>`
     for untracked).
   - **skip**: keep HEAD/disk version, ignore stash version.
   - **merge**: for structured files (settings.json, state.vscdb) — merge
     stash-only content into HEAD/disk version.
   - **defer**: skip for now, handle later.

5. **Proceed to the next file** only after the user decides.

---

##### Step 3 — "Not in HEAD" rule presentation**

Files that exist only in the stash (`A` in `--name-status`, or present in
stash^2/stash^3 but absent from HEAD and the working tree) are presented
with a strong recommendation to restore — the user chose to snapshot them;
the snapshot should be honored unless explicitly skipped. The final decision
is always the user's.

---

##### Step 4 — Restoring Added files from stash trees

When the user chooses **restore** for an `A` file:

- **If the file was staged** at stash time (found in stash^2):

  ```bash
  git checkout stash@{N} -- <path>
  ```

- **If the file was untracked** at stash time (found in stash^3):

  ```bash
  git show stash@{N}^3:<path> > <path>
  ```

The stash^2 (index) and stash^3 (untracked) trees are read-only — these
commands never modify the stash entry.

#### Non-Destructive Extraction to a New File Path

When the user wants to examine, compare, or archive stash content without
overwriting the working tree's HEAD version, extract the stash file to a
**new** path instead:

```bash
git -C <repo> show stash@{N}:<path> > <path_stash_vN.ext>
```

Use a naming convention that makes the origin clear and avoids confusion
with the tracked file — for example, append `_stash_v{N}` before the
extension (e.g., `SKILL_stash_v3.md` alongside `SKILL.md`).

**When to offer this option:**

- The stash draft contains useful reference material (code examples,
  documentation snippets, test patterns) that was trimmed or replaced in
  the committed version — the user may want to keep both.
- The user explicitly asks to save stash content without applying it.
- `git stash apply` fails on the file (divergent edits), but the user
  wants to copy specific sections manually.

**After extraction**, verify the file exists and note it in `git status`:

```bash
ls -la <path_stash_vN.ext>
git -C <repo> status --short
```

The extracted file is now an untracked working-tree artifact. The user
MUST decide its fate (commit, `.gitignore`, or delete) — it is NOT
automatically cleaned up by Phase 5.

---

##### Step 5 — Verification

After all files are processed:

```bash
git -C <repo> status --short
git -C <repo> diff --stat
```

Confirm the working tree matches the expected state. Present a summary to the
user listing which files were restored/skipped/merged/deferred.

---

### Phase 5 — Clean Up Inspection Artifacts

```powershell
Remove-Item "$repo\.stash_stat.txt", "$repo\.stash_patch.txt", "$repo\.stash_diff.txt" `
  -ErrorAction SilentlyContinue
git -C $repo status --short   # MUST be clean
```

---

## SSOT Compliance

This skill consumes — never duplicates — the following authoritative rules:

- **Commit construction** — every commit produced in Phase 4 MUST follow
  [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
  for atomicity, staging discipline, and message format.
- **Commit messages** — Conventional Commits subject + body per the
  project's commit-message rules (resolved via
  [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md)
  when retrofitting).
- **Personal sandbox routing** — Bucket C dispositions MUST delegate
  branch/remote setup to
  [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md)
  rather than inventing a parallel scheme.
- **Push authorization** — when the disposition includes a push, the
  global "agent MUST NEVER `git push` automatically" rule from
  [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
  applies — explicit user `start` required.
- **VS Code state.vscdb analysis** — when Phase 4d encounters `state.vscdb`
  files, analysis MUST use
  [`vscode-state-vscdb-merge`](../vscode-state-vscdb-merge/SKILL.md)'s
  `scripts/analyze-state-vscdb.py` for key-level comparison, never a raw
  binary diff. The `--merge` flag MUST NOT be invoked without explicit user
  authorization after the analysis report is presented.

---

## Anti-Patterns

| Anti-pattern | Why it's wrong | Correct alternative |
| --- | --- | --- |
| `git stash show -p stash@{0}` in agent terminal without `--no-pager` | Hangs VS Code (pager blocks on TTY) | Phase 1 dump-to-file pattern |
| `git stash pop` followed by attempt to commit | If commit fails after pop, stash is gone | `apply` + verify + `drop` (Phase 4b) |
| Auto-drop "obviously obsolete" stash without user confirmation | Stash content is unrecoverable after drop | Phase 3 user gate |
| `Out-File -Encoding utf8` for commit message | Writes UTF-8 BOM → subject shows `∩╗┐` glyph | `[IO.File]::WriteAllText` with `UTF8Encoding($false)` |
| Double-quoted here-string (`@"..."@`) for commit message body | PowerShell expands `$var` / `${var}` mid-message | Single-quoted (`@'...'@`) here-string |
| `git stash show -p stash@{0} -- '*.launch'` | `stash show -p` does NOT accept pathspec — fails with "Too many revisions" | Use `git diff 'stash@{N}^' 'stash@{N}' -- '*.launch'` instead |
| Prescribing a fixed per-file action during selective restoration (e.g., "settings.json → always merge") without presenting analysis first | File-specific action without user review bypasses the per-file triage gate | Always analyze stash vs HEAD (or stash vs on-disk), present findings, recommend action, then let user decide — even for well-known file types |
| Showing raw `git diff` for state.vscdb binary files during per-file triage | Binary diff is noise; no meaningful key-level differences visible | Delegate to `vscode-state-vscdb-merge` script with `--json` for per-key comparison |

---

## Traceability

- Initial design driven by a live-session episode where an unaudited stash
  containing 46 PDE artifacts + 2 personal launch tweaks was discovered,
  classified as Bucket C (Personal Sandbox), and promoted to
  `personal/sandbox` on a freshly-created personal remote via the
  [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md)
  skill — surfaced the hang-prevention, apply-not-pop, BOM-free,
  expansion-safe, and `stash show -p` pathspec-limitation rules captured
  here.
- A subsequent session triaged 4 stashes (all Bucket A — safety snapshots
  whose content was already committed or superseded). One stash contained
  ~100 lines of Playwright E2E test code that had been drafted but replaced
  in the commit with a cross-reference. The content was extracted to a new
  file (`SKILL_stash_v3.md`) before dropping the stash — surfaced the need
  for blob-hash supersession check (§2.2), chronological timeline analysis
  (§2.2), and non-destructive extraction to a new file path (§4d).

---

<!-- Generated by the Skill Factory (skill-factory v1) -->
