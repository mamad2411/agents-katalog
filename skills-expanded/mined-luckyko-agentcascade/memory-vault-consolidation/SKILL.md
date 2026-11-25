---
name: memory-vault-consolidation
description: "Procedure for consolidating .agent_lessons/ vaults: smart-action triage, hub generation, de-indexing, and scope labeling. Run during AFK Admin tier 5 cleanup."
triggers:
  - "memory vault consolidation"
  - "agent lessons cleanup"
  - "hub generation"
  - "supersede lessons"
  - "de-index lessons"
  - "vault triage"
  - "consolidation delta audit"
version: "1.1.0"
---

# Memory Vault Consolidation

Consolidate `.agent_lessons/` vaults: dedup, tier, hub, and scope. All actions are **de-index or additive** — nothing is deleted (house rule: recoverable-truncation-no-irreversible-memory-loss).

## Live vault set

`discover_vaults()` returns `.agent_lessons` children of `base_dir ∪ extra RO/RW`. Iterate ONLY these — never glob `N:\work\WD\*\` (impostor trees like `AgentCascade_unified` are excluded by construction).

## Feature A — Smart-action triage (supersede/merge/archive)

### Triage pipeline (scale: 2000+ files)

1. **Group by backlink graph + filename family.** Build an undirected graph: node = lesson; edge if (a) one file's `related:` names another's stem, or (b) they share the 2-segment filename prefix family. Take connected components.
2. **Multi-member clusters (≥2) → smart-action queue.** Solo files with no family siblings are NOT touched.
3. **Per cluster, the agent decides one of:**
   - `superseded` — older/less-complete member gets `status: superseded` + `superseded_by: [[survivor]]`; survivor gets `supersedes: [[…]]`
   - `merge` — fold unique content into survivor (use `lossless-merge-fold-then-gated-delete`), then mark folded files `status: superseded`
   - `archived` — historically interesting but no longer actionable → `status: archived`
   - `leave active` — distinct facets sharing a name family (default when unsure)

### Frontmatter schema

```yaml
status: active | superseded | archived   # strict enum, OPTIONAL, default=active
superseded_by: [[new-canonical]]          # present iff status: superseded
supersedes: [[old-lesson]]               # on the survivor
last_validated: 2026-11-11               # audit-only, ISO date
```

**Allowlist de-index rule:** a file is excluded from hinting ONLY if `status:` (lowercased, stripped) is exactly `superseded` or `archived`. Everything else (including 17 existing free-form values, no-frontmatter files) stays active. The code choke-point is `vault.py:rescan()` → `_is_deindexed(meta)`.

### Staleness de-index (Tier 2)

The ONLY automatic-ish prune reason. For a candidate: grep the cited symbol/path in the live project; if the path no longer exists, mark `status: archived` + write the grep command + date into the body. Expect ≈0 content-prunes on a healthy tree. Do NOT archive on filename age alone.

## Feature B — Hub generation (summary hierarchy)

### Clustering algorithm (no embeddings)

1. Undirected graph from `related:` backlinks + 2-segment filename families (same graph as Feature A).
2. **Connected components** = first-pass clusters.
3. **Orphans** (size 1): group by dominant `tags` (most-specific tag, not top-generic like `bugfix`/`testing`). Orphans with no distinctive tag stay solo.
4. **Only emit a hub for clusters ≥3.** Size 2 → Feature A merge. Size ≥8 → split by sub-family prefix.
5. Cap total hubs at ~10% of vault size.

### Hub file format

Lives in the **same vault** as its leaves, named `<cluster-slug>-hub.md`:

```yaml
---
tags: [<cluster-slug>, summary, hub]
hub_id: <cluster-slug>
status: active
last_validated: <date>
---
# <Cluster> — map of content
> Summary layer over K leaf lessons. Leaves are verbatim and never rewritten.
## One-line state of the cluster
<2-4 sentence synthesized state>
## Common gotchas (deduped across leaves)
- <recurring facts>
## Leaves
- [[leaf-1]] — one line
```

### Leaf side

Each leaf gets `hub: <cluster-slug>` in frontmatter (additive; body untouched). The hint render path appends ` (hub: #<slug>)` to the hinted leaf's line. **Leaves are never suppressed** — hubs are additive index files.

### AFK procedure (idempotent, incremental)

**Step 0 — Delta audit (do this FIRST, before any writes; use the scripts' self-reported delta, not manual counts):**
1. Run the pipeline in **dry-run** to read the delta the scripts report themselves:
   - `python cluster_vaults.py` — recomputes + **overwrites** `logs/clusters.json` (safe, regeneratable).
   - `python generate_hubs.py` (dry) → read **"hubs newly written: N"** (N=0 → no new clusters) and **"leaves got hub: field: M"**.
   - `python triage_superseded.py` (dry) → read **"status: superseded added: K"**.
2. **If N=0 AND K=0 → no delta, stop** (report "no delta, nothing to do"). A nonzero M with N=0 is just re-tagging existing clusters — not a reason to run.
3. **Do NOT use an mtime / `LastWriteTime` "modified in the last hour" filter to find new hubs.** `generate_hubs.py` bumps `last_validated` on **every** existing hub, so a time-based glob reports ALL hubs (e.g. 72) as new when only N are genuinely new. The true delta = the script's "hubs newly written" counter, **cross-checked by diffing live `*-hub.md` against the pre-run dated backup** (a hub present live but absent from the backup = new).
4. If there IS a delta, proceed to Step 1.

**Step 1 — Execute (only the delta):**
1. **Snapshot** the vault dir(s) to a dated backup before any write (e.g. `logs/lessons-backup-<YYYYMMDD-HHMM>/<vault>/`).
2. `python cluster_vaults.py` → fresh `clusters.json`.
3. `python generate_hubs.py --execute` → writes new hubs, refreshes `last_validated` on all hubs, adds `hub:` to untagged leaves.
4. `python triage_superseded.py --execute` → flips explicitly-declared supersessions (conservative; 0 on a clean tree).

**Verification (always, even on skip):**
- **Cross-check every `[[leaf]]` ref in each NEW hub against disk:** regex-extract the `[[slug]]` stems from the new hub files and confirm `<vault>/<slug>.md` exists (expect 0 missing). Stronger than spot-checking one hub.
- Spot-check a tagged leaf: `hub:` field present and matches a real hub file.
- Confirm the triage target carries `status: superseded` (de-indexed via `vault.py:_is_deindexed()`).
- Optionally run 1 memory_hint test to confirm de-indexed files are excluded.

Re-run finds existing hubs, updates only `last_validated`, adds no duplicate links.

## Feature C — Scope labels + relocation

### Scope derivation (union rule)

`scope: [vault_default] ∪ [project tags from frontmatter]`
- workspace → `global`; project vaults → their project name
- A workspace file tagged `ninfer` → `scope: [global, ninfer]`
- A project-vault file with no tags → `scope: [<vault_default>]`
- Missing `scope:` → treated as `global` (always eligible)

### Matching rule (task side)

A job's active-scope = `{global} ∪ {project}`. A doc is eligible if its scope intersects the allowed set OR contains `global`. **Exact segment match** (not prefix) to avoid `llama-autoloader`↔`llama-cpp` false positives.

### Relocation (workspace → project vaults)

Files with a single unambiguous project tag move to that project's vault. **Framework/generic lessons must NOT move** (e.g. `framework-prefix-invalidation-after-compaction` is tagged `llama-cpp` but is cross-project). The single-project-tag heuristic over-flags this class — require manual review.

### Code (ships dark)

`matcher.match(query, allowed_scope=None)` — when `allowed_scope` is not None, skip docs whose scope doesn't intersect. Default `None` = no-op. The `project` field on `AgentInstance` is the v2 prerequisite; until then the filter is dark.

## Scripts (in `AgentWorkspace/scripts/`, stdlib-only, dry-run by default, `--execute` to write)

- `cluster_vaults.py` — recomputes full clustering; **overwrites** `logs/clusters.json`; prints a summary (leaf count, clusters ≥3, files covered, size histogram). Always writes (regeneratable artifact).
- `generate_hubs.py` — writes new `<slug>-hub.md` for new clusters, refreshes `last_validated` on existing hubs, adds `hub:` to untagged leaves. **Self-reports the delta:** "hubs newly written: N", "hubs already existed (refreshed): P", "leaves got hub: field: M".
- `triage_superseded.py` — conservative + deterministic: flips a lesson to `status: superseded` ONLY if it EXPLICITLY carries `superseded_by: [[X]]` AND X exists in the vaults; adds the reciprocal `supersedes:` on the survivor. **Self-reports:** "declarations validated: D", "status: superseded added: K". Never infers; idempotent (K=0 on re-run).
- `relocate_lessons.py` / `add_scope_labels.py` — Feature C (relocation/scope), not needed for a routine consolidation.
- `memory_vault_common.py` — shared VAULTS map (6 vaults: workspace, AgentCascade, llama-autoloader, Strata, llama.cpp, ninfer-all), tolerant frontmatter parser, `list_md`/`read_text`.

## Invariants

- **Nothing is deleted.** Superseded/archived files stay on disk, greppable.
- **Hubs are additive.** Deleting a hub reverts to leaf-only hints.
- **Leaves are never suppressed** by a hub's presence.
- **Reversible:** remove `status:` line / delete hub file / restore from the dated backup.
