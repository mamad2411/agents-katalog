---
name: rta-smriti-brain
description: Use Rta-Smriti Brain before project work to retrieve local repo memory, context packs, graph facts, and stale-file status.
---

# Rta-Smriti Brain

Use this skill when working in a project that has a Rta-Smriti SQLite brain or when the user asks for durable local project memory.

## First Command

Verify the brain:

```powershell
rta-brain.cmd doctor --json --db <brain.sqlite>
```

If `rta-brain.cmd` is not on PATH, run it by absolute path from the Rta-Smriti deliverable folder.

## Install For Reuse

To make wrappers available from any project:

```powershell
rta-brain.cmd install-local --target "$env:USERPROFILE\.local\bin" --json
```

Add that target folder to PATH if needed.

## Bootstrap A Project

Create one brain per project. Use the exact `rta-brain` wrapper path returned by
`install-local`; Windows wrappers end in `.cmd`, while macOS and Linux wrappers
have no suffix. The examples below assume the wrapper directory is on `PATH`.

Windows PowerShell:

```powershell
rta-brain.cmd bootstrap-project <repo-path> --project <project-name> --brain-dir "$env:USERPROFILE\Documents\Rta-Smriti\brains" --write-agents --json
```

Then verify readiness:

```powershell
rta-brain.cmd --db "$env:USERPROFILE\Documents\Rta-Smriti\brains\<project-name>.sqlite" self-check --project <project-name> --json
```

macOS or Linux:

```bash
rta-brain bootstrap-project <repo-path> --project <project-name> --brain-dir "$HOME/.local/share/rta-smriti/brains" --write-agents --json
rta-brain --db "$HOME/.local/share/rta-smriti/brains/<project-name>.sqlite" self-check --project <project-name> --json
```

## MCP Server

If the host supports MCP, generate a native configuration from the CLI:

```powershell
rta-brain.cmd --db <brain.sqlite> --json mcp-config --project <project-name> --name rta-smriti
```

```bash
rta-brain --db <brain.sqlite> --json mcp-config --project <project-name> --name rta-smriti
```

Available MCP tools:

- `brain_search`
- `brain_context_pack`
- `brain_remember`
- `brain_ingest_repo`
- `brain_ingest_thread`
- `brain_repo_map`
- `brain_stale_check`
- `brain_checkpoint`
- `brain_continuation_prompt`
- `brain_reflect`
- `brain_doctor`

## Before Coding

Generate a context pack:

```powershell
rta-brain.cmd context-pack "<task>" --project <project-name> --db <brain.sqlite>
```

Verify the canonical root and Git identity at the top of the pack. Read the freshness line; if it says stale, re-read changed or missing files before relying on memory-derived context.

## Search

```powershell
rta-brain.cmd search "<query>" --project <project-name> --json --db <brain.sqlite>
```

Prefer exact project-scoped searches. Use results as pointers to evidence, not as a replacement for current file reads.

## Remember

Use one atomic memory per command:

```powershell
rta-brain.cmd remember "<durable fact>" --type decision --pramana sabda --project <project-name> --priority 8 --db <brain.sqlite>
```

For a verified claim, attach `--source-path`, `--source-hash`, `--verification-command`, and `--verification-status verified`.

Pramana policy:

- `pratyaksha`: directly observed from file, test, tool, or command output.
- `sabda`: user instruction or trusted documentation.
- `anumana`: inference.
- `smriti`: prior memory.
- `kalpana`: hypothesis or creative possibility.

## Repo Refresh

```powershell
rta-brain.cmd ingest-repo <repo-path> --project <project-name> --db <brain.sqlite>
```

Run after meaningful code or documentation changes.

## Thread Ingestion

When a long thread, rollout summary, handoff, or JSONL session contains useful context:

```powershell
rta-brain.cmd ingest-thread <thread-or-handoff-path> --project <project-name> --title "<short title>" --db <brain.sqlite>
```

Then run reflection:

```powershell
rta-brain.cmd reflect --project <project-name> --json --db <brain.sqlite>
```

## End A Work Session

Save a structured checkpoint before handing work to another task or agent:

```powershell
rta-brain.cmd checkpoint --project <project-name> --db <brain.sqlite> --objective "<objective>" --verified-evidence "<verified evidence>" --remaining-gaps "<remaining gaps>" --next-action "<next action>" --prohibited-repetition "<do not repeat>"
```

Use `continue-prompt` or the dashboard's **Copy New Task Prompt** action for the next task.

## Do Not

- Do not store secrets or credentials.
- Do not use stale memory as current truth.
- Do not mix unrelated projects into one brain unless explicitly authorized.
- Do not store broad transcripts when one durable fact is enough.
