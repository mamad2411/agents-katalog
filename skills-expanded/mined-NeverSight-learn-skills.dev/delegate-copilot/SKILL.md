---
name: delegate-copilot
description: Delegate work to GitHub Copilot CLI so token usage and rate-limit pressure can be shifted off the current lane.
allowed-tools: Bash(copilot *)
disable-model-invocation: true
---

# Delegate Copilot

Use the local `copilot` CLI as a delegated execution lane for interactive or programmatic prompt execution.

## What this skill should do

1. Convert the request into a compact Copilot prompt.
2. Hand the work off to Copilot in non-interactive mode.
3. Return the result and mention the selected model when relevant.
4. Surface the top recommendations or dissenting view.

## Default command

```bash
copilot -p "$ARGUMENTS" --allow-all-tools
```

## Useful variants

```bash
copilot -p "$ARGUMENTS" --model gpt-5 --allow-all-tools
copilot -p "$ARGUMENTS" --continue --allow-all-tools
copilot -p "$ARGUMENTS" --output-format=json --allow-all-tools
copilot -p "$ARGUMENTS" --silent --allow-all-tools
```

## Good prompts

- Review this code for hidden failure modes.
- Suggest a cleaner interface for this service object.
- Compare this approach with a queue-based design.
- Explain what is fragile in this deployment workflow.

## Notes

- `-p` or `--prompt` executes a prompt programmatically and exits after completion.
- `--allow-all-tools` is required when using Copilot CLI programmatically so tools can run without confirmation.
- Use `--continue` to resume the most recent session.
- Use `--output-format=json` for JSONL output in automation.
- Use `--silent` with `-p` when you want only the agent response without usage statistics.
- The exact CLI name can vary by installation; adjust if your binary is not `copilot`.
- If Copilot CLI is missing, explain that it must be installed and authenticated first.
