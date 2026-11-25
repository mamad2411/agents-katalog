---
name: are-generate
description: Generate AI-friendly documentation for the entire codebase
disable-model-invocation: true
---

Generate comprehensive documentation for this codebase using agents-reverse-engineer.

<execution>
Run the generate command in the background and monitor progress in real time.

## Steps

1. **Read version**: Read `.claude/ARE-VERSION` → store as `$VERSION`. Show the user: `agents-reverse-engineer v$VERSION`

2. **Run the generate command in the background** using `run_in_background: true`:
   ```bash
   npx agents-reverse-engineer@$VERSION generate --backend claude $ARGUMENTS
   ```

3. **Monitor progress** by polling the latest progress log:
   - Wait ~15 seconds (use `sleep 15` in Bash), then use **Glob** to find the latest `.agents-reverse-engineer/progress-*.log` file, and **Read** it (use the `offset` parameter to read only the last ~20 lines for long files)
   - Show the user a brief progress update (e.g. "32/96 files analyzed, ~12m remaining")
   - Check whether the background task has completed using `TaskOutput` with `block: false`
   - Repeat until the background task finishes
   - **Important**: Keep polling even if no progress log exists yet (the command takes a few seconds to start writing)

4. **On completion**, read the full background task output and summarize:
   - Number of files analyzed and any failures
   - Number of directories documented
   - Any inconsistency warnings from the quality report

This executes a two-phase pipeline:

1. **File Analysis** (concurrent): Discovers files, applies filters, then analyzes each source file via AI and writes `.sum` summary files with YAML frontmatter (`content_hash`, `file_type`, `purpose`, `public_interface`, `dependencies`, `patterns`).

2. **Directory Aggregation** (sequential): Generates `AGENTS.md` per directory in post-order traversal (deepest first, so child summaries feed into parents), and writes `CLAUDE.md` pointers.

**Options:**
- `--dry-run`: Preview the plan without making AI calls
- `--eval`: Namespace output by backend.model for side-by-side comparison (e.g., `file.ts.claude.haiku.sum`, `AGENTS.claude.haiku.md`)
- `--concurrency N`: Control number of parallel AI calls (default: auto)
- `--fail-fast`: Stop on first file analysis failure
- `--debug`: Show AI prompts and backend details
- `--trace`: Enable concurrency tracing to `.agents-reverse-engineer/traces/`
</execution>
