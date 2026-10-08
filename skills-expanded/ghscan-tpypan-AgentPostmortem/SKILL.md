---
name: retry
description: Preview or emit a guardrailed retry prompt from the latest non-command user task.
---

## What I do

- Preview or emit a retry prompt for the last failed user task
- Can explain, skip rule IDs, or confirm retry
- Safe for memory by default

## How to run

Call the tool directly:

```
tool: postmortem_retry
tool: postmortem_retry --skip rule-a --skip rule-b --explain
tool: postmortem_retry --yes
```

## Argument mapping

- `yes` (bool): Confirm retry
- `explain` (bool): Explain the retry
- `skip` (string[]): Rule IDs to skip
- `json` (bool): Output as JSON

## Safety

- All output is redacted by default for memory safety
- Never request or display secrets
- To delete all postmortem data, first run `tool: postmortem_config --action show --json` to get the `root` path, then delete it manually with `rm -rf "<root>"`.
- Repo-local storage is opt-in via `.opencode/postmortem.json`.
