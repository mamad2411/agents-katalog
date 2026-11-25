---
id: "skill_ad46655dfa65459495db46461e581c09"
name: "pinakes-verifiable-retrieval"
display-name: "Pinakes Verifiable Retrieval"
description: "Retrieve reproducible, complete, verifiable records from 26 public biomedical sources (PDB, UniProt, NCBI Protein/Virus/Datasets, ClinVar, Ensembl, gnomAD, PubChem, AlphaFold, ClinicalTrials, openFDA, Open Targets, Reactome, GTEx, GWAS Catalog, and more — run `catalog` for the full list) via Pinakes — the same 8 verbs over an MCP server (pinakes_<verb> tools) or the identical pinakes CLI. Use when an agent must pull biomedical data that has to be reproducible, deterministic, byte-identical, complete-or-fail, or independently verifiable; when a record count, cited fact, or dataset must carry provenance a reviewer can re-derive offline; when pinning a content-addressed snapshot; reading a manifest's completeness or reproducible flag; verifying before citing; or self-correcting a rejected filter. Teaches the judgement the tool schemas do not: pin-or-no-determinism, complete vs best_effort, and verify-before-cite."
short-description: "Retrieve reproducible, complete, verifiable biomedical records via Pinakes (MCP pinakes_<verb> tools or the identical CLI) over 26 public sources. Use when data must be deterministic, byte-identical, complete-or-fail, snapshot-pinned, or carry provenance a reviewer can re-derive offline — and when reading a manifest, verifying before citing, or self-correcting a rejected filter."
category: "methodology"
keywords: "pinakes, reproducible, deterministic, verifiable, provenance, manifest, snapshot, content-addressed, complete-or-fail, verify, offline, MCP, CLI, biomedical, UniProt, PDB, ClinVar, Ensembl, gnomAD, PubChem, AlphaFold, NCBI Virus, NCBI Protein, NCBI Datasets, ClinicalTrials, openFDA, Open Targets, Reactome, GTEx, GWAS Catalog, InterPro, Rhea, JASPAR, Monarch, HPO, Gene Ontology, citation, completeness, maturity"
version: "1.0"
last-updated: "2026-06-13"
---

# Pinakes Verifiable Retrieval

Pinakes is a deterministic, verifiable **input layer** for AI agents over 26
public biomedical sources, shipped as one static Go binary that exposes the same
8 verbs over an MCP server (`pinakes_<verb>` tools), an identical CLI
(`pinakes <verb>`), and a loopback REST server. Its value is **invisible from the
tool schemas**, which is why this skill exists: every result pins a
content-addressed snapshot (byte-reproducible forever), retrieval is
**complete-or-fail** (reconciled against the source's authoritative total — never
a silent partial), and every result ships a re-runnable **manifest** that
`verify` re-derives **offline**. This skill teaches the judgement layer — *pin or
you get no determinism, read completeness honestly, verify before you cite* — not
the schemas (`tools/list` and `pinakes catalog` already carry field names,
operators, and enums; do not duplicate them here).

**Boundary.** Pinakes fixes the *input* only. It does **not** run analysis, does
not build evolutionary trees, and **never claims a source is wrong** — the public
databases are authoritative. It fixes naive client retrieval (no imposed order,
no reconciliation, no provenance). It covers **public** sources only. The arXiv
literature corpus is **not yet shipped** — do not assume it. Hand the verified
manifest to a domain skill for the actual science.

---

## When to Use This Skill

✅ **Use when:**
- An agent must pull biomedical data that has to be **reproducible /
  deterministic / byte-identical** across runs.
- You need a **record count** that goes in a methods section and must reproduce
  next month.
- You need a **cited fact** a reviewer can independently re-fetch and check.
- You are handed a **manifest** and must confirm it reproduces before building on
  it (verify-before-cite).
- A query was **rejected** (`UNKNOWN_FIELD`, `BAD_ENUM`, `INVALID_FILTER`,
  `UNSATISFIABLE_QUERY`) and the agent must self-correct rather than retry blind.
- You must know whether a result is **complete vs best_effort vs partial**, or
  whether it is **reproducible** at all.
