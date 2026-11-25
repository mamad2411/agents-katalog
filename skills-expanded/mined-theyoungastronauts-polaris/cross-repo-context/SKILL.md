---
name: cross-repo-context
description: "Bridging decoupled backend and frontend repos: pulling backend context and generating or consuming integration summaries as API contracts. Apply when working across a backend/frontend boundary."
---

# Skill: Cross-Repo Context

## Purpose
Manage context sharing between decoupled backend and frontend repositories.

## The Problem
Full-stack features span multiple repos. Claude Code works best within a single repo, but needs awareness of the other side's contracts, types, and behaviors.

## The Integration Summary Protocol

### Backend → Frontend (after backend work completes)

Generate `docs/integration/[feature-name].md` with:

```markdown
# Integration Summary: [Feature Name]
Generated: [date]
Backend Branch: [branch name]

## Endpoints

### [METHOD] /api/v1/[path]
- Auth: [required/optional/none]
- Permissions: [list]

**Request:**
```json
{ "example": "request body" }
```

**Response (200):**
```json
{ "example": "response body" }
```

**Error Responses:**
- 400: { "detail": "..." }
- 403: { "detail": "..." }

## Models Changed
- [Model]: [brief description of changes]

## Notes
- [Any special behavior, pagination details, WebSocket events, etc.]
```

### Frontend → Backend (when frontend needs backend changes)

Create a request document:
```markdown
# API Request: [Feature Name]

## What I Need
- Endpoint: [METHOD] /api/v1/[desired-path]
- Purpose: [what the frontend needs to do]

## Desired Response Shape
```json
{ "what_i_want": "..." }
```

## Context
- Which screen/component needs this
- User flow description
```

## When to Pull Backend Context Directly

Sometimes the integration summary isn't enough. Use the `context-pull.sh` script (in the Polaris repo — e.g. `~/prj/polaris/context-pull.sh ../backend-api`) to extract relevant backend code when:
- Debugging a mismatch between expected and actual API behavior
- The integration summary is outdated or incomplete
- You need to understand validation rules or business logic
- Building complex forms that need to match backend validation exactly

The script extracts serializers, views, models, and URL configs into a single context document.

## Best Practices
- Always generate/update the integration summary when backend API changes
- Frontend should never assume — verify types against actual API responses
- If the summary and reality don't match, update the summary first
- Keep summaries in version control so both repos can reference them
- When in doubt, err on the side of over-documenting the API contract
