---
name: research-data-governance
description: Design right-sized research-data governance with steward roles, a lightweight council, policy-as-code, and certification that distinguishes hard-stop security/legal failures from visibility-only quality gaps. Use for governance operating models, data stewards, global-versus-local rules, certification, policy automation, data-mesh maturity, governance bottlenecks, approval queues, or governance theater.
---

# Research Data Governance

## Purpose
Design governance that makes research data safe, interoperable, and trustworthy **without** becoming the bottleneck that manual, centralized validation always becomes at scale. Governance's original meaning is "to steer a vessel," not "to rule with authority" — the deliverable is an operating model where policy *definition* is centralized and lightweight, policy *enforcement* is automated and embedded in each dataset, and the humans involved are existing researchers wearing steward hats, not a new approval bureaucracy. Risk is managed early and throughout via automation, not late via review meetings. (Dataset-level compliance evidence comes from the sibling `data-product-reviewer` skill's scores.)

## Core model to hold in your head

### The governance spectrum (place the org, then blend)
| | Lightweight council (Maffeo-style) | Federated computational (mesh-style) |
|---|---|---|
| Decision-making | Cross-functional council of stewards, chaired; framework + roadmap | Federation of domain data-product owners + platform owners; global rules minimized |
| Enforcement | Human review, standards documents, training | Policy-as-code and standards-as-code executed by the platform inside each dataset at build/deploy/access time |
| Control style | Approve projects and tools | Certification: producers self-certify against centrally defined policies; status published via API |
| Scales by | Adding stewards and meetings | Adding automated policies; governance invisible in the optimal state |
| Fails as | Council bottleneck, slow queues | Under-invested platform → policies exist on paper only |

**Recommended blend for a research division**: council-light for the human layer (a small steward council that defines policy and adjudicates edge cases), computational for the enforcement layer (certification checks in CI, policies embedded per dataset). Researchers keep shipping; the platform says no, rarely and automatically.

