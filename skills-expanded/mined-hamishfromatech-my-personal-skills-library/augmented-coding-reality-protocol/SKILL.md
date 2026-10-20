---
name: augmented-coding-reality-protocol
description: Make strategic, evidence-based decisions about AI coding tool adoption based on 2026 independent research. Use when piloting AI-assisted development, evaluating vendor productivity claims, training senior developers on sustainable AI workflows, or architecting code quality gates for AI-generated contributions. NOT for teams seeking justification for unlimited AI tool deployment or greenfield prototyping where code longevity is irrelevant.
---

# Augmented Coding Reality Protocol

## Overview

Independent research in 2026 reveals that AI coding tools make experienced developers 19% slower on realistic production tasks despite feeling 20% faster — a 39-percentage-point perception-reality gap. Code quality degrades measurably: refactoring collapses from 25% to under 10% of changed lines, duplication increases 4×, and security vulnerabilities rise 2.74×. This skill provides the evidence-based framework for adopting AI tools as productivity-neutral augmentation rather than magic multiplier, preserving code quality and team sustainability.

## When to Use

- Piloting AI coding tools before enterprise-wide rollout and need objective measurement criteria
- Evaluating vendor claims of 55%+ productivity gains against independent research
- Training senior developers to recognize AI-specific failure patterns during code review
- Designing CI/CD gates that catch AI-generated quality degradation before it compounds
- Creating engineering policy that distinguishes augmented coding (disciplined) from vibe coding (reckless)
- Building business cases for AI tooling that account for total cost of ownership, not just license fees

NOT for:
- Justifying unchecked AI tool adoption to leadership
- One-off prototypes expected to be discarded
- Teams without code review, testing, or CI/CD infrastructure
- Junior-heavy teams without senior oversight for AI-generated output

## Core Insight: The Productivity Illusion

Vendor benchmarks claim 55% faster completion (GitHub) and 2× productivity (Cursor). Independent studies tell a different story:

| Study | Design | Finding |
|-------|--------|---------|
| METR | RCT, 16 experienced developers, 246 real issues | 19% slower with AI; 39-point perception-reality gap |
| GitClear | Longitudinal, 211M lines, 2020–2024 | Refactoring 25% → <10%; duplication 8.3% → 12.3% |
| CodeRabbit | Structured PR analysis, 470 PRs | 1.7× more issues; 3× readability degradation; 2.74× security issues |
| Tenzai | Security audit, 15 production apps | 100% lacked CSRF protection and security headers |
| Cortex | Pipeline observational, 1,255 teams | PRs/author +20%, incidents/PR +23.5% |
| Faros AI | Delivery pipeline longitudinal | PR sizes +154%, review times +91% |

**The tax exceeds the benefit.** Time saved during initial generation is consumed by verification, debugging hallucinations, refactoring duplicated output, and resolving premature revisions that passed tests but failed in production.

## Core Process / Workflow

### Step 1: Establish the Baseline Reality

Before introducing AI tools, measure your current state. These metrics become your control group.

| Metric | Measurement Tool | Why It Matters |
|--------|-----------------|--------------|
| Refactoring rate | GitClear, GitPrime | Target ~25% of changed lines; AI pushes this below 10% |
| Code duplication | jscpd, Simian, SonarQube | Baseline typically 3–8%; AI drives 4× increase |
| Code churn | GitClear, custom queries | Premature rewrites within 30 days of merge |
| Security vulnerability density | Semgrep, Snyk, Veracode | Compare AI vs. human baseline per PR |
| Mean review time | GitHub/GitLab analytics | AI-generated PRs require 91% longer review |
| Cyclomatic complexity | SonarQube, Code Climate | AI generates verbose, nested code |

**Governance principle:** Treat AI-generated code as untrusted input requiring the same scrutiny as outsourced contractor code.

### Step 2: Implement the Augmented Coding Protocol

Kent Beck distinguishes augmented coding from vibe coding: "In vibe coding you don't care about the code, just the behaviour of the system. In augmented coding you care about the code, its complexity, the tests, & their coverage."

**The four disciplines:**

1. **Test-Driven Development (TDD) Enforcement**
   - Write the test before asking AI to generate the implementation
   - AI output must pass existing tests before acceptance
   - Regression tests are mandatory for every bug fix

2. **Mandatory Code Review with Comprehension Contract**
   - Label all AI-generated PRs automatically (>50% AI-generated lines)
   - Reviewer must explain the code back in their own words
   - If the reviewer cannot explain it, the code is rejected for clarification
   - Senior developer approval required for junior developer AI usage

