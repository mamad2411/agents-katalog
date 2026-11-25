---
name: read-only-shell-guard
description: Use when deciding whether shell commands are truly read-only, safe for concurrent execution, and free of path, git, redirection, or command-shape risks that should force a stricter permission path
---

# Read Only Shell Guard

## Overview

Not every harmless-looking command is actually read-only. This skill follows the guardrails in `src/tools/BashTool/readOnlyValidation.ts` and related shell validation utilities.

## Read-Only Means

A read-only command may inspect state, but it must not:

- modify files
- create files
- redirect output into files
- invoke write-capable git flows
- change system state

## Safe Categories

Usually safe when validated:

- `rg`, `grep`, `find`, `cat`, `head`, `tail`, `wc`, `stat`
- read-only `git` queries
- read-only `gh` queries
- filtered inspection commands with safe flags

## Automatic Red Flags

Treat the command as non-read-only when you see:

- output redirection
- file creation or mutation
- mixed `cd` and `git` compound commands in sandboxed contexts
- git operations outside the original cwd when sandbox rules depend on cwd
- writes into git-internal paths
- UNC path or traversal risk
- shell parse failure

## Compound Command Rule

The whole command is only read-only if every subcommand is read-only.

One unsafe segment makes the batch unsafe.

## Validation Rule

Do not trust the command's story. Validate:

- parseability
- flags
- path handling
- cwd sensitivity
- git-specific escape conditions

If validation fails or is ambiguous, escalate to stricter permission handling.

## Concurrency Rule

Read-only work may be run concurrently. Mixed or write-capable work must not inherit that privilege just because part of it looks harmless.

## Anti-Patterns

- assuming `git` is always read-only
- treating a shell parse failure as probably safe
- allowing redirection because the main command is read-only
- classifying a compound command by its first segment only

## Done Condition

You have applied this skill correctly when only truly read-only commands get the fast path, and ambiguous or risky command shapes are forced into the stricter permission path.
