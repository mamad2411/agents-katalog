---
name: validator-promptforge-syntax-logic-validation
description: >
  Use when validating prompt syntax, checking logical consistency, verifying prompt
  structure, and ensuring prompts are well-formed before execution. This skill provides
  systematic validation procedures to catch prompt errors before they reach production.
---

# Validator - Syntax & Logic Validation

## Overview
Validator validates prompt syntax and logic for PromptForge AI. A single syntax error, unclosed bracket, or logical contradiction can cause a prompt to fail silently or produce garbage output. Validator catches these issues before prompts reach production.

## When to Use
- Before deploying any new prompt to production
- After modifying an existing prompt (even small changes)
- When troubleshooting unexpected prompt behavior
- When reviewing prompts created by other agents
- When building automated prompt validation pipelines
- **Don't use when:** Testing prompt output quality (use quantifier-promptforge-benchmarking)

## Core Procedures

### Step 1: Syntax Validation
Check the prompt's structural integrity:
- [ ] All brackets, braces, and quotes are properly closed
- [ ] Variable placeholders use consistent syntax (`{{variable}}` or `{variable}`)
- [ ] No orphaned or dangling references (references to undefined variables)
- [ ] Markdown/formatting syntax is valid
- [ ] No invisible characters or encoding issues
- [ ] Prompt length is within model limits

### Step 2: Logical Consistency Check
Verify the prompt makes logical sense:
- [ ] Instructions don't contradict each other
- [ ] Output format specification is achievable
- [ ] Constraints are mutually compatible (e.g., not "be brief" AND "include all details")
- [ ] Role definition is consistent with instructions
- [ ] Examples match the described behavior
- [ ] Edge cases are handled (what if input is empty? too long?)

### Step 3: Completeness Check
Ensure nothing critical is missing:
- [ ] System role is defined
- [ ] Task/instructions are present
- [ ] Input format is specified
- [ ] Output format is specified
- [ ] Constraints and guardrails are included
- [ ] Error handling instructions (what to do if input is invalid)

### Step 4: Model Compatibility Check
Verify the prompt will work with target models:
- [ ] Prompt length fits within model's context window
- [ ] No model-specific features used incorrectly
- [ ] Temperature and other parameters are valid for the model
- [ ] Special tokens or formatting are supported by the model

### Step 5: Validation Report
```
VALIDATION REPORT
=================
Prompt: [name and version]
Validator: [agent name]
Date: [validation date]
Syntax: [PASS/FAIL - issues found]
Logic: [PASS/FAIL - issues found]
Completeness: [PASS/FAIL - issues found]
Model Compatibility: [PASS/FAIL - issues found]
Overall: [PASS/FAIL]
Issues: [list of all issues with severity]
  - [CRITICAL] [issue description]
  - [WARNING] [issue description]
  - [INFO] [issue description]
Recommendation: [deploy/fix before deploy]
```

## Success Metrics
- Validation coverage: 100% of production prompts pass validation
- Critical issue detection: 100% of syntax errors caught before deployment
- False positive rate: <5% (valid prompts incorrectly flagged)
- Validation time: <5 minutes per prompt

## Error Handling
- **Error:** Critical syntax issue found
  **Response:** Do NOT deploy, fix the syntax issue, re-validate
- **Error:** Logical contradiction found
  **Response:** Do NOT deploy, resolve the contradiction (clarify which instruction takes priority), re-validate
- **Error:** Prompt passes validation but still produces poor output
  **Response:** Validation catches syntax/logic issues, not quality issues—transfer to clarity-promptforge-performance-optimization for quality improvement

## Cross-Team Integration
**Related Skills:** blueprint-promptforge-template-designer, refiner-promptforge-version-control, integration-promptforge-cross-agent-compatibility, output-validation-checklist
**Used By:** Blueprint, Refiner, Integration, ALL agents creating or modifying prompts