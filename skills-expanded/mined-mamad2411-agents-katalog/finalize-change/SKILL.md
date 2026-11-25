---
name: finalize-change
description: Review and finalize uncommitted CompetitorIQ changes through deterministic formatting, verification, changelog, commit, and optional push workflows with explicit user approval.
---

# Finalize Change

## Purpose

Use this skill when the user asks to finalize completed repository work.

The workflow must always begin with a code review before any files are modified.

The agent is responsible only for:

- reviewing the change;
- classifying findings;
- deciding whether the workflow may continue;
- selecting an accurate changelog category and message;
- presenting results to the user.

Deterministic operations must be delegated to:

```bash
uv run python scripts/finalize_change.py <command>
```

Do not manually reproduce operations already implemented by the script.

---

# Approval Boundaries

Explicit user approval is required immediately before:

- creating a commit;
- pushing the branch.

These approvals are separate.

Approval to commit does not authorize pushing.

General instructions such as:

- “finish it”;
- “finalize everything”;
- “do the whole workflow”

do not replace the required commit and push confirmations.

No approval is normally required for:

- repository inspection;
- code review;
- Ruff formatting and automatic fixes;
- test execution;
- changelog updates;
- commit-message preparation.

Stop before those operations when the user explicitly requested approval before any file modification.

---

# Forbidden Actions

Never:

- review only after committing;
- commit before the review passes;
- commit directly on `main`;
- push directly from `main`;
- merge into `main`;
- force-push;
- bypass failing checks;
- remove or weaken tests merely to make checks pass;
- disable quality rules merely to make checks pass;
- invent changelog claims;
- stage or commit secrets;
- claim a command passed without executing it;
- treat commit approval as push approval.

If the deterministic script refuses an operation, report the reason and stop.

Do not bypass its safeguards.

---

# Workflow

## Phase 1: Review Before Modification

Read and follow:

```text
.cursor/skills/review-change/SKILL.md
```

Perform the complete review workflow described there.

The review must cover all current changes, including untracked files.

### When the review is blocked

If one or more blocking findings exist:

1. present the findings;
2. stop the finalization workflow;
3. do not run Ruff fixes;
4. do not update the changelog;
5. do not prepare a commit;
6. ask whether the user wants the blocking issues corrected.

### When the review passes

If no blocking findings exist:

1. summarize the review result;
2. continue to deterministic verification.

Do not ask the user to approve the review result unless clarification or a product decision is required.

---

## Phase 2: Deterministic Formatting and Verification

Run:

```bash
uv run python scripts/finalize_change.py verify
```

The script is responsible for executing configured deterministic operations, including:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run pytest
```

If verification fails:

1. report the failing command;
2. summarize the actionable error;
3. stop;
4. do not update the changelog;
5. do not prepare a commit.

Do not mark verification as successful manually.

---

## Phase 3: Review Automatic Changes

Run:

```bash
uv run python scripts/finalize_change.py inspect
```

Inspect changes introduced by Ruff or other deterministic tooling.

Confirm that:

- automatic fixes are safe;
- formatting did not reveal or introduce an issue;
- no unintended files appeared;
- the final change still matches its intended scope.

This is not a complete second review unless the automatic changes were substantial.

If a new blocking issue exists, stop.

---

## Phase 4: Update the Changelog

Determine one concise changelog entry from the final diff.

The agent may decide only:

- the category;
- the message.

The script controls insertion and formatting.

Choose exactly one category:

```text
Added
Changed
Fixed
Removed
Security
```

The message must:

- describe an actual change;
- describe user-visible or contributor-visible behavior;
- be supported by the final diff;
- be written in the past tense;
- fit on one line;
- omit a final period;
- avoid low-level implementation trivia.

Run:

```bash
uv run python scripts/finalize_change.py changelog \
  --category "<CATEGORY>" \
  --message "<MESSAGE>"
```

Do not edit `CHANGELOG.md` manually unless the script reports an invalid or unsupported changelog structure.

---

## Phase 5: Final Deterministic Check

Run:

```bash
uv run python scripts/finalize_change.py final-check
```

The command must validate:

- the active branch;
- repository state;
- changelog structure;
- forbidden files;
- Ruff checks;
- formatting;
- tests;
- commit readiness.

If it fails, report the failure and stop.

---

## Phase 6: Prepare the Commit Message

Run:

```bash
uv run python scripts/finalize_change.py prepare-message
```

The script deterministically derives a proposed commit message from repository state and the changelog.

Do not replace it merely because another wording is preferred.

A different message may be proposed only when the generated message is inaccurate or misleading.

Present the user with:

```markdown
## Ready to commit

**Branch:** `<branch>`

**Review:** Passed

**Verification:**
- Ruff check and automatic fixes: Passed
- Ruff formatting: Passed
- Tests: Passed

**Changelog:**
- `<category>`: `<message>`

**Proposed commit message:**

`<message>`

**Changed files:**
- `<file>`
```

Then ask:

> The change is ready. Should I create this commit?

Stop and wait for explicit approval.

---

## Phase 7: Commit After Approval

Only after explicit approval, run:

```bash
uv run python scripts/finalize_change.py commit
```

The script must:

- refuse protected branches;
- use the prepared message;
- stage eligible changes;
- reject forbidden files;
- create one commit;
- report the commit hash.

Report the resulting commit.

Then ask separately:

> The commit was created successfully. Should I push this branch?

Stop and wait for explicit push approval.

---

## Phase 8: Push After Separate Approval

Only after explicit push approval, run:

```bash
uv run python scripts/finalize_change.py push
```

The script must:

- refuse to push `main` or another protected branch;
- refuse to push a dirty working tree;
- push only the current branch;
- set its upstream when necessary;
- never force-push.

Report:

- the pushed branch;
- the remote;
- whether an upstream was created.

Do not merge the branch.

---

# Completion Report

At the end, state only actions that actually occurred.

Use:

```markdown
## Finalization complete

- Review: Passed
- Ruff: Passed
- Tests: Passed
- Changelog: Updated
- Commit: `<hash>` or Not created
- Push: Completed or Not performed

### Non-blocking observations

- None
```

Never describe a proposed commit or push as completed.