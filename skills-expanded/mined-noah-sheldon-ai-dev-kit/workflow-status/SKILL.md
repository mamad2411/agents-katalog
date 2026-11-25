---
name: workflow-status
description: Query and report the real-time status of multi-agent workflows. Reads .workflow/ state files, computes progress, identifies blockers, and formats status dashboards. Used by the /multi-agent-status command and the multi-agent-project-manager agent.
origin: AI Dev Kit
---

# Workflow Status

Query and report the real-time status of all active multi-agent workflows.

## When to Use

- A user runs `/multi-agent-status`
- The multi-agent-project-manager agent needs a status update for its 60-second cycle
- An agent needs to check if a dependency micro-task is complete before starting
- Escalation requires current workflow state

## Status States

Each workflow progresses through these states:

```
proposed → scanning → decomposing → executing → reviewing → done
                                                ↕
                                            blocked
```

| State | Meaning |
|---|---|
| `proposed` | Feature spec or issue exists but workflow not started |
| `scanning` | Repo scanner is reading the repo and mapping surfaces |
| `decomposing` | Micro-task decomposer is breaking the feature into atomic tasks |
| `executing` | Coding agents are working on micro-tasks in parallel |
| `reviewing` | All micro-tasks done, validation loop is running |
| `blocked` | Workflow cannot proceed — waiting on human, dependency, or max retries |
| `done` | All quality gates passed, merged to main |

## Status File Format

Each workflow maintains `.workflow/<feature-name>/status.json`:

```json
{
  "feature": "semantic-caching",
  "source": "docs/features/semantic-caching/spec.md",
  "state": "executing",
  "created": "2026-04-12T13:00:00Z",
  "updated": "2026-04-12T14:32:00Z",
  "micro_tasks": {
    "total": 12,
    "done": 8,
    "in_progress": 2,
    "waiting": 2,
    "blocked": 0
  },
  "agents": {
    "active": ["backend-1", "backend-2", "test-1", "test-2", "frontend-1", "infra-1"],
    "count": 6
  },
  "validation_loop": {
    "iteration": 0,
    "max": 30,
    "gates": {
      "code_quality": "not_started",
      "test_coverage": "not_started",
      "security": "not_started",
      "functionality": "not_started",
      "documentation": "not_started",
      "operations": "not_started"
    }
  },
  "blocker": null,
  "retry_count": 0
}
```

## Query Patterns

### List All Workflows

```bash
for dir in .workflow/*/; do
  feature=$(basename "$dir")
  state=$(python3 -c "import json; print(json.load(open('$dir/status.json'))['state'])")
  echo "$feature: $state"
done
```

### Get Blocking Workflows

```bash
for dir in .workflow/*/; do
  blocker=$(python3 -c "
import json
s = json.load(open('$dir/status.json'))
b = s.get('blocker')
print(b['type'] if b else 'none')
")
  if [ "$blocker" != "none" ]; then
    echo "$(basename "$dir"): BLOCKED by $blocker"
  fi
done
```

### Get Validation Loop Status

```bash
python3 -c "
import json, sys
feature = sys.argv[1]
with open(f'.workflow/{feature}/status.json') as f:
    s = json.load(f)
loop = s['validation_loop']
print(f'Iteration: {loop[\"iteration\"]}/{loop[\"max\"]}')
for gate, status in loop['gates'].items():
    mark = '✓' if status == 'pass' else '✗' if status == 'fail' else '·'
    print(f'  {mark} {gate}: {status}')
" semantic-caching
```

## Dashboard Generation

Generate `.workflow/dashboard.md` from all workflow status files:

```
Read all .workflow/*/status.json files
Group by state: proposed, scanning, decomposing, executing, reviewing, blocked, done
Count agents across all active workflows
Compute overall progress: done_micro_tasks / total_micro_tasks
Compute loop pass rate: workflows_exited_loop / total_loop_attempts
Write formatted markdown to .workflow/dashboard.md
```

## Integration with /multi-agent-status Command

When `/multi-agent-status` is run:

1. Read `.workflow/dashboard.md` (cached, updated every 60s by PM agent)
2. If dashboard is stale (>60s old), trigger a fresh scan
3. Apply filters if flags are provided (--backlog, --in-progress, --review, --blocked, --completed)
4. If a feature name is provided, show detailed status from that workflow's status.json
5. Format and display
