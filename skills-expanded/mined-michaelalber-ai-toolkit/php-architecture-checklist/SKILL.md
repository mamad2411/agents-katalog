---
name: php-architecture-checklist
audience: team
description: >
  Grades an existing PHP/Laravel codebase. Detects PHP version, framework
  (Laravel/Symfony/plain), and autoloading layout, then checks service-layer boundaries, strict
  typing, input validation, query safety, and config/secrets hygiene with file:line evidence.
  Use to review or grade a PHP codebase. Not for Socratic critique (architecture-review),
  security audits (php-security-review), or new test-first code (tdd-loop).
---

# PHP Architecture Checklist

> "A checklist cannot fly a plane, but a pilot cannot fly safely without one."
> — Atul Gawande

## Core Philosophy

Shared across the `dotnet` / `python` / `php` / `rust` architecture checklists — same values, language-specific checks.

**Non-Negotiable Constraints:**
1. **Detect before judging** — no checklist item is applied until the version, framework, and structure are known
2. **Evidence or it is not a finding** — every finding cites `file:line` and the offending pattern
3. **Version-correct advice only** — never recommend an API the detected version does not have
4. **The grade is counted, not felt** — the A–F grade comes from the tally of findings

| # | Value | What it means |
|---|-------|---------------|
| 1 | **Evidence over opinion** | Every finding cites `file:line` and the offending pattern. "Overuses facades" is not a finding; "`OrderController.php:42` calls `DB::raw` with request input" is. |
| 2 | **Feature cohesion** | Organized by business capability, not technical layer. Cross-feature coupling is a violation. |
| 3 | **Dependencies point inward** | Domain/service logic does not depend on framework facades or HTTP. Boundaries are explicit. |
| 4 | **Explicit error handling** | Failures handled at the right layer; no silent swallowing; errors carry diagnostic context. |
| 5 | **Config & secrets hygiene** | No hardcoded secrets; configuration injected, not reached for globally; secrets from env / secret-manager. |
| 6 | **Tests gate change** | Untested code is a finding; high-risk modules without tests are prioritized. |

## Workflow

Shared skeleton: `DETECT → SCAN → REPORT → RECOMMEND`.

```
DETECT     PHP version (composer.json `require.php`), framework (Laravel/Symfony/plain + version),
           autoloading (PSR-4 in composer.json), and whether a test suite exists (PHPUnit/Pest).
           Record findings; if a version cannot be determined, ask — never assume 8.3.

SCAN       Run the PHP Checklist below section by section. Gather evidence with tooling:
             phpstan analyse              # static analysis (target level >= 6)
             php-cs-fixer fix --dry-run   # PSR-12 style drift (Laravel projects: `pint --test` instead — wraps php-cs-fixer with Laravel's preset)
             composer outdated            # dependency currency
           Every violation becomes a finding with file:line and a severity (critical/high/medium/low).

REPORT     Emit the graded report (Output Template). Grade = function of counted findings.

RECOMMEND  Prioritize: critical → quick wins → modernization. Version-gate every recommendation;
           never suggest an API absent from the detected PHP / Laravel version.
```

**Load on demand — `references/operating-guide.md`:** PHP Checklist, AI Discipline Rules. Deeper detail: `references/php-conventions.md`, `references/review-checklist.md`.

## State Block

```
<arch-checklist-state>
language: php
mode: DETECT | SCAN | REPORT | RECOMMEND | COMPLETE
detected: [php 8.x | framework+version | psr-4 | tests:yes/no]
issues_found: [critical:N high:N medium:N low:N]
last_action: [what was just done]
next_action: [what should happen next]
</arch-checklist-state>
```

## Output Template

Shared across all four architecture checklists.

```markdown
## Architecture Checklist: [project] (PHP)
**Version**: [8.x] | **Framework**: [Laravel x/Symfony/plain] | **Tests**: [yes/no]

| Section | Pass | Fail | Warn |
|---------|------|------|------|
| Boundaries / Typing / Validation / Queries / Config / PSR / Tests | … | … | … |

### Grade: [A–F]
Grading: **A** 0 crit/0 high/≤3 med · **B** 0 crit/≤2 high · **C** 0 crit, gaps in one area ·
**D** 1+ crit · **F** fundamental problems (raw SQL on input, secrets in code, no service layer).

| Severity | Location | Finding | Recommendation |
|----------|----------|---------|----------------|
| CRITICAL | file:line | [pattern] | [version-gated fix] |

**Quick wins**: [low-effort, high-impact] · **Modernization**: [larger items with effort estimate]
```

## Integration with Other Skills

- **`architecture-review`** — When the grade is D/F, escalate to the Socratic critic: this checklist finds _what_ is wrong; `architecture-review` builds _why_.
- **`php-security-review`** — Companion for the security dimension (OWASP, mass-assignment, query injection).
- **`tdd-loop`** — Methodology for adding tests the checklist flags as missing, and for driving any refactor.
- **`dotnet` / `python` / `rust`-architecture-checklist** — Sibling skills sharing this exact Core Values + workflow + output.
