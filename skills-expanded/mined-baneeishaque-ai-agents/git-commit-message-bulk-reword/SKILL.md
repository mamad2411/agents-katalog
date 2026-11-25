---
name: git-commit-message-bulk-reword
description: Composer — audit a contiguous range of commits against the
    project's commit-message rules, propose Conventional Commits
    replacements with diff-driven scopes, and reword them all in a
    single non-interactive rebase by amortizing the
    git-commit-message-reword primitive across the range.
category: Git & Repository Management
---

# Git Commit Message Bulk Reword Skill

> **Skill ID:** `git-commit-message-bulk-reword`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

When a contiguous range of commits has non-compliant subject lines
(e.g., GitHub Web UI auto-generated `Create X.md` / `Update X.md`,
or other non-Conventional-Commits messages), this skill:

1. Enumerates every commit in the range.
2. For each commit, inspects the diff to determine the appropriate
   `type(scope): description` Conventional Commits replacement.
3. Presents the full proposal table to the user for approval.
4. Executes a **single** non-interactive `git rebase -i` that
   rewords all approved commits in one pass — far faster and
   safer than 27 sequential `git commit-edit` invocations.

## Composition Rationale

This is a **range composer** in a 3-layer stack:

```
git-commit-edit                       (base — generic per-commit edit)
└── git-commit-message-reword         (composer — single-commit, rules-driven)
    └── git-commit-message-bulk-reword (THIS — range over the single-commit composer)
```

| Concern | Owner |
|---|---|
| Per-commit reword mechanics (sed anchor, `GIT_EDITOR`, descendant replay) | [`git-commit-edit`](../git-commit-edit/SKILL.md) |
| Reading the project's commit-message rules and authoring a single compliant message | [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md) |
| Range enumeration, per-commit diff classification across the range, batch proposal table, single-pass rebase execution | **this skill** |

The composer **MUST NOT** reimplement the per-commit primitive. It
amortizes the single-commit skill across N commits by building one
shared map and one rebase invocation, then delegates all safety
mandates (backup branches, push authorization, cleanup) to the base
skill's protocol.

## Source Rules

| Rule File | Scope Incorporated |
|---|---|
| `<repo>/git-commit-message-rules.md` (resolved per-project) | Conventional Commits format, imperative mood, 50/72 limits, body bullet style, no redundancy |
| [`git-commit-message-reword/SKILL.md`](../git-commit-message-reword/SKILL.md) | **SSOT** for rules-file discovery (§0a), per-commit message authoring + body authoring (§0c, Fidelity Mandate, Self-Documenting Titles, body checklist), and Conventional Commits lint regex (§2a) |
| [`git-commit-edit/SKILL.md`](../git-commit-edit/SKILL.md) | All Step 0e backup, Step 7b push authorization, Step 8 cleanup mandates; sed-anchor trailing-space pattern; rebase-merge worktree-safe path |

### SSOT Delegation Map

This composer **does not restate** anything from its base or sibling.
The following concerns live in the referenced skills only:

