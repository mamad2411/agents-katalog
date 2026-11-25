---
name: git-atomic-commit-construction
description: Analyze, group, and arrange working-tree changes into logical,
    independent atomic commits — with hunk-based staging, formatting
    isolation, and mandatory user authorization.
category: Git & Repository Management
---

# Git Atomic Commit Construction Skill

> **Skill ID:** `git-atomic-commit-construction`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Construct high-quality, atomic Git commits from a set of working-tree
changes. This skill covers the full lifecycle: environment validation,
change analysis, logical grouping, hunk-based staging, formatting
isolation, commit message quality, execution with user authorization,
and post-commit verification.

Every commit produced by this skill is independent, logically coherent,
and buildable. Mixed concerns are never committed together. Formatting
is separated from logic. Configuration is coupled to its functional
change. The user retains full control via mandatory preview and explicit
"start" authorization.

## Source Rules

This skill distills and operationalizes the following rule files:

| Rule File | Scope Incorporated |
|---|---|
| [`git-atomic-commit-construction-rules.md`](../../../ai-agent-rules/git-atomic-commit-construction-rules.md) | All 15 phases (primary source) |
| [`git-operation-rules.md`](../../../ai-agent-rules/git-operation-rules.md) | Phase -1, 0, 1 (environment, repo context, change detection) and Sections 2–4 (commit/push/stash protocols) |

For history refinement (splitting existing commits), see the
[`git_history_refinement`](../git-history-refinement/SKILL.md) skill.
For complex multi-branch rebasing, see the
[`git_rebase`](../git-rebase-standardization/SKILL.md) skill.

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Access | Write access to the project repository |
| Auth | GitHub CLI authenticated (if pushing to GitHub) |

## When to Apply

Apply this skill when:

- A user asks to "commit changes," "arrange commits," or "stage and commit"
- `git status` shows staged, unstaged, or untracked modifications
- Multiple unrelated changes exist in the working tree and need separation
- A user asks to review what should be committed
- **After ANY submodule commit is executed, the skill AUTOMATICALLY checks for
  and offers the parent repository submodule SHA update (if applicable) and
  executes it upon user "yes" — no separate user request needed**

Do NOT apply when:

- The user asks to refine or split **existing** commits — use
  [`git_history_refinement`](../git-history-refinement/SKILL.md) instead
- The user asks to rebase branches — use
  [`git_rebase`](../git-rebase-standardization/SKILL.md) instead
- The request is a simple single-file, single-concern commit with no
  mixed changes (a lightweight commit suffices without the full protocol)
- The files being committed are **personal-only** and should NOT reach the
  team's `origin` — route the commit to a personal sandbox branch via
  [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md)
  (this skill still applies to the commit itself, but the destination
  remote/branch changes)

**Push Policy (GLOBAL)**: The agent MUST NEVER execute `git push` automatically.
After any commit(s), the agent MAY OFFER to push (e.g., "Push to remote?") but
MUST WAIT for explicit user approval. Only push when the user explicitly says
"yes", "push", or issues a direct `git push` command. No exceptions.

---

## Step-by-Step Procedure

### Step 0 — Environment & Repository Context

Before any Git commands, validate the environment and establish context.

#### 0a — Authenticate Services

Verify authentication for required services:

```powershell
gh auth status        # GitHub CLI
```

If authentication is missing, guide the user through login.

#### 0b — Identify the Target Repository

Determine the correct repository from the user's request and file paths.

- **Nested repositories:** If changes are in a sub-directory that is its
  own Git project, use `PAGER=cat git -C` to execute `PAGER=cat git` commands in that repository.
- **Ambiguity:** If multiple repositories exist in the workspace and the
  target is unclear, ask the user for clarification.

#### 0c — Working Directory Persistence (Critical)

When working with `git` commands, use `git -C <path>` for reliable directory targeting:

```powershell
# Recommended: git -C with absolute path
git -C /path/to/repo status
git -C /path/to/repo diff HEAD

# Why this matters: Shell `cd` commands do not persist across tool invocations
# in stateless execution environments. Using git -C ensures consistent behavior
# across all command chains and multi-step workflows.

# Pattern for multi-repo work:
git -C /repo1 status
git -C /repo2 status
git -C /repo1 add file.txt
```

**When `cd` alone is insufficient:**

- In tools/environments where `cd` doesn't persist state across invocations
- When working with multiple repositories in sequence
- For clarity in tool-generated scripts and audit trails

**Legacy pattern (avoid):**

```powershell
# ❌ May not reliably persist across invocations
cd /path/to/repo; git status
```

**Preferred pattern:**

```powershell
# ✅ Reliable and explicit
git -C /path/to/repo status
```

#### 0d — Verify Build Tool Permissions

Ensure build tools have execute permissions:

```bash
chmod +x gradlew      # Gradle wrapper example
```

#### 0e — Active Branch Verification (Critical)

The agent MUST ensure the repository is not in a "detached HEAD" state before committing.

1. **Check Current Branch**: Run `git branch --show-current`.
2. **Handle Detached HEAD**: If the output is empty (detached HEAD), the agent MUST
   identify and checkout the appropriate branch (usually the default branch,
   e.g., `main`) before proceeding.
3. **Upstream Alignment**: Run `git pull` to synchronize with the remote and avoid push-time conflicts. This planning-stage check goes stale — it does NOT replace the mandatory pre-commit refresh in §9a.1 before every `git commit`.

#### 0f — Pre-Edit Repo Role Classification (Critical for unfamiliar repos)

When the upcoming commit touches files in a repository this session has not
previously edited — especially when two cloned-locally repos share a name
prefix or suffix — invoke the
[`canonical-source-vs-workflow-repo-audit`](../canonical-source-vs-workflow-repo-audit/SKILL.md)
audit BEFORE the first edit:

```bash
python3 .agents/skills/canonical-source-vs-workflow-repo-audit/scripts/audit-repo-role.py /path/to/file
```

If the verdict is `workflow` or `mirror`, STOP and locate the canonical
source repo. If the verdict is `unknown`, ask the user. Skipping this
audit risks landing the work in a repo whose changes never reach the
canonical artifact (real-world precedent: Account-Ledger-Server vs
Account-Ledger-Server-PHP, May 2026)

---

### Step 1 — Deep Change Analysis

Perform a dependency analysis of ALL modifications before staging
anything.

#### 1a — Detect All Changes

Use `git status` to discover staged, unstaged, and untracked changes:

```powershell
git status
```

**Complete Scope (Critical):** The analysis MUST cover ALL three change
categories — **staged**, **unstaged**, AND **untracked** — as a single
unified inventory from the very first step. Untracked files are
first-class members of the change scope, not a secondary check.
Failing to include untracked files in the initial analysis leads to
incomplete commit plans and files discovered only after execution.

**Untracked files:** Any untracked file not excluded by `.gitignore` is
a candidate for version control. The agent **MUST NOT** stage untracked
files without explicit user confirmation to avoid committing credentials,
large binaries, or environment-specific files. When an untracked file's
origin is unclear (cross-repo scratch, tool dump, captured diff), invoke
the [`untracked-scratch-triage`](../untracked-scratch-triage/SKILL.md)
skill to classify and dispose of it before continuing the inventory.

#### 1b — Use `git ls-files` as Source of Truth

For rename or restructuring operations, `git ls-files` is the
authoritative list of tracked files — not `Get-ChildItem` or `find`,
which include git-ignored content:

```powershell
git ls-files
```

#### 1c — Read `.gitignore` for Tracked vs Ignored

Read `.gitignore` carefully, paying special attention to **negation
patterns** (`!`) that re-include specific files inside ignored
directories:

```gitignore
# Example: directory ignored, but .zip files are tracked
pevers/*
!pevers/*.zip
```

#### 1d — Analyze Change Dependencies

- **Shared Identifiers:** Group changes that modify the same functions,
  classes, or constants across different files.
- **Cross-File References:** If file A depends on a change in file B
  (e.g., an import, a link, a `.gitignore` pattern), they MUST be in
  the same atomic commit.
- **Categorical Alignment:** Group changes by architectural layer (UI,
  Logic, Docs) unless they are functionally coupled.

#### 1e — Workflow-First Priority

If changes involve CI/CD workflows (GitHub Actions, scripts), the agent
**MUST** fix, test, and verify workflow functionality **BEFORE** arranging
or executing commits. Pipeline stability takes precedence over
documentation or stylistic refinements.

#### 1f — Present Complete Inventory

