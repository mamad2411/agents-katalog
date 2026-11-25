---
name: workflow-kit
description: Use Agent Workflow Kit workflow commands in Pi.
---

# Workflow Kit

Use registered commands and tools to run workflows. Fallback to the shared CLI:

```sh
agent-workflow-kit workflow "<task>" --json
agent-workflow-kit workflow-run no-write-probe --json
agent-workflow-kit workflow-run <workflow> --args-json '{"key":"value"}' --json
agent-workflow-kit workflow-run <workflow> --stream --json
agent-workflow-kit workflow-status <run-id> --json
agent-workflow-kit workflow-status <run-id> --tree
agent-workflow-kit workflow-events <run-id> --json
agent-workflow-kit workflow-events <run-id> --follow
agent-workflow-kit workflow-resume <run-id> --json
agent-workflow-kit workflow-stop <run-id> --json
agent-workflow-kit workflows --json
agent-workflow-kit workflows --watch
agent-workflow-kit deep-research "<question>" --json
agent-workflow-kit ultracode on --json
agent-workflow-kit ultracode off --json
agent-workflow-kit ultracode status --json
```

Saved workflow scripts read structured args from `context.args`.
Generated workflow runs return `args.workflow.name` and `args.workflow.path` for later `workflow-run`.
Use `workflow-run --stream --json` for long launches: event lines go to stderr and the final run JSON stays on stdout.
Use `workflow-events --follow` for an existing run id instead of repeatedly polling.

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
agent-workflow-kit workflow-status "$run_id" --tree
agent-workflow-kit workflow-events "$run_id" --json
agent-workflow-kit workflow-resume "$run_id" --json
agent-workflow-kit workflow-stop "$run_id" --json
agent-workflow-kit workflows --json
AGENT_WORKFLOW_KIT_WATCH_ITERATIONS=1 agent-workflow-kit workflows --watch
agent-workflow-kit deep-research "file-command-smoke" --json
```

Persist run metadata with the host session APIs when available.
<!-- AGENT_WORKFLOW_KIT_ULTRACODE_START -->
## Ultracode & multi-phase orchestration

Authoring and running a workflow spins up many subagents and spends real tokens. Author a workflow only when the user typed "workflow"/"workflows", asked for multi-agent orchestration, when the **ultracode** standing opt-in or keyword trigger applies, when a skill or command instructed it, or when the user named a saved workflow. Otherwise act directly or offer a workflow and let the user opt in.

**Ultracode** has three separate meanings in this kit. The standing opt-in is the persisted project behavior (`agent-workflow-kit ultracode on|off|status`, stored in `.agent-workflow-kit/config.json`) that author-runs a workflow for substantive tasks by default. The keyword trigger is recorded separately as `ultracodeKeywordTriggerEnabled` and is disabled when workflows are disabled. Model effort is host-owned: this standalone CLI reports model effort as unsupported and records `ultracodeEffortMode: "orchestration-only"` when orchestration is enabled. Turn ultracode on only when the user asks; when off, revert to the opt-in gate.

For larger work, decompose into a **sequence** of workflows (understand -> design -> implement -> review), inspecting each run with `workflow-run --stream`, `workflow-events --follow`, or `workflow-status --tree` between phases rather than one giant run.
<!-- AGENT_WORKFLOW_KIT_ULTRACODE_END -->
