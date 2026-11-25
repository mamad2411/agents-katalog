---
name: refiner-promptforge-version-control
description: >
  Use when managing prompt versions, tracking changes, implementing iterative
  improvement processes, and maintaining prompt evolution history. This skill
  provides version control procedures specific to prompt engineering workflows.
---

# Refiner - Iterative Improvement & Version Control

## Overview
Refiner manages version control and iterative improvement for PromptForge AI. Prompts evolve over time—Refiner ensures every change is tracked, every version is recoverable, and improvements are systematic rather than ad-hoc.

## When to Use
- When making changes to an existing prompt (any change, no matter how small)
- When comparing prompt versions to understand what changed and why
- When rolling back a prompt to a previous version
- When tracking the improvement trajectory of a prompt over time
- When managing multiple variants of a prompt for different use cases
- **Don't use when:** Creating a brand-new prompt with no prior version

## Core Procedures

### Step 1: Version Before Changing
Before any prompt modification:
1. Record current version number (semver: MAJOR.MINOR.PATCH)
2. Document what the current version does well
3. Document known issues with current version
4. Create version snapshot (full prompt text + metadata)

### Step 2: Plan the Change
```
CHANGE PLAN
===========
Prompt: [name and current version]
Change Type: [major/minor/patch]
Reason: [why this change is needed]
What Changes: [specific sections to modify]
Expected Impact: [how this should improve the prompt]
Risk: [what could go wrong]
Rollback Plan: [how to revert if needed]
```

### Step 3: Implement Change
- Make the planned changes only (don't scope creep)
- Update version number according to change type:
  - **MAJOR:** Breaking change (output format changes, behavior fundamentally different)
  - **MINOR:** New capability added (backward compatible)
  - **PATCH:** Bug fix, clarification, typo correction
- Update changelog entry

### Step 4: Validate Change
- [ ] New version produces expected output
- [ ] New version doesn't regress on previous capabilities
- [ ] Change is documented in changelog
- [ ] Previous version is archived and recoverable
- [ ] Stakeholders notified of the change

### Step 5: Track Improvement Over Time
Maintain prompt improvement history:
```
PROMPT VERSION HISTORY
======================
Prompt: [name]
Version | Date | Change Type | Reason | Result | Next Action
--------|------|-------------|--------|--------|----------
v1.0.0  | ...  | Initial     | ...    | ...    | ...
v1.1.0  | ...  | Minor       | ...    | ...    | ...
```

## Success Metrics
- Version tracking: 100% of prompt changes have version records
- Rollback success rate: 100% (any version can be recovered)
- Change documentation: 100% of changes have documented reason and result
- Average improvement cycle: <1 week from issue identification to fix deployment

## Error Handling
- **Error:** New version performs worse than previous version
  **Response:** Rollback immediately, investigate why change degraded performance, revise change plan
- **Error:** Change introduces unexpected behavior in edge cases
  **Response:** Rollback, add edge case to test suite, redesign change to handle edge case
- **Error:** Multiple conflicting versions exist (version drift)
  **Response:** Identify authoritative version, archive conflicting versions, establish single source of truth

## Cross-Team Integration
**Related Skills:** blueprint-promptforge-template-designer, validator-promptforge-syntax-logic-validation, version-control-best-practices, regression-prevention
**Used By:** Blueprint, Validator, ALL agents modifying existing prompts