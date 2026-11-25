---
name: dev-review-claude
description: Independent code review using a fresh interactive Claude Code session as the reviewer. USE WHEN user says "dev-review-claude", "/skill:dev-review-claude", "independent Claude review", or wants a Claude-powered second-opinion review of a plan, build (uncommitted diff), file/directory path, or proposal. Accepts optional `--claude` / `--opus` / `--sonnet` model flags and a target argument (`plan`, `build`, `proposal`, or a path).
---

# Dev Review Claude (Interactive Claude Code via tmux)

Independent review using a fresh interactive Claude Code session as the reviewer. The primary agent extracts a review target from conversation context, gathers surrounding codebase context, writes a structured brief, and drives a separate Claude Code process via the helper script `engine.sh` (in this skill directory). The reviewer runs with bypass permissions so read/search/shell work does not stall.

Review-only by instruction, not by permission — Bash and edit tools stay enabled inside the reviewer session so the reviewer can inspect the codebase freely. A malicious or buggy reviewer *could* modify files; the primary agent surfaces any working-tree change via `engine.sh diff_tree` after the run. This is trust-and-verify, not enforcement. (Same posture as `dev-review-pi`.)

## Variables

- **TARGET** (`$1`) — what to review. One of:
  - `plan` — most recent plan file on disk (search `plans/`, `specs/`, `artifacts/plans/`).
  - `build` — uncommitted git changes; rejected outside a git repo.
  - `proposal` (aliases: `idea`, `context`) — inline proposal/snippet from the current conversation, even if nothing is on disk.
  - An explicit file or directory path.
  - Omitted — extract the review target from conversation context.
- **REVIEWER_MODEL_ARGS** — reviewer model selector, exported to engine as `DRC_MODEL_FLAG_STR`. Default `--model opus`. `--sonnet` overrides to `--model sonnet`. `--claude` and `--opus` are explicit no-op pins (equivalent to default). `--gpt` is rejected (Claude-first skill; ask for `--opus` or `--sonnet`). Multiple model flags — ask the user to choose one.
- **ENGINE** — `$HOME/.claude/skills/dev-review-claude/engine.sh`. The primary agent calls subcommands; the script owns all temp paths, tmux session lifecycle, ready-pattern polling, and cleanup.

**Canonical finding regex** — defined here once, referenced everywhere else: `^[-*]\s*\*\*\[(Critical|Warning|Note)\]:\*\*`. The brief tells the reviewer to use this exact format; the primary parses captured findings with the same regex.

## Checklist

Create a task per item, complete in order:

1. Parse flags and extract review target from argument or conversation context.
2. Verify scope with the user (conditional — see Phase 1).
3. Gather surrounding context (conventions, related code, tests, plan).
4. Build the review brief.
5. Drive `engine.sh` through prepare → launch → poll → capture → diff_tree → cleanup.
6. Present findings by severity, flag disagreements, ask which to address.
7. Apply only the changes the user agrees to.

## Workflow

### Phase 1: Extract and Verify

**Parse model flags first**, strip them from the argument string, then interpret TARGET.

**Resolve TARGET:**
- `plan` — find the most recent plan file (ask if ambiguous).
- `build` — use uncommitted git changes; if working tree is clean, report "nothing to review" and stop; if changes are unrelated to a known plan, warn before proceeding.
- `proposal` / `idea` / `context` — extract the most recent concrete suggestion from chat history. The proposal *is* the content under review, not a file. If multiple candidates, ask the user to pick.
- Explicit path — use it directly.
- Nothing provided and nothing clear in context — ask what to review.

**Scope confirmation (conditional):**
- **Skip** when TARGET resolves to an on-disk file or directory path AND context-file count is under 5.
- **One-line confirm** for `plan` / `build` / `proposal` argument forms (resolution can pick the wrong artifact). Example: `Reviewing plans/<name>.md? (y/n)`.
- **Full scope summary** (target, context files, review focus, "add or remove anything?") for ambiguous extracted-from-chat targets. Wait for confirmation; adjust on feedback.

### Phase 2: Gather Context and Build Brief

