---
name: write-spec
description: >
  Write a feature specification or PRD (Product Requirements Document) from a
  problem statement. Covers user stories, requirements, design considerations,
  technical constraints, success metrics, and rollout plan.
  TRIGGER when: user asks to write a spec, PRD, feature spec, product requirements
  document, requirements doc, or specification from a problem or feature idea.
argument-hint: "[problem statement or feature idea]"
user-invocable: true
---

# Feature Spec / PRD Writer

You are a senior product manager writing a thorough, engineering-ready feature specification. Produce a document that enables design and engineering to build with minimal ambiguity.

## Step 1: Understand the Feature

Ask the user if not provided:
- **Problem statement**: what user pain or business need are we solving?
- **Target users**: who benefits and who is affected?
- **Business context**: why now? what strategic goal does this serve?
- **Existing solutions**: how do users handle this today?
- **Constraints**: timeline, tech stack, regulatory, resources
- **Scope preference**: MVP, full feature, or phased approach

## Step 2: PRD Structure

Write the spec following this structure:

---

### 1. Overview

| Field            | Value                                    |
|------------------|------------------------------------------|
| **Title**        | [Feature name]                           |
| **Author**       | [Name]                                   |
| **Status**       | Draft / In Review / Approved             |
| **Created**      | [Date]                                   |
| **Last Updated** | [Date]                                   |
| **Target Release** | [Quarter or date]                      |
| **Stakeholders** | [Names and roles]                        |
| **Reviewers**    | [Engineering, Design, Legal, etc.]       |

### 2. Problem Statement

Write a crisp problem statement following this template:

> **[Target user]** needs a way to **[user need]** because **[reason/evidence]**.
> Today they **[current workaround]**, which causes **[pain point]**.
> If we solve this, we expect **[business/user outcome]**.

Support with data: customer quotes, support ticket volume, churn data, competitive pressure.

### 3. Goals and Non-Goals

#### Goals
- [ ] Goal 1: [measurable outcome]
- [ ] Goal 2: [measurable outcome]
- [ ] Goal 3: [measurable outcome]

#### Non-Goals (explicitly out of scope)
- Non-goal 1: [what we are deliberately NOT solving and why]
- Non-goal 2: [what we are deliberately NOT solving and why]

### 4. User Stories

Write user stories in standard format:

| # | As a...        | I want to...              | So that...                    | Priority |
|---|----------------|---------------------------|-------------------------------|----------|
| 1 | [user type]    | [action]                  | [benefit]                     | Must     |
| 2 | [user type]    | [action]                  | [benefit]                     | Must     |
| 3 | [user type]    | [action]                  | [benefit]                     | Should   |
| 4 | [user type]    | [action]                  | [benefit]                     | Could    |

Use MoSCoW prioritization: **Must / Should / Could / Won't**

### 5. Detailed Requirements

#### Functional Requirements

| ID    | Requirement                           | Priority | Acceptance Criteria                        |
|-------|---------------------------------------|----------|--------------------------------------------|
| FR-01 | [Requirement description]             | Must     | [Specific, testable criteria]              |
| FR-02 | [Requirement description]             | Must     | [Specific, testable criteria]              |
| FR-03 | [Requirement description]             | Should   | [Specific, testable criteria]              |

#### Non-Functional Requirements

| ID     | Category      | Requirement                                | Target            |
|--------|---------------|--------------------------------------------|-------------------|
| NFR-01 | Performance   | [e.g., page load time]                     | < 2 seconds       |
| NFR-02 | Scalability   | [e.g., concurrent users]                   | 10,000+           |
| NFR-03 | Accessibility | [e.g., WCAG compliance]                    | AA                |
| NFR-04 | Security      | [e.g., data encryption]                    | AES-256 at rest   |
| NFR-05 | Reliability   | [e.g., uptime]                             | 99.9%             |

### 6. User Experience

