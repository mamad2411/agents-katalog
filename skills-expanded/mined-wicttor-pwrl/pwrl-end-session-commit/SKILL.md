---
name: pwrl-end-session-commit
description: Draft commit message, handle version bumps, and create the session commit.
argument-hint: "[Input: checkpoint artifact from Phase 1]"
user-invocable: false
---

# PWRL End Session Commit

Draft a descriptive commit message and create the session commit with proper attribution.

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What summarizes this session's work? Provide context and key decisions for the commit message."
- Provide clear recovery suggestions when errors occur

## Purpose

Commit is the second phase of session cleanup. It takes the checkpoint artifact from Phase 1, crafts a meaningful commit message that explains the session's work and next steps, detects version changes, and creates the commit:

- Draft commit subject (imperative mood, ≤50 chars)
- Write commit body with decisions, blockers, and next steps
- Detect version bumps and update `CHANGELOG.md` if needed
- Get user approval, stage files, and create commit
- Capture commit SHA for logging and learnings chaining

## Usage

```bash
# Typically invoked by /pwrl-end-session after checkpoint succeeds
# Direct usage for testing or recovery:
/pwrl-end-session-commit [checkpoint-artifact-path]
```

This is the second phase of `/pwrl-end-session` orchestrator, executed after Phase 1 (checkpoint) completes.

## Support Files

- `references/commit-protocol.md` — Message drafting rules and version bump handling
- `references/commit-examples.md` — Examples for different session completion types

## Detailed Workflow

For complete step-by-step instructions, see [commit-protocol.md](references/commit-protocol.md).

This SKILL.md provides an overview. The detailed workflow document contains:

- Commit subject drafting with imperative mood
- Commit body structure (why/what/next)
- Version bump detection and CHANGELOG.md updates
- User approval flow with edit capability
- Git staging and commit creation
- Error handling and recovery

## Quality Gate Validation

After completing this phase, run quality gate validation:

```bash
/pwrl-phase-checkpoint end-session 2 [artifact-path]
```

See [pwrl-phase-checkpoint](../../pwrl-phase-checkpoint/SKILL.md) for validation rules.

---

## Workflow

### Phase 1: Draft Commit Message

Create a meaningful commit message with subject and body.

**See detailed workflow:** [commit-protocol.md](references/commit-protocol.md#phase-1-draft-commit-message)

- Draft subject line (imperative, ≤50 chars)
- Write body: explain why, what changed, blockers/notes, next steps
- Validate format (subject ≤50, body readable, proper structure)

### Phase 2: Handle Version Bump

Detect and process version changes with CHANGELOG.md updates.

**See detailed workflow:** [commit-protocol.md](references/commit-protocol.md#phase-2-handle-version-bump)

- If version_bumped flag is false: skip to Phase 3
- If true: extract new version from checkpoint artifact
- Update CHANGELOG.md with entry (date, version, summary)
- Stage CHANGELOG.md alongside approved files

### Phase 3: User Approval

Get explicit approval of commit message before staging/committing.

**See detailed workflow:** [commit-protocol.md](references/commit-protocol.md#phase-3-user-approval)

- Display full commit message to user
- Ask approve/edit/cancel
- If edit: allow modification of subject/body/next steps
- Re-validate message after edits
- Once approved, proceed to staging

### Phase 4: Create Commit

Stage files and create the commit with proper git handling.

**See detailed workflow:** [commit-protocol.md](references/commit-protocol.md#phase-4-create-commit)

- Verify git state (no merge/rebase in progress)
- Stage approved files: `git add [files...]`
- Verify staging with `git status`
- Create commit: `git commit -m "[subject]" -m "[body]"`
- Capture commit SHA
- Verify commit exists and contains `[AGENT: ...]` trailer

## Rules

- ✓ Commit subject must be ≤50 chars, imperative mood
- ✓ User approval required before staging/committing
- ✓ No automatic push (user controls push timing)
- ✓ Version bump detection automatic, CHANGELOG.md auto-staged if needed
- ✓ Capture and return commit SHA for audit trail and learnings chaining

## Best Practices

- Subject should be a clear, single action: "Fix typo" not "Fixed some typos and other stuff"
- Body should explain _why_ work ended here, not just _what_ changed
- Link to task/plan file if applicable (e.g., "Completed: `docs/tasks/to-do/U1-feature.md`")
- If work is partial or blocked, be explicit about blockers and next steps
- Keep message readable and future-friendly (someone will read this in 6 months)

## Acceptance Criteria

- ✓ Input: Checkpoint artifact with approved_files and session_reason
- ✓ Output: Commit artifact with commit_sha, message, version_bumped flags
- ✓ Message: Subject ≤50 chars, body explains why/what/next, trailer present
- ✓ Verification: Commit created, SHA captured, version bump detected and CHANGELOG.md staged if needed
- ✓ User approval: Explicit confirmation obtained before committing
