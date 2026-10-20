## Agent skills

### Running tests

Main agent delegates test runs to the `test-runner` subagent; Use either of these:

- `pnpm run tdd` for inner RED→GREEN cycle
- `pnpm run e2e` for final check before closing

### Issue tracker

GitHub Issues on `WilliamChelman/sparqly` via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Agent exploration

Exploring the code base, use the `explorer` subagent for ≥400-line files or for broad spectrum searches.

## Issues reading

Reading issues linked to the current issue being worked on, use the `explorer` subagent to read it to extract relevant information.
