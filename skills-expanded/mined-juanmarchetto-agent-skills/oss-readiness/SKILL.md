---
name: oss-readiness
description: "Evaluate if your project is ready for open source. 5 specialist agents audit in parallel — licensing, documentation, security, community readiness, API surface — then synthesize a unified readiness score with prioritized fixes. Use when: open source my project, ready for open source, prepare for public release, open source checklist, publish my code, should I open source this."
license: MIT
metadata:
  version: 1.0.0
  category: evaluation
  tags: [open-source, evaluation, multi-agent, licensing, security, documentation, community]
---

# OSS Readiness — Open Source Readiness Evaluator

Evaluate whether your project is ready to be open-sourced. Five specialist agents audit your codebase simultaneously, then a synthesizer produces a unified readiness score with prioritized fixes sorted by severity.

## How It Works

Input is a project path. Five agents scan the project in parallel:

1. **License Auditor** (`agents/license-auditor.md`) — checks LICENSE file presence and type, dependency license compatibility (copyleft contamination in permissive projects), attribution requirements, patent clauses, files with conflicting license headers
2. **Documentation Reviewer** (`agents/docs-reviewer.md`) — README completeness (description, install, usage, examples, badges), CONTRIBUTING.md quality, CHANGELOG.md presence, API documentation for libraries, code comment quality on public functions, quick-start guide
3. **Security Scanner** (`agents/security-scanner.md`) — hardcoded secrets (API keys, tokens, passwords) in code, .env files not in .gitignore, secrets accidentally committed in git history, known vulnerable dependencies, debug/test credentials left in code, overly permissive file permissions
4. **Community Readiness** (`agents/community-readiness.md`) — issue templates, PR templates, CODE_OF_CONDUCT.md, governance model, onboarding friction (steps from clone to running), labels/milestones setup, first-time contributor friendliness
5. **API Surface Analyzer** (`agents/api-surface-analyzer.md`) — public API clearly defined (exports, public modules), semver compliance readiness, breaking change risk, backwards compatibility, type definitions/interfaces documented, deprecation policy

After all five agents complete, the **Synthesizer** (`agents/synthesizer.md`) combines their outputs into a unified assessment with weighted scoring, blocker identification, and a phased release plan if the project is not ready.

## Usage

```
"Is my project ready to open source? ./my-project"
"Evaluate open source readiness for this repo"
"What do I need to fix before publishing this code?"
"Prepare ./my-library for public release"
"Open source checklist for this project"
```

## Output Format

The evaluation produces a structured report:

```
OPEN SOURCE READINESS EVALUATION
Project: [name]

Overall Readiness: 7.2/10 — CONDITIONAL GO

| Dimension      | Score | Critical Issues                          |
|----------------|-------|------------------------------------------|
| Licensing      | 9/10  | MIT license, all deps compatible         |
| Documentation  | 6/10  | README good, missing CONTRIBUTING.md     |
| Security       | 4/10  | 2 hardcoded API keys found in git history|
| Community      | 5/10  | No issue templates, no CoC              |
| API Surface    | 8/10  | Stable public API, semver ready          |

BLOCKERS (fix before publishing):
1. [SECURITY] Remove API keys from git history (use BFG Repo Cleaner)
2. [SECURITY] Add .env to .gitignore

HIGH PRIORITY:
3. [DOCS] Create CONTRIBUTING.md
4. [COMMUNITY] Add issue templates
5. [COMMUNITY] Add CODE_OF_CONDUCT.md

RECOMMENDED:
6. [DOCS] Add API documentation
7. [COMMUNITY] Define governance model
```

This is followed by:
- **Blocker details** with specific fix instructions
- **Phased release plan** if the project is not ready
- **Quick wins** that can be fixed in under 30 minutes
- **Verdict**: GO / CONDITIONAL GO / NOT READY

## Agent Files

| Agent | Purpose |
|-------|---------|
| `agents/license-auditor.md` | Scans LICENSE file, dependency licenses, attribution, patent clauses |
| `agents/docs-reviewer.md` | Evaluates README, CONTRIBUTING, CHANGELOG, API docs, code comments |
| `agents/security-scanner.md` | Finds secrets, vulnerable deps, .env exposure, git history leaks |
| `agents/community-readiness.md` | Checks issue templates, CoC, governance, onboarding friction |
| `agents/api-surface-analyzer.md` | Analyzes public API stability, semver readiness, breaking changes |
| `agents/synthesizer.md` | Combines all 5 into weighted score, blockers, and release plan |

## References

| File | Content |
|------|---------|
| `references/oss-checklist.md` | Comprehensive open-source checklist organized by category, severity, and effort |

## Error Handling

- **No LICENSE found**: License Auditor flags this as a BLOCKER and recommends license selection based on project type and dependency licenses
- **No README found**: Documentation Reviewer flags as a BLOCKER and provides a README template tailored to the project
- **No git history**: Security Scanner skips history analysis but warns that uninitialized repos cannot be verified for leaked secrets; other checks proceed normally
- **No package manager**: License Auditor skips dependency license scan but notes it as a limitation; manual dependency review is recommended
- **Binary/non-code project**: API Surface Analyzer returns "Not Applicable" and the synthesizer redistributes its weight across the other four dimensions

When a dimension cannot be fully assessed, the agent returns a partial score with clear notation of what was checked vs. what was skipped. The synthesizer adjusts weights accordingly.

## Scoring Weights

The synthesizer uses weighted scoring reflecting real-world open-source risk:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Security | 30% | Leaked secrets or vulnerabilities can cause immediate harm |
| Licensing | 25% | License incompatibility can force takedowns or legal action |
| Documentation | 20% | Poor docs prevent adoption and contribution |
| API Surface | 15% | Unstable APIs cause downstream breakage |
| Community | 10% | Important but can be built incrementally post-release |

## Verdict Thresholds

| Score Range | Verdict | Meaning |
|-------------|---------|---------|
| 8.0 - 10.0 | **GO** | Ready to publish. Minor improvements optional. |
| 5.0 - 7.9 | **CONDITIONAL GO** | Publishable after fixing blockers. No showstoppers. |
| 0.0 - 4.9 | **NOT READY** | Significant work required. Phased plan provided. |

## Language

All agents respond in the same language the user writes in. Detected automatically — no configuration needed.
