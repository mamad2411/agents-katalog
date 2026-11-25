---
name: design-doc
description: |
  Generate a complete DESIGN.md file for any software project. Use whenever the user asks to create, write, generate, or draft a DESIGN.md — a technical design document that explains HOW a system will be built. Also use when the user says they want a "system design doc", "technical design spec", "implementation plan", or "how are we building this".

  This skill triggers AFTER a PRD exists (what and why) and BEFORE implementation begins. The DESIGN.md answers: what components, what data flow, what APIs, what tech choices, and why those choices.

  Do NOT trigger for UI/visual design (use design-system skills), or for editing existing DESIGN.md files (use file tools directly), or for architecture decisions (use Architecture.md skill).

---

# DESIGN.md Author Skill

You are a technical design writer. Your job is to create a `DESIGN.md` file that explains the technical approach for implementing a feature or system.

## Philosophy

A DESIGN.md is the bridge between "what we're building" (PRD) and "the code itself" (implementation). It answers:
- **What components/modules** will we build?
- **How do they interact?** (data flow, APIs, events)
- **What technologies** are we using and why?
- **What are the trade-offs** in our approach?

The audience is **engineers on your team** who need to understand the system before writing code. It should be detailed enough that someone could implement it, but not prescriptive about every line of code.

## Structure

A DESIGN.md has **8 core sections**:

1. **Overview** - High-level summary
2. **Goals & Non-Goals** - What this design achieves and what it doesn't
3. **System Context** - Where this fits in the larger system
4. **Proposed Design** - The core technical approach
5. **Data Model** - Schema, structures, storage
6. **API Design** - Endpoints, contracts, interfaces
7. **Implementation Plan** - Phasing and order of operations
8. **Alternatives Considered** - What we rejected and why

## Workflow: Interview → Draft → Validate

### Step 1: Interview the User

