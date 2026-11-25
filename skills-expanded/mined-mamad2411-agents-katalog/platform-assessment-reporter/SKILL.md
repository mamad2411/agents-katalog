---
name: platform-assessment-reporter
description: Turn platform and agentic-readiness assessment results into evidence-backed reports and executive visuals, including separate cited radar/spider maturity profiles for platform aspects, ASDLC paths, and Agentic Developer Portal readiness gates. Use whenever someone wants an assessment report, domain-by-stage maturity chart, evaluation ledger, exec readout, quadrant, platform-value radar, before/after impact view, or golden-path coverage map. Fires on phrasing like "build the report", "visualize the assessment", "show each domain's stage", "justify the maturity level", "radar chart of our platform", "where do we sit", or "make this presentable to leadership". Every result must trace to rubric checks, evidence citations, a source/model version, and confidence; qualitative or unobserved findings remain visibly distinct.
---

# Platform Assessment Reporter

## Purpose

Render the outputs of platform assessments — maturity results, ROI evidence, org diagnostics — as reports a leadership audience can act on: separate maturity radars, cited evaluation ledgers, a production-system quadrant, a six-vector value radar, golden-path coverage maps, and before/after ledgers.

For a full discovery engagement, consume the evidence catalog and three-part readout from `platform-maturity-discovery`: platform-engineering maturity, ASDLC maturity, and ADP readiness gates. Keep them separate; never average them into one score.

The skill's one non-negotiable rule: **visuals inherit the evidence discipline of the data behind them.** Every plotted point carries a metric, a source, a date, and a confidence tier. Where no measurable metric exists, the point is rendered and labeled as qualitative — visibly distinct from measured data. A chart that hides fuzziness is a lie with better production values.

Sibling skills feed this one: `asdlc-maturity-assessment` (level scores, path matrix), `platform-roi-scorecard` (cost/value numbers, benchmark calibration), `platform-org-design-advisor` (structure diagnostics). Assess first, then report. Client context: [YOUR ORGANIZATION / CLIENT].

## Core model

### 1. Evidence tiers — the confidence vocabulary

Every data point rendered anywhere gets exactly one tier:

| Tier | Definition | Visual encoding |
|---|---|---|
| **Measured** | System data pulled from tooling (VCS, CI/CD, tracker, cloud APIs) with a stated query and date | Solid fill, full opacity |
| **Surveyed** | Structured survey with cohort, n, date, observation window, and suppression rule stated | Solid fill, lighter shade, "cohort, n=X, survey MM/YYYY" footnote |
| **Estimated** | Derived arithmetic (e.g., hours-saved × rate) with stated assumptions | Outlined fill, assumptions footnoted |
| **Qualitative (fuzzy)** | Judgment, anecdote, or inherently unmeasurable dimension | Hatched/dashed rendering + explicit "qualitative" label on the axis or point |

Encoding rules: never render a Qualitative or Estimated point with the same visual weight as a Measured one. Never average tiers into a composite score without stating the mix (e.g., "composite of 4 measured, 2 qualitative axes"). Every chart ships with an evidence appendix table: axis → metric → source → date → tier.

For a maturity-radar point supported by several evidence tiers, encode the point using the **weakest evidence tier required to justify the claimed result**: Qualitative, then Estimated, then Surveyed, then Measured. Do not downgrade for optional corroboration that did not control the result; show the complete evidence-tier mix in the adjacent ledger. If the controlling evidence cannot be identified, encode the point as Qualitative.

### 2. Maturity radar profiles

Generate only the profiles supported by available formal outputs. Never combine these models into one radar or average their axes:

| Profile | Axes | Display scale | Formal result shown in ledger |
|---|---|---|---|
| **Platform engineering** | Investment, Adoption, Interfaces, Operations, Measurement | Provisional=0, Operational=1, Scalable=2, Optimizing=3 | CNCF-aligned stage per aspect from `platform-maturity-benchmark` |
| **Agentic delivery** | Retrieve, Implement, Validate, Promote, Deploy, Observe, Remediate, Dispatch | ASDLC Level 0-3; show Level 4 only as a labeled outlook ring, never as an achieved score | Level per path from `asdlc-maturity-assessment` |
| **Agentic Developer Portal readiness** | Organizational context, Platform capabilities, Deterministic delivery, Agent identity, Governed execution, Evaluation/observability, Human adoption/trust | Fail=0, Partial=1, Pass=2; render Unobserved as a gap or hollow point | Gate status for the named use case, not an enterprise maturity level |

Treat the numeric mapping as chart geometry only. Put the real stage, level, or status in the axis label, adjacent table, and accessible text. Do not calculate an overall radius, polygon area, or enterprise average.

Every profile requires an adjacent evaluation ledger:

