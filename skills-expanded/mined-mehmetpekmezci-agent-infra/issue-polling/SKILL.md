---
name: issue-polling
description: Continuously check the project-01 Gitea issues assigned to the Worker and pick the next one to work on. Use this skill whenever the Worker agent starts, finishes an issue and resets, or has no current task, and whenever the Worker must decide which issue to do next, even if the user only says "start working" or "check for tasks".
---

# issue-polling

The Worker has no task list of its own. The Gitea issues assigned to it are the task list, and the Worker reads them in a loop.

## Procedure

1. Find the next issue:

```bash
python3 $AGENT_INFRA_DIR/harness/worker-skills/issue-polling/scripts/next_issue.py
```

The script prints the oldest open issue assigned to this Worker as JSON. It skips `status:blocked` and `status:done`. Exit code 1 means there is nothing to do.

2. When there is nothing to do, wait and check again. Do not invent work:

```bash
python3 .../next_issue.py --wait 60
```

3. Claim the issue before starting, so the Coordinator sees it is taken:

```bash
python3 $AGENT_INFRA_DIR/harness/base-skills/gitea-issues/scripts/gitea.py status <n> in-progress
```

4. Load the role with `role-loader`, do the work, then finish with `issue-completion` and `worker-reset`.

## Rules

- Work on one issue at a time. Finish or block it before looking at the next.
- An issue already `status:in-progress` and assigned to you means an earlier session was interrupted. Read its comments first, then resume.
- Read all comments, not only the issue body. The Human or Coordinator may have changed the task.
- If an issue has no `Role:` line, do not guess. Return it with `status:blocked` and a comment asking the Coordinator for the role.