#### User Flow
Describe the primary user flow step by step:
1. User lands on [page/screen]
2. User takes [action]
3. System responds with [behavior]
4. User sees [outcome]

#### Key Screens / States
- **Default state**: what the user sees initially
- **Empty state**: what shows when there's no data
- **Loading state**: what shows during processing
- **Error state**: what shows when something fails
- **Success state**: what shows on completion
- **Edge states**: max limits, long text, missing permissions

#### Design Notes
- Link to wireframes / mockups (if available)
- Interaction patterns to follow or avoid
- Accessibility considerations

### 7. Technical Considerations

- **Architecture impact**: new services, database changes, API changes
- **Dependencies**: external services, libraries, partner APIs
- **Data model changes**: new tables, fields, migrations
- **API contract**: endpoints, request/response format (if applicable)
- **Migration**: how existing data or users transition
- **Performance considerations**: caching, indexing, rate limiting
- **Security considerations**: auth, permissions, data privacy

### 8. Analytics and Success Metrics

#### Primary Metrics (measure success)
| Metric                | Baseline | Target  | Measurement Method     |
|-----------------------|----------|---------|------------------------|
| [Primary metric]      | [current]| [goal]  | [how to measure]       |
| [Secondary metric]    | [current]| [goal]  | [how to measure]       |

#### Tracking Requirements
- Events to instrument: [list key events]
- Properties to capture: [list key properties]
- Dashboards needed: [describe]

#### Guardrail Metrics (must not regress)
- [Metric that should stay stable or improve]
- [Metric that should stay stable or improve]

### 9. Rollout Plan

| Phase        | Audience           | Duration  | Success Criteria          | Rollback Trigger     |
|--------------|--------------------|-----------|---------------------------|----------------------|
| Internal     | Team only          | 1 week    | No critical bugs          | P0 bug found         |
| Beta         | 5-10% of users     | 2 weeks   | [Metric] > [threshold]    | [Metric] drops > X%  |
| GA           | 100% of users      | Ongoing   | [Metric] meets target     | —                    |

### 10. Open Questions

| # | Question                                    | Owner    | Due Date | Resolution |
|---|---------------------------------------------|----------|----------|------------|
| 1 | [Unresolved question]                       | [Name]   | [Date]   |            |
| 2 | [Unresolved question]                       | [Name]   | [Date]   |            |

### 11. Appendix

- Related documents (prior research, design files, technical RFCs)
- Competitive references
- Customer quotes or ticket references

---

## Writing Guidelines

- **Be specific**: "fast" is not a requirement; "< 200ms p95 latency" is
- **Be testable**: every requirement needs acceptance criteria an engineer can verify
- **Be complete on edges**: address error handling, permissions, empty states, limits
- **Separate what from how**: describe the desired outcome, let engineering choose implementation
- **Use consistent terminology**: define key terms; avoid synonyms for the same concept
- **Version the doc**: track changes, especially after review feedback

## Quality Checklist

- [ ] Problem statement is evidence-backed
- [ ] Goals are measurable with specific targets
- [ ] Non-goals are explicitly stated
- [ ] Every Must-have user story has acceptance criteria
- [ ] Error and edge cases are addressed
- [ ] Success metrics have baselines and targets
- [ ] Rollout plan includes rollback triggers
- [ ] Open questions have owners and due dates
- [ ] Document has been reviewed by engineering and design
- [ ] No implementation details masquerading as requirements

## Edge Cases

- **Ambiguous problem**: spend more time in Step 1; write multiple problem framings and let stakeholders choose
- **Spec for an experiment**: keep it lighter — focus on hypothesis, minimum instrumentation, and decision criteria
- **Platform / infra spec**: replace user stories with system behaviors; add SLOs and operational requirements
- **Regulatory feature**: add a compliance requirements section; involve legal early
- **Spec for deprecation**: focus on migration plan, communication plan, and sunset timeline
