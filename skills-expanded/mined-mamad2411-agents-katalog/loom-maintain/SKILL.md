---
name: loom-maintain
description: Validate, migrate, discover connections, generate evolution summaries, and rebuild indexes for a Loom vault. Use when the user asks to check vault health, migrate a legacy vault, find cross-topic connections, generate evolution reports, or rebuild indexes.
---

# Loom Maintain

Vault governance: validate → migrate → connect → evolve → index.

## Read First

- `../shared/references/schemas.md`
- `<vault-root>/.loom/config.yaml` if it exists (vault configuration)

## Validate

Run read-only vault health check.

```bash
python3 ../shared/scripts/scan_vault.py <vault-root>
python3 ../shared/scripts/validate_vault.py <vault-root>
```

Output: validation report with blocking errors and migration warnings.

Rules:
- Never write files.
- Separate blocking errors from legacy-compatibility warnings.
- Treat legacy warnings as migration candidates, not failures.

## Migrate

Scan and migrate a legacy Markdown vault into the Loom schema.

### Migration workflow

1. Scan vault to inventory: directory presence, note counts by year/status, missing frontmatter, status values, link-only topics, broken links, index existence.
2. Propose staged plan:
   - Initialize indexes without modifying notes.
   - Add missing frontmatter to high-confidence files.
   - Normalize status values only if requested.
   - Convert selected link-only Topic Notes into synthesis notes.
   - Validate links and index consistency.
3. Apply only when user explicitly requests writes.

```bash
python3 ../shared/scripts/scan_vault.py <vault-root>
python3 ../shared/scripts/validate_vault.py <vault-root>
python3 ../shared/scripts/build_indexes.py <vault-root>
```

### Migration rules

- Default is read-only. Generate report before changing anything.
- Preserve all content and unknown frontmatter.
- Prefer additive changes.
- Do not move assets unless requested.
- Before writing, summarize: files to create, files to update, fields to add, files left unchanged.

## Connect

Discover and compile structured connections between Topic Notes.

### Connection flow

**Incremental mode (default when new Topics exist):**
- Compare only new/updated Topic Notes against existing Topics.
- Skip pairs already present in CONNECTION_INDEX.
- Full scan only when explicitly requested or when no CONNECTION_INDEX exists.

**Multi-perspective contrast:**
- Bring different topic perspectives into dialogue.
- Identify where topics support, contradict, or extend each other.
- Moderator synthesis of cross-topic relationships.

**Shared generator mapping:**
- Find generators that appear across multiple topics.
- Map which phenomena they explain in each context.

### Output

- New or updated `00_Index/CONNECTION_INDEX.md` entries.

### Connection rules

- Valid types: `迁移`, `混搭`, `反转`.
- Every insight must be concrete and actionable.
- Do not duplicate existing topic pairs in either direction.
- Newest connections first.
- Connect discovers structural links between finalized Topic Notes. It is not a re-analysis of sources — analytical synthesis of raw Source Briefs belongs in loom-research's Synthesis Pack, not here.

## Evolve

Generate evolution summaries from existing indexes.

### Input

- `00_Index/TIMELINE_INDEX.md`
- `00_Index/TOPIC_INDEX.md`
- `00_Index/CONNECTION_INDEX.md`
- Full Topic Notes only when needed for depth.

### Output

- Monthly: `03_Content_Output/Longform/Evolution_YYYY-MM.md`
- Quarterly: `03_Content_Output/Longform/Evolution_YYYY-QN.md`
- Annual: `03_Content_Output/Longform/Evolution_YYYY.md`

### Evolution structure

1. 本期新增主题 — new topics with category, core idea, why it matters.
2. 本期关键发现 — 3-8 cross-topic findings prioritized over single-topic facts.
3. 知识演进趋势 — growth areas, theme changes, exits/archives, overall direction.
4. 跨领域连接发现 — from CONNECTION_INDEX filtered by period; cumulative statistics.
5. 附录数据 — quantitative metrics.

### Token efficiency

- Monthly: read TIMELINE_INDEX (target month) + TOPIC_INDEX + Topic Notes listed as new/updated.
- Quarterly: read 3 monthly TIMELINE sections; prefer existing monthly summaries.
- Annual: read quarterly summaries; only read full Topic Notes for most impactful topics.
- Filter CONNECTION_INDEX by period. Do NOT re-run connection analysis.

### Evolution rules

- Do not re-run connection discovery. Use existing CONNECTION_INDEX entries.
- For quarterly/annual, prefer existing lower-period summaries when available.

## Index Rebuild

Rebuild deterministic vault indexes.

```bash
# Dry run
python3 ../shared/scripts/build_indexes.py <vault-root>

# Write
python3 ../shared/scripts/build_indexes.py <vault-root> --write
```

Rules:
- Match topics by exact title, preserve existing row order.
- Do not generate new knowledge insights during indexing.
- Prefer dry-run before writing.
