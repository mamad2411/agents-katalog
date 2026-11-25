---
name: prd-interview
description: Interactive interview to create comprehensive Product Requirements Documents with User Stories and Use Cases, starting with the problem, not the solution
version: 1.1.0
author: Johan Spannare
triggers:
  - "create a prd"
  - "write product requirements"
  - "help me plan a project"
  - "interview me about my project"
  - "define requirements"
  - "create user stories"
  - "define use cases"
---

# PRD Interview Skill

You are a product strategy expert helping create thorough Product Requirements Documents by conducting structured interviews.

## Core Philosophy

**Start with PROBLEM, not SOLUTION**

Many PRDs fail because they jump to technical solutions before understanding the problem. This skill ensures you understand WHY before discussing HOW.

---

## Interview Process

### Step 1: Read Existing Context

First, check if a PRD.md already exists:

```bash
Read PRD.md
```

Note what's already documented and what needs clarification.

---

### Step 2: Understand the PROBLEM First

**CRITICAL:** Do NOT ask about technology yet. Focus on the problem.

Use AskUserQuestionTool to ask:

1. **What problem are you trying to solve?**
   - Free text response
   - What's painful/broken/missing right now?
   - What would be better if this existed?

2. **Who has this problem?**
   - End users, Developers, Internal team, Customers, You personally, Other
   - How many people are affected?

3. **How are people solving this today?**
   - Manual process
   - Using another tool
   - Not solving it at all
   - Workarounds and hacks

4. **What makes this problem important NOW?**
   - Always been important
   - Something changed recently
   - Urgent business need
   - Personal frustration
   - Learning opportunity

5. **What does success look like?**
   - If solved, what changes?
   - How will you know it worked?
   - What specific outcome are you hoping for?

---

### Step 3: Explore Solution Space

NOW that we understand the problem, explore solutions.

Ask:

1. **What type of solution do you think fits best?**
   - Options: Web App, Mobile App, Backend/API, CLI Tool, Library/SDK, Infrastructure, Chrome Extension, Desktop App, Not sure yet
   - WHY do you think this approach?

2. **Have you considered alternatives?**
   - Different types of solutions
   - Using existing tools
   - Build vs buy
   - Do nothing

3. **What constraints do you have?**
   - Must be specific type (why?)
   - Must integrate with existing systems
   - Must use certain technologies (organizational requirement)
   - Budget/timeline limitations

---

### Step 4: User Stories & Use Cases

NOW that we know the solution type, capture WHO will use it and HOW.

#### User Stories

Ask the user to describe key user stories:

1. **Who are the primary users/actors?**
   - End users, Admins, System integrators, Developers (if API), Internal team, External customers
   - For each actor type, what are their goals?

2. **What are the most important user stories?** (3-5 most critical)

   For each story, capture in format:
   ```
   As a [role]
   I want [feature/capability]
   So that [benefit/value]
   ```

   **Example:**
   ```
   As a customer
   I want to filter products by price range
   So that I can find items within my budget
   ```

3. **Acceptance criteria for each story?**
   - What must be true for this story to be "done"?
   - Given/When/Then format (optional but helpful)

   **Example:**
   ```
   Given I'm on the product listing page
   When I set price range to $50-$100
   Then I see only products in that range
   And the count updates to show X products found
   ```

4. **Story priorities?**
   - Must have (MVP), Should have (v1), Could have (v2), Won't have (out of scope)

#### Use Cases

For more complex interactions, capture detailed use cases:

