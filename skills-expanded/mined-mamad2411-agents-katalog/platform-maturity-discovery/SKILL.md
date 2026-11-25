---
name: platform-maturity-discovery
description: Discover evidence of an organization's maturity toward platform engineering and an Agentic Developer Portal (ADP) by triangulating emails and chat, meetings, work items, code and repositories, CI/CD, infrastructure and cloud systems, service telemetry, documentation, and developer sentiment toward automation. Use for platform maturity discovery, organizational sensing, ADP readiness, current-state assessments, evidence plans, connector mapping, interviews or surveys, developer experience, workflow friction, manual toil, automation adoption, shadow AI usage, or roadmap baselining. Produces a privacy-bounded evidence catalog, confidence-scored signal matrix, platform and ASDLC maturity inputs, ADP readiness gates, contradictions, and a phased roadmap. Never use it to surveil or score individuals.
---

# Platform Maturity Discovery

## Purpose

Establish how an organization actually builds and operates software before prescribing a platform or ADP. Gather behavioral and human evidence across the organization, reconcile contradictions, and produce three separate readings:

1. platform-engineering maturity;
2. agentic software-delivery maturity;
3. readiness for an Agentic Developer Portal.

This skill owns discovery and evidence quality. Full scoring uses `platform-maturity-benchmark` from the separate `adp-enablement` plugin and `asdlc-maturity-assessment` from this plugin, then hands the result to `idp-adp-architect`. Check those dependencies at intake. If a scorer is unavailable — including when this skill is uploaded to Perplexity by itself — deliver the evidence package, aspect/path coverage, qualitative hypotheses, and ADP gates, but leave the missing formal score unassigned.

## Terminology and scope

- **Internal Developer Portal** — a human-facing interface: catalog, documentation, scorecards, templates, search, and self-service entry points. It is one interface over platform capabilities, not the whole platform.
- **Internal Developer Platform** — the capabilities and orchestration behind the interfaces: APIs, pipelines, infrastructure, policy, identity, observability, and support model.
- **Agentic Developer Portal (ADP)** — the interaction, discovery, orchestration, and governance surface through which human and agent users consume organizational knowledge and platform capabilities. It includes portal experiences but also machine interfaces, agent identity, governed execution, evaluation, audit, and feedback loops.

Avoid the ambiguous abbreviation **IDP** in deliverables; write “Internal Developer Portal” or “Internal Developer Platform” in full. In this suite, **ADP means Agentic Developer Portal**.

## Discovery doctrine

### Observe behavior, not aspiration

Policies, architecture diagrams, and executive interviews describe intent. Repositories, work queues, deployment events, infrastructure state, support demand, communication patterns, and practitioner sentiment reveal the operating system people actually use. Score current behavior; record planned work separately.

### Triangulate every material finding

Use three evidence classes:

- **Behavioral:** events or configuration from systems of record — strongest.
- **Derived:** a reproducible calculation from behavioral data.
- **Attested:** survey, interview, sensing session, or document — necessary for experience and intent, but weaker alone.

Also tag the collection method as **static scan**, **runtime/API observation**, **computed cross-reference**, or **human sensing**. Evidence strength depends on the question: prefer static or runtime evidence for structural facts, and use attested evidence for intent, trust, and adoption motivation. Do not apply one numerical weight across every question.

A high-confidence maturity finding requires behavioral evidence plus an independent corroborating source. One source is a lead, not a conclusion. Reconcile each material finding as **confirmed**, **contradicted**, or **gap-filled**. Preserve contradictions as findings; do not average them away.

### Measure systems, never people

Assess queues, paths, team interfaces, controls, and aggregate experience. Do not rank employees, infer motivation from private messages, identify “low performers,” or use communication volume as productivity. Sentiment is valid only in aggregate and with enough context to protect respondents.

## Signal map

