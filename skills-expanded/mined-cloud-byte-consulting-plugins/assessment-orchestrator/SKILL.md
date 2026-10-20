---
name: assessment-orchestrator
description: >-
  Coordinate a platform-engineering and Agentic Developer Portal maturity
  assessment as permission-scoped increments run by different organizational
  roles, then merge the evidence into one auditable assessment state with three
  separate maturity readings. Use when users need an incremental or phased
  assessment, must split work across platform, security, FinOps, data, delivery,
  and leadership roles, need a read-only permissions plan, want to resume or
  reconcile partial assessment work, or ask "who needs to run what", "what access
  do we need", "we cannot access this system", "continue the assessment", or
  "merge these assessment results". This skill owns engagement sequencing,
  permission contracts, evidence-state handoffs, and synthesis coordination.
  platform-maturity-discovery owns collection and evidence quality;
  platform-maturity-benchmark and asdlc-maturity-assessment own formal scoring;
  platform-assessment-reporter owns presentation.
---

# Assessment Orchestrator

## Purpose

Run an assessment even when no participant can access every source. Divide work
by real permission boundaries, let authorized roles collect evidence without
moving raw data across those boundaries, and merge stable evidence records into
one audit trail. Missing access limits coverage; it never authorizes broader
collection or an invented score.

The assessment produces three separate outputs:

1. platform-engineering stages for five CNCF aspects;
2. ASDLC levels for eight agentic delivery paths;
3. seven use-case-specific Agentic Developer Portal readiness gates.

Never average or translate them into one maturity number. In this suite, ADP
means **Agentic Developer Portal**, not Agentic Developer Platform.

## Engagement model

### Scope increments by permission boundary

An increment is the largest assessment slice one role can complete with access
they already hold or can receive through a least-privilege read-only grant. If
roles or system boundaries differ, split an increment further. The catalog is a
starting point; the evidence contract is the invariant.

### Keep one canonical state and parallel deltas

The assessment lead owns `assessment-state.yaml`. A participant working
sequentially may append directly after loading the latest state. Parallel
participants emit `assessment-delta-<increment>-<date>.yaml`; they must not edit
the canonical file concurrently. The lead or I8 imports deltas, rejects duplicate
evidence IDs, and records the merge date. This prevents silent clobbering while
preserving an append-only audit trail.

### Separate findings from raw data

Raw exports, query results, pod inventories, billing details, and survey response
files stay inside the source owner's approved boundary. State contains only
minimized aggregate findings, stable source locators, dates, methods, confidence,
and restrictions. Do not include credentials, secrets, names, private message
text, or raw survey responses.

## Increment catalog

All system access is read-only. Check the root `ASSESSMENT-GUIDE.md` and current
provider documentation before requesting named roles or token permissions.

| ID | Increment | Typical operator | Minimum capability | Primary outputs |
|---|---|---|---|---|
| I1 | Repositories and delivery artifacts | Git organization reader | Selected repository list/content, PR metadata, rulesets/branch protection | Catalog, IaC, golden-path, ownership, agent-context, and interface evidence |
| I2 | CI/CD and delivery flow | Delivery/release engineer | Pipeline run/check metadata and deployment events; existing DORA tool viewer when available | Delivery-path and Measurement evidence |
| I3 | Kubernetes and platform infrastructure | Platform engineer | `get/list/watch` only for approved inventory, policy, workload, quota, node, and CRD resources; observability viewer | Infrastructure, tenancy, self-service, reliability, and Operations evidence |
| I4 | Cloud cost and FinOps | FinOps/cloud analyst | Cost and billing viewer at the approved scope; Kubecost/OpenCost viewer | Investment, allocation, demand, and unit-cost evidence |
| I5 | Security and agent governance | Security/identity engineer | Security findings, approved agent/tool inventory, non-human identity metadata, and audit-event viewer | Identity, governed execution, control, exception, and audit evidence |
| I6 | Data platform | Data platform owner | Catalog/metastore, lineage, schema, quality-result, and pipeline metadata viewer | Data product, context, discoverability, and reproducibility evidence |
| I7 | Surveys and interviews | Platform product/assessment lead | Approved authority to distribute the survey and conduct interviews; no communication-content access by default | Aggregate adoption, trust, friction, cognitive-load, and intent evidence |
| I8 | Reconciliation and synthesis | Assessment lead | Canonical state, deltas, scorer versions, and approved evidence summaries | Coverage, contradictions, three separate readings, report input, and roadmap |
| I9 | Cloud estate (Azure) | Platform engineer | Azure `Reader` at approved scope: Resource Graph, azqr, Governance Visualizer viewers; `aztfexport --hcl-only`/Bicep decompile with no state writes | Estate inventory, IaC-coverage ratio, governance/policy map, best-practice findings, and a workload disposition map (wrap/refactor/leave/retire); runs via `azure-platform-engineering:azure-estate-assessor` |

