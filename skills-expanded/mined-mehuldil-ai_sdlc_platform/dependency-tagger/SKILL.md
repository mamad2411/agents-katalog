---
name: dependency-tagger
description: Auto-tag cross-team dependencies and track blocker relationships
model: haiku-4-5
token_budget: {input: 2000, output: 800}
---

# Dependency Tagger Skill

Automatically identify and tag cross-team dependencies in work items.

## Dependency Types

- **Blocks**: This blocks another team
- **Blocked By**: Waiting on another team
- **Feeds**: Provides data/services to team
- **Fed By**: Consumes data/services from team
- **Integrates With**: Cross-team integration point

## Detection Patterns

- References to other team's components
- Mentions of external APIs
- Dependencies on shared services
- Cross-pod feature coordination
- Platform/backend dependencies

## Triggers

Use this skill when:
- Story mentions cross-team work
- Epic planning with multiple teams
- Dependency mapping needed
- Pre-grooming brief creation

## Inputs

- Story/epic description
- Team list
- Service registry/architecture

## Outputs

- Tagged dependencies in ADO
- Dependency matrix
- Critical path identification
- Risk assessment

## Quality

- Accurate team assignment
- Clear dependency type
- Proper work item linking
- Complete coverage
