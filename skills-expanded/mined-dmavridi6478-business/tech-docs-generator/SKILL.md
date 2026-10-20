---
name: tech-docs-generator
description: Read a codebase or code snippets and generate technical documentation — architecture overviews, setup guides, API references, and README files. Use when the user has undocumented code and needs docs written from the source, or wants to produce a specific type of technical document (API ref, onboarding guide, architecture diagram narrative) from existing code. Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today."
---

# Technical Documentation Generator

Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today" (Intermediate Tier, #14).

> Reads a codebase and writes architecture docs, setup guides, and API references.

## Document types this skill produces

| Type | Use when |
|---|---|
| Architecture overview | New team member onboarding, system design review |
| Setup / quickstart guide | Getting the project running from zero |
| API reference | Documenting endpoints, params, responses, auth |
| README | Top-level project description for a repo |
| Code module doc | Explaining what a specific file/module/class does |
| Deployment guide | How to get the code into production |

## Copy-paste prompts by document type

### Architecture Overview

```
You are a senior software engineer who specializes in writing clear technical documentation.

Here is the codebase (or key files):
[PASTE CODE, FILE TREE, OR DESCRIBE THE SYSTEM]

Write an architecture overview document that covers:
1. What this system does (one paragraph, non-technical)
2. System components: name each major component and its responsibility
3. How data flows: entry point → processing → storage → output
4. Key technology choices and why they matter (don't just list them)
5. What is NOT in scope for this system (boundaries)
6. A simple diagram in ASCII or Mermaid showing the main components and connections

Audience: a developer joining the team who has not seen this code before.
```

### API Reference

```
You are a technical writer producing API documentation.

Here is the API code (routes, handlers, or OpenAPI spec):
[PASTE CODE]

For each endpoint, document:
- Method + path
- Description (what it does in one sentence)
- Authentication required (yes/no/type)
- Request parameters: name | type | required | description
- Request body (if any): field | type | required | description | example
- Response: status code | description | example JSON
- Error responses: status code | error code | what it means

Format as clean Markdown. Developers will paste this into a docs site.
```

### Setup / Quickstart Guide

```
You are a developer advocate writing onboarding documentation.

Here is the project (code, package.json/requirements.txt, config files):
[PASTE CODE AND CONFIG]

Write a setup guide that takes a developer from zero to running the project locally in under 15 minutes:

1. Prerequisites (what they need installed before starting)
2. Clone and install (exact commands — don't describe, show)
3. Environment variables (list each one, what it's for, where to get it)
4. Database/service setup (if needed)
5. Run the development server (exact command)
6. Verify it's working (what URL to visit / what output to expect)
7. Common errors and how to fix them (top 3)

Rules:
- Use code blocks for every command
- Don't assume knowledge — be explicit
- Flag anything that differs between Mac, Windows, and Linux
```

### README

```
Write a README.md for this project.

Project code / description:
[PASTE CODE OR DESCRIBE THE PROJECT]

Include:
1. Project name + one-sentence description
2. What problem it solves and who it's for
3. Screenshot or demo link placeholder
4. Quick install (3 commands max)
5. Basic usage example (with code)
6. Configuration options (table: option | default | description)
7. Contributing section (how to open a PR)
8. License

Keep it scannable — developers read READMEs in 90 seconds or less.
```

## Related skills

- **pdf**: Extract text from PDF specs or design docs to feed into this skill
- **n8n-agent-builder**: Automate doc generation — trigger when code changes, regenerate docs, push to Notion/Confluence
- **saas-mvp-24h**: Tech docs are Phase 4 of a production-ready MVP — generate them before launch
