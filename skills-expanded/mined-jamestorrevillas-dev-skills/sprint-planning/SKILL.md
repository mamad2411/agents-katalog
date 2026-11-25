---
name: sprint-planning
description: Use this skill for Agile and Scrum workflows — writing user stories, defining acceptance criteria, estimating story points, generating sprint goals, running retrospectives, backlog grooming, standup updates, or onboarding documentation. Trigger on keywords: user story, sprint, backlog, story points, acceptance criteria, retrospective, standup, DSU, scrum, agile, estimation, epic, ticket.
---

# Sprint Planning

## User Story Writing

### Format
```
As a [type of user],
I want [goal or action],
So that [benefit or value].
```

### Acceptance Criteria Format (Gherkin)
```
Given [initial context or precondition],
When [action or event occurs],
Then [expected outcome].
```

### User Story Example
I want to reset my password via email,
So that I can regain access to my account if I forget my credentials.

Acceptance Criteria:
Given I am on the login page,
When I click "Forgot Password" and enter my email,
Then I should receive a password reset email within 2 minutes.

Given I click the reset link in the email,
When I enter a new valid password,
Then my password should be updated and I should be logged in.
```

### Story Quality Checklist (INVEST)
- **I**ndependent — can be developed without depending on other stories
- **N**egotiable — details can be discussed
- **V**aluable — delivers value to a user or stakeholder
- **E**stimable — team can estimate it
- **S**mall — completable in one sprint
- **T**estable — acceptance criteria are verifiable

---

## Story Point Estimation

### Scale Reference
| Points | Size | Description |
|---|---|---|
| 1 | XS | Trivial change, well-understood, < 2 hours |
| 3 | S | Small, clear scope, half a day |
| 5 | M | Medium complexity, 1–2 days |
| 8 | L | Complex, cross-cutting, 3–4 days |
| 13 | XL | Very complex or uncertain, needs breakdown |

### Estimation Rules
- If a story is 13 points, break it down into smaller stories
- Points represent **complexity + uncertainty**, not just time
- Estimate as a team — avoid anchoring bias (don't share estimates until everyone reveals simultaneously)
- Use historical velocity to validate sprint capacity

---

## Sprint Goal Formula (FOCUS Model)

A good sprint goal is:
- **F**un — memorable and motivating title
- **O**utcome-oriented — what value is delivered, not what tasks are done
- **C**ollaborative — agreed upon by the whole team
- **U**ltimate — answers "why are we doing this sprint?"
- **S**ingular — one clear goal, not a list

### Sprint Goal Example
By end of sprint, users can sign up, log in, and access their dashboard —
giving us a working auth system to build all future features on.
```

---

## Standup / DSU Format

### Structure
```
Yesterday: [What I completed]
Today: [What I'm working on]
Blockers: [Anything blocking me — or "none"]
```

### Example (Taglish style for Filipino dev teams)
```
Good afternoon. 
Yesterday, na-finish ko yung unit tests para sa [feature]. 
Today, mag-a-address ako ng review comments sa [PR] tapos mag-s-start ng [next task].
Wala naman blocker at the moment.
That's all from me, [name].
```

---

## Backlog Grooming

### Grooming Checklist (per story)
- [ ] Story is written in proper user story format
- [ ] Acceptance criteria are defined and testable
- [ ] Story is estimated
- [ ] Dependencies are identified and documented
- [ ] Story is small enough to complete in one sprint
- [ ] Definition of Done is clear

### Prioritization Framework (MoSCoW)
| Priority | Meaning |
|---|---|
| **Must Have** | Critical for this sprint/release |
| **Should Have** | Important but not critical |
| **Could Have** | Nice to have if time permits |
| **Won't Have** | Out of scope for now |

---

## Sprint Retrospective

### Format (Start / Stop / Continue)
```
START: Things we should start doing
STOP: Things we should stop doing  
CONTINUE: Things that are working well
```

### AI-Assisted Retrospective Prompt
```
Given these sprint outcomes: [outcomes]
And these blockers encountered: [blockers]
Generate a Start/Stop/Continue retrospective with:
- 2-3 items per category
- Actionable items, not vague complaints
- One owner assigned per action item
```

---

## Onboarding Documentation

### New Developer Onboarding Checklist
```markdown
## Day 1
- [ ] Dev environment setup (see README)
- [ ] Access to all required systems (GitHub, Jira, Slack, cloud console)
- [ ] First PR — fix a small bug or add a test

## Week 1
- [ ] Understand the domain and architecture (see ARCHITECTURE.md)
- [ ] Shadow a code review
- [ ] Complete first solo story (1–3 points)

## Month 1
- [ ] Own a feature end-to-end
- [ ] Contribute to architecture discussion
- [ ] Give feedback in retrospective
```

### Repository Intelligence File (CLAUDE.md / copilot-instructions.md)
Every repo should have an onboarding file that answers:
1. What does this project do?
2. How do I set it up locally?
3. What are the coding conventions?
4. How do I run tests?
5. How do I deploy?
6. Who do I ask for help?
