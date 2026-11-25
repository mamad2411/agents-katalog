---
name: trust-center-readiness-review
description: Design and audit public trust centers, security pages, privacy/compliance portals, subprocessors, uptime/status links, data protection summaries, policy libraries, evidence request flows, customer assurance, sales enablement, and review cadence. Use when a SaaS, developer tool, marketplace, AI product, or enterprise product needs credible trust proof before procurement or launch.
---

# Trust Center Readiness Review

Use this skill to convert a trust centers, public security/privacy proof, compliance evidence, subprocessors, uptime, and sales assurance question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify buyer segment, trust objections, claims, evidence sources, policy owners, compliance status, subprocessor exposure, and sales/security questionnaire needs.
2. Read `references/trust-center-readiness-patterns.md`.
3. Classify trust-center surface: public overview, gated evidence room, security questionnaire support, compliance portal, status/uptime hub, or enterprise sales enablement.
4. Define claim-proof boundaries, policy library, evidence request workflow, owner cadence, update triggers, access controls, and sales/support handoffs.
5. Produce trust center plan, state machine, decision table, event schema, evidence checklist, and stale-claim review loop.

## Guardrails

- Do not publish certifications, audits, SLAs, encryption claims, or subprocessors without current evidence and owner approval.
- Do not expose sensitive architecture, pentest, customer, or incident details in public trust pages.
- Do not let sales use trust-center claims that are broader than the published evidence.
- Do not keep stale subprocessors, policies, screenshots, or compliance status visible after changes.

## Output format

```text
Trust center context:
Buyer / claim / evidence / public-private boundary:

Trust center plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Claims, evidence, and owners:
- <item> -> <policy, metric, edge case, support note>

Stale-claim and evidence-request handling:
- <trigger> -> <action, communication, owner>
```