- You are pulling from PDB, UniProt, NCBI Protein, NCBI Virus, ClinVar, Ensembl,
  gnomAD, PubChem, AlphaFold, ChEMBL, ClinicalTrials, openFDA, cBioPortal, or
  NCBI Datasets and want provenance, not just bytes.

❌ **Do not use when:**
- The task is **analysis** (differential expression, alignment, tree-building,
  modeling). Use this to *fetch the verified input*, then a domain skill.
- You want to assert a source is **wrong** or compute a "true eternal count" —
  Pinakes does neither; a count is a property of a pin, not of all time.
- The source is **private/internal** or behind a login — Pinakes serves public
  databases only.
- You need the **arXiv** corpus — not shipped yet.
- A raw, throwaway lookup where reproducibility genuinely does not matter (rare —
  if it will be cited or re-run, it matters).

---

## Clarification Questions

### 1. ⚠️ CRITICAL: ASK THIS FIRST — Will this result be reported, cited, or re-run?

If **yes**, you MUST pin a concrete `snapshot_version` (`sha256:…`, never empty,
never `latest`) and `verify` the manifest **before** citing. An unpinned result is
served from `latest` ⇒ `reproducible:false`, and a re-run next month silently
returns a different set — so a bare count or fact with no pin is not a fact you can
cite. If the answer is genuinely **no** (a throwaway lookup nobody will repeat),
you may skip the pin — but confirm that explicitly, because this is rare.

### 2. Which source, and is it materializable?

- Which of the 26 sources answers the question (run `catalog` to confirm the id
  and its filter schema)?
- Is that source **L2+** and **HostServe**? A copyleft source (**ChEMBL**, served
  live) can **never** be `reproducible:true` — if the task demands reproducibility,
  route to a materializable source instead (see *Picking a Connector*).

### 3. Does the answer have to be complete, or is best-effort acceptable?

- If it must be the **whole** answer, **do not pass a `limit`** — a cap below the
  authoritative total downgrades the result to `best_effort` (it cannot be
  reconciled). Let complete-or-fail reconcile.
- If a sample is fine, label it `best_effort` honestly — never present a capped or
  best-effort set as "all matching records".

---

## Setup & Surface Detection

Pinakes is **client-neutral**: the same 8 verbs are an MCP tool *and* a CLI
subcommand. Detect the surface and degrade gracefully.

**Rule:** *use the MCP `pinakes_<verb>` tool if it is present in your tools; else
shell out to the identical `pinakes <verb>` CLI.* Every recipe below is shown in
both forms — they are interchangeable.

- **MCP present** (tools named `pinakes_catalog`, `pinakes_search`, …): call them
  directly. Generic stdio registration is just:
  ```json
  {"mcpServers": {"pinakes": {"command": "pinakes", "args": ["mcp"]}}}
  ```
  No token, no Docker, no `env`. If a GUI client can't find `pinakes` on its
  `PATH`, replace `"command": "pinakes"` with the absolute path from
  `which pinakes`.
- **CLI only** (no MCP tools, but `which pinakes` resolves): run `pinakes <verb>`
  with the same arguments. Pass a manifest as `--manifest @manifest.json`.
- **Neither** (`which pinakes` is empty): you cannot fetch. Say so plainly and
  stop — do not fabricate records or a manifest. Point the user at install (depth
  → [references/setup.md](references/setup.md)).

Confirm wiring with `pinakes catalog` (CLI) or `pinakes_catalog` (MCP) before the
first real query. Depth: [references/setup.md](references/setup.md).

---

## The Core Loop (1–8)

Run this loop for any retrieval that will be reported, cited, or re-run. The
hinge steps are **4 (pin a snapshot)**, **5 (read the manifest)**, and **7
(verify)** — skip any one and the determinism guarantee silently evaporates.

1. **Catalog.** `pinakes_catalog` / `pinakes catalog` to list sources (id,
   maturity, license); scope to one source to get its **filter schema** (fields,
   operators, enums). This is how you learn what is queryable.
2. **Validate locally.** Check every filter field/operator/value against that
   schema *before* any network call. A bad one is rejected locally with a precise
   code (`UNKNOWN_FIELD` / `BAD_ENUM` / `INVALID_FILTER`) — fix it here, cheaply.