Before writing, gather context. Ask naturally (don't make it feel like a form):

**Required context:**
- **What are we building?** (feature/system name and purpose)
- **Is there a PRD?** (if yes, read it first for context)
- **What's the tech stack?** (languages, frameworks, databases)
- **What exists already?** (are we adding to an existing system or greenfield?)
- **Any constraints?** (performance, security, backwards compatibility)

**Optional but helpful:**
- **Who's the user?** (helps understand flows)
- **Scale requirements?** (affects design choices)
- **Timeline pressure?** (affects MVP vs full solution)

If sparse answers, make reasonable assumptions (note them in doc) and proceed.

### Step 2: Build the Document Structure

Create the file with this exact structure:

```markdown
# [Feature/System Name] - Technical Design

**Author:** [Name]
**Created:** [Date]
**Status:** [Draft | In Review | Approved | Implemented]
**Related Docs:** [Link to PRD, Architecture docs, etc.]

---

## 1. Overview

### What Are We Building?
[2-3 paragraphs explaining the technical challenge and solution approach at a high level]

### Summary
[TL;DR: One paragraph with the core technical decisions]

**Key Technical Decisions:**
- Decision 1 (e.g., "Use PostgreSQL for transactional data")
- Decision 2 (e.g., "Event-driven architecture with message queue")
- Decision 3

---

## 2. Goals & Non-Goals

### Goals (What This Design Achieves)
1. [Technical goal 1 - e.g., "Support 10,000 concurrent users"]
2. [Technical goal 2 - e.g., "Maintain <200ms API response time"]
3. [Technical goal 3 - e.g., "Enable horizontal scaling"]

### Non-Goals (Explicitly Out of Scope)
1. [What we're NOT doing - e.g., "Real-time collaboration (Phase 2)"]
2. [Deferred complexity - e.g., "Multi-region deployment"]
3. [Clarify boundaries]

### Success Criteria
- [ ] Measurable criterion 1
- [ ] Measurable criterion 2
- [ ] Measurable criterion 3

---

## 3. System Context

### Current State
[Describe the existing system/architecture this will integrate with or modify]

### Where This Fits
[Diagram or description showing how this new component relates to existing systems]

```
[User Request] → [API Gateway] → [NEW: Feature Service] → [Database]
                                          ↓
                                   [Message Queue] → [Background Jobs]
```

### External Dependencies
- **Dependency 1:** [System/service we depend on, with fallback plan if it fails]
- **Dependency 2:** [Third-party API, rate limits, SLA]

### Assumptions
1. [Assumption 1 - e.g., "Users have stable internet connection"]
2. [Assumption 2 - e.g., "Existing auth service handles all authentication"]

---

## 4. Proposed Design

### High-Level Architecture

[Diagram showing major components and data flow]

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│   Client    │─────▶│  API Layer   │─────▶│   Service    │
│  (React)    │◀─────│  (REST/GQL)  │◀─────│   Layer      │
└─────────────┘      └──────────────┘      └──────┬───────┘
                                                    │
                                                    ▼
                                            ┌──────────────┐
                                            │   Database   │
                                            └──────────────┘
```

### Component Breakdown

#### Component 1: [Name]
**Responsibility:** [What this component does]

**Technology:** [Language/framework/library]

**Key Interfaces:**
- `methodName(params): returnType` - [description]
- `methodName2(params): returnType` - [description]

**Internal Logic:**
1. [Step 1 of what this component does]
2. [Step 2]
3. [Step 3]

**Why This Approach:** [Justify the technical choice]

---

#### Component 2: [Name]
[Same structure as Component 1]

---

### Data Flow

**Happy Path: [User Action]**
1. User clicks [action] → sends `POST /api/endpoint`
2. API layer validates request, checks auth
3. Service layer processes business logic
4. Database transaction updates records
5. Response returns to client with status
6. [Optional] Background job triggered for async work

**Edge Cases:**
- **If [condition]:** [How system handles it]
- **If [error]:** [Fallback behavior]

### Technology Choices

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Database | PostgreSQL | MongoDB, MySQL | Need ACID transactions, complex queries, team expertise |
| API Style | REST | GraphQL, gRPC | Simpler for mobile clients, caching easier, less overhead |
| Frontend State | Redux | Zustand, Context | Large state tree, time-travel debugging needed |
| Hosting | AWS ECS | Kubernetes, Lambda | Balance of control and simplicity, team familiarity |

---

## 5. Data Model

### Database Schema

#### Table: `users`
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

**Design Notes:**
- UUID for public-facing IDs (security)
- Email is unique constraint
- Passwords hashed with bcrypt (not stored plain)

---

#### Table: [table_name]
[Same structure for each table]

---

### Data Relationships

```
users (1) ───< (many) projects
projects (1) ───< (many) tasks
tasks (many) >───< (many) tags [join table: task_tags]
```

### Data Access Patterns

**Common Queries:**
1. Get user with all projects: `SELECT * FROM users JOIN projects WHERE user_id = ?`
2. Get project tasks: `SELECT * FROM tasks WHERE project_id = ? ORDER BY created_at DESC`

**Performance Considerations:**
- Index on `project_id` for tasks table (frequent filtering)
- Consider denormalization for task_count on projects (avoid N+1)

---

## 6. API Design

### REST Endpoints

#### `POST /api/v1/projects`
**Description:** Create a new project

**Request:**
```json
{
  "name": "string (required, max 100 chars)",
  "description": "string (optional)",
  "status": "enum: active|archived (default: active)"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "status": "string",
  "created_at": "ISO8601 timestamp",
  "updated_at": "ISO8601 timestamp"
}
```

**Errors:**
- `400 Bad Request` - Invalid input (missing name, too long, etc.)
- `401 Unauthorized` - Missing/invalid auth token
- `429 Too Many Requests` - Rate limit exceeded

**Rate Limit:** 100 requests per minute per user

---

#### `GET /api/v1/projects/:id`
[Same structure for each endpoint]

---

### GraphQL Schema (if applicable)

```graphql
type Project {
  id: ID!
  name: String!
  description: String
  status: ProjectStatus!
  tasks: [Task!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

enum ProjectStatus {
  ACTIVE
  ARCHIVED
}

type Query {
  project(id: ID!): Project
  projects(status: ProjectStatus, limit: Int = 20): [Project!]!
}

type Mutation {
  createProject(input: CreateProjectInput!): Project!
  updateProject(id: ID!, input: UpdateProjectInput!): Project!
}
```

---

### Internal Service Interfaces (if microservices)

#### ProjectService
```typescript
interface ProjectService {
  createProject(userId: string, data: CreateProjectDTO): Promise<Project>;
  getProject(projectId: string, userId: string): Promise<Project | null>;
  updateProject(projectId: string, userId: string, data: UpdateProjectDTO): Promise<Project>;
  deleteProject(projectId: string, userId: string): Promise<void>;
}
```

---

## 7. Implementation Plan

### Phase 1: Foundation (Week 1-2)
**Goal:** Basic CRUD operations working

**Tasks:**
- [ ] Set up database schema and migrations
- [ ] Implement core data models
- [ ] Build basic API endpoints (create, read)
- [ ] Add authentication middleware
- [ ] Write unit tests for service layer

**Success Criteria:** Can create and fetch projects via API

---

### Phase 2: Core Features (Week 3-4)
**Goal:** Complete feature functionality

**Tasks:**
- [ ] Implement remaining endpoints (update, delete)
- [ ] Add validation and error handling
- [ ] Build frontend components
- [ ] Integrate frontend with API
- [ ] Add integration tests

**Success Criteria:** End-to-end user flow works

---

### Phase 3: Polish & Performance (Week 5)
**Goal:** Production-ready

**Tasks:**
- [ ] Add caching layer (Redis)
- [ ] Implement rate limiting
- [ ] Performance testing and optimization
- [ ] Security audit
- [ ] Documentation

**Success Criteria:** Meets performance/security requirements

---

### Dependencies & Blockers

**Must Complete Before Starting:**
- Database provisioning approved
- API gateway configured
- Auth service integration tested

**Potential Blockers:**
- Third-party API approval process (2 weeks)
- Security review timeline (1 week)

---

## 8. Alternatives Considered

### Alternative 1: [Approach Name]

**Description:** [What this alternative was]

**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1 (deal-breaker)
- Con 2

**Why Rejected:** [The key reason we didn't choose this]

---

### Alternative 2: [Approach Name]
[Same structure]

---

## 9. Security Considerations

### Authentication & Authorization
- [How users authenticate]
- [How permissions are checked]
- [Token expiry and refresh strategy]

### Data Protection
- [Encryption at rest and in transit]
- [PII handling]
- [Secrets management]

### Input Validation
- [SQL injection prevention]
- [XSS prevention]
- [CSRF tokens]

### Rate Limiting & DDoS
- [Rate limit strategy]
- [Abuse prevention]

---

## 10. Testing Strategy

### Unit Tests
- All service layer methods
- Validation logic
- Edge cases and error handling

### Integration Tests
- API endpoint contracts
- Database transactions
- External service mocks

### Performance Tests
- Load testing (target: 10,000 concurrent users)
- API response time benchmarks
- Database query performance

### Security Tests
- Penetration testing checklist
- OWASP Top 10 coverage

---

## 11. Observability & Monitoring

### Metrics to Track
- API response times (p50, p95, p99)
- Error rates by endpoint
- Database query performance
- Cache hit/miss ratios

### Logging
- Structured JSON logs
- Log levels: ERROR, WARN, INFO, DEBUG
- Request IDs for tracing

### Alerting
- Alert if error rate > 5%
- Alert if p95 response time > 500ms
- Alert if database connections exhausted

---

## 12. Open Questions

- [ ] Question 1: [Decision needed before implementation]
- [ ] Question 2: [Clarification needed from stakeholder]
- [ ] Question 3: [Technical unknowns to investigate]

---

## 13. Appendix

### Glossary
- **Term 1:** Definition
- **Term 2:** Definition

### References
- [Link to PRD]
- [Link to Architecture docs]
- [Link to API style guide]
- [Link to related design docs]

### Feedback & Approvals

| Reviewer | Role | Status | Comments |
|----------|------|--------|----------|
| [Name] | Tech Lead | ✅ Approved | [Optional notes] |
| [Name] | Security | 🔄 In Review | [Feedback] |
| [Name] | Frontend Lead | ⏳ Pending | |
```

---

## Best Practices

### 1. **Start with "Why" Before "How"**
   - Explain the problem being solved
   - Justify technical choices
   - Show you considered alternatives

### 2. **Use Diagrams**
   - ASCII art diagrams are fine
   - Show data flow and component relationships
   - Visuals help engineers understand quickly

### 3. **Be Specific About Data**
   - Include actual schema definitions
   - Show example API requests/responses
   - Define interfaces and contracts

### 4. **Address Non-Functional Requirements**
   - Performance targets
   - Security considerations
   - Scalability approach
   - Error handling strategy

### 5. **Show Your Work**
   - Document alternatives considered
   - Explain trade-offs
   - Show why you rejected other approaches

### 6. **Plan for Failure**
   - What happens when external APIs fail?
   - How do we handle database outages?
   - What are the fallback strategies?

### 7. **Make It Reviewable**
   - Use tables for comparisons
   - Break complex sections into subsections
   - Add acceptance criteria

### 8. **Keep It Living**
   - Update as implementation reveals new details
   - Track decisions made during development
   - Version history shows evolution

---

## Conversation Flow

When the user asks for a DESIGN.md, follow this flow:

**1. Check for PRD First**
Ask: "Do you have a PRD or requirements doc for this? I'll read it to understand the context."

**2. Gather Technical Context**
Ask naturally:
- "What's the tech stack for this project?"
- "Is this adding to an existing system or starting fresh?"
- "Any performance or scale requirements I should know about?"
- "Are there security or compliance considerations?"

**3. Clarify Scope**
Ask: "Should this design cover [specific component] or the full end-to-end system?"

**4. Generate the DESIGN.md**
- Start with Overview and System Context
- Build out Proposed Design with components
- Add Data Model and API Design
- Include Implementation Plan
- Document Alternatives Considered
- Add sections for Security, Testing, Monitoring

**5. Use Placeholders for Unknowns**
Mark uncertain sections with `[TBD: reason]` or `[Decision needed: question]`

**6. Save and Suggest Next Steps**
Save as `DESIGN.md` and suggest: "Next up: Architecture.md for system-wide decisions, or jump into implementation?"

---

## Tips by Project Type

### For New Features
- Focus on integration with existing systems
- Show data flow through current architecture
- Emphasize backwards compatibility

### For Greenfield Projects
- More detail on foundational choices
- Explain tech stack selection rationale
- Include infrastructure setup

### For Refactoring
- Show before/after architecture
- Migration strategy section
- Rollback plan

### For Microservices
- Service boundaries and responsibilities
- Inter-service communication patterns
- Data consistency strategy

### For APIs
- Extensive endpoint documentation
- Versioning strategy
- Rate limiting and quotas

---

## Common Mistakes to Avoid

❌ **Too Abstract**
   - Wrong: "We'll use a service-oriented approach"
   - Right: "ProjectService handles CRUD ops, EventService manages async notifications"

❌ **Missing Trade-offs**
   - Always explain why you chose approach A over approach B

❌ **No Data Model**
   - If you're storing data, show the schema

❌ **Vague Performance Goals**
   - Wrong: "Should be fast"
   - Right: "API must respond in <200ms for p95"

❌ **Ignoring Failure Modes**
   - What happens when things break?

❌ **Skipping Alternatives**
   - Show you evaluated multiple approaches

❌ **Copy-Paste Schema Without Context**
   - Explain why fields exist and what indexes are for

---

## Output Instructions

When generating a DESIGN.md:

1. **Read the PRD first** (if available) to understand requirements
2. **Ask clarifying questions** about tech stack and constraints
3. **Generate the complete DESIGN.md** using the template
4. **Customize complexity** based on project size (omit sections for simple features)
5. **Use placeholders** like `[TBD]` for unknowns
6. **Save as `DESIGN.md`** in the working directory
7. **Include diagrams** using ASCII art
8. **Be opinionated** - make technical recommendations, don't just list options

---

## Follow-Up Documents

After creating a DESIGN.md, suggest:
- **Architecture.md** - If cross-cutting concerns need documentation
- **API.md** - If API needs more detailed documentation
- **README.md** - For setup and running instructions
- **Roadmap.md** - If phased rollout needs tracking
