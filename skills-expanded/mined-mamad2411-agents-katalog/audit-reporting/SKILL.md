---
name: audit-reporting
description: >
  Structured finding format: severity, impact, PoC, remediation. Templates and
  classification standards for audit output. Used by Report Compiler.
---

# Audit Reporting Skill

## Purpose

Ensure all audit outputs follow a consistent, auditor-grade format with proper severity
classification, concrete impact descriptions, and traceable evidence chains.

## Severity Classification (Immunefi Standard)

| Severity | Criteria |
|----------|---------|
| **Critical** | Direct loss of funds, permanent freezing of funds, protocol insolvency |
| **High** | Theft of unclaimed yield, permanent DoS, governance manipulation |
| **Medium** | Griefing with material loss, temporary DoS, value extraction below threshold |
| **Low** | Non-critical issues, informational findings, gas optimizations |

## Finding Report Structure

Every confirmed finding must include:

1. **Title**: One-line description
2. **Severity**: Critical/High/Medium/Low with justification
3. **Impact**: Concrete description (e.g., "Attacker can drain 100% of vault TVL")
4. **Root Cause**: Specific code flaw with file and line reference
5. **Attack Path**: Step-by-step, numbered sequence
6. **PoC**: Link to runnable Foundry test
7. **Affected Code**: File, lines, snippet
8. **Remediation**: Specific fix with code example

## Evidence Chain

Every finding must have a traceable path:

```
Task (specs/tasks/TASK-{N}.md)
  → Reasoning (specs/reasoning/TASK-{N}-reasoning.md)
    → Verification (specs/verification/TASK-{N}-verification.md)
      → Finding (findings/FINDING-{ID}.md)
```

## What Makes a Finding Actionable

- ❌ "There may be a reentrancy risk" — NOT actionable
- ✅ "Reentrancy in Vault.withdraw() allows attacker to drain all ETH. PoC at test/exploit.t.sol" — actionable

## Coverage Reporting

The coverage map must honestly distinguish:
- **Full coverage**: Function analyzed with multiple task approaches
- **Partial coverage**: Function analyzed but not all paths/values tested
- **No coverage**: Function not targeted by any task (must be in gap record)
