---
name: paseo-loop
description: Run a task in a loop until an exit condition is met. Use when the user says "loop", "loop this", "keep trying until", "babysit", "poll", or wants iterative autonomous execution.
user-invocable: true
---

# Loop Skill

You are setting up an autonomous loop. An agent runs repeatedly until an exit condition is met.

**User's arguments:** $ARGUMENTS

---

## Prerequisites

Load the **Paseo skill** first — it contains the CLI reference for all agent commands.

## What Is a Loop

A loop runs an agent repeatedly until it's done. There are two modes:

### Self-terminating (no verifier)

A single worker agent runs each iteration. It returns `{ done: boolean, reason: string }` via structured output. The loop exits when `done` is true.

### Worker + Verifier

A worker agent runs each iteration (detached, no structured output). After the worker finishes, a separate verifier agent evaluates the verification prompt and returns `{ done: boolean, reason: string }`. The loop exits when `done` is true.

### Feedback between iterations

In both modes, the `reason` from the previous iteration is fed back to the next worker as `<previous-iteration-result>`. This gives the worker context about what happened last time.

## Live Steering

Each loop run persists state in:

```text
~/.paseo/loops/<loop-id>/
  worker-prompt.md     # worker prompt (live-editable)
  verifier-prompt.md   # verifier prompt (live-editable, only when verifier is used)
  last_reason.md       # latest iteration result
  history.log          # per-iteration records
```

Edits to prompt files are picked up on the next iteration without restarting the loop.

## Parsing Arguments

Parse `$ARGUMENTS` to determine:

1. **Worker prompt** — what the worker does each iteration
2. **Verifier prompt** (optional) — what the verifier checks after each worker iteration
3. **Worker** — which agent does the work (default: Codex)
4. **Verifier** — which agent verifies (default: Claude sonnet)
5. **Sleep** (optional) — delay between iterations
6. **Name** — a short name for tracking
7. **Max iterations** — safety cap (default: unlimited)
8. **Archive** — whether to archive agents after each iteration
9. **Worktree** — whether to run in an isolated git worktree

### Examples

```
/loop babysit PR #42 until CI is green, check every 5 minutes
→ worker-prompt: "Check the CI status of PR #42 using `gh pr checks 42`. Report done when ALL checks
  have passed (no pending, no failures). If any checks are still running or have failed, report not
  done and list which checks are pending or failing."
  No verifier (self-terminating: the worker inspects CI and reports done when green)
  sleep: 5m
  archive: yes
  name: babysit-pr-42

/loop implement the auth refactor from the plan in /tmp/plan.md
→ worker-prompt-file: /tmp/plan.md
  verifier-prompt: "Verify every step of the plan was implemented. Check file changes, types, and
  run `npm run typecheck` and `npm test`. Report each criterion individually with evidence."
  name: auth-refactor
  worktree: auth-refactor

/loop run the test suite until it passes
→ worker-prompt: "Run `npm test`. If any tests fail, read the failure output, investigate the root
  cause in the source code, and fix it. Report done when `npm test` exits with code 0 and all
  tests pass. Report not done if any test still fails, and explain which tests failed and why."
  No verifier (self-terminating: worker reports done when tests pass)
  name: fix-tests

/loop watch error rates after deploy, check every 10 minutes
→ worker-prompt: "Check the error rate for the canary deployment by running `./scripts/check-canary.sh`.
  Report done when the error rate has been below 0.1% for at least 2 consecutive checks. Report not
  done with the current error rate and trend."
  No verifier (self-terminating: worker reports done when error rate is stable)
  sleep: 10m
  max-iterations: 30
  archive: yes
  name: canary-watch
```

## Using the Script

The loop is implemented as a bash script at `~/.claude/skills/paseo-loop/bin/loop.sh`.

```bash
# Self-terminating: worker checks PR CI and reports done when all checks pass
~/.claude/skills/paseo-loop/bin/loop.sh \
  --worker-prompt "Check CI status of PR #42 using gh pr checks 42. Report done when ALL checks pass. Report not done with a list of pending/failing checks." \
  --name "babysit-pr" \
  --sleep 5m \
  --archive

# Worker + verifier: worker implements, verifier independently checks
~/.claude/skills/paseo-loop/bin/loop.sh \
  --worker-prompt "Implement the auth refactor: ..." \
  --verifier-prompt "Verify the auth refactor is complete. Run npm run typecheck and npm test. Check that all file changes match the plan. Report each criterion with evidence." \
  --name "auth-refactor" \
  --worktree "auth-refactor"
```

### Arguments

