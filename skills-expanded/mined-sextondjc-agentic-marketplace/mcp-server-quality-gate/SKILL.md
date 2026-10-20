---
name: mcp-server-quality-gate
description: Use when an MCP server candidate needs an expert, evidence-first quality decision before merge or promotion.
---

# MCP Server Quality Gate

## Specialization

Provide a deterministic go or no-go decision for MCP server readiness based on protocol compliance, security posture, reliability, and operational evidence.

## Trigger Conditions

- A server change is ready for merge or release decision.
- Security or reliability risk is non-trivial.
- Multiple quality dimensions must be consolidated into one disposition.

## Hard Constraints

- Use only official MCP sources from [source-catalog.md](./references/source-catalog.md).
- SDK-specific checks apply only to C# and TypeScript implementations.
- Exclude community aggregators and unofficial source bundles.

## Inputs

- Candidate change scope and target environment.
- Test evidence and inspector outputs.
- Security and operability evidence.
- Known risks and unresolved findings.

## Required Outputs

- Severity-ranked findings list.
- Quality scorecard across core dimensions.
- Go, no-go, or go-with-conditions recommendation.
- Mandatory remediation list for blocking issues.

## Quality Dimensions

- Protocol correctness: primitives, capabilities, transport behavior.
- Contract quality: schema quality, validation, and error semantics.
- Security posture: auth boundaries, secret handling, sensitive tool controls.
- Reliability: timeout behavior, cancellation, retries, progress reporting.
- Operability: logs, diagnostics, and recoverability.

## Deterministic Workflow

1. Validate evidence completeness.
2. Evaluate each quality dimension.
3. Record findings with severity (`critical`, `high`, `medium`, `low`).
4. Reject promotion if any `critical` finding is unresolved.
5. Issue final disposition with explicit remediation ownership.

## Scorecard Template

| Dimension | Status | Key Evidence | Blocking |
|---|---|---|---|
| Protocol correctness | Pass or Fail | Spec and inspector evidence | Yes or No |
| Contract quality | Pass or Fail | Schema and error behavior checks | Yes or No |
| Security posture | Pass or Fail | Auth and data-protection checks | Yes or No |
| Reliability | Pass or Fail | Timeout and resilience checks | Yes or No |
| Operability | Pass or Fail | Logging and supportability checks | Yes or No |

## Disposition Rules

- `No-Go`: unresolved critical findings.
- `Go-With-Conditions`: no critical findings, but high findings with explicit mitigations.
- `Go`: no blocking findings and evidence complete.

## Done Criteria

- Findings are severity-ranked and complete.
- Scorecard is complete across all dimensions.
- Final recommendation is explicit and justified.