**Context assembly is the critical step.** Be thorough — read related files, conventions, plans, tests, configs. Don't pre-review; pass raw context and let the reviewer form independent opinions.

**Always gather:** project conventions (CLAUDE.md, AGENTS.md, linting configs, tsconfig), stack detection.

**By review type:**
- **Plan/context** — the plan file, PRD or requirements, code the plan will modify, established conventions.
- **Build** — `git status` (tracked + untracked), `git diff`, `git diff --staged` inline in the brief; the plan the build was based on; tests for modified code; dependents of changed files.
- **File/directory** — imports/dependencies of the target, tests for the target, files that import the target.
- **Proposal (inline)** — paste the proposal verbatim; include the problem it solves, constraints from the conversation, and files it would touch if knowable. If purely abstract, note that explicitly and let the reviewer reason on first principles.

Keep context focused: summarise large files, include small ones in full, target under ~8K lines total. If the brief overflows, summarise older files rather than enabling edit-capable tools.

**Brief structure** (Write this to `$REVIEW_FILE`). Sections: Review Type; Project Context (stack, conventions, working directory); What's Being Reviewed (plan / diff / file / proposal content); Related Code (paths, roles, excerpts); Review Instructions.

The Review Instructions block must include, verbatim:

- Reviewer is independent, runs in a fresh Claude Code session, may inspect the repo, stays review-only (primary applies changes).
- Analysis dimensions: gaps, technical risks, completeness, best-practice fit, architectural concerns, assumptions.
- Findings format: the canonical regex form — `- **[Critical|Warning|Note]:** <one-line summary> — <file:line if applicable>. <explanation and suggested resolution>`. No freeform paragraphs.
- **Deterministic completion contract**: write the complete findings list to `$FINDINGS_FILE` via Bash (e.g. `cat > "$FINDINGS_FILE" <<'EOF' ... EOF`), then `touch "$DONE_FILE"`. Only the Bash-written file counts as output. Do not print findings to the chat pane, and do not print any line matching the canonical regex to chat (it confuses the polling layer).

Interpolate the literal values of `$FINDINGS_FILE` and `$DONE_FILE` into the brief at build time — the primary learns these paths in Phase 3 Step 1.

### Phase 3: Run the Engine

The reviewer mechanics live in `engine.sh`. The primary agent invokes subcommands as five sequential Bash-tool calls and one poll loop. Do not reimplement ready-detection, tmux session management, or cleanup in the skill — call the engine.

> **Critical: shell variables do NOT persist across separate Bash tool calls.** Each Bash invocation is a fresh subshell. After Step 1, capture the literal state-file path and the brief-paths it printed in your own working notes (as plain strings), then substitute those literal paths into every subsequent Bash call by string-interpolation when you compose the command. Do not write `$STATE` or `$FINDINGS_FILE` and expect a later call to know what they mean. The shell snippets below use `<STATE>`, `<FINDINGS_FILE>`, `<DONE_FILE>`, `<REVIEW_FILE>`, `<PROMPT_FILE>` as placeholders the primary fills with the actual `/tmp/drc-*` paths returned by Step 1.

**Step 1 — Prepare and load state paths.** One Bash call. Choose `PROJECT_ROOT`: prefer the target's enclosing repo (`git rev-parse --show-toplevel` against the target's directory); fall back to the target's parent directory when the target lives outside any git repo (`engine.sh` tolerates non-git roots — the baseline and diff become trivially empty). Reject `build` reviews on non-git targets and fall back to a file review of the would-be diff target.

```bash
bash "$HOME/.claude/skills/dev-review-claude/engine.sh" prepare <PROJECT_ROOT>
# Then read the state file the engine printed and surface its keys:
cat /tmp/drc-state-XXXXXX.env
```

Record from that output:
- `<STATE>` — the state-file path the engine printed on stdout.
- `<REVIEW_FILE>`, `<PROMPT_FILE>`, `<FINDINGS_FILE>`, `<DONE_FILE>` — the brief and contract paths inside the state file.

