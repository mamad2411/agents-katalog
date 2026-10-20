---
name: write-mcp-servers
description: Use when creating a new MCP server implementation with expert-level contracts for tools, resources, prompts, transports, and operational safety.
---

# Write MCP Servers

## Specialization

Design and author MCP servers with explicit contracts, deterministic implementation steps, and release-ready defaults.

## Trigger Conditions

- A new MCP server must be built.
- Existing APIs or workflows need first-time MCP exposure.
- A reusable server template is required for cross-project adoption.

## Hard Constraints

- Use only official MCP sources listed in [source-catalog.md](./references/source-catalog.md).
- Limit SDK implementation guidance to C# and TypeScript.
- Exclude community aggregator sources.

## Inputs

- Server objective and user outcomes.
- Tool/resource/prompt candidates.
- Transport and deployment constraints.
- Security and authentication requirements.

## Required Outputs

- Primitive contract set: tools, resources, prompts, and capability declarations.
- Transport contract with default and fallback behavior.
- Implementation checklist with deterministic validation steps.
- Risk list with mitigation and ownership.

## Deterministic Workflow

1. Define server objective and non-goals.
2. Classify primitives into tools, resources, and prompts.
3. Define input/output schemas and validation behavior.
4. Select transport model and session strategy.
5. Define authentication and sensitive-operation boundaries.
6. Define observability: logs, progress, and notifications.
7. Validate using inspector-driven test cases.
8. Publish completion summary with residual risks.

## Output Quality Rules

- Tool contracts must specify side effects and error semantics.
- Resource contracts must be read-safe and explicitly bounded.
- Prompt contracts must include argument behavior and defaults.
- Transport selection must include rationale and operational limits.

## Validation Checklist

- Schema coverage complete for all exposed primitives.
- Error paths and cancellation behavior documented.
- Inspector test run includes list/call/read/get flows.
- Security-sensitive tools include auth and authorization notes.

## Done Criteria

- Required outputs are complete and consistent.
- Policy constraints are satisfied.
- Validation checklist has no open critical gaps.
