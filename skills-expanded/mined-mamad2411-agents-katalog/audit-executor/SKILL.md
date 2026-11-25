---
name: audit-executor
description: 'Orchestrates full governance audit across all customization types and produces a single executive aggregate report with per-type highlights, governance health assessment, and remediation summary.'
trigger: 'User requests a comprehensive governance audit or when release governance requires a full workspace health assessment.'
scope: 'Planning, Execution, Review lanes. Operationalizes governance-audit, audit-customization-types, execute-customization-audit, and governance-health-overview skills.'
inputs:
  - 'scope: all (fixed) — always audits agents, instructions, prompts, and skills'
outputs:
  - 'Executive aggregate report written to `.docs/governance/audit-executor-report.md`'
  - 'Report includes: executive summary, per-type audit highlights (severity-ranked findings), cross-type findings, governance health status, and remediation recommendations'
  - 'Links to detailed audit artifacts in `.docs/changes/governance/type-audits/` for each customization type'
related_skills:
  - 'audit-customization-types — primary audit source for all customization types'
  - 'execute-customization-audit — aggregates per-type audit outputs into executive-style findings'
  - 'governance-health-overview — contributes governance health assessment'
  - 'governance-audit — workspace-wide governance audit context'
workflow: |
  1. **Phase 1: Type audits** — Invoke `audit-customization-types` to audit agents, instructions, prompts, and skills independently, producing type-level findings in `.docs/changes/governance/type-audits/`.
  2. **Phase 2: Aggregation** — Invoke `execute-customization-audit` to compose the per-type audit outputs into an executive-style aggregate finding set with severity ranking and cross-type interaction analysis.
  3. **Phase 3: Governance health** — Invoke `governance-health-overview` to assess overall workspace governance health (completeness, consistency, traceability).
  4. **Phase 4: Report synthesis** — Synthesize a single `.docs/governance/audit-executor-report.md` containing:
     - Executive summary (overall health score, critical/high/medium/low finding counts)
     - Per-type audit highlights (top 3–5 findings per type by severity, with links to detailed audit)
     - Cross-type findings summary
     - Governance health assessment (coverage, drift, remediation readiness)
     - Remediation recommendation roadmap
     - Links to detailed audit artifacts
  5. **Phase 5: Closure** — Report the artifact path and key metrics to the user.
invocation: 'Invoke this skill when: (a) comprehensive governance audit is required before release or major workstream, (b) periodic governance health check is needed, or (c) governance-wide remediation tracking begins.'
self_contained: true
---

# audit-executor

Orchestrates all governance audits across customization types (agents, instructions, prompts, skills) and produces **one executive aggregate report** with severity-ranked findings, per-type highlights, governance health status, and remediation roadmap.

## When to Use

- **Release governance gate:** Before promoting to production, run this skill to confirm governance health across all customization types.
- **Periodic health checks:** Monthly or quarterly governance audits to track drift and remediation progress.
- **Remediation tracking:** Use this skill to establish a baseline when starting a governance remediation workstream.
- **Compliance and audit:** When external audit or certification requires evidence of consistent governance practices.

## Workflow

```
[Phase 1: Type Audits]
  ↓
  invoke audit-customization-types → agents, instructions, prompts, skills audits
  ↓
[Phase 2: Aggregation]
  ↓
  invoke execute-customization-audit → executive findings + severity ranking
  ↓
[Phase 3: Governance Health]
  ↓
  invoke governance-health-overview → health assessment
  ↓
[Phase 4: Synthesis]
  ↓
  produce single .docs/governance/audit-executor-report.md with:
    - Executive summary
    - Per-type highlights (top findings by severity, linked to detailed audits)
    - Cross-type findings
    - Governance health status
    - Remediation roadmap
```

## Inputs

- **Scope:** Fixed to all customization types (agents, instructions, prompts, skills). No filtering.

## Outputs

- **`.docs/governance/audit-executor-report.md`** — Single executive aggregate report containing:
  - Executive summary (overall health, finding counts by severity)
  - Per-type audit highlights with severity-ranked top findings
  - Cross-type interaction findings
  - Governance health assessment
  - Remediation recommendations
  - References to detailed audit artifacts in `.docs/changes/governance/type-audits/`

## Report Structure

```markdown
# Governance Audit Report
> Executive aggregate audit across all customization types

## Executive Summary
- Overall governance health score
- Critical/high/medium/low finding counts across all types
- Key remediation priorities

## Per-Type Audit Highlights
### Agents
- [Top 3–5 findings by severity]
- [Link to detailed audit: .docs/changes/governance/type-audits/agents-audit.md]

### Instructions
- [Top 3–5 findings by severity]
- [Link to detailed audit: .docs/changes/governance/type-audits/instructions-audit.md]

### Prompts
- [Top 3–5 findings by severity]
- [Link to detailed audit: .docs/changes/governance/type-audits/prompts-audit.md]

### Skills
- [Top 3–5 findings by severity]
- [Link to detailed audit: .docs/changes/governance/type-audits/skills-audit.md]

## Cross-Type Findings
- [High-priority cross-type interaction issues]

## Governance Health Assessment
- Coverage (% of assets with required metadata, docs, traceability)
- Consistency (naming, structure, policy alignment)
- Remediation readiness

## Remediation Roadmap
- [Ordered list of remediation actions with owner and lane classification]

## Audit Metadata
- Date run: [timestamp]
- Artifacts used: [list of audit artifact paths]
```

## Related Skills

- **`audit-customization-types`** — Audit agents, instructions, prompts, and skills independently and produce per-type findings.
- **`execute-customization-audit`** — Aggregate and rank per-type findings into an executive report.
- **`governance-health-overview`** — Assess workspace governance health (coverage, consistency, policy alignment).
- **`governance-audit`** — Broader workspace governance audit (use when governance-wide policy review is needed beyond customization types).

## Success Criteria

- [ ] All four customization types are audited
- [ ] Per-type audit artifacts are created in `.docs/changes/governance/type-audits/`
- [ ] Executive report is written to `.docs/governance/audit-executor-report.md`
- [ ] Report includes severity-ranked per-type findings linked to detailed audits
- [ ] Cross-type findings are surfaced
- [ ] Governance health assessment is included
- [ ] Remediation roadmap is actionable and assigned
