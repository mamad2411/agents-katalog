---
name: tpl-situacao-sprint-planning-tecnico
description: Template do pack (situacao/12-sprint-planning-tecnico.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/12-sprint-planning-tecnico.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Technical Sprint Planning

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/12-sprint-planning-tecnico.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when breaking down features into tasks for sprint planning, refining a backlog, estimating effort, or facilitating technical planning sessions. Good sprint planning produces tasks that are independently completable, correctly sized, clearly defined, and don't create bottlenecks between developers. Bad sprint planning produces chaos week two.

## OBJECTIVES
- Break features into vertical slices that deliver value independently
- Balance technical debt reduction against feature delivery
- Surface hidden dependencies and risks before they block the sprint
- Write acceptance criteria that leave no ambiguity about "done"
- Calibrate estimates against team velocity (not ideal time)

## APPROACH RULES

1. **Vertical slices, not horizontal layers.** A vertical slice delivers end-to-end functionality (UI + API + DB) for a narrow user scenario. A horizontal layer (e.g., "build the entire data model") is not a user story — it's a task that rarely delivers value on its own.

2. **If a story touches more than 3 layers, split it.** Backend integration, frontend, tests, and documentation should rarely all be in one story unless the scope is very small.

3. **Technical debt gets a budget, not a sprint.** Reserve 20% of sprint capacity for technical debt. Do not postpone it indefinitely. Do not let it consume the whole sprint. Negotiate explicitly.

4. **Acceptance criteria must be testable.** "Works correctly" is not an acceptance criterion. "User can submit the form with valid data and sees a success message" is. Every AC should be falsifiable.

5. **Estimate by complexity, not by time.** Story points measure relative complexity compared to a reference story. Never say "this is 3 points because it takes 3 hours." That anchors estimates to ideal time and ignores unknowns.

6. **Dependencies are risks.** Any story that depends on another story, external team, or external service is at risk. Surface all dependencies. Either resolve them before the sprint starts or flag the story as blocked.

7. **Capacity ≠ Sprint Length × Team Size.** Account for: meetings, code reviews, incidents, holidays, onboarding. Real capacity is typically 60-70% of theoretical capacity.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| A story estimated over 8 points | Split it. Stories over 8 points are too uncertain to estimate accurately. Find a vertical slice. |
| Story with no acceptance criteria | Do not take it into the sprint. Write AC in refinement. |
| "Also include X while we're at it" | Scope creep. Create a new ticket. Keep the current story focused. |
| A story blocked by another team | Flag it. Move to the backlog unless the blocker resolves before sprint starts. |
| Story touching database AND UI AND external API | Likely 3 stories. Split: (1) data model, (2) API endpoint, (3) UI integration. |
| Technical debt story with no concrete impact | Reframe: "Refactor X to enable Y" or "Reduce deploy time from 15min to 5min." Impact must be measurable. |
| Stakeholder requesting estimate in hours/days | Convert to a range: "Given our velocity, this is likely 3-5 business days." Never commit to hours publicly. |
| Story depends on design that isn't ready | Block the story. Design must be definition-of-ready before a story enters sprint planning. |
| Same story re-estimated 3+ times | It needs a spike (research task) to reduce uncertainty first. Cap spike at 1-2 days. |
| Story with "let's figure it out as we go" | Red flag. Discovery tasks exist. Write a spike story. Never put an unscoped story in a sprint. |

## Story Template

```markdown
## [Story Title]

**Type:** Feature / Bug / Tech Debt / Spike

**As a** [type of user]
**I want** [some goal]
**So that** [some reason / business value]

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]
- [ ] Error cases: [what happens on validation failure, network error, etc.]
- [ ] [Performance] Response time < 500ms under normal load

**Technical Notes:**
- Affected files/services: [list]
- Dependencies: [other stories, external services]
- Known risks: [what could go wrong]

**Definition of Done:**
- [ ] Code merged to main
- [ ] Tests written and passing (coverage ≥ 80% on new code)
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Acceptance criteria verified by PO or QA

**Estimate:** [story points]
```

## Story Point Reference Scale

| Points | Description | Example |
|--------|-------------|---------|
| 1 | Trivial, zero unknowns | Change a label, update a config value |
| 2 | Simple, well-understood change | Add a new field to an existing form + save to DB |
| 3 | Standard, some design needed | New CRUD endpoint with validation |
| 5 | Complex, significant design work | New OAuth integration |
| 8 | Very complex, multiple unknowns | Real-time feature with WebSockets |
| 13+ | Too large — must be split | — |

## Technical Debt Categories

| Category | Example | Priority |
|----------|---------|----------|
| Security debt | Unvalidated user input | Critical — fix immediately |
| Reliability debt | No error handling in payment flow | High |
| Test debt | Critical path with 0% coverage | High |
| Performance debt | N+1 query in hot path | Medium |
| Maintainability debt | 500-line god function | Low-Medium |
| Documentation debt | Undocumented architecture | Low |

## DO NOT

- **DO NOT** let a sprint start with undefined acceptance criteria on any story
- **DO NOT** carry over more than 20% of stories from the previous sprint — investigate why
- **DO NOT** assign stories by seniority only — knowledge silos kill team velocity
- **DO NOT** create a "Miscellaneous" or "Chores" story as a catch-all
- **DO NOT** estimate in the same session as requirements clarification — those are two different meetings
- **DO NOT** add stories to an active sprint without removing equal points — protect the sprint
- **DO NOT** use sprint planning to make architectural decisions — that's a separate RFC/ADR session

## OUTPUT FORMAT

Sprint planning output should produce:

```markdown
## Sprint [N] Plan — [start date] to [end date]

### Capacity
- Team: 4 developers
- Working days: 10
- Estimated capacity: 40 points (accounting for 20% overhead)
- Reserved for tech debt: 8 points

### Stories (by priority)
| # | Story | Points | Owner | Dependencies |
|---|-------|--------|-------|-------------|
| 1 | User can reset password via email | 3 | Dev A | Email service configured |
| 2 | Add rate limiting to auth endpoints | 5 | Dev B | none |

### Risks & Blockers
- [Story X] depends on design mockups not yet ready
- [Story Y] requires access to staging payment gateway

### Tech Debt Budget
| Item | Points | Impact |
|------|--------|--------|
| Refactor AuthMiddleware (enables easier testing) | 5 | Unblocks 3 future stories |
| Remove deprecated API v1 endpoints | 3 | Reduces maintenance surface |

### Sprint Goal
[One sentence describing the main user-facing outcome of this sprint]
```

## QUALITY GATES

- [ ] Every story has at least 2 acceptance criteria in testable format
- [ ] No story estimated above 8 points (split if so)
- [ ] All dependencies between stories identified and declared
- [ ] Sprint capacity calculated with realistic overhead (not 100% of working hours)
- [ ] 20% capacity reserved for technical debt
- [ ] Sprint goal stated in one sentence (business outcome, not task list)
- [ ] All team members voiced concerns or questions before plan is finalized
- [ ] Stories marked "blocked" have blocking condition and resolution owner