| Concern | SSOT Location |
|---|---|
| Locate commit-message rules file + extract constraints | [`git-commit-message-reword` §0a](../git-commit-message-reword/SKILL.md#0a--locate-the-commit-message-rules) |
| Per-commit body authoring (Fidelity Mandate, Self-Documenting Titles 3-condition opt-out, body content checklist) | [`git-commit-message-reword` §0c](../git-commit-message-reword/SKILL.md#0c--author-the-new-message-fidelity-mandate) |
| Conventional Commits lint regex | [`git-commit-message-reword` §2a](../git-commit-message-reword/SKILL.md#2a--conventional-commits-lint) (range invocation in §4a is the only local variant) |
| Sed trailing-space anchor wisdom | [`git-commit-message-reword` Step 1 IMPORTANT note](../git-commit-message-reword/SKILL.md#step-1--delegate-to-git-commit-edit-reword-mode) |
| Backup branch creation, force-push gate, cleanup gate | [`git-commit-edit` Step 0e / 7b / 8](../git-commit-edit/SKILL.md) |
| `rebase-merge` path resolution in submodule worktrees | [`git-commit-edit` §5b](../git-commit-edit/SKILL.md#5b--handle-corrupted-rebase-state) |

This composer **owns**:

- Range enumeration (§0b) and chronological ordering
- Type/scope **heuristic table** for batch pattern recognition (§0c)
- Batch proposal table format (§0d)
- Map file + sequence-editor + commit-msg-editor scripts (Steps 1–2)
- Map Freshness Check (§1a) and Rewrite-Count Assertion (§4b)
- Diagnostic tracing snippets (§6a)

## Source Conversations

| Date | Topic |
|---|---|
| 2026-05-09 | Bulk reword of 27 GitHub-UI auto-generated commits in `ai-agent-rules` `master-2` branch; first attempt no-opped due to stale-SHA map (now §1a) and submodule-worktree path (now Step 2 critical note); body-mandatory default and rewrite-count assertion (§4b) added from this session |

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | Bash 4+ / Zsh / PowerShell 5.1+ |
| State | Clean working tree on the branch containing the range |
| Access | Write access to the repository |
| Project | A `git-commit-message-rules.md` (or equivalent) defining the project's commit-message standard |

## When to Apply

Apply this skill when:

- The user identifies a **range of commits** (start..end SHAs,
  start^..end, OR a list of contiguous and non-contiguous SHAs
  spanning a single rebase region) with non-compliant subject lines.
- The repository has documented commit-message rules to enforce.
- The user wants the entire range fixed in a single coherent rebase
  rather than 1 commit at a time.

### Inclusive Range Semantics

When the user supplies endpoints `<A>..<B>` in natural language
("from A to B"), they almost always mean **both A and B included**.
The canonical Git form for that intent is `<A>~1..<B>` (note the
`~1`). The agent MUST always use the inclusive form.

### Selective Non-Contiguous Targets

The map-driven mechanism (§2) supports **selective rewording across
a non-contiguous set of SHAs in a single rebase pass**:

- Choose the rebase base as the parent of the **earliest** target
  (`<earliest>~1`).
- Include the targets' abbreviated SHAs as keys in `_bulk_reword_map.txt`.
- Intermediate commits whose SHAs are **not** in the map remain as
  `pick` (unchanged), because the sequence-editor sed only mutates
  matched lines.

This is preferable to running multiple separate rebases when targets
are scattered: one backup, one rebase, one force-push.

Do NOT apply when:

- Only **one** commit needs rewording — use
  [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md).
- The commits also need **content** changes (file edits, file
  removal) — use [`git-commit-edit`](../git-commit-edit/SKILL.md)
  per commit (this skill is reword-only).
- The range spans a **public, shared base branch** (e.g., `master`
  with active collaborators) — coordinate with the team first;
  force-push will rewrite their history.

---

## Step-by-Step Procedure

### Step 0 — Pre-Reword Audit

#### 0a — Confirm Commit-Message Rules File

**Delegated SSOT:** apply
[`git-commit-message-reword` §0a](../git-commit-message-reword/SKILL.md#0a--locate-the-commit-message-rules)
verbatim. Read the project's commit-message rules file in full and
extract the same constraint set (format, types, scope, length,
wrap, mood, punctuation, body authoring rules) once at the start
of the bulk run. The extracted constraints apply uniformly to
every commit in the range.

#### 0b — Enumerate the Range

```bash
git log --reverse --oneline <start>~1..<end>
git log --reverse --oneline <start>~1..<end> | wc -l
```

> [!IMPORTANT]
> Use `--reverse` so commits are listed **chronologically (oldest
> first)**, matching the order they will appear in the rebase todo.

#### 0c — Diff-Driven Classification & Body Authoring (Fidelity Mandate)

For **each** commit, fetch the **full content diff** (not just stats)
to determine the correct Conventional Commits type, scope, AND to
author a content-faithful body:

```bash
git show --name-only <sha>           # file set (no path truncation)
git show <sha>                       # full unified diff
git show <sha> -- <changed-files>    # per-file deep dive
```

Use `--name-only` (not `--stat`) for the initial file list to avoid
path truncation. See
[`git-commit-message-delivery` §2](../git-commit-message-delivery/SKILL.md#2-verification-pattern)
for the rationale. `--stat` may be used for human-readable line-count
summary only.

Classify type and scope via the heuristic table below (range-specific
pattern recognition), then author the body per the **delegated SSOT**
below.

| Diff signature | Suggested type | Scope hint |
|---|---|---|
| New rule file in `ai-agent-rules/` | `docs(rules)` | the rule's domain |
| Edit to existing rule file | `docs(rules)` | the rule's domain |
| New skill / modified `SKILL.md` | `feat(skills)` or `docs(skills)` | skill name |
| Source code addition | `feat(<module>)` | module |
| Source code fix | `fix(<module>)` | module |
| Test addition | `test(<module>)` | module |
| Refactor without behavior change | `refactor(<module>)` | module |
| Build / CI / config | `chore(<scope>)` or `build(<scope>)` | ci / build / deps |

##### Body Authoring — delegated SSOT

**Body authoring rules (MANDATORY-by-default, Self-Documenting
Titles 3-condition opt-out, body content checklist) live in
[`git-commit-message-reword` §0c](../git-commit-message-reword/SKILL.md#0c--author-the-new-message-fidelity-mandate)
and are NOT restated here.** Apply that section verbatim to every
commit in the range. The proposal table (§0d) MUST surface the
authored body of every commit, or explicitly justify each
subject-only entry against those three conditions.

#### 0d — Reword Proposal Table

The agent **MUST** present the full proposal as a table:

````markdown
## Bulk Reword Proposal

**Repository:** `<repo>`
**Branch:** `<branch>`
**Range:** `<start>..<end>` (`<N>` commits)
**Backup target:** `backup/pre-bulk-reword-<n>`

| # | SHA | Old subject | New subject |
|---|-----|-------------|-------------|
| 1 | `abc1234` | `Create X.md` | `docs(rules): introduce X protocol` |
| 2 | `def5678` | `Update X.md` | `docs(rules): clarify X edge case` |
| ... | ... | ... | ... |

### Body strategy

Bodies follow the **delegated SSOT** in
[`git-commit-message-reword` §0c](../git-commit-message-reword/SKILL.md#0c--author-the-new-message-fidelity-mandate)
(MANDATORY by default; Self-Documenting Titles 3-condition opt-out;
body content checklist). The proposal table MUST surface the body
of every commit, or explicitly justify each subject-only entry
against the three conditions.

### Risks
- Range size: `<N>` → estimated rebase replay time
- Conflicts: `<low|medium|high>` based on file overlap with
  descendants outside the range
- Force-push required: `<yes|no>`

Proceed with the bulk reword? (yes / no)
````

**The agent MUST NOT execute the rebase until the user approves
the entire table.** Partial approvals (e.g., "fix all but #5") MUST
result in a regenerated table.

#### 0e — Workspace Backup

Per the [base skill's Step 0e](../git-commit-edit/SKILL.md#0e--workspace-backup-safety-first):

```bash
git branch backup/pre-bulk-reword-<n>
git push origin backup/pre-bulk-reword-<n>
```

---

### Step 1 — Generate the Reword Map

Materialize two files in `/tmp` (or `$TMPDIR`):

1. **`/tmp/_bulk_reword_map.txt`** — one line per commit:
   `<short-sha>=<new-subject>`
2. **`/tmp/_bulk_reword_bodies/<short-sha>.txt`** — the body file.
   Per the Body Authoring mandate (§0c), this file is the **default**
   for every map entry. Omit ONLY for commits that justified
   subject-only status against the Self-Documenting Titles checklist
   in the proposal table.

Example map file:

```text
3c029bc=docs(rules): add GitHub Actions rule baseline
fa41f0f=docs(rules): expand GitHub Actions usage notes
807b937=docs(rules): add Flutter Android app baseline
```

#### 1a — Map Freshness Check (MANDATORY before Step 3)

**The map's abbreviated SHAs MUST match the current branch tip's
rebase region.** If the branch was rewritten (rebase, amend,
cherry-pick) between when the map was authored and when the rebase
is launched, every key will silently miss its `pick` line and the
rebase will replay the range with **zero rewords**, producing the
appearance of success while changing nothing.

Run this check immediately before Step 3:

```bash
MAP=/tmp/_bulk_reword_map.txt
MISSING=0
while IFS='=' read -r sha _; do
  [ -z "$sha" ] && continue
  if ! git log --pretty='%h' <start>~1..HEAD | grep -qx "$sha"; then
    echo "MISSING: $sha"
    MISSING=$((MISSING+1))
  fi
done < "$MAP"
echo "Missing keys: $MISSING / $(wc -l < "$MAP")"
```

If `MISSING > 0`, **STOP**. Either the branch was rewritten or the
map was built against a different branch / backup. Rebuild the map
from the current SHAs (re-run §0b enumeration) before proceeding.

---

### Step 2 — Build the Sequence Editor and Commit Editor

Two scripts drive the non-interactive rebase:

**`/tmp/_bulk_seq.sh`** — marks every mapped commit as `reword`:

```sh
#!/bin/sh
TODO="$1"
MAP=/tmp/_bulk_reword_map.txt
while IFS='=' read -r sha _; do
  # Match "pick <sha> ..." at start of line, change to "reword"
  sed -i.bak "s/^pick $sha /reword $sha /" "$TODO"
done < "$MAP"
```

**`/tmp/_bulk_msg.sh`** — replaces the commit message buffer.

> [!CRITICAL]
> **`HEAD` cannot identify the current commit during `reword`.** When
> Git invokes `GIT_EDITOR`, the new commit has already been applied,
> so `HEAD` points to the **just-rewritten** commit, not the original.
> The reliable source of the original SHA is the **last line** of
> `rebase-merge/done` (resolved via `git rev-parse --git-path`),
> which contains the original full SHA in column 2.

> [!CRITICAL]
> **NEVER hardcode `.git/rebase-merge/done`.** In a submodule worktree
> (or any linked worktree) `.git` is a *file* pointing into
> `<superproject>/.git/modules/<name>`, so the literal path does not
> exist. Always resolve via `git rev-parse --git-path rebase-merge/done`,
> which returns the correct absolute path in every worktree topology
> (top-level repo, submodule, `git worktree add`).

```sh
#!/bin/sh
COMMIT_MSG_FILE="$1"
MAP=/tmp/_bulk_reword_map.txt
DONE=$(git rev-parse --git-path rebase-merge/done)
[ -f "$DONE" ] || exit 0
# Last line of done = current commit being processed.
# Format: "reword <full-40-char-sha> # <subject>"
FULL_SHA=$(awk 'END{print $2}' "$DONE")
[ -n "$FULL_SHA" ] || exit 0
# Map keys are abbreviated SHAs; match as PREFIX of the full SHA.
NEW_SUBJECT=$(awk -F= -v sha="$FULL_SHA" \
  'index(sha, $1)==1 {print substr($0, length($1)+2); exit}' "$MAP")
[ -n "$NEW_SUBJECT" ] || exit 0

ABBREV=$(awk -F= -v sha="$FULL_SHA" \
  'index(sha, $1)==1 {print $1; exit}' "$MAP")
BODY_FILE="/tmp/_bulk_reword_bodies/$ABBREV.txt"
{
  printf '%s\n' "$NEW_SUBJECT"
  if [ -f "$BODY_FILE" ]; then
    echo
    cat "$BODY_FILE"
  fi
} > "$COMMIT_MSG_FILE"
```

> [!IMPORTANT]
> The sequence-editor pattern `pick <sha> ` MUST end with a space
> to anchor on the SHA token. The git interactive rebase todo format
> is `pick <abbrev-sha> # <subject>` — the trailing space is what
> distinguishes `923c42a` from `923c42ab`.

---

### Step 3 — Execute the Rebase

```bash
GIT_SEQUENCE_EDITOR=/tmp/_bulk_seq.sh \
GIT_EDITOR=/tmp/_bulk_msg.sh \
git rebase -i <start>~1
```

**Expected output:** `Successfully rebased and updated refs/heads/<branch>.`

#### 3a — Conflict Handling

If a descendant commit conflicts (rare for reword-only):

1. Inspect: `git status && git diff`
2. Resolve and `git add <files>`
3. `git rebase --continue`

If a mapped commit becomes empty after rebase, the agent MUST
**stop** and consult the user — do not auto-skip.

---

### Step 4 — Verification

```bash
git log --oneline <start>~1..HEAD | head -<N+5>
git log --oneline <start>~1..HEAD | wc -l
```

The count MUST equal the original range size. Spot-check 3
random commits — use `git show --name-only <sha>` for reliable
file-set verification (no path truncation), and
`git show <sha>` for full diff inspection.

#### 4a — Conventional Commits Lint

Run a lint pass on every reworded commit's subject:

```bash
git log --pretty=format:'%h %s' <start>~1..HEAD | \
  grep -vE '^[0-9a-f]+ (feat|fix|docs|style|refactor|test|chore|perf|build|ci)(\([^)]+\))?: .+'
```

Empty output = all subjects compliant.

#### 4b — Rewrite-Count Assertion (MANDATORY)

A "successfully rebased" message does **NOT** mean any commit was
reworded — a rebase that re-picks the entire range with zero
matches will also report success. Confirm the rewrites actually
landed:

```bash
REWORDED=$(git log --pretty='%s' <start>~1..HEAD | \
  grep -cE '^(feat|fix|docs|style|refactor|test|chore|perf|build|ci)(\([^)]+\))?: ')
echo "Reworded subjects: $REWORDED"
```

`$REWORDED` MUST be `>=` the map size. If it equals the count from
*before* the rebase, **the rebase no-opped** — reset to the backup
and return to §1a (Map Freshness Check).

---

### Step 5 — Push Authorization & Cleanup

Delegate to the base skill's
[Step 7b](../git-commit-edit/SKILL.md#7b--pre-push-remote-backup--push-authorization)
and [Step 8](../git-commit-edit/SKILL.md#step-8--final-history-verification--backup-cleanup):

1. Create remote-state backup: `git branch backup/pre-force-push-<n> origin/<branch>`
2. Push backup: `git push origin backup/pre-force-push-<n>`
3. Offer (do **not** execute): `git push --force-with-lease origin <branch>`
4. After user pushes, offer cleanup commands for backup branches.

> [!CRITICAL]
> All push and cleanup steps inherit the base skill's
> **explicit-authorization** mandate. The composer is **PROHIBITED**
> from executing `git push --force-with-lease` without separate user
> approval.

---

### Step 6 — Cleanup

Remove temporary files:

```bash
rm -f /tmp/_bulk_seq.sh /tmp/_bulk_msg.sh /tmp/_bulk_reword_map.txt
rm -f /tmp/_msg_trace.log /tmp/_seq_input_snapshot.txt /tmp/_seq_output_snapshot.txt
rm -rf /tmp/_bulk_reword_bodies
```

#### 6a — Diagnostic Tracing (when debugging)

If the first rebase attempt no-ops or behaves unexpectedly, add
these trace lines to the scripts before re-running:

```sh
# In _bulk_seq.sh, after reading $TODO:
cp "$TODO" /tmp/_seq_input_snapshot.txt
# ...sed loop...
cp "$TODO" /tmp/_seq_output_snapshot.txt

# In _bulk_msg.sh, at the top:
echo "[msg $(date +%T)] msg=$1 done=$DONE full=$FULL_SHA match=$MATCH" \
  >> /tmp/_msg_trace.log
```

Then inspect after the rebase:

```bash
grep -c '^reword' /tmp/_seq_output_snapshot.txt   # MUST equal map size
grep -c '^\[msg\] match=' /tmp/_msg_trace.log     # MUST equal map size
```

If either count is below the map size, the corresponding script is
failing to match — inspect the snapshots before re-attempting.

---

## Scope Coverage

| Category | Convention |
|---|---|
| Range enumeration | `git log --reverse --oneline <start>~1..<end>` |
| Diff classification | `git show --name-only <sha>` (no path truncation) + heuristic table |
| Batch reword execution | Single `git rebase -i` with `GIT_SEQUENCE_EDITOR` + `GIT_EDITOR` scripts |
| Conventional Commits compliance | Lint regex in §4a |
| Backup, force-push, cleanup | **Delegated** to [`git-commit-edit`](../git-commit-edit/SKILL.md) |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Inlining the per-commit reword primitive** — the rebase machinery
  is owned by the base skill; this composer only assembles the map and
  scripts.
- **Executing the rebase without the §0d proposal table approved** —
  bulk reword without per-commit visibility is an SSOT violation.
- **Auto-skipping conflicted or empty commits** — every conflict
  requires user consultation.
- **Pushing to remote without explicit per-step authorization** —
  inherits all base-skill push gates.
- **Generating filler bodies or omitting required bodies** — inherits
  the body-authoring mandate from
  [`git-commit-message-reword` §0c](../git-commit-message-reword/SKILL.md#0c--author-the-new-message-fidelity-mandate);
  do not restate or relax those rules.
- **Using long SHAs in the sequence-editor sed pattern** — Git's
  rebase todo uses abbreviated SHAs; matching against the long form
  silently no-ops.

---

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Rebase produces no changes — sed pattern didn't match | Run §1a Map Freshness Check **before** every rebase; the map's abbreviated SHAs must exist in the current `<start>~1..HEAD` range |
| Rebase reports success but §4b shows zero rewrites | Branch was rewritten between map construction and rebase. Reset to backup, rebuild map from current SHAs, retry |
| Msg script never finds `rebase-merge/done` (submodule worktree) | Use `git rev-parse --git-path rebase-merge/done` — NEVER hardcode `.git/rebase-merge/done` |
| Sequence editor leaves `.bak` files in `rebase-merge/` | Use `sed -i.bak` then ensure the `.bak` extension is harmless (Git ignores extra files in the todo dir) |
| Body file forgotten for one commit | Re-check §0c Self-Documenting Titles checklist; if the commit failed all 3 conditions, author and re-run with the body file added |
| Detached HEAD after rebase | Caller invoked rebase from a non-branch state. Recover with `git checkout <branch> && git reset --hard <new-tip>` after verifying the new tip is correct |
| Force-push rejected with `stale info` | Branch advanced on remote between backup and push — re-run §0e backup, re-fetch, re-evaluate |
| Lint regex flags revert / merge commits | Add `Revert\|Merge ` to the allowed prefix alternation in the §4a regex |

---

## Related Skills

- [`git-commit-message-reword`](../git-commit-message-reword/SKILL.md) —
  single-commit composer; the per-commit primitive this skill
  amortizes across a range.
- [`git-commit-edit`](../git-commit-edit/SKILL.md) — base of the
  3-layer stack (reword mechanics, backup, push gates).
- [`git-history-refinement`](../git-history-refinement/SKILL.md) —
  use when commits also need content changes or splitting, not just
  reword.
- [`noise-removal-via-commit-edit`](../noise-removal-via-commit-edit/SKILL.md) —
  another composer over the same base, for IDE artifact removal.
- [`git-branch-promotion`](../git-branch-promotion/SKILL.md) —
  **post-processing** composer; consume the refined branch produced
  here and promote it onto the canonical branch.

## Post-Processing

This skill commonly produces a parallel/refined branch (e.g.,
`<branch>-2`) so the original canonical branch (`<branch>`) remains
untouched on `origin` until the user is satisfied. To replace the
canonical branch with the refined branch — including cherry-pick
equivalence audit for any canonical-only commits that landed during
or after the bulk reword, tree-parity verification, and authorized
force-push — the agent MUST delegate to the
[`git-branch-promotion`](../git-branch-promotion/SKILL.md) skill.
Manual `git reset --hard <refined> && git push --force` on the
canonical branch WITHOUT that skill's §2 audit and §4 parity gate is
FORBIDDEN — it silently drops any commit that landed on canonical
after the bulk reword started.

**Submodule case (chained post-processing):** If the reworded range
lives in a **submodule**, after
[`git-branch-promotion`](../git-branch-promotion/SKILL.md) succeeds in
the submodule, EVERY parent-repository commit whose tree referenced
the old (now-orphaned) submodule SHAs is invalidated — even if the
parent commits themselves were not edited. The parent repository's
history MUST be repaired via
[`git-submodule-pointer-repair` §5](../git-submodule-pointer-repair/SKILL.md#5-mass-pointer-reconciliation-full-history-rewrite-recovery)
using the **reword-tolerant match key** in §5.2.0 (subject EXCLUDED).
Before initiating the bulk reword, the agent MUST ensure that at least
one of the following pre-rewrite SHA sources will remain available for
the pointer-repair session: a pre-rewrite local clone of the submodule,
a retained backup branch (per Step 0e of
[`git-commit-edit`](../git-commit-edit/SKILL.md)), or origin's still-
reachable dangling commits (typically until the next remote `gc`).
