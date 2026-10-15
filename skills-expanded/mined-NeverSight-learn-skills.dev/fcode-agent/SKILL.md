---
name: fcode-agent
description: Iterative, confirmation-driven workflow for building Factorial Code processes and modules end to end — plan-and-confirm, discovery scripts, incremental implementation validated with the run_code MCP tool, exposing processes as MCP tools, plus security and error-handling practices. Use when asked to build, automate, or integrate something on Factorial Code (fcode) and you need the recommended working method.
license: MIT
metadata:
  category: factorial-code
---

# Factorial Code — agent workflow

How to build Factorial Code processes and modules through an iterative,
confirmation-driven approach, using the Factorial Code MCP tools. Pair this with
`fcode-core-concepts`, `fcode-javascript`/`fcode-python`, and `fcode-cli`.

## Core principles

- **Explain before acting** — describe what you'll do and why.
- **Confirm before changing** — get explicit approval before significant or
  destructive changes (refactors, dependency changes, variable changes).
- **Iterate in small steps** — deliver working increments, validate, then expand.
- **Be safe by default** — never hardcode or log secrets.

## Workflow

### Phase 1 — Plan & confirm

Before writing code or using any tool, produce a short plan and confirm it.

1. **Analyze current context.** Check the process language (`index.js` → JS,
   `main.py` → Python; new code must match), what the current script does, which
   variables/dependencies/modules already exist (don't remove or overwrite them).
2. **Identify alternatives.** For common needs (email, SMS, payments, storage),
   present options — third-party service vs direct protocol, library choices —
   with brief trade-offs, and ask the user to choose. Don't assume an approach
   when alternatives exist.
3. **Identify needed components:** config variables, secrets (the user must
   create these), input parameters (+ types), dependencies (verify they exist,
   prefer recent stable versions), and modules worth creating for reuse.
4. **Define input-parameter requirements** (fields, types, validations, any
   dynamic fields needing API calls). See `fcode-json-schema`.
5. **Present the plan** (what you'll build, variables you'll create vs the user
   must create, input parameters, dependencies, reusable modules, expected
   behavior) and ask "Shall I proceed?"
6. **Wait for explicit confirmation** before proceeding.

### Phase 2 — Iterative development

Work in small steps, confirming at each one.

- **Iteration 1 (setup & discovery):** create config variables and ask the user
  to create the sensitive ones; if useful, write a **discovery script** and run
  it with `run_code` to validate connectivity and learn the API/data shapes.
  Share results.
- **Iteration 2+:** for each step — explain it, get confirmation, implement
  following the language code rules (validation, error handling, logging),
  validate pieces with `run_code`, then create/update the process (code,
  parameters, descriptions). Tell the user what changed and let them review
  before the next iteration.

### Phase 3 — Test & refine (via the CLI)

Propose a full execution test using the `fcode` CLI (see `fcode-cli`), get
confirmation, run it with test parameters, review results together, and iterate.
Then offer next steps: scheduling, webhooks (maybe with auth), a form, or
exposing the process as an MCP tool — and pushing to cloud when ready.

## Creating MCP tools

Do **not** write standalone MCP server code. Any Factorial Code process becomes
an MCP tool: (1) create a process implementing the logic, (2) define its input
parameters via `parametersSchema.json` (they become the tool's parameters),
(3) **tag** the process (e.g. `mcp-tool`). It's then automatically available in
any MCP client connected to the Factorial Code MCP Server — tag and go.

## Available MCP tools

- **`run_code`** — execute JS/Python for validation and testing before updating
  process files.
- **`yc_api_<method>`** — manage Factorial Code resources (e.g.
  `yc_api_create_process`, `yc_api_update_process`, `yc_api_delete_process`).
- Use other Factorial Code MCP tools when needed.

## Code quality & security

- Try/catch (try/except) with meaningful messages; validate inputs at the start;
  log key steps; extract reusable logic into modules; clean up resources.
- **Never** hardcode or log secrets — always use variables/env vars; validate
  external inputs.
- See the module-naming and `variables.env` gotchas in `fcode-core-concepts`.

## Error handling

Explain what went wrong, propose a fix, and get confirmation — don't silently
retry. If tests fail repeatedly or the root cause is unclear, stop and ask the
user rather than trial-and-error.

## Anti-patterns

- Don't assume API structure without testing → use discovery scripts first.
- Don't create variables without checking what exists → review first.
- Don't overwrite the whole `variables.env` → read, then append/patch only.
- Don't write a whole complex process without testing parts → validate with
  `run_code` first.
- Don't guess between alternatives → present options and let the user choose.

## When to ask for help

Ask instead of guessing on: ambiguous requirements, missing info (credentials,
endpoints, package names), repeated failures, architecture/trade-off decisions,
security concerns, or uncertain root cause.

## Example

For a full worked example of this workflow (a Shopify → email integration),
read `references/example-interaction.md`.
