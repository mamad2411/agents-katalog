---
name: route-task
description: Decide which CLI worker (Claude, OpenCode, or Gemini) should implement a given task. Routes by task type — large-context to Gemini, mechanical to OpenCode, judgment to Claude. Returns the chosen worker and a short rationale; the caller invokes the worker via the orchestrator's invoke-worker.sh chokepoint.
---

# route-task

Encapsulates the task-type → worker mapping in one place so routing stays debuggable.

## Routing rules (v1)

| Worker | When to pick |
| **Gemini CLI** | Large-context: read whole repo, summarize, doc generation, second-opinion review |
| **OpenCode** | Mechanical: refactors, test scaffolding, parallel subtasks, codemods |
| **Claude Code (self)** | Architecture, ambiguous tasks, post-review fixes, anything where judgment beats throughput |
| **Smart Worker** | High-capability open-source models (Kimi, DeepSeek) via OpenRouter. Pick for complex implementation tasks when session budget is low. |

## Inputs

The caller (usually `start-feature` or `pr-loop`) provides:

- `task` — path to a markdown file describing the work
- `pr_number` — the in-flight PR (used for cache path)
- `round` — `0` for initial implementation, `≥3` for escalation re-routing
- `exclude` (optional, comma-separated) — workers already tried and to skip; required when `round ≥ 3`
- `budget_status` (optional) — `normal` or `low`. If omitted, defaults to `normal` unless `MCO_LOW_BUDGET=1` is set in the environment.

## Runbook

### Step 1 — Decide the worker

Determine the `budget_status`:
```bash
if [[ "${MCO_LOW_BUDGET:-0}" == "1" ]]; then
  status="low"
else
  status="${budget_status:-normal}"
fi
```

Spawn the `route-task-routing-judge` subagent (Agent tool, `subagent_type: route-task-routing-judge`). Pass it:

- The contents of the task file
- The routing rules above (verbatim)
- The exclude list (if present)
- The `budget_status`: $status

Expect the subagent to return three fields, parseable from its message:

```
worker: <claude|opencode|gemini|smart-worker>
```

rationale: <one sentence>
prompt: <the task prompt rewritten for the chosen worker>
```

If parsing fails (missing field, unknown worker, worker is in `exclude`), retry the subagent once with the explicit constraint quoted back. If it fails again, return failure to the caller — do not silently default to a worker.

### Step 2 — Cache the routing decision

```bash
round_dir=".mco-cache/$pr_number/round-$round"
mkdir -p "$round_dir"
echo "$worker" > "$round_dir/worker"
echo "$rationale" > "$round_dir/rationale"
printf '%s' "$prompt" > "$round_dir/prompt.md"
# role: implementation | fix | escalation — used by pr-loop's handover summary
if [[ "$round" == "0" ]]; then
  echo "implementation" > "$round_dir/role"
else
  echo "escalation" > "$round_dir/role"
fi
```

### Step 3 — Invoke the worker

```bash
# invoke-worker.sh ships inside the start-feature skill; resolve via the
# canonical install path (override with MCO_SKILL_ROOT for tests).
INVOKE="${MCO_SKILL_ROOT:-$HOME/.agents/skills/start-feature}/scripts/invoke-worker.sh"
bash "$INVOKE" "$worker" "$round_dir/prompt.md" "$round_dir"
```

Exit code handling:
- `0` → continue to Step 4
- non-zero → retry **once** with the same prompt. If it fails again, return failure to the caller (do **not** auto-reroute here; that's `pr-loop`'s job on round 3).

### Step 4 — Capture commits and push

The worker is expected to commit to the current branch. Verify it did:

```bash
git diff --quiet HEAD@{1} HEAD || echo "worker produced commits"
git status --porcelain  # should be empty; refuse to push if dirty (worker forgot to commit)
git push
```

If the worker left an unstaged diff (didn't commit), surface that to the caller as a failure rather than committing on its behalf — committing for the worker hides routing/prompt bugs.

### Step 5 — Return to caller

Return the `{worker, rationale}` pair so the caller (e.g. `pr-loop`) can log it and feed it into round-3 escalation logic.

## Subagent

`agents/claude-code/routing-judge.md` and `agents/opencode/routing-judge.md` — same role, two CLI-specific frontmatter variants. Registered as `route-task-routing-judge` after the post-install bootstrap (`~/.agents/skills/start-feature/scripts/install-agents.sh`) runs. Keep both bodies in sync.
