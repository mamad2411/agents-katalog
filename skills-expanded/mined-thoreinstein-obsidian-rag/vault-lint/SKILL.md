---
name: vault-lint
description: >-
  Use when the user wants a health audit of the vault — stale content,
  provenance drift, frontmatter compliance, or MOC coverage gaps. Triggers
  on "lint vault", "vault health", "check vault", "stale notes", "vault
  audit", "vault quality", or "check conventions".
---

# Vault Lint

Comprehensive vault health audit. Checks five dimensions and presents a prioritized report with fix options.

## Checks

### 1. Frontmatter Compliance

Scan `Engineering/` notes for missing required frontmatter fields per VAULT_CONVENTIONS:

1. Call `obsidian_list_notes` with `subfolder: "Engineering"`.
2. For each note, call `obsidian_read_note` and check frontmatter for:
   - `type:` — must be pattern, trap, decision, or concept
   - `project:` — must be present
   - `status:` — must be present
   - `tags:` — must be a list
   - `created:` — must be a date
3. Report notes with missing or malformed fields.
4. Offer to fix with `obsidian_update_frontmatter` (one at a time, user confirms).

### 2. Provenance Drift

Find Engineering/ notes where the `provenance:` block suggests high uncertainty:

1. From the notes already read in Check 1, filter those with `provenance:` frontmatter.
2. Flag notes where `inferred` > 0.5 — these are majority-synthesized and may need source verification.
3. Flag notes where `ambiguous` > 0.1 — these have unresolved contradictions.
4. Report flagged notes with their provenance fractions.

### 3. Stale Content

If `.manifest.json` exists at vault root:

1. Read it with the `Read` tool.
2. For each entry in `sources`, check if `pages_created` or `pages_updated` notes still exist using `obsidian_read_note`.
3. If a source file's modification time on disk is newer than `ingested_at`, the derived notes may be stale.
4. Report stale notes and suggest re-ingesting with `/wiki-ingest --force <source>`.

If no `.manifest.json` exists, skip this check and note that no ingest tracking is available.

### 4. MOC Coverage

Check whether recent Engineering/ notes appear in at least one thematic MOC:

1. Call `obsidian_list_notes` with `subfolder: "MOCs"`.
2. For each MOC, call `obsidian_read_note` and extract all `[[wikilinks]]`.
3. Build a set of all notes referenced by at least one MOC.
4. Compare against the Engineering/ note list — any note not in the MOC set is uncovered.
5. Exclude notes created in the last 24 hours (grace period).
6. Report uncovered notes and suggest which MOC(s) they belong in via `obsidian_rag_query` (query the note title against MOC titles).

### 5. Orphan Check

Defer to the existing `link-audit` skill (Phase 2). Mention this in the report:
> "For orphan detection, run `/link-audit`."

## Report Format

Present findings as a prioritized summary:

```
## Vault Health Report

### Critical (fix now)
- 3 Engineering/ notes missing `type:` frontmatter
- 1 note with ambiguous provenance > 0.1

### Warning (review soon)
- 5 notes with inferred provenance > 0.5
- 2 notes with stale source material

### Info
- 8 Engineering/ notes not in any MOC
- Run `/link-audit` for orphan detection

### Stats
- Total Engineering/ notes scanned: N
- Frontmatter compliant: N/N (X%)
- Provenance tracked: N/N (X%)
- MOC coverage: N/N (X%)
```

## Arguments

- Optional scope: `/vault-lint Engineering/Patterns/`
- Optional check: `/vault-lint --check frontmatter` (run only one check)

## Tips

- Run after a batch `/wiki-ingest` to catch compliance issues early
- High `inferred` fractions aren't inherently bad — they just need periodic human review
- For large vaults, scope to a subfolder first to keep the audit manageable
- Pair with `/cross-linker` after fixing MOC coverage gaps