List **ALL changes** — staged, unstaged, AND untracked (not just
violations or modifications to already-tracked files) — with their
status. This gives the user full visibility and ensures no file is
analyzed as an afterthought:

| # | File | Status | Action |
|---|---|---|---|
| 1 | `.gitignore` | Modified | 🔄 Update |
| 2 | `src/main.java` | Modified | 🔄 Stage |
| 3 | `README.md` | Untracked | ❓ Confirm with user |

---

### 1g — Redaction Pre-Check (Sensitive Content Audit)

Before any staging or logical grouping, audit all **new/untracked** and
**modified** files for content that must be redacted per the
[redaction-portability](../redaction-portability/SKILL.md) skill — especially
prose-heavy files like skill `SKILL.md`, rule docs, and conversation logs.

**Scan for:**

1. **Organization-specific Jira ticket IDs** (e.g., `PROJ-1234`) — replace with
   `<TICKET-ID>` or `<TICKET-ID-PROJ>`.
2. **Internal repository URLs** (e.g., `github.com/<org>/<repo>`) — replace
   `<org>/<repo>` with `<ORG>/<REPO>`.
3. **Cross-repo relative links** — `../` chains that escape the current repo's
   root into a sibling directory (no `.gitmodules` registration). Run the
   [detect-cross-repo-links.py](../redaction-portability/scripts/detect-cross-repo-links.py)
   script from the redaction-portability skill.
4. **Literal organization names, internal codenames, hostnames, and usernames**
   in prose — replace with canonical placeholders (`<corp>`, `<author>`, etc.).
5. **Project-specific skill names / paths** in base-published skills (e.g., a
   composer row in a base skill referencing a project-specific skill in a
   different repo).

**When to run this audit:**

- **Immediately after Step 1f** (Complete Inventory) — you have the full file
  list, and no work has been wasted on grouping or staging content that will
  need post-hoc redaction.
- **Any time a new file is added** to the working tree mid-session (e.g.,
  skill-factory generation, conversation export).

**Remediation workflow:**