### Steward taxonomy — mapped onto existing researchers
Stewards are found, not hired: they already know the stack and the data. Split **business stewards** (own meaning, classification, taxonomy for their domain's data — e.g., the lead of the annotation program stewards label semantics) from **technical stewards** (own systems, pipelines, and modeling — e.g., the platform engineer who owns the Iceberg catalog). Council roles, each aligned to a framework area and fillable part-time:

| Role | Owns | Research-division mapping |
|---|---|---|
| Council chair | Strategy, role assignment, cross-org representation, defines "quality data" | Head of data/research infrastructure |
| Security steward | Sensitivity classifications, access policy, audit posture, reviews new tools | Platform/security engineer |
| Ethics & transparency steward | Compliance standards for collection/use, documented decision rationale, license and consent posture of corpora | Senior researcher with review-board experience |
| Documentation steward | Definitions, dataset-card standards, the documentation repository, dictionaries/glossaries | Research engineer who already writes the docs |
| Compliance steward | Regulatory tracking (data-protection law, model-training provenance rules), interprets law into policy | Legal/ops partner; can double with ethics in small orgs |
| Domain stewards (business + technical, per domain) | Local rules, quality, access grants for their datasets | The researchers producing each corpus |
One person may hold two roles in a small division; every framework area must have exactly one accountable name.

### Global vs domain-local rule split
Minimize global rules relentlessly — each one adds friction everywhere; implement every one you keep as automated platform capability:

| Global (all datasets, platform-enforced) | Domain-local (each producing team decides) |
|---|---|
| Sensitivity classification scheme + enforcement; PII handling | Schema and modeling of their datasets |
| Discovery/observability/SLO API standards; addressing convention | Quality thresholds beyond the global floor; SLO targets |
| Contract requirement at cross-team boundaries; semver breaking-change policy | Timeliness/freshness commitments (the collecting team knows the sensor) |
| Identifier/polyseme standards for cross-corpus join; lineage emission | Curation methods, dedup strategy, annotation guidelines |
| License/provenance recording; legal-hold and retention floors | Internal zone layout, tooling choices within platform-supported set |
| Ownership heuristics for new/aggregate datasets | Local access grants within global policy |

### Certification, not gatekeeping
Replace pre-publication approval with **governance-by-certification** — like UL/CSA marks for physical products: the standard is central, the attestation is the producer's.
- The center defines policies; each dataset team implements, attests, and **publishes certification status** through a standard interface (`/certify/status` → OK / NOT COMPLIANT; `/certify/report` → per-policy detail).
- Data contracts inserted between interface and data are the natural enforcement point — certification checks largely *are* contract checks running in CI.
- Split certification failures by policy class. Noncritical quality/documentation failures are visibility-based (flagged, ranked down, beta-only). Security, access-control, privacy/PII, license/provenance, legal-hold, retention, consent, and eval-contamination failures are hard stops that block publication, access expansion, and egress until remediated or formally waived by the accountable authority. Exploratory work may remain in a quarantined restricted zone; it is never discoverable as approved data.
- Prefer **feedback loops over control structures**: don't pre-approve datasets to prevent duplication — let self-registration + usage/satisfaction telemetry rank duplicates down and nudge owners to prune (automated garbage collection). Balancing loops degrade the redundant; reinforcing loops ("success to the successful") promote the useful — and need an upper-bound leverage point (lead-time-to-change ceilings) so winners don't bloat into god-datasets.
- Pair **local incentives** (dataset-user satisfaction and growth) with **global incentives** (adoption of global policies counts in the steward's success measures); without the global half, policy work always loses to feature work.

### Six-step bootstrap sequence
1. **Write the data mission statement** — one/two sentences deriving from the division's research mission ("we govern data to maximize trustworthy training signal per GPU-hour while minimizing legal and ethical harm"). Every later dispute maps back to it.
2. **Adopt the framework** — the areas the council owns: transparency & ethics, trust & security, quality, documentation, training & enablement, culture & communication, compliance. Each area gets a steward (step 3) and a policy owner.
3. **Select stewards** — inventory who already owns which data de facto; name business + technical stewards per domain and fill the council roles from the taxonomy above. Put stewardship in role descriptions and evaluations so the work is recognized, not charity.
4. **Stand up the council** — chair, cadence (biweekly, 45 min), decision log kept by the documentation steward, explicit remit: define global policies, adjudicate ownership of aggregates, tune incentives. The council decides *rules*, never individual dataset releases.
5. **Automate the first policies** — pick 3–5 global rules and implement them as code in the platform (sensitivity-tag lint, contract-required check, license-field check, contamination gate). Certification goes live when the checks do, in early days harvesting checks that pioneer teams already built.
6. **Operate and mature** — measure fitness functions (lead time for a dataset to adopt a new policy; % datasets certified; time-to-access for consumers; council decision latency), review quarterly, and prune rules that automation can't enforce or that nobody has violated in a year.

### Maturity anchoring (score honestly, target one level up)
- **Data Mesh CMM**: Initial (ad hoc PoCs) → **Data-as-a-product** (owned, contracted, discoverable datasets) → **Manufactured** (templated factory production of datasets) → **Governed** (certification replaces top-down governance) → **Innovating** (data products drive research strategy). Most research divisions should target Data-as-a-product, then Governed; skipping to certification without contracts in place fails.
- **Enterprise data maturity** (context check): Reactive (spreadmarts) → Informative (centralized) → Predictive (cloud, ML-integrated) → Transformative (any data, self-service). Governance design must match the stage — federated computational governance presumes at least Predictive-stage engineering practice (CI/CD, APIs, modern stack).

### Anti-patterns (name them when seen)
- **Council bottleneck** — council approving individual datasets/tools; queues form; researchers route around it (shadow data). Fix: council sets rules; automation applies them.
- **Governance theater** — policies documented, nothing enforced or measured; certification badges without checks behind them.
- **Canonical-model mandate** — one global schema/definition for contested terms ("document", "session"); use bounded contexts and translation instead.
- **KPI inversion** — counting datasets or policies as success; measure usage links, policy-adoption lead time, and consumer trust instead.
- **Governance as IT-only initiative** — parallel to the research org rather than embedded in it; stewards must be the researchers, not proxies.
- **Premature globalization** — promoting a local rule to global before two domains actually need it.

### Signals the design is working (check at each quarterly review)
- Time from "dataset ready" to "published and certified" is measured in hours, not weeks.
- The council's decision log contains rules and ownership calls, zero individual dataset approvals.
- Policy-adoption lead time falls with each new policy (the platform is absorbing the work).
- Shadow datasets (data shared outside the platform) are shrinking, not growing — the sanctioned path is the easy path.
- At least one global rule has been *retired* — governance that only accretes is calcifying.

## Workflow
1. **Assess**: current maturity (both ladders), existing de facto stewards, current friction points (interview 3 producers + 3 consumers: where do requests queue?).
2. **Place the org on the spectrum** and record the blend decision with rationale tied to research-velocity constraints.
3. **Run the six-step bootstrap**, producing the mission statement, framework-to-steward mapping table, council charter, and the first policy-as-code list with owners.
4. **Draw the global/local split** for this org — start from the table, cut anything without a named cross-domain need.
5. **Design certification**: classify every policy as hard-stop or visibility-only; define check implementation, accountable waiver authority and expiry, status interface, quarantine behavior, visibility consequences, and incentive wiring.
6. **Define fitness functions** and the quarterly review that tunes rules, incentives, and council scope.

## Output spec
Deliver: (a) governance design doc — spectrum placement, blend rationale, global/local rule table; (b) steward roster mapping named people to roles and framework areas; (c) council charter (remit, cadence, decision log location, what it explicitly does NOT decide); (d) certification spec (policies, checks, interface, consequences); (e) bootstrap plan with the six steps dated; (f) fitness-function list with measurement sources.

## Guardrails
- Never design a model where a human approval sits between a researcher and publishing an exploratory dataset — gates apply at cross-team consumption boundaries only.
- Every global rule must ship with (or name) its automated enforcement; a rule with no check is a request, and the doc must label it as such.
- No steward role without a named person, and no person without the role in their evaluation — unfunded mandates are how councils die.
- Don't copy an enterprise governance framework wholesale; anything not traceable to the data mission statement gets cut.
- Score maturity on evidence, not aspiration, and never recommend Governed-level certification to an org without working contracts (Data-as-a-product level).
- Keep the council small (5–8); bigger councils meet more and decide less.

## Suggested effort
High — assessment interviews + design workshop + bootstrap plan; expect the six steps to span a quarter, with steps 1–4 in the first month and certification (step 5) landing with the first automated checks.