3. **Estimate (optional).** `pinakes_estimate` / `pinakes estimate` for a dry-run
   record/byte/call count. **An estimate never substitutes for reconciliation** —
   it is a cost preview, not a completeness claim.
4. **Retrieve WITH a pinned `snapshot_version`.** `search` / `get` / `resolve`,
   always passing a concrete `snapshot_version` (`sha256:…`). **Empty or
   `latest` ⇒ not reproducible.** This is the #1 footgun (see below).
5. **Read Completeness + `reproducible`.** Inspect the manifest: is
   `completeness.state` `complete`? Is `reproducible` `true`? Do not report until
   you have read these — the records alone don't tell you.
6. **Export (optional).** `pinakes_export` / `pinakes export` to materialize to
   parquet/json/fasta/vcf/mmcif. The reproducibility anchor stays the canonical
   NDJSON `logical_record_hash`, **not** the export bytes.
7. **Verify.** `pinakes_verify` / `pinakes verify --manifest @manifest.json`
   re-derives the count and record hash from the pinned snapshot **offline**.
   Exit 0 / `verified:true` ⇒ it reproduces. A refusal ⇒ stop, do not cite.
8. **Cite the manifest.** The citation *is* the manifest: `source_id`, pinned
   `snapshot_version`, `logical_record_hash`, `completeness.state`, and per-source
   `license`/attribution. Hand this to the next skill.

**Copy-able checklist:**
```
[ ] 1. catalog → confirmed source + read filter schema
[ ] 2. filters validated locally (no UNKNOWN_FIELD / BAD_ENUM / INVALID_FILTER)
[ ] 3. (estimate, if cost matters — not a completeness claim)
[ ] 4. snapshot_version pinned (concrete sha256:… — NOT empty, NOT "latest")
[ ] 5. manifest read: completeness.state == complete? reproducible == true?
[ ] 6. (export, if a file is needed — hash is over NDJSON, not export bytes)
[ ] 7. verify → exit 0 / verified:true (offline)
[ ] 8. cited the manifest (source_id + snapshot_version + logical_record_hash
       + completeness + license/attribution)
```

---

## Pin or no determinism (the #1 footgun)

This is the single most common failure. The `snapshot_version` is what makes a
result reproducible. **No pin ⇒ the engine serves `latest` ⇒
`reproducible:false`**, and a re-run next month silently returns a different set.
A bare count or fact with no pin is not a fact you can cite.

A manifest is `reproducible:true` **only when ALL of these hold** (the engine's
`SetReproducible` enforces every one — you cannot bypass it):

| # | Condition | Source of truth |
|---|-----------|-----------------|
| 1 | Served from a **pinned snapshot** (`served_from` = `snapshot@…`) | `ServedFrom.DeterminismClaimable()` |
| 2 | Completeness is **`complete`** and reconciled (count == authoritative) | `Completeness.Reconciled()` |
| 3 | At least one source, and **every** source is **L2+** (any L0/L1 ⇒ false) | `MaturityLevel.DeterminismClaimable()` |
| 4 | **Every** source pins a concrete snapshot — **not empty, not `latest`** | `SetReproducible` |

If any row fails, `reproducible` is `false` — honestly. The fix is almost always
row 1/4: **pass a `snapshot_version`.** Full table:
[references/manifest-and-completeness.md](references/manifest-and-completeness.md).

---

## Reading the Manifest

The manifest is the product. Read it; never infer from the record list.

**Completeness decision table** (`completeness.state`):

| State | Means | What you may say | Action |
|-------|-------|------------------|--------|
| `complete` | Retrieved count **reconciled** against the source's authoritative total and they **match** | "the whole answer (N/N)" | Safe to cite as complete |
| `best_effort` | No trustworthy authoritative total exists (carries a mandatory `reason`) | "a best-effort set, completeness unproven" — **never** "all" | Report the `reason`; do not claim complete |
| `partial` | A multi-source query where ≥1 upstream failed (has `reason` + `resume_cursor`) | "partial; some upstream failed" | Resume via cursor or report the gap |

**The limit footgun.** A `limit` below the source's authoritative total **cannot
be reconciled**, so the engine downgrades the result to **`best_effort`** — not
`complete`. If you need a `complete` answer, **drop the cap** and let
complete-or-fail reconcile, or report honestly that the set is `best_effort`.
Treating a `limit`-capped set as "all matching records" is a classic error.

