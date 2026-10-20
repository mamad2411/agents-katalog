# Cline Rules (minimal)

Cline (v3.37.0+) reads `AGENTS.md` automatically.
Treat `AGENTS.md` as canonical project instructions.

## Preferences
- Prefer CLI-first workflow (`camofox ...`) for automation tasks.
- Use `--format json` when output is consumed by tools/agents.
- Follow snapshot-first interaction: snapshot -> refs -> action -> snapshot.
- Use element refs (`eN`) before CSS selectors.
- Always keep operations scoped by `userId` / `--user`.
- Use search macros instead of building ad-hoc search URLs.
- Use auth vault commands for credentials; do not expose secrets in output.
- Preserve compatibility routes/commands when modifying behavior.

## Practical hints
- For UI actions, collect fresh refs after each significant page change.
- For scripts, prefer `camofox run <file>` over ad-hoc shell loops.
- For endpoint details and edge cases, defer to `AGENTS.md`.
