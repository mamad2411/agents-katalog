---
name: defensive-appsec-review-skill
author: jovd83
version: 4.1.1
description: Use when you need an authorized, non-destructive security review of repos, APIs, and cloud apps. Trigger for OWASP reviews, dependency/secret audits, scanner consolidation, and security reports. Use for AppSec triage. Do NOT use for offensive exploitation or unauthorized testing.
metadata:
    author: jovd83
    version: 4.1.1
    dispatcher-layer: feedback
    dispatcher-lifecycle: active
    display-name: Defensive AppSec Review Skill
    category: security
    dispatcher-output-artifacts: security_findings, remediation_report, review_plan
    dispatcher-risk: medium
    dispatcher-writes-files: true
    dispatcher-input-artifacts: repository_context, scanner_results, architecture_notes, review_scope
    dispatcher-capabilities: defensive-appsec-review, security-triage, remediation-reporting
    dispatcher-stack-tags: security, appsec, review
    dispatcher-accepted-intents: review_application_security, triage_security_findings, plan_security_review
    dispatcher-category: security

---

# Defensive AppSec Review Skill

> **Author:** jovd83 | **Version:** 4.1.1| **Maturity:** production | **License:** MIT. See LICENSE  
> **Compatibility:** Designed for Agent Skills compatible coding agents. Bundled automation requires Node.js 18+ when running scripts. Local file access is sufficient for the core workflow; network access is optional and should not be assumed.


Perform defensive, evidence-based application security assessments for authorized targets.

Use this skill to turn a vague "security check" request into a scoped, non-destructive review with clear findings, honest blind spots, and remediation-ready output. Prefer passive analysis, deterministic evidence collection, and explicit limits over speculative or offensive behavior.

## Outcomes This Skill Owns

- Scope the assessment safely before making risk claims.
- Choose the right review lens for the target surface.
- Build an attack-surface-aware review plan.
- Run safe local review steps when local artifacts are available.
- Normalize external static-analysis results into one findings contract.
- Produce remediation-oriented findings and stakeholder-ready reports.

## Boundaries This Skill Must Preserve

- Do not perform exploit development, post-exploitation, persistence, credential theft, evasion, or destructive testing.
- Do not treat unclear authorization as implicit permission.
- Do not claim compliance, exploitability, or production impact without evidence.
- Do not blur runtime notes, project-local files, and shared memory into one vague memory layer.

If the request crosses these boundaries, decline the unsafe portion and offer a safe alternative such as scoped review planning, passive code review, or report consolidation.

## Activation Checklist

Before acting, confirm or infer the minimum safe context:

- target surface: `web`, `api`, `mobile`, `repo`, `iac`, `pipeline`, or `mixed`
- goal: `triage`, `review`, `verification`, `plan`, `report`, or `normalize`
- scope: paths, services, endpoints, workflows, or components in scope
- authorization: explicit permission or clearly defensive local context
- constraints: read-only, no network, no production interaction, timebox, exclusions
- evidence available: source code, manifests, CI files, prior findings, SARIF, JSON outputs

If the user only says "run a security check," default to the safest passive interpretation and keep the review read-only.

## Choose One Primary Mode

Pick the narrowest mode that satisfies the request. State the chosen mode in the response so the user knows what work was actually done.

### 1. Triage

Use for quick repo or config checks when the user wants the few issues that matter most.

Do:

- identify the highest-signal attack surface
- collect deterministic evidence quickly
- report only the most actionable findings
- call out what was not verified

### 2. Standards-Aligned Review

Use when the user names a framework or wants a structured control lens.

Recommended standards:

- web: OWASP WSTG, ASVS, OWASP Top 10
- api: OWASP API Top 10, ASVS
- mobile: OWASP MASVS
- repo, SDLC, CI/CD, supply chain: NIST SSDF, OWASP SCVS, SLSA, OWASP SAMM
- AI-enabled systems: app-surface standard first, AI boundary review second

See [references/frameworks-guide.md](references/frameworks-guide.md) when the standard choice is unclear.

### 3. Report Compilation

Use when the user already has findings and needs a clean report, delta report, or SARIF output.

### 4. Result Normalization

