---
name: dataset-catalog-designer
description: Design an identity-aware dataset catalog or marketplace that supports human and agent discovery without leaking unauthorized metadata. Use for dataset search, catalog metamodels, knowledge graphs, glossaries and taxonomies, lineage, self-registration, pull-versus-push metadata, semantic search, role assignment, agent APIs, stale catalog data, or recall and precision problems.
---

# Dataset Catalog Designer

## Purpose
Design the layer where a researcher — or an ADP agent — goes from "I need multilingual dialogue data with permissive licenses" to a pinned, accessible dataset version, without asking around in Slack. Two failure modes dominate: catalogs that centralize and duplicate metadata until it is stale and unloved, and catalogs whose domain structure mirrors pipelines or org charts and is therefore unsearchable. The design deliverable is a metamodel, role model, glossary plan, and architecture choice (catalog, marketplace, or hybrid) with search quality and agent consumability as the acceptance criteria. Search works on **metadata quality, not data quality** — a catalog over pristine data with thin metadata finds nothing.

## Core model to hold in your head

### Three browse dimensions (every design must serve all three)
| Dimension | Structure | Research question it answers |
|---|---|---|
| Vertical | Domains → subdomains → data sources → assets | "What eval corpora does the safety domain have?" |
| Horizontal | Lineage (ETL/ELT flow of whole assets) | "What raw crawls fed this curated set, and which checkpoints consumed it?" |
| Relational | Graph of semantic relations between parts of assets | "What else uses this entity-ID scheme / annotator pool / license?" |

Lineage extended to **checkpoints** is the research division's killer horizontal feature: dataset version → training run → model checkpoint, browsable both directions.

### Domains from knowledge, not from pipelines (the DDD caution)
Data-mesh practice borrows Domain-Driven Design for domain boundaries, but DDD was built for software, not for searchable organization: if catalog domains follow data flow (lineage strings of software components), the "vertical" browse collapses into a second lineage view — technically correct, conceptually confusing, and it will not deliver the total, searchable overview. Instead define domains information-science style: a group of people sharing **knowledge** (concepts and relations), **goals**, **methods**, and **communication** — e.g., "speech data", "safety evals", "web-scale text", regardless of which pipeline produced what. Choose **capabilities** (what is done — nouns: Collection, Annotation, Curation, Evaluation) or **processes** (how it is done — value-chain steps) as the top-level structure; never the org chart (it reorganizes constantly; domains must be stable landing zones). Mind each domain's **intension** (depth of subdomain hierarchy — match the experts' real granularity) and **extension** (breadth); metadata quality is then judged as **exhaustivity** (glossary/structure could describe the domain fully) × **specificity** (assets are actually tagged to that depth) — high exhaustivity with low specificity means search still fails.

### Role model (who keeps metadata alive)
| Role | Responsibility |
|---|---|
| Domain owner | Defines what belongs in the domain, assigns roles |
| Domain steward | Curates the domain, interviews incoming source owners, manages access |
| Data source owner | Owns an IT system / store feeding the catalog (e.g., the annotation platform) |
| Asset owner | Owns the data in the source; grants access on request |
| Asset steward | Practical curation of many assets (descriptions, tags) |
| Term owner / term steward | Own and manage glossary terms (domain or global) |
Map these onto the same researchers named as stewards in the sibling `research-data-governance` skill — one roster, two views. Every asset must carry all relevant roles; unowned assets are lifecycle risks the catalog surfaces.

### Glossary governance — three types, run simultaneously
| Type | Structure | Control | Use |
|---|---|---|---|
| Free glossary | Folksonomy (tags) | None — anyone tags | Long-tail, emergent vocabulary a central team would never predict ("hallucination-bait", "ocr-noisy") |
| Domain glossary | Taxonomy (hierarchy, optionally faceted) | Domain glossary team | Domain's formal self-description ("speech → conversational → multi-speaker"); facets (language × modality × license) power filtered search |
| Global glossary | Thesaurus (preferred term + variants/related/narrower/broader terms) | Central glossary team | Cross-domain concepts; synonym control so "dialogue"/"conversation"/"chat" resolve to one PT |
Strive for control *and* no-control at once: a fully controlled vocabulary looks clean but freezes learning; folksonomy tags reveal how users actually think, feeding taxonomy evolution. A glossary is not a data dictionary (field-level types live in contracts); it contextualizes assets into the division's knowledge.

