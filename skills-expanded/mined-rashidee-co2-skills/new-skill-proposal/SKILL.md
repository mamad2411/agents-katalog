---
name: New Skill Proposal
about: Propose a new CO2 skill before starting development
title: "feat(<skill-name>): <short description>"
labels: new-skill
assignees: rashidee
---

## Skill Name

<!-- Follow the CO2 naming convention: <prefix>-<stack>-<variant>
     e.g. specgen-django-postgres, mockgen-bootstrap, testgen-cypress -->

**Proposed name:** `<skill-name>`

## Skill Family

- [ ] `specgen-*` — Technical specification generator (highest priority)
- [ ] `modelgen-*` — Data model generator
- [ ] `mockgen-*` — UI mockup generator
- [ ] `testgen-*` — Test scaffold generator
- [ ] `util-*` — Utility / clean-up operation
- [ ] `conductor-*` — Multi-skill orchestrator

## Problem Statement

<!-- Why does this skill need to exist?
     What gap in the CO2 workflow does it address?
     Who benefits and how? -->

## Technology Stack

<!-- Be specific about versions. CO2 skills are opinionated — version pinning is intentional.
     e.g. Django 4.2 LTS + PostgreSQL 16 + Django REST Framework 3.15 + SimpleJWT 5.x -->

## CO2 Phase

<!-- Which phase of the CO2 workflow does this skill belong to?
     Context Window Preparation / PRD Clean-Up / Artifact Generation / Orchestration -->

## Prerequisites

<!-- Which context artifacts must exist before this skill can run?
     e.g. PRD.md, model/, mockup/, specification/ -->

- [ ] `CLAUDE.md`
- [ ] `PRD.md`
- [ ] `model/` output from `modelgen-*`
- [ ] `mockup/` output from `mockgen-*`
- [ ] `specification/` output from `specgen-*`
- [ ] Other: <!-- specify -->

## Input Contract

<!-- How will the skill resolve its inputs?
     Reference the CO2 standard: <app_folder>/context/ -->

## Output Contract

<!-- List every file the skill will produce and its exact path.
     Follow the CO2 directory structure convention. -->

```
<app_folder>/context/
└── specification/
    ├── <module_1>/
    │   └── SPEC.md
    └── SPECIFICATION.md
```

## Traceability

<!-- How will this skill preserve CO2 traceability tags?
     [USL000001], [NFRL000001], [CONL000001] must be traceable end-to-end. -->

## Are you willing to implement this skill?

- [ ] Yes — I will open a PR
- [ ] No — I am proposing this for someone else to pick up

## Additional Context

<!-- Reference implementations, existing frameworks, design decisions, known constraints. -->
