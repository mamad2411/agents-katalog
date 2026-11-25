---
name: skill-project-onboarding
description: Build the initial project brain by scanning architecture, services, stack, dependencies, environment, and test policy.
category: workflow
---

# Skill: Project Onboarding

Use when `.maestro/knowledge/project.yaml` is missing, stale, or incomplete.

## Scan order

```text
Root metadata and package/workspace files
Application and service folders
Entry points
Shared libraries
Database and migration locations
API/event/schema contracts
CI/CD and environment files without reading secrets
Existing tests and test commands
Coding conventions from repeated patterns
```

## Output

```text
project.yaml
.maestro/knowledge/index.yaml
.maestro/registry/components.yaml
.maestro/knowledge/test-policy.yaml
.maestro/knowledge/components/<component-id>.yaml
agent candidates requiring user approval
```

## Do not

```text
Do not modify source code.
Do not generate coder agents.
Do not assume unit tests are required without evidence.
Do not copy secret values into memory.
```

## Deep project intelligence scan

Onboarding must go deeper than stack and service detection. It must also extract reusable project knowledge that prevents generated coders from rewriting existing patterns.

Scan and record:

- Reusable utilities, shared components, base classes, hooks, middleware, validators, mappers, serializers, API clients, repositories, transaction helpers, event helpers, payment helpers, notification helpers, and test helpers.
- Project coding flow: request lifecycle, command/use-case lifecycle, data access flow, transaction flow, event publish/consume flow, error flow, logging flow, migration flow, and test flow.
- Business and technical flows: entrypoints, services, steps, data entities, external integrations, emitted events, consumed events, critical checks, and reusable assets used by the flow.
- Conventions: folder structure, naming rules, layering rules, API rules, validation rules, error handling rules, logging rules, transaction rules, testing rules, environment/config rules.
- Anti-patterns: repeated patterns the project clearly avoids, plus safer existing alternatives.

Evidence requirement:

- Every reusable asset or convention must include source paths and confidence.
- Do not claim a convention from one isolated file unless confidence is low or user confirms it.
- Prefer repeated usage evidence over guesswork.
- Do not paste large source code into memory. Store path, purpose, when to reuse, and evidence only.

Output targets:

- Structured summary in .maestro/knowledge/project.yaml under deep_project_intelligence.
- Component-specific details in .maestro/knowledge/components/<component-id>.yaml under component_deep_intelligence.
- Service path and coding boundary contracts in .maestro/registry/components.yaml.
- Human-readable reusable assets in .maestro/memory/project/common/generics.md.
- Human-readable conventions in .maestro/knowledge/conventions.md.
- Business/technical flows in .maestro/knowledge/architecture.md.
- Selective-read routing metadata in .maestro/knowledge/index.yaml.