3. **Architectural Oversight**
   - AI is constrained to well-understood, bounded tasks (boilerplate, tests, documentation)
   - Novel architectural decisions require human design review
   - Load CONVENTIONS.md and utility catalogs into AI context before generation

4. **Prompt Engineering for Quality**
   - Default prompts include security requirements: "Write a secure login function using bcrypt, with rate limiting and timing-attack protection"
   - Multi-stage generation: initial prompt → security verification prompt → adversarial challenge testing
   - Never accept first-generation output without refinement

### Step 3: Deploy the Four Quality Gates

```
┌─────────────────────────────────────────────────────────────┐
│ Gate 1: Pre-Commit Secrets Detection                        │
│ • GitGuardian / TruffleHog / Semgrep at commit time         │
│ • Block, don't warn — AI-assisted commits leak at 2× rate   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Gate 2: AI-Specific SAST (Blocking)                         │
│ • CWE-94 (Injection), CWE-79 (XSS), CWE-352 (CSRF)          │
│ • Custom rules: missing error handling, hardcoded values    │
│ • 100% of AI-assisted PRs must pass before merge            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Gate 3: Duplication & Complexity Controls                   │
│ • Fail build if duplication increases >3% per PR            │
│ • Cyclomatic complexity limit per function (e.g., <15)        │
│ • "Re-implements existing utility" detection                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Gate 4: Post-Merge Monitoring                               │
│ • Error rate telemetry by file age and generation source    │
│ • Monthly architectural drift scoring                       │
│ • Refactoring budget: allocate 15% of sprint capacity         │
└─────────────────────────────────────────────────────────────┘
```

### Step 4: Measure the Perception-Reality Gap

**Monthly survey protocol:**
- Ask developers: "How much faster do you feel with AI tools?" (self-reported)
- Measure objective: story point velocity, cycle time, defect escape rate (measured)
- Calculate the gap. If self-reported > measured by >15 percentage points, investigate.

**Warning signs the gap is widening:**
- Developers report feeling productive while sprint velocity declines
- PR counts increase but features shipped per sprint decrease
- Test coverage drops while "code written" metrics rise
- Security findings increase quarter-over-quarter

### Step 5: Apply the 80/20 AI Rule

| Task Category | AI Allocation | Human Requirement |
|-------------|---------------|-------------------|
| Boilerplate, scaffolding, documentation | 90% AI | Review for consistency |
| Test generation | 80% AI | Verify edge case coverage |
| Bug fixes in known code | 60% AI | Comprehension contract |
| New features in existing architecture | 40% AI | Design review mandatory |
| Novel architectural decisions | 0% AI | Human-led with AI as research assistant |

**The refactoring budget:** Allocate 15% of every sprint to refactoring AI-generated code from prior sprints. This is not overhead — it is maintenance of the AI productivity dividend.

### Step 6: Train for Augmented Coding, Not Vibe Coding

**Curriculum modules:**

1. **AI Failure Pattern Recognition**
   - Hallucinations: fake libraries, invented APIs, non-existent parameters
   - Logic gaps: missing null checks, edge case blindness, off-by-one errors
   - Security omissions: missing CSRF, CORS, headers, input validation
   - Readability degradation: long functions, inconsistent naming, minimal comments

2. **The Comprehension Contract**
   - Reviewer reads every line of AI-generated code
   - Identifies the design pattern and one failure mode
   - Confirms fit with existing architecture
   - Documents understanding before approval

3. **Prompt Engineering for Security**
   - Include security requirements in every prompt
   - Use multi-stage generation with verification prompts
   - Challenge-test with adversarial inputs before merge

4. **When to Override AI**
   - AI suggests deprecated APIs or outdated patterns
   - Generated code duplicates existing utilities
   - Security controls are omitted for brevity
   - The task requires architectural reasoning beyond pattern matching

## When AI Tools Add Value

| Scenario | Value | Caveat |
|----------|-------|--------|
| Prototyping and proof-of-concepts | High | Code will be rewritten; don't merge to production |
| Learning new frameworks | Moderate | AI provides examples; human must understand them |
| Tedious boilerplate generation | High | Must be reviewed for consistency with project conventions |
| Test scaffolding | Moderate | Verify edge cases and failure modes are covered |
| Greenfield isolated functions | Moderate | Low architectural context required |

## When AI Tools Create Risk

| Scenario | Risk Level | Mitigation |
|----------|-----------|------------|
| Production systems with long lifecycles | Critical | Mandatory architectural review, refactoring budget |
| Security-facing applications | Critical | Blocking SAST gates, security-trained reviewers |
| Complex existing codebases | High | Context window loading, ADR visibility, senior oversight |
| Junior-heavy teams without senior review | Critical | Restrict AI to scaffolding, mandatory senior review |
| Regulated environments (SOC 2, HIPAA) | Critical | Full audit trail, AI provenance metadata, policy-as-code |

