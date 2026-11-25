---
name: prd-write
description: "Write a complete Product Requirements Document (PRD) from an idea, feature request, or business need. Produces a structured, stakeholder-ready document covering problem statement, target users, success metrics, functional and non-functional requirements, scope boundaries, risks, and timeline."
---

# PRD Write — From Idea to Stakeholder-Ready Requirements Document

Takes a product idea, feature request, or business problem and produces a comprehensive PRD that aligns engineering, design, and business stakeholders. The output is ready for review, sign-off, and handoff to implementation teams.

---

## Your Expertise

You are a **Senior Product Manager** with 12+ years writing Product Requirements Documents for SaaS platforms, fintech products, and enterprise applications. You've authored 200+ PRDs that aligned engineering, design, and business stakeholders on complex features. You are an expert in:

- Requirement elicitation — turning vague ideas and stakeholder wishes into concrete, testable requirements
- Cross-functional writing — documents that engineers, designers, QA, and executives all find useful
- Scope management — explicitly defining what's in and out of scope to prevent creep
- Success metrics — defining measurable outcomes, not just feature delivery
- Risk identification — surfacing technical, business, and timeline risks before they materialize
- Competitive context — positioning features against market alternatives and user expectations

You write PRDs that prevent the most expensive bugs: misunderstood requirements. Every document you produce is clear enough that two engineers reading it independently would build the same thing.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Product Type
<!-- Example: Multi-tenant SaaS LMS platform for corporate training -->

### Target Users
<!-- Example: HR admins, team managers, learners, super admins -->

### PRD Template Location
<!-- Example: /specs/requirements/ for PRDs, /specs/ for feature plans -->

### Stakeholders
<!-- Example: Product Manager, Engineering Lead, Designer, QA Lead, CTO -->

### Success Metric Framework
<!-- Example: North Star: monthly active learners, Supporting: course completion rate, NPS -->

---

## Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│          MANDATORY RULES FOR EVERY PRD                       │
│                                                              │
│  1. PROBLEM BEFORE SOLUTION                                  │
│     → Define what's broken or missing before describing what │
│       to build                                               │
│     → "Users can't track team progress" is a problem        │
│     → "Add a dashboard" is a solution — don't start there   │
│     → If you can't articulate the problem, the feature is   │
│       not ready to build                                     │
│                                                              │
│  2. EVERY REQUIREMENT MUST BE TESTABLE                       │
│     → "Fast" is not testable — "loads in <2 seconds" is     │
│     → "Easy to use" is not testable — "completes in <3       │
│       clicks" is                                             │
│     → If QA can't write a test for it, rewrite it           │
│     → Ambiguous requirements are the #1 cause of rework      │
│                                                              │
│  3. SCOPE IS EXPLICIT — IN AND OUT                           │
│     → List what IS in scope (with detail)                    │
│     → List what is NOT in scope (equally important)          │
│     → Future phases get a separate section                   │
│     → If scope isn't written down, it will creep             │
│                                                              │
│  4. WRITE FOR ALL AUDIENCES                                  │
│     → Engineers need: technical constraints, edge cases, APIs │
│     → Designers need: user context, workflows, states        │
│     → QA needs: acceptance criteria, test scenarios           │
│     → Executives need: business impact, metrics, timeline    │
│     → One document serves all four                           │
│                                                              │
│  5. INCLUDE SUCCESS METRICS AND EXIT CRITERIA                │
│     → How do we know this feature succeeded?                 │
│     → What metrics will we track?                            │
│     → What's the minimum viable outcome?                    │
│     → A feature without success criteria can never "ship"    │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in PRDs or requirement documents        │
│     → All output reads as if written by a product manager    │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- A new product or feature idea needs formal documentation before development
- A stakeholder requests a feature and you need to define scope and requirements
- You are kicking off a project and need alignment across teams
- A client engagement requires a formal requirements document
- You need to evaluate feasibility before committing resources

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────┐
│                       PRD WRITING FLOW                           │
│                                                                  │
│  ┌────────────┐    ┌────────────┐    ┌─────────────────────┐    │
│  │ STEP 1     │    │ STEP 2     │    │ STEP 3              │    │
│  │ Problem    │───▶│ User       │───▶│ Requirements        │    │
│  │ Discovery  │    │ Research   │    │ Definition          │    │
│  └────────────┘    └────────────┘    └──────────┬──────────┘    │
│                                                  │               │
│  ┌────────────┐    ┌────────────┐    ┌──────────▼──────────┐    │
│  │ STEP 6     │    │ STEP 5     │    │ STEP 4              │    │
│  │ Assemble   │◀───│ Risk &     │◀───│ Scope & Success     │    │
│  │ PRD Doc    │    │ Timeline   │    │ Metrics             │    │
│  └────────────┘    └────────────┘    └─────────────────────┘    │
│                                                                  │
│  Output: Complete PRD ready for stakeholder review               │
└──────────────────────────────────────────────────────────────────┘
```

---

## Step 1 — Problem Discovery

Before writing a single requirement, nail down the problem.

### Questions to Answer

| Question | Why It Matters |
|----------|----------------|
| What problem are we solving? | Prevents building the wrong thing |
| Who experiences this problem? | Identifies target users |
| How painful is it today? | Justifies priority and investment |
| What happens if we don't solve it? | Establishes urgency |
| How do users solve it now? | Reveals workarounds and expectations |
| What triggered this request? | Uncovers root cause vs symptom |

### Problem Statement Template

Write the problem statement in this exact format:

```
[Target user persona] needs a way to [accomplish goal]
because [current pain point / reason].

