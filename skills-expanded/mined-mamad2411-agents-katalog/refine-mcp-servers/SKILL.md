---
name: refine-mcp-servers
description: Use when iterating an existing MCP server to improve schema quality, robustness, transport behavior, and operator ergonomics.
---

# Refine MCP Servers

## Specialization

Improve existing MCP servers through bounded, evidence-based deltas that preserve compatibility while raising quality.

## Trigger Conditions

- An existing MCP server is functional but needs quality improvements.
- Tool/resource/prompt contracts are ambiguous or weakly validated.
- Transport, auth, or observability behavior needs hardening.

## Hard Constraints

- Official MCP sources only, from [source-catalog.md](./references/source-catalog.md).
- SDK implementation guidance limited to C# and TypeScript.
- No community aggregators or unofficial source lists.

## Inputs

- Current server behavior and known issues.
- Change goals and non-regression constraints.
- Existing test evidence and operational signals.

## Required Outputs

- Prioritized delta backlog with severity and effort.
- Non-breaking refinement plan with ordered rollout.
- Verification matrix for compatibility and behavior.
- Residual risk list with owner and follow-up action.

## Deterministic Workflow

1. Establish baseline behavior and known constraints.
2. Classify findings: contract, transport, security, observability, or developer experience.
3. Prioritize deltas by risk reduction and compatibility safety.
4. Apply bounded changes with explicit non-regression checks.
5. Verify via inspector and SDK-level tests.
6. Publish refinement disposition with remaining risks.

## Refinement Heuristics

- Prefer additive changes before breaking changes.
- Preserve tool semantics unless explicitly reversioned.
- Strengthen schema validation before extending behavior.
- Improve failure messaging and progress signaling for long operations.

## Verification Matrix Template

| Area | Check | Evidence |
|---|---|---|
| Tool contracts | Input/output schema stability | Tool list and call results |
| Resource contracts | URI, pagination, and update signaling | Resource list/read and update notifications |
| Prompt contracts | Argument handling and return format | Prompt list/get outputs |
| Transport behavior | Timeout, session, and reconnect behavior | Inspector UI or CLI traces |

## Done Criteria

- Required outputs are complete.
- No unapproved breaking changes remain.
- Verification matrix is complete with evidence.
