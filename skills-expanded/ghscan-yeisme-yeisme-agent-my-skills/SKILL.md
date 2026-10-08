---
name: yeisme-mcp-builder
description: Use when creating, structuring, reviewing, or documenting self-built MCP servers, tools, transports, schemas, adapters, or debugging entry points under this repository's mcp/ directory.
---

# Yeisme MCP Builder

Use this skill when the requested work is about self-built MCP capability in this repository.

## Boundary

- Put MCP implementations under `mcp/`.
- Put reusable agent workflow instructions under `.skills/imported/`.
- Put CLI wrappers under `cli/`.
- Put gateway runtime and deployment assets under `apigateway/`.
- If a capability has both CLI and MCP surfaces, keep the project under `mcp/` and provide a CLI entry there when it is tightly coupled to the MCP service.
- Prefer CLI plus skills when the task is local, project-specific, or already well supported by tools such as `gh`. Use MCP mainly for cross-project, cross-service, reusable, or long-lived integration surfaces.

An MCP can have a companion skill, but the skill should explain how to build, test, or review the MCP. It should not contain the MCP implementation.

## Tool Surface Policy

Expose as few MCP tools as practical. The default shape should be:

- `search`: discover, list, query, inspect, or preview available targets.
- `execute`: perform an action against a selected target with explicit parameters.

Add more tools only when one of these is true:

- The schema would become ambiguous or unsafe if folded into `search` or `execute`.
- The action has materially different permissions, side effects, or audit requirements.
- A separate tool significantly reduces tokens for common calls.

Use Cloudflare's official MCP style as a reference point for compact, task-oriented tool surfaces: broad capability behind small numbers of well-scoped tools, structured inputs, and explicit account/resource boundaries.

## CLI First Rule

Before creating or using an MCP, check whether a CLI already solves the job cleanly.

- If `gh`, cloud CLIs, package managers, or repo scripts can do the job with low context, prefer CLI plus a skill.
- For GitHub workflows, `gh` plus a project skill is usually better than GitHub MCP unless cross-project automation, service-to-service reuse, or live tool discovery is required.
- Do not create an MCP just to wrap one local command.
- Use MCP when the value is portability across projects, consistent service access, permission mediation, or a stable agent-facing interface.

The goal is not to avoid MCP. The goal is to reserve MCP for places where it beats CLI on reuse, boundary control, and integration reach.

## Token Budget Policy

Design MCP responses to stay close to CLI efficiency.

- Return compact structured data by default.
- Support pagination, limits, filters, and field selection.
- Avoid dumping large documents, logs, diffs, or search results unless explicitly requested.
- Prefer stable IDs and short summaries, then let `execute` fetch or act on a selected item.
- Include enough context for the next step, not the whole world.
- Make verbose output opt-in with a parameter such as `detail`, `include`, or `format`.

If a CLI command gives a shorter, clearer answer than the MCP tool, improve the MCP response shape or use the CLI.

## Permission Policy

Every MCP must define permission boundaries before implementation:

- allowed operations
- denied operations
- credential source
- resource scope
- read-only versus write modes
- confirmation requirements for destructive actions
- audit/logging behavior

Default to read-only search and explicitly gated execution. `execute` should validate both the requested action and the target resource before doing work.

## MCP Work Checklist

1. Identify the MCP boundary:
   - server
   - tool
   - resource
   - prompt
   - transport
   - adapter
   - local debug entry
2. Create a focused directory under `mcp/<mcp-name>/`.
3. Define the contract before implementation:
   - tool names
   - input schemas
   - output schemas
   - side effects
   - credentials
   - timeout and retry behavior
4. Start with `search` and `execute`; justify any additional tool in the MCP README or design notes.
5. Add local debug instructions in the MCP directory.
6. Keep real credentials in user-level local config, a user-level secret store, service-local ignored env files, documented environment variables, or deployment secret managers. Do not commit real credentials or add shell credential scripts as the persistence path.
7. Add tests or a repeatable smoke command when the implementation has executable code.

## Recommended Layout

```text
mcp/<mcp-name>/
  README.md
  src/
  tests/
  examples/
```

Use the repository's actual language and package patterns once they exist. Do not introduce a new framework if the MCP can fit an existing local convention.

If the MCP and CLI are inseparable, use:

```text
mcp/<mcp-name>/
  README.md
  src/
  cli/
  tests/
  examples/
```

Do not split a tightly coupled CLI into top-level `cli/` just to satisfy directory purity. Use top-level `cli/` for shared human/deploy entry points that are not owned by one MCP.

## Review Points

- Tool names are stable and descriptive.
- The tool count is minimal, usually `search` and `execute`.
- Inputs are validated with structured schemas.
- External side effects are explicit.
- CLI was considered first, especially for GitHub and local project workflows.
- Responses are compact and support limits or field selection.
- Permissions are enforced by mode, credential scope, and target resource.
- Errors are actionable and do not leak secrets.
- Timeouts prevent hanging agent sessions.
- Debug commands can be run by another developer.

## When Not To Use

Do not use this skill for:

- ordinary skill authoring in `.skills/imported/`
- agent runtime integration under `agent/`
- gateway deployment under `apigateway/`
- generic code review unrelated to MCP
