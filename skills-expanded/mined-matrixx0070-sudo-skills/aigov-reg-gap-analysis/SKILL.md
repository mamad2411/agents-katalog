---
name: aigov-reg-gap-analysis
version: 1.0.0
description: Compare an organization's current AI governance practices against an applicable framework (EU AI Act, NIST AI RMF, ISO 42001) and produce a prioritized gap list scored by severity and effort with concrete remediation actions.
author: matrixx0070
tags: [gap-analysis, eu-ai-act, nist-ai-rmf, iso-42001, compliance, remediation]
capabilities: []
---

## When to use

Use this when an organization needs to know where it stands against a named framework or regime — the EU AI Act obligations for its role and risk tiers, the NIST AI RMF functions, or ISO/IEC 42001 — and wants a ranked list of what is missing and what to fix first. Reach for it before an audit or filing, when scoping a remediation budget, or when leadership asks "are we compliant." The output is a prioritized gap register that turns a framework into an actionable plan.

**Not for:** cataloguing the systems being assessed (use aigov-ai-inventory), tiering a single use case (use aigov-use-case-triage), writing one system's impact assessment (use aigov-aia-generation), drafting the policy the gaps call for (use aigov-policy-starter), reviewing one vendor product (use aigov-vendor-ai-review), tracking regulatory change over time (use aigov-policy-monitor), running the intake interview that seeds a program (use aigov-cold-start-interview), adapting a template (use aigov-customize), or organizing the matter file (use aigov-matter-workspace).

This skill is decision-support, not legal advice. A qualified attorney must confirm which regime applies, your role under it, your systems' risk tiers, and any gap characterization before it is relied on for compliance, disclosed, or filed.

## Method

1. Fix the target: which framework(s) apply, in which jurisdictions, and — critically — the org's **role** (provider vs deployer vs distributor/importer) and the **risk tiers** of its systems. Pull the inventory for the system list.
2. Select the obligation set: derive the concrete requirements the applicable role and tier impose (high-risk EU AI Act duties, NIST AI RMF outcomes, ISO 42001 clauses). Do not assess against obligations that do not apply.
3. Gather current-state evidence per obligation: what document, control, or process exists today, and where it lives. No evidence = a gap, even if "we do that informally."
4. Score each gap: **severity** (regulatory/liability exposure if unaddressed) × **effort** (cost and time to remediate). **Decision:** rank remediation by severity first, then within a severity band do the low-effort items first — high-severity/low-effort gaps are the immediate action list.
5. Write a specific remediation action per gap: the artifact or control to build, the owner, and a target date — not "improve documentation."
6. Note interdependencies: some gaps block others (no inventory blocks risk management; no logging blocks post-market monitoring). Sequence accordingly.
7. Mark role, tier, and applicability as PROVISIONAL pending counsel, and version the register.

## Example

A firm deploys a third-party resume-screener (EU AI Act Annex III → high-risk; the firm is a **deployer**). Assessing deployer obligations: no human-oversight procedure (severity high, effort low → do now), no logging retention arrangement with the vendor (high/medium), no record it informs candidates (medium/low → do now), and no monitoring of accuracy across demographic groups (high/high → plan). Training-data governance is flagged high-severity because the firm cannot evidence the vendor's data quality. Ranked action list leads with the two high-severity/low-effort gaps. Role and tier marked PROVISIONAL for counsel.

## Pitfalls

- **Assessing the wrong role.** Provider and deployer obligations differ sharply; scoring a deployer against provider duties produces a false gap list. Confirm role first.
- **Crediting informal practice as a control.** If it is not documented and evidenced, it is a gap — regulators and auditors need artifacts, not assurances.
- **Ranking by severity alone.** A high-severity gap that takes a year should not block three high-severity fixes achievable this week. Score effort too.
- **Vague remediations.** "Strengthen data governance" is not actionable. Name the artifact, the owner, and the date, or the register does not drive work.

## Output format

```
# AI Governance Gap Analysis — <org> — <framework(s)> — <date> — v<n>
Role: provider | deployer | distributor (PROVISIONAL)
Risk tiers in scope: [...]   Jurisdictions: [...]

## Gap register
| ID | Obligation (source) | Current state / evidence | Gap | Severity | Effort | Priority | Remediation action | Owner | Target |

## Immediate action list (high severity × low effort)
- <gap> — <action> — <owner> — <date>

## Blocking dependencies
- <gap A> blocks <gap B>

Role, tier, and applicability are PROVISIONAL. Attorney must confirm before reliance or filing.
```

