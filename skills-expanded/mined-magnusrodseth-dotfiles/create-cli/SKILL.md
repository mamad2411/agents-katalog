---
name: create-cli
description: Design and build command-line tools, both the interface spec (args, flags, subcommands, help, output modes, errors, exit codes, config) per clig.dev and the implementation using Magnus's agent-ready Rust house style (clap derive, global --json, keychain/op/file secret backends, in-repo agent skills, AGENTS.md) modeled on sparebank1-cli and skatteetaten-cli. Use when the user wants to create a new CLI, design a CLI interface, scaffold a command-line tool, or make an existing CLI agent-friendly.
---

# Create CLI

Two modes. Pick from what the user asked for:

- **Design**: produce an interface spec the user (or a later session) can
  implement. Language-agnostic.
- **Build**: scaffold and implement, defaulting to the house style (Rust +
  clap) unless the user names another stack.

## Do This First

- Read `references/cli-guidelines.md` (condensed clig.dev; the baseline
  rubric for any CLI).
- Read `references/house-style.md` (Magnus's agent-ready skeleton, with
  `~/dev/personal/sparebank1-cli` and `~/dev/personal/skatteetaten-cli` as
  living exemplars to copy from).

## Clarify (fast, then proceed with defaults)

- Name + one-sentence purpose. Short 2-3 char binary name?
- Primary consumers: humans, scripts, AI agents, or all three. (Default
  here: agents are first-class consumers.)
- Read-only or mutating? Mutating means confirm-prompts, `-y`, and scope
  restrictions from day one. Read-only as a design invariant is worth
  stating explicitly.
- Auth/secrets involved? Which backend story (keychain/op/file)?
- Distribution: personal (`install.sh` + cargo) or public (crates.io,
  release matrix)?

## Design mode: deliverables

Produce a compact spec:

- Command tree + USAGE synopsis (noun-verb grouping; the `--help` tree is
  how agents discover capabilities, so make it a deterministic search tree).
- Args/flags table: types, defaults, required/optional, examples.
- Output contract: stdout vs stderr, `--json` (table stakes for agents),
  TTY detection, `--quiet`/`--verbose`, color rules (`NO_COLOR`).
- Error + exit-code map for the top failure modes, with messages that state
  the fix.
- Safety rules: confirmations, `-y`/`--force`, `--no-input`, dry-run story.
- Config/env precedence: flags > env > project config > user config.
- 5-10 example invocations, including piped/stdin and agent (`--json`) use.

## Build mode: house style

Follow `references/house-style.md`. The short version: clap derive with
global `--json` and `--mask`, stdout-is-data discipline, three-backend
secret store defaulting to keychain, thiserror + anyhow two-layer errors,
confirm-before-mutation, polite API etiquette (honest User-Agent, no retry
loops), co-located tests for pure logic, fmt/clippy/test CI, and the
`install.sh` + tag-driven release pipeline. Copy `secrets.rs`, `install.sh`,
`error.rs`, and the workflows from an exemplar repo and rename.

Every CLI ships its agent surface in the same repo:

- `AGENTS.md` at root with explicit operating rules for agents.
- `skills/<tool>-shared/SKILL.md` as the runtime contract (command map,
  storage table, output contract, etiquette), plus per-area skills when the
  command surface grows.

## Notes

- Full upstream guidelines: https://clig.dev/
- Check current library docs (clap etc.) via find-docs/ctx7 before coding;
  do not trust memorized API details.
- If the request is design-only, do not drift into implementation.
