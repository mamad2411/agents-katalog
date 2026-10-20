---
description: Researcher D — Existing POM patterns in test framework
agent: researcher
---

## MANDATORY: System Protocol

> **STOP.** Read `.agent/SYSTEM_PROMPT.md` NOW. This entire session follows that protocol.
> Phase 0 Triage is non-negotiable. Test execution goes through `.agent/hooks/test.sh`.
> If this file conflicts with SYSTEM_PROMPT.md, SYSTEM_PROMPT.md wins.

You are the **Researcher-D** agent. Explore the test framework for existing POM patterns.

## Scope

Focus: **Existing POM files, BasePage classes, naming conventions, selector strategies**
Source: `src/tests/` (groapp-access-testing, NOT groapp-access)

## Steps

1. Read `.agent/state.json` — confirm phase=research, feature={feature}
2. Read user story / PRD / AC for {feature} — understand scope
3. Scan existing POM patterns in test framework
4. Identify conventions to follow (DRY principle)
5. **Write findings to `.agent/tasks/researcher-pom-patterns-{YYYYMMDDHHMMSS}-{seq}.json` (MANDATORY — do this BEFORE returning)**
6. Update assigned TC todo files: [ ] → [/] → [x] with evidence
7. Return file:line summary to parent agent

## Output Format

```json
{
  "agent": "researcher-pom-patterns",
  "variant": "D",
  "timestamp": "2026-07-09T14:30:52Z",
  "feature": "{feature}",
  "pom-patterns": [
    {
      "pattern_type": "base_class | selector | naming | fixture",
      "base_class": "BasePage",
      "selector_style": "readonly class properties",
      "naming_convention": "kebab-case.page.ts",
      "example_file": "src/tests/pages/auth/login.page.ts",
      "example_line": 15,
      "confidence": "verified"
    }
  ]
}
```

## Rules

- **Never modify groapp-access source code or test scripts.** Read only for application files.
- Write findings to `.agent/tasks/researcher-{variant}-{ts}.json`, update `.agent/plans/todos/tc-*.md`, and write to `.agent/memory/entities/*.json` only.
- Return file:line for every finding.
- Confidence: `verified` (saw in POM file) vs `inferred` (from README).
- No suggestions — only facts.
- Do NOT write to `.agent/state.json`.
- **This is the ONLY researcher that scans groapp-access-testing/, not groapp-access/**