Key manifest fields to cite: `manifest_schema_version`, `engine_version`, per-
source `snapshot_version` + `maturity` + `license`, `logical_record_hash` (the
SHA-256 over canonical NDJSON — the anchor), `completeness`, `served_from`, and
`reproducible`. Depth:
[references/manifest-and-completeness.md](references/manifest-and-completeness.md).

---

## Picking a Connector

Short routing table (26 sources). **L0** = catalog-only (not queryable); **L1** =
queryable but **never** reproducible (live proxy); **L2+** = reproducible against
a pinned snapshot. All 26 shipped connectors are **L2**. `catalog` is the live
source of truth; this table is the at-a-glance version, the full one with SPDX and
attribution flags lives in [references/sources.md](references/sources.md).

| Source id | Domain | Maturity | License posture |
|-----------|--------|----------|-----------------|
| `pdb` | structures | L2 | public-domain → materializable |
| `uniprot` | proteins | L2 | attribution (CC-BY-4.0) → materializable |
| `ncbi-protein` | sequences | L2 | public-domain → materializable |
| `ncbi-virus` | viruses | L2 | public-domain → materializable |
| `ncbi-datasets` | genes | L2 | public-domain → materializable |
| `clinvar` | variants | L2 | public-domain → materializable |
| `ensembl` | genomics | L2 | no-restrictions → materializable |
| `gnomad` | variants | L2 | public-domain → materializable |
| `pubchem` | compounds | L2 | public-domain → materializable |
| `alphafold` | structures | L2 | attribution (CC-BY-4.0) → materializable |
| `clinicaltrials` | clinical_trials | L2 | public-domain → materializable |
| `openfda` | drug_labels | L2 | public-domain → materializable |
| `opentargets` | target-disease | L2 | public-domain → materializable |
| `reactome` | pathways | L2 | public-domain → materializable |
| `interpro` | protein_families | L2 | public-domain → materializable |
| `complex-portal` | protein_complexes | L2 | public-domain → materializable |
| `rhea` | reactions | L2 | attribution (CC-BY-4.0) → materializable |
| `gene-ontology` | ontology | L2 | attribution (CC-BY-4.0) → materializable |
| `gtex` | expression | L2 | IndexProxy (`redistribute:false`) — see note |
| `gwas-catalog` | gwas | L2 | IndexProxy (`redistribute:false`) — see note |
| `jaspar` | tf_motifs | L2 | IndexProxy (`redistribute:false`) — see note |
| `monarch` | phenotypes | L2 | IndexProxy (`redistribute:false`) — see note |
| `hpo` | phenotypes | L2 | IndexProxy (`redistribute:false`) — see note |
| `cbioportal` | cancer_genomics | L2 | IndexProxy (`redistribute:false`) — see note |
| `chembl` | drugs | L2 | **copyleft (share-alike) → served LIVE, `reproducible:false`** |
| `guide-to-pharmacology` | pharmacology | L2 | **copyleft (share-alike) → served LIVE, `reproducible:false`** |

**⚠️ Copyleft caveat (ChEMBL, Guide to PHARMACOLOGY).** These two are
Creative Commons Attribution-ShareAlike (copyleft / share-alike). The engine
**refuses to materialize** a share-alike source, so **every result from them is
served live and is `reproducible:false`** by construction — no pin makes it
reproducible. Carry the attribution string; for a reproducible drug-data answer,
prefer a materializable source. Full routing, license postures, and attribution
rules: [references/sources.md](references/sources.md).

---

## Worked Recipe A — Ebola, reproduced (flagship)

Goal: the **complete-genome records for *Zaire ebolavirus*** in NCBI Virus,
pinned, complete, and offline-verified. Exact values from the repo case study.

**MCP form:**
```json
{
  "name": "pinakes_search",
  "arguments": {
    "source_id": "ncbi-virus",
    "filters": [
      { "field": "organism_taxon_id", "operator": "eq", "value": "186538" },
      { "field": "complete_only",     "operator": "eq", "value": "true" },
      { "field": "released_since",    "operator": "gte", "value": "2023-01-01" }
    ],
    "snapshot_version": "sha256:b1983c09cd5c70137db4724494d2efaf263baa88c795b4ff1a457ba82fe72f90"
  }
}
```
Then `pinakes_verify` with the returned manifest.

