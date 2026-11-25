---
name: Remediation Playbook
description: Actionable fix patterns for LLM vulnerabilities — system prompt hardening, input validation, output filtering, and tool sandboxing
version: 1.0.0
---

# Remediation Playbook

## Purpose

Provides the remediation-agent with concrete fix patterns for each vulnerability class. Every fix should be specific, implementable, and verifiable.

## When to Use

- After scan results show vulnerabilities
- When the user asks "how do I fix this?"
- When generating remediation reports
- During security reviews

## Fix Categories

| Category | Fixes | When to Apply |
|----------|-------|---------------|
| **System Prompt Hardening** | Instruction boundaries, explicit denials, XML-tagged input isolation | Jailbreak, injection findings |
| **Input Validation** | Length limits, character filtering, injection detection, sanitization | Injection, tool abuse findings |
| **Output Filtering** | PII redaction, content moderation, response validation | PII, harmful content findings |
| **Tool Sandboxing** | Parameterized queries, permission scoping, allowlists, capability limits | Tool abuse findings |

## Priority Framework

1. **Critical** — Fix immediately: prompt injection with data access, PII exposure, tool abuse with DB/file access
2. **High** — Fix this sprint: jailbreaks bypassing core restrictions, bias in customer-facing apps, compliance violations
3. **Medium** — Fix next sprint: partial prompt leaks, edge case harmful content, low-confidence findings
4. **Low** — Track and monitor: cosmetic issues, theoretical attacks, defense-in-depth improvements

## Reference Files

- [System Prompt Hardening](references/system-prompt-hardening.md)
- [Input Validation](references/input-validation.md)
- [Output Filtering](references/output-filtering.md)
- [Tool Sandboxing](references/tool-sandboxing.md)
