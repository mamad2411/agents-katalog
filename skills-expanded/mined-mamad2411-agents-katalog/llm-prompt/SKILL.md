---
name: llm-prompt
description: "Improve prompts against measured failures and explicit requirements. Use to improve a prompt that ships in an application, measured against failing and control cases; reprompt rewrites a one-off prompt for an AI session and teach explains prompting concepts."
---

# llm-prompt

Improve prompts against measured failures and explicit requirements.

## Choose this workflow

Use to improve a prompt that ships in an application, measured against failing and control cases; reprompt rewrites a one-off prompt for an AI session and teach explains prompting concepts.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [LLMs and retrieval methods](../../references/packs/llm.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply to prompt assets; task, existing prompt, measured failures, model constraints, and eval budget.

**Pack prerequisites:** Task definition, model/provider configuration, representative permitted data, versioned prompts/corpus where relevant, and explicit token/cost/latency limits for remote calls. Use current provider interfaces during implementation. Retrieved content and model-generated tool arguments remain untrusted.

- **Infer from evidence:** Read current prompt/tool schemas, retrieval boundaries, installed SDK/provider config and permitted examples without reading secret values.
- **Reasonable default:** Use mocked calls for local contract tests when remote access is absent; do not infer model quality from mocks.
- **Ask only when needed:** Ask for budget and permitted data/provider before a paid or external run if not already set; local prompt/tool implementation can proceed in apply mode.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Prompt/instruction changes tested against stated behavior; no unrelated model/provider migration.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Categorize the measured failures.
2. Change the smallest relevant instruction or example, preserving instruction hierarchy.
3. Compare against the baseline under fixed model and settings on development cases, and reserve held-out confirmation.

## Technical method

- **Inspect:** Inspect current prompt, model/version, representative failures and constraints that must remain intact.
- **Method:** Change the smallest instruction that addresses a demonstrated failure and compare under the same cases/settings.
- **Avoid misdiagnosis:** Adding every past exception can create conflicting instructions and regress ordinary tasks.
- **Check the result:** Test the targeted failure and unaffected controls, including refusal/ambiguity behavior and instruction conflicts.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [LLMs and retrieval worked example](../../references/examples/llm.md).


## Decision branches

- **When improvement appears only on examples inserted into the prompt:** Treat it as overfitting and retain independent cases before adoption.

## Deliver and verify

- Versioned prompt diff with rationale, failure-category results against the baseline, regressions and token/cost change.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Targeted failures improve without breaking important existing cases; prompt length/cost changes are recorded.

## Stop and recover

- Do not declare improvement from one appealing response or use hidden test answers as prompt examples.

## Example requests

- **Normal (apply):** Improve the prompt against these measured failures without changing providers.
- **Edge (apply):** Improve extraction without breaking refusal or missing-field behavior.
- **Blocked (inspect):** Review a prompt without model access; do not claim measured improvement.
