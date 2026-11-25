---
name: compost
description: Run long or repetitive commands (builds, pytest/ctest, SLURM jobs, solver logs) through a clustering summarizer instead of reading raw output; re-runs show only what changed. Use for output likely over ~100 lines or fix-test-fix loops.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/bin/compost *), Bash("${CLAUDE_SKILL_DIR}/bin/compost" *)
---

# compost

!`"${CLAUDE_SKILL_DIR}/bin/compost" mode --banner`

Agents that do not expand the line above (e.g. Codex): run
`<this-skill-dir>/bin/compost mode --banner` first and follow it.

Offline, deterministic: output is parsed and clustered by script (no LLM);
the full raw output is always kept on disk. Skip it for short output --
just read that directly.

`compost` is not on PATH: always use the full `<this-skill-dir>/bin/compost`
path (or `python3 <this-skill-dir>/scripts/compost.py` if executables are
not permitted).

1. Run: `<this-skill-dir>/bin/compost run -- <command...>`
   (pipes/redirects need `bash -c '...'`). Prints the root error (first
   error in user code), secondary failure groups with counts, warnings,
   numerical summary, and a `raw_output_id`.
2. Read the summary, not the raw log.
3. Re-run the same command the same way: only new/resolved errors and
   count deltas are printed ("No structural changes." if none).
4. Only if the summary is insufficient, use the printed
   `retrieval_handles` (`get <id> --lines A:B`, `event <id> --event N`,
   `grep <id> '<pattern>'`, `show <id> --json`). They never re-run the
   command; they read the already-stored raw output.
5. Existing log file: `bin/compost ingest --file <path>` (or `--stdin`).
6. The plugin's Bash hook may deny a raw build/test command and name the
   compost command to run instead: run that. Need raw output (e.g. to show
   the user)? Append `# raw` to the command.

Profiles (auto-detected, `--profile` to override): pytest, ctest, gcc/clang,
cmake, python_traceback, slurm, numerical_solver, generic.

Output fields, statuses, storage and retention: `references/schema.md`.
Per-profile detection: `references/profiles.md`.
