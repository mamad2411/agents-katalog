# Project Instructions

This project uses the Ralph Wiggum loop for iterative AI-driven development.

## Important Rules
- Do NOT commit code — ralph.sh handles all git operations
- Do NOT modify state/prd.json — ralph.sh manages task status
- Do NOT work on more than one story per session
- Always run verification steps before finishing
- Append learnings to state/progress.txt before exiting

## Project Structure
- `specs/` — Topic-of-concern specification files
- `state/prd.json` — Task tracking (read-only for agents)
- `state/progress.txt` — Append-only iteration log (your external memory)
- `AGENTS.md` — Codebase patterns and conventions (update as you discover them)

## Testing
Run all quality checks before considering work done. Read error output carefully — it tells you exactly what to fix.