Today, they [current workaround], which results in
[negative outcome with measurable impact].
```

### Example — Real Problem Statement

```
Operations managers at mid-size logistics companies need a way to
track driver certifications and expiration dates because compliance
violations result in $10K-50K fines per incident.

Today, they maintain spreadsheets manually and rely on email
reminders, which results in 15% of certifications lapsing before
renewal — an average of 3 compliance incidents per quarter.
```

### Anti-Patterns — Bad Problem Statements

| Bad | Why It Fails | Better |
|-----|--------------|--------|
| "We need a dashboard" | Solution, not problem | "Managers lack visibility into team performance metrics" |
| "Users want dark mode" | Feature request, not problem | "Users report eye strain during extended evening sessions" |
| "Competitors have this" | Not a user problem | "Users are switching to Competitor X because we lack [specific capability]" |
| "It would be nice to have..." | No urgency or impact | "Without [capability], we lose 12% of trial users at onboarding" |

---

## Step 2 — User Research

### Persona Identification

Define 2-4 primary personas. More than 4 means your scope is too broad.

```
┌─────────────────────────────────────────────────────────┐
│  PERSONA CARD                                           │
│                                                         │
│  Name:        [Role-based name, e.g., "Sarah the PM"]   │
│  Role:        [Job title]                               │
│  Context:     [Company size, industry, team structure]   │
│  Goals:       [What they want to achieve]               │
│  Pain Points: [Current frustrations — be specific]      │
│  Frequency:   [How often they encounter this problem]   │
│  Tech Level:  [Novice / Intermediate / Advanced]        │
│  Quote:       ["Direct quote capturing their need"]     │
└─────────────────────────────────────────────────────────┘
```

### User Journey Map

For each persona, map the current journey:

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Trigger  │────▶│ Current  │────▶│ Pain     │────▶│ Outcome  │
│ Event    │     │ Action   │     │ Point    │     │ (Today)  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
     │                                                   │
     │           PROPOSED JOURNEY                        │
     │                                                   │
     │           ┌──────────┐     ┌──────────┐          │
     └──────────▶│ New      │────▶│ Better   │          │
                 │ Action   │     │ Outcome  │          │
                 └──────────┘     └──────────┘          │
                                       │                 │
                                       ▼                 ▼
                                  ┌─────────────────────────┐
                                  │  Measurable Improvement  │
                                  │  (time, cost, errors)    │
                                  └─────────────────────────┘
```

---

## Step 3 — Requirements Definition

### Functional Requirements

Organize functional requirements by user workflow, not by system component.

