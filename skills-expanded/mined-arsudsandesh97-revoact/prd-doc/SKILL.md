---
name: prd-doc
description: Generate comprehensive Product Requirements Documents (PRDs) for any software project, feature, or product initiative
---

# PRD Generator Skill

Use this skill to create professional Product Requirements Documents that clearly define what needs to be built, why it matters, and who it serves.

## When to Use This Skill

Trigger this skill when the user asks to:
- "Create a PRD for [feature/project]"
- "Write a product requirements document"
- "Document product requirements"
- "Generate a PRD"
- "I need a PRD for..."
- Any request to formalize product specifications

## PRD Structure Template

A comprehensive PRD should follow this structure:

```markdown
# [Project/Feature Name] - Product Requirements Document

**Document Owner:** [Name/Role]
**Created:** [Date]
**Last Updated:** [Date]
**Status:** [Draft | In Review | Approved | In Progress | Completed]

---

## 1. Executive Summary

**TL;DR:** [2-3 sentence overview of what this is and why it matters]

### Quick Facts
- **Target Launch:** [Date/Quarter]
- **Priority:** [P0 - Critical | P1 - High | P2 - Medium | P3 - Low]
- **Estimated Effort:** [T-shirt size: XS/S/M/L/XL or story points]
- **Team:** [Team/squad responsible]

---

## 2. Problem Statement

### What Problem Are We Solving?
[Clearly articulate the core problem. Be specific about pain points.]

### Who Has This Problem?
[Define the target user/persona/segment experiencing this problem]

### How Do We Know This Is a Problem?
[Evidence: user research, data, feedback, metrics, market research]
- Data point 1
- Data point 2
- User quote or feedback example

### What Happens If We Don't Solve This?
[Impact of inaction: lost revenue, churn, competitive disadvantage, etc.]

---

## 3. Goals & Success Metrics

### Primary Goals
1. [Goal 1 - what you want to achieve]
2. [Goal 2]
3. [Goal 3]

### Success Metrics (How We'll Measure Success)

| Metric | Current Baseline | Target | Measurement Method |
|--------|------------------|--------|-------------------|
| [e.g., User adoption rate] | [current %] | [target %] | [how measured] |
| [e.g., Task completion time] | [current time] | [target time] | [analytics tool] |
| [e.g., Customer satisfaction] | [current score] | [target score] | [survey/NPS] |

### Non-Goals (What We're NOT Doing)
- [Explicitly state what's out of scope]
- [Helps prevent scope creep]

---

## 4. User Stories & Use Cases

### Primary User Stories

**As a** [user type]
**I want to** [action/capability]
**So that** [benefit/value]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

[Repeat for 3-5 key user stories]

### User Scenarios
[Describe 2-3 realistic scenarios showing how users will interact with this]

**Scenario 1: [Name]**
- **Context:** [situation]
- **Action:** [what user does]
- **Expected Outcome:** [what happens]

---

## 5. Requirements

### Functional Requirements (What It Must Do)

#### Must Have (P0 - Launch Blockers)
1. [Requirement 1 - essential functionality]
2. [Requirement 2]
3. [Requirement 3]

#### Should Have (P1 - Important but not blockers)
1. [Requirement 4]
2. [Requirement 5]

#### Could Have (P2 - Nice to have)
1. [Requirement 6]
2. [Requirement 7]

#### Won't Have (This Release)
1. [Deferred requirement 1]
2. [Deferred requirement 2]

### Non-Functional Requirements

**Performance:**
- [e.g., Page load time < 2 seconds]
- [e.g., API response time < 200ms]

**Scalability:**
- [e.g., Support 10,000 concurrent users]

**Security:**
- [e.g., All data encrypted at rest and in transit]
- [e.g., Role-based access control]

**Accessibility:**
- [e.g., WCAG 2.1 Level AA compliant]

**Compatibility:**
- [Browser/platform requirements]
- [Device support]

**Reliability:**
- [e.g., 99.9% uptime]
- [Error handling requirements]

---

## 6. User Experience & Design

### Key User Flows
[Describe or link to diagrams showing main user journeys]

1. **Flow 1: [Name]**
   - Step 1 → Step 2 → Step 3 → Outcome

### Design Requirements
- [Visual design considerations]
- [Branding guidelines to follow]
- [UI component requirements]

### Wireframes/Mockups
[Link to Figma/design files or embed key screens]

---

## 7. Technical Considerations

### Integration Points
- [System/API 1 we need to integrate with]
- [System/API 2]

### Data Requirements
- [What data needs to be stored/processed]
- [Data migration needs]

### Dependencies
- [External libraries/services needed]
- [Other teams/projects this depends on]

### Technical Constraints
- [Platform limitations]
- [Technology stack requirements]

---

## 8. Assumptions & Risks

### Assumptions
1. [Assumption 1 - e.g., "Users have stable internet connection"]
2. [Assumption 2]

### Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|-------------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How we'll address it] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Mitigation plan] |

---

## 9. Stakeholders & Roles

| Name | Role | Responsibility |
|------|------|----------------|
| [Name] | Product Manager | Overall ownership & decisions |
| [Name] | Engineering Lead | Technical feasibility & implementation |
| [Name] | Designer | UX/UI design |
| [Name] | QA Lead | Testing strategy |
| [Name] | Stakeholder | Approval/sign-off |

---

## 10. Timeline & Milestones

### Phased Rollout (if applicable)

**Phase 1: MVP** (Target: [Date])
- [Feature subset 1]
- [Feature subset 2]

**Phase 2: Enhancement** (Target: [Date])
- [Additional features]

**Phase 3: Scale** (Target: [Date])
- [Optimization and expansion]

### Key Milestones
- **[Date]:** Design complete
- **[Date]:** Development starts
- **[Date]:** Alpha/Beta release
- **[Date]:** Production launch

---

## 11. Open Questions

- [ ] [Question 1 that needs answering before we proceed]
- [ ] [Question 2]
- [ ] [Question 3]

---

## 12. Appendix

### References
- [Link to user research]
- [Link to competitive analysis]
- [Link to related docs]

### Glossary
- **Term 1:** Definition
- **Term 2:** Definition

### Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | [Date] | [Name] | Initial draft |
| 0.2 | [Date] | [Name] | Updated after review |
```

