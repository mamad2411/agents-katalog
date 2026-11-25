---
title: IT Code Generation & Scaffolding
description: Skill for template-based code generation with AST validation, React component scaffolding, and code quality enforcement in the ConstructAI platform
frequency: Per code generation task
success_rate: 85%
tags:
  - it-operations
  - code-generation
  - scaffolding
  - react-components
  - ast-validation
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/skills/shared/test-driven-development/SKILL.md
  - docs_construct_ai/skills/shared/testing-verification/SKILL.md
  - docs_construct_ai/skills/domainforge_ai/it-system-architecture-design/SKILL.md
---

# IT Code Generation & Scaffolding

## Overview

This skill covers template-based code generation and scaffolding for the ConstructAI platform. It encompasses React component generation, CSS module scaffolding, API handler templates, form component templates, and code quality validation through AST parsing. Primary agent: 02050-003 Code Forge. Supporting skills: `shared/test-driven-development`, `shared/testing-verification`.

## Triggers

- New page component needs to be created
- Existing component needs refactoring pattern applied
- New modal type needs implementation scaffold
- API integration requires handler generation
- Form or modal interface needs code scaffolding
- CSS modules need to be created for new components

## Prerequisites

- Architecture design completed (from `it-system-architecture-design`)
- Design system and component conventions available
- Target file structure and naming conventions defined
- Linting and formatting rules accessible

## Steps

### Step 1: Template Selection
- Identify appropriate template for component type (page, container, modal, form, API handler, utility)
- Select based on architecture design specifications
- Check template currency and validity
- Load template into generation context

### Step 2: Data Injection
- Map template variables to actual values (component name, props, state variables, API endpoints)
- Inject structured data from architecture design
- Validate all placeholders are mapped
- Handle conditional template sections based on requirements

### Step 3: Code Generation
- Generate code from populated template
- Apply consistent naming conventions (kebab-case files, PascalCase components, camelCase variables)
- Ensure import paths are correct and resolve to existing modules
- Generate CSS module following existing patterns

### Step 4: AST Validation
- Parse generated code through AST parser
- Validate syntax correctness
- Check import resolution and module dependencies
- Verify component structure matches React conventions
- Flag any AST validation failures

### Step 5: Quality Validation
- Run ESLint check on generated code
- Verify TypeScript strict compliance
- Check for accessibility patterns (aria attributes, keyboard navigation)
- Validate responsive design patterns in CSS
- Run test generation if applicable

### Step 6: Integration Validation
- Verify generated code integrates with existing navigation patterns
- Check accordion component integration if applicable
- Verify chatbot integration points
- Validate modal container integration
- Confirm state management connections

### Step 7: Documentation Generation
- Generate JSDoc comments for component functions
- Generate component usage examples
- Update related documentation files
- Tag generated code with provenance

### Step 8: Output & Filing
- Write generated files to correct locations
- Create any necessary directories
- Run formatting enforcement (Prettier)
- Verify no existing files are overwritten unexpectedly

## Success Criteria

- Generated code passes all AST validation checks
- Code passes ESLint and TypeScript strict mode
- All imports resolve correctly
- Generated component integrates with existing patterns
- CSS module follows existing naming and structure conventions
- Test cases are generated or scaffolded
- Documentation is created alongside generated code

## Common Pitfalls

1. **Incorrect import paths**: Generated imports may reference non-existent modules — always verify
2. **CSS naming conflicts**: Unique module names prevent specificity collisions
3. **Missing state handling**: Ensure all required state variables are scaffolded
4. **No error boundaries**: Always scaffold error boundaries with new components
5. **Template staleness**: Verify templates match current architecture patterns before generation
6. **AST parse failures**: Check generated syntax before accepting code

## Cross-References

- `shared/test-driven-development/SKILL.md` — TDD patterns for generated components
- `shared/testing-verification/SKILL.md` — Test validation for generated code
- `it-system-architecture-design/SKILL.md` — Architecture design input for code generation
- `it-documentation-generation/SKILL.md` — Documentation creation for generated code

## Usage

Use this skill when generating new code components, refactoring existing components, creating API handlers, or scaffolding forms and modals. Apply after architecture design is complete and before code review.

## Metrics

- **Generation Accuracy**: 85%+ of generated code passes validation without manual edits
- **AST Pass Rate**: 95%+ of generated code passes AST validation
- **Test Generation Rate**: 80%+ test coverage for generated components
- **Import Resolution**: 100% of generated imports resolve correctly
- **Documentation Coverage**: 90%+ of generated code has JSDoc comments