**CLI form (identical):**
```sh
PIN=sha256:b1983c09cd5c70137db4724494d2efaf263baa88c795b4ff1a457ba82fe72f90
pinakes search --source-id ncbi-virus \
  --filters organism_taxon_id:eq:186538 \
  --filters complete_only:eq:true \
  --filters released_since:gte:2023-01-01 \
  --snapshot-version "$PIN"            # → 32 records, Complete (32/32)
pinakes verify --manifest @manifest.json   # → {"verified": true}, offline
```

**Result (this pin):** 32 records, `completeness.state = complete` (32 == 32
authoritative), `logical_record_hash = sha256:01fffd0c…`, NCBI datasets version
`18.30.1`, `reproducible: true`. `verify` re-derives the count and hash from the
snapshot **offline** — a shortened or altered snapshot is refused
(`COMPLETENESS_DRIFT` / `HASH_MISMATCH`).

**Cite it like this:** "NCBI Virus, complete-genome records for taxon 186538
released since 2023-01-01; snapshot `sha256:b1983c09…`; 32 records, Complete
(32/32); `logical_record_hash sha256:01fffd0c…`; verified offline." The "32" is a
property of **this pin**, not an eternal count — NCBI grows daily; the pin always
yields this set. More recipes (UniProt, resolve, export, multi-filter):
[references/recipes.md](references/recipes.md).

---

## Error Handling

Stable, surface-independent codes (identical across MCP/CLI/REST). Group them by
**action**, not by name:

| Band | Codes | Action |
|------|-------|--------|
| **Self-correct locally** | `UNKNOWN_FIELD`, `BAD_ENUM`, `INVALID_FILTER` | Re-read the catalog filter schema; fix the field / value / operator **before** any network call |
| **Self-correct the query** | `UNSATISFIABLE_QUERY` | Caller-fixable (maps to 4xx/422); read the message, **change** the query (add a co-filter, shrink the window) — **never retry unchanged** |
| **Pin / input problems** | `UNKNOWN_SOURCE`, `SNAPSHOT_NOT_FOUND`, `UNPINNED_SOURCE`, `IMMATURE_SOURCE` | Fix the source id or supply a valid pinned `snapshot_version`; an L0/L1 source cannot be reproducible |
| **Verify refusals (manifest input)** | `MANIFEST_NIL`, `NOT_REPRODUCIBLE`, `NO_SOURCES`, `MULTI_SOURCE_UNSUPPORTED` | The manifest can't be verified as posed; report it — do not fabricate a pass |
| **Drift refusals — a FEATURE** | `HASH_MISMATCH`, `COMPLETENESS_DRIFT`, `SPEC_DRIFT`, `FILTER_DRIFT`, `SERIALIZER_DRIFT`, `SCHEMA_DRIFT`, `GRAPH_DRIFT`, `PROVENANCE_DRIFT`, `SERVED_FROM_DRIFT`, `LICENSE_DRIFT`, `ENGINE_MISMATCH`, `MANIFEST_SCHEMA_DRIFT`, `QUERY_SNAPSHOT_MISMATCH`, `MANIFEST_DRIFT` | **Stop and report the exact code.** A drift refusal caught a real reproducibility problem; it is not a bug to retry around |
| **Fallback** | `INTERNAL` | Unexpected; report verbatim, do not paper over |

A `verify` that returns a drift code is doing its job — refusing a result that
does **not** reproduce. Full ~28-code table grouped by recover-or-stop:
[references/errors.md](references/errors.md).

---

## Decision Points