---

## Best Practices for PRD Generation

When creating a PRD, follow these guidelines:

### 1. **Start with the Problem, Not the Solution**
   - Focus on *what* problem exists and *why* it matters
   - Avoid jumping straight to "how to build it"
   - Let the problem guide the solution

### 2. **Be Specific and Measurable**
   - Use concrete numbers and metrics
   - Avoid vague terms like "improve user experience"
   - Define clear success criteria

### 3. **Know Your Audience**
   - Engineers need technical details
   - Executives need business impact
   - Designers need user flows
   - Tailor sections accordingly

### 4. **Prioritize Ruthlessly**
   - Use MoSCoW method (Must/Should/Could/Won't)
   - Be explicit about what's OUT of scope
   - Resist scope creep

### 5. **Use Data to Support Decisions**
   - Back claims with user research, analytics, or market data
   - Include quotes from real users
   - Show the ROI

### 6. **Make It Scannable**
   - Use headers, tables, and bullet points
   - Add a TL;DR at the top
   - Busy stakeholders should grasp it in 2 minutes

### 7. **Keep It Living**
   - Update as decisions are made
   - Track version history
   - Mark sections as "TBD" if uncertain

### 8. **Get Feedback Early**
   - Share drafts with stakeholders
   - Iterate based on questions
   - Get alignment before development starts

---

## Conversation Flow When User Requests a PRD

When the user asks for a PRD, gather context first:

**Ask these questions if information is missing:**
1. "What's the project or feature you're building?"
2. "What problem does this solve, and for whom?"
3. "Do you have any specific goals or success metrics in mind?"
4. "What's the rough timeline or priority level?"
5. "Are there any technical constraints I should know about?"

**Then generate the PRD by:**
1. Starting with the executive summary and problem statement
2. Filling in user stories and requirements based on their responses
3. Using placeholders `[TBD]` for sections they haven't defined yet
4. Keeping it concise for small features, comprehensive for large projects
5. Saving the output as `PRD.md` in their working directory

---

## Examples of Good PRD Sections

### Example: Problem Statement
```markdown
## Problem Statement

### What Problem Are We Solving?
Users currently spend 10-15 minutes manually exporting data from our dashboard, 
formatting it in Excel, and emailing it to stakeholders. This is tedious and 
error-prone, especially for weekly reports that follow the same format.

### Who Has This Problem?
Account managers and customer success teams who need to send regular reports 
to clients (approximately 40% of our user base, ~2,000 users).

### How Do We Know This Is a Problem?
- Support tickets: 127 requests for "automatic report export" in Q2
- User interviews: 8 out of 10 AMs cited this as their #1 pain point
- Time tracking data: Users spend avg 12 min per export, 3x per week = 36 min/week
- Churn analysis: 3 customers cited lack of automated reporting in exit surveys

### What Happens If We Don't Solve This?
- Continued manual work costs ~1,200 hours per month across all users
- Competitive disadvantage: 4 competitors offer automated reports
- Potential revenue impact: $150K ARR at risk from customers considering churn
```

### Example: Success Metrics Table
```markdown
| Metric | Current Baseline | Target | Measurement Method |
|--------|------------------|--------|-------------------|
| Time to generate report | 12 min | < 2 min | User activity logs |
| Weekly report adoption | 0% (manual) | 60% | Feature usage analytics |
| Support tickets re: exports | 127/quarter | < 20/quarter | Zendesk dashboard |
| User satisfaction (this feature) | N/A | 4.5/5 | In-app survey |
```

### Example: User Story with Acceptance Criteria
```markdown
**As an** account manager
**I want to** schedule automated weekly reports to be sent to my clients
**So that** I don't have to manually export and email data every Monday morning

**Acceptance Criteria:**
- [ ] User can select report type from template library
- [ ] User can choose delivery frequency (daily/weekly/monthly)
- [ ] User can customize recipient email addresses (up to 10)
- [ ] User receives confirmation when report is sent
- [ ] User can preview report before scheduling
- [ ] System sends reports on schedule with 99% reliability
- [ ] Reports include data up to the previous complete day/week/month
```

---

## Tips for Different Project Sizes

### For Small Features (1-2 weeks of work)
- Keep it to 2-3 pages
- Focus on problem, user story, and must-have requirements
- Skip elaborate timelines and extensive stakeholder lists

### For Medium Projects (1-2 months)
- Use the full template
- Include phased rollout if applicable
- Add wireframes and technical considerations

### For Large Initiatives (3+ months)
- Create a master PRD with linked sub-PRDs for major components
- Include extensive competitive analysis
- Add detailed risk assessment and contingency plans
- Schedule regular PRD review meetings

---

## Output Instructions

When generating a PRD:

1. **Ask clarifying questions** if the user hasn't provided enough context
2. **Generate the complete PRD** using the template above
3. **Save it as `PRD.md`** in the working directory
4. **Customize sections** based on project complexity (omit unnecessary sections for simple features)
5. **Use placeholders** like `[TBD]` or `[To be determined with design team]` for unknowns
6. **Make it actionable** - stakeholders should know exactly what to do next after reading

---

## Common Mistakes to Avoid

❌ **Writing solutions instead of requirements**
   - Wrong: "Add a blue button that opens a modal"
   - Right: "Users need a way to create a new project from the dashboard"

❌ **Vague success metrics**
   - Wrong: "Improve user engagement"
   - Right: "Increase daily active users by 15% within 3 months"

❌ **Skipping the 'why'**
   - Always explain the business value and user benefit

❌ **Feature creep in requirements**
   - Use "Won't Have" section to explicitly defer nice-to-haves

❌ **No stakeholder alignment**
   - Get reviews from engineering, design, and business stakeholders

❌ **Stale PRDs**
   - Update as decisions change; don't let it become outdated

---

## Follow-Up Documents

After creating a PRD, the user may need:
- **Design.md** - Technical design for implementation
- **Architecture.md** - System architecture decisions
- **Roadmap.md** - Timeline and phased delivery plan
- **README.md** - End-user documentation

Suggest these follow-ups when appropriate!
