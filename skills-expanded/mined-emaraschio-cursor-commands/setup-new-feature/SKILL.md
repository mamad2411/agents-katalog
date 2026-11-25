---
name: setup-new-feature
description: Scaffold a new feature across layers
user-invocable: false
---
## Overview

Systematically set up a new feature from initial planning through to implementation structure.

## Steps

1. **Define requirements**
    - Clarify feature scope and goals
    - Identify user stories and acceptance criteria
    - Plan technical approach
2. **Create feature branch**
    - Branch from main/develop
    - Set up local development environment
    - Configure any new dependencies
3. **Plan architecture**
    - Design data models and APIs
    - Plan UI components and flow
    - Consider testing strategy

## Setup New Feature Checklist

- [ ] Requirements documented
- [ ] User stories written
- [ ] Technical approach planned
- [ ] Feature branch created
- [ ] Development environment ready

## Guardrails

- Scaffold only what the feature needs now; do not over-engineer or add speculative layers.
- Match the existing project structure, naming, and conventions instead of inventing a new layout.
- Plan requirements and architecture before writing code; do not commit, push, or merge without an explicit request.