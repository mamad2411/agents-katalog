---
name: lyra-analyze-codebase
description: "Read-only codebase analysis across architecture, security, performance, and code quality, producing a severity-ranked report with evidence-backed findings."
metadata:
  version: "1.0.0"
  author: "Alexandru Miron"
compatibility: "Read-only tools only (Read, Grep, Glob, LS, non-mutating Bash). Never Edit/Write/MultiEdit. Optional: lyra-debug for bug root-cause, lyra-clean-architecture for architecture assessment, lyra-code-review for diff-level review."
---

# lyra-analyze-codebase

## What it does

Walks any codebase — language-agnostic, read-only — across four dimensions: architecture, security, performance, and code quality. A five-phase workflow (map → patterns → risks → prioritize → report) produces a structured, severity-ranked report with evidence-backed findings, not a bullet dump. Each finding cites a file and line, earns a P0–P3 severity, and carries a specific recommendation. When the analysis surfaces bugs it points to `lyra-debug` with the file; when architecture is the concern it points to `lyra-clean-architecture` with the boundary — both with concrete references, never as vague advice.

## The workflow

1. **Map structure** — `LS` the root, `Glob` manifests and entry points, read key manifests to identify languages, frameworks, build system, test setup, CI.
2. **Identify patterns** — `Grep` for routes/controllers/services/repositories, read representative files, trace data flow, locate cross-cutting concerns (auth, logging, validation, config).
3. **Find risks** — `Grep` for hardcoded secrets, injection, N+1 queries, sync I/O in hot paths, `TODO`/`FIXME`, bare catches, oversized files; read lockfiles for outdated or vulnerable dependencies.
4. **Prioritize** — read surrounding context to verify each finding, assign final P0–P3 severity, group by dimension, order P0 first, de-duplicate, cluster by root cause.
5. **Produce the report** — fill the template below; write the Executive Summary last, after every finding is prioritized.

## The rules

### 1. Read-only, no exceptions.

Never use `Edit`, `Write`, `MultiEdit`, or mutating `Bash` on the target codebase. A modified codebase can't be trusted as an analysis target — if you change a file to "check the fix," every prior finding is suspect.

### 2. Evidence or it doesn't exist.

Every finding cites a specific file path and line range — `Grep` to locate, `Read` to confirm, then cite `path/to/file.ext:42–58`. "The codebase has security issues" with no file is speculation, not a finding.

### 3. Verify before reporting.

A `Grep` match is a lead, not a finding — `password` in `passwordMinLength = 8` is not a hardcoded secret, `eval` in a comment is not code execution. Read the surrounding context before classifying; one false positive makes the reader doubt every true positive.

bad: report `password` in a variable name as a hardcoded secret.
good: read the line, see `passwordMinLength = 8`, drop the finding.

### 4. Severity is earned.

P0 = exploitable vuln, data loss, or crashing bug on a critical path; P1 = significant weakness or architectural flaw; P2 = tech debt and code quality; P3 = style. Don't inflate to seem thorough or deflate to seem reassuring — both are dishonest.

bad: calling everything P0 so the report feels urgent.
good: a hardcoded production database password is P0; a missing docstring is P3.

### 5. Every finding has a recommendation.

If you can't name a specific fix, you don't understand the finding well enough to report it. "Improve security" is a complaint, not a recommendation.

bad: "Improve security."
good: "Replace the hardcoded API key with `process.env.API_KEY` and add it to `.env.example`."

### 6. Discover the stack, don't assume it.

Don't run TypeScript patterns on a Python repo. Read the manifests in Phase 1, then choose language-agnostic `Grep` patterns — the same skill handles a Go monolith, a Python ML repo, and a PHP e-commerce site.

### 7. The report is the product, not a bullet dump.

Follow the template — sections, findings with all required fields, a prioritized recommendations list. "Here's what I noticed:" followed by 30 bullets is a brain dump, not analysis.

### 8. Phases run in order.

Map before patterns, patterns before risks, risks before prioritization, prioritization before report. A security finding in a module you haven't mapped is a guess about what the module does.

### 9. Executive summary first, written last.

It stands alone — a reader who reads only the summary should understand the codebase's health, top risks, and recommended actions. Write it after every finding is prioritized.

### 10. Quantify where you can.

Use read-only `Bash` (`wc -l`, `find ... | wc -l`, `git log --oneline | wc -l`) for file counts, LOC, test-to-source ratio, TODO counts. "42 TODOs" beats "many TODOs."

### 11. Lead with P0s.

A single P0 buried under ten P3s is a failed report. Within each category, order findings P0 → P3; the prioritized recommendations list puts P0s at the top.

### 12. Recommend integrations with a file reference.

When you find bugs, point to `lyra-debug` with the specific files and symptoms; when architecture is the concern, point to `lyra-clean-architecture` with the specific boundaries. "Consider lyra-debug" without a file is not a recommendation.

## The report

```
# Codebase Analysis Report: [Project Name]
**Date:** [date] | **Path:** [root] | **Languages:** [langs] | **Frameworks:** [frameworks]

## 1. Executive Summary
[2–3 paragraphs: overall health, key strengths, top risks by severity. Stands alone.]

| P0 | P1 | P2 | P3 |
|----|----|----|----|
| N  | N  | N  | N  |

## 2. Codebase Overview
- **Structure:** [directory map or tree]
- **Stack:** [languages, frameworks, build tools, databases, CI]
- **Entry points:** [file paths]
- **Metrics:** [file count, LOC, test-to-source ratio, TODO count]

## 3. Architecture Analysis
[Style, patterns, data flow, boundary assessment, strengths, concerns]

## 4. Findings

### Security
#### [S1] P0 — [Title]
- **File:** `path/to/file.ext:42–58`
- **Description:** [what the issue is]
- **Impact:** [what could go wrong]
- **Recommendation:** [specific, actionable fix]
[...ordered P0 → P3; same format for Performance (P#), Code Quality (Q#), Dependencies & Config (D#)]

## 5. Prioritized Recommendations
1. **[P0]** [Action] — refs: S1, S2
2. **[P1]** [Action] — refs: P1, Q3

## 6. Recommended Next Steps
- **lyra-debug:** [specific findings warranting root-cause debugging, with file refs]
- **lyra-clean-architecture:** [architecture concerns warranting full assessment, with file refs]
```

---

_Part of the [skill collection](../README.md)._