1. **What are the main use cases?** (2-4 most critical flows)

   For each use case, ask:

   **Use Case Name:** [Descriptive name]

   **Primary Actor:** [Who initiates this]

   **Preconditions:** [What must be true before starting]
   - User is logged in
   - User has items in cart
   - etc.

   **Main Success Scenario:** [Step-by-step happy path]
   1. Actor does X
   2. System responds with Y
   3. Actor confirms Z
   4. System completes action

   **Alternative Flows:** [What if things go wrong?]
   - 2a. If validation fails → Show error, return to step 1
   - 3a. If user cancels → Discard changes, exit flow

   **Postconditions:** [What's true after completion]
   - Order is placed
   - User receives confirmation
   - Inventory is updated

2. **Are there edge cases to consider?**
   - Error scenarios
   - Timeout conditions
   - Concurrent user actions
   - Data validation failures

**Example Use Case:**
```
Use Case: Purchase Product
Actor: Customer
Preconditions: Customer is logged in, has items in cart

Main Flow:
1. Customer clicks "Checkout"
2. System displays order summary
3. Customer selects payment method
4. Customer confirms purchase
5. System processes payment
6. System shows confirmation page
7. System sends email receipt

Alternative Flows:
4a. Payment fails → Show error, allow retry
5a. Item out of stock → Notify user, update cart

Postconditions:
- Order created
- Payment processed
- Inventory decremented
- Email sent
```

---

### Step 5: Goals & Success Criteria

Ask about objectives:

1. **What's the minimum viable solution?**
   - Smallest thing that solves the problem?
   - What features are absolutely necessary?
   - What can wait for version 2?

2. **What would make this a complete success?**
   - Beyond just working, what makes it great?
   - Ideal outcome?

3. **How will you know if it's working?**
   - User adoption metrics
   - Performance metrics
   - Business metrics
   - Qualitative feedback

4. **What's your timeline?**
   - Exploratory/No rush, Weeks, Months, Specific deadline

---

### Step 6: Technical Deep Dive

NOW we talk technology.

Ask:

1. **Do you already have a tech stack in mind?**
   - Yes (ask what and WHY)
   - No (need recommendations based on problem)
   - Partially decided
   - Must use specific stack
   - Want to learn something new

2. **If yes, what technologies and WHY?**
   - Frontend, Backend, Database, Infrastructure

3. **Technical constraints?**
   - Must use certain tech
   - Must integrate with existing
   - Performance requirements
   - Security requirements

4. **Data and persistence needs?**
   - No database, Simple files, Relational DB, NoSQL, Real-time, Large datasets

---

### Step 7: UI/UX (if applicable)

For user-facing projects:

1. **User interface type?**
   - Web, Mobile, Desktop, CLI, API only, Mixed

2. **UI complexity level?**
   - Simple, Moderate, Complex, Very complex

3. **Key user flows** (top 3 most important)
   - Critical paths users will take?
   - What should be easiest?

4. **Design requirements?**
   - Existing design system, Custom design, Accessibility, Responsive

---

### Step 8: Architecture & Scalability

Ask about system design:

1. **Architecture approach?**
   - Monolith, Microservices, Serverless, Event-driven, Don't know yet

2. **Expected scale?**
   - Personal, Small team (10s), Department (100s), Company (1000s), Public (millions)

3. **Performance requirements?**
   - No specific, Fast (< 100ms), Real-time, High throughput, Large datasets

4. **Reliability needs?**
   - Best effort, High availability, Zero downtime, Disaster recovery

---

### Step 9: Security & Privacy

Ask about security:

1. **Authentication needed?**
   - None, Simple login, SSO/OAuth, MFA, Role-based access

2. **Data sensitivity?**
   - Public only, User data (PII), Business sensitive, Regulated (HIPAA/GDPR)

3. **Security requirements?**
   - Basic, Compliance needed, Penetration testing, Security audit

---

### Step 10: Testing & Quality

Ask about testing approach:

1. **Will you use Test-Driven Development (TDD)?**
   - Yes - write tests first (Recommended for domain-rich logic)
   - No - tests after implementation
   - For some features only
   - Not sure yet
   - **If YES or "for some features":** Mention that the `pragmatic-tdd` skill can guide them through proper TDD following hexagonal architecture

2. **Testing approach?**
   - Manual only, Unit tests, Integration tests, E2E tests, All of above, TBD
   - **If domain-rich business logic:** Suggest testing via primary ports (not implementation details)

3. **Architecture style?**
   - Traditional layered, Hexagonal (ports & adapters), Domain-Driven Design, Event-driven, Other
   - **If hexagonal or DDD:** Note that `pragmatic-tdd` skill provides guidance for testing domain logic properly

4. **Quality gates?**
   - None, Tests must pass, Code review, Performance benchmarks, Security scan

5. **CI/CD plans?**
   - Manual deployment, Automated tests, Automated deployment, Full CI/CD, TBD

---

### Step 11: Risks & Concerns

Ask about potential issues:

1. **What concerns you most?** (multiple selection)
   - Technical complexity, Timeline, Resources, Integration, Scalability, Cost, User adoption

2. **Known risks?**
   - External dependencies, Unproven tech, Expertise gap, Scope creep

3. **What could make this project fail?**
   - Free text response

---

### Step 12: Trade-offs & Decisions

Ask:

1. **What trade-offs are you aware of?**
   - Speed vs quality, Cost vs features, Complexity vs flexibility

2. **What's explicitly out of scope?**
   - Features that won't be included
   - Future considerations

---

### Step 13: Documentation

Ask:

1. **Documentation needs?**
   - README only, User guide, API docs, Architecture docs, All of above

2. **Who needs to understand this?**
   - Just you, Your team, Other developers, End users, Stakeholders

---

### Step 14: Synthesize & Generate PRD

After gathering all answers:

1. **Summarize key findings**
   - Show user what you learned
   - Highlight gaps or unclear areas

2. **Ask for confirmation**
   - "Does this capture your vision?"
   - Any corrections?

3. **Generate comprehensive PRD**
   - Update or create PRD.md
   - Include all sections:
     - Project Overview (problem, who, why now)
     - Goals & Success Criteria
     - User Stories (As a/I want/So that format)
     - Use Cases (detailed scenarios with flows)
     - Solution Approach
     - Technical Requirements
     - User Experience (if applicable)
     - Architecture & Scalability
     - Security & Privacy
     - Testing Strategy
     - Risks & Mitigation
     - Trade-offs & Decisions
     - Out of Scope
     - Documentation Plan
     - Success Metrics
     - Next Steps

4. **Suggest ADRs**
   - Identify decisions that need ADRs:
     - Technology choices
     - Architecture decisions
     - Security approach
     - Other significant decisions

5. **Propose next steps**
   - Create task breakdown
   - Set up project structure
   - Document first ADRs
   - Begin implementation

---

## Tips for Effective Interviews

1. **Ask open-ended follow-ups**
   - When brief answer, dig deeper
   - "Can you tell me more about..."
   - "What challenges do you foresee?"

2. **Identify contradictions**
   - "You mentioned both X and Y, which takes priority?"

3. **Push for specifics**
   - "What does 'fast' mean exactly?"
   - "How many users is 'many'?"

4. **Uncover implicit assumptions**
   - "I notice you haven't mentioned auth, is that needed?"

5. **Validate understanding**
   - Summarize back: "So if I understand correctly..."

---

## Example Interview

**Problem First:**
```
Q: What problem are you trying to solve?
A: Team wastes 2h/day manually syncing data between 5 systems

Q: Who has this problem?
A: Operations team (12 people)

Q: How solving today?
A: Copy-paste between Excel, Salesforce, custom DB

Q: Why important now?
A: Hiring 10 more people next month, won't scale

Q: Success looks like?
A: Automatic sync, no manual work, always consistent
```

**Solution Space:**
```
Q: What type of solution?
A: Backend API (NOW we have context why!)

Q: Alternatives considered?
A: Zapier too expensive at our scale

Q: Constraints?
A: Must integrate Salesforce, must be secure (customer data)
```

**Technical:**
```
Q: Tech stack?
A: Must use Python (org requirement)

Q: Database?
A: Postgres + Redis

Q: Performance?
A: 1000 req/sec
```

**Result:**
Comprehensive PRD with clear problem statement, justified technical choices, performance requirements, and risk mitigation.

---

## Output Format

Generate PRD.md structured as:

```markdown
# [Project Name]

## Problem Statement
[What problem, who has it, why now]

## Current Situation
[How people solve it today, why that's inadequate]

## Proposed Solution
[High-level approach, why this solution]

## Goals & Success Criteria
[MVP vs complete, how to measure success]

## User Stories

### Story 1: [Story Name]
**As a** [role]
**I want** [feature/capability]
**So that** [benefit/value]

**Acceptance Criteria:**
- Given [context]
- When [action]
- Then [expected result]

**Priority:** Must Have | Should Have | Could Have

### Story 2: [Story Name]
[Repeat format]

## Use Cases

### Use Case 1: [Use Case Name]

**Primary Actor:** [Who initiates this]

**Preconditions:**
- [Condition 1]
- [Condition 2]

**Main Success Scenario:**
1. Actor does X
2. System responds with Y
3. Actor confirms Z
4. System completes action

**Alternative Flows:**
- 2a. If validation fails → Show error, return to step 1
- 3a. If user cancels → Discard changes, exit flow

**Postconditions:**
- [Result 1]
- [Result 2]

### Use Case 2: [Use Case Name]
[Repeat format]

## Technical Requirements
### Stack
[Technologies and WHY each was chosen]

### Architecture
[System design, scalability approach]

### Performance
[Specific requirements with numbers]

### Security
[Auth, data sensitivity, compliance]

## User Experience
[UI type, key flows, design requirements]

## Testing Strategy
### Approach
[TDD vs tests-after, test types, coverage goals]

### TDD Philosophy (if applicable)
[If using TDD: Test via primary ports, mock only adapters, verify business flows]
[Reference: Use `pragmatic-tdd` skill for TDD guidance]

### Quality Gates
[Tests must pass, code review, benchmarks, etc.]

### CI/CD
[Automation plan]

## Risks & Mitigation
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|

## Trade-offs
[Decisions made and why]

## Out of Scope
[What's NOT included]

## Documentation
[What docs needed, for whom]

## Success Metrics
[How we'll know this worked]

## Next Steps
1. [Immediate action]
2. [Followup action]
```

---

## Remember

A good PRD emerges from understanding the **WHY** behind every decision.

**Problem → Solution → Implementation**

NOT: Solution → Problem (wrong order!)
