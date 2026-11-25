---
name: create-api
description: Use when creating or changing backend API endpoints; requires domain rules, edge cases, team conventions, incident review, implementation, and verification before completion.
---

# Purpose

Reusable workflow for API implementation.

# Required Knowledge

- `ai-workspace/70-knowledge/company/`
- `ai-workspace/70-knowledge/teams/ai-agents/conventions.md`
- `ai-workspace/70-knowledge/domains/{domain}/business-rules.md`
- `ai-workspace/70-knowledge/domains/{domain}/edge-cases.md`
- `ai-workspace/70-knowledge/incidents/`

# Inputs

- endpoint
- request payload
- response model
- auth and permission requirements
- domain name
- verification expectation

# Workflow

1. Load required knowledge.
2. Validate business rules.
3. Validate edge cases and related incidents.
4. Identify existing API style and contracts.
5. Generate or update DTO/request/response models.
6. Generate or update controller/route handler.
7. Generate or update service interaction.
8. Generate or update tests.
9. Generate documentation or examples if the project already uses them.
10. Verify consistency.
11. Append logs if necessary.

# Safety Rules

- Never ignore domain edge cases.
- Preserve existing API contracts unless explicitly asked to change them.
- Preserve naming and response conventions.
- Do not run migrations without human approval.
- Do not hide failed verification.

# Incident References

- Check incidents for retries, duplicated execution, reconnects, partial failures, auth bypass, and timeout retry loops.

# Output

- implementation artifact
- verification summary
- related task/log references

# Verification

- Relevant tests or build checks passed.
- API contract impact reviewed.
- Business rules and edge cases documented or linked.