Never request `cluster-admin`, repository write, billing contributor, secret
read, mailbox/chat content, or raw production/customer data for the default
assessment. If a narrower question genuinely needs sensitive content, stop until
the charter names the purpose, population, approver, minimization, retention, and
analysis boundary.

## State contract

Use stable increment-prefixed evidence IDs such as `I3-E017` so parallel work
cannot collide. A minimal state looks like:

```yaml
assessment:
  organization: <name>
  scope: <business units, value streams, repositories, clusters>
  started: <date>
  models:
    platform: cncf-platform-maturity-<version>
    asdlc: asdlc-<version>
    adp_readiness: adp-seven-gates-<version>
privacy:
  classification: restricted
  raw_evidence_owner: <role or system, never a person in reports>
  deletion_date: <date>
increments:
  - id: I3
    run_by_role: platform-engineer
    completed: <date>
    access_confirmed: [k8s-inventory-read, metrics-viewer]
    access_denied: [cloud-cost-viewer]
evidence:
  - id: I3-E017
    increment: I3
    targets:
      - {model: platform, domain: Operations}
      - {model: adp_readiness, domain: Platform capabilities}
    evidence_class: Derived       # Behavioral | Derived | Attested
    collection_method: computed-cross-reference
    evidence_tier: Measured       # Measured | Surveyed | Estimated | Qualitative
    finding: "14 of 17 eligible namespaces lack an approved quota profile"
    source:
      system: kubernetes-api
      locator: "approved aggregate query I3-Q04"
      retrieved: <timestamp>
      observation_window: <window or snapshot>
    confidence: high
    restriction: aggregate-only
reconciliations: []               # confirmed | contradicted | gap-filled
open_gaps:
  - target: {model: platform, domain: Investment}
    reason: "I4 cost access pending"
readings:
  platform: pending
  asdlc: pending
  adp_readiness: pending
```

Evidence is immutable after merge. Correct an error with a new record containing
`supersedes: <evidence-id>` and a reason. Record exact model versions and do not
mix versions inside one assessment cycle.

## Reconciliation contract

Use the evidence classes and collection methods from
`platform-maturity-discovery`. For every material claim:

- **Confirmed:** independent sources support the same interpretation.
- **Contradicted:** sources materially disagree; preserve both, reduce
  confidence, and identify the evidence needed to resolve the disagreement.
- **Gap-filled:** one class answers a question another class cannot observe;
  preserve the coverage limitation.

Do not automatically average conflicting readings or assign the lower numeric
value. Send the full contradiction to the controlling scorer. If its rubric
cannot resolve the result, report partial, unobserved, or Pending as appropriate.

## Workflow

1. **Charter.** Record the decision, scope, models, systems, populations,
   observation windows, approvals, evidence owners, retention, and prohibited
   uses. Stop on unclear authority for sensitive sources.
2. **Plan increments.** Map current access to I1–I9. Start any authorized
   increment now; create an access-gap queue for the rest. Prefer bounded exports
   when a source owner cannot grant direct access.
