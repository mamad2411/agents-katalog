# Project Status

Show a quick status report for the cowork-mcp project.

## What To Do

Run these in parallel:

1. **List active plans** — Read each `plan.md` in `agent-projects/` subdirectories and extract frontmatter (`status`, `owner`, `created`, `summary`). Skip `agent-projects/README.md`.

2. **Read project facts** — Read `docs/facts.json`

3. **List recent ADRs** — List files in `docs/decisions/` (if the directory exists) and read the most recent 3 by filename order

4. **Check open issues** (best-effort):
   ```bash
   gh issue list --state open 2>/dev/null | head -20
   ```

## Report Format

Display a concise status report:

### Project Overview
- Project name and description (from facts.json)
- Python version, key dependencies

### Active Plans
For each plan with `status: in-progress`:
- Plan name (directory)
- Summary (from frontmatter)
- Created date

### Completed Plans
For each plan with `status: complete`:
- Plan name and completion date (one line each)

### Pending Plans
For each plan with `status: pending` or `status: draft`:
- Plan name and summary

### Recent Decisions
List the most recent ADRs from `docs/decisions/` (read titles directly from files)

### Open Issues
List any open GitHub issues (if gh CLI available)

### Next Steps
Based on in-progress and pending plans, recommend what to work on next.