| Domain | Evidence sources | Useful signals | Do not infer |
|---|---|---|---|
| Communication and knowledge | Email/chat themes, docs, wikis, search logs, support channels | Repeated how-to requests, approval hops, knowledge gaps, shadow workflows, durable decision records | Productivity from message counts; intent from isolated messages |
| Meetings and collaboration | Calendars, agendas, transcripts where authorized, decision logs | Coordination load, recurring operational meetings, approval latency, cross-team dependencies, repeated incident themes | Meeting attendance as contribution; sentiment from tone alone |
| Work demand and flow | Jira, Azure Boards, GitHub Issues/Projects, ServiceNow | Queue time, blocked reasons, handoffs, toil share, request recurrence, rework, unmet self-service demand, agent-linked work | Story points across teams as comparable productivity |
| Code and delivery | Repositories, ownership, PRs, CI/CD, releases, test and policy results | Traceability, automation coverage, review latency, pipeline reliability, catalog completeness, template provenance, agent-instruction quality, security gates, agent attribution | Lines of code or commit volume as value; maturity from file presence alone |
| Infrastructure and operations | Cloud inventory, Kubernetes, IaC state, CMDB, observability, incidents, costs | IaC coverage, unmatched live resources, configuration drift, provisioning lead time, self-service coverage, reliability, fleet currency, cost attribution | Maturity from tool presence without adoption or outcomes; unmanaged resources and configuration drift as the same condition |
| Developer experience and sentiment | Anonymous surveys, standardized interviews, sensing sessions, retrospectives, onboarding studies | Trust in automation, perceived usefulness, friction, psychological safety, willingness to delegate, bypass reasons, fear and training needs | Organization-wide sentiment from a vocal minority |
| Agent and governance evidence | Approved-tool inventory, agent identities, session logs, tool calls, sandboxes, evals, policy decisions, audit trails | AI-stance clarity, inventory coverage, scoped identity, governed execution, deterministic validation, exception rates, acceptance/rework, shadow-agent usage | Safe autonomy from license adoption or demo success |

Book-informed discovery methods reinforce this map: use standardized interview questions, group sensing sessions, developer surveys, usage analytics, ticket-flow timing, operational metrics, and continuous feedback. The book does not define an ADP or a cross-system discovery architecture; this skill extends those methods into an evidence model for agentic readiness.

For the framework crosswalk, scanner design, survey pattern, and source cautions synthesized from the user-provided maturity research, read [references/discovery-research-crosswalk.md](references/discovery-research-crosswalk.md). Treat that research as a question and signal catalog, not as authority for a combined maturity score.

### Connector plan

Map each source to the organization's first-party, read-only API or connector before collection:

| Signal | Preferred surfaces |
|---|---|
| Email, chat, calendar, meetings, documents | Microsoft 365 or Google Workspace organizational APIs/connectors; aggregate metadata first, content only when authorized |
| Work and service demand | Jira/Atlassian, Azure Boards, GitHub Issues/Projects, ServiceNow |
| Code, ownership, and review | GitHub, GitLab, Azure Repos, repository rules and audit APIs |
| Build, test, deploy, and policy | GitHub Actions, Azure DevOps Pipelines, GitLab CI/CD, deployment and artifact systems |
| Infrastructure, reliability, and cost | Cloud-provider APIs, Kubernetes APIs, IaC state, observability, incident, CMDB, and cost systems |
| Agent behavior | Approved agent audit/session telemetry, non-human identities, tool-call logs, eval results, and commit/PR attribution |
| Sentiment | Anonymous survey tooling plus standardized interviews or sensing sessions |

Verify connector availability, license requirements, permissions, retention behavior, and field semantics at engagement time. If a surface is unavailable, document the blind spot and use a bounded export or representative sample; never silently substitute self-report for missing behavioral evidence.

## Core measures

Use a stable observation window — normally the last 90 days plus a 12-month trend where available. Publish every definition and denominator.