3. **Collect.** Invoke `platform-maturity-discovery` within each increment. Use
   first-party read-only APIs, predetermined questions, published denominators,
   and minimized aggregate findings.
4. **Close the increment.** Emit the delta or updated state, a one-paragraph
   coverage/confidence summary, and a handoff naming the next increment, operator
   role, exact access gap, and state location.
5. **Merge.** Verify IDs, scope, source dates, restrictions, and model targets.
   Append new records, reconcile claims, and preserve unresolved gaps.
6. **Synthesize.** I8 can issue a partial coverage report after two increments,
   but formal results require the evidence prerequisites of each controlling
   scorer. Run `platform-maturity-benchmark`, `asdlc-maturity-assessment`, and the
   ADP gates separately; leave unsupported results Pending or unobserved.
7. **Report and roadmap.** Send the three readings and evidence ledger to
   `platform-assessment-reporter`; send capability gaps to `idp-adp-architect`.
   Keep unresolved access and evidence gaps for the next cycle.

## Privacy rules for I7 and communications

- Select the smallest approved instrument that closes the evidence gap:
  `maturity-survey-instrument.md` for the core survey,
  `idp-adp-maturity-survey-by-role.md` for role-specific distribution, or the
  relevant section of
  `methodology-specific-confirmation-gap-fill-questionnaires.md` for a targeted
  methodology check. Do not issue all instruments by default.
- Preserve wording, cohort definitions, response rate, and suppression rules
  across cycles. Record which instrument version and question IDs were used.
- Aggregate to team level or higher and suppress cohorts below the approved
  threshold.
- Keep raw responses with the survey owner; state receives counts and themes.
- Do not infer intent from tone, rank people, or use message volume as output.
- In applicable jurisdictions, complete privacy-impact and worker-representation
  review before any email, chat, meeting, or transcript analysis.
- Redact direct identifiers inside the approved boundary before external LLM use.

## Output contract

Every increment returns exactly:

1. an assessment delta or updated canonical state;
2. a short coverage, finding, and confidence summary;
3. a handoff block with the next role and minimum access gap.

I8 additionally returns separate platform, ASDLC, and ADP ledgers; coverage and
contradictions; stable evidence citations; a reporter-ready summary; and a
sequenced roadmap. A partial synthesis is valid, but it must name every Pending
or unobserved result.

## References

- [references/maturity-survey-instrument.md](references/maturity-survey-instrument.md)
  — concise core CONFIRM/GAP-FILL survey and analysis contract.
- [references/idp-adp-maturity-survey-by-role.md](references/idp-adp-maturity-survey-by-role.md)
  — extended I7 instrument segmented for engineers, technical leads, managers,
  directors, and executive leadership.
- [references/methodology-specific-confirmation-gap-fill-questionnaires.md](references/methodology-specific-confirmation-gap-fill-questionnaires.md)
  — targeted prompts for unresolved CNCF, Microsoft, DORA, SPACE, Cortex,
  OpsLevel, CSA MCP, agent-instruction, and Team Topologies evidence gaps.
- [references/research-alignment.md](references/research-alignment.md) — source
  stance, retained research mechanics, rejected combined-score proposals, and
  primary references.
- [references/idp-adp-maturity-assessment-research.md](references/idp-adp-maturity-assessment-research.md)
  — user-supplied background research. Read it for framework context and source
  leads only; its ADP terminology and unified scoring proposal are not
  controlling in this repository.

## Guardrails

- No write permission, active scan, remediation, survey distribution, or message
  access merely because the assessment is running; each action needs its own
  authority.
- No formal score from a collection increment or from survey evidence alone.
- No single enterprise average or unified platform-and-agent maturity level.
- No individual name, productivity score, sentiment score, or disciplinary use.
- No maturity proof from file, policy, portal, license, or tool presence alone.
- No assumption that a missing signal means missing behavior; record visibility.
- No raw evidence copied across a permission boundary.
- Keep Internal Developer Portal, Internal Developer Platform, and Agentic
  Developer Portal distinct in every artifact.