## Reference

Substantive overview below — accurate to the frameworks as commonly described, but not legal advice. Applicability, role, tiers, and obligations must be confirmed by counsel for your jurisdiction and the current version of each regime.

### EU AI Act — high-risk obligations (the core assessment set)

For systems classified high-risk (Annex III use cases such as employment, education, essential services, biometrics, law enforcement, migration; and safety components of regulated products), the Act imposes a defined obligation set. Assess each:

| Obligation | What it requires |
|-----------|------------------|
| **Risk management system** | A continuous, documented process to identify, evaluate, and mitigate risks across the lifecycle |
| **Data & data governance** | Training/validation/test data that is relevant, representative, and examined for bias and errors |
| **Technical documentation** | Documentation demonstrating conformity, kept current (Annex IV) |
| **Record-keeping / logging** | Automatic logging of events over the system's lifetime for traceability |
| **Transparency to deployers** | Instructions for use enabling deployers to operate and oversee the system |
| **Human oversight** | Designed-in measures letting humans understand, monitor, intervene, and override |
| **Accuracy, robustness, cybersecurity** | Appropriate performance levels and resilience to error, faults, and attacks |
| **Quality management system** | An organizational QMS ensuring ongoing compliance (provider duty) |
| **Conformity assessment & registration** | Assessment before market entry; registration in the EU database (provider duty) |
| **Post-market monitoring** | Ongoing collection and analysis of performance; incident reporting |

### Provider vs deployer — the role split

Obligations attach to your **role**, and most organizations are deployers of others' systems:

| | **Provider** (develops / places on market) | **Deployer** (uses under its authority) |
|--|--|--|
| Build risk-mgmt & QMS | Yes | No (relies on provider) |
| Technical documentation & conformity assessment | Yes | No |
| Registration in EU database | Yes | For some high-risk deployments |
| Human oversight in operation | Designs it | **Operates it** — assign competent humans |
| Use per instructions & monitor | — | **Yes** — follow instructions, monitor, keep logs |
| Inform affected persons / transparency | — | **Yes** — where required |
| Fundamental-rights impact assessment | — | Required for certain deployers (public bodies, some services) |

Note: a deployer that substantially modifies a system, rebrands it, or puts its own name on it can be **reclassified as a provider** and inherit provider duties. GPAI (foundation-model) providers carry a separate obligation set (technical docs, training-data summary, added duties for systemic-risk models). Flag both.

### NIST AI RMF — assessment scaffold (GOVERN / MAP / MEASURE / MANAGE)

Use the four functions as the structure for the whole assessment; they are voluntary but map cleanly onto most obligations:

| Function | Assess whether the org... |
|----------|---------------------------|
| **GOVERN** | Has policies, named accountability, culture, and risk tolerance for AI (cross-cutting) |
| **MAP** | Has catalogued systems and their context, purpose, and risks (needs an inventory) |
| **MEASURE** | Assesses and tracks performance, bias, robustness, and impacts with metrics |
| **MANAGE** | Prioritizes, responds to, and monitors risks, including incident response |

ISO/IEC 42001 (AI management system) complements this with a certifiable **management-system** structure (context, leadership, planning, support, operation, evaluation, improvement) — assess it where certification is a goal; its clauses overlap heavily with GOVERN and MANAGE.

### Gap-scoring rubric (severity × effort)

Score each gap on both axes, then set priority:

| | **Severity** | **Effort** |
|--|--|--|
| **1 (Low)** | Minor/documentation, low exposure | Days; existing owner |
| **3 (Med)** | Notable exposure or audit finding | Weeks; cross-team |
| **5 (High)** | Prohibited practice, high-risk non-conformity, or direct liability | Months; new capability/budget |

Priority: **P1** = high severity × low effort (do now); **P2** = high severity × high effort (plan/fund); **P3** = low severity × low effort (quick wins); **P4** = low severity × high effort (defer). Rank the register by severity first, then effort within band.

### Training-data governance — a common high-severity gap

Data governance is the gap most organizations underestimate. Deployers frequently cannot evidence the quality, representativeness, or provenance of the data behind a system they use, and providers often lack documentation of bias testing and dataset lineage. Because EU AI Act data-governance duties and NIST MEASURE bias outcomes both hinge on it — and because bias in training data drives discrimination liability — an unevidenced data-governance control should default to **high severity**. Remediation typically requires provider attestations or contract terms (for deployers) and documented dataset examination, bias testing, and lineage records (for providers).