| Field | Requirement |
|---|---|
| Domain/path/gate | Use the scorer's exact name |
| Formal result | Stage, level, or gate status; write Pending when the required scorer is unavailable |
| Display ordinal | State the mapping used for chart geometry |
| Evaluation score | Report `criteria met / applicable criteria`; list partial, contradicted, and unobserved checks separately. If the scorer does not define countable criteria, report evidence coverage instead of inventing a ratio |
| Justification | One concise claim tied to the controlling rubric requirement |
| Confidence | High/medium/low with the evidence-tier mix |
| Citations | Stable evidence IDs plus the rubric/benchmark source and version |

Assign a stage or level from the controlling rubric, not from the criteria ratio. The evaluation score explains the decision; it does not override mandatory gates or convert partial checks into fractional credit.

### 3. Production-system quadrant

A 2×2 diagnostic of how an organization produces software:

- **X axis — ownership:** fragmented ↔ concentrated (end-to-end)
- **Y axis — design:** implicit (tribal, negotiated) ↔ explicit (deliberate, documented)

| Quadrant | Traits | Failure mode |
|---|---|---|
| **Artisanal** (implicit + fragmented) | Informal coordination, diffuse responsibility, negotiation-driven | High variance in execution |
| **Hero-based** (implicit + concentrated) | Expertise islands, high individual ownership | Fragile scalability; bus-factor risk |
| **Bureaucratic** (explicit + fragmented) | Prescribed process, strong controls, weak accountability | Stable but slow; optimizes compliance over flow; decays quietly under pressure |
| **Platform** (explicit + concentrated) | Deliberate design, explicit interfaces, end-to-end ownership, continuous improvement | Target quadrant |

Most organizations oscillate among the three non-platform quadrants rather than sitting still. Placement is a diagnosis of the production system, not the people: organizations rarely fail from incompetence — the production system makes competence fragile.

**Evidence-backed placement rubric.** Score each axis 0–4 from at least two evidence points; below two, the placement is Qualitative and must be rendered as such.

*Design explicitness (Y):*
- % of delivery workflows with a written path definition or definition of done (Measured — repo/wiki audit)
- Policy-as-code coverage: % of policy checks enforced in pipeline vs. in review comments (Measured — CI config audit)
- Pipeline definitions version-controlled vs. UI-defined (Measured)
- Onboarding time to first meaningful PR (Measured — tracker/VCS)

*Ownership concentration (X):*
- CODEOWNERS / service-catalog coverage: % of repos/services with a named owning team (Measured)
- Bus factor on critical components: contributors covering 80% of commits (Measured — VCS)
- On-call rotation breadth vs. single-hero pattern (Measured — paging tool)
- % of incidents resolved by the owning team without escalation (Measured/Surveyed)

Caution: concentrated ownership scores high on X only when ownership is *team-level and end-to-end*. A bus factor of 1 is Hero-based concentration, not Platform concentration — check breadth before placing high-right.

### 4. Six-vector value radar

Radar/spider chart comparing the org (and optionally: target state, industry benchmark, before/after) across six value dimensions. Each axis scored 0–4, each with a defined metric set and an honest tier ceiling:

| Vector | Metric set | Best achievable tier |
|---|---|---|
| **Delivery velocity** | Deployment frequency, lead time for changes | Measured |
| **Outcome predictability** | Change failure rate; forecast-vs-actual delivery variance | Measured |
| **Operational resiliency** | MTTR, error-budget adherence, incident recurrence | Measured |
| **Maintenance efficiency** | KTLO share of engineering time, rework/revert rate, dependency currency (N-1 version %) | Measured/Surveyed (KTLO share usually survey or time-tracking) |
| **Organizational learning** | Postmortem completion + action closure rate, onboarding time trend, internal-docs contribution rate | Surveyed/Estimated — partially measurable proxies; the construct itself is soft. Flag axis as mixed-tier. |
| **Structural incentive** | Whether the system rewards platform use vs. bypass: golden-path adoption %, voluntary vs. mandated usage split | Qualitative with measurable fragments — default to Qualitative unless adoption telemetry exists |

Rendering rules: axes at different tiers get different stroke treatments (solid for Measured, dashed for Qualitative) and the legend says so. If comparing to an industry benchmark, state the survey year — benchmarks age. Do not plot a "target state" polygon as if it were data; label it target.

### 5. Golden-path coverage map

