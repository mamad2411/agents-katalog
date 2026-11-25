---
name: comfyui-workflow-validation
description: Use when a ComfyUI workflow fails to load, validate, queue, execute, or produce expected outputs, or when checking node availability, links, inputs, models, workflow JSON, frontend/API representation, or compatibility before execution.
metadata:
  version: "00.01.11"
---
# ComfyUI Workflow Validation

## Validation layers

Validate in this order where applicable:

1. JSON parse and representation detection;
2. current/version-matched workflow schema;
3. live node existence;
4. input names and required values;
5. output/link compatibility;
6. enum/model/resource values exposed by the target;
7. custom-node-specific constraints;
8. official validator/test framework when available;
9. representative execution only after preflight passes.

## CLI failure guidance

If validation is happening because a `comfy-cli` job failed, inspect the current/version-matched CLI debugging guidance in addition to this structural validation skill. Use the CLI guidance for its error envelope and remediation flow; use the target schema/node catalog for workflow correctness.

## Live catalog

Prefer the running target's node definitions over a bundled/static catalog. A static catalog cannot prove that the user's installed custom nodes match it.

If the `comfyui-development` skill is available, use its conservative workflow-preflight helper as a fallback. Activate that skill through the harness rather than assuming its files are reachable from this skill directory. The fallback is not a substitute for a stronger current official validator when one is available.

## Official tooling

When `comfy-cli`, `comfy-mcp`, or the official test framework is installed, inspect its current help/docs and use the relevant validation command. Do not assume command syntax from an old version.

A command invocation succeeding is not the same as a valid workflow. Read the returned verdict/errors.

## Debugging procedure

1. Preserve the failing workflow before edits.
2. Capture exact error text and server/browser logs.
3. Determine frontend vs API representation.
4. Compare failing node definitions with live target data.
5. Check whether custom-node imports failed at startup.
6. Check resource/model names against target choices.
7. Reduce to a minimal failing graph if the cause remains unclear.
8. Make one causal fix at a time.
9. Revalidate.

## Do not

- randomly rewire sockets until the error disappears;
- replace missing nodes with unrelated alternatives without explaining the semantic change;
- clear queues/history or delete user data as a diagnostic shortcut;
- upgrade the user's installation unless the task is specifically an upgrade.

## Acceptance gate

Before calling a workflow fixed or valid:

- preserve the original failing workflow;
- capture the exact failure evidence;
- identify the workflow representation;
- resolve all deterministic validation errors found by the strongest available validator;
- re-run validation after the fix;
- report any live/runtime gate that could not be completed instead of treating it as a pass.