- **Queue ratio** = waiting time / total lead time.
- **Handoff density** = ownership or system-boundary transitions / completed work item.
- **Manual-toil share** = recurring manual operational work / total sampled operational work.
- **Self-service completion** = successful platform requests without human intervention / eligible requests.
- **Golden-path adoption** = eligible new workloads using a supported path / eligible new workloads.
- **Unmet self-service demand** = recurring eligible platform requests still requiring human fulfillment / recurring eligible platform requests.
- **Unmatched-live-resource ratio** = sampled live resources with no authoritative IaC or state match / sampled live resources; report configuration drift separately.
- **Path completion** = completed path executions / started executions; segment failures by stage.
- **Automation acceptance** = accepted automated or agent outputs / reviewed automated outputs; pair with rework and escaped-defect rates.
- **Shadow-automation gap** = attested automation use not visible in approved telemetry / attested total use.
- **Agent-context coverage** = eligible repositories with current, substantive, tested agent instructions / eligible repositories.
- **Agent-tool inventory coverage** = discovered agent or MCP tool configurations matched to the approved inventory / discovered configurations.
- **Knowledge findability** = sampled questions answered from maintained sources without synchronous escalation / sampled questions.
- **Sentiment delta** = change in matched, anonymous survey items over time; never compare differently worded surveys as a trend.

Counts are not outcomes. Pair every adoption or activity measure with quality, reliability, experience, or business impact.

## Maturity readout

Do not collapse the assessment into one average.

### 1. Platform-engineering maturity

Feed the evidence into `platform-maturity-benchmark` and report its five aspects independently: Investment, Adoption, Interfaces, Operations, and Measurement. An Internal Developer Portal is evidence only for Interfaces; it cannot by itself prove platform maturity.

Standalone fallback: for each aspect, report **evidence sufficient / partial / unobserved** and a clearly labeled qualitative stage hypothesis only when evidence supports one. Do not calculate a percentile or claim a CNCF stage without the scorer and its source-versioned benchmark.

### 2. Agentic delivery maturity

Feed path-level evidence into `asdlc-maturity-assessment`. Score who initiates and executes work, how identity is represented, how validation loops operate, what humans review, and whether production evidence supports the claimed autonomy level.

Standalone fallback: organize evidence against the retrieve, implement, validate, promote, deploy, observe, remediate, and dispatch paths, but leave the ASDLC level unassigned. Do not reconstruct the rubric from memory.

### 3. ADP readiness gates

Mark each gate **pass / partial / fail / unobserved**, with evidence and confidence:

1. **Organizational context** — authoritative, current knowledge is searchable and machine-consumable.
2. **Platform capabilities** — repeatable capabilities have governed APIs or executable paths, not portal-only buttons or tickets.
3. **Deterministic delivery** — CI/CD, tests, policy, promotion, rollback, and environment provisioning can govern agent-volume work.
4. **Agent identity and authorization** — non-human actors are attributable, scoped, short-lived, and revocable.
5. **Governed execution** — isolated workspaces, network/tool boundaries, secrets handling, quotas, and concurrency controls exist.
6. **Evaluation and observability** — output quality, agent actions, cost, failures, and exceptions are measured and auditable.
7. **Human adoption and trust** — practitioners understand the automation, see value, can challenge it safely, and have a feedback and escalation route.

The ADP is ready for a use case only when every gate required by that use case passes. Report partial readiness by path or cohort; never convert the gates into a misleading enterprise-wide percentage.

## Privacy and authority boundary

Before collection, write a discovery charter covering purpose, approved systems, population, time window, fields, retention, access, and intended decisions. Confirm legal, HR, privacy, security, labor/works-council, and data-owner requirements where applicable. Determine whether a jurisdiction-specific privacy impact assessment or worker-consultation process is required; do not treat the skill as legal advice.

- Collect metadata and aggregates before content; collect content only when necessary and explicitly authorized.
- Use least-privilege, read-only access and query only in-scope populations and dates.
- Minimize, redact, and aggregate personal data; suppress small groups that could identify individuals.
- Redact names and direct identifiers inside the approved ingestion boundary before sending excerpts to an LLM or external analysis service.
- Separate raw evidence from assessment outputs; restrict raw evidence and set a deletion date.
- Record connector visibility gaps, telemetry opt-outs, and sampling bias.
- Give practitioners a confidential way to provide sentiment and a route to challenge findings.
- Never use this workflow for covert monitoring, employee discipline, individual performance evaluation, or inference of protected characteristics.

