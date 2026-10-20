---
name: gitea-issues
description: Read, create, comment on, assign, label, and change the state of issues in the project-01 Gitea repository using the agent's own access token. Use this skill whenever an agent must communicate through Gitea issues - picking up work, reporting results, assigning an issue to Human, Coordinator, or Worker, or changing issue status - even if the user only says "update the issue" or "tell the coordinator".
---

# gitea-issues

Gitea issues are the only message channel between Human, Coordinator, and Worker. Use the bundled CLI instead of hand-written HTTP calls: it already handles paging, auth, and label ids, so results are consistent between agents.

## Setup (already done by start_agents.sh)

The CLI reads these environment variables. `GITEA_ACCESS_TOKEN` comes from the agent's own `.kilo/kilo.jsonc` (`COORDINATOR1_PERSONAL_ACCESS_TOKEN` or `WORKER1_PERSONAL_ACCESS_TOKEN`), so every action is attributed to the right agent.

| Variable | Meaning |
| --- | --- |
| `GITEA_URL` | Base URL, e.g. `http://localhost:3000` |
| `GITEA_OWNER`, `GITEA_REPO` | Repository, normally `project-01` |
| `GITEA_ACCESS_TOKEN` | Token of the current agent |

Run `python3 scripts/gitea.py ensure-labels` once per repository. It creates the `status:*` and `role:*` labels.

## Commands

```bash
G="python3 $AGENT_INFRA_DIR/harness/base-skills/gitea-issues/scripts/gitea.py"
$G whoami                                   # login of the current agent
$G list --assignee <user> [--state open] [--label status:todo] [--json]
$G get <n> --comments                       # full issue + comment history as JSON
$G create --title "..." --body-file body.md --assignee <user> --label role:analyzer
$G comment <n> --body-file comment.md       # use '-' to read stdin
$G assign <n> <user> [<user>...]            # replaces assignees
$G status <n> todo|in-progress|blocked|done # swaps the status:* label only
$G state <n> open|closed
$G labels <n> --add X --remove Y
```

## Conventions

- **Status** lives in a `status:*` label (`todo`, `in-progress`, `blocked`, `done`) because Gitea only knows open/closed. Use `status` rather than editing labels by hand so only one status label exists at a time.
- **Role** for a Worker issue is written in the issue body on its own line: `Role: <Name>` (see `role-selection`). The `role:<name>` label is an optional mirror for filtering.
- Read the whole comment history (`get --comments`) before acting. Earlier comments often hold Human decisions that change the task.
- Write comments with the `issue-comment-protocol` skill and hand off with `gitea-assignment-handoff`.
- Never close an issue the agent did not work on.
