---
name: n8n-workflow-automation
description: "Build n8n automations: node contracts, expression syntax, error workflows, credentials handling and versioned export/import."
type: procedural
category: automation
domain: automation
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - n8n workflow design
  - n8n expression syntax
  - n8n error workflow
  - n8n self hosted setup
  - n8n credential handling
keywords:
  - n8n
  - automation
  - workflow
  - nodes
  - webhook
  - expressions
source: custom
enabled: true
---

# n8n Workflow Automation

## Purpose

Build n8n automations: node contracts, expression syntax, error workflows, credentials handling and versioned export/import.

## When to Use

- Business processes must be automated without bespoke services.
- An existing n8n workflow fails silently and needs error handling.
- Workflows must be exported, reviewed and versioned.

## When NOT to Use

- The integration needs transactional guarantees and typed contracts better served by code.
- The workflow handles regulated data without an approved storage path.
- You need realtime low-latency processing.

## Capabilities

- Design node flows with explicit inputs, outputs and error branches.
- Write expressions that reference node data safely.
- Attach error workflows and retries instead of relying on manual recovery.
- Version workflows as JSON in git and promote between instances.

## Inputs

- The trigger type (webhook, schedule, app event) and expected payload shape.
- The n8n version and whether it is cloud or self-hosted.
- Credential names available in the instance.

## Workflow

1. Start from the trigger and write down the payload contract.
2. Keep each node single-purpose; branch with Switch rather than nested IFs.
3. Add an error workflow that notifies and records the failed execution.
4. Store credentials in n8n's credential store; reference them by name.
5. Export the workflow JSON into git and import it into the next environment.

## Tools

- n8n editor
- n8n CLI (import/export)
- n8n MCP connector

## Examples

- `allskills mcp install --harness claude --servers n8n`
- `n8n export:workflow --all --output=workflows/`
- `allskills route "automate invoice processing"`

## Safety

- Webhook triggers without authentication accept anything the internet sends.
- Unbounded loops and retries can duplicate downstream side effects.
- Never hardcode credentials in node parameters; they leak in exports.

## Source

All-Skills canonical library (`skills/automation/n8n-workflow-automation`). First-party skill, maintained in this repository.

## Notes

- `$json` refers to the current item; `$node["Name"].json` reaches earlier nodes.
- Error workflows are the difference between silent failure and a fixable incident.
- Pairs with: `automation/automation-audit-ops`, `integration/webhook-delivery-design`.