### Marketplace vs catalog (the architecture decision)
| Concern | Traditional catalog | Data (mesh) marketplace |
|---|---|---|
| Metadata flow | **Push**: shipped to and duplicated in a central repository | **Pull**: fetched live from each dataset's own discovery API; marketplace stores only a 2-paragraph summary + links |
| Registration | Central team coaxes owners to submit and fix metadata | **Self-registration** by the producer, minutes to publish |
| Incentives | Incentive gap: disengaged owners, central team carries staleness (Conway's law clash) | Two-sided marketplace: producers publish because consumers find them; usage/feedback visible to producers |
| Freshness | Decays between sync jobs | As fresh as the product's own API |
| Search | Index over central metadata | NL/semantic search over vectorized summaries; detail resolved from the product live |
| Precondition | Works with dumb data sources | Requires datasets to expose standard discovery/observability interfaces (data products) |
Decision rule: if datasets are becoming products with self-describing APIs (the mesh path), build the **marketplace pattern** — window into the mesh, no metadata duplication. If most sources are passive buckets today, start catalog-style but adopt marketplace properties immediately: self-registration, producer-owned metadata, summaries-plus-links rather than full duplication. Hybrid is the honest state for most research divisions mid-transition.

**Non-leaky discovery is a hard boundary.** Authenticate before retrieval, filtering, ranking, autocomplete, graph traversal, and detail resolution. Partition indexes/embeddings by policy domain or apply identity-aware filters before candidate generation—not after results are ranked. Unauthorized users and agents must not learn asset names, summaries, license/PII flags, lineage, counts, or existence through search, vector similarity, errors, or timing.

### Search quality (define acceptance before building)
- **Recall** (find everything relevant) vs **precision** (find only relevant) — dataset discovery is recall-first at the browse stage (missing the one good corpus is costly), precision-first at the ranking stage. Measure both with a benchmark set of ~20 real research queries with known-correct answers.
- Support the three query patterns:
  - **Known-item** — "the RedPajama derivative v3"; needs exact-match on names, IDs, aliases.
  - **Exploratory** — "what German speech do we have?"; needs facets, glossary expansion, graph traversal.
  - **Verificative/compliance** — "everything containing annotator PII"; needs tag-complete metadata; this is also the legal-hold and inspection-support path.
- Ranking as a governance feedback loop: usage, satisfaction, and certification status boost rank; duplicates and unowned assets sink — the catalog quietly garbage-collects.
- Offer three search surfaces: simple search, faceted browse (from the domain taxonomies), and an advanced query language (IRQL/SPARQL-class) for power users and agents; teach users which fits which pattern.
- Instrument search: log zero-result queries and abandoned sessions — they are the backlog for glossary and metadata work.

### Agent-consumability requirements (first-class, not a bolt-on)
The ADP's agents are catalog users with no tolerance for tribal knowledge:
1. **Everything a UI shows must be API-readable**: search, browse, asset detail, glossary, lineage — machine endpoints with stable schemas (MCP-style tool surface over the catalog is the target interface).
2. **Addressability**: every asset resolvable by permanent URI to an aggregate root (docs, schema, SLOs, access) — agents chain discovery → contract → access without a human.
3. **Structured, standards-based metadata**: contracts as metadata source of truth; schema.org semantic tags on fields; sensitivity classes machine-readable so agents can self-filter what they may retrieve.
4. **Knowledge-graph readiness**: prefer a flexible, visual, extendable, queryable metamodel (knowledge-graph catalogs) so agents traverse relations ("datasets sharing this entity scheme") rather than keyword-match; the mesh-level graph can emerge from per-dataset semantic links instead of central modeling.
5. **Policy-partitioned vectorized summaries** for natural-language search — embed only approved metadata, bind each vector to enforceable access policy, and filter before similarity retrieval. Never place restricted summaries in a globally searchable index.
6. **Certification and SLO status inline** in results so agents (and ranking) can filter to trustworthy assets automatically.

### User groups (design for all three, sized honestly)
- **Analytics/research end users** — researchers hunting training/eval data; they deliver the catalog's ROI and their discovery continues *into* the data (EDA), so hand-off to query tools must be seamless.
- **Governance end users** — hunting confidential/sensitive data to protect it; need tag-complete verificative search.
- **Everyday end users** — over time the catalog trends toward company search engine (reports, SOPs, docs); plan for it, don't build for it first.
- **Agents** — treat as a fourth group with the strictest requirements (see above); an agent-usable catalog is automatically better for all humans.

## Workflow
1. **Inventory and users**: data sources, asset count, the three user groups (analytics/research, governance, everyday) plus agents; collect 20 benchmark queries from real researchers.
2. **Choose domain basis** (capabilities vs processes) and draft the domain map with the domain teams — never solo; validate intension depth with each domain's experts.
3. **Design the metamodel**: entities (domain, dataset, asset, term, person, checkpoint, training run), relations, and the lineage-to-checkpoint edge; prefer an extendable graph metamodel.
4. **Make the marketplace/catalog call** using the decision table; specify pull vs push per source class and the self-registration flow (summary + links, minutes not weeks).
5. **Assign roles** per the role model, reconciled with the governance steward roster; define the glossary plan (all three types, owners, promotion path folksonomy → taxonomy → thesaurus).
6. **Specify authorized search**: identity-aware filtering before retrieval/ranking, index partitioning, non-leaking errors, query patterns, facets, ranking signals, and recall/precision targets measured within each caller's authorized corpus.
7. **Specify the agent surface**: API list, addressing convention, metadata schemas, non-human identity and authorization model, and tests proving unauthorized metadata cannot enter results or embeddings.
8. **Pilot with two domains**, run the benchmark queries (human and agent), measure, then scale by self-registration — not by central data entry.

## Output spec
Deliver: (a) domain map + metamodel diagram description; (b) architecture decision record (marketplace/catalog/hybrid, pull-push matrix); (c) role assignment table; (d) glossary governance plan; (e) search spec with benchmark query set and recall/precision targets; (f) agent-consumability spec (endpoints, schemas, addressing); (g) pilot plan with success metrics (time-to-find, % assets self-registered, % assets fully role-assigned).

## Guardrails
- Never structure domains by org chart or by pipeline/lineage alone — stability and searchability, not reporting lines, define domains.
- No central metadata duplication without a stated staleness budget and sync ownership; prefer summaries-plus-live-links.
- Metadata quality is the search ceiling: block "index everything now, describe later" plans — undescribed assets pollute recall.
- Every asset ships with owners/stewards assigned or is flagged, not hidden; unowned data is a finding.
- Don't promise NL search as a substitute for glossary work — embeddings over bad summaries return confident junk.
- Controlled glossaries are still biased; keep the folksonomy channel open as the correction signal.

## Suggested effort
High — domain mapping workshops per domain, metamodel + architecture design, and a two-domain pilot before scale-out; the glossary and role assignments are ongoing operational work, not a project phase.