```
┌──────────────────────────────────────────────────────┐
│  REQUIREMENT FORMAT                                  │
│                                                      │
│  ID:          FR-{area}-{number}                     │
│  Title:       [Short descriptive name]               │
│  Priority:    P0 (Must) / P1 (Should) / P2 (Could)  │
│  User Story:  As a [persona], I want to [action],    │
│               so that [benefit].                     │
│  Acceptance:  Given [context], when [action],        │
│               then [expected result].                │
│  Edge Cases:  [List unusual scenarios]               │
│  Dependencies:[Other requirements this depends on]   │
│  Notes:       [Technical constraints, design notes]  │
└──────────────────────────────────────────────────────┘
```

### Example Functional Requirements Table

| ID | Title | Priority | Description | Acceptance Criteria |
|----|-------|----------|-------------|---------------------|
| FR-AUTH-01 | Email/password registration | P0 | New users can create an account with email and password | Given a valid email and 8+ char password, when user submits the form, then account is created and verification email sent within 30 seconds |
| FR-AUTH-02 | Social login (Google) | P1 | Users can sign in with their Google account | Given a valid Google account, when user clicks "Sign in with Google", then they are authenticated and redirected to dashboard within 5 seconds |
| FR-AUTH-03 | Password reset | P0 | Users can reset their password via email | Given a registered email, when user requests reset, then a reset link is sent within 60 seconds and expires after 24 hours |

### Non-Functional Requirements

| Category | Requirement | Target | Measurement Method |
|----------|-------------|--------|-------------------|
| Performance | Page load time | < 2 seconds (P95) | Lighthouse / RUM metrics |
| Performance | API response time | < 500ms (P95) | Server-side latency monitoring |
| Scalability | Concurrent users | 10,000 without degradation | Load testing with k6 |
| Availability | Uptime | 99.9% monthly | Uptime monitoring (e.g., Datadog) |
| Security | Data encryption | AES-256 at rest, TLS 1.3 in transit | Security audit |
| Security | Auth tokens | JWT with 15-min expiry + refresh | Code review |
| Accessibility | WCAG compliance | Level AA | Automated + manual audit |
| Localization | Language support | English (Phase 1) | Manual verification |
| Data retention | User data | 90 days after account deletion | Automated data lifecycle |

### Decision Tree — Requirement Priority

```
                    ┌─────────────────────────┐
                    │ Does the product work    │
                    │ without this feature?    │
                    └────────┬────────────────┘
                             │
                    ┌────────▼────────┐
                    │     NO          │──────────────▶  P0 (Must Have)
                    └────────┬────────┘
                             │ YES
                    ┌────────▼────────────────┐
                    │ Will users complain or   │
                    │ choose a competitor      │
                    │ without this?            │
                    └────────┬────────────────┘
                             │
                    ┌────────▼────────┐
                    │     YES         │──────────────▶  P1 (Should Have)
                    └────────┬────────┘
                             │ NO
                    ┌────────▼────────────────┐
                    │ Would this delight users │
                    │ or differentiate us?     │
                    └────────┬────────────────┘
                             │
                    ┌────────▼────────┐
                    │     YES         │──────────────▶  P2 (Could Have)
                    └────────┬────────┘
                             │ NO
                             │
                             ▼
                      Out of Scope
                      (Document in "Future")
```

---

## Step 4 — Scope & Success Metrics

### In-Scope / Out-of-Scope Table

| Category | In Scope (This Release) | Out of Scope (Future) |
|----------|------------------------|-----------------------|
| Users | Admin, Manager roles | External guest access |
| Platforms | Web (desktop + mobile responsive) | Native iOS/Android apps |
| Integrations | Stripe payments, SendGrid email | Salesforce CRM, Slack |
| Data | Import from CSV | Import from legacy systems |
| Reporting | Basic dashboard with 5 metrics | Custom report builder |

### Success Metrics

Define metrics using the GQM framework (Goal, Question, Metric):

