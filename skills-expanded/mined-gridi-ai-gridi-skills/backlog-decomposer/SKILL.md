---
name: backlog-decomposer
description: >
  A skill that decomposes broad implementation requests into multiple independent backlog items.
  It transforms high-level requests like "Build me a shopping mall" into a prioritized backlog list based on MVP.
  Supports AI builder workflows for building full applications from a single prompt.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

# Backlog Decomposer

Decomposes broad implementation requests into systematic backlog items.

## Overview

When a user makes a high-level request like "Build me a shopping mall" or "Develop a blog platform",
this skill decomposes it into small, implementable backlog units so they can be developed sequentially.

```
┌─────────────────────────────────────────────────────────────┐
│  User Input                                                  │
│  "Build me an AI-powered resume builder"                     │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  1. Requirements Analysis                            │    │
│  │     - Identify core features                         │    │
│  │     - Determine tech stack                           │    │
│  │     - Identify constraints                           │    │
│  └─────────────────────────────────────────────────────┘    │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  2. Backlog Decomposition                            │    │
│  │     - Define MVP scope                               │    │
│  │     - Create backlogs per feature                    │    │
│  │     - Analyze dependencies                           │    │
│  └─────────────────────────────────────────────────────┘    │
│       │                                                     │
│       ▼                                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  3. Prioritization                                    │    │
│  │     - MoSCoW classification                          │    │
│  │     - Dependency-based ordering                      │    │
│  │     - MVP vs Future distinction                      │    │
│  └─────────────────────────────────────────────────────┘    │
│       │                                                     │
│       ▼                                                     │
│  Backlog List (in priority order)                            │
│  1. Project initial setup                                    │
│  2. User authentication                                      │
│  3. Resume creation basic feature                            │
│  4. AI recommendation feature                                │
│  ...                                                        │
└─────────────────────────────────────────────────────────────┘
```

## Decomposition Principles

### 0. Service Context Preservation ⚠️ Top Priority Principle

**Problem**: When decomposing backlogs, the original service context can become diluted, risking each backlog being implemented as an entirely different service.
- ❌ Bad example: "AI Service Builder" → "Project Creation and Management" (could be mistaken for a marketing campaign analysis tool)
- ✅ Good example: "AI Service Builder" → "AI Service Project Creation and Management (create a new AI service project in the builder)"

**Principles**:
1. **Include service domain keywords in all backlogs**: The title must include core domain keywords from the original service
2. **Mandatory context inheritance field**: Add a `service_context` field to each backlog to maintain the link to the original request
3. **Specify implementation constraints**: State in each backlog that "This feature must operate within {original service}"
4. **Include example scenarios**: Include concrete usage examples within the service context for each backlog

### 1. MVP First (Minimum Viable Product)

- Prioritize minimum features that deliver core value
- Classify additional features as post-MVP
- Each backlog must be independently deployable

### 2. Technical Dependency Consideration

```
Project Initial Setup
       │
       ▼
  User Authentication ───────────────┐
       │                    │
       ▼                    ▼
  Core Feature A          Core Feature B
       │                    │
       └────────┬───────────┘
                ▼
          Integration Feature
                │
                ▼
          Additional Features
```

### 3. User Value Centric

| Priority | Classification | Description |
|----------|---------------|-------------|
| P0 | Must Have | Essential for MVP; product has no value without it |
| P1 | Should Have | Important but can be added after MVP |
| P2 | Could Have | Nice to have but not core |
| P3 | Won't Have (now) | For future consideration |

## Output Format

### Backlog List Document

```markdown
# Project: {Project Name}

## Overview
- **Request**: {Original user request}
- **Analysis Date**: {Date}
- **Total Backlogs**: {N}
- **MVP Scope**: Backlogs 1-{M}

## ⚠️ Service Context Definition (Applies to All Backlogs)
- **Service Type**: {Core identity of the service, e.g., AI service builder, e-commerce platform, SaaS dashboard}
- **Domain Keywords**: {Core keywords that must be included in all backlogs}
- **Target Users**: {Who uses this service}
- **Core Value**: {Unique value this service provides}
- **Implementation Constraints**: {Boundaries that must not be exceeded}

> 📌 **Implementation Note**: When implementing each backlog, always refer to the service context above.
> For example, the "Project Management" feature must be implemented within the context of "{Service Type}".

## Tech Stack (Recommended)
- Frontend: {Framework}
- Backend: {Framework}
- Database: {DB}
- Other: {Other tools}

## Backlog List

### MVP (Phase 1)

#### BL-001: {Service Name} Project Initial Setup
- **Priority**: P0 (Must Have)
- **Dependencies**: None
- **Service Context**: This feature builds the foundation of {service type}, ensuring all subsequent features operate according to {service domain}.
- **Description**: Project structure, development environment, and basic CI/CD setup for {service type}
- **Implementation Note**: Set up with a structure specialized for {service type}, not a generic web app
- **Expected Deliverables**:
  - Project scaffolding ({service domain} specialized)
  - Development environment setup
  - Basic routing
- **Usage Example**: "{Target user} accesses {service name} and..."

#### BL-002: {Service Name} User Authentication
- **Priority**: P0 (Must Have)
- **Dependencies**: BL-001
- **Service Context**: Authentication system for {service type} users (e.g., {target users})
- **Description**: Sign-up, login, and logout features for {service type} users
- **Implementation Note**: Authentication flow must be designed to match {service domain} usage scenarios
- **Expected Deliverables**:
  - Authentication API (for {service domain} users)
  - Login/sign-up UI
  - Session management
- **Usage Example**: "{Target user} logs into {service name} to perform {core feature}..."

#### BL-003: {Service Name} {Core Feature}
- **Priority**: P0 (Must Have)
- **Dependencies**: BL-001, BL-002
- **Service Context**: ⚠️ Core feature of {service type}. This feature must be implemented within {implementation constraints}.
- **Description**: {Feature description} in the {service domain}
- **Implementation Note**: ❌ Not a generic {similar feature}, ✅ Implement as a {feature} specialized for {service type}
- **Expected Deliverables**:
  - {Deliverables list} ({service domain} specialized)
- **Usage Example**: "{Target user} in {service name} {specific scenario}..."

### Post-MVP (Phase 2+)

#### BL-00N: {Service Name} {Additional Feature}
- **Priority**: P1 (Should Have)
- **Dependencies**: {Dependent backlogs}
- **Service Context**: {Feature description} within {service type}
- **Description**: {Feature description}
- **Implementation Note**: Implement while maintaining the {service domain} context
- **Usage Example**: "{Specific scenario}"

## Dependency Diagram

{ASCII or Mermaid diagram}

## Execution Order

1. BL-001: Project Initial Setup
2. BL-002: User Authentication
3. BL-003: Core Feature A
...

## Notes

- {Project-specific notes}
- {Technical considerations}
```