Per-path structural diagram for reporting platform completeness. Each golden path renders as a column: **Interface** (how it's invoked) → **Capability** (tools & resources; lifecycle & guardrails; abstraction promise — what detail the path commits to hiding) → **Output**, with shared **Identity** entering above and shared **Policies/State** below, and a continuous-improvement loop from outcomes back into the platform.

Report per path: definition exists (Y/N), invocation telemetry (Measured adoption %), validation/guardrail coverage, and output feedback wiring. Paths with no telemetry render hatched — "defined but unobserved."

### 6. Before/after ledger

Two-column table for any claimed improvement: metric, before (value + date), after (value + date), delta, tier, source. A before/after claim without a baseline date is an anecdote — render it in the Qualitative style or cut it.

### 7. Adoption trajectory panel

For roll-out reporting: S-curve expectation (slow MVP → ramp → saturation), plotted actual (users, voluntary usage share, services migrated — Measured), annotated interventions. Flag the known failure pattern: early demand tempting the team to abandon structured onboarding, after which learning stalls and the platform team decays into reactive support. Rhythm metric: onboarding-loop runs per quarter and cohort size — measurable and honest.

## Citation contract

Assign every evidence item a stable ID such as `E-014`. Cite each maturity claim and ledger row to one or more evidence IDs, then resolve them in an evidence appendix with source system, artifact or query, observation window, population, retrieval date, evidence class, collection method, and confidence. Cite public framework and benchmark sources separately with title, version/date, and URL.

Use redacted, durable references appropriate to the report medium:

- Markdown/HTML: linked footnotes or anchors from each ledger row to the evidence appendix.
- DOCX/PDF: numbered notes or endnotes plus page/section references where available.
- Slide deck: short evidence IDs on the slide and full citations in notes or an appendix.

Do not place private raw message or transcript text in a chart. Cite the approved aggregate query or redacted evidence record. If a citation cannot be shared with the report audience, mark it restricted and name the evidence custodian instead of silently dropping provenance.

## Minimum report package

- Executive summary with the decision, scope, observation window, and limitations.
- Separate maturity radar profiles for available platform, ASDLC, and ADP outputs.
- Adjacent evaluation ledger for every profile.
- Confirmed, contradicted, gap-filled, and unobserved findings.
- Priority gaps and sequenced roadmap.
- Evidence appendix, framework/benchmark bibliography, and reproduction note.
- Accessible data tables and text summaries for every chart.

## Workflow

1. **Intake.** Collect the three-part discovery readout and formal scorer outputs, including scorer/benchmark versions and rubric checks. Identify audience ([EXEC / PLATFORM TEAM / BOARD]) and decision the report should enable. Mark unavailable formal outputs Pending.
2. **Build the evidence and evaluation ledgers first.** Before any chart, map every candidate result to rubric checks, criteria met/applicable or evidence coverage, source, date, evidence tier, contradictions, confidence, and stable evidence IDs. Data with no source stays Qualitative or gets cut.
3. **Select visuals.** Use separate maturity radars for domain-by-stage profiles; quadrant for production-system framing; value radar for outcome dimensions; path map for platform completeness; ledger for ROI claims; trajectory panel for adoption. Skip a radar whose formal scorer is unavailable or whose axes would be majority unobserved.
4. **Encode axes.** Apply the display-only ordinal mappings above. Respect mandatory scorer gates, tier ceilings, and per-path/per-cohort variation. Never derive a formal result from polygon geometry.
5. **Render.** Use SVG/HTML for radars, Mermaid for supported quadrants/path maps, and Markdown/HTML tables for ledgers. Include axis-stage labels, model/version/date, legend, evidence IDs, and an accessible table/text equivalent. Use print-safe patterns as well as color.
6. **Run the citation pass.** Resolve every claim and plotted point to the evidence appendix and every framework claim to a versioned public source. Remove or label any unsupported assertion.
7. **Add the discovery appendix.** Include evidence coverage by signal domain and collection method, confirmed/contradicted/gap-filled findings, cohort perception gaps, missing-data limitations, and the seven ADP readiness gates.
8. **Run the fuzziness pass.** Check for points that look measured but are not, hidden unobserved axes, mixed cohorts, or a criteria ratio presented as a maturity score. Add a one-line “what we could not measure and why” note per chart.
9. **Deliver.** Include the minimum report package and a reproduction note so the next assessment can use identical queries, mappings, and rubric versions.

## Guardrails

- Never render a qualitative judgment in the same visual style as measured data — no exceptions for aesthetics.
- Never place platform aspects, ASDLC paths, and ADP gates on one polygon or average them into one maturity number.
- Never use polygon area, radius, or a criteria ratio to assign a formal maturity stage.
- Never composite mixed-tier axes into a single score without disclosing the mix.
- No quadrant placement from fewer than two evidence points per axis — render as Qualitative hypothesis instead.
- Benchmarks and surveys always carry their year and n. Vendor-published numbers are Qualitative regardless of how precise they look.
- Illustrative/hypothetical comparison polygons (target state, idealized platform) must be labeled as such — never presented as observed data.
- A missing baseline kills a before/after claim; report the after-value as a snapshot, not an improvement.
- Report what could not be measured. An all-solid chart of a low-maturity org is a red flag, not an achievement.
- Every formal result and plotted point must have an adjacent evaluation row and citations; otherwise leave it unplotted.

## Suggested effort

- **Quick readout** (existing assessment data, 1–2 visuals): low — evidence table + radar or quadrant.
- **Full report** (all five visual types + appendix): medium — requires complete sibling-skill outputs.
- **Recurring reporting program** (quarterly comparable series): high first cycle (reproduction notes, query library), low thereafter.
