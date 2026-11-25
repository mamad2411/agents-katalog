---
name: code-intelligence-doctor
description: Check whether global code intelligence tools are installed and configured consistently.
execution_mode: command
command: ./scripts/doctor.sh
runtime: shell
safe_to_retry: true
writes_files: false
produces_json: false
supported_agents:
  - codex
  - claude
---

# Code Intelligence Doctor

Use this skill when a repo's code intelligence tools feel unavailable, slow, or inconsistent.

## What it does

The doctor checks:

- `plugin-kit-ai`
- `uv` and `uvx`
- installed `semble==0.2.0`
- installed `codegraphcontext==0.4.11`
- optional installed `serena-agent==1.5.1`
- CGC config hints, including whether SCIP appears enabled

## When to use

- before relying on the global plugin in a fresh machine/session
- after updating `plugin-kit-ai`, Serena, Semble, or CGC
- when an agent claims a code intelligence tool is missing

## How to run

```bash
./plugin/skills/code-intelligence-doctor/scripts/doctor.sh
```

From a generated/copied skill directory, run:

```bash
./scripts/doctor.sh
```

## Constraints

The doctor is read-only. It does not install packages, index repositories, or edit config.
