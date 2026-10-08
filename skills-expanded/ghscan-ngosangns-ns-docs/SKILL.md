---
name: mdvdb-vault-health
description: >
  Run diagnostic health checks on an mdvdb Collection: doctor checks
  (including relation and Shard configuration integrity), Formula/Lookup/Rollup
  module diagnostics, missing Shard/sub-collection folders, orphan detection,
  and schema analysis. Use when the user reports issues, stale or missing
  computed values, or wants to audit their knowledge base.
---

# Vault Health Check

Comprehensive diagnostics for the markdown vault.
Only works with `.md` files indexed by mdvdb.

## Steps

1. Detect available built-in modules first:

   ```
   mdvdb modules list --json
   ```

   Then run these commands in parallel:

   ```
   mdvdb doctor --json
   mdvdb orphans --json
   mdvdb schema --json
   mdvdb status --json
   mdvdb config --json
   mdvdb shards list --json
   mdvdb modules status formula --json
   mdvdb modules status lookup_rollup --json
   ```

   Run the `lookup_rollup` status command only when `modules list` advertises
   that descriptor; older CLIs can render existing materialized fields but
   cannot execute or diagnose this module.
   (`config` shows the fully resolved configuration — provider, model,
   clustering, chunking — after merging shell env, project YAML, `.env`
   secrets, and user YAML; use it to see current values before suggesting
   `config set` fixes.)

2. Present a health report:

   **Doctor Checks** (from Collection-wide `doctor`; it has no `--shard`):
   - Config loads (`.markdownvdb/config.yaml` — YAML; legacy dotenv configs
     auto-migrate on first load)
   - Embedding provider reachable, index integrity, file discovery
   - **Relations check**: dangling relation targets (frontmatter links to
     files that don't exist, shown as `source#field → target`), overlay
     `target:` folders matching no files, and unquoted `[[x]]` frontmatter
     values (the YAML nested-array footgun)
   - **Shards check**: malformed project-local definitions, missing folders,
     or malformed local Topics. Unrelated Collection commands remain usable
     when one Shard's local Topics are malformed.
   - List any failing checks with error messages

   **Shard definitions** (from `shards list`):
   - Report `exists: false` separately from malformed configuration. Missing
     folders are retained intentionally so external renames can be repaired.
   - Validate inferred nesting and segment boundaries; `docs` must not become
     the parent of `docs-old`.

   **Orphan Files** (from `orphans`):
   - Files with zero incoming or outgoing links (frontmatter relations count
     as links)
   - Orphan count vs. total file count (percentage)

   **Schema Analysis** (from `schema`):
   - Metadata fields found across the vault, with types and coverage
   - `Relation` fields (link-shaped values) and their `relation_target` folder
     if declared in the `.markdownvdb.schema.yml` overlay
   - `File` fields (mdvdb ≥ 0.2.0) and whether values consistently use quoted,
     root-relative arrays; `relation_target` must remain null
   - `Lookup`/`Rollup` fields and their `relation_field`, exact top-level
     `target_field`, effective `relation_direction`, and any incoming
     `relation_scope` source folder; Rollup also declares `formula` and
     `result_type`
   - Inconsistencies (e.g., a field that varies in type across files —
     `Mixed` type)

   **Computed Fields** (from both module-status commands):
   - Group diagnostics by module, path, and output field. Broken Relations,
     missing target keys, result-type errors, dependency cycles/failures, and
     refused source/dependency races are data-integrity findings, not values
     to estimate or silently omit.
   - Successful materialized frontmatter is authoritative. Never use an old
     disk value when `computed_field_errors` reports that field.

3. Provide a health summary:
   - **Healthy**: all checks pass, low orphan rate, consistent schema
   - **Warning**: minor issues (some orphans, dangling relations, optional
     checks failing)
   - **Critical**: provider unreachable, index corrupt, many errors

4. For each issue found, suggest a specific fix:
   - Unquoted wiki-link → replace it with the preferred plain path,
     `client: clients/acme.md`; quoting the existing wiki link also remains valid
   - Dangling relation → fix the path or create the target file, then
     `mdvdb ingest --file <path>` (see the manage-relations skill)
   - Broken File reference → correct the root-relative path or unlink it;
     unlinking must not delete the physical file
   - Lookup/Rollup failure → repair its Relation, target field, source-folder
     membership, formula, or dependency, then run
     `mdvdb modules run lookup_rollup --json`; never hand-write the output
   - Config problems → adjust via `mdvdb config set <dotted.key> <value>`
   - Missing Shard after one rename → `mdvdb shards update <id> --path <path>`
   - Renamed prefix with nested Shards → `mdvdb shards retarget <old> <new>`

Do not suggest `ingest` to repair a Shard definition. Shard management is raw
project-config work and never changes the shared index. After repairing a
definition for a folder that physically moved, the watcher or a subsequent
Collection-wide ingest must still refresh the indexed document paths. Use
manage-shards for the safe sequence.