## Workflow

1. **Charter the discovery.** Define the decision to support, assessment boundary, populations, systems, observation window, privacy approvals, and data-retention plan. Stop if authority for sensitive sources is unclear.
2. **Map the organization and systems.** Identify business units, product teams, platform/enabling/security/operations teams, critical value streams, toolchain, infrastructure estate, and systems of record. Record connector and sampling gaps.
3. **Write discovery questions.** For each maturity aspect and ADP gate, state the question, expected evidence, source, calculation, and confidence rule before collecting data. Tag human questions **CONFIRM** when they test an observed signal and **GAP-FILL** when the answer cannot be observed reliably.
4. **Collect behavioral evidence.** Prefer first-party, read-only connectors or APIs. Separate static repository/configuration scans, runtime/API inventories, and deterministic cross-references such as IaC-to-live-resource reconciliation. Pull work-flow events, CI/CD configuration, deployment and incident events, platform usage, infrastructure state, cost and reliability data, and approved aggregate communication/meeting metadata.
5. **Collect human evidence.** Use one anonymous practitioner survey plus standardized interviews or sensing sessions. Sample platform users, bypassers, platform staff, security, operations, and leaders. Keep core questions and observation windows consistent across cohorts; compare perception gaps without exposing small groups.
6. **Normalize and triangulate.** Redact before qualitative extraction, use a constrained evidence schema, build the evidence catalog, calculate the core measures, and grade provenance and completeness. Classify findings as confirmed, contradicted, or gap-filled. Investigate material mismatches — for example, complete catalog metadata alongside low catalog trust or fast pipeline telemetry alongside widespread reports of slow delivery.
7. **Produce the three readings.** Check scorer availability, then run `platform-maturity-benchmark`, `asdlc-maturity-assessment`, and the ADP readiness gates. If either scorer is unavailable, use its standalone fallback and label the formal score pending. Preserve per-team and per-path variation; do not average away weak areas.
8. **Prioritize the roadmap.** Convert evidence gaps and failed gates into sequenced capabilities. Start with measurement and the most repeated high-friction path; define owner, target cohort, success measure, control boundary, and review date for each milestone.
9. **Report and dispose.** Deliver the evidence-backed readout through `platform-assessment-reporter`, publish limitations and confidence, obtain stakeholder challenge, and delete raw discovery data on schedule.

## Deliverables

- Discovery charter and authority/privacy boundary.
- Organization, value-stream, and systems-of-record map.
- Evidence catalog: source, query/window, owner, evidence class, confidence, retention.
- Signal heatmap by domain, team/cohort, and path.
- Contradiction and missing-evidence register.
- CONFIRM/GAP-FILL survey instrument with cohort coverage and suppression rules.
- Platform-engineering maturity grid, or aspect evidence coverage with the formal score marked pending.
- ASDLC path matrix and agent-attribution findings, or path evidence coverage with the formal level marked pending.
- ADP readiness-gate table.
- Per-aspect/path/gate evaluation ledger: formal result or Pending, criteria met/applicable or evidence coverage, partial/contradicted/unobserved checks, confidence, and stable evidence citations.
- Sentiment and adoption findings with sampling limitations.
- Prioritized roadmap tied to measurable evidence.

## Guardrails

- No maturity claim without provenance, time window, and confidence.
- No high-confidence score from interview or survey evidence alone.
- No individual productivity, sentiment, or automation score.
- No portal screenshot or license count as proof of platform or ADP maturity.
- No catalog file, agent-instruction file, MCP configuration, or policy document as proof without checking completeness, freshness, adoption, and observed behavior.
- No inference that missing telemetry means missing behavior; size the visibility gap.
- No single enterprise average when teams, paths, or business units differ materially.
- Keep Internal Developer Portal, Internal Developer Platform, and Agentic Developer Portal distinct in every deliverable.

## Suggested effort

High. A useful pilot covers one value stream and two or three teams; an enterprise baseline is a multi-week discovery with explicit privacy governance and stakeholder validation.
