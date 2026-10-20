---
name: profiles
description: "Browse engineering role profiles and compare their priorities, boundaries and verification. Use to discover roles; profile selects or clears the active task role, while tools discovers actions."
---

# profiles

Browse engineering role profiles and compare their priorities, boundaries and verification.

## Choose this workflow

Use to discover roles; profile selects or clears the active task role, while tools discovers actions.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [General methods](../../references/packs/general.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect only. Accept a role, discipline, level or task description as appended context.

**Pack prerequisites:** Resolve the user brief and inspect the relevant project or supplied evidence. External capabilities are optional unless the selected action actually needs them.

- **Infer from evidence:** Resolve the named files, existing scripts, current task and earlier corrections from the conversation and repository.
- **Reasonable default:** Use the narrowest interpretation that completes a reversible local task; state a consequential assumption once.
- **Ask only when needed:** Ask when competing targets or incompatible success conditions would change the result; continue independent inspection first.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

The shipped profile catalog and supplied task context.

No changes to active profile, project files, global settings or external state.

## Execute

1. Run toolkit profiles with the full relevant query; for specific details run toolkit profile ID. Read [profile selection](../../references/profiles.md) for scope and precedence.
2. Return a focused comparison and useful examples. Search is lexical discovery, not an authority or competence score.
3. Role discovery lists priorities and concrete contributions; browsing a role does not activate it.

## Technical method

- **Inspect:** Inspect role purpose, priorities, boundaries and candidate workflows relevant to the requested job.
- **Method:** Compare roles by concrete decision focus, then link the workflows supplying technical methods.
- **Avoid misdiagnosis:** A job title is neither a credential nor evidence that all specialty checks were performed.
- **Check the result:** Explain how candidate roles would change priorities on the same task without widening permissions or claiming a team exists.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [General worked example](../../references/examples/general.md).


## Decision branches

- **When several profiles appear relevant:** Compare primary responsibility and actual task evidence; show options without silently activating one.

## Deliver and verify

- Relevant role IDs, purpose, priorities and example use.
- Clear distinctions between close profiles and their suggested workflows.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Every listed profile exists in the installed catalog. Discovery leaves the active task selection unchanged.

## Stop and recover

- Do not activate a role, install tools or execute suggested workflows from a discovery request.

## Example requests

- **Normal (inspect):** Show profiles for machine learning engineering and model operations.
- **Edge (inspect):** Compare senior, staff, principal and software architect profiles for this migration.
- **Blocked (inspect):** Find a profile for an unsupported specialty without pretending it is installed.
