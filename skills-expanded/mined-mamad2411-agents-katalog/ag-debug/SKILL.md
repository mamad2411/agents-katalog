---
name: ag-debug
description: Debug systematically with root cause analysis before fixes. Use for bugs,
  test failures, unexpected behavior, performance issues, call stack tracing, multi-layer
  validation, log analysis, CI/CD failures, database diagnostics, system investigation.
---


# Debugging & System Investigation

Comprehensive framework combining systematic debugging, root cause tracing, defense-in-depth validation, verification protocols, and system-level investigation (logs, CI/CD, databases, performance).

## Core Principle

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

Random fixes waste time and create new bugs. Find root cause, fix at source, validate at every layer, verify before claiming success.

## When to Use

**Code-level:** Test failures, bugs, unexpected behavior, build failures, integration problems
**System-level:** Server errors, CI/CD pipeline failures, performance degradation, database issues, log analysis
**Always:** Before claiming work complete

## Techniques

### 1. Systematic Debugging (`references/systematic-debugging.md`)

Four-phase framework: Root Cause Investigation → Pattern Analysis → Hypothesis Testing → Implementation. Complete each phase before proceeding. No fixes without Phase 1.

**Load when:** Any bug/issue requiring investigation and fix

### 2. Root Cause Tracing (`references/root-cause-tracing.md`)

Trace bugs backward through call stack to find original trigger. Fix at source, not symptom. Includes `scripts/find-polluter.sh` for bisecting test pollution.

**Load when:** Error deep in call stack, unclear where invalid data originated

### 3. Defense-in-Depth (`references/defense-in-depth.md`)

Validate at every layer: Entry validation → Business logic → Environment guards → Debug instrumentation

**Load when:** After finding root cause, need comprehensive validation

### 4. Verification (`references/verification.md`)

**Iron law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE. Run command. view_file output. Then claim result.

**Load when:** About to claim work complete, fixed, or passing

### 5. Investigation Methodology (`references/investigation-methodology.md`)

Five-step structured investigation for system-level issues: Initial Assessment → Data Collection → Analysis → Root Cause ID → Solution Development

**Load when:** Server incidents, system behavior analysis, multi-component failures

### 6. Log & CI/CD Analysis (`references/log-and-ci-analysis.md`)

Collect and analyze logs from servers, CI/CD pipelines (GitHub Actions), application layers. Tools: `gh` CLI, structured log queries, correlation across sources.

**Load when:** CI/CD pipeline failures, server errors, deployment issues

### 7. Performance Diagnostics (`references/performance-diagnostics.md`)

Identify bottlenecks, analyze query performance, develop optimization strategies. Covers database queries, API response times, resource utilization.

**Load when:** Performance degradation, slow queries, high latency, resource exhaustion

### 8. Reporting Standards (`references/reporting-standards.md`)

Structured diagnostic reports: Executive Summary → Technical Analysis → Recommendations → Evidence

**Load when:** Need to produce investigation report or diagnostic summary

### 9. Task Management (`references/task-management-debugging.md`)

Track investigation pipelines via Claude Native Tasks (TaskCreate, TaskUpdate, TaskList). Hydration pattern for multi-step investigations with dependency chains and parallel evidence collection. **Fallback:** Task tools are CLI-only — if unavailable (VSCode extension), use `TodoWrite` for tracking. Debug workflow remains fully functional.

**Load when:** Multi-component investigation (3+ steps), parallel log collection, coordinating debugger subagents

### 10. Frontend Verification (`references/frontend-verification.md`)

Visual verification of frontend implementations via `ag-agent-browser`, `ag-chrome-profile`, Chrome MCP / `chrome-devtools-mcp`, or project-native browser tests. Use `ag-chrome-profile` and its exact tab binding when real Chrome profile state matters; raw Chrome MCP navigation is only for generic/profile-independent inspection. Detect if frontend-related → check browser tool availability → screenshot + console error check → report. Skip if not frontend.

**Load when:** Implementation touches frontend files (tsx/jsx/vue/svelte/html/css), UI bugs, visual regressions

## Quick Reference

```
Code bug       → systematic-debugging.md (Phase 1-4)
  Deep in stack  → root-cause-tracing.md (trace backward)
  Found cause    → defense-in-depth.md (add layers)
  Claiming done  → verification.md (verify first)

System issue   → investigation-methodology.md (5 steps)
  CI/CD failure  → log-and-ci-analysis.md
  Slow system    → performance-diagnostics.md
  Need report    → reporting-standards.md

Frontend fix   → frontend-verification.md (agent-browser/chrome-profile/Chrome MCP)
```

## Tools Integration

- **Database:** `psql` for PostgreSQL queries and diagnostics
- **CI/CD:** `gh` CLI for GitHub Actions logs and pipeline debugging
- **Codebase:** `ag-docs-seeker` skill for package/plugin docs; `ag-repomix` skill for codebase summary
- **Scouting:** `/ag-scout` or `/ag-scout ext` for finding relevant files
- **Frontend:** `ag-agent-browser`, `ag-chrome-profile`, Chrome MCP / `chrome-devtools-mcp`, or project-native browser tests for visual verification. For real profile state, let `chrome-profile open --json` create the tab and bind to its returned selector before using MCP inspection tools.
- **Skills:** Activate `ag-problem-solving` skill when stuck on complex issues

## Red Flags

Stop and follow process if thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "It's probably X, let me fix that"
- "Should work now" / "Seems fixed"
- "Tests pass, we're done"

**All mean:** Return to systematic process.

## Workflow Position

**Typically follows:** `/ag-scout` (after locating relevant code)
**Typically precedes:** `/ag-fix` (fix the diagnosed issue), `/ag-brainstorm` (explore solutions for complex problems)
**Related:** `/ag-scout` (discover before debugging), `/ag-fix` (fix after diagnosing)