1. Read each flagged file, identify the violating strings.
2. Apply canonical placeholders per
   [redaction-portability §2](../redaction-portability/SKILL.md#2-canonical-placeholder-vocabulary).
3. If the violation is a cross-repo link: either delete the link entirely or
   replace with a name-only reference (see redaction-portability repair rules).
4. Re-run the audit to confirm zero remaining violations.
5. Only then proceed to Step 2 (Logical Grouping).

The redaction-portability skill **MUST** be cited as a dependency in any commit
that touches skill or rule files, so downstream tooling knows to invoke the
same audit.

---

### Step 2 — Logical Grouping (Arrangement)

Arrange detected changes into a proposed sequence of commits.

#### 2a — Independence Principle

Each commit must stand alone. If the repository were checked out at
that commit, it should still build/function (or be logically coherent).

#### 2b — Atomic Principle

Never commit half of a logical change. If a file contains two unrelated
changes, use **hunk-based staging** (Step 3).

#### 2c — Buildable State Priority

While atomicity is the goal, maintaining a buildable repository takes
precedence. If a core infrastructure change (e.g., a signature change in
a shared helper) breaks all consumers, the refactor and the resulting
fixes in consumer files MUST be consolidated into a single commit.

#### 2d — The Commit Preview (Mandatory Verbose Display)

Present the proposed "Arranged Commits" using a structured format with
**maximum detail**. For files with mixed concerns requiring hunk-based
staging, the preview **MUST** include the specific git hunks.

**Mandates for writing the preview:**

1. **`@@` Header Verification** — Before writing any `@@ -N,M +N,M @@` line,
   run `git diff --unified=3 -- <file>` and copy the exact range header from
   the actual output. Never estimate or compute from memory — wrong headers
   make the preview useless for verification.

2. **Fence Collision Handling** — When a diff hunk contains lines that are
   themselves triple-backtick fenced code blocks (` ```text`, ` ```bash`,
   and their closing ` ``` `), wrap the diff in **`~~~diff`** / **`~~~`**
   instead of ` ```diff ` / ` ``` `. Backtick fences inside a backtick-fenced
   block terminate the outer block prematurely, breaking the markdown preview.
   The tilde fence (`~~~`) is only closed by another `~~~`, so inner backtick
   blocks survive as literal content.

3. **No Content Truncation** — All hunks MUST be shown in full. Lines of
   context MUST NOT be replaced with `...` or any other truncation marker.
   If the combined diff is too large for one conversation message, split the
   preview across batches ($2g) and present one batch at a time.

4. **Preview Artifact** — Write the full preview to
   `scratch/commit-preview.md` (use
   [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md)
   to ensure `scratch/` exists and is gitignored). The user can then refer to
   specific line numbers when giving feedback. Present the summary in the
   conversation as well.

Template:

````markdown
## Arranged Commits Preview

### Commit 1: [type](scope): [title]
- **Files**: [file1.md], [file2.md]
- **Message**:
  ```
  [type](scope): [title]

  [Body line 1]
  [Body line 2]
  ```
- **Hunks/Preview**:
  ```diff
  [Show actual hunks for this commit — use ~~~diff/~~~ if hunks contain ```
  ]
  ```

### Commit 2: [type](scope): [title]
- **Files**: [file3.md]
- **Message**:
  ```
  [type](scope): [title]

  [Body line 1]
  ```
---
Please say "start" to begin the sequential execution of these atomic
commits.
````

#### 2d.1 — Iterative Preview Fixup

After presenting the commit preview, the user may give feedback by line
number (e.g., "check line 98 — still broken"). Feedbacks typically
point to one of these issues in the preview:

- Wrong `@@` header (fix by verifying against actual `git diff`)
- Truncated content with `...` (restore full hunk)
- Nested fenced code blocks breaking markdown (switch to `~~~diff`/`~~~`)
- Missing context lines around changes (include the default 3-line context)

Fix, re-write the preview to `scratch/commit-preview.md`, and re-present.
Loop until the user confirms the preview is correct. Do NOT begin execution
until the user says "start".

#### 2d.2 — Post-Execution Preview Verification

After all arranged commits have been executed (or when resuming a session
that may have previously generated a commit preview), verify completion
by checking the preview against `git log`.

**Automated verification (preferred):**

Delegate to the
[`git-commit-preview-verify`](../git/basic/edit/git-commit-preview-verify/SKILL.md)
base skill:

```bash
python3 .agents/skills/git/basic/edit/git-commit-preview-verify/scripts/verify-commit-preview.py \
    --preview scratch/commit-preview.md \
    --format text
```

This parses the preview's `Commit N:` sections (any heading level),
cross-references each commit title against `git log --oneline`, and
reports done/pending status. Use `--format json` for machine-readable
output.

**Manual verification (fallback):**

1. Read `scratch/commit-preview.md` and extract each `Commit N:` title
2. Run `git log --oneline -20` and check for matching titles
3. Report which commits are done and which are pending

**Cleanup:**

Once all commits are verified as executed, delete the preview file:

```bash
# Automated (with verification gate)
python3 .agents/skills/git/basic/edit/git-commit-preview-verify/scripts/verify-commit-preview.py \
    --preview scratch/commit-preview.md \
    --cleanup

# Manual
trash scratch/commit-preview.md
```

The preview file MUST NOT be deleted until all commits are confirmed
executed. If any commits are pending, the preview must be retained for
the next session.

#### 2e — Commit Authorization

The agent **MUST NOT** proceed with any commit execution until the user
explicitly says **"start"**. Other triggers like "commit" or "go" are
insufficient.

#### 2f — Interleaving Mandate (Artifact + Registry Registration)

Whenever a commit introduces or renames an artifact **and** a shared index /
registry file (e.g., `AGENTS-legacy.md` skills table, `.gitmodules`, CI
workflow manifests) needs a corresponding row or entry for that artifact, the
registry hunk MUST be **staged in the same commit** as the artifact itself —
never batched into a separate "registration" commit at the end. This applies to:

- **New skills**: `AGENTS-legacy.md` row for the skill → same commit as the skill
  `SKILL.md` / `scripts/` files.
- **Submodule syncs**: `.gitmodules` URL change and any `AGENTS-legacy.md` row
  referencing the submodule → same commit as the submodule pointer advance.
- **Any artifact with a shared index entry**: treat the index row as part of the
  artifact's definition, not as metadata to collect last.

When the registry file contains mixed hunks (some for this artifact, some
unrelated): use `git add -p <registry>` to stage only the relevant hunk(s)
alongside the artifact files; leave unrelated hunks unstaged for their own commits.

**When `git add -p` hunk boundaries don't align with row boundaries** (e.g.,
two session rows land in the same hunk as an out-of-scope row), use the
[`agents-md-stage-row.py`](../git-hunk-staging-primitives/scripts/agents-md-stage-row.py) script instead:

```bash
# Dry-run: preview alphabetical position
python3 .agents/skills/git-hunk-staging-primitives/scripts/agents-md-stage-row.py \
    --row "| My Skill | [path](path) | description |" \
    --dry-run

# Stage exactly one row (default --mode staged: reads HEAD:AGENTS.md,
# inserts row, updates index; working tree is NOT touched)
python3 .agents/skills/git-hunk-staging-primitives/scripts/agents-md-stage-row.py \
    --row "| My Skill | [path](path) | description |"
```

In default `--mode staged`, the script reads `HEAD:AGENTS.md` (not the working
tree), inserts the row at the alphabetically correct position, writes a new
blob via `git hash-object -w`, and updates the index via
`git update-index --cacheinfo` — so only the new row is staged while all other
working-tree changes remain unstaged.

The script also supports `--mode worktree` for the skill-factory registration
case (AGENTS.md is clean and you just want the row written to the working tree
for ordinary `git status` review and `git add`). See
[`skill-factory/SKILL.md` §2.4](../skill-factory/SKILL.md) for the registration
workflow.

Forbidden anti-pattern: "commit all artifacts first, then one final commit
registers them all in AGENTS-legacy.md" — this makes individual commits incomplete
(skill exists but is not discoverable) and destroys per-feature traceability.

See [Atomic Commit Construction Rules §3.1](../../../ai-agent-rules/git-atomic-commit-construction-rules.md#31-interleaving-mandate-artifact--registry-registration).

#### 2f.1 — Deferred Cross-Reference Hunk Pattern

When two new artifacts (X and Y) ship in **separate commits B and C**, and one or
both files already contain a "Related Skills" / index row referencing the OTHER
artifact in the working tree, the cross-reference row must be deferred to whichever
commit lands the artifact it points to. Concretely: commit B (introduces X) MUST
NOT carry a row that references Y — Y does not yet exist in the tree, and the row
would dangle until commit C lands.

Three viable techniques, in order of preference:

1. **`stage-file-excluding-lines.py`** (preferred — no working-tree mutation): write
   a blob equal to the working tree minus the deferred row(s), stage it directly
   via `git update-index --cacheinfo`, leave the working tree untouched. The
   deferred rows are picked up cleanly by `git add <file>` for commit C.

   ```bash
   python3 .agents/skills/git-hunk-staging-primitives/scripts/stage-file-excluding-lines.py \
       --file .agents/skills/X/SKILL.md \
       --exclude "../Y/SKILL.md" \
       --dry-run

   python3 .agents/skills/git-hunk-staging-primitives/scripts/stage-file-excluding-lines.py \
       --file .agents/skills/X/SKILL.md \
       --exclude "../Y/SKILL.md"
   ```

   When the deferred row belongs to a larger block (section header + table +
   trailing blank), append **`--blank-context 1`** to also strip the contiguous
   blank line after each match so no orphaned section header remains in the
   staged blob:

   ```bash
   python3 .agents/skills/git-hunk-staging-primitives/scripts/stage-file-excluding-lines.py \
       --file .agents/skills/cra-reset-mocks-test-strategy/SKILL.md \
       --exclude "## Composition" \
       --exclude "Composition Mechanism" \
       --exclude "mrt-component-test-strategy" \
       --exclude "--- | ---" \
       --blank-context 1
   ```

2. **Temporary edit + restore** (when the script is unavailable): edit the file to
   remove the deferred row, `git add` it, commit B, then re-insert the row in the
   working tree for commit C. Higher risk of forgetting the restore step; use only
   as a fallback.

3. **`git add -p`** (when hunk boundaries align with row boundaries): split the
   hunk interactively. Often fails because Markdown table rows pack multiple
   logical entries into a single hunk; falls back to technique 1 or 2.

**Forbidden anti-pattern**: staging the deferred row in commit B "to keep the file
self-consistent" — the row points to an artifact that does not yet exist at
commit B, breaking checkout-at-B build/lint and destroying per-commit
traceability.

#### 2g — Batch-by-Batch Authorization (Long Sequences)

When the Arranged Commits sequence exceeds **5 commits**, split the preview
into batches of at most 5 commits and request a separate `"start"` per batch:

1. Present each batch in the full §2d verbose format before executing any
   commit in that batch.
2. After each batch executes, emit a one-line summary `Batch N committed:
   SHA1, SHA2, …` and present the next batch's preview.
3. The user MAY abort, reorder, or modify subsequent batches between
   authorizations — do NOT pre-stage files for batches that have not yet
   been authorized.
4. The first batch MUST include a top-level **Master Plan Table**
   (`# | type(scope): title | files | batch`) so the user has a single-pane
   view before authorizing batch 1.

See [Atomic Commit Construction Rules §3.2](../../../ai-agent-rules/git-atomic-commit-construction-rules.md#32-batch-by-batch-authorization-long-sequences).

#### 2h — Pre-Execution Safety Stash (Mandatory for ≥ 2 Commits)

Before executing the first commit of any sequence of two or more commits
(including any batch governed by §2g), capture an apply-not-pop safety
snapshot of the full working-tree state (tracked modifications, staged
hunks, AND untracked files) and re-apply it immediately so execution
proceeds against an unchanged tree. The snapshot persists across the
entire sequence and is verified-then-dropped only at end-of-session.

Delegate the full three-phase protocol (Snapshot → Hold → Verify-and-
Release) to [`git-pre-execution-safety-stash`](../git-pre-execution-safety-stash/SKILL.md):

- **Phase 1 — Snapshot** before the first commit: classify any
  pre-existing stashes via [`git-stash-triage`](../git-stash-triage/SKILL.md),
  push with `git stash push -u -m "safety: ..."`, immediately
  `git stash apply` (NEVER `pop`), verify parity.
  > **If `git stash apply` fails** due to live editor conflicts (VS Code,
  > Copilot, Eclipse, IntelliJ rewriting files between push and apply),
  > do NOT retry — follow the [Selective File Extraction from Stash
  > (Phase 1g)](../git-pre-execution-safety-stash/SKILL.md#1g--stash-apply-conflict-recovery-via-selective-file-extraction)
  > recovery path in `git-pre-execution-safety-stash`.
- **Phase 2 — Hold** across the sequence: never drop, pop, or clear the
  `safety:` entry mid-sequence; re-verify presence at batch boundaries.
- **Phase 3 — Verify-and-Release** after the final commit: `git stash
  apply` again, confirm the apply is a clean no-op against HEAD, then
  ask the user explicitly before `git stash drop` per
  [`git-operation-rules.md` §5](../../../ai-agent-rules/git-operation-rules.md).

See [Atomic Commit Construction Rules §3.3](../../../ai-agent-rules/git-atomic-commit-construction-rules.md#33-pre-execution-safety-stash-mandatory-for-multi-commit-sequences).

---

### Step 3 — Interactive Hunk-Based Staging

When a file contains mixed concerns, use interactive staging to
partition changes.

#### 3a — Command

```powershell
git add -p <file>
```

#### 3b — Hunk-by-Hunk Evaluation

During interactive staging, evaluate and respond to each hunk
individually (`y`, `n`, `s`, etc.). Do NOT batch responses. Every
modified line must be evaluated: "Does this line belong to the
*current* atomic goal?"

#### 3c — Granular Hygiene

If a grammatical fix is discovered while implementing a feature, it
MUST be staged and committed separately unless it is part of the same
logical chunk.

#### 3d — Verification After Staging

After staging each chunk, verify strictly atomic contents:

```powershell
git diff --cached
```

#### 3e — Discard Rejected Noise

After accepting the desired hunks and rejecting noise, discard the
rejected changes from the working tree if they are unintentional:

```powershell
git checkout -- <file>
```

#### 3f — Mixed-Concern Noise Handling Workflow

When a file contains both functional changes AND unrelated noise
(invisible characters, spurious whitespace, trailing `\r` differences),
follow this workflow:

1. **Attempt to fix the noise in the editor** — remove the spurious
   whitespace or extra blank lines directly. This may resolve it.
2. **Re-check the diff** — run `git diff <file>`. If the noise persists
   (e.g., invisible character differences that the editor cannot show),
   fall back to hunk-based staging.
3. **Stage only functional hunks** — run `git add -p <file>`, accepting
   (`y`) only the hunks that belong to the current atomic goal and
   rejecting (`n`) the noise hunks.
4. **Discard the remaining noise** — run `git checkout -- <file>` to
   revert the rejected noise from the working tree. This preserves the
   staged functional changes.
5. **Verify staged state is clean** — run `git diff --cached <file>` to
   confirm only functional changes are staged, then run `git status` to
   confirm no unstaged changes remain.

**PowerShell caveat:** Piping input to `git add -p` is unreliable in
PowerShell (standard pipe methods like `echo`, `Write-Output`, and
string joins often fail to register). Preferred workaround:

- Accept the functional hunks manually or in a sequence where piping
  works, then use `git checkout -- <file>` to discard whatever noise
  remains unstaged.

#### 3g — Post-Edit Indent Verification & Repair

Markdown edits can silently shift continuation-line indent on unrelated
lines near the edit site (common when tools re-emit fenced blocks or
when an edit operation touches adjacent lines). A `git diff` that shows
the correct content at the wrong indent is incomplete — staging it
propagates whitespace drift into the commit.

Delegate detection and repair to the
[`list-indent-consistency`](../general/list-indent-consistency/SKILL.md)
base skill.

**Acceptance criterion:** run `detect-list-indent-drift.py` on the affected
file(s); the script MUST exit 0 before `git add` is run.

See also: Common Pitfalls — `Indent drift after markdown edit silently staged`.

#### 3h — IDE Artifact Bulk Discard

IDE tooling (VS Code Java Language Server, Eclipse, IntelliJ) often
auto-modifies project metadata files across **many** sub-projects at
once — for example, adding `<filteredResources>` blocks to every
Eclipse `.project` file. These changes **may** be noise — but some
projects intentionally track IDE metadata for reproducible workspace
setup. The agent **MUST NOT** assume these are discardable.

**Detection pattern:**

- `git diff --stat` shows a large number of identical-looking changes
  (e.g., 50+ `.project` files each with exactly +11 lines)
- The diff content is the same boilerplate repeated per file
- The change was not initiated by the developer

**Common IDE artifact files to watch for:**

| Pattern | Source |
|---|---|
| `**/.project` | Eclipse / VS Code Java Language Server |
| `**/.classpath` | Eclipse JDT |
| `**/.settings/**` | Eclipse workspace preferences |
| `**/*.iml` | IntelliJ IDEA module files |
| `**/.idea/**` | IntelliJ IDEA project files |

**Tracked vs Untracked Pre-Check (Critical):**

Before discarding anything, the agent **MUST** distinguish between
**tracked** (version-controlled) and **untracked** (new/generated)
files in the affected area. This is critical because directories
like `.settings/` often contain a **mix** of tracked files (e.g.,
`org.eclipse.jdt.core.prefs` committed by the team) and untracked
files (e.g., `org.eclipse.m2e.core.prefs` auto-generated by the
JDT Language Server).

```powershell
# List tracked files under .settings/
git ls-files .settings/

# List untracked files under .settings/
git ls-files --others --exclude-standard .settings/

# For modified tracked files, show what changed
git diff --stat HEAD -- .settings/
```

**⚠️ Never bulk-delete a directory that contains tracked files.**
Using `Remove-Item ".settings" -Recurse -Force` when the directory
contains tracked files will cause those files to appear as deleted
in `git status`, requiring immediate restoration via
`git checkout -- <file>`. Instead, remove only the specific
untracked files.

**JDT Language Server + m2e Auto-Injection:**

When the JDT Language Server detects a `pom.xml`, it automatically
imports the project as Maven-managed and injects:

- `org.eclipse.m2e.core.maven2Builder` into `.project` `<buildSpec>`
- `org.eclipse.m2e.core.maven2Nature` into `.project` `<natures>`
- `.settings/org.eclipse.m2e.core.prefs` (untracked)
- `.settings/org.eclipse.core.resources.prefs` (untracked)

These are **not** from the VS Code Maven extension
(`vscjava.vscode-maven`) — that extension provides the UI only.
The `.project` modifications come from the **Eclipse JDT Language
Server** (`eclipse.jdt.ls`) which bundles **m2e** internally.

**Mandatory User Confirmation Workflow:**

The agent **MUST** present suspected noise to the user and obtain
explicit confirmation before discarding. Never silently discard
changes to IDE metadata files — the project may rely on them.

1. **Present the suspected noise** — Show the user a categorized
   summary separating modified tracked files from untracked files,
   and include the proposed discard steps:

   ````markdown
   ## Suspected IDE Artifact Noise

   ### Modified Tracked Files
   | File | Change | Source |
   |---|---|---|
   | `.project` | +17 lines (Maven builder/nature + filteredResources) | JDT LS / m2e auto-import |

   ### Untracked Files (IDE-generated)
   | File | Content | Source |
   |---|---|---|
   | `.settings/org.eclipse.m2e.core.prefs` | m2e workspace config | JDT LS m2e import |
   | `.settings/org.eclipse.core.resources.prefs` | Encoding `Cp1252` | Eclipse workspace |
   | `.gitignore` | `/bin/` | Possibly auto-generated |

   ### Already-Tracked Files (will NOT be touched)
   | File | Status |
   |---|---|
   | `.settings/org.eclipse.jdt.core.prefs` | ✅ Tracked, unchanged — preserved |

   **Proposed discard steps:**
   ```powershell
   # 1. Revert modified tracked file
   git checkout -- .project

   # 2. Remove specific untracked files (NOT the whole directory)
   Remove-Item ".settings/org.eclipse.m2e.core.prefs" -Force
   Remove-Item ".settings/org.eclipse.core.resources.prefs" -Force
   Remove-Item ".gitignore" -Force

   # 3. Verify
   git status --short
   ```

   **⚠️ Warning:** `.settings/org.eclipse.jdt.core.prefs` is tracked
   and will be preserved. The discard targets only IDE-generated noise.

   Should I discard these changes? (yes / no / inspect further)
   ````

2. **Act on user feedback:**
   - **"yes" / "discard"** — Execute the proposed discard steps
     **exactly as presented**, then verify with `git status --short`.
   - **"no" / "keep"** — Leave the changes in the working tree.
     They may be staged as a separate commit (e.g.,
     `chore: update Eclipse project metadata`) or left for later.
   - **"inspect further"** — Show full diffs for additional files
     so the user can distinguish intentional changes from noise.
   - **Partial discard** — If the user identifies some files as
     intentional and others as noise, discard only the confirmed
     noise files individually.

3. **Post-discard verification:**

   ```powershell
   git status --short
   git diff --stat HEAD
   ```

   If any tracked file appears as deleted (accidentally removed),
   restore it immediately:

   ```powershell
   git checkout -- <accidentally-deleted-file>
   ```

**Prevention:** Add IDE artifact patterns to `.gitignore` if the
project does not require IDE metadata to be version-controlled. If
the project *does* track them, coordinate with the team on which
metadata files are shared vs personal before discarding.

#### 3h — Hunk-Stage Backup Cleanup (Sidecar Discipline)

Every `git add -p` session, every in-editor `e` (edit-hunk) action,
and every programmatic `git apply` with a manually authored patch
may leave a sidecar file on disk: `<file>.orig`, `<file>.bak`,
`<file>.full.bak`, `<file>.rej`, `<file>.staging-tmp`, etc. These
sidecars MUST be detected and disposed of before the commit lands,
never absorbed into it.

Four-step protocol (Detect → Classify → Verify → Never-`add`):

1. **Detect** after each `git add -p` and after any `e`/`apply`:

   ```powershell
   git status --short | Select-String -Pattern '\.(orig|bak|full\.bak|rej|staging-tmp)$'
   ```

   The output MUST be empty before the commit.

2. **Classify** every detected sidecar:
   - **Recoverable** — content the agent or user still needs (e.g., a
     `.rej` requiring manual re-application, or a `.full.bak` from
     an aborted edit). Move it OUT of the working tree (e.g., to
     `<workspace-root>/../scratch/` or a personal-sandbox branch).
   - **Disposable** — content already represented in the index, HEAD,
     or another branch. Delete directly.

3. **Verify** before committing: re-run the §3h detect command and
   confirm zero matches. Sidecars MUST NOT be added to `.gitignore`
   as a substitute for cleanup — that hides the symptom and lets the
   next session re-encounter the same disposal decision blind.

4. **NEVER `git add` a sidecar** "to clean up history later". The
   commit itself is the disposal decision; once a sidecar reaches the
   index, the only safe recovery is `git reset HEAD -- <sidecar>`
   followed by the classification above.

This rule composes with §2h (Pre-Execution Safety Stash): the safety
stash captures the pre-execution working tree once; the sidecar
cleanup happens per `add -p` invocation inside that window.

See [Atomic Commit Construction Rules §4.3](../../../ai-agent-rules/git-atomic-commit-construction-rules.md#43-hunk-stage-backup-cleanup-sidecar-discipline).

#### 3i — Selective Hunk Extraction via Diff Patching

When `git add -p` hunk boundaries don't align with the logical boundary
(common in Markdown table rows, contiguous prose sections, or adjacent
list items), and the complementary `stage-file-excluding-lines.py` (§2f.1)
is the wrong tool because you want to stage ONLY the matching content
(rather than exclude it), use the `stage-hunk-from-diff.py` script:

This script reads the file's diff, parses it into hunks, keeps only
hunks whose content matches one or more `--match` / `--match-regex`
patterns, and stages them via `git apply --cached`. Non-matching hunks
remain unstaged; the working tree is never modified.

```bash
# Dry-run: preview matched hunks without staging
python3 .agents/skills/git-hunk-staging-primitives/scripts/stage-hunk-from-diff.py \
    --file .agents/skills/foo/SKILL.md \
    --match "blockquote" \
    --check

# Stage only hunks containing a specific substring:
python3 .agents/skills/git-hunk-staging-primitives/scripts/stage-hunk-from-diff.py \
    --file .agents/skills/foo/SKILL.md \
    --match "Phase 1g"

# Stage hunks matching ANY of multiple patterns:
python3 .agents/skills/git-hunk-staging-primitives/scripts/stage-hunk-from-diff.py \
    --file .agents/skills/foo/SKILL.md \
    --match "stash-apply" \
    --match "live editor"

# Stage hunks from a regex pattern:
python3 .agents/skills/git-hunk-staging-primitives/scripts/stage-hunk-from-diff.py \
    --file .agents/skills/foo/SKILL.md \
    --match-regex "Phase\s+1[g-h]"

# Stage hunks from the staged diff (--cached) instead of the working tree:
python3 .agents/skills/git-hunk-staging-primitives/scripts/stage-hunk-from-diff.py \
    --file .agents/skills/foo/SKILL.md \
    --match "submodule" \
    --cached
```

**How it works:**

1. Runs `git diff [--cached] -- <file>` to capture the full patch.
2. Parses the unified diff into a header (before the first `@@`) and a
   list of hunks (each `@@ ... @@` block with its context and changes).
3. For each hunk, checks whether ANY of the `--match` substrings or
   `--match-regex` patterns appear anywhere in the hunk text (context
   lines, old lines, AND new lines).
4. Reconstructs a filtered patch from the header + matching hunks only.
5. Runs `git apply --cached` with the filtered patch to stage exactly
   those hunks into the index. Non-matching hunks remain unstaged.

**Complementary primitives (delegated to base skill `git-hunk-staging-primitives`):**

| Script | Action | Used in |
|---|---|---|
| `stage-hunk-from-diff.py` | Stage ONLY matching hunks | §3i (this section) |
| `stage-file-excluding-lines.py` | Stage file MINUS matching lines | §2f.1 |
| `agents-md-stage-row.py` | Stage exactly one AGENTS.md row | §2f |
| `stage-head-synthesize.py` | Stage HEAD with substitutions | §13 |
| `stage-specific-hunks.py` | Stage specific hunk indices | §3i.1, §13 |
| `git add -p` | Interactive hunk-by-hunk staging | §3a–§3f |

**Edge cases:**

- **Zero hunks matched:** exits with error. Use `--check` to preview.
- **File has no diff:** exits with error (nothing to extract).
- **Filtered patch wouldn't apply:** `--check` reveals the issue.
  Common causes: the index has drifted from HEAD (e.g., some changes
  already staged for this file). Use `--cached` to target staged
  changes, or commit/reset the existing staged content first.

**See also:** `stage-hunk-from-diff.py --help` for full argument docs.

#### 3i.1 — Adjacent-Lines Isolation (git add -p Split Failure Fallback)

When `git add -p` presents a single hunk with multiple adjacent
added or deleted lines and `s` (split) returns "Sorry, cannot split
this hunk," the lines are too close (no intervening context line) for
Git's hunk-split algorithm. `stage-hunk-from-diff.py` (§3i) stages
the ENTIRE hunk when ANY line matches your filter — it cannot isolate
individual adjacent lines within a hunk.

**Preferred fallback:** `stage-file-excluding-lines.py` (§2f.1) stages
the file with the unwanted line(s) EXCLUDED, leaving the working tree
untouched. The excluded line stays on disk and is picked up cleanly by
`git add <file>` in the next commit.

**Example — two adjacent additions, each needs its own commit:**

```bash
# Commit 1: stage the file minus the second addition
python3 .agents/skills/git-hunk-staging-primitives/scripts/stage-file-excluding-lines.py \
    --file <file> \
    --exclude "<content-of-second-line>"

git commit …   # only the first line change is committed

# Commit 2: HEAD now has the first line; working tree still has both.
# git add sees only the second line as a delta from HEAD:
git add <file>
git commit …   # only the second line change is committed
```

**How it works** (re-stated for this use case, SSOT is §2f.1):

1. Reads the CURRENT working-tree version of `<file>`.
2. Removes every line matching `--exclude`.
3. Writes the result as a new blob via `git hash-object -w`.
4. Updates the index entry via `git update-index --cacheinfo`.
5. Working tree is never modified — the excluded line persists on disk.

**Why prefer this over manual editing (Intermediate State Synthesis,
§13):**

- Zero working-tree mutation — no risk of forgetting the restore step.
- The index blob is computed from the exact working-tree content
  (minus matched lines) — no accidental whitespace drift from a
  manual copy.
- Audit trail: the script logs the excluded line content + blob SHA
  to stderr.

**When manual editing is still appropriate (fallback to §13):**

- The script is unavailable (no `.agents/` tree, or Python not on PATH).
- Lines to exclude span multiple non-adjacent positions (one
  `--exclude` call handles one line; for scattered exclusions, manual
  may be faster).

---

### Step 4 — Formatting & Structural Partitioning

Stylistic and structural changes MUST be explicitly separated from
functional commits.

#### 4a — Formatting & Stylistic Consolidation

**Target:** Purely aesthetic changes — indentation, whitespace,
Markdown header-level corrections, single blank line adjustments.

**Rule:** If multiple files require these adjustments, club them into a
single dedicated commit. Commit type: `style`.

**Trivial hunks:** A single blank-line insertion or removal (e.g.,
missing blank line before a code block in a skill doc) is a
formatting-only change. Use `git add -p` to isolate that hunk from any
functional changes in the same file, then commit it separately as a
`style:` commit. See
[`separate-content-from-formatting-commits`](../separate-content-from-formatting-commits/SKILL.md)
for complex cases (pervasive reformatting mixed with content changes).

#### 4b — Structural Refactor Isolation

**Target:** Functional-preserving reorganizations — alphabetical
reordering of methods, variables, or constants.

**Rule:** Isolate into dedicated commits. Commit type: `refactor`.
Large structural reorders should be committed per-file or
per-logical-group for clear "move" history.

#### 4c — Zero Mixture

Never mix formatting (4a) with structural refactors (4b) or functional
logic (Step 2). Use `git add -p` or Intermediate State Synthesis
(Step 12) to ensure absolute partitioning.

---

### Step 5 — Configuration Coupling

Tool configurations and metadata MUST be atomically linked to the code
they support.

- **Functional Pairing:** Updates to `.vscode/settings.json` (e.g.,
  cSpell words), `.lintrc`, or other config files MUST be staged and
  committed alongside the functional changes that necessitate them.
- **IDE Project Files:** Shared IDE config files (`.idea/` core XMLs,
  `.vscode/` shared settings) that establish project structure MUST be
  tracked. Personal settings (e.g., `workspace.xml`) MUST remain ignored.
- **Example:** If adding a new rule file introduces technical terms, the
  cSpell update for those terms MUST be part of the same atomic unit.

---

### Step 6 — Submodule Synchronization Protocol

When managing submodules, the main repository's history must remain descriptive and clear.

- **Submodule-First Discipline**: All submodule commits MUST be completed
  BEFORE handling any parent-repository work. Submodule work is highest
  priority; parent sync follows immediately after.
- **Synchronized Commits**: Every functional update in a submodule requiring a
  pointer update in the main repo MUST be coupled with its relevant main-repo
  configuration changes (e.g., CI scripts or IDE settings).
- **Orchestration**: Delegate metadata extraction to the
  **[Git Submodule Commit Details](../git-submodule-commit-details/SKILL.md)**
  skill to ensure zero-omission fidelity.
- **Commit Message Generation**: All submodule sync commits MUST follow the
  strict formatting, chronological ordering, and metadata requirements defined in
  **[Submodule Sync Commits](../../../ai-agent-rules/git-commit-message-rules.md#5-submodule-sync-commits-parent-repository)**.
- **Submodule History Integrity**: Before updating a submodule pointer in the
  parent repository, the changes *within* the submodule MUST be committed
  according to these exact atomic construction rules. A "dirty" or
  uncommitted submodule state is prohibited during a parent-repo sync.

### Step 7 — Parent Sync Offer & Change Grouping

Immediately after finalizing all submodule commits, the agent MUST evaluate the
parent repository.

#### 7a — Parent State Analysis

1. Check if the containing parent repo exists and tracks current dir as submodule.
2. Verify parent's recorded SHA differs from submodule HEAD → stale pointer confirmed.

#### 7b — Related Parent Changes Detection

- **Inventory parent changes**: Run `git -C <parent-path> status` to list all
  modified/untracked files in the parent.
- **Determine coupling**: Are any parent changes **directly related** to the
  submodule commit (e.g., implementing the rule just added, updating CI to use
  the new submodule feature, docs that reference the new behavior)?
    - **Yes** → Group with the submodule SHA sync in a **single unified commit**.
    - **No** → Keep parent sync minimal (SHA-only), commit related changes
    separately afterward.

#### 7c — Arranged Commit Preview

Present the parent sync commit using full arranged commit format (§4). Include
both the submodule SHA delta and any grouped parent-side changes in the message body.

#### 7d — Execution Prompt

```text
The parent repository needs a submodule SHA update. Execute sync?
```

- On **"yes"** → Execute the presented commit immediately.
- On **"no"** or ambiguous → Do NOT commit; await explicit directive.
- **Never auto-push** — push offers come AFTER commit execution, never before.

#### 7e — Post-Sync Cleanup

If parent-side unrelated changes were detected but NOT grouped, they remain in
the parent working tree as separate atomic units. Arrange and commit them
independently following the standard protocol.

---

### Step 8 — Generated vs Custom File Splitting

When a file contains both standard API-generated content (e.g., from
gitignore.io) and user-defined custom rules, split into separate commits.

- **Commit A (Foundation):** Commit only the standard, API-generated
  portion first. Back up the full file, overwrite with the exact API
  content, and commit. This establishes a clean, reproducible baseline.
- **Commit B (Customization):** Commit the user-defined sections in a
  subsequent commit. This clearly distinguishes "standard boilerplate"
  from "project-specific logic."
- **User Modifications:** If the user has altered the API-generated
  portion, separate those alterations from the raw API import if
  possible, or document clearly as user-patches.

---

### Step 9 — Commit Message Quality Standards

Every commit message MUST meet these quality requirements:

| Requirement | Detail |
|---|---|
| **Specificity** | Avoid generic titles. List specific components (e.g., `add linux, macos, and windows gitignore rules` not `os-specific`) |
| **Anti-Repetition** | The body MUST NOT merely rephrase the title |
| **Context Enrichment** | Explain the 'Why' — especially for architectural or security decisions |
| **Atomic Rationale** | The body MUST state WHY these specific changes are grouped together. If multiple files, explain their functional coupling |
| **Constraint Documentation** | Mention constraints or external dependencies that influenced grouping |
| **Contextual Accuracy** | Use precise terms (e.g., "Supabase project-specific" not generic "project-specific") |
| **Body/Diff Congruence** | The message body MUST be a complete, accurate summary of ALL changes in the staged hunks. Any discrepancy requires an immediate corrected preview |

---

### Step 10 — Execution & Verification

#### 9a — Step-by-Step Execution

Execute commits one-by-one according to the approved arrangement.
**Chaining commands (e.g., `git add . && git commit`) is FORBIDDEN.**
Each command MUST be issued as a separate step so the user can inspect
intermediate state (`git status`, diff, preview) before authorizing the
next action. Chaining suppresses this verification window.

#### 9a.1 — Pre-Commit Sync Refresh (Mandatory before every commit)

The Step 0e upstream check goes stale the moment time passes (preview,
user authorization, staging). Planning-stage sync is NOT enough. After
`git diff --cached` verification and BEFORE each `git commit`:

1. Run `git fetch origin` (non-mutating, safe without approval) and
   compare `HEAD` against `origin/<branch>`.
2. If the branch is behind, STOP — do NOT commit. Report the divergence
   and ask the user whether to `git pull --rebase` or merge (per
   [`git-operation-rules.md`](../../../ai-agent-rules/git-operation-rules.md),
   pull/rebase requires explicit approval). Commit only after sync.
3. Repeat this refresh before EVERY commit in a multi-commit sequence,
   not just the first — each commit gets its own fetch-and-compare.

#### 9b — Recovery

If a mistake is made during staging:

- **Unstage:** `git reset <file>`
- **Selective discard:** `git checkout -p`
- **WARNING:** Never use `git reset --hard` for synchronization.
  Always prefer `git pull`.

#### 9c — Pull Before Push

Always `git pull` (or `git pull --rebase` upon explicit approval) before
pushing to incorporate latest remote changes.

#### 9d — Opaque Content Analysis

For files flagged as binary or large assets (LFS), verify internal
consistency by inspecting file contents (e.g., `cat -v` or hex dump) to
ensure the commit message accurately reflects the data being stored.

#### 9e — History Refinement Delegation

If existing commits need to be split or refined (e.g., to fix non-atomic
changes), delegate to the
[`git_history_refinement`](../git-history-refinement/SKILL.md) skill.

#### 9f — Stash Workflow for Rebase

If rebase fails due to unstaged changes:

```powershell
git stash push -m "Descriptive message"
git pull --rebase origin <branch>
git stash pop
```

If `git stash pop` creates conflicts, resolve manually, then:

```bash
PAGER=cat git add <resolved-files>
PAGER=cat git stash drop
```

> **Stash preservation rule:** `git stash drop`/`pop`/`clear` are destructive and require explicit per-stash user
> authorization — even inside a "cleanup" batch. See
> [`git-operation-rules.md` §5 — Stash Preservation](../../../ai-agent-rules/git-operation-rules.md) for the
> Inventory → Inspect → Authorize → Act protocol and recovery window. For triage of pre-existing stashes whose
> origin is unclear (Bucket A/B/C/D classification, hang-free inspection, apply-not-pop), use
> [`git-stash-triage`](../git-stash-triage/SKILL.md).
>
> **Stash provenance note:** Before applying or popping a stash, consider checking its origin commit to understand
> what state it was created from. Use the [`git-stash-parent-commit`](../git-stash-parent-commit/SKILL.md) base skill:
> `& "<skill-path>/scripts/get-stash-parent.ps1" -StashRef stash@{n}` outputs the commit hash and subject
> that was HEAD when the stash was created.

#### 9g — Corrupted Rebase State Recovery

If `git rebase --continue` or `git rebase --abort` fails with
`warning: could not read '.git/rebase-merge/head-name'`, the
`.git/rebase-merge` directory is likely empty or corrupted.

**Diagnostic:**

```powershell
Test-Path ".git/rebase-merge"           # True = directory exists
Get-ChildItem ".git/rebase-merge"       # Empty = corrupted state
```

**Resolution:**

1. **Verify staged changes are intact** — run `PAGER=cat git diff --cached` to
   confirm your staged work is preserved.
2. **Remove the corrupted directory:**

   ```powershell
   Remove-Item ".git/rebase-merge" -Recurse -Force
   ```

3. **Verify clean state** — run `PAGER=cat git status` to confirm the rebase
   state indicator is gone.
4. **Commit directly** — since the rebase state is cleared, use a
   normal `PAGER=cat git commit` with the planned message instead of
   `PAGER=cat git rebase --continue`.

#### 9h — Pre-Existing Staged Content Handling

Before staging files for a new commit, check whether the index already
contains staged changes from a prior operation (previous commit,
interrupted workflow, or manual staging):

```bash
git diff --cached --stat
```

If the output is **non-empty**, pre-existing staged content exists. The
agent MUST:

1. **Present** the pre-existing staged content to the user with a warning.
2. **Unstage** it if it does not belong to the current commit:

   ```bash
   git reset HEAD -- .
   ```

3. **Re-verify** with `git diff --cached` that the index is now clean.
4. **Stage only the files intended** for the current atomic commit.

This prevents accidental inclusion of stale staged content. The `git reset
HEAD -- .` command only unstages files — it does NOT discard working-tree
changes.

#### 9i — Commit Message Delivery (Safe Pattern)

Delegated to the
[`git-commit-message-delivery`](../git-commit-message-delivery/SKILL.md)
base skill. Apply the **heredoc → `-F`** pattern (§1.2) for all multi-line
or special-character commit messages:

```bash
cat > /tmp/commit_msg <<'EOF'
<type>(<scope>): <title>

<body>
EOF

git commit -F /tmp/commit_msg
rm -f /tmp/commit_msg
```

Do NOT use `git commit -m '...'` when the message is multi-line or contains
shell-special characters (`'`, `$`, `` ` ``). See the base skill for the
complete pattern reference and selection criteria.

#### 9j — Post-Commit Verification

After each commit executes, verify its file set using `--name-only`, not
`--stat`:

```bash
git show --name-only HEAD
```

`git show --stat` truncates long file paths with `.../`, which causes `grep`
(or `Select-String`) to miss matches. `--name-only` outputs every path in
full, one per line, and is safe for programmatic matching.

Verify three things:

1. **File set is correct** — the committed files match what was staged.
2. **Count matches** — the number of committed files equals the expected
   number.
3. **No unintended files** — no sidecar files (`.orig`, `.bak`, `.rej`) or
   IDE artifacts leaked into the commit.

If the file set is wrong, diagnose via `git diff HEAD~1..HEAD` and correct
before the next commit.

---

### Step 11 — Logic-Documentation Compass

Visualize the commit history as a compass where each direction is a
logical area:

| Direction | Area |
|---|---|
| **North** | Architectural / Schema changes |
| **East** | Logic / Feature implementation |
| **West** | Testing / Verification |
| **South** | Documentation / Refinement |

A high-quality commit history moves clearly through these directions
without "spinning" (mixing logic and documentation in one commit).

#### External Tool Asset Granularity

When versioning assets for external tools (Postman, Insomnia, DBeaver),
maximize granularity by separating:

- **Environments:** Endpoints, variables, credentials
- **Collections:** Logical groupings of requests, tests, scripts
- **Data Tables:** CSV/JSON templates for bulk-run or validation

Never group these into a single generic `test(tooling)` commit if they
serve distinct purposes.

---

### Step 12 — Source Logic & Generated Files

#### 11a — Update the Source, Not the Output

Never manually edit generated files. Always update the source logic
(templates, scripts, CI/CD workflows) that produces them:

- `README.md` from `templates/README.md.template` → edit the template
- Build artifacts, compiled code → edit source code or configuration

#### 11b — Identify Synchronization Mechanisms

Before making changes:

1. **Detect Generation:** Check for `<!-- AUTO-GENERATED -->` comments,
   build scripts, or CI/CD workflows that regenerate files.
2. **Locate Source:** Find the template, script, or configuration that
   produces the generated file.
3. **Document Sync:** Note in commit messages if manual synchronization
   is required (e.g., "Run `npm run build` to regenerate").

#### 11c — CI/CD Managed File Exclusion

Files managed by CI/CD automation MUST be excluded from manual edits.

- Maintain an explicit exclusion list (e.g., `README.md`,
  `agent-rules.md`)
- When verifying link updates, use `--exclude` flags:

```powershell
git grep -r "old-name.md" . --exclude-dir=.git --exclude=README.md
```

- Before committing, run `git diff --cached` and verify no CI/CD managed files are staged unless
  the commit explicitly targets the source logic that generates them.

---

### Step 13 — Intermediate State Synthesis

When a file contains interleaved changes or massive structural reorders
(50+ lines moved) mixed with functional fixes, hunk-based staging may
become unreliable. This also applies when `git add -p` hunk splitting
fails on **adjacent added or deleted lines** that must go into separate
commits — see §3i.1 for the scripted fallback.

#### Preferred: Scripted Fallback (no working-tree mutation)

When `git add -p` split fails and the unwanted content is isolated to
single lines, prefer `stage-file-excluding-lines.py` over manual
editing:

1. **Isolate with script:** Run
   `stage-file-excluding-lines.py --file <f> --exclude "<unwanted-line>"`
   to stage only the desired line(s) via a cacheinfo blob (§3i.1).
   Working tree is untouched — zero risk of forgetting a restore step.
2. **Commit:** Commit the staged intermediate version.
3. **Iterate:** `git add <f>` picks up the remaining lines as unstaged
   deltas from the new HEAD. Repeat for the next commit.

See [§3i.1](#3i1--adjacent-lines-isolation-git-add--p-split-failure-fallback)
for the full procedure, invocation examples, and the decision of when
to fall back to manual editing.

#### Fallback: Manual De-construction (The Synthesis Strategy)

When the scripted fallback is unavailable (no `.agents/` tree, Python
not on PATH), or unwanted content spans multiple non-adjacent positions:

1. **De-construct:** Manually edit the file (or use selective
   undo/revert) to match the current atomic goal BEFORE staging.
2. **Stage & Commit:** Stage the "synthesized" intermediate version that
   contains ONLY the intended logical unit.
3. **Iterate:** Repeat for remaining changes until the working directory
   is clean.

This guarantees that even high-entropy working states can be refactored
into pristine, industrial-grade commit history.

**Formatter-mixed files (JSON, YAML, config):** When a tool (editor,
runtime, formatter) has also reformatted the file, the diff is too noisy
for manual de-construction. Use the dedicated
[`separate-content-from-formatting-commits`](../separate-content-from-formatting-commits/SKILL.md)
skill, which automates intermediate-state building via Python helpers that
preserve the original format across all content commits and optionally
append a single `style:` reformat commit at the end.

#### HEAD-Synthesis Staging (cacheinfo-based)

When the desired intermediate state can be expressed as the committed HEAD
version with a set of mechanical substitutions (e.g., replace all occurrences
of `<private-config-repo>` with `<private-repo>`), use `stage-head-synthesize.py`
to stage a HEAD-derived blob directly — no working-tree file is touched.

1. **Synthesize and stage:** Run
   `stage-head-synthesize.py --file <f> --replace "old|new"` to read
   HEAD:`<f>`, apply the replacements, write a new blob, and stage it via
   `git update-index --cacheinfo`. The working tree remains unchanged.
2. **Commit:** Commit the staged intermediate version.
3. **Iterate:** `git add <f>` picks up the remaining working-tree delta from
   the new HEAD. Repeat for the next commit.

This fills the gap between `stage-file-excluding-lines.py` (working-tree-based
exclusion) and `agents-md-stage-row.py` (AGENTS.md-row-only). All three scripts
are siblings under `scripts/`:

- `agents-md-stage-row.py` — HEAD + one new row, alphabetically inserted.
- `stage-file-excluding-lines.py` — working tree minus matching lines.
- `stage-head-synthesize.py` — HEAD with mechanical substitutions.
- `stage-hunk-from-diff.py` — selective hunk staging from a diff.

See also [`stage-head-synthesize.py`](../git-hunk-staging-primitives/scripts/stage-head-synthesize.py) for
invocation examples and safety guards.

---

### Step 14 — User-Requested Coupling & Deviations

If the user explicitly requests coupling unrelated changes or deviating
from atomic rules:

1. **Warn First:** Explicitly warn: "This coupling technically violates
   Rule [X] because [reason]."
2. **Explicit Override:** Accept the coupling ONLY if the user
   re-confirms after the warning.
3. **Documentation:** Document the deviation rationale in the commit
   message body (e.g., "Coupled with IDE updates per user request for
   atomic convenience").

---

### Step 15 — Push Protocol

After commits are complete, follow the push protocol:

- **Explicit Request Required:** Do NOT execute `git push` unless the
  user explicitly requests it.
- **Offer, Don't Execute:** After commits, OFFER to push. Wait for
  explicit "yes" or `git push` command.
- **Status Check:** Always run `git status` before push.
- **Discover Default Branch:** Do NOT assume the default branch name.
  Discover it programmatically:

```powershell
git branch -r
```

---

### Step 16 — Guardrail Against Predictive Planning

The agent must never "commit" in a plan to what will be changed in the
future. Commit construction is a **Real-Time Analysis** task. The plan
serves only as a roadmap for the **Protocol** of commitment, not the
**Content** of the commits themselves. Logic for commit construction must
be synthesized from real-time analysis, never mocked in a plan.

---

## Scope Coverage

| Category | Convention |
|---|---|
| Functional changes | One logical unit per commit |
| Formatting / style | Dedicated `style` commit |
| Structural refactors | Dedicated `refactor` commit |
| Config updates | Coupled with their functional change |
| Submodule pointer updates | Descriptive title, coupled with main-repo config |
| Submodule commit auto-sync | Automatic parent repo SHA update offer after every submodule commit; execute on user "yes" |
| Generated vs custom content | Split into Foundation + Customization commits |
| CI/CD managed files | Excluded from manual edits |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Auto-committing** — Never commit without explicit user "start"
  authorization
- **Auto-pushing** — Never push without explicit user request
- **Mixing concerns** — Never combine formatting + logic + refactor in
  one commit
- **Staging untracked files without confirmation** — Especially in repos
  with minimal `.gitignore`
- **Using `git reset --hard` for synchronization** — Use `git pull`
  instead
- **Skipping the commit preview** — The verbose arranged commits display
  is mandatory
- **Excluding untracked files from initial analysis** — Untracked files
  MUST be included in the Step 1 inventory alongside staged and unstaged
  changes; discovering them post-commit is a protocol violation
- **Predicting commit content in plans** — Commits are built from
  real-time analysis only
- **Editing generated files directly** — Update the source logic instead
- **Using generic commit messages** — Every message must be specific and
  non-repetitive
- **Command chaining (`&&`)** — Chaining `git add . && git commit && git push`
  (or any variant) suppresses per-step verification and is FORBIDDEN
- **Batching hunk responses** — Each hunk must be evaluated individually
- **Skipping empty commits without user confirmation** — During rebase
  operations
- **Bulk-deleting directories with mixed tracked/untracked files** —
  Never `Remove-Item` a directory that contains tracked files; remove
  only specific untracked files to avoid accidental deletions

## Related Skills

- **[Git Submodule Commit Details](../git-submodule-commit-details/SKILL.md)**
  — MANDATORY for extracting metadata during parent-repo sync commits (Step 6).
- **[Git Commit Metadata Extraction](../git-commit-metadata-extraction/SKILL.md)**
  — The foundational primitive for all high-fidelity extraction.
- **[Git Commit Preview Verify](../git/basic/edit/git-commit-preview-verify/SKILL.md)**
  — Base skill for post-execution verification of commit previews (§2d.2).
- **[Git History Refinement](../git-history-refinement/SKILL.md)**
  — For splitting or refining non-atomic existing commits.
- **[Claude Config Change Gate](../claude-config-change-gate/SKILL.md)**
  — Pre-flight check: before any commit workflow against a repo with
  auto-timestamped claude config files, run this gate first. If it
  BLOCKS, only trivial timestamp changes exist and the commit SHOULD
  be cancelled. If it PASSES or the repo has no claude config files,
  the atomic commit workflow proceeds normally.
- **[Repo Scratch Output Capture](../repo-scratch-output-capture/SKILL.md)**
  — For writing the commit preview artifact to `scratch/commit-preview.md`
  (§2d mandate 4) with the `ensure-scratch-gitignored.py` helper.
- **[Git Hunk Staging Primitives](../git-hunk-staging-primitives/SKILL.md)**
  — Base skill providing all 5 hunk-staging primitives via public CLI
  contract: `stage-file-excluding-lines.py`, `stage-hunk-from-diff.py`,
  `agents-md-stage-row.py`, `stage-head-synthesize.py`,
`stage-specific-hunks.py`. This skill is a composer: it does NOT
   re-implement hunk-staging primitives; it orchestrates the base skill.
- **[Git Commit Dangling-Link Audit](../git-commit-dangling-link-audit/SKILL.md)**
  — MANDATORY pre-flight before finalizing any preview that
  reorders/moves paths: run the link classifier, then Gate 4 on ranges.

## Composition Rationale

This skill is a **composer**: it does NOT re-implement hunk-staging primitives.
It orchestrates the base skill `git-hunk-staging-primitives` via its public
CLI contract. The base skill owns the 5 generic primitives
(`stage-file-excluding-lines.py`, `stage-hunk-from-diff.py`,
`agents-md-stage-row.py`, `stage-head-synthesize.py`,
`stage-specific-hunks.py`) as domain-agnostic deterministic Tier-A scripts.
This skill adds the domain-specific logic: commit-preview quality mandates
(§2d), deferred cross-reference handling (§2f.1), adjacent-lines fallback
(§3i.1), HEAD-synthesis (§13), and the full atomic commit construction
protocol (§0–§16). Inlining the primitives would split the SSOT and force
other composers (`git-history-refinement`, `git-pre-execution-safety-stash`)
to duplicate them.

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Scanned with `Get-ChildItem` and got false positives | Use `git ls-files` as source of truth for tracked files |
| `.gitignore` negation patterns missed | Read `.gitignore` carefully — `!dir/*.zip` means those zips ARE tracked |
| `.gitignore` references to renamed directories not updated | `.gitignore` is a critical blast-radius target — update patterns or tracked files become untracked |
| `git mv` failed on empty directory | Empty dirs aren't tracked by Git — use `Rename-Item` or `mv` instead |
| `git add -p` split rejected on adjacent added/deleted lines | Use `stage-file-excluding-lines.py --exclude "<unwanted-line>"` (§3i.1) to stage only the desired line(s); commit; then `git add` the remaining lines as the next commit's delta. Prefer this over manual file editing. |
| Noise from unrelated hunks leaked into functional commit | Use `git add -p` and verify with `git diff --cached` after staging |
| Formatting fix discovered during feature work | Stage and commit separately via hunk-based staging |
| Committed half a logical change across two commits | If file A depends on file B's change, they MUST be in the same commit |
| Untracked files discovered only after committing staged/unstaged changes | Include ALL three categories (staged + unstaged + untracked) in the initial Step 1 inventory — untracked files are first-class scope members |
| CI/CD managed file manually edited | Check for auto-generation markers and CI workflows before editing |
| Piped input to `git add -p` didn't register in PowerShell | Use file-based input or discard noise via `git checkout --` after accepting desired hunks |
| Corrupted rebase state (`rebase-merge` dir empty) | Remove empty `.git/rebase-merge` directory to clear the broken state |
| Commit message body just rephrases the title | Body must add WHY, not repeat WHAT |
| Submodule pointer updated without verifying remote | Always verify the referenced commit exists in the remote submodule repo |
| Cross-reference row to a not-yet-created artifact leaked into the earlier commit | Use `stage-file-excluding-lines.py --exclude <pointer>` (§2f.1) to stage the file minus the deferred row; the row stays in the working tree for the later commit |
| Submodule sync commit follows legacy formatting | Always use 'Changes' and 'Metadata' headers and include chronological logs |
| IDE auto-modified 50+ `.project` / `.classpath` files with boilerplate | Present suspected noise to user with sample diff and proposed discard command; never auto-discard — project may intentionally track IDE metadata |
| Bulk-deleted `.settings/` directory and a tracked file disappeared | Use `git ls-files .settings/` to identify tracked files first; remove only specific untracked files, never the whole directory |
| Assumed Maven nature/builder in `.project` came from `vscjava.vscode-maven` | The `.project` modifications come from **JDT Language Server** (embedded m2e), not the Maven UI extension; attribute correctly when presenting to user |
| Indent drift after markdown edit silently staged | Discover correct indent via `pathlib.Path.read_text().splitlines()` `repr` scan of unmodified siblings; repair with a targeted Python `write_text`; re-verify before `git add` — do not stage drifted whitespace. See `§3g`. |
| Commit preview shows wrong `@@` line numbers | Verify every `@@` header against actual `git diff --unified=3 -- <file>` before writing the preview — never estimate from memory |
| Markdown preview breaks when diff contains fenced code blocks | Wrap the diff in `~~~diff`/`~~~` instead of ` ```diff `/` ``` ` — backtick fences inside a backtick-fenced block terminate the outer block prematurely |
| Commit preview lines refer to wrong line numbers after edits | Re-run `git diff` to get fresh `@@` headers after any working-tree change and re-write the preview |
