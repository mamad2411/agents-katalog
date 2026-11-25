---
name: prd-writer
description: "PRD authoring and refinement. Activated when the user says \"write PRD\", \"draft PRD\", \"break down feature\", \"scope this\", \"requirements for\", \"define feature\", or wants to turn a rough idea into a structured product document."
allowed tools: Read, Write, Edit, Grep, Glob
---

# PRD Writer

Turn rough ideas into structured PRDs following the project's template.
The PRD is the single source of truth for what to build and why.

## Rules

1. **Always use the template** — read `docs/product/_template-prd.md` first
2. **Clarify before writing** — ask questions if the idea is ambiguous (max 5 questions)
3. **Scope aggressively** — define what is OUT of scope as clearly as what is IN scope. The "Not Doing" list is arguably the most valuable part of the PRD
4. **User stories over descriptions** — "As a [user], I want [action], so that [benefit]"
5. **Acceptance criteria are testable** — each criterion must be verifiable by running code
6. **Check memory first** — search for past features that might overlap or inform this one
7. **Reference, don't duplicate** — link to ADRs, specs, and existing PRDs with `[[wiki-links]]`
8. **Output to docs/product/** — never create PRDs elsewhere

## Workflow

### Phase 1: Understand the idea
1. Read the user's description / rough idea
2. Search memory for related past features: `python memory/query.py "[topic]"`
3. Check existing PRDs in `docs/product/` for overlap
4. If the idea is vague, ask up to **5 clarifying questions**:
   - Who is the target user?
   - What problem does this solve?
   - What does "done" look like?
   - Are there constraints (timeline, tech, regulatory)?
   - What is explicitly out of scope?

### Phase 2: Draft the PRD
Read the template and fill in every section:

1. **Context** — why now? What triggered this feature?
2. **Objective** — one sentence: what this feature will accomplish
3. **Scope**
   - Includes: specific deliverables
   - Excludes: what this PRD does NOT cover (critical for preventing scope creep)
4. **"Not Doing" list** — explicitly document what you chose NOT to build and why.
   This is arguably the most valuable section: it prevents scope creep and aligns expectations.
   ```markdown
   ## Not Doing (and why)
   - **Multi-language support** — not needed for MVP; all users are PT-BR
   - **Admin dashboard** — managed via database until user count justifies UI
   - **Email notifications** — WhatsApp is the primary channel; email adds complexity without value
   ```
5. **User stories** — 3-7 stories in `As a... I want... So that...` format
6. **Design** — reference Figma link OR note "use design tokens" for agent flow
7. **Acceptance criteria** — numbered, testable statements:
   - `AC-1: When [condition], then [expected result]`
   - Each must be verifiable by running a test or checking behavior
8. **Technical decisions** — link to existing ADRs or note that new ones are needed
9. **Impact on specs** — check each active spec module:
   - [ ] Compliance: personal data? Legal basis needed?
   - [ ] Security: new attack surface? Auth changes?
   - [ ] Observability: new metrics/alerts needed?
   - [ ] Scalability: performance impact?
   - [ ] Accessibility: WCAG compliance needed?
   - [ ] i18n: new strings to translate?
   - Skip modules that don't apply
10. **Rollout** — feature flags, migration plan, rollback strategy

### Phase 3: Review
1. Read the PRD back and verify:
   - Every user story has acceptance criteria
   - Scope excludes are clear
   - Technical decisions reference ADRs
   - Spec impact is assessed
2. Name the file: `docs/product/feat-{short-name}.md`
3. Present the PRD summary and ask for approval before saving

## PRD Quality Checklist
- [ ] Objective is one sentence
- [ ] Scope has both includes AND excludes
- [ ] "Not Doing" list with at least 3 items and justifications
- [ ] At least 3 user stories
- [ ] Every acceptance criterion is testable (not "should be intuitive")
- [ ] Design section specifies Figma link OR "use design tokens"
- [ ] Active spec modules checked for impact
- [ ] No implementation details in the PRD (that's the ADR's job)
- [ ] File saved in `docs/product/`

## References
- `docs/product/_template-prd.md` — the template
- `docs/product/vision.md` — product vision (PRD must align)
- `docs/architecture/` — existing ADRs to reference
- `docs/specs/` — active spec modules to check for impact
