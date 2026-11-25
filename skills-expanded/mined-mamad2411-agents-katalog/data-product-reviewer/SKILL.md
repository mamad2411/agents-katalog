---
name: data-product-reviewer
description: Review whether a research dataset qualifies as a secure, usable data product using the DAUTNIVS attributes, evidence, API affordances, and source/consumer/aggregate archetypes. Use for dataset readiness, FAIR or data-as-a-product assessments, marketplace publication, agent consumability, maturity scoring, cold-start tests, gap analysis, or deciding whether an asset is a product, beta, or merely files.
---

# Data Product Reviewer

## Purpose
Answer "is this dataset a data product, or just files someone shared?" with an evidence-backed score, not a vibe. Data-as-a-product inverts responsibility: quality and usability accountability sits with the producing team (the researchers closest to the source), not a downstream central team — a shift-left for data. What gets shared on the mesh is not merely data; it's a product whose users' experience is the success metric. The review scores a dataset against the non-negotiable baseline usability attributes (DAUTNIVS — an extension of FAIR: findable, accessible, interoperable, reusable), audits its affordances, and hands back ranked gaps with remediation. (Gaps in contracts route to the sibling `data-contract-author`; gaps in SLOs to `dataset-qos-slo-designer`.)

## Core model to hold in your head

### Archetype first: source-aligned vs consumer-aligned vs aggregate
Classify before scoring, because the bar differs:
- **Source-aligned** — models the reality of collection as it happened (raw crawl events, sensor streams, annotation logs). Must serve *unknown future uses*: capture high-resolution, assume little about consumption. Owned by the collecting team.
- **Consumer-aligned (fit-for-purpose)** — shaped for a known use (an instruction-tuning mix, a benchmark suite). Owned by the team whose use case primarily consumes it.
- **Aggregate** — composes several products (a cross-domain training mix). Ownership is genuinely ambiguous; the review should say who *should* own it (incentivized source domain, primary consumer, or a new domain) rather than leave it orphaned.
Misclassification is itself a finding: a "curated" dataset that is really a lightly renamed raw dump usually fails Understandable and Trustworthy at once.

### The DAUTNIVS rubric (score each 0–2 with evidence)
0 = absent, 1 = partial/manual, 2 = present and self-serve. Evidence means artifacts, not assurances.

| Attribute | Evidence questions for a research dataset |
|---|---|
| **Discoverable** | Is it registered (self-registered, not hand-curated by a central team) in the catalog/marketplace? Does the product itself publish discovery info at build/deploy/run time — origin, owners, timeliness, quality metrics, sample data? Are consumer-contributed signals (top use cases, checkpoints trained on it) visible? Can an ADP agent find it via API query, not just a human via UI? |
| **Addressable** | Is there one permanent, unique URI following the global convention — an aggregate root leading to docs, SLOs, schema, and the data? Does the address survive schema evolution, new snapshots/partitions, and new access modes? Can a training config pin `dataset://domain/name@2.1.0+snapshot=8412370493812` and resolve it a year later? |
| **Understandable** | Semantics documented: entities, relationships, adjacent products? Dataset card with granularity, collection method, label taxonomy? Sample records + example consumer code (ideally a computational notebook that runs)? Can a new researcher or an agent use it with zero hand-holding? Is meaning formalized (contract, schema.org tags), not tribal? |
| **Trustworthy** | Published SLOs (see list below)? Quality metrics computed and served, not claimed? Provenance and license recorded per source? Known-caveats section honest about biases and holes? |
| **Natively accessible** | Served in the modes its users actually work in — Parquet/Iceberg tables for Spark/Trino, streaming for online eval, files for dataloaders — without asking the producer to export? Read paths fast enough for GPU-node consumption? Access request-to-data time measured? |
| **Interoperable** | Uses the platform's global standards: shared identifiers/polysemes (doc IDs, entity IDs across corpora), common schema conventions, standard metadata APIs? Can it be joined/composed with sibling datasets without a bespoke crosswalk? Does it avoid demanding a tightly coupled shared schema from its neighbors? |
| **Valuable (on its own)** | Does it serve a use standalone — at least one named consumer, checkpoint, or paper? Usage telemetry exists (readers, downstream products)? Or is it inventory published to inflate a dataset count? |
| **Secure** | Access control enforced at the product (policy-as-code executed at read time), not by bucket obscurity? Sensitivity classes tagged per field and honored (masking/redaction)? Access audited? PII posture stated and tested? |

Trust is "a confident relationship with the unknown" — the product must close the gap between what users confidently know and what they need to know. The SLO set that closes it (check each is published and measured):

- **Interval of change** — how often changes in the data are reflected
- **Timeliness** — skew between a fact occurring (collection event, annotation) and availability to users
- **Completeness** — degree of availability of all necessary information
- **Statistical shape** — distribution, range, volume; served as computed profiles per snapshot
- **Lineage** — the transformation journey from source to here (and onward to checkpoints)
- **Precision/accuracy over time** — truthfulness as the corpus and the world drift
- **Operational qualities** — freshness, general availability, performance of the read path

### Affordance review (the APIs that make attributes real)
Attributes are outcomes; affordances are the mechanics. Check each exists and note the interface:

