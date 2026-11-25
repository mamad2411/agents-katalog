---
name: vault-lint
description: >-
  Audits graph health, validates Open Knowledge Format (OKF v0.3/v0.2) frontmatter compliance, detects broken links, finds orphaned notes, repairs escaped table pipes, upgrades vaults to OKF v0.3, and verifies freshness across the central Obsidian Vault ($OBSIDIAN_VAULT_PATH or ~/ObsidianVault). Use when the user invokes /vault-lint or /lint, asks to lint the vault, check vault health, audit the vault, repair vault links, migrate a vault to OKF v0.3, or after major batch ingestions and refactors. Don't use for ingesting new raw documents (use ingest) or launching the interactive 3D WebGL graph server (use vault-graph).
---

# 🧹 Vault Lint & Health-Check Skill (`/vault-lint`)

This skill performs automated graph validation, OKF v0.3/v0.2 frontmatter schema verification, one-command v0.2 -> v0.3 migration, orphan detection, and link health checks across the central **Knowledge Compiler** Obsidian Vault (`$OBSIDIAN_VAULT_PATH`, defaults to `~/ObsidianVault`).

---

## 🚀 Triggers & Commands

- `/vault-lint` or `/lint`
- Natural language triggers:
  - *"Check vault health"*
  - *"Lint the Obsidian vault"*
  - *"Find broken links or orphan notes in the vault"*
  - *"Verify OKF schema compliance"*

---

