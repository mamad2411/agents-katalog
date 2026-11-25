---
name: n8n-workflow-as-code
description: >-
  Treat n8n workflows as code with the official @n8n/workflow-sdk: convert
  workflow JSON to SDK TypeScript for a readable pull-request diff, convert SDK
  code back to JSON, validate a workflow offline against generated node
  definitions, render a Mermaid graph for docs, and build through the official
  n8n MCP server's create_workflow_from_code. Use when a reviewer needs to read
  a workflow change, when the task says workflow-as-code, SDK, TypeScript
  workflow, json-to-code, code-to-json, Mermaid diagram of a workflow, or when
  building a workflow through the official n8n MCP rather than n8n-mcp. Not for
  node parameter lookup (n8n-node-configuration) or deploying (n8n-instance-ops,
  n8n-promotion-pipeline).
---

# n8n workflow as code

Written 2026-10-19 from `@n8n/workflow-sdk` 0.36.5 (first published
2026-02-16, part of `github.com/n8n-io/n8n`, bundles `n8n-workflow` 2.43.5).
Verified on this machine: `generateWorkflowCode`, `workflowToMermaid` and
`validateWorkflow` all ran on a real workflow JSON. Re-check the export list
with `node -e 'console.log(Object.keys(require("@n8n/workflow-sdk")))'` when
the pin moves.

## The rule that does not change

**Workflow JSON in git is still the source of truth.** SDK code is a second
view of it, like the canvas: better for a human reviewer, not a replacement
for the artifact the instance runs. Generate code from JSON for review;
generate JSON from code for deploy; never let the two be edited independently
without a round trip (`json-to-code` then `code-to-json` must reproduce the
behavior, check with `scripts/wf-diff.sh`).

## What the package gives you

| Need | Call |
|---|---|
| Readable diff of a workflow change | `workflow-sdk json-to-code <file.json>` or `generateWorkflowCode(wf)` |
| Build JSON from code | `workflow-sdk code-to-json <file.ts>` or `parseWorkflowCode(src)` |
| Offline validation with parameter schemas | `workflow-sdk validate <file.ts> [--node-types <dir>]` or `validateWorkflow(wf)` |
| Architecture diagram for a runbook | `workflowToMermaid(wf)` |
| Lint Python Code nodes | `lintPythonCode(src)` |
| The SDK reference the official MCP uses | `require('@n8n/workflow-sdk/prompts/sdk-reference')` |

Binary: `workflow-sdk` (`node_modules/.bin/workflow-sdk`). Pin it in the
engagement like `n8n-mcp`: `npm i --save-exact @n8n/workflow-sdk@0.36.5`.
It pulls `n8n-workflow` at a fixed version, so its idea of node versions is
tied to that n8n release; a customer on an older n8n may see `typeVersion`
values the instance does not have. Compare against `doctor.sh`'s reported
instance version before trusting a validation pass.

## Pull-request review recipe

What a reviewer sees today for a workflow change is a JSON blob where a
dragged node and a changed credential look the same. Two layers fix that:

1. `scripts/wf-textconv.mjs` as the git `textconv` for `workflows/**/*.json`
   (the engagement scaffold wires it): `git diff` shows normalized behavior,
   positions and ids gone.
2. For anything beyond a one-line parameter change, attach the generated code:

```bash
npx workflow-sdk json-to-code workflows/dev/order-intake.json > /tmp/order-intake.ts
```

Output shape (verified):

```ts
const set_Greeting = node({
  type: 'n8n-nodes-base.set',
  version: 3.5,
  config: { name: 'Set Greeting', parameters: { ... }, position: [220, 0] }
});
const wf = workflow('', 'hello-set', { executionOrder: 'v1' });
export default wf.add(when_clicking_Test_workflow).to(set_Greeting)
```

Node declarations are one per node, wiring is `.add().to()` chains, control
flow uses `ifElse`, `switchCase`, `merge`, `splitInBatches`, `nextBatch`, AI
sub-nodes use `languageModel`, `memory`, `tool`, `outputParser`,
`vectorStore`, `embedding`. A reviewer reads the wiring in ten lines instead of
a `connections` object.

Mermaid for the runbook, next to the workflow table:

```bash
node -e 'const s=require("@n8n/workflow-sdk");console.log(s.workflowToMermaid(JSON.parse(require("fs").readFileSync(process.argv[1],"utf8"))))' workflows/dev/order-intake.json
```

## Offline validation

`validateWorkflow(wf)` returns `{ valid, errors, warnings }` over the graph and
node schemas. Parameter-level checks need generated node definitions, which the
CLI resolves from the workflow file's directory and cwd, from
`N8N_NODE_DEFINITION_DIRS` (path-separated), or `--node-types <dir>` (repeat).
Definitions live in `n8n-nodes-base/dist/node-definitions` when
`n8n-nodes-base` is installed next to the SDK; without them the validator
checks structure only and says so in its trailer. Errors block, warnings do
not.

This complements, not replaces, `scripts/validate.sh` (structural, zero
dependencies) and n8n-mcp's `validate_workflow` (node schemas for 2,500+
nodes including community ones). Run the dependency-free one everywhere, the
SDK one where Node packages are allowed, n8n-mcp's where that server is
present.

## Building through the official n8n MCP

The official instance-level MCP server exposes `get_workflow_sdk_reference`,
`get_workflow_best_practices`, `create_workflow_from_code`, `validate_workflow`,
`test_workflow`, `get_workflow_history`, `get_workflow_versions_diff`,
`restore_workflow_version`, and `publish_workflow`. Its build loop:

1. `get_workflow_sdk_reference` (never write SDK code from memory; the
   reference is versioned with the instance).
2. `get_workflow_best_practices` once per technique (`scheduling`, `triage`,
   `document_processing`, `human_in_the_loop`, ...).
3. `search_nodes` and `validate_node_config` per node.
4. `create_workflow_from_code`, then `validate_workflow`, then `test_workflow`.
5. `publish_workflow` only after a passing test and a read-back.

Rules the reference enforces, which carry over to hand-written SDK code:
credentials via `newCredential('Name')`, never a synthesized id; input and
output indices are 0-based (`merge.input(0)` is the first input); do not add
`alwaysOutputData` to keep an empty chain alive; `executeOnce: true` on nodes
that must not run per item; inserting a node changes what downstream `$json`
reads; polling triggers that create records need a mark-as-handled step after
the create.

Version history on the official server (`get_workflow_history`,
`get_workflow_versions_diff`) is the instance's own audit trail. It is not git.
Export and commit remain the rollback point the customer controls.

## When not to use code

- A one-parameter change on a live workflow: `n8n-instance-ops`, partial
  update, read-back. Code adds nothing.
- A customer whose reviewers never read TypeScript: ship the textconv diff and
  the Mermaid graph, skip the `.ts` attachment.
- Instances older than the SDK's bundled `n8n-workflow`: validate with
  n8n-mcp against the instance's version instead.

## Related

- `n8n-promotion-pipeline`: the gates and the mechanism that moves the JSON.
- `n8n-canvas-docs`: positions are stripped from diffs, but the canvas layout
  is still a deliverable; the layout checker runs on the JSON.
- `n8n-mcp-tools-expert`: the community server's `validate_workflow` and
  `get_node`, which cover community nodes the SDK does not.