## A-Tech Product Applications

### A-Coder (IDE)
- **Reality dashboard:** Display objective productivity metrics alongside self-reported feelings
- **Comprehension checkpoint:** Require developer acknowledgment before accepting blocks >20 lines
- **AI-generated code labeling:** Auto-label diffs; trigger designated security reviewer for >50% AI-generated PRs
- **Vendor claim counterweight:** Built-in tooltip citing METR, GitClear, and CodeRabbit findings when developers see "2× productivity" marketing

### Be Practical (Playbooks)
- "The Augmented Coding Playbook" — 6-lesson curriculum covering the four disciplines
- Case study: How one team recovered from 6 months of accumulated AI technical debt
- Template: AI-assisted development policy for solo founders and small teams
- Calculator: Total cost of ownership worksheet (licensing + review time + security audits + refactoring)

### Builder's Club
- **Open-source Semgrep rules:** Community-maintained rules for AI-specific vulnerabilities
- **Peer review pairing:** Match members for AI code review exchange
- **Reality reporting:** Quarterly publish anonymized benchmark data from member teams using AI tools
- **Vibe Security Radar contribution:** Include AI provenance metadata in commits to enable CVE attribution

## Measurement Framework

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Perceived productivity gain | N/A | Within 10 points of measured | Monthly survey + velocity |
| Refactoring rate | 25% | Maintain ≥20% | GitClear / Git analytics |
| Code duplication | Baseline | < +3% per PR | jscpd / SonarQube |
| Security issues per AI PR | 10.83 (CodeRabbit) | < 6.45 (human baseline) | SAST + manual audit |
| Review time per AI PR | +91% vs baseline | < +30% vs baseline | Git analytics |
| CSRF coverage | 0% (Tenzai baseline) | 100% of routes | Security audit |
| Comprehension contract compliance | N/A | 100% of AI PRs | PR checklist audit |
| Refactoring budget allocation | 0% | 15% of sprint capacity | Sprint planning audit |

## Key Data Points (2026)

- **19% slower:** METR RCT on experienced developers using early-2025 AI tools on real issues
- **39-point gap:** Developers predicted 24% speedup, felt 20% faster, were objectively 19% slower
- **25% → <10%:** Refactoring collapse per GitClear longitudinal analysis of 211M lines
- **8.3% → 12.3%:** Code duplication increase (4× growth in duplication events)
- **10.83 vs 6.45:** Issues per PR in AI-generated vs human-only code (CodeRabbit)
- **2.74×:** Security vulnerabilities in AI-generated PRs vs human-only
- **3×:** Readability issues in AI-generated code vs human-only
- **100%:** Of 15 vibe-coded production apps lacked CSRF and security headers (Tenzai)
- **45%:** Of AI-generated code contains security vulnerabilities (Veracode)
- **41%:** Of global code is AI-generated; 61% in Java projects (Index.dev)
- **+154%:** PR size increase with AI adoption (Faros AI)
- **+91%:** Code review time increase with AI adoption (Faros AI)
- **+20% / +23.5%:** PRs per author up 20%, incidents per PR up 23.5% (Cortex)

## References
- See [references/metr-study-analysis.md](references/metr-study-analysis.md) for the full METR randomized controlled trial methodology and findings.
- See [references/gitclear-longitudinal-data.md](references/gitclear-longitudinal-data.md) for the 211-million-line code quality analysis.
- See [references/coderabbit-pr-analysis.md](references/coderabbit-pr-analysis.md) for the structured pull request comparison methodology.

## Sources
- METR — "How early-2025 AI tools affect experienced open-source developers' productivity" (2026)
- GitClear — "Code Quality Changes in the AI Era" (Longitudinal analysis, 2020–2024)
- CodeRabbit — "State of AI vs Human Code Generation Report" (December 2025)
- Tenzai — "AI Coding Tools Introduce 69 Vulnerabilities in 15-App Study" (December 2025)
- Cortex — Engineering pipeline observational study (2026)
- Faros AI — Delivery pipeline longitudinal analysis (2026)
- Veracode — "AI-Generated Code Poses Major Security Risks" (July 2025)
- Kent Beck — "Augmented Coding vs Vibe Coding" framework (2025–2026)
- Simon Willison — "Vibe Engineering" eleven practices (2026)
- Gary Marcus — Evidence on vibe coding declining adoption (2026)
- Index.dev — Global code generation statistics (2026)
