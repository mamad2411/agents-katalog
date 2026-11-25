---
name: cli-forge-plan
description: "Plan stage for the cli-forge skill family: define the detailed CLI contract including commands, flags, output formats, capability scope, and daemon contract before scaffold or extend stages proceed."
---

# cli-forge Plan

Use this stage to translate the approved design contract into a detailed,
actionable CLI contract that Scaffold, Extend, and Validate will consume as
their authoritative reference.

## Purpose

Define the detailed CLI contract: every command, every flag, every output
format, every behavioral rule. This stage answers the question **"How does the
CLI work?"** while the Design stage upstream answered **"What is this skill?"**

The `cli-plan.yml` produced by this stage is the single source of truth that
Scaffold uses for template expansion, Extend uses for capability pre-checks,
and Validate uses as the compliance baseline.

## Canonical References

- [`./instructions/plan-cli.md`](./instructions/plan-cli.md)
- [`../planning-brief.md`](../planning-brief.md)
- [`../contracts/cli-plan.yml.tpl`](../contracts/cli-plan.yml.tpl)
- [`../contracts/design-contract.yml.tpl`](../contracts/design-contract.yml.tpl)

## Entry Gate

| #   | Check                                         | Source       |
| --- | --------------------------------------------- | ------------ |
| 1   | `design-contract.yml` exists and is approved  | Design stage |
| 2   | Skill scope is clear from the design contract | Design stage |

## Required Inputs

- Approved `design-contract.yml` from the Design stage
- User requirements for CLI behavior (commands, flags, formats)
- Capability scope decisions (stream, repl, daemon: in-scope or out-of-scope)

## Workflow

1. Load the approved `design-contract.yml` from `.cli-forge/`.
2. Read [`../planning-brief.md`](../planning-brief.md) to load the shared
   constraints.
3. Follow the detailed steps in
   [`./instructions/plan-cli.md`](./instructions/plan-cli.md).
4. Define the command tree:
   - Primary CLI entrypoint
   - Subcommands (if any)
   - The `help` subcommand (always present)
   - The `daemon` subcommand group (if daemon is in scope)
5. For each command, lock:
   - Required flags with types, defaults, and descriptions
   - Optional flags with types, defaults, and descriptions
   - Supported output formats
   - Error format (always `structured_stderr`)
6. Lock the invocation hierarchy:
   - Shipped: `<skill-name> ...`
   - Dev: `cargo run -- ...`
   - Release binary: `./target/release/<skill-name> ...`
7. Lock the help behavior:
   - Plain-text: `--help` flag on any command
   - Structured: `help` subcommand with `--format`
8. Lock capability scope — for each of `stream`, `repl`, `daemon`, explicitly
   state `in_scope` or `out_of_scope`.
9. When daemon is in scope, lock the full daemon contract:
   - Managed background mode only
   - Single-instance default
   - Lifecycle commands: start, stop, restart, status
   - Transport modes: stdio, tcp, unix
   - WebSocket framing, TLS support, auth modes
10. Lock runtime directory and Active Context behavior.
11. Generate `.cli-forge/cli-plan.yml` using the format defined in
    [`../contracts/cli-plan.yml.tpl`](../contracts/cli-plan.yml.tpl).
12. Present the CLI plan to the user for approval. Use a dialog-based chooser
    whenever the platform supports it (for example, `request_user_input`) so
    the user can select `approve and continue`, `request changes`, or `stop for
now`. Do not require an exact reply string.

## Outputs

- `.cli-forge/cli-plan.yml` — approved detailed CLI contract

## Exit Gate

| #   | Check                                                         |
| --- | ------------------------------------------------------------- |
| 1   | Command tree is fully defined                                 |
| 2   | Every command has its flags listed with types and defaults    |
| 3   | Output format strategy is locked                              |
| 4   | Help behavior (plain-text and structured) is defined          |
| 5   | Each capability is explicitly marked in_scope or out_of_scope |
| 6   | Daemon contract is locked (if daemon is in_scope)             |
| 7   | Runtime directory and Active Context behavior are defined     |
| 8   | `cli-plan.yml` is generated and approved                      |

## Guardrails

- **CRITICAL DIRECTIVE TO THE ASSISTANT**: You MUST STOP execution and ask for the user's explicit approval after generating `cli-plan.yml`. Do NOT proceed to the Scaffold stage autonomously. Use a dialog-based approval prompt whenever supported, and never require the user to type the literal word `approved`.
- Do not change the skill's purpose or positioning here. That work was done in
  the Design stage and is locked in `design-contract.yml`.
- Do not begin implementing code. This stage produces a plan document, not
  source files.
- Every decision in `cli-plan.yml` must be traceable to the planning brief
  constraints.
- If a capability is out of scope, say so explicitly. Do not leave it
  undefined.
- When the Extend stage later adds a feature, it must update `cli-plan.yml` to
  reflect the new capability. Plan is the living contract.

## Next Step

Continue with
[`../cli-forge-scaffold/SKILL.md`](../cli-forge-scaffold/SKILL.md) to create
the project from the approved plan.