| Decision | Default | Override when |
|----------|---------|---------------|
| Pin a `snapshot_version`? | **Always** | Never skip if the result is reported/cited/re-run |
| MCP tool vs CLI | MCP `pinakes_<verb>` if present | CLI `pinakes <verb>` when no MCP tool; same args |
| Apply a `limit`? | **No** (limit ⇒ `best_effort`) | Only for a deliberate sample you label non-complete |
| `estimate` before `search`? | Skip for small queries | Use when cost/size is unknown — not a completeness claim |
| Verify before citing? | **Always** | No exception — verify is the gate |
| Use ChEMBL for a reproducible answer | **No** (served live) | Use only when live drug data is acceptable; carry attribution |
| Accept `best_effort` | Only if labeled as such | Never present `best_effort`/`partial` as "all" |

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `reproducible:false` on a clean query | No `snapshot_version` (served `latest`) | Pass a concrete `sha256:…` pin |
| Count differs on re-run | Ran against `latest`; source grew | Pin a snapshot; report count as a property of the pin |
| Result marked `best_effort` unexpectedly | A `limit` below the authoritative total | Drop the `limit`; let complete-or-fail reconcile |
| `IMMATURE_SOURCE` on verify | Source is L0/L1 (not L2+) | Reproducibility is impossible below L2; pick an L2+ source |
| ChEMBL never reproducible | Copyleft (share-alike) → served live | Expected; carry attribution, prefer a materializable source for reproducibility |
| `UNSATISFIABLE_QUERY` loops | Retried identical filters | Read the message; change the query (co-filter, smaller window) |
| `UNKNOWN_FIELD` / `BAD_ENUM` | Filter not in the source schema | Re-read `catalog --source-id <id>`; fix locally before the call |
| `SNAPSHOT_NOT_FOUND` | Pinned a snapshot not in the store | Use a snapshot the catalog/case study actually pins |
| `HASH_MISMATCH` / `COMPLETENESS_DRIFT` on verify | Snapshot shortened/altered, or drift | **Stop**; do not cite — the refusal is correct |
| MCP client can't find `pinakes` | Not on the GUI app's `PATH` | Use the absolute path from `which pinakes` in the config |
| Export bytes differ but hash matches | Export format isn't the anchor | The anchor is the NDJSON `logical_record_hash`, not export bytes |
| Treating an estimate as the count | `estimate` is a dry run | Estimates never substitute for reconciliation; run `search` |
| Multi-source verify refused | `MULTI_SOURCE_UNSUPPORTED` (deferred) | Verify single-source manifests; split the query |
| Asked for arXiv / literature | Not shipped yet | Out of scope; use a literature tool, not Pinakes |
| `resolve` returns ambiguities | Many-to-many identifier mapping | Surfaced on purpose, not an error; read `ambiguities`, pick per authority |

---

## Suggested Next Steps

Pinakes produces the **verified input**; hand the manifest to a domain skill for
the science:

1. **Variant work** (`clinvar` / `gnomad` / `ensembl` results) →
   `genetic-variant-annotation`, `genetic-target-hypothesis`.
2. **Drug / compound data** (`chembl` / `pubchem` / `openfda`) →
   `clinicaltrials-landscape`, `literature-preclinical`.
3. **Structures** (`pdb` / `alphafold`) → structure-facing wet-lab skills
   (e.g. `adaptyv-api` for characterization).
4. **Any dataset** → `data-analysis-best-practices` **before** the first model —
   carry the manifest as the provenance record.

Always pass along the `logical_record_hash` + `snapshot_version` so the next
skill inherits a re-checkable input, not a loose number.

---

## References

**Bundled (one level deep, on-demand):**
- [references/verbs.md](references/verbs.md) — the 8 verbs, chaining, gotchas, and the `pinakes_<verb>` ↔ CLI mapping.
- [references/manifest-and-completeness.md](references/manifest-and-completeness.md) — completeness + reproducible truth tables, manifest citation fields.
- [references/errors.md](references/errors.md) — the full stable error-code vocabulary grouped by recover-or-stop action.
- [references/sources.md](references/sources.md) — the 26-connector routing table, maturity, license/posture.
- [references/setup.md](references/setup.md) — client-neutral install, generic stdio config, `which pinakes` fallback, MCP-or-CLI rule.
- [references/recipes.md](references/recipes.md) — Recipes B–F (UniProt, resolve, export, …), each ending in cite-the-manifest, in both MCP + CLI forms.

**Scripts:**
- `scripts/verify_and_cite.sh` — verify a manifest, and on pass print a paste-ready citation; degrades to a no-op message if `pinakes` is absent.

**Self-describing surface:** `pinakes catalog` and MCP `tools/list` carry the
live source list, filter schemas, and every verb's parameters — the contract is
in-band. This skill is the judgement layer on top.
