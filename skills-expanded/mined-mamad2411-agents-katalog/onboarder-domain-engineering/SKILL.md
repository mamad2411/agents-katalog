---
name: onboarder-domain-engineering
description: Domain-level onboarding knowledge for Engineering. Covers architecture, tech stack, coding standards, and shared services across all engineering teams. Fetched at runtime by the onboarder orchestrator skill.
---

# Engineering Domain — Onboarding Knowledge

This skill provides domain-level onboarding knowledge for the **Engineering** discipline. It sits between the company-wide layer (shared by everyone) and the team-specific layer (unique to each team within engineering).

## What This Layer Covers

- **Architecture overview** — How systems in engineering are structured, key design decisions, and why they were made
- **Tech stack** — Languages, frameworks, infrastructure, and tools used across engineering
- **Standards and conventions** — Coding standards, review processes, naming conventions, documentation expectations
- **Shared services** — Internal libraries, APIs, or platforms that engineering teams share
- **Glossary** — Engineering-specific terminology used within the organisation
- **Learning path** — Recommended reading, courses, or resources for ramping up

## Knowledge Source

All domain knowledge is stored in `data/domain.json` within this repo.

## Teams in This Domain

Teams are registered in `registry.json` and fetched at runtime from their own GitHub repos.

Available teams:
- **platform** — Infrastructure, developer tooling, and platform services
