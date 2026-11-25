---
name: tpl-situacao-onboarding-novo-dev
description: Template do pack (situacao/11-onboarding-novo-dev.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/11-onboarding-novo-dev.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Onboarding a New Developer

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/11-onboarding-novo-dev.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when preparing documentation, materials, or guidance to onboard a new developer (or when acting as guide for a developer learning a codebase). Good onboarding is not a one-day orientation — it's a structured 30-day ramp that reduces "bus factor", distributes knowledge, and makes the new developer productive faster. The CLAUDE.md file is itself a powerful onboarding artifact.

## OBJECTIVES
- Get the new developer from zero to first PR within their first week
- Document the architecture so it doesn't require a senior developer to explain it
- Identify and eliminate tribal knowledge ("only Ana knows how X works")
- Establish a "first contribution" experience that builds confidence
- Keep onboarding materials accurate by treating them as living documentation

## APPROACH RULES

1. **CLAUDE.md is onboarding documentation.** The CLAUDE.md in a repository is the first thing a new developer (or AI assistant) should read. Treat it as the authoritative explanation of the project. Update it whenever the codebase changes significantly.

2. **Document the "why", not the "what".** New developers can read code. They cannot read minds. Document: why certain technology was chosen, why certain patterns exist, what decisions were almost made differently, and what to do in common scenarios.

3. **First PR within 5 days or onboarding is failing.** The first PR should be small and low-risk (a documentation fix, a small bug, a minor improvement). The goal is to experience the full contribution cycle: branch → code → review → merge.

4. **Assume zero context.** Write documentation as if the reader has never heard of the project, the team's conventions, or the problem domain. Jargon must be defined or linked.

5. **Bus factor audit.** For every critical piece of knowledge, ask: "if [person] left today, could the team continue?" If the answer is no, that knowledge must be documented before this onboarding session ends.

6. **Pair programming is the highest-bandwidth onboarding tool.** Schedule at least 3 pair sessions in the first two weeks. The new developer should drive while the senior navigates.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| New repo without CLAUDE.md | Create it now. It's the most valuable onboarding artifact. See template below. |
| "Ask Bob about how X works" | Bus factor alert. Sit with Bob, document X, add to architecture docs or CLAUDE.md. |
| Setup process that took > 30 minutes | Document every step that was unclear. PR the improvement to the README. |
| Acronym or internal term not defined | Add to the project glossary (or create one) |
| Architecture never drawn or documented | Create a C4 diagram (Context → Containers → Components) using Mermaid in docs/ |
| New dev asking the same question twice | That question needs to be answered in docs. The question is the documentation gap. |
| First PR blocked by unfamiliar process | Process must be in CONTRIBUTING.md. Update it immediately. |
| On-call rotation for new dev | Do not add to on-call rotation until they can independently resolve P1 incidents. At minimum: 30 days. |
| Code review feels overwhelming for new dev | Start with a review of a small PR by them. The first review teaches more than any document. |
| New dev from different tech stack | Create a "coming from X" guide highlighting the biggest differences. Especially: error handling, async patterns, testing philosophy. |

## CLAUDE.md Template for Onboarding

```markdown
# Project: [Name]

## What This Is
[One paragraph. What problem does this solve? Who are the users?]

## Architecture Overview
[Diagram or description. Key services, their responsibilities, how they communicate.]

## Tech Stack
| Layer | Technology | Why We Chose It |
|-------|-----------|----------------|
| API | Fastify | Performance, TypeScript-first |
| Database | PostgreSQL | ACID compliance, strong ecosystem |
| Cache | Redis | Session storage, rate limiting |
| Queue | BullMQ | Job processing, retries |

## Key Concepts
[The 3-5 domain concepts a developer MUST understand to work effectively.
Example: "A 'Campaign' is different from an 'Ad Set'. Campaigns hold budget,
Ad Sets hold targeting. Never confuse them."]

## Common Tasks
### How to add a new API endpoint
1. Create handler in src/api/[resource].ts
2. Register route in src/router.ts
3. Add service method in src/services/[resource]Service.ts
4. Add migration if schema change needed
5. Write tests in tests/integration/[resource].test.ts

### How to run database migrations
```bash
npm run db:migrate
```

## Architecture Decisions
See docs/adr/ for all Architecture Decision Records.
Key decisions: [links to 3-5 most important ADRs]

## Glossary
| Term | Definition |
|------|-----------|
| [Term] | [Plain English definition] |

## Common Gotchas
- [Thing that trips up everyone their first week]
- [Behavior that seems wrong but is intentional]

## Who To Ask About What
| Topic | Person / Team | Where |
|-------|-------------|-------|
| Auth system | Security team | #security channel |
| Payments | @ana | Pull her into a PR |
| Infrastructure | DevOps | #infra channel |
```

## 30-Day Onboarding Plan

```
Week 1: Environment & Orientation
- Day 1: Setup (README → running local environment)
- Day 2: Architecture overview session (pair with senior)
- Day 3: Read 5 recent PRs to understand patterns
- Day 4: First task: fix a documentation gap found during setup
- Day 5: First PR merged 🎉

Week 2: First Feature
- Pair programming on a real (small) task
- Attend sprint planning
- First code review (receive)
- Learn deployment process (observe, don't run yet)

Week 3: Independent Work
- Own a well-defined task independently
- Give a code review to someone else
- First deployment with buddy present

Week 4: Integration
- Own a task from estimate to deployment
- Participate in incident review (read past post-mortems)
- 30-day retrospective: what was confusing? Update docs.
```

## DO NOT

- **DO NOT** give a new developer an ambiguous task their first week
- **DO NOT** add them to on-call before they can independently debug production issues
- **DO NOT** pair with them only once — the highest-value onboarding is repeated pairing
- **DO NOT** have them start on a legacy, untested, "here be dragons" part of the codebase
- **DO NOT** let tribal knowledge remain undocumented after onboarding reveals it
- **DO NOT** expect the new developer to figure out unwritten conventions — if it's a convention, write it down

## OUTPUT FORMAT

At the end of onboarding preparation, produce:

1. **Updated CLAUDE.md / README** with any gaps identified during onboarding
2. **Glossary** of project-specific terms
3. **"First PR" task** — a concrete, scoped task ready for the new developer to pick up
4. **Knowledge gaps list** — things discovered during onboarding that still need documentation
5. **Updated CONTRIBUTING.md** if any process was unclear

## QUALITY GATES

- [ ] New developer successfully ran the project locally using only the README (no external help)
- [ ] CLAUDE.md or architecture document exists and is current
- [ ] Glossary exists for all domain-specific terms
- [ ] First PR merged within first 5 days
- [ ] Bus factor reduced: at least one "only X knows this" knowledge item documented
- [ ] New developer can describe the architecture in their own words after week one
- [ ] 30-day retro done: docs updated based on what was confusing
- [ ] New developer knows who to ask for help on each major subsystem
