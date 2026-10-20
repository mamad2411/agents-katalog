---
name: codex-luna
description: "Codex-only workflow for non-trivial implementation: the current Codex session freezes the plan, delegates scoped execution to a separate Codex CLI process using gpt-5.6-luna at max reasoning, then reviews and verifies the result. Use when Luna should implement a resolved plan without redesigning it. Skip in every non-Codex harness and never let the executor recursively delegate."
---

# Codex Luna

## Session Gate

Apply this gate before running any CLI command:

- Codex session: continue. The current session is the coordinator and owns planning, scope decisions, review, and verification.
- Any non-Codex harness: stop applying this skill.

This skill intentionally permits one nested `codex exec` process as the Luna executor. Never use that process as another planner, and explicitly forbid it from invoking `$codex-luna`, launching another agent CLI, or delegating recursively.

## Route

Use this workflow when:

- implementation is non-trivial and needs an explicit plan before edits
- the desired outcome is known and the exact file-level execution path can be frozen
- a separate `gpt-5.6-luna` execution pass at `max` reasoning is worth the delegation overhead
- the coordinator can independently inspect the diff and run verification

Do not use it for tiny edits, design-only work, or ordinary one-pass investigation. For a read-only investigation or review, use this workflow only when the user explicitly asks for a separate Luna pass.

Keep in the coordinator:

- architecture, API, naming, UX, and final scope decisions
- session-only tools, secrets, authenticated state, and user interaction
- destructive operations, releases, pushes, and external mutations
- plan acceptance, diff review, verification, and final reporting

## Freeze The Plan

The accepted plan must resolve assumptions and contain:

1. problem framing and non-goals
2. exact files or modules to inspect and change
3. ordered implementation steps
4. exact tests and verification commands
5. risks, protected paths, and out-of-scope items

Do not hand Luna unresolved alternatives unless choosing among them is explicitly part of the task.

## Invoke Luna Executor

Pass the accepted plan to a fresh, persistent Codex CLI session. Keep the prompt in a file so shell quoting cannot alter the spec:

```bash
LP=$(mktemp)
cat >"$LP" <<'EOF'
Execute the frozen implementation spec below. Do not redesign it or broaden scope.
Do not invoke any delegation workflow, launch another agent CLI, or delegate recursively.

Repo:
<absolute repo path>

Coordinator constraints:
<protected paths, non-goals, and exact verification expected>

Frozen coordinator plan:
<paste the accepted plan>

Output shape:
- files changed
- commands run and their results
- deviations from the plan, with reason
EOF

command codex exec --yolo -C <repo> \
  --model gpt-5.6-luna \
  -c model_reasoning_effort="max" \
  -o /tmp/codex-luna-last.md \
  - <"$LP" 2>/dev/null
```

- `--yolo` matches the `codex-first` house default; Luna may run commands and tests freely, so keep prompts scoped to the target repo.
- `command codex` bypasses shell aliases and functions. If Codex is not on `PATH`, fix the local CLI installation before delegating.
- Stderr is suppressed to keep thinking noise out of coordinator context; remove `2>/dev/null` only when debugging a failed run.
- Read `/tmp/codex-luna-last.md`; executor claims are advisory until verified.
- Do not parse a JSONL stream; use the saved final-output file.
- For long runs, use a background shell job and do not kill a quiet run under 30 minutes.
- Use separate prompt and output files for independent tasks.
- Outside a Git repository, add `--skip-git-repo-check`.

## Follow-Up Fixes

- Bad or incomplete plan: correct it in the coordinator before asking Luna to continue.
- Sound plan but faulty execution: resume the most recent session with the failing proof and a narrow correction.
- After two failed Luna execution rounds, stop delegating and take over in the coordinator.

Follow-up fixes are cheaper than fresh runs and retain executor context. As in `codex-first`, `resume` has no `-C` or `--yolo`; run it from the repo directory, use `--last`, and spell out the unrestricted flag.

```bash
P2=$(mktemp)
cat >"$P2" <<'EOF'
Fix only:
<specific correction>

Failure proof:
<test output, diff concern, or reviewer finding>

Expected verification:
<commands>

Do not invoke any delegation workflow, launch another agent CLI, or delegate recursively.
EOF

(cd <repo> && command codex exec resume --last \
  --model gpt-5.6-luna \
  -c model_reasoning_effort="max" \
  --dangerously-bypass-approvals-and-sandbox \
  -o /tmp/codex-luna-last.md \
  - <"$P2" 2>/dev/null)
```

## Prompt Contract

Every executor process starts with zero coordinator conversation context.

- Luna is the only external agent in this workflow.
- Include the goal, repo, relevant paths, constraints, non-goals, expected proof, and output shape in every fresh prompt.
- State that the plan is frozen and recursive delegation is forbidden.
- Do not assume the executor can see chat history, screenshots, secrets, MCP state, or coordinator-only reasoning.
- Preserve unrelated worktree changes and name protected paths explicitly when the checkout is dirty.

## Verify In The Coordinator

- run `git status -sb` and read the full diff
- compare Luna's changes with the accepted plan
- run focused tests and inspect their real output
- verify documentation when behavior, commands, configuration, or runtime architecture changed
- keep pushes, releases, and other irreversible operations in the coordinator

## Economics

The only valid path is current Codex planning -> one Luna executor -> current Codex verification. Do not add a nested planning pass or an executor delegation tree.
