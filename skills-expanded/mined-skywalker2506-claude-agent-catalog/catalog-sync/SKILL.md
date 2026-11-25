# /catalog-sync

Sync agent counts across ecosystem READMEs. Wrapper around `hq sync` for use within the catalog project.

## Trigger

```
/catalog-sync [--dry-run]
```

## What it does

1. Counts agents in `agent-registry.json`
2. Updates README.md badge: `registry-<N>_agents`
3. Delegates full ecosystem sync to `ClaudeHQ/scripts/hq sync`

## When to use

- After adding or removing an agent from the registry
- After a PR merges that changes agent count
- As part of the release checklist

## Output

```
Catalog Sync — 2026-04-22
Registry agents: 134
README badge before: 196_agents
README badge after: 134_agents (updated)
→ Run 'hq sync' from ClaudeHQ for full ecosystem update
```

## See also

- `docs/ecosystem-sync.md` — full sync documentation
- `scripts/validate_registry.py` — validate registry before syncing