## ⚡ Execution Workflow

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       VAULT LINT EXECUTION PIPELINE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Step 1: Automated Graph & Schema Scan]                                    │
│  Run vault_lint.py across $OBSIDIAN_VAULT_PATH or ~/ObsidianVault           │
│                                │                                            │
│                                ▼                                            │
│  [Step 2: Diagnostic Evaluation]                                            │
│  Analyze broken links, orphan notes, schema defects & stale_after dates     │
│                                │                                            │
│                                ▼                                            │
│  [Step 3: Automated Remediation]                                            │
│  Auto-repair broken link aliases, index missing notes, fix escaped pipes   │
│                                │                                            │
│                                ▼                                            │
│  [Step 4: Audit Trail Logging]                                              │
│  Append audit summary to ObsidianVault/log.md                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. Run Automated Linter, Strict Mode, Migration & Human Approval
Execute the OKF v0.3/v0.2 vault linter script via `run_command` (OKF v0.3 bundle root `.`, compiled concepts in `wiki/`):
```bash
# Standard health & OKF conformance audit (plus optional upstream spec check)
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" --check-okf-upstream

# Strict CI / conformance mode (fails with exit 1 on stale_notes, orphan_notes, missing_from_index, legacy_sources_notes)
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" --strict --json

# Repair escaped table pipes AND opt-in migrate legacy string sources to OKF {id, resource} objects
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" --fix --migrate-sources

# Upgrade an OKF v0.2 vault to OKF v0.3 (root index.md okf_version: "0.3", frontmatter-free log.md & wiki/**/index.md, leading '/' bundle paths, x-kc-* epistemic keys)
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" --fix --migrate-v03

# Also rewrite resolved Obsidian [[wikilinks]] to portable OKF v0.3 RFC 3986 relative Markdown links and x-kc-* bundle-root paths
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" --fix --migrate-v03 --portable-links

# Stamp explicit human verification onto a reviewed wiki/ note (Trust Tier: human-reviewed)
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" \
  --approve-human wiki/concepts/MyNote.md --actor human:<username>

# Detect synthesis drift & plain-text unlinked mentions (fail strictly on stale_syntheses via --strict-drift)
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" --mentions --strict-drift

# Two-phase deduplication: (1) generate read-only manifest, review & flip "approved": true, (2) apply with SHA-256 CAS
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" --dedup-manifest /tmp/dedup_manifest.json
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}" --apply-manifest /tmp/dedup_manifest.json
```
- Pass `--check-okf-upstream` whenever checking whether a newer version of the official Open Knowledge Format specification has been published at [`github.com/open-knowledge-format/open-knowledge-format`](https://github.com/open-knowledge-format/open-knowledge-format) (`SPEC.md`, currently `v0.3`).

#### Exit Codes
- `0`: Conformant (`is_healthy == True` and zero warnings when `--strict` is active).
- `1`: Conformance errors (`missing_frontmatter`, missing `type`, `<= 16 KiB` or YAML anchor/alias violations, invalid `Attested Computation` or `sources` dict entries), `broken_links`, `table_invariant_violations`, or warnings under `--strict`.
- `2`: Invalid or missing vault path, missing `wiki/` bundle root, or invalid `--approve-human` target (outside `wiki/`, symlink, traversal, `raw/`, or root file).

### 2. Inspect Audit Heuristics & Graph Intelligence
The linter verifies critical health metrics and computes graph structural insights:
1. **Broken Links (`🔗`) & `wanted_pages`**: Unresolved `[[Target]]` wikilinks where the destination markdown file does not exist, aggregated and ranked in `wanted_pages` by inbound reference count (`inbound_count` descending).
2. **Table Pipe Invariants (`⚠️`)**: Verifies no escaped pipe characters exist inside tables (`[[Target|Alias]]` required).
3. **Orphan Notes (`🏝️`)**: Notes with 0 inbound wikilinks from other notes or `index.md`.
4. **Dead-End Notes (`🛑`)**: Notes with 0 outbound links.
5. **Freshness & Stale Claims (`⏳`)**: Flags any notes in `stale_notes` where `current_time >= stale_after` (warning by default; fails under `--strict`).
6. **Unindexed Wiki Notes (`📑`)**: Markdown notes in `wiki/` that are omitted from `index.md`.
7. **OKF v0.2 Bundle Compliance & Trust Tiers (`📐`)**: Validates every non-reserved note in `wiki/` (`type` required, YAML `<= 16 KiB` without `&`/`*` anchors/aliases, `sources` validation with `legacy_sources_notes` notice, footnote checks, and `Attested Computation` contracts) and computes `trust_tier_counts` (`unverified`, `machine-confirmed`, `human-reviewed`). Also validates root Workspace Profile files (`index.md`, `log.md`, `GEMINI.md`).
8. **4-Signal Graph Relevance Engine (`🧠`)**:
   - **Bridge Hubs**: High-degree nodes bridging $\ge 2$ distinct knowledge domains.
   - **Cluster Cohesion**: Calculates subgraph density $\frac{2E}{V(V-1)}$ across directories to spot sparse conceptual clusters.
   - **Cross-Synthesis Recommendations**: Uses composite multi-signal scoring ($W = 3.0 \cdot \text{Direct} + 4.0 \cdot \text{SourceOverlap} + 1.5 \cdot \text{Adamic-Adar} + 1.0 \cdot \text{TypeAffinity}$) to recommend missing cross-domain syntheses.

### 3. Automated Remediation
- **Missing Index Entries**: Automatically add missing notes into the appropriate section in `index.md`.
- **Table Pipe Invariant Violations**: Run `--fix` to repair escaped pipe characters inside markdown table links (replace `[[Target\|Alias]]` with `[[Target|Alias]]`).
- **Legacy Sources Migration**: Run `--fix --migrate-sources` to deterministically upgrade legacy string `sources:` entries into `{id, resource}` mappings.
- **Human Trust-Tier Approval**: Run `--approve-human <wiki-note-path>` after manual review to stamp `verified: [{ by: human:<id>, at: <UTC> }]`.
- **Orphan & Wanted Pages Resolution**: Add reciprocal connections in corresponding concept or source summaries, or create high-priority notes listed in `wanted_pages`.
- **Cross-Synthesis Creation**: When recommended by the 4-signal engine, suggest or create `wiki/synthesis/` notes bridging high-affinity topics.

### 4. Append Audit Entry to `log.md`
Prepend a lint audit entry to `${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}/log.md`:
```markdown
## [YYYY-MM-DD] lint | Vault Health & 4-Signal Graph Audit
- Scanned N notes across wiki/, raw/, and index.md.
- Graph connections: N resolved links, 0 broken links.
- OKF compliance: 100%.
- Bridge Hubs identified: <list of key hubs>.
- Remediations: <list of auto-repaired links or index entries>.
```

---

## 🛡️ Critical Invariants
- **Table Wikilink Invariant**: Inside markdown tables, **never escape the pipe character** (always use `[[Target|Alias]]`, never `[[Target\|Alias]]`).
