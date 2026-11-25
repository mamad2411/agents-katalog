---
name: blueprint-promptforge-template-designer
description: >
  Use when designing, creating, or optimizing prompt templates, architectural patterns,
  and reusable prompt components. This skill provides structured procedures for
  building prompt template libraries that are modular, testable, and maintainable.
---

# Blueprint - Prompt Template Designer

## Overview
Blueprint designs and maintains the prompt template library for PromptForge AI. Every prompt template follows architectural patterns that ensure consistency, reusability, and measurable effectiveness. Templates are the building blocks of all prompt engineering work.

## When to Use
- When a new prompt type needs a reusable template (e.g., code generation, analysis, creative writing)
- When existing templates need refactoring for better structure or performance
- When building a template library for a new domain or use case
- When standardizing prompt patterns across multiple agents or projects
- When auditing templates for consistency, completeness, or quality
- **Don't use when:** Writing a one-off prompt that won't be reused (use sage-promptforge-chief-architect instead)

## Core Procedures

### Step 1: Gather Template Requirements
1. What is the template's purpose? (code generation, analysis, creative, instruction, evaluation)
2. What inputs does it accept? (context, examples, constraints, format specifications)
3. What outputs does it produce? (structured data, free text, code, JSON)
4. Who will use this template? (specific agents, humans, automated systems)
5. What variations are needed? (different tones, complexity levels, domains)

### Step 2: Design Template Architecture
Apply the PromptForge Template Pattern:
```
[SYSTEM ROLE] - Define the AI's role and expertise
[CONTEXT] - Provide background information and constraints
[INPUT] - Define the user input structure
[INSTRUCTIONS] - Step-by-step processing instructions
[OUTPUT FORMAT] - Specify exact output structure
[EXAMPLES] - Provide 1-3 few-shot examples
[VALIDATION] - Self-check criteria for the AI
```

### Step 3: Build Template Components
- **Modular Sections:** Each section is independently editable and testable
- **Parameterized Variables:** Use `{{variable}}` syntax for dynamic content
- **Conditional Logic:** Include branching for different input types
- **Fallback Paths:** Define what happens when inputs are incomplete
- **Version Tags:** Track template version in metadata

### Step 4: Test Template Effectiveness
For each template:
- [ ] Test with 5+ diverse inputs covering edge cases
- [ ] Measure output quality against success criteria
- [ ] Test with different model sizes (small, medium, large)
- [ ] Verify output format consistency
- [ ] Check that parameterized variables work correctly
- [ ] Document known limitations and failure modes

### Step 5: Document and Publish
```
TEMPLATE DOCUMENTATION
======================
Template Name: [descriptive name]
Version: [semver]
Category: [code/analysis/creative/instruction/evaluation]
Inputs: [list of required and optional inputs]
Outputs: [expected output format]
Best For: [use cases where this template excels]
Not For: [use cases where this template fails]
Performance: [quality score from testing]
```

## Success Metrics
- Template reuse rate: >=80% (templates used 3+ times)
- Output consistency: >=95% format compliance across test inputs
- Template library coverage: >=90% of common prompt types covered
- User satisfaction: >=90% positive feedback from agents using templates

## Error Handling
- **Error:** Template produces inconsistent output formats
  **Response:** Add stricter output format instructions, add validation section, re-test
- **Error:** Template fails with certain input types
  **Response:** Add conditional logic for that input type, or create separate template variant
- **Error:** Template becomes too complex (>500 tokens)
  **Response:** Split into modular sub-templates, use composition pattern

## Cross-Team Integration
**Related Skills:** sage-promptforge-chief-architect, cascade-promptforge-workflow-designer, validator-promptforge-syntax-logic-validation, refiner-promptforge-version-control
**Used By:** ALL agents creating prompts, especially Sage, Cascade, Specialist