## Decomposition Process

### Step 1: Requirements Analysis

1. Extract core keywords from the user request
2. Reference similar services/products (known patterns)
3. Derive implicit requirements (authentication, admin, etc.)

### Step 2: Create Feature List

Common pattern-based checklist:

```
[ ] Project initial setup
[ ] User authentication/authorization
[ ] User profile management
[ ] Core domain features (CRUD)
[ ] Search/filtering
[ ] Notifications/email
[ ] Admin features
[ ] Payment (if needed)
[ ] External integrations (if needed)
```

### Step 3: Dependency Analysis

- Identify prerequisites for each feature
- Remove circular dependencies
- Apply minimum dependency principle

### Step 4: Prioritization

MoSCoW + dependency based:

1. Must Have with no dependencies first
2. Must Have with dependencies
3. Should Have (post-MVP)
4. Could Have / Won't Have

## Common Backlog Patterns

### Basic Web Application

```
1. Project initial setup
2. User authentication (sign-up/login)
3. User profile
4. [Core domain] creation
5. [Core domain] list/view
6. [Core domain] edit/delete
7. Search/filter
8. Notifications
9. Admin dashboard
```

### E-commerce

```
1. Project initial setup
2. User authentication
3. Product catalog
4. Product detail
5. Shopping cart
6. Order/payment
7. Order history
8. Search/filter
9. Reviews/ratings
10. Wishlist
11. Admin: Product management
12. Admin: Order management
```

### SaaS/Dashboard

```
1. Project initial setup
2. User authentication
3. Organization/workspace
4. Team member management
5. [Core feature] dashboard
6. [Core feature] CRUD
7. Data visualization
8. Settings/preferences
9. Payment/subscription
10. Notifications/email
```

## Tech Stack Decision Guide

### Recommended Stack by Project Type

| Type | Frontend | Backend | DB |
|------|----------|---------|-----|
| General Web App | Next.js | Next.js API | PostgreSQL |
| Dashboard | React + Vite | FastAPI | PostgreSQL |
| Mobile First | React Native | NestJS | PostgreSQL |
| Real-time App | Next.js | NestJS + WS | PostgreSQL + Redis |
| AI Integration | Next.js | FastAPI | PostgreSQL + Vector DB |

### When an Existing Project Exists

1. Analyze the existing stack (package.json, requirements.txt, etc.)
2. Extend in a way compatible with the existing stack
3. Minimize introduction of new technologies

## Usage

### Starting the Workflow

```
"Build me a shopping mall"
"Develop a blog platform"
"Build a team collaboration tool"
```

### Output Location

```
docs/
├── project-backlog.md          # Full backlog list
└── {backlog-keyword}/             # Working directory for each backlog
    ├── user-stories.md
    ├── wireframes.md
    └── ...
```

## Validation Checklist

Verify after decomposition:

### Service Context Validation (Top Priority) ⚠️
- [ ] **Is the service context definition section clearly written?**
- [ ] **Do all backlog titles include service domain keywords?**
- [ ] **Does each backlog have a "Service Context" field?**
- [ ] **Does each backlog have an "Implementation Note" field?**
- [ ] **Does each backlog have a "Usage Example" within the service context?**
- [ ] **Can you tell what service it is just by reading the backlog titles?** (Context test)
  - ❌ Bad example: "Project Creation Feature" (what project?)
  - ✅ Good example: "AI Service Builder: AI Service Project Creation"

### Existing Validation Items
- [ ] Are all backlogs independently defined?
- [ ] Are dependencies clearly indicated?
- [ ] Is the MVP scope clear?
- [ ] Is each backlog completable within 1-2 days?
- [ ] Are there no circular dependencies?
- [ ] Are there no missing implicit features? (authentication, error handling, etc.)

## PO Review Points

PO approval required after backlog decomposition:

```markdown
## Review Request

### Document Location
docs/project-backlog.md

### Review Items

#### ⚠️ Service Context Review (Top Priority)
1. **Does the service context definition accurately reflect the intent of the original request?**
2. **Is it clear that each backlog will be implemented within this service context?**
3. **Can you identify which service a feature belongs to just by its backlog title?**

#### Feature Review
4. Does the backlog list meet the requirements?
5. Is the MVP scope appropriate?
6. Are the priorities correct?
7. Are there any missing features?
8. Is the tech stack appropriate?

### Result
- Approved → Start development with the first backlog
- Revision needed → Re-decompose backlog
  - Revision must be requested especially when the service context is unclear
```