| Flag | Required | Default | Description |
|---|---|---|---|
| `--worker-prompt` | Yes* | — | Prompt given to the worker each iteration |
| `--worker-prompt-file` | Yes* | — | Read the worker prompt from a file |
| `--worker` | No | `codex` | Worker agent (`provider/model`, e.g. `codex/gpt-5.4`, `claude/sonnet`) |
| `--verifier-prompt` | No* | — | Verification prompt for a separate verifier agent |
| `--verifier-prompt-file` | No* | — | Read the verifier prompt from a file |
| `--verifier` | No | `claude/sonnet` | Verifier agent (`provider/model`) |
| `--name` | Yes | — | Name prefix for agents |
| `--sleep` | No | — | Delay between iterations (e.g. `30s`, `5m`, `1h`) |
| `--max-iterations` | No | unlimited | Safety cap on iterations |
| `--archive` | No | off | Archive agents after each iteration |
| `--worktree` | No | — | Worktree name. Created on first use, reused after. |
| `--thinking` | No | `medium` | Thinking level for worker |

\* Provide exactly one of `--worker-prompt` or `--worker-prompt-file`. Provide at most one of `--verifier-prompt` or `--verifier-prompt-file`.

### Behavior by parameters

| Parameters | Mode | Use case |
|---|---|---|
| `--worker-prompt` only | Self-terminating worker | Worker does work and decides when done |
| `--worker-prompt` + `--verifier-prompt` | Worker + verifier | Worker implements, verifier independently checks |
| `--worker-prompt` + `--sleep` | Polling with self-termination | Periodic check until a condition is met |
| `--worker-prompt` + `--verifier-prompt` + `--sleep` | Periodic work + verifier | Periodic work with independent verification |

### Agent Naming

Without verifier: agents are named `{name}-{N}`:
```
babysit-1     # First iteration
babysit-2     # Second iteration
```

With verifier: workers are `{name}-{N}`, verifiers are `{name}-verify-{N}`:
```
feat-1          # First worker
feat-verify-1   # First verifier
feat-2          # Second worker (with previous result context)
feat-verify-2   # Second verifier
```

### Worktree Support

When `--worktree` is passed, all agents run in the same git worktree. The worktree is created on first launch and reused for all subsequent agents.

```bash
~/.claude/skills/paseo-loop/bin/loop.sh \
  --worker-prompt "Implement the feature..." \
  --verifier-prompt "Verify the feature works and typecheck passes" \
  --name "feature-x" \
  --worktree "feature-x"
```

## Your Job

1. **Understand the task** from the conversation context and `$ARGUMENTS`
2. **Decide the mode** — does this need a separate verifier, or can the worker self-terminate?
3. **Write the worker prompt** — what the worker does each iteration. Must be self-contained (the agent has zero prior context).
4. **Write the verifier prompt** (if needed) — what the verifier checks. Should be factual and verifiable.
5. **Choose sleep** — if the task is polling/monitoring, add a sleep duration
6. **Choose archive** — use `--archive` for long-running or polling loops to keep the agent list clean
7. **Choose agents** — default: `codex` worker + `claude/sonnet` verifier
8. **Choose a name** — short, descriptive
9. **Run the script** — call `loop.sh` with all the arguments

### When to use a verifier vs self-terminating

Use a verifier (`--verifier-prompt`) when:
- The worker's job is to implement something and you want independent verification
- You want the verification done by a different agent than the worker
- The worker should focus on doing work, not on judging its own work

Use self-terminating (no verifier) when:
- The worker is checking/polling an external condition (CI status, deployment health)
- The worker can objectively determine when it's done (tests pass, file exists)
- You want a single agent doing both the work and the evaluation

### Writing a Good Worker Prompt

The worker prompt is what the agent receives each iteration. It must be:

1. **Self-contained** — The agent starts with zero context. Everything needed is in the prompt.
2. **Specific** — Name files, functions, types, URLs. Be concrete.
3. **Action-oriented** — Tell the agent what to do, not what to think about.

### Writing a Good Verifier Prompt

The verifier prompt defines what the verifier checks after each worker iteration. It can range from strict factual checks to qualitative code review:

**Factual / objective checks:**
- "Run `npm test` and `npm run typecheck`. Report done only if both pass with zero failures."
- "Check that PR #42 has all CI checks green and no unresolved review comments."
- "Verify the API responds to `GET /health` with status 200 within 500ms."

**Code quality / style checks:**
- "Review the changes for DRY violations. Report done when there is no duplicated logic across files."
- "Check that the implementation does not over-engineer. No unnecessary abstractions, no premature generalization, no feature flags for single-use code."
- "Verify the code follows the project's conventions: functional style, no classes, explicit types, no `any`."

**Performance / resource checks:**
- "Run the benchmark suite. Report done when p99 latency is under 100ms."
- "Check bundle size. Report done when the production build is under 500KB gzipped."

**Comprehensive verification:**
- "Verify every step of the plan was implemented. Check file changes, types, test output. Run `npm run typecheck` and `npm test`. Report each criterion individually with evidence."

The verifier should report facts with evidence, not suggest fixes.

### Skill Stacking

You can instruct the worker to use other skills:

```bash
~/.claude/skills/paseo-loop/bin/loop.sh \
  --worker-prompt "Use /committee to plan, then fix the provider list bug. The bug is..." \
  --verifier-prompt "The provider list renders correctly and npm run typecheck passes" \
  --name "provider-fix"
```

### Composing with Handoff

A handoff can launch a loop:

```
/handoff a loop in a worktree to babysit PR #42
```