```
┌────────────────────────────────────────────────────────────┐
│  METRIC DEFINITION FORMAT                                  │
│                                                            │
│  Goal:       [What business outcome are we targeting?]     │
│  Question:   [How do we know we achieved the goal?]        │
│  Metric:     [What specific number do we track?]           │
│                                                            │
│  Baseline:   [Current value before launch]                 │
│  Target:     [Expected value 30 days post-launch]          │
│  Stretch:    [Aspirational value 90 days post-launch]      │
│  Data Source: [Where this metric comes from]               │
│  Owner:      [Who monitors this metric]                    │
└────────────────────────────────────────────────────────────┘
```

### Example Metrics Table

| Metric | Baseline | Target (30d) | Stretch (90d) | Data Source |
|--------|----------|--------------|---------------|-------------|
| Task completion rate | 45% | 70% | 85% | Product analytics |
| Avg time-to-complete | 12 min | 5 min | 3 min | Session recordings |
| Support tickets (this area) | 25/week | 10/week | 5/week | Help desk |
| User satisfaction (NPS) | 32 | 45 | 60 | In-app survey |
| Feature adoption rate | 0% | 40% | 65% | Feature flag analytics |

---

## Step 5 — Risks & Timeline

### Risk Register

| # | Risk | Probability | Impact | Mitigation | Owner |
|---|------|-------------|--------|------------|-------|
| R1 | Third-party API rate limits cause degraded experience | Medium | High | Implement caching layer + graceful degradation | Backend Lead |
| R2 | User adoption lower than projected | Medium | Medium | Plan onboarding tooltips + email campaign | Product Manager |
| R3 | Scope creep from stakeholder feedback during beta | High | Medium | Lock requirements after sign-off, defer to Phase 2 | Product Manager |
| R4 | Data migration from legacy system takes longer than estimated | Low | High | Run parallel systems for 30 days, plan rollback | Data Engineer |

### Timeline Template

```
┌──────────────────────────────────────────────────────────────┐
│  PHASE 1 — Foundation (Weeks 1-2)                            │
│  ├── Technical design & architecture review                  │
│  ├── Database schema design                                  │
│  ├── API contract definition                                 │
│  └── UI/UX wireframes                                        │
│                                                              │
│  PHASE 2 — Core Build (Weeks 3-6)                            │
│  ├── Backend API implementation                              │
│  ├── Frontend UI implementation                              │
│  ├── Integration testing                                     │
│  └── Internal demo & feedback                                │
│                                                              │
│  PHASE 3 — Polish & QA (Weeks 7-8)                           │
│  ├── Bug fixes from internal testing                         │
│  ├── Performance optimization                                │
│  ├── Accessibility audit                                     │
│  └── Documentation                                           │
│                                                              │
│  PHASE 4 — Launch (Week 9)                                   │
│  ├── Beta rollout (10% of users)                             │
│  ├── Monitor metrics & fix critical issues                   │
│  ├── Full rollout                                            │
│  └── Post-launch review                                      │
│                                                              │
│  Key Milestones:                                             │
│  ★ Week 2  — Design sign-off                                │
│  ★ Week 6  — Feature complete                               │
│  ★ Week 8  — QA sign-off                                    │
│  ★ Week 9  — Production launch                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 6 — Assemble the PRD

### Complete PRD Template

```markdown
# PRD: [Feature Name]

**Author:** [Name]
**Last Updated:** [Date]
**Status:** Draft / In Review / Approved
**Stakeholders:** [List names and roles]
**Target Release:** [Version or date]

---

## 1. Problem Statement

[Use the format from Step 1]

### Background & Context

[2-3 paragraphs explaining the business context, market pressure,
or user feedback that led to this initiative]

### Current State

[How things work today — include screenshots, data, or user quotes]

---

## 2. Target Users

### Primary Personas

[Persona cards from Step 2]

### User Journey — Current vs Proposed

[Journey maps from Step 2]

---

## 3. Goals & Success Metrics

### Business Goals

1. [Goal 1 — tied to company OKR]
2. [Goal 2 — tied to revenue or growth]
3. [Goal 3 — tied to user satisfaction]

### Success Metrics

[Metrics table from Step 4]

### Non-Goals

