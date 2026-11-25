---
title: IT System Architecture Design
description: Skill for designing and implementing system architecture patterns including page components, state management, navigation systems, and routing in the ConstructAI platform
frequency: Per architecture change
success_rate: 90%
tags:
  - it-operations
  - system-architecture
  - component-design
  - state-management
  - navigation-patterns
  - 02050_information-technology
docs:
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/02050_information-technology/agent-data/domain-knowledge/02050_GLOSSARY.MD
  - docs_construct_ai/disciplines/02050_information-technology/01500_MASTER_GUIDE_INFORMATION_TECHNOLOGY.md
  - docs_construct_ai/skills/shared/systematic-debugging/SKILL.md
  - docs_construct_ai/skills/shared/database-schema-management/SKILL.md
---

# IT System Architecture Design

## Overview

This skill covers the design and implementation of system architecture patterns for the ConstructAI platform. It encompasses page component design, state management architecture, three-state navigation patterns, routing, modal systems, and CSS architecture. Primary agent: 02050-001 IT System Architect. Supporting skills: `shared/systematic-debugging`, `shared/database-schema-management`.

## Triggers

- New discipline page needs to be created
- Existing page architecture requires refactoring
- Navigation pattern needs enhancement or modification
- State management architecture requires updates
- Modal system needs new modal types or patterns
- CSS architecture requires overhaul or standardization

## Prerequisites

- Access to existing component library and CSS architecture
- Knowledge of ConstructAI page patterns and conventions
- Understanding of React component lifecycle and hooks
- Access to domain knowledge for target discipline
- Understanding of three-state navigation pattern

## Steps

### Step 1: Architecture Assessment
- Analyze existing architecture patterns for similar pages
- Identify reusable components and patterns
- Document constraints and dependencies
- Define scope of architectural changes needed

### Step 2: Component Design
- Design page-level component structure (container, content, controls)
- Define props interface and state requirements
- Plan subcomponent hierarchy (navigation, content area, modals)
- Design data flow between components

### Step 3: State Management Design
- Design state variables (page state, UI state, data state)
- Plan state persistence mechanisms
- Design state reset and initialization logic
- Plan cross-component state sharing if needed

### Step 4: Navigation Design
- Design navigation pattern (single-state, three-state, accordion)
- Plan navigation state transitions
- Design navigation button behavior and styling
- Implement navigation state persistence

### Step 5: Modal System Design
- Design modal types and sizing patterns
- Plan modal trigger mechanisms
- Design modal content loading strategy
- Implement modal stacking and focus management

### Step 6: CSS Architecture Design
- Design page-specific CSS modules
- Plan theme integration and variable usage
- Design responsive breakpoint strategy
- Implement background image and theming hooks

### Step 7: Integration Points Design
- Design chatbot integration points
- Design API connection requirements
- Design data loading and error boundary strategy
- Plan event handling and callbacks

### Step 8: Validation & Testing
- Validate design against existing conventions
- Create test scenarios for all state transitions
- Verify modal behavior edge cases
- Validate CSS for all screen sizes and themes

## Success Criteria

- Component design follows existing patterns and conventions
- State management handles all required state variables
- Navigation transitions are smooth and state is preserved
- Modal system handles loading, error, and cancellation states
- CSS architecture is consistent and responsive
- Integration points are properly designed and documented
- All test scenarios pass validation

## Common Pitfalls

1. **Ignoring existing patterns**: Don't reinvent patterns that exist in other pages
2. **Incomplete state design**: Consider all UI states (loading, error, empty, success)
3. **Modal state collisions**: Handle modals with same state variables
4. **CSS specificity issues**: Use consistent naming to avoid conflicts
5. **Missing error boundaries**: Always design error handling at component level
6. **No loading states**: Design skeleton/loading states for all async operations

## Cross-References

- `shared/systematic-debugging/SKILL.md` — Debugging architecture and component issues
- `shared/database-schema-management/SKILL.md` — Database schema changes from architecture updates
- `it-code-generation-scaffolding/SKILL.md` — Code generation for designed components
- `it-documentation-generation/SKILL.md` — Documentation from architecture decisions

## Usage

Use this skill when designing new discipline pages, refactoring existing pages, or creating new architectural patterns. This is the foundational skill applied before any code generation or implementation work.

## Metrics

- **Design Consistency**: 90%+ adherence to existing architecture patterns
- **State Coverage**: 100% of required states designed
- **Modal Coverage**: 100% of modal types designed for use cases
- **Test Pass Rate**: 95%+ of architecture test scenarios pass
- **Code Quality**: 90%+ of generated code passes review without changes