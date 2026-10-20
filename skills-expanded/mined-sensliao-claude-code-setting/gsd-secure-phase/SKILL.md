---
name: gsd-secure-phase
canonical_id: gsd.workflow.secure_phase
aliases: [secure-phase, gsd-security-verify]
description: "Retroactively verify threat mitigations for a completed phase. GSD-namespace adapter, NOT an AppSec capability skill — namespace boundary intentional, do NOT merge into appsec-security-orchestrator."
argument-hint: "[phase number]"
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - OWASP ASVS: 5.0
  - NIST CSF: 2.0 (ID.RA, PR / RS)
upstream:
  - gsd-pipeline-orchestrator
  - gsd-execute-phase (post-completion)
downstream:
  - gsd-security-auditor (agent, opus)
  - appsec-security-orchestrator (for AppSec Release Evidence integration)
external_workflow: "@$HOME/.claude/get-shit-done/workflows/secure-phase.md (180 lines, full STRIDE retroactive-mode workflow)"
forbidden-tools: WebFetch
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "credentials.json"]
  never_write: ["production data", "real PII"]
  redact_on_output: ["tokens", "credentials", "PII"]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

<objective>
Verify threat mitigations for a completed phase. Three states:
- (A) SECURITY.md exists — audit and verify mitigations
- (B) No SECURITY.md, PLAN.md with threat model exists — run from artifacts
- (C) Phase not executed — exit with guidance

Output: updated SECURITY.md.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/secure-phase.md
</execution_context>

<context>
Phase: $ARGUMENTS — optional, defaults to last completed phase.
</context>

<process>
Execute end-to-end.
Preserve all workflow gates.
</process>
