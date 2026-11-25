---
name: tpl-situacao-documentacao-tecnica
description: Template do pack (situacao/06-documentacao-tecnica.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/06-documentacao-tecnica.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Writing Technical Documentation

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/06-documentacao-tecnica.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when writing, updating, or auditing technical documentation — including README files, Architecture Decision Records (ADRs), API documentation, runbooks, onboarding guides, data flow diagrams, and system overviews. Good documentation is code: it has an audience, a purpose, and must be maintained. The best documentation is the minimum needed to answer a reader's question.

## OBJECTIVES
- Produce documentation that answers the reader's actual question, not just what's interesting to write
- Establish documentation that stays accurate over time (documentation-as-code)
- Make decisions and their rationale discoverable months after they were made
- Enable a new developer to become productive independently within their first week

## APPROACH RULES

1. **Audience first.** Before writing, state who will read this: junior developer onboarding? DevOps engineer on-call at 2am? External API consumer? Each audience needs different information, level of detail, and vocabulary.

2. **Documentation-as-code.** Documentation must live in the same repository as the code. It must go through code review. It must be updated in the same PR that changes the behavior it describes.

3. **Docs that go stale are worse than no docs.** A wrong runbook executed at 3am causes an outage. If you can't commit to maintaining a doc, write less and make it timeless, or add a "last verified" date and owner.

4. **Show, don't just describe.** Every procedure should have a concrete example. Every API endpoint should have a real request/response example. Every architecture diagram should answer "what happens when X calls Y?"

5. **ADR for every significant architectural decision.** Did you choose Redis over Memcached? Pick PostgreSQL over MongoDB? Choose a microservice over a monolith? Write an ADR. Decisions without recorded rationale are forgotten and re-made.

6. **README is the front door.** Every repository needs a README that answers in under 2 minutes: what does this do, how do I run it, how do I contribute.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| New repository without README | Write a README following the template below before writing any feature code |
| An architectural decision being made | Write an ADR immediately. Accepted ADRs are immutable — write a new one to supersede |
| An API endpoint being added | Write OpenAPI/Swagger spec inline. Never write API docs separately from the spec |
| A complex setup process | Write a runbook with numbered steps. Test it by following it on a clean machine |
| Business logic that's hard to understand | Write inline comments explaining WHY (the what is in the code). Link to business requirement |
| Tribal knowledge ("only Bob knows how to X") | That's a documentation emergency. Interview Bob. Write the runbook. |
| Dependency on external service behavior | Document the dependency's API version, expected behavior, and what to do if it's unavailable |
| Post-mortem / incident | Write it within 48 hours. Use blameless format. Link to it from runbook. |
| Onboarding gap reported by new hire | Treat as a bug. Fix immediately. Update onboarding guide. |
| System diagram older than 6 months | Verify it's still accurate. Update or mark as "unverified - [date]" |

## README Template

```markdown
# [Project Name]

> One sentence describing what this does.

## What This Does
[2-3 sentences max. What problem does this solve? What does it NOT do?]

## Prerequisites
- Node.js 20+
- PostgreSQL 15+
- [Any other hard requirement]

## Getting Started
```bash
git clone [repo]
cd [repo]
cp .env.example .env
# Edit .env with your values
npm install
npm run db:migrate
npm run dev
```

## Project Structure
```
src/
  api/       # HTTP route handlers
  services/  # Business logic
  models/    # Database models
  utils/     # Shared utilities
```

## Key Concepts
[Only the 2-3 things a new dev must understand to be productive]

## Contributing
[Link to CONTRIBUTING.md or brief guide]

## Documentation
- [Architecture Decisions](./docs/adr/)
- [API Reference](./docs/api.yaml)
- [Runbooks](./docs/runbooks/)
```

## ADR Template

```markdown
# ADR-[number]: [Short Decision Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Deciders:** [Names]

## Context
[What is the problem? What constraints exist? What options were available?]

## Decision
[What was decided? Be specific.]

## Consequences
**Positive:**
- [Expected benefits]

**Negative / Tradeoffs:**
- [Known downsides we accept]

**Neutral:**
- [Side effects that are neither good nor bad]
```

## DO NOT

- **DO NOT** document HOW code works — that's what the code is for. Document WHY decisions were made.
- **DO NOT** use passive voice in runbooks — "The service should be restarted" → "Run: `systemctl restart myservice`"
- **DO NOT** write docs that require running an external proprietary tool to read (Notion, Confluence) — keep it in the repo as Markdown
- **DO NOT** leave TODO items in published documentation — finish docs before merging
- **DO NOT** write an ADR after the fact to justify a decision already made — write it during the decision process
- **DO NOT** use "etc." — either list the things or don't. Vague lists lose meaning quickly.

## OUTPUT FORMAT

Every documentation artifact should include a header block:

```markdown
---
title: [Title]
audience: [who reads this]
last-verified: YYYY-MM-DD
owner: [team or person]
---
```

For runbooks, use numbered steps where order matters and bullets where it doesn't. Never mix the two in the same procedure.

For API docs, every endpoint must show:
- HTTP method + path
- Required and optional parameters with types
- At least one successful response example
- At least one error response example

## QUALITY GATES

- [ ] Audience is explicitly identified at the top of every document
- [ ] Every code example is syntactically correct and has been manually tested
- [ ] README tested on a fresh machine: can someone follow it and get the project running?
- [ ] All ADRs have Status (not left as "Proposed" forever)
- [ ] No documentation references a filename, URL, or service that no longer exists
- [ ] Runbooks end with a verification step (how do you know it worked?)
- [ ] API docs match actual API behavior (tested against running service)
- [ ] Documentation updated in same PR as code change it describes
- [ ] Last-verified date set on all time-sensitive docs (runbooks, setup guides)
