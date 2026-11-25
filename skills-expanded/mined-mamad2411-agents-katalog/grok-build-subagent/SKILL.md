---
name: grok-build-subagent
description: >-
  Delegates focused software implementation to Grok Build CLI in headless mode,
  then reviews and verifies the result. Use when the user asks to use Grok,
  Grok Build, grok -p, or a Grok subagent to implement, refactor, test, or
  investigate code.
version: 0.1.0
---

# Grok Build Subagent

Use Grok as an implementation worker. The parent agent owns scope, review,
verification, commits, and external publication.

## Workflow

### 1. Confirm the local CLI contract

Run:

```bash
grok --version
grok --help
```

Prefer the flags reported by the installed binary. Grok Build 1.0.4 uses:

- `-p, --single <PROMPT>` for one headless turn
- `--prompt-file <PATH>` for a prompt file
- `--cwd <PATH>` for the working directory
- `--permission-mode acceptEdits` for implementation
- `--no-subagents` to prevent nested delegation

Other projects named Grok CLI use incompatible flags such as `--prompt` and
`--directory`. Never translate examples across CLI variants without checking
`--help`.

### 2. Establish the boundary

Before delegation:

1. Inspect repository status and current branch.
2. Preserve and describe any pre-existing changes.
3. Give Grok one focused task with explicit completion criteria.
4. Name files or local reference implementations worth inspecting.
5. Specify the exact verification commands.
6. Reserve commit, tag, push, package publication, and destructive Git actions
   for the parent agent unless the user explicitly delegates them to Grok.

For parallel or risky work, create isolation outside Grok before invocation.
Headless `-p` does not create a worktree from `--worktree`.

### 3. Invoke Grok headlessly

When the host supports shell subagents, delegate this invocation to one so the
parent remains available to orchestrate other work. The shell subagent must
actually run Grok rather than implement the task in its place.

Use an absolute repository path and quote the prompt with a heredoc:

```bash
grok -p "$(cat <<'EOF'
Work in /absolute/path/to/repository.

Task:
- <one focused implementation goal>

Requirements:
- <behavior and compatibility constraints>
- Preserve existing public APIs unless explicitly changed.
- Preserve pre-existing uncommitted changes.

Verification:
- Run <exact test/build commands>.
- Run git diff --check.

Do not commit, tag, push, publish, reset, or discard unrelated changes.
Return changed files, design decisions, test results, and unresolved risks.
EOF
)" \
  --cwd "/absolute/path/to/repository" \
  --permission-mode acceptEdits \
  --no-subagents
```

Use `command -v grok` when the executable path is unknown. Use
`--prompt-file` for very long generated prompts. Keep credentials, tokens, and
private data out of prompts.

### 4. Review centrally

Treat Grok's report as a claim to verify:

1. Inspect `git status`, `git diff --stat`, `git diff --check`, and the full
   relevant diff.
2. Read every new public interface and security-sensitive path.
3. Confirm deletions and dependency changes are intentional.
4. Run the required tests and builds independently.
5. Search for obsolete references when the task replaces an old API or
   package.
6. Check that only intended files changed.

The step is complete only when the parent can explain the resulting design and
has direct evidence that verification passed.

### 5. Use focused correction passes

If review finds a defect, send Grok a narrow correction containing:

- the concrete defect and why it matters
- the required behavior
- tests that must change or be added
- the same Git and scope guardrails

Resume the same host shell subagent when practical so it retains implementation
context. Run Grok again inside that subagent, then repeat central review.

If Grok stalls or exits without edits, inspect its output and repository state.
Retry once with a smaller task and sharper completion criteria. Do not repeat
the same invocation without new evidence.

## Prompt checklist

- Absolute repository path
- One focused goal
- Existing changes to preserve
- Exact behavior and non-goals
- Language and architecture constraints
- Relevant source and reference paths
- Error and compatibility expectations
- Required tests and build commands
- No-commit/no-push guardrail
- Expected final report

## Completion report

Report:

- Grok command shape and CLI version
- implementation summary
- files changed or deleted
- independent test/build results
- commits or publications performed by the parent
- remaining blockers or physical-device/runtime verification
