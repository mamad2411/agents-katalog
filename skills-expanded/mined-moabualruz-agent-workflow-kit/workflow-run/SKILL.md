---
name: workflow-run
description: Run a saved Agent Workflow Kit workflow in Antigravity.
---

# Workflow Run

Run saved workflows through the shared CLI:

```sh
agent-workflow-kit workflow-run <workflow> --json
agent-workflow-kit workflow-run <workflow> --args-json '{"key":"value"}' --json
agent-workflow-kit workflow-run <workflow> --stream --json
agent-workflow-kit workflow-status <run-id> --json
agent-workflow-kit workflow-events <run-id> --json
agent-workflow-kit workflow-events <run-id> --follow
agent-workflow-kit workflow-resume <run-id> --json
agent-workflow-kit workflow-stop <run-id> --json
agent-workflow-kit workflows --json
agent-workflow-kit deep-research "<question>" --json
agent-workflow-kit ultracode status --json
```

Saved workflow scripts read structured args from `context.args`.
Use `workflow-run --stream --json` for long launches: event lines go to stderr and the final run JSON stays on stdout.
Use `workflow-events --follow` for an existing run id instead of repeatedly polling.

Use `--project-root "${AGENT_WORKFLOW_KIT_PROJECT_ROOT:-$PWD}"` when the active Antigravity workspace root is ambiguous.

Executable smoke:

```sh
generated_json="$(agent-workflow-kit workflow "file command generated" --json)"
generated_name="$(printf '%s' "$generated_json" | bun -e 'const fs = require("fs"); const data = JSON.parse(fs.readFileSync(0, "utf8")); console.log(data.args.workflow.name);')"
printf '%s\n' "$generated_json"
agent-workflow-kit workflow-run "$generated_name" --json
run_json="$(agent-workflow-kit workflow-run no-write-probe --json)"
run_id="$(printf '%s' "$run_json" | bun -e 'const fs = require("fs"); const data = JSON.parse(fs.readFileSync(0, "utf8")); console.log(data.runId);')"
printf '%s\n' "$run_json"
agent-workflow-kit workflow-status "$run_id" --json
agent-workflow-kit workflow-events "$run_id" --json
agent-workflow-kit workflow-resume "$run_id" --json
agent-workflow-kit workflow-stop "$run_id" --json
agent-workflow-kit workflows --json
agent-workflow-kit deep-research "file-command-smoke" --json
```
