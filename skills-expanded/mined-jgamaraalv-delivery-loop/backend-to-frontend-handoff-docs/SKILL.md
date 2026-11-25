---
name: backend-to-frontend-handoff-docs
description: Create API handoff documentation for frontend developers. Use when backend work is complete and needs to be documented for frontend integration, or user says 'create handoff', 'document API', 'frontend handoff', or 'API documentation'.
---

# API Handoff Mode

> **No Chat Output**: Produce the handoff document only. No discussion, no explanation—just the markdown block saved to the handoff file.

You are a backend developer completing API work. Your task is to produce a structured handoff document that gives frontend developers (or their AI) full business and technical context to build integration/UI without needing to ask backend questions.

> **Simple API shortcut**: If the API is straightforward (CRUD, no complex business logic, obvious validation), skip the full template—just provide the endpoint, method, and example request/response JSON. Frontend can infer the rest.

## Goal
Produce a copy-paste-ready handoff document with all context a frontend AI needs to build UI/integration correctly and confidently.

## Inputs
- Completed API code (endpoints, controllers, services, DTOs, validation).
- Related business context from the task/user story.
- Any constraints, edge cases, or gotchas discovered during implementation.

## Workflow

1. **Collect context** — confirm feature name, relevant endpoints, DTOs, auth rules, and edge cases.
2. **Create/update handoff file** — write the document to `.claude/docs/ai/<feature-name>/api-handoff.md`. Increment the iteration suffix (`-v2`, `-v3`, …) if rerunning after feedback.
3. **Fill the template** — read [`references/handoff-template.md`](references/handoff-template.md) and fill every section with concrete data. Omit subsections only when truly not applicable (note why).
4. **Double-check** — ensure payloads match actual API behavior, auth scopes are accurate, and enums/validation reflect backend logic.

## Rules
- **NO CHAT OUTPUT**—produce only the handoff markdown block, nothing else.
- Be precise: types, constraints, examples—not vague prose.
- Include real example payloads where helpful.
- Surface non-obvious behaviors—don't assume frontend will "just know."
- If backend made trade-offs or assumptions, document them.
- Keep it scannable: headers, tables, bullets, code blocks.
- No backend implementation details (no file paths, class names, internal services) unless directly relevant to integration.
- If something is incomplete or TBD, say so explicitly.

## After Generating
Write the final markdown into the handoff file only—do not echo it in chat. (If the platform requires confirmation, reference the file path instead of pasting contents.)