Use when the user has outputs from tools such as CodeQL, Semgrep, Gitleaks, Trivy, OSV-Scanner, OpenSSF Scorecard, or Dependency-Check and wants one unified findings envelope.

### 5. Review Planning

Use when the user needs a safe attack-surface-aware plan before any evidence collection starts.

## Core Workflow

Follow this order unless the user explicitly asks for only one artifact.

### 1. Scope the review

- name the asset and exclusions
- identify trust boundaries, privileged flows, secrets, and third-party dependencies
- state the likely risk themes before scanning

For larger systems, summarize:

- entry points
- authentication and authorization surfaces
- data ingress and storage paths
- external services and integrations
- CI/CD and deployment trust boundaries

### 2. Collect safe evidence

Prefer repository and configuration review over active interaction.

When local files are available, use the bundled scripts instead of re-inventing the workflow:

```powershell
node scripts/audit-scan.js --target . --type repo --standard nist-ssdf --output sandbox/raw-findings.json
```

For API-focused review:

```powershell
node scripts/audit-scan.js --target . --type api --standard owasp-api-top10 --output sandbox/raw-findings.json
```

For repo or supply-chain review with external result ingestion:

```powershell
node scripts/audit-scan.js --target . --type repo --standard owasp-scvs --depth deep --output sandbox/raw-findings.json
```

If external findings already exist, normalize them first when needed:

```powershell
node scripts/normalize-external-results.js --tool sarif --input sandbox/codeql.sarif --output sandbox/codeql-findings.json --target . --type repo --standard owasp-top10
```

Do not fabricate missing evidence. If a runtime check would materially improve confidence, describe it as a follow-up instead of performing it unless the user explicitly authorizes that mode and it remains safe.

### 3. Validate candidate findings

Use the two-layer method from [references/detection-methodology.md](references/detection-methodology.md):

- Layer 1: gather candidate issues conservatively
- Layer 2: read enough context to downgrade false positives and confirm real weaknesses

A finding is not ready to report as verified unless it has:

- a concrete artifact or observation
- a navigable location, ideally `file:line`
- a plain-language impact statement
- a remediation step an engineer can act on
- an honest confidence level

If confidence is partial, label it as `needs manual verification` rather than overstating certainty.

### 4. Produce the right deliverable

Choose the smallest useful output:

- chat summary for fast triage
- markdown report for engineering handoff
- HTML report for stakeholder distribution
- SARIF for CI or code-scanning ingestion
- machine-readable findings JSON for downstream tooling

Use the reporter when a file deliverable is useful:

```powershell
node scripts/generate-report.js sandbox/raw-findings.json --output sandbox/final-security-report.md
node scripts/generate-report.js sandbox/raw-findings.json --format html --output sandbox/final-security-report.html
node scripts/generate-report.js sandbox/raw-findings.json --format sarif --output sandbox/findings.sarif.json
```

## Response Contract

Unless the user asks for something narrower, structure the response in this order:

### Assessment Summary

- what was reviewed
- which mode and standards were used
- what stayed passive and non-destructive
- what remained out of reach

### Key Findings

For each reported finding include:

- severity and title
- affected asset or location
- why it matters
- evidence basis
- recommended fix

Add framework mappings only when they help remediation, ownership, or governance.

### Gaps and Follow-Ups

- missing artifacts
- blind spots
- runtime checks intentionally deferred
- items that still need manual verification

If no findings are verified, say that explicitly and still report residual risk and blind spots.

## Finding Quality Bar

Good findings are:

- evidence-backed
- specific
- reproducible or independently reviewable
- severity-justified
- remediation-oriented

Do not turn generic hardening ideas into findings unless there is an observed weakness. Exclude obvious fixtures, demo material, placeholders, and documentation snippets unless there is evidence they are shipped or live.

## Memory Model

Keep memory responsibilities explicit and separate.

### Runtime memory

Use for:

- current scope
- working hypotheses
- temporary scan outputs
- draft findings under review

Do not imply runtime notes are durable.

### Project-local persistent memory

Use repository files for:

- schemas
- templates
- references
- deterministic helper scripts
- examples and eval artifacts

Do not store secrets, tokens, or target-sensitive evidence beyond what the user explicitly wants in local outputs.

### Shared memory

