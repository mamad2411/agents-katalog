---
name: data-contract-author
description: Draft, review, and validate contracts for research training and evaluation datasets using ODCS, Data Contract CLI, or JSON Schema, with field-level sensitivity classification and semantic versioning. Use for dataset handoffs, contract YAML, schema agreements, breaking-change policy, PII tagging, contract CI, source licenses, or reproducibility metadata linking snapshots to materialized artifact manifests.
---

# Data Contract Author

## Purpose
Turn "the training team keeps getting surprised by upstream dataset changes" into a versioned, machine-verifiable YAML contract per dataset — not a wiki page that decays. A data contract is an agreement between a data producer (here: a researcher or collection pipeline) and consumers (curation, training, eval teams, and the ADP's agents), covering schema, semantics, quality, service levels, and people. Contracts are executed in CI, not merely read — that is what separates them from data dictionaries, which drift because nothing fails when they lie. (For scoring whether the dataset behind the contract qualifies as a data product, hand off to the sibling `data-product-reviewer` skill.)

## Core model to hold in your head

### Contracts live at boundaries, not everywhere
Do not contract every table. Apply contracts only at **team, process, or system boundaries** — that is where expectations break and where the definition/enforcement effort pays back. For a research data platform the canonical boundaries are:

| Boundary | Producer → Consumer | What the contract pins down |
|---|---|---|
| Collection → Curation | scrapers/sensors/annotation vendors → curation pipeline | raw schema, encoding, arrival cadence, dedup keys, license/provenance fields |
| Curation → Training | curation team → model-training runs | curated schema, label semantics, quality thresholds, snapshot/version addressing |
| Curation → Eval | curation team → evaluation harness | eval-set freeze policy, contamination guarantees (no train overlap), refresh cadence |
| Dataset → External/ADP | dataset owner → other domains, portal agents | discovery metadata, access roles, sensitivity classes, deprecation dates |

One contract per **dataset + version**. A dataset (product) may carry multiple contracts across versions and variations (raw, curated, aggregated).

### Spec selection (decide once, per platform)
Evaluate against three criteria from the practitioner literature: **guidance** (does the spec prompt you for what to capture?), **extensibility** (custom properties, low switching cost), **tooling** (can something consume the contract and do work?).

| Criterion | ODCS (Bitol / Linux Foundation) | datacontract.com spec | Plain JSON Schema / OpenAPI |
|---|---|---|---|
| Guidance | High — purpose-built; 8 sections prompt semantics, quality, SLAs, people | High — robust, approachable, purpose-built | Low — schema/transport only; roles, semantics, SLAs all DIY conventions |
| Extensibility | Custom properties section; open standard, no vendor lock-in | Custom fields; converts to ODCS, JSON Schema, dbt via CLI (lowest switching cost) | `x-` extensions; everything else is on you to validate |
| Tooling | Growing vendor list; integrates with Data Contract CLI and test-data tools | Strongest: Data Contract CLI (validate, test, diff, generate), online editor, Data Mesh Manager | Massive codegen/validation ecosystem, but permissive datatypes and no data-QoS notions |
| Fit here | Default standard to author in — open governance suits a research org publishing datasets | Use its CLI regardless; adopt spec if CLI-first workflow dominates | Only as a generated artifact for API consumers, never as the source of truth |

Recommended stance for a research division: **author in ODCS, operate through Data Contract CLI** (it reads ODCS), generate JSON Schema/pydantic/dbt artifacts from the contract. Do not roll a bespoke spec — the maintenance cost lands after the author leaves; start from the least egregious open spec instead.

### ODCS section-by-section (v3)
Author in this order; the file is YAML in a Git repo — reviewable, diffable, CI-enforceable.

1. **Fundamentals & demographics** — id, name, domain, version, status. Use the dataset's mesh-wide namespace so the contract is joinable to catalog entries.
2. **Dataset & schema** — one dataset, its tables/objects and properties. Use `businessName`, `description`, `examples`, and `dataGranularityDescription` per column; link contested or computed fields to `authoritativeDefinitions` (businessDefinition URL + referenceImplementation repo). This is where tribal knowledge gets written down.
3. **Data quality** — rules tied to schema fields (see sibling `dataset-qos-slo-designer` for choosing dimensions and thresholds).
4. **Pricing** — usually omit internally; use for cross-charging GPU-adjacent storage if the org does showback.
5. **Stakeholders / team** — the human lineage: `username`, `role`, `dateIn`, `dateOut`, `replacedByUsername`. Researchers rotate; this section is who to ask when the labeler heuristics are undocumented.
6. **Roles** — access roles per consumption mode (read curated, read raw, PII-clear).
7. **Service-level agreements** — the SLIs/SLOs the producer commits to (frequency of update, latency, retention, time-to-detect/notify/repair, end-of-support).
8. **Custom properties** — key-value escape hatch. Research-division staples: `trainedCheckpoints`, `sourceLicense`, `collectionMethod`, `evalFrozen: true`, `icebergSnapshotId`, and `materializedArtifactManifest` (URI + digest). A snapshot identifies logical table state; reproducibility also requires hashes for the materialized shards plus transform/image/loader versions, ordering, and seed.

### Worked example (curated instruction-tuning corpus, ODCS v3 excerpt)
```yaml
apiVersion: v3.0.0                 # fundamentals
kind: DataContract
id: instr-tuning-curated
domain: curation
version: 2.1.0
status: active
schema:
  - object: pairs
    logicalType: object
    physicalType: table            # Iceberg table on MinIO/S3
    description: Deduplicated prompt/response pairs for instruction tuning
    dataGranularityDescription: One row per accepted annotation, keyed pair_id
    properties:
      - name: pair_id
        logicalType: string
        physicalType: varchar(26)  # ULID
        isUnique: true
      - name: response_text
        logicalType: string
        description: Final adjudicated response. Use this, not draft_text,
                     which predates adjudication.
      - name: annotator_id
        logicalType: string
        customProperties:
          - property: sensitivityClass
            value: confidential
          - property: semanticType
            value: https://schema.org/identifier
        authoritativeDefinitions:
          - url: https://catalog.internal/term/annotator
            type: businessDefinition
team:
  - username: kfarrell
    role: dataset-owner
    dateIn: 2026-02-01
slaProperties:
  - property: frequencyOfUpdate
    value: weekly
  - property: endOfSupport
    value: 2027-01-31
customProperties:
  - property: icebergSnapshotId
    value: "8412370493812"
  - property: materializedArtifactManifest
    value: "s3://ml-artifacts/manifests/instr-tuning-2.1.0.json#sha256=<digest>"
  - property: evalFrozen
    value: false
```

### Versioning and breaking-change policy (semver, enforced)
| Artifact | Patch (x.y.Z) | Minor (x.Y.0) — backward compatible | Major (X.0.0) — breaking |
|---|---|---|---|
| Table/schema | — | Add optional column; logic change to existing column | Change column type or name; remove column; merge tables |
| Data contract | Metadata/description edits; stakeholder changes | Revise a quality rule; add optional key or key with default; add custom property | Change type/name of a key; remove a key |
| Research-specific | Fix typo in label taxonomy description | Add a new label class (consumers ignore unknowns) | Redefine an existing label class; re-split train/eval; change dedup key |

Policy: majors require a deprecation window with old and new versions served in parallel (state the window in SLAs); consumers pin a major and migrate deliberately. Producers follow Postel's law — conservative in what you publish, liberal in what you accept. A re-annotation that silently changes label semantics without a major bump is a contract violation even though the schema is unchanged — say so in review.

### CI workflow with Data Contract CLI
Run in the dataset repo's pipeline (Argo Workflows/GitHub Actions on the K8s platform):
1. `datacontract lint <contract>.yaml` — spec validity, on every PR.
2. `datacontract test` — executes the embedded quality checks (SodaCL / Great Expectations / Monte Carlo syntax) against the actual store; run post-ingest and scheduled.
3. `datacontract breaking old.yaml new.yaml` (diff/changelog) — detects breaking changes between versions without touching the database; gate contract PRs on it and require a major bump + migration note when it fires.
4. `datacontract export` — generate consumer artifacts: JSON Schema, pydantic models for loaders, dbt models, SQL DDL, HTML catalog page. Consumers code against generated artifacts, never hand-copied schemas.

### PII and sensitivity tagging
Two orthogonal annotations on every field, including nested fields, both machine-readable so policy engines and the ADP's agents can act on them:
- **Sensitivity classification** — `public | internal | confidential | restricted | not-sensitive`; drives access roles, masking, and which zones the field may reach. Enforce presence for every field regardless of type—dates, numeric identifiers, coordinates, booleans, and structures can be sensitive. Define how container classifications inherit to nested fields and reject ambiguous overrides.
- **Semantic tagging** — schema.org URLs (`birthDate`, `email`, `postalCode`, `identifier`) to say *what the field is*, independent of storage type. This doubles as the RAG/agent-retrieval hook: agents resolve meaning from the ontology, not column names.
Research corpora scraped from the web contain incidental PII — the contract must state the scrubbing guarantee (e.g., "email-pattern redaction ≥ 99.5%") as a quality rule, not a hope. Disambiguate overloaded terms ("curated", "gold", "labeled") with bounded contexts: define the term per domain in `authoritativeDefinitions` rather than fighting for one global definition.

## Workflow
1. **Locate the boundary.** Confirm the contract sits at a team/process/system boundary from the table above; if it's internal plumbing of one team, advise against contracting it.
2. **Identify parties and purpose.** Producer, consumers (include agent consumers), producer-led or consumer-led, what decisions the data feeds, cadence constraints.
3. **Elicit meaning before rules.** Concrete example records (valid and invalid), what's "normal" per attribute, in/out of collection scope, overloaded terms → bounded-context definitions.
4. **Select spec** via the criteria table (default: ODCS + Data Contract CLI); record the rationale in one paragraph.
5. **Draft the contract** section by section per the guide, worked example as skeleton. Tag sensitivity + semantics on every field; fill the team section with real humans and dates.
6. **Define enforcement**: quality checks embedded, violation handling chosen per check (halt / quarantine invalid records / pass with segmentation), CLI stages wired into CI.
7. **Set the change policy**: semver table adopted, deprecation window stated, `breaking` gate on contract PRs.
8. **Get sign-off** from producer and at least one named consumer; merge; the contract's Git history is its audit trail.

## Output spec
Deliver: (a) the contract YAML file(s), one per dataset+version; (b) a one-page decision record (spec choice, boundary map for the pipeline, violation-handling choices); (c) the CI snippet running lint/test/breaking/export; (d) the breaking-change policy table adapted to the org. Everything a consumer needs must be in or generated from the contract — if a consumer still needs to Slack the producer to use the data, the contract is incomplete.

## Guardrails
- Never produce a contract that is schema-only — semantics, people, SLAs, and sensitivity are the point; "not only schema" is the standard's core principle.
- Refuse silent breaking changes: any type/name/removal/semantic redefinition without a major bump is a defect to flag, not a style preference.
- Don't duplicate the contract's content into a separate data dictionary — generate views from the contract instead; parallel documents decay.
- Don't gate research iteration on contract ceremony for exploratory scratch data — contracts start where a second team (or an agent) consumes the data.
- Plain-text YAML in version control, never spreadsheets or wiki tables as the source of truth.

## Suggested effort
Moderate for a single boundary (one elicitation session + draft + CI wiring); high for a full collection→curation→training→eval pipeline (boundary mapping first, then one contract per handoff, sequenced by consumer pain).
