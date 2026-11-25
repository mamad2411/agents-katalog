---
name: git-commit-message-reword
description: Composer — reword a single existing commit's message into
    Conventional Commits format compliant with the project's commit
    message rules, delegating the rebase mechanics to git-commit-edit.
category: Git & Repository Management
---

# Git Commit Message Reword Skill

> **Skill ID:** `git-commit-message-reword`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Reword a **single** existing commit's message so it complies with the
project's commit-message rules (Conventional Commits format,
imperative mood, length limits, body bullet style, no
title-body redundancy).

This skill owns the **rules-driven message authoring** concern. The
mechanics of marking the target commit as `reword` and replaying
descendants are owned by the base [`git-commit-edit`](../git-commit-edit/SKILL.md)
skill.

## Composition Rationale

This is a **composer** over [`git-commit-edit`](../git-commit-edit/SKILL.md).

| Concern | Owner |
|---|---|
| Locate target commit, verify branch, descendant count, remote divergence | [`git-commit-edit`](../git-commit-edit/SKILL.md) |
| Backup branch (local + remote) | [`git-commit-edit`](../git-commit-edit/SKILL.md) |
| Interactive rebase with `reword` action, descendant replay, conflict handling | [`git-commit-edit`](../git-commit-edit/SKILL.md) |
| Force-push authorization, backup-branch cleanup | [`git-commit-edit`](../git-commit-edit/SKILL.md) |
| **Read project's commit-message rules** | **this skill** |
| **Inspect target commit's diff and classify** | **this skill** |
| **Author the new Conventional Commits message** | **this skill** |
| **Lint-verify the new message** | **this skill** |

The composer **MUST NOT** reimplement the `reword` mechanics; it
provides the authored message as input to the base skill's `reword`
flow.

## Source Rules

| Rule File | Scope |
|---|---|
| `<repo>/git-commit-message-rules.md` (or equivalent) | Conventional Commits format, types, scopes, length, mood, body style |
| [`git-commit-edit/SKILL.md`](../git-commit-edit/SKILL.md) | All backup, push, cleanup mandates |

## Source Conversations

| Date | Topic |
|---|---|
| 2026-05-09 | Reword of `923c42a3` `Create NestJS-React-App-rules.md` in `ai-agent-rules` |

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | Bash 4+ / Zsh / PowerShell 5.1+ |
| State | Clean working tree (or willingness to stash) |
| Project | A `git-commit-message-rules.md` (or equivalent) defining the commit-message standard |

## When to Apply

Apply this skill when:

- A user wants to fix the **message only** of a single existing commit.
- The commit message is non-compliant (e.g., GitHub Web UI auto-generated
  `Create X.md` / `Update X.md`, missing scope, wrong mood, exceeding
  length limits).
- The commit's **content is correct** — only the message needs to change.

### Inclusive Target Semantics

When the user says "reword `<sha>`", they mean that exact commit —
the rebase base for the procedure is `<sha>~1`. The agent MUST always
use the parent (`~1`) as the rebase base so the target commit is
included in the todo list.

Do NOT apply when:

- The commit also needs **content** changes (file edits, file removal,
  author fix) — use [`git-commit-edit`](../git-commit-edit/SKILL.md)
  directly.