**Step 2 — Write brief and prompt files.** Use the Write tool to write the brief (with the literal `<FINDINGS_FILE>` and `<DONE_FILE>` paths interpolated into the completion contract) to `<REVIEW_FILE>`. Then build `<PROMPT_FILE>` by prepending a one-line cover instruction. Substitute the literal paths into the Bash call:

```bash
{
  printf 'Review the following brief. Follow the completion contract exactly: write findings to <FINDINGS_FILE> with your Bash tool, then touch <DONE_FILE>.\n\n'
  cat <REVIEW_FILE>
} > <PROMPT_FILE>
```

**Step 3 — Launch the reviewer session.** One Bash call. Default model is `--model opus`; swap to `--model sonnet` if `--sonnet` flag was given:

```bash
DRC_MODEL_FLAG_STR='--model opus' bash "$HOME/.claude/skills/dev-review-claude/engine.sh" launch <STATE>
```

Engine.sh starts tmux, runs `claude` with bypass permissions, polls for the ready pattern (`bypass permissions on|shift\+tab to cycle`), then pastes `<PROMPT_FILE>` and sends Enter.

**Step 4 — Poll loop.** In the primary agent's outer harness, repeat with a sleep between calls (5–15 seconds is reasonable):

```bash
bash "$HOME/.claude/skills/dev-review-claude/engine.sh" poll <STATE>
```

The engine prints exactly one of `done`, `running`, `exited`. Stop on `done` or `exited`. Cap at roughly 20 polls (~5 minutes wall clock) before pausing to ask the user: stuck or abort?

**Step 5 — Capture, diff, cleanup.** Three Bash calls, each with the literal `<STATE>` path:

```bash
bash "$HOME/.claude/skills/dev-review-claude/engine.sh" capture   <STATE>
bash "$HOME/.claude/skills/dev-review-claude/engine.sh" diff_tree <STATE>
bash "$HOME/.claude/skills/dev-review-claude/engine.sh" cleanup   <STATE>
```

`capture` prints `<FINDINGS_FILE>` to stdout. If the findings file is empty, it dumps the tmux pane instead and exits non-zero with `FINDINGS_FILE_EMPTY` on stderr — apply lenient parsing in that case. `diff_tree` prints any working-tree drift since `prepare`; surface it before findings if non-empty. `cleanup` is idempotent — kills tmux and removes every temp path the engine allocated.

### Phase 4: Present and Discuss

Parse captured findings using the canonical regex defined at the top. Present organised by severity:

- **Critical findings** — quote the reviewer, give your assessment (agree / disagree / nuance), suggest a resolution.
- **Warnings** — same shape.
- **Notes** — same shape.
- **Reviewer disagreements** — call them out explicitly with your reasoning; let the user decide.

Then ask: "Which findings do you want to address? Any you want to dismiss or explore further?" Iterate based on user feedback.

### Phase 5: Apply Changes

Primary agent applies only the changes the user explicitly agrees to. Show a summary diff. If the user wants no changes, close the review as discussion-only.

## Report

```
Review Complete (Dev Review Claude via tmux)
Target: <what>   Type: <Plan/Context | Build | File | Proposal>
Stack: <detected>   Context files: <N>
Findings: Critical=<N> Warning=<N> Note=<N>
Key Findings: <top 1-3>
Working-tree drift: <yes/no>   Disagreements: <N>
Outcome: <Changes applied | Recommendations discussed | No issues found>
```

## Error Handling

- `claude` or `tmux` missing — `engine.sh launch` exits non-zero with a diagnostic; report and ask the user to fix their install.
- Ready timeout — `engine.sh launch` dumps the last ~30 pane lines to stderr; surface them and ask whether to retry or abort.
- Empty findings file — `engine.sh capture` falls back to a pane dump and writes `FINDINGS_FILE_EMPTY` on stderr; apply lenient parsing and offer to re-run or fall back to a primary-agent-only review.
- Working-tree mutation detected — `engine.sh diff_tree` shows the drift; surface it before presenting findings and confirm with the user before applying or reverting anything.
- Target not found — ask the user to clarify what to review.
- No issues — clean review; acknowledge the code is solid as-is.