Shared memory is out of scope for this skill. If broader cross-agent reuse is needed, integrate with an external shared-memory skill rather than embedding that infrastructure here.

## Error Handling

If tooling fails:

1. say what failed and why
2. fall back to a narrower manual review when safe
3. record the blind spot in the final output

Common cases:

- missing Node.js runtime
- invalid target path
- repository too large for a broad scan
- missing manifests or lockfiles
- external tool output that needs human validation before promotion into verified findings

## Gotchas

- **Node.js 18+ Required**: Automation scripts (`scripts/*.js`) require Node.js 18 or higher. They will fail on older runtimes.
- **Target Must Be a Directory**: The `audit-scan.js` script expects a `--target` that is a directory. Passing a single file path will result in an error.
- **Default Exclusions**: Directories like `node_modules`, `.git`, `dist`, `build`, and `target` are skipped by default to ensure performance and reduce noise. If you need to scan these, you must manually review them or modify the script constants.
- **File Size Limits**: Files exceeding 1MB are skipped by the scanner to prevent memory exhaustion and hanging. These are recorded as "oversized" in the scan telemetry.
- **Passive-Only Enforcement**: This skill is intentionally designed to be non-destructive. It will refuse to perform active exploitation, credential brute-forcing, or any action that could impact production stability.
- **Confidence Levels**: Not all findings are verified. Some may be marked with `Low` or `Medium` confidence or labeled `needs manual verification`. Always review the `evidence` field before acting on a finding.
- **Normalization Tool Compatibility**: `normalize-external-results.js` supports specific formats (SARIF, Gitleaks, Trivy, OSV-Scanner, Scorecard, Dependency-Check). If your tool's output isn't in one of these formats, normalization will fail.
- **Autodiscovery for Deep Scans**: When using `--depth deep`, the scanner searches for common tool outputs (e.g., `semgrep.sarif`, `trivy.json`) in the current directory and `sandbox/`. Ensure your external results are named correctly or provide them explicitly using `--deep-inputs`.

## Resource Map

Load deeper resources only when needed:

- [references/scope-intake-template.md](references/scope-intake-template.md): structured intake for broader assessments
- [references/capability-matrix.md](references/capability-matrix.md): safe capability and coverage selection
- [references/frameworks-guide.md](references/frameworks-guide.md): standards mapping guidance
- [references/detection-methodology.md](references/detection-methodology.md): false-positive reduction and verification guidance
- [references/external-tooling-guide.md](references/external-tooling-guide.md): external scanner normalization workflow
- [references/review-checklist.md](references/review-checklist.md): final delivery quality check
- [schemas/security-assessment.schema.json](schemas/security-assessment.schema.json): machine-readable findings contract
- [scripts/audit-scan.js](scripts/audit-scan.js): deterministic local scan helper
- [scripts/normalize-external-results.js](scripts/normalize-external-results.js): external result normalizer
- [scripts/generate-report.js](scripts/generate-report.js): markdown, HTML, and SARIF report generator

## Quick Examples

**Repo triage**

User:
`Review this service repo for secrets, risky CI permissions, and unsafe config. Stay read-only.`

Expected behavior:

- confirm local defensive scope
- run or emulate a passive repo review
- return high-signal findings plus blind spots

**API review**

User:
`Assess this API codebase against OWASP API Top 10 and focus on authorization risk.`

Expected behavior:

- choose API review mode
- prioritize BOLA, BFLA, mass assignment, sensitive logging, and request-driven trust boundaries
- separate verified weaknesses from runtime follow-ups

**Unsafe request**

User:
`Try to break into this third-party login page and see what works.`

Expected behavior:

- decline the offensive request
- explain the authorization boundary
- offer a safe alternative such as a scoped defensive review plan

## Maintenance Notes

- Keep this file activation-friendly and move deep detail into `references/`.
- Keep metadata aligned with `package.json`, `README.md`, and `agents/openai.yaml`.
- Prefer adding deterministic tooling or reference material over bloating the main prompt.

## Telemetry & Logging

When using this skill, agents MUST log the following telemetry to the project's security audit ledger:
- Assessment mode and standards used
- Scope and trust boundaries identified
- Verified findings and remediation recommendations
- Intentional blind spots and deferred checks
- Tooling versions and scan duration
- Resource map and script usage for traceability