| Affordance | Present when… |
|---|---|
| Serve data | Read-only, immutable, versioned/bitemporal output ports; multiple modes; no update-in-place semantics leaking through |
| Consume data | Declared, configured upstream sources only — input ports are explicit (no side-door ingests) |
| Transform data | Transformation code/model versioned with the product; reproducible from inputs |
| Discover / understand / explore / trust | Discovery + docs + SLO APIs served by the product itself (standard endpoints, e.g. via a product gateway/sidecar) |
| Compose | Joinable programmatically with other products via shared IDs and set operations |
| Manage life cycle | Build/runtime config as code; owner can deploy, evolve, retire it independently |
| Observe / debug / audit | Logs, lineage, runtime metrics, access logs via API — lineage to model checkpoints counts here |
| Govern | Policies configured build-time, executed at access time in the product's own context; certification status publishable |

A dataset scoring 2s on attributes but lacking serve/discover/govern interfaces is being propped up by human effort that won't scale — score the attribute down to 1 and say why.

### Architecture cross-checks (raise findings even when scores pass)
- **Design for change**: aspects fronted by APIs; time as an attribute of data, model, and SLOs; all artifacts versioned. A product whose consumers break on every schema tweak fails this even with good docs.
- **Design for scale**: no central chokepoint in its access path (policy runs in the product's own execution context, not a shared gateway that queues).
- **Design for value**: shortcut APIs for the common case (default "latest" without forcing every consumer through bitemporal machinery).

### Scoring output
- **Per-attribute score with the evidence cited** (artifact links, API responses, catalog entries).
- **Verdict bands with floors**: 14–16 may publish only when Discoverable, Addressable, Understandable, Trustworthy, and Secure each score at least 1 and Secure has no unresolved hard-stop policy. A zero in any core attribute means beta/non-product regardless of total. Scores 10–13 may publish behind beta only when all hard-stop policies pass; < 10 remains a dataset, not a product.
- **Top-3 gaps ranked by consumer impact**, each with a remediation, an owner, and the sibling skill that does the work (contract → `data-contract-author`; SLOs → `dataset-qos-slo-designer`; discovery metadata → `dataset-catalog-designer`; storage/versioning mechanics → `training-storage-architect`).
- **Archetype call** and, for aggregates, the ownership recommendation.

## Evidence sources
Pull evidence directly rather than accepting self-report:
- **Catalog/marketplace entry** — registration mode (self-registered vs centrally entered), summary quality, roles assigned, usage stats.
- **The contract and SLO doc in Git** — versions, CI check history, last `datacontract test` result.
- **The product's own APIs** — hit the discovery, SLO, and certify endpoints; record responses as evidence.
- **Storage layer** — snapshot history and retention on the underlying table (reproducibility claims are checkable).
- **Consumers** — experiment-tracker records showing checkpoints pinned to this dataset's versions; one consumer interview.

## Workflow
1. **Scope**: dataset name, version under review, claimed archetype, owner, named consumers. No owner = automatic Trustworthy cap at 1 and a governance flag.
2. **Classify the archetype** and adjust expectations (source-aligned: penalize premature consumer assumptions; consumer-aligned: demand the consumer be named and satisfied).
3. **Collect evidence**: pull the catalog entry, contract, SLO doc, dataset card, sample access via the published address; attempt the "cold-start test" — use the dataset from scratch following only self-serve materials, and time it.
4. **Run the agent-consumability probe**: can a programmatic client resolve address → metadata → schema → sample → access policy without human intervention? The ADP's agents are first-class consumers; a product only humans can navigate scores Discoverable/Understandable ≤ 1.
5. **Score DAUTNIVS** (0–2 each) with evidence per cell; then run the affordance checklist and reconcile (affordance gaps pull attribute scores down).
6. **Interview one real consumer** (or read usage telemetry): does experienced trust match published SLOs? Discrepancy is a finding on Trustworthy regardless of documentation quality.
7. **Write the report**: scores, verdict band, ranked gaps with remediations and skill routing, archetype/ownership call, and a re-review trigger (next major version or 90 days).

## Output spec
A review report containing: metadata block (dataset, version, owner, archetype, date); the 8-row scoring table with evidence; affordance checklist results; verdict band; ranked gap/remediation list with owners; cold-start and agent-probe timings. Keep it to two pages — the score table and the gap list are the deliverable, the prose is connective tissue.

## Guardrails
- Evidence or it didn't happen: a README claiming SLOs without measurement, or "discoverable" meaning "ask in Slack", scores 0–1, never 2.
- Never average away a Secure failure — any 0 on Secure blocks publication regardless of total score.
- Don't reward volume: many datasets published ≠ value; usage links and named consumers are the fitness signal, and Valuable scores on them.
- Score the product, not the team's intentions or roadmap; planned capabilities score as absent with a note.
- Don't let this review become gatekeeping theater for exploratory research data — only datasets intended for cross-team or agent consumption enter review at all.
- Re-reviews are mandatory on major versions; scores decay — a 2024 review does not certify a 2026 snapshot.

## Suggested effort
Light-moderate per dataset (half a day with evidence access: cold-start test + scoring + report). Higher for the first review in an org, which also calibrates the rubric's 0/1/2 anchors against local reality.
