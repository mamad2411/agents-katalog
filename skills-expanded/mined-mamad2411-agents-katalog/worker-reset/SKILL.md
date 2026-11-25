---
name: worker-reset
description: Clean the Worker workspace and context after an issue is finished - run clear_worker.sh, then the /reset and /reload commands - so the next issue starts clean. Use this skill whenever the Worker has finished or blocked an issue and has posted its completion comment, and before it picks up another issue.
---

# worker-reset

Each issue should start with a clean workspace and an empty context. Leftover files, loaded roles, and old reasoning from the previous issue cause wrong assumptions in the next one.

## Order matters

Run this only after `issue-completion`. The reset removes everything that is not saved in the repository, wiki, or issue.

1. Check that the completion comment is posted and that the work is committed or saved.
2. Run the cleanup:

```bash
$AGENT_INFRA_DIR/harness/worker-skills/worker-reset/scripts/reset_worker.sh
```

This calls `$AGENT_INFRA_DIR/harness/clear_worker.sh`.

3. Run the agent command `/reset`.
4. Run the agent command `/reload`. It reloads the skills and configuration, including the `.kilo/skills` links.
5. Go back to `issue-polling`.

`/reset` and `/reload` are commands of the agent, not shell commands, so the script only reminds you to run them.
