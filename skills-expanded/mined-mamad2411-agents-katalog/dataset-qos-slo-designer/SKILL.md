---
name: dataset-qos-slo-designer
description: Define measurable dataset SLOs and executable quality checks for research training and evaluation data across accuracy, completeness, conformity, consistency, coverage, timeliness, and uniqueness. Use for data SLIs/SLAs, freshness, label accuracy, deduplication, retention, throughput, producer-consumer negotiation, quarantine-versus-halt policy, Great Expectations, SodaCL, or deciding how good a corpus must be.
---

# Dataset QoS & SLO Designer

## Purpose
Replace "we need better quality data" — which is as diagnosable as telling a doctor "I'm unwell" — with named dimensions, numeric objectives, and executable checks. Data QoS combines **data quality** (the condition of the data) with **service levels** (expectations about its delivery: availability, freshness, support). The output is a negotiated SLO document per dataset that producers can meet, consumers can plan against, and pipelines can enforce. What consumers actually want is a better *experience* of the data; undefined expectations, not messy data, are the usual root cause. (To place these numbers into a versioned contract, hand off to the sibling `data-contract-author` skill.)

## Core model to hold in your head

### SLI → SLO → SLA, and intrinsic vs extrinsic
An **SLI** is what you measure; an **SLO** is the target you set on it; an **SLA** is the agreement (possibly with consequences) with consumers. Quality dimensions split into **intrinsic** (assessable without knowing the use case — conformity, uniqueness) and **extrinsic** (contingent on use — coverage of edge cases matters differently to a safety-eval team than to a pretraining team). Producers cannot address extrinsic dimensions without knowing consumers' use; consumers cannot trust data without visibility of intrinsic ones. This asymmetry is why the SLO doc is a *negotiation instrument*, not a producer decree.

### The seven data-quality dimensions (EDM Council alignment)
Sequence matters operationally: check accuracy before consistency; uniqueness only once volume is significant.

| Dimension | Definition | Training-data failure it names |
|---|---|---|
| Accuracy (Ac) | Data matches its authoritative source / business rules | Label disagrees with adjudicated gold; caption doesn't describe the image; transcription mishears audio |
| Completeness (Cp) | Required attributes populated (not null) | Samples missing labels, license fields, or provenance; empty responses in dialogue pairs |
| Conformity (Cf) | Values match required syntax, type, range, domain values | Malformed JSON turns; label outside the taxonomy; tokenizer-breaking encodings; image not in accepted formats |
| Consistency (Cs) | Values/formats/definitions match across stores and shards | Timestamps UTC in one shard, local in another; "toxicity" scored on different scales across annotation batches |
| Coverage (Cv) | All records that should be present are present | Long-tail languages/domains/edge cases absent; a source silently dropped mid-crawl; class imbalance vs collection plan |
| Timeliness (Tm) | Data reflects current conditions, available when needed | Eval set stale vs current model behavior; news corpus lagging its cutoff claim |
| Uniqueness (Uq) | No involuntary duplication of records/attributes | Near-duplicate documents inflating loss; **train/eval contamination** — the research division's costliest uniqueness failure |

### The SLI menu (service levels complement quality)
Grouped as in the Data QoS table — data at rest, in motion, performance, lifecycle, behavior, time-related:

