---
name: repo-sync-enforcer
description: Prevents drift in schemas, schema-paths.json, OpenAPI, and docs across BWMACRO, RiskModels_API, and Risk_Models. Activates on schema/JSON/OpenAPI/doc changes.
---

# Repo Sync Enforcer

When editing schemas, OpenAPI specs, MCP data, or tracking docs across the RiskModels repos, follow this workflow to prevent drift.

## Step 1: Identify Canonical Repo

| Asset | Canonical Repo | Path |
|-------|----------------|------|
| JSON schemas | RiskModels_API | `mcp/data/schemas/*.json` |
| schema-paths.json | RiskModels_API (edit first) | `mcp/data/schema-paths.json` |
| capabilities.json | RiskModels_API | `mcp/data/capabilities.json` |
| openapi.json (generated) | RiskModels_API | `mcp/data/openapi.json` |
| OPENAPI_SPEC.yaml | RiskModels_API | `OPENAPI_SPEC.yaml` |
| CHANGELOG | RiskModels_API | `CHANGELOG.md` |
| MASTER_BACKLOG.md (engineering OSOT) | BWMACRO | `docs/ceo/MASTER_BACKLOG.md` |
| current_state.md (API narrative) | BWMACRO | `docs/api_roadmap/current_state.md` |

**Path note:** canonical is `RiskModels_API/mcp/` (singular). The portal mirror lives at `Risk_Models/riskmodels_net/mcp-server/` (different subdir name). Don't confuse them — copying into the wrong path creates phantom drift that passes `diff -q` only if both sides have the same subdir name.

## Step 2: New Schema Workflow

1. **Create/edit schema** in `RiskModels_API/mcp/data/schemas/`
2. **Add to schema-paths.json** in RiskModels_API:
   ```json
   "/schemas/NEW_SCHEMA-v1.json"
   ```
3. **Copy schema to Risk_Models** (or merge to RiskModels_API `main` and rely on **Sync MCP data to Risk_Models** in that repo — requires `REPO_ACCESS_TOKEN` with write to Risk_Models; see `docs/AGENTS_CROSS_REPO.md`):
   ```bash
   cp RiskModels_API/mcp/data/schemas/NEW_SCHEMA-v1.json \
      Risk_Models/riskmodels_net/mcp-server/data/schemas/
   ```
4. **Update schema-paths.json** in Risk_Models (same entry)
5. **Add CHANGELOG entry** in RiskModels_API
6. **Update MASTER_BACKLOG.md** (terse burn-down row) and **`current_state.md`** (narrative / tables) in BWMACRO when format, gap, or endpoint surface changes

### Full artifact resync (when portal drift is broader than one schema)

When the portal is behind on multiple artifacts at once, do a full one-directional sync rather than cherry-picking. Copy all four from API canonical → portal mirror, then verify with `cmp`:

```bash
API=/path/to/RiskModels_API/mcp/data
PORTAL=/path/to/Risk_Models/riskmodels_net/mcp-server/data
cp -r "$API/schemas/." "$PORTAL/schemas/"
cp "$API/schema-paths.json" "$PORTAL/schema-paths.json"
cp "$API/capabilities.json" "$PORTAL/capabilities.json"
cp "$API/openapi.json"       "$PORTAL/openapi.json"
diff -q "$API/schemas/" "$PORTAL/schemas/"   # expect no output
cmp "$API/schema-paths.json" "$PORTAL/schema-paths.json" && echo MATCH
cmp "$API/capabilities.json" "$PORTAL/capabilities.json" && echo MATCH
cmp "$API/openapi.json"       "$PORTAL/openapi.json"       && echo MATCH
```

Portal is never canonical — if the portal file is newer than the API's, that's a process violation; push the change to the API side first, then resync down.

## Step 3: OpenAPI Additions (e.g. format=parquet)

1. Edit `RiskModels_API/OPENAPI_SPEC.yaml`
2. Add parameter, response content types, schemas as needed
3. On merge to RiskModels_API **`main`**, workflow **`.github/workflows/sync-mcp-to-risk-models.yml`** runs **`npm run build:openapi`** and pushes **`mcp/data/openapi.json`**, **`schema-paths.json`**, **`schemas/`**, and **`capabilities.json`** to Risk_Models. Requires **`REPO_ACCESS_TOKEN`** (write) on Risk_Models in the API repo secrets. Weekly schedule + `workflow_dispatch` also available.
4. Update **`MASTER_BACKLOG.md`** plus `current_state.md` Response Format / Data Endpoints table in BWMACRO

## Step 4: Sync Checklist (Always Output)

When making cross-repo changes, output this checklist and mark items as you complete them:

```
Sync checklist:
- [ ] RiskModels_API: schema/spec/changelog updated
- [ ] Risk_Models: schema copied, schema-paths.json updated (if schema added)
- [ ] BWMACRO: MASTER_BACKLOG.md + current_state.md updated (if scope/format/gap changed)
- [ ] Manual copy steps executed (schemas, schema-paths.json)
```

## Step 5: Offer Sync Checklist Draft

At the end of your response, offer: "I can draft a sync checklist for the other repos, or a small bash script to automate the copies."

## Pitfall: shared Supabase migration history

All three repos (BWMACRO, RiskModels_API, Risk_Models) push migrations into the **same** Supabase project ("BW Web Data Engine"). There is no dev/prod split. The project's `supabase_migrations.schema_migrations` registry is shared state.

**Symptom:** `supabase db push` from one repo fails with:

```
Remote migration versions not found in local migrations directory.
...try repairing the migration history table:
supabase migration repair --status reverted <versions…>
```

This means another repo has applied migrations that the current repo doesn't have locally. **The CLI's suggested command is wrong** — `--status reverted` tells Supabase "those migrations didn't happen," which would cause them to re-run and potentially conflict.

**Correct recovery options**, from safest to most surgical:

1. **Apply the single needed migration via the Supabase SQL editor.** Paste the idempotent SQL (`CREATE … IF NOT EXISTS`, `ADD COLUMN … IF NOT EXISTS`) directly. Skips the migration registry entirely — acceptable because the other repos are also bypassing it. Lowest blast radius.
2. **Mark the foreign migrations as applied in THIS repo:**
   ```bash
   supabase migration repair --status applied <remote-only-versions…>
   supabase db push
   ```
   This is accurate — those migrations WERE applied. After this, the current repo can `db push` its local-only migrations. Do this when you have multiple local-only migrations to push and want the registry clean.
3. **Pull the remote schema down to catch up:**
   ```bash
   supabase db pull
   ```
   Generates a single catch-up migration that encodes the drift. Messier; risks encoding unintended changes from other repos. Only use when you're actually adopting the canonical state as-is.

**Prevention:** treat all schema changes as production-ish. Either author migrations in a designated repo (BWMACRO recommended since it already pushes other artifacts) and sync down, or coordinate by paste-into-SQL-editor so no repo's migration folder is ever considered authoritative.

## Invocation

Prefix prompts with `@repo-sync-enforcer` when working on schemas, OpenAPI, or docs to invoke this skill. The Cursor rule `.cursor/rules/repo-sync-enforcer.mdc` also applies when editing matching files.
