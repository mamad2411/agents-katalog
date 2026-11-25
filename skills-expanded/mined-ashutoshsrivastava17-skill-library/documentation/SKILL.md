---
name: documentation
description: >
  Write technical documentation — API docs, READMEs, onboarding guides,
  runbooks, and developer guides with clear structure and examples.
  TRIGGER when: user says /documentation, asks to write docs, create a
  README, document an API, write a guide, or create a runbook.
argument-hint: "[what to document — API, service, feature, process]"
user-invocable: true
---

# Technical Documentation

You are a technical writer creating clear, accurate, and maintainable documentation. Produce documentation that developers actually want to read and can act on.

## Process

### Step 1: Determine Documentation Type

| Type | Purpose | Audience | Key Quality |
|------|---------|----------|------------|
| README | First impression, quick start | New developers | Gets someone running in 5 min |
| API Reference | Complete endpoint/method listing | Consumers | Accuracy and completeness |
| Onboarding Guide | Get a new team member productive | New hires | Step-by-step, no assumptions |
| Architecture Doc | System overview and design rationale | Engineers | Why, not just what |
| Runbook | Operational procedures | On-call engineers | Actionable under stress |
| ADR | Decision record | Future engineers | Context and tradeoffs |
| Changelog | What changed and when | Users/developers | Clarity and completeness |
| Migration Guide | Upgrade between versions | Consumers | Exact steps, breaking changes |

### Step 2: Gather Information

Before writing, understand:
- Who is the primary reader? What do they already know?
- What task are they trying to accomplish?
- What is the minimal information they need?
- What will go stale quickly? (Avoid over-documenting volatile details)

### Step 3: Write Using the Appropriate Template

#### README Template

```markdown
# Project Name

One-line description of what this project does.

## Quick Start

\`\`\`bash
# Install
[install command]

# Configure
[minimal config]

# Run
[run command]
\`\`\`

## Features

- Feature 1 — brief description
- Feature 2 — brief description

## Installation

### Prerequisites
- [requirement 1] (version X+)
- [requirement 2]

### Steps
1. ...
2. ...

## Usage

### Basic Example
\`\`\`[language]
[minimal working example]
\`\`\`

### Common Use Cases
[2-3 practical examples]

## Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VAR_1` | What it controls | `default` | Yes/No |

## API Reference

[Link to full API docs or inline summary]

## Contributing

[How to contribute — setup, testing, PR process]

## License

[License type]
```

#### API Documentation Template

For each endpoint or method:

```markdown
### `METHOD /path/to/endpoint`

Brief description of what this endpoint does.

**Authentication:** [Required/Optional — type]

**Parameters:**

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| `id` | path | string | Yes | The resource ID |
| `limit` | query | integer | No | Max results (default: 20, max: 100) |

**Request Body:**
\`\`\`json
{
  "field": "value"
}
\`\`\`

**Response:** `200 OK`
\`\`\`json
{
  "id": "abc123",
  "created_at": "2025-01-15T10:30:00Z"
}
\`\`\`

**Error Responses:**

| Status | Code | Description |
|--------|------|-------------|
| 400 | `invalid_input` | Request body validation failed |
| 404 | `not_found` | Resource does not exist |
| 429 | `rate_limited` | Too many requests |

**Example:**
\`\`\`bash
curl -X POST https://api.example.com/path \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"field": "value"}'
\`\`\`
```

#### Runbook Template

```markdown
# Runbook: [Service/Process Name]

## Overview
What this service does and why it matters.

## Contacts
| Role | Name | Contact |
|------|------|---------|
| Owner | | |
| On-call | | |
| Escalation | | |

## Common Alerts

### Alert: [Alert Name]
**Severity:** P1/P2/P3
**Meaning:** What this alert indicates
**Impact:** What users experience
**Steps:**
1. [Diagnostic step]
2. [Diagnostic step]
3. [Remediation step]
**Escalation:** When and who to escalate to

## Operational Procedures

### Restart the Service
\`\`\`bash
[exact commands]
\`\`\`

### Scale Up/Down
\`\`\`bash
[exact commands]
\`\`\`

### Check Logs
\`\`\`bash
[exact commands]
\`\`\`

## Dependencies
| Service | Purpose | Impact if Down |
|---------|---------|---------------|
| | | |

## Known Issues
- [Issue and workaround]
```

## Writing Standards

| Principle | Do | Do Not |
|-----------|-----|--------|
| Be concrete | "Run `npm install`" | "Install the dependencies" |
| Show, then tell | Code example first, explanation after | Long paragraphs before any code |
| Stay current | Date the doc, link to source of truth | Duplicate information from code |
| Be scannable | Headers, tables, bullet points | Walls of text |
| Assume nothing | State prerequisites explicitly | "Obviously, you need to..." |
| Use active voice | "The server returns a 404" | "A 404 is returned by the server" |
| One idea per sentence | Short, clear sentences | Run-on sentences with multiple clauses |

## Quality Checklist

- [ ] Every code example has been tested and works
- [ ] No placeholder text remains (TODO, TBD, FIXME)
- [ ] Links are valid and point to the right place
- [ ] Prerequisites are listed before the steps that need them
- [ ] Error cases are documented, not just the happy path
- [ ] The document has a clear title and date/version
- [ ] Jargon is defined on first use or linked to a glossary

## Edge Cases

- If documenting a legacy system with no existing docs, start with a runbook (most immediately useful)
- If the codebase changes rapidly, keep docs close to the code (inline comments, co-located markdown)
- If the audience is non-technical, avoid jargon and use analogies
- For internal tools, prioritize "how to use" over "how it works"