- A **range** of commits needs rewording — use
  [`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md).
- The commit is the most recent and the branch was never pushed —
  `git commit --amend -m "..."` is sufficient (no rebase needed).

---

## Step-by-Step Procedure

### Step 0 — Pre-Reword Audit

#### 0a — Locate the Commit-Message Rules

```bash
find . -maxdepth 4 -iname "*commit*message*rule*"
```

Read the file in full and extract the constraints:

- Required format (Conventional Commits? Other?)
- Allowed types (`feat | fix | docs | style | refactor | test | chore | perf | build | ci`)
- Scope conventions
- Title length (typical: 50 ideal / 72 hard)
- Body wrapping (typical: 72)
- Imperative mood
- Punctuation rules
- Body authoring rules (this skill defaults to **MANDATORY**
  per §0c; the rules file may further constrain when subject-only
  is permitted)

#### 0b — Inspect the Target Commit

```bash
git show --name-only <sha>
git show <sha> -- <changed-files>
```

Use `--name-only` (not `--stat`) for the initial file list to avoid path
truncation. See
[`git-commit-message-delivery` §2](../git-commit-message-delivery/SKILL.md#2-verification-pattern)
for the rationale. `--stat` may be used for human-readable line-count
summary but never for programmatic path matching.

Determine:

- **Type** from diff signature (new file → likely `docs/feat`, edit
  → likely `docs/refactor/fix`, etc.).
- **Scope** from primary directory or module touched.
- **Description** that captures the *intent* (not just the
  filename) — read the actual content change to derive intent.

#### 0c — Author the New Message (Fidelity Mandate)

Apply the rules verbatim. Default template:

```text
<type>(<scope>): <imperative description, ≤ 50 chars ideal>

<body — bullets, ≤ 72 char wrap, no title redundancy>
```

##### Body is MANDATORY by default

Per the source rules' Fidelity Mandate (Zero Omission) and §3 *Body*
clause, the body is **MANDATORY by default** and MUST be authored from
the **actual diff content** (not the filename, stats, or prior
knowledge).

A body MAY be omitted **only** when ALL of the following hold (the
*Self-Documenting Titles* exception):

1. The diff is genuinely trivial (e.g., 1–3 line single-file change).
2. The title fully captures the intent without loss of fidelity.
3. There is no "why" beyond what the title states.

If any of the three is uncertain, **author a body**. Padding is
still prohibited — every bullet MUST reference a real diff fact.

###### Body content checklist

- Use bullets (`-`), wrap at 72 chars per line.
- Capture **substantive technical specifics** (new sections, flags,
  refactor mechanics, file moves, dependency pins, format
  migrations) — NOT just "updates X".
- Capture the **Why** when discoverable from diff context. Omit
  rather than fabricate.
- No title-body redundancy — the body adds, never repeats.

#### 0d — Reword Proposal

The agent **MUST** present:

````markdown
## Reword Proposal

**Repository:** `<repo>`
**Branch:** `<branch>`
**Target commit:** `<short-sha>`

**Old message:**
```
<old-subject>
<old-body-if-any>
```

**New message:**
```
<new-subject>

<new-body-if-any>
```

**Rule compliance:**
- Conventional Commits: ✓
- Imperative mood: ✓
- Title length: <N> chars (limit: 72)
- Body wrap: ≤ 72 chars per line ✓
- No title-body redundancy: ✓

**Backup target:** `backup/pre-reword-<n>`
**Descendant commits to replay:** `<count>`
**Remote divergence:** `<yes/no>` → force-push `<required/not required>`

Proceed? (yes / no)
````

**The agent MUST NOT begin the rebase until the user confirms.**

---

### Step 1 — Delegate to git-commit-edit (Reword Mode)

Follow the [base skill's procedure](../git-commit-edit/SKILL.md#step-by-step-procedure)
with these specializations:

1. **Step 0e (Backup)** — name as `backup/pre-reword-<n>`.
2. **Step 2a (Sequence Editor)** — change `pick <sha>` to **`reword <sha>`**
   (NOT `edit`). Use a sed pattern matching the **abbreviated** SHA
   in Git's todo format `pick <abbrev-sha> # <subject>`:

    ```sh
    sed -i.bak "s/^pick <abbrev-sha> /reword <abbrev-sha> /" "$1"
    ```

3. **Step 2b (Launch)** — set `GIT_EDITOR` to a script that
   replaces the message buffer (`$1`) with the authored message
   from §0c. Example:

    ```sh
    cat > /tmp/_reword_msg.sh <<'EOF'
    #!/bin/sh
    cat > "$1" <<'MSG'
    <new-subject>

    <new-body-if-any>
    MSG
    EOF
    chmod +x /tmp/_reword_msg.sh

    GIT_SEQUENCE_EDITOR=/tmp/_reword_seq.sh \
    GIT_EDITOR=/tmp/_reword_msg.sh \
    git rebase -i <sha>~1
    ```

4. **Step 3 (Edit) — SKIPPED** — `reword` skips the manual edit
   pause; Git applies the new message and continues to descendants.
5. **Step 4 (Amend) — SKIPPED** — already applied by the editor
   script.
6. **Step 5 (Continue) — AUTOMATIC** — `reword` rebases descendants
   without manual `git rebase --continue`.
7. **Step 7b (Push Authorization)** — inherit verbatim.
8. **Step 8 (Cleanup)** — inherit verbatim, plus
   `rm -f /tmp/_reword_seq.sh /tmp/_reword_msg.sh`.

> [!IMPORTANT]
> The sed pattern MUST anchor on the abbreviated SHA followed by a
> **trailing space** (`pick <abbrev> `), because Git's todo format is
> `pick <abbrev-sha> # <subject>` and matching `pick <abbrev>` without
> the space would also match a longer SHA that happens to share the
> prefix.

---

### Step 2 — Verification

```bash
git show --name-only HEAD~<N>  # verify file set (no path truncation)
git show --stat HEAD~<N> | head -20  # human-readable line-count summary
```

> **Path truncation note:** `--stat` truncates long paths with `.../`, making
> `grep` unreliable. Use `--name-only` for programmatic path matching. See
> [`git-commit-message-delivery` §2](../git-commit-message-delivery/SKILL.md#2-verification-pattern).

Confirm:

- New message is applied verbatim.
- Diff content is **identical** to the original commit.
- Descendant count is preserved (use the count from §0d).

#### 2a — Conventional Commits Lint

```bash
git log --pretty=format:'%h %s' -1 <new-sha> | \
  grep -E '^[0-9a-f]+ (feat|fix|docs|style|refactor|test|chore|perf|build|ci)(\([^)]+\))?: .+'
```

Non-empty match = compliant.

---

### Step 3 — Push Authorization & Cleanup

Inherit [Step 7b](../git-commit-edit/SKILL.md#7b--pre-push-remote-backup--push-authorization)
and [Step 8](../git-commit-edit/SKILL.md) of the base skill.

---

## Scope Coverage

| Category | Convention |
|---|---|
| Rules-file discovery | `find . -iname "*commit*message*rule*"` |
| Diff classification | `git show --name-only <sha>` (no path truncation) + heuristic mapping to `<type>(<scope>)` |
| Message authoring | Inline per the project's rules; bodies MANDATORY by default per §0c, with the 3-condition Self-Documenting Titles opt-out |
| Reword execution | **Delegated** to [`git-commit-edit`](../git-commit-edit/SKILL.md) (`reword` action via `GIT_SEQUENCE_EDITOR` + `GIT_EDITOR`) |
| Backup, push, cleanup | **Delegated** to [`git-commit-edit`](../git-commit-edit/SKILL.md) |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Inlining the reword mechanics** — sed-anchoring the SHA, env-var
  setup, descendant replay are owned by the base skill; this composer
  only authors the message and delegates.
- **Authoring a message without first reading the project's
  commit-message rules** — the rules file is the SSOT, not the
  agent's prior knowledge.
- **Omitting the body without satisfying ALL three Self-Documenting
  Titles conditions** (§0c) — the body is MANDATORY by default per
  the source rules' Fidelity Mandate.
- **Padding the body to meet a perceived length quota** — every
  bullet MUST reference a real diff fact; filler violates the
  Fidelity Mandate just as omission does.
- **Beginning the rebase without §0d approval**.
- **Pushing to remote without explicit authorization** — inherits
  base-skill push gates.

---

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Sed pattern matches no lines | Git's todo uses **abbreviated** SHAs; do NOT match against the full 40-char SHA. Anchor on the abbreviated form + trailing space. |
| `GIT_EDITOR` not invoked | When `reword` is the action, Git invokes `GIT_EDITOR` (or `core.editor`) for the message; verify your script is executable (`chmod +x`). |
| New message ends with stray comment lines | Ensure the editor script writes ONLY the message (no `# comment` lines from the buffer carry over). |
| Detached HEAD after rebase | Caller invoked rebase from a non-branch state; recover with `git checkout <branch> && git reset --hard <new-tip>`. |
| Commit-message rules not found | Ask the user to point to the rules file; do NOT invent rules. |

---

## Related Skills

- [`git-commit-edit`](../git-commit-edit/SKILL.md) — base skill
  (reword mechanics, backup, push gates).
- [`git-commit-message-bulk-reword`](../git-commit-message-bulk-reword/SKILL.md)
  — composer over THIS skill for ranges.

## Post-Processing

When this skill is invoked on a commit that lives on a
parallel/refined branch (e.g., `<branch>-2`) intended to replace the
canonical branch on `origin`, the message-only rewrite produced here
is only the first half of the workflow. The promotion of the refined
branch onto the canonical branch — cherry-pick equivalence audit for
canonical-only commits, tree-parity verification, and authorized
force-push — MUST be delegated to the
[`git-branch-promotion`](../git-branch-promotion/SKILL.md) skill.
Do NOT bypass its audit + verification gates.

**Submodule case (chained post-processing):** If the reworded commit
lives in a **submodule**, after
[`git-branch-promotion`](../git-branch-promotion/SKILL.md) succeeds the
parent repository's pointer commits to the (now-orphaned) old SHA are
invalidated. The parent's history MUST be repaired via
[`git-submodule-pointer-repair` §5](../git-submodule-pointer-repair/SKILL.md#5-mass-pointer-reconciliation-full-history-rewrite-recovery)
using the **reword-tolerant match key** in §5.2.0 (subject EXCLUDED —
because this very skill changes the subject).
