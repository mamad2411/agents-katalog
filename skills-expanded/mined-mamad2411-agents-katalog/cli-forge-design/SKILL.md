---
name: cli-forge-design
description: "Design stage for the cli-forge skill family: define or refresh the generated skill's high-level identity, purpose, positioning, and description contract before downstream stages proceed."
---

# cli-forge Design

Use this stage when the workflow needs one authoritative description contract
for a generated Rust CLI Skill before later stages proceed.

## Purpose

Define the skill's high-level identity: what it is, who it serves, and how it
is positioned. Produce a single approved description contract that all
downstream surfaces must reuse instead of inventing competing wording.

This stage answers the question **"What is this skill?"** The detailed CLI
contract (commands, flags, formats) belongs to the Plan stage downstream.

## Canonical References

- [`./instructions/design-contract.md`](./instructions/design-contract.md)
- [`./planning-brief.md`](./planning-brief.md)
- [`./contracts/design-contract.yml.tpl`](./contracts/design-contract.yml.tpl)

## Entry Gate

| #   | Check                                              | Source                  |
| --- | -------------------------------------------------- | ----------------------- |
| 1   | `handoff.yml` exists with `classification: design` | Router                  |
| 2   | Skill scope is at least partially known            | User request or handoff |

## Required Inputs

- Classified workflow intent from the Router
- Current or proposed skill scope
- Any existing description surfaces that must stay aligned
- Whether this is a new skill or a refresh of an existing contract

## Workflow

1. Confirm whether the work creates a new skill or changes the user-facing
   contract of an existing one.
2. Read [`./planning-brief.md`](./planning-brief.md) to load the shared
   constraints.
3. Define or refresh the approved purpose summary (one line).
4. Define or refresh the positioning statement (one paragraph).
5. Record which downstream surfaces must stay synchronized:
   - `Cargo.toml` package.description
   - `SKILL.md` purpose section
   - `README.md` header and description
   - Help text summary line
   - Release notes summary (when publish is in scope)
   - npm package description (when distribute is in scope)
6. Record the publish-channel preference (repo-native only, or repo-native
   plus optional npm).
7. Generate `.cli-forge/design-contract.yml` using the format defined in
   [`./contracts/design-contract.yml.tpl`](./contracts/design-contract.yml.tpl).
8. Request user approval of the design contract before moving forward. Use a
   dialog-based chooser (for example, `request_user_input`) so the user can
   select `approve and continue`, `request changes`, or `stop for now`. Do not
   require an exact reply string, and do not ask for numbered or manually typed
   menu responses.

## Outputs

- `.cli-forge/design-contract.yml` — approved description contract

## Exit Gate

| #   | Check                                           |
| --- | ----------------------------------------------- |
| 1   | Single-line purpose summary is approved         |
| 2   | Positioning statement is approved               |
| 3   | Sync surfaces list is complete                  |
| 4   | Publish-channel preference is recorded          |
| 5   | `design-contract.yml` is generated and approved |

## Guardrails

- **CRITICAL DIRECTIVE TO THE ASSISTANT**: You MUST STOP execution and ask for the user's explicit approval after generating `design-contract.yml`. Do NOT proceed to the Plan or Scaffold stage autonomously. Use a dialog-based approval prompt, and never replace it with free-form or numbered text input.
- This stage is the authoritative source for user-facing purpose and
  positioning. Downstream stages consume the approved contract; they do not
  redefine it.
- Do not define CLI commands, flags, or output formats here. That work belongs
  to the Plan stage.
- When publish support is later adopted, all release-facing wording must reuse
  the approved summary.
- If optional npm distribution is later adopted, its package descriptions must
  reuse the same approved contract without presenting npm as the default
  release channel.

## Next Step

Continue with [`../cli-forge-plan/SKILL.md`](../cli-forge-plan/SKILL.md) to
define the detailed CLI contract.