| SLI | Question it answers | Research example objective |
|---|---|---|
| Availability (Av) | Can I connect/read at all? | Curated bucket + Iceberg catalog reachable 99.9% |
| Throughput (Th) | How fast can data be read? | Sustained ≥ 2 GB/s aggregate to GPU nodes during training windows |
| Error rate (Er) | How often is served data wrong, over what period? | < 0.1% failed record decodes per epoch |
| General availability (Ga) | When is a version ready for consumption? | v2.1.0 GA on the 1st; alpha/beta status flagged in catalog |
| End of support (Es) | Until when are issues fixed? | Prior major supported 90 days after new GA |
| End of life (El) | When does access stop entirely? | Raw crawl deleted per license after 18 months |
| Retention (Re) | How long are records kept? | Full snapshot history 12 months (reproducibility window) |
| Frequency of update (Fy) | How often refreshed? | Curated: weekly; frozen eval sets: never (that's the guarantee) |
| Latency (Ly) | Production-to-availability delay | New annotations queryable within 24h of adjudication |
| Time to detect (Td) | How fast do we find a problem? | Quality-gate failure detected within one pipeline run |
| Time to notify (Tn) | How fast do consumers hear? | Alert to #dataset-announce within 1h of detection |
| Time to repair (Tr) | How fast is it fixed? | Contaminated eval overlap purged within 5 business days |

### Per-dimension example SLIs for training data (the negotiation menu)
Present this crossed view; let producer and consumers pick the few cells that matter:
- **Label accuracy** (Ac): ≥ 97% agreement with double-annotated audit sample, measured weekly on n=500 (a "Friday afternoon measurement" with humans reviewing recent records is the cheap starter before automation).
- **Edge-case coverage** (Cv): each declared slice (language, domain, difficulty band) ≥ its collection-plan floor; alert when any slice share drifts > 20% from plan.
- **Eval freshness** (Tm + Fy): eval sets carry an explicit freeze date and refresh policy; "frozen" is an SLO of *zero* updates plus contamination Tr.
- **Dedup/contamination** (Uq): near-dup rate < 0.5% intra-train (MinHash threshold stated); train↔eval n-gram overlap 0 above declared n.
- **Schema conformity** (Cf): 100% parse rate; label values ⊆ taxonomy version pinned in the contract.
- **Cross-shard consistency** (Cs): identical schema + unit conventions across all shards of a snapshot; batch-effect stats within bounds across annotation vendors.

### Enforcement mapping
Every SLO maps to a check that runs in orchestration (Airflow/Argo on the K8s platform) — an SLO without a check is decoration:

| SLO type | Check implementation | Where it runs | On violation |
|---|---|---|---|
| Conformity, completeness, uniqueness rules | SodaCL checks or Great Expectations suites (both embeddable in the contract; executable via Data Contract CLI `test`) | Post-ingest step, pre-publish gate | Choose per check: halt pipeline / quarantine invalid records / pass-through with segmentation label |
| Accuracy vs gold | Scheduled audit-sample job + human adjudication queue | Weekly DAG | Notify (Tn), open remediation with Tr clock |
| Coverage/drift | Profiling job comparing slice distributions to plan | Per snapshot | Notify; block GA of the snapshot if floor breached |
| Contamination | Overlap scan train↔eval at snapshot creation | Pre-publish gate | Halt — never publish a contaminated eval snapshot |
| Availability/throughput/latency | Platform observability (Prometheus on the serving path) | Continuous | Ops alerting; feeds Td/Tn/Tr measurement |

Violation-handling default: bias toward consumer risk tolerance. Three questions decide it per check:
- What is the cadence of decisions made on this data (per training run? weekly curation cycle?)
- What is the sunk cost of proceeding on bad data (a wasted multi-day GPU run is expensive; a skewed ad hoc EDA is not)?
- What is the opportunity cost of *not* proceeding (a blocked pretraining ingest idles the cluster)?
For eval sets, halt; for pretraining bulk, quarantine-and-flow usually beats blocking a 10-TB ingest on 0.02% bad rows. Whatever the choice, invalid records stay inspectable (quarantine, not silent drop) so stewards can route them back to the source.

### SLO document template
Per dataset+version, sections in order:
1. **Parties and use cases** — producer, named consumers (human and agent), the decisions the data feeds.
2. **Objectives table** — chosen dimensions × SLIs, each with objective, measurement method, window, and current measured baseline.
3. **Intrinsic/extrinsic split** — which consumer supplied each extrinsic target and why.
4. **Enforcement table** — check implementation, where it runs, violation behavior (halt/quarantine/segment).
5. **Incident clocks** — Td/Tn/Tr targets and the notification channel.
6. **Lifecycle** — Ga, Fy, Re, Es, El per version; freeze policy for eval sets.
7. **Review cadence** — when the numbers get renegotiated, and by whom.

## Workflow
1. **Identify the consumers and their decisions.** Pretraining, fine-tuning, eval, agent retrieval — each weighs dimensions differently; an SLO set with no named consumer is theater.
2. **Elicit "normal".** For each key attribute, what values are unremarkable? Prior incidents? This seeds thresholds better than round numbers.
3. **Walk the 7×SLI menu** with producer and consumers together; select the minimal set of cells (aim: 5–12 SLOs per dataset, not 40). Record who wanted each and why.
4. **Set objectives with measurement methods** — every SLO states metric, window, and how it's computed; prefer measured baselines ("current dup rate is 1.8%") over aspirations.
5. **Map enforcement** per the table; decide halt/quarantine/segment per check; wire checks into the orchestration DAG and, where supported, embed them in the data contract so `datacontract test` runs them.
6. **Set the incident clocks** (Td/Tn/Tr) and channel — knowing your users is a prerequisite to Tn.
7. **Draft the SLO doc** from the template, get producer + consumer sign-off, and schedule the review cadence (quarterly, or on any major dataset version).

## Output spec
Deliver: (a) the filled SLO document; (b) the check implementations (SodaCL/Great Expectations snippets) or precise specs for them; (c) the enforcement/violation table; (d) a one-paragraph negotiation record of what each consumer traded off (e.g., freshness for completeness). Numbers destined for the contract go to `data-contract-author` unchanged.

## Guardrails
- No SLO without an SLI measurement method and an owner — "high quality" and "fresh" are banned words in the deliverable.
- Never let the producer set extrinsic targets alone or consumers set intrinsic ones without producer feasibility review — the doc is bilateral.
- Don't blanket-apply all 7 dimensions × 14 SLIs; over-instrumented datasets rot as surely as undocumented ones. Fewer, enforced, beats many, ignored.
- Eval-set contamination checks are non-negotiable whenever a dataset feeds both training and evaluation.
- Latency vs freshness confusion is common — standardize on the Data QoS vocabulary (latency = production-to-availability) in all documents.
- Distinguish measured, claimed, and target numbers in the doc; baseline before you promise.

## Suggested effort
Moderate per dataset: one producer+consumer workshop, one drafting pass, one wiring pass for checks. High for the first dataset on a platform (you're also standing up the enforcement pattern others will copy).
