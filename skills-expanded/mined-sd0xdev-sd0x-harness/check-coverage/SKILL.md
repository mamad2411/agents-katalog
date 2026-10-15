---
name: check-coverage
description: "Comprehensive assessment of Unit / Integration / E2E three-layer test coverage, identify gaps and provide actionable recommendations."
allowed-tools: Read, Grep, Glob, Bash(ls:*), Bash(find:*), Bash(wc:*), Agent
---

# Test Coverage Analysis

## Trigger

- Keywords: check coverage, test coverage, coverage analysis, coverage gaps, check-coverage

## When NOT to Use

- Test sufficiency review via Codex (use `/codex-test-review`)
- Generating tests (use `/codex-test-gen`)
- Running tests (use `/verify`)

## Parent Skill Reference

See `@skills/test-review/SKILL.md` for Codex-based test review workflow.

## Agent Dispatch

```
Agent({
  description: "Assess three-layer test coverage and identify gaps",
  subagent_type: "coverage-analyst",
  prompt: `Assess Unit / Integration / E2E test coverage for the feature docs at: $ARGUMENTS
Follow the steps defined in this skill.`
})
```

## Task

### Step 1: Read Feature Documentation

Read specified feature docs. Extract:
- Feature name and objectives
- Involved Service / Provider / Entity
- Core flows and boundary conditions

### Step 2: Identify Related Source Code

Search related source code based on feature documentation. Build source code inventory.

### Step 3: Map Test Files

Check whether each source file has corresponding tests (unit, integration, e2e).

### Step 4: Analyze Coverage Gaps

For each source file:
1. Read source: Identify public methods, important branches, error handling
2. Read tests: Identify covered cases
3. Compare gaps: missing methods, uncovered branches, untested error scenarios

### Step 5: Classify and Recommend

| Severity | Description |
|----------|-------------|
| 🔴 Critical | Core logic, data writes, amount calculations |
| 🟠 Major | Important branches, error handling |
| 🟡 Minor | Edge cases, utility functions |
| ⚪ Nice-to-have | Logging, formatting |

## Output

```markdown
# Test Coverage Analysis Report

## Feature Overview
- Feature name: <from documentation>
- Documentation path: $ARGUMENTS
- Related modules: <list>

## Current Coverage
| Module | Source Path | Test Path | Coverage Status |
|--------|------------|-----------|----------------|

## Coverage Gaps
### 🔴 Critical
### 🟠 Major
### 🟡 Minor

## Recommended New Tests
| Priority | Test Type | Test Case | Target File |
|----------|-----------|-----------|-------------|

## Coverage Summary
| Metric | Status |
|--------|--------|
| Feature coverage | X/Y (Z%) |
| Happy path | ✅/❌ |
| Error path | ✅/❌ |
| Edge cases | ✅/❌ |
```