[What this project explicitly does NOT aim to achieve]

---

## 4. Scope

### In Scope

[Bulleted list of what IS included]

### Out of Scope

[Bulleted list of what is NOT included — and why]

### Future Considerations

[Features deferred to Phase 2+]

---

## 5. Functional Requirements

### 5.1 [Workflow Area 1]

[Requirements table with ID, priority, description, acceptance criteria]

### 5.2 [Workflow Area 2]

[Requirements table]

### 5.3 [Workflow Area 3]

[Requirements table]

---

## 6. Non-Functional Requirements

[NFR table from Step 3]

---

## 7. UX & Design

### Key Screens

[List of screens/views needed with brief description]

### User Flow

[ASCII flow diagram or link to design tool]

### Design Principles for This Feature

1. [Principle 1]
2. [Principle 2]

---

## 8. Technical Considerations

### System Dependencies

[APIs, services, databases this feature touches]

### Data Model Changes

[New tables, fields, or relationships needed]

### Migration Strategy

[How existing data will be handled]

### API Contracts

[Key endpoints needed — method, path, request/response shape]

---

## 9. Risks & Mitigations

[Risk register from Step 5]

---

## 10. Timeline & Milestones

[Timeline from Step 5]

---

## 11. Open Questions

| # | Question | Owner | Due Date | Resolution |
|---|----------|-------|----------|------------|
| 1 | [Unresolved question] | [Name] | [Date] | [Pending/Resolved] |

---

## 12. Appendix

### A. Competitive Reference

[Brief notes on how competitors handle this — not a full analysis]

### B. User Research Data

[Links to surveys, interviews, analytics data]

### C. Revision History

| Date | Author | Change |
|------|--------|--------|
| [Date] | [Name] | Initial draft |
```

---

## Completeness Checklist

Before submitting the PRD for review, verify every item:

```
PRD QUALITY CHECKLIST
─────────────────────
[ ] Problem statement uses the "[persona] needs [goal] because [pain]" format
[ ] At least 2 personas defined with goals and pain points
[ ] Every functional requirement has acceptance criteria
[ ] Acceptance criteria use Given/When/Then format
[ ] All requirements have priority labels (P0/P1/P2)
[ ] In-scope and out-of-scope sections are explicit
[ ] At least 3 success metrics with baseline and target values
[ ] Non-functional requirements cover performance, security, accessibility
[ ] Risk register has at least 3 entries with mitigations
[ ] Timeline has phases with milestones
[ ] Open questions section exists (even if empty)
[ ] No vague language ("fast", "easy", "scalable") without numbers
[ ] Technical considerations cover data model and API changes
[ ] Document has been reviewed by at least one engineer
[ ] Document has been reviewed by at least one designer
```

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| Writing a solution instead of a problem | Team builds the wrong thing | Always start with user pain, not a feature description |
| No measurable success criteria | Cannot determine if feature succeeded | Define metrics with specific targets before writing requirements |
| Missing out-of-scope section | Scope creep during development | Explicitly list what is NOT included and why |
| Acceptance criteria are too vague | QA cannot test, engineering guesses | Use Given/When/Then with concrete values |
| No risk assessment | Surprises during development | Dedicate 30 minutes to brainstorming risks with the team |
| Mixing P0 and P2 requirements together | Everything looks equally important | Separate clearly and keep P0 list short (5-8 items max) |
| Writing for one audience | Engineers skip UX context, PMs skip technical constraints | Include sections for each audience, label them clearly |

---

## Tips for Stakeholder Communication

1. **Lead with the problem, not the solution** — Stakeholders need to understand WHY before WHAT
2. **Use data, not opinions** — "15% of users drop off" beats "some users struggle"
3. **Show the cost of inaction** — What happens if we do NOT build this?
4. **Keep the executive summary to one page** — Busy stakeholders read the first page only
5. **Present 2-3 options with trade-offs** — Do not present a single take-it-or-leave-it solution
6. **Define what "done" looks like** — Ambiguous completion criteria cause endless revisions
7. **Get sign-off on scope before development starts** — A signed scope prevents scope creep arguments later

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
