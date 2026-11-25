---
name: notebooklm
description: Use this skill when the user wants to work with Google NotebookLM from Codex through the `notebooklm-py` CLI, including logging in, listing notebooks, selecting a notebook, adding sources, asking questions, exporting metadata, or generating NotebookLM artifacts.
---

# NotebookLM

Use this skill to operate NotebookLM from Codex through a local wrapper script that runs:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh ...
```

The wrapper uses `uvx --from notebooklm-py notebooklm ...` so it does not depend on the system `python3` version.

## Workflow

1. Check current auth/context first:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh status
```

2. If the user is not authenticated yet, start login:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh login
```

3. For notebook-specific work, pick or confirm the active notebook:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh list
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh use <notebook-id-or-prefix>
```

4. Then run the requested action directly through the wrapper.

## Common Commands

List notebooks:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh list
```

Create a notebook:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh create "My Notebook"
```

Ask the current notebook a question:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh ask "Summarize the main findings."
```

List sources in the current notebook:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh source list
```

Add a local file as a source:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh source add "/absolute/path/to/file.pdf"
```

Export notebook metadata:

```bash
/Users/rr/.codex/skills/notebooklm/scripts/notebooklm.sh metadata
```

## Notes

- The default NotebookLM session storage path is `~/.notebooklm/storage_state.json`.
- The wrapper honors `NOTEBOOKLM_STORAGE_PATH` if a custom storage file is needed.
- When a command fails, surface the CLI error clearly instead of guessing.
- If NotebookLM requires interactive browser authentication, let the login flow complete before proceeding.
