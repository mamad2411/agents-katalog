---
name: phase-1-spec
description: Phase 1 of the development cycle. Turns a raw idea into an approved product specification (docs/spec/PRODUCT_SPEC.md) with user stories, testable acceptance criteria, priorities, and non-functional requirements, by interviewing the user and then having the spec-reviewer agent check it.
disable-model-invocation: true
argument-hint: "[your idea in a sentence or two]"
---

# Phase 1 — Idea → Product spec

Idea from the user: $ARGUMENTS

Goal: a spec clear enough that someone else could design and test the product from it. No code in this phase.

## Steps

```
Phase 1 progress:
- [ ] 1. Interview the user
- [ ] 2. Write docs/spec/PRODUCT_SPEC.md
- [ ] 3. Review with the spec-reviewer agent
- [ ] 4. Fix gaps, get user approval
```

**1. Interview.** Ask questions in at most three short rounds. Don't ask everything at once, and don't invent answers. Cover:
- Problem: what pain, for whom, and how do they cope today?
- Users: the main user types (personas) and what each one needs to get done.
- Goals: what success looks like, in numbers if possible (sign-ups, time saved, revenue).
- Scope: the must-haves for a first version, and what is explicitly *not* in v1.
- Constraints: deadline, budget, team, required tech or platforms, regulations (GDPR, HIPAA, PCI).
- Quality needs: expected users and traffic, speed, uptime, security and privacy, accessibility, languages, devices.

If the user says "you decide" on something, propose a sensible default and mark it `(assumed)`.

**2. Write the spec** using the template below. Every user story gets acceptance criteria in Given/When/Then form. Each criterion must be testable, so avoid vague words like "fast" or "easy". Prioritize with MoSCoW: Must, Should, Could, Won't (for now).

**3. Review.** Use the **spec-reviewer** agent on `docs/spec/PRODUCT_SPEC.md`.

**4. Fix and approve.** Apply the reviewer's fixes, and ask the user about anything only they can answer. Show the user a short summary and ask for approval. When approved, set `Status: Approved`.

Finish by telling the user: "Next: `/phase-2-architecture`".

## Template — docs/spec/PRODUCT_SPEC.md

```markdown
# <Product name> — Product spec

Status: Draft | Approved · Version: 0.1 · Last updated: YYYY-MM-DD

## 1. Summary
<3–4 sentences: what it is, who it's for, why it matters.>

## 2. Problem
## 3. Users (personas)
| Persona | Description | Main goals |
|---------|-------------|------------|

## 4. Goals and success metrics
| Goal | Metric | Target |
|------|--------|--------|

## 5. Scope
### In scope (v1)
### Out of scope (v1)

## 6. Features and user stories
### F1. <Feature name> — Priority: Must
**US-1.1** As a <persona>, I want <action> so that <benefit>.
Acceptance criteria:
- AC-1.1.1 Given <context>, when <action>, then <observable result>.
- AC-1.1.2 Given …, when …, then ….

## 7. Non-functional requirements
| ID | Category | Requirement (measurable) |
|----|----------|--------------------------|
| NFR-1 | Performance | 95% of page loads < 2 s on 4G |
| NFR-2 | Availability | 99.5% monthly |
| NFR-3 | Security | … |
| NFR-4 | Accessibility | WCAG 2.2 AA |

## 8. Constraints and assumptions
## 9. Risks
## 10. Open questions
| # | Question | Owner | Status |
```
