---
name: rust-architecture-checklist
audience: team
description: >
  Grades an existing Rust codebase. Detects Rust edition, async runtime, and workspace
  structure, then checks ownership discipline, trait coherence, error-handling conventions,
  unsafe-block justification, and crate-boundary hygiene with file:line evidence. Use to review
  or grade a Rust codebase. Not for Socratic critique (architecture-review), security audits
  (rust-security-review), or new test-first code (tdd-loop).
---

# Rust Architecture Checklist

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
| 1 | **Evidence over opinion** | Every finding cites `file:line` and the offending pattern. "Overuses clone" is not a finding; "`handlers/order.rs:47` clones a `Vec<OrderItem>` that could be borrowed" is. |
| 2 | **Feature cohesion** | Organized by business capability, not technical layer. Cross-feature coupling is a violation. |
| 3 | **Dependencies point inward** | Domain logic does not depend on I/O or framework crates. Boundaries are explicit (`pub(crate)` by default). |
| 4 | **Explicit error handling** | Failures handled at the right layer; no silent swallowing; errors carry diagnostic context. |
| 5 | **Config & secrets hygiene** | No hardcoded secrets; configuration injected, not reached for globally; secrets from env / secret-manager. |
| 6 | **Tests gate change** | Untested code is a finding; high-risk modules without tests are prioritized. |

## Workflow

Shared skeleton: `DETECT → SCAN → REPORT → RECOMMEND`.

```
DETECT     Rust edition (Cargo.toml `edition`), async runtime (Tokio/async-std/none), and structure
           (workspace vs single crate). Record findings; edition changes what is idiomatic.

SCAN       Run the Rust Checklist below section by section. Gather evidence with tooling:
             cargo clippy -- -D warnings   # baseline — must pass before the checklist
             cargo audit                   # CVEs in the dependency tree
             grep -rn "unsafe" src/        # enumerate unsafe blocks for the audit
           Every violation becomes a finding with file:line and a severity (critical/high/medium/low).

REPORT     Emit the graded report (Output Template). Grade = function of counted findings.

RECOMMEND  Prioritize: critical → quick wins → modernization. Edition-gate every recommendation.
```

**Load on demand — `references/operating-guide.md`:** Rust Checklist, AI Discipline Rules. Deeper detail: `references/clippy-configuration.md`, `references/review-checklist.md`.

## State Block

```
<arch-checklist-state>
language: rust
mode: DETECT | SCAN | REPORT | RECOMMEND | COMPLETE
detected: [edition | runtime | workspace/single | tests:yes/no]
issues_found: [critical:N high:N medium:N low:N]
last_action: [what was just done]
next_action: [what should happen next]
</arch-checklist-state>
```

## Output Template

Shared across all four architecture checklists.

```markdown
## Architecture Checklist: [crate] (Rust)
**Edition**: [2015/2018/2021/2024] | **Runtime**: [Tokio/async-std/none] | **Tests**: [yes/no]

| Section | Pass | Fail | Warn |
|---------|------|------|------|
| Ownership / Traits / Errors / unsafe / Boundaries / Async / Tests | … | … | … |

### Grade: [A–F]
Grading: **A** 0 crit/0 high/≤3 med · **B** 0 crit/≤2 high · **C** 0 crit, gaps in one area ·
**D** 1+ crit · **F** fundamental problems (unjustified `unsafe`, runtime conflict, library `.unwrap()` everywhere).

| Severity | Location | Finding | Recommendation |
|----------|----------|---------|----------------|
| CRITICAL | file:line | [pattern] | [edition-gated fix] |

**`unsafe` audit**: | location | SAFETY comment | quality | risk |
**Quick wins**: [low-effort, high-impact] · **Modernization**: [larger items with effort estimate]
```

## Integration with Other Skills

- **`architecture-review`** — When the grade is D/F, escalate to the Socratic critic: this checklist finds _what_ is wrong; `architecture-review` builds _why_.
- **`rust-security-review`** — Companion for the security dimension (`unsafe` audit for memory-safety vulns, `cargo-audit`).
- **`rust-feature-slice`** — Correct-pattern reference when the checklist flags structural violations.
- **`tdd-loop`** — Methodology for adding tests the checklist flags as missing, and for driving any refactor.
- **`dotnet` / `python` / `php`-architecture-checklist** — Sibling skills sharing this exact Core Values + workflow + output.
