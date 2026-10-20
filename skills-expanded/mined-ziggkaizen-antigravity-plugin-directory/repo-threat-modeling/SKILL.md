---
name: repo-threat-modeling
description: Creates lightweight threat models for repository changes, new features, trust boundaries, external integrations, sensitive data flows, and security-sensitive architecture decisions. Use before implementing high-risk features or reviewing major design changes.
---

# Repo Threat Modeling

Use this skill to reason about threats before or during implementation.

## When to Use This Skill

Use this skill for:

- new APIs, services, jobs, integrations, webhooks, callbacks, or data pipelines
- authentication, authorization, roles, permissions, tenant boundaries, or admin paths
- file upload/download, URL fetching, redirects, or user-controlled paths
- payment, billing, personal data, customer data, or regulated data handling
- new external dependencies or third-party services
- infrastructure, deployment, CI/CD, or runtime boundary changes

## Lightweight Threat Modeling Process

1. Define the feature or change.
2. Identify actors.
3. Identify assets and sensitive data.
4. Identify trust boundaries.
5. Identify entry points and exit points.
6. Identify misuse cases.
7. Identify controls and missing controls.
8. Define security tests and monitoring signals.
9. Record open questions.

## Workflows

Use `workflows/repo-threat-model-workflow.md` for a structured threat-model pass.

## Resources

Use:

```text
resources/threat-model-template.md
resources/trust-boundary-checklist.md
```
