---
name: team-docs
description: Technical documentation writing methodology. README, usage guide, API documentation and architecture note. The playbook of the docs role.
---

# Technical Documentation

## Core principle

**Verify everything you document.** Do not write it if you have not run the command. Do not write it if you have not read the code. Wrong documentation is worse than no documentation — the user looks in the wrong direction.

## README template

```markdown
# Project Name

One sentence: what it does.

## Installation
## Usage
## Development
## Test
## Deployment
## Architecture (short)
## Contributing
## License
```

Rules:
- Every command in a **copyable** block
- Prerequisites (runtime version, required tools) stated explicitly
- "Requirements" section with version numbers (Node 20+)
- A project explainable in 5 lines should have a 5-line README. An overly long README is a badly written README.

## Verification loop

For every command:

1. **Run** the command.
2. If it works, write its output into the README.
3. If it does not work, either fix it or remove it from the README.

If you cannot do this, do not write that section of the README and report it as "unverifiable".

## API documentation

| Method | Path | Auth | Body | Response | Errors |
|---|---|---|---|---|---|

An example for each endpoint:

**POST /api/v1/invoices**

```http
POST /api/v1/invoices
Content-Type: application/json
Authorization: Bearer <token>
```

```json
{ "number": "INV-2026-001", "total": 249.90, "currency": "EUR" }
```

**201 Created**

```json
{ "id": "inv_01H...", "number": "INV-2026-001", "total": 249.90, "currency": "EUR" }
```

The error body format and a list of error codes (400 / 401 / 403 / 404 / 422 / 500).

## Architecture note

A short ADR-like note:

```markdown
## Decision: <topic>
**Context:** <why this decision is needed>
**Decision:** <what we are doing>
**Alternatives:** <the ones not chosen and why>
**Consequences:** <the benefit and the cost>
```

Do not write more than 10 decisions. Write the 5-10 most impactful ones.

## Language rule

README, API documentation, code examples, comments → **English**.

## Common mistakes

| Mistake | The right way |
|---|---|
| Writing a command you have not run | Run it or do not write it |
| Badge, emoji and "Built with" clutter | Only information that is useful |
| "See the docs for details" | Write the detail |
| Repeating the same information everywhere | One source, link to it |
| Leaving outdated documentation around | Update or delete it |

## Output format

A list of the files written/updated + what was added to each file. Also a list of the points that could not be documented and what is still missing.
