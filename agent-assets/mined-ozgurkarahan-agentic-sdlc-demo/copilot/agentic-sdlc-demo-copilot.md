# Copilot Instructions

Read these files for full context:

- `AGENT.md` — project overview, architecture, environment vars, workflow rules, platform notes, and references (start here)
- `.github/instructions/end-session.instructions.md` — the end-session workflow

## Copilot-Specific Tips

- Use `@workspace` to give Copilot full project context.
- Pin `AGENT.md` in chat for persistent context.
- Use Copilot Edits (Ctrl+Shift+I) for multi-file changes.
- Run tests manually — Copilot CLI cannot execute long-running tests in your IDE flow.
- When corrected, capture the lesson in your team wiki (not in a project-local `.ai/` folder).

## End-Session Workflow

See `.github/instructions/end-session.instructions.md` for the project-specific shim. Summary:

1. Project docs sweep (AGENT.md, .claude/CLAUDE.md Project Context block)
2. Wiki compounding (graduate durable findings via [[ingest]] workflow)
3. Git status check
4. Smoke check (run `AGENT.md` § How to Verify checks)
5. Summary report

## Shared knowledge base (memory wiki)

A compounding cross-project knowledge base lives at `~/projects/memory`
(`%USERPROFILE%\projects\memory` on Windows; resolve `~` to your home dir).
**Consult it reflexively before answering about clients, domains, patterns,
tools, colleagues, or past work** — do not answer from memory when the wiki
has the answer.

```bash
# from ANY repo — resolves the wiki root from the script's own location
python ~/projects/memory/scripts/wiki-search.py <terms>          # ranked hits
python ~/projects/memory/scripts/wiki-search.py <terms> --full   # + Summary
```

- Read the top matching page(s) in full before you answer.
- Compact catalog / router: `~/projects/memory/index.md` (per-category summaries
  in `~/projects/memory/wiki/{category}/_index.md`).
- When you learn something durable about this project or client, ask the user to
  run `ingest` in the memory repo so it compounds for future sessions.
