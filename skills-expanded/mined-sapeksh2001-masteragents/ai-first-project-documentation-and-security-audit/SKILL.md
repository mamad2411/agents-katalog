---
name: ai-first-project-documentation-and-security-audit
version: 1.0.0
description: |
  Documentation scaffold and security audit skill for AI-assisted app development.
  Use when a user wants to create or update any project doc (README, PRD, APP_FLOW,
  TECH_STACK, FRONTEND_GUIDELINES, BACKEND_STRUCTURE, IMPLEMENTATION_PLAN), audit
  code or APIs for SQLi/XSS/injection, enforce secret isolation, IDOR access control,
  auth hardening, or rate limiting, identify hardcoded credentials or insecure auth
  patterns, generate AI prompts to scaffold the 7 canonical project documents, or
  review a project for missing documentation and create it from scratch.
  TRIGGER for any mention of: PRD, app flow, tech stack, frontend guidelines, backend
  structure, implementation plan, README, security audit, IDOR, rate limiting, XSS,
  SQLi, bcrypt, JWT, session hardening, secret leakage, or documentation-first.
  If any of the 7 documents is missing, immediately offer to scaffold it.
---

# AI-First Project Documentation & Security Audit Skill

## Overview

This skill governs two tightly coupled responsibilities:

1. **Documentation Scaffolding** — Generate, audit, and maintain the 7 canonical project
   documents that form a complete AI-readable knowledge base before any code is written.
2. **Security Audit & Refactor** — Perform full-stack security analysis and remediation
   to bring any project to production-grade safety standards.

Both responsibilities operate under the same rule: **if a project does not have a required
document or security control, create it. If it exists, audit and update it.**

---

## How to Use This Skill

### Step 1 — Detect what exists
Before generating anything, inspect the project for existing documentation files:
```
README.md
PRD.md
APP_FLOW.md
TECH_STACK.md
FRONTEND_GUIDELINES.md
BACKEND_STRUCTURE.md
IMPLEMENTATION_PLAN.md
```

### Step 2 — For each missing file: create it
Use the prompts and templates in this skill to generate each document from scratch,
customized to the project in context.

### Step 3 — For each existing file: audit and update it
Review the existing document against the structure template in this skill. Identify gaps,
outdated sections, security violations, or missing fields, and update them with precise
line-number references.

### Step 4 — Apply the security audit
After documentation is in order, run the security audit against all entry points, secrets,
auth logic, access control, and deployment configuration.

---

## Part 1: Documentation Guide

These 7 documents form the complete knowledge base. When AI reads them:

- **README.md** tells it WHAT the project is and HOW to get started
- **PRD.md** tells it WHAT to build
- **APP_FLOW.md** tells it HOW users navigate
- **TECH_STACK.md** tells it WHICH tools to use
- **FRONTEND_GUIDELINES.md** tells it HOW it should look
- **BACKEND_STRUCTURE.md** tells it HOW data works
- **IMPLEMENTATION_PLAN.md** tells it WHAT ORDER to build

Together, they eliminate AI hallucinations and ensure builds match exact specifications.

---

## Document 0: README.md

### Purpose
The front door to any project. Tells developers, contributors, and AI exactly what the
project is, how to install it, how to run it, and where to find everything else.
This is the document most often missing — always create it if absent.

### Best Practices
- Keep the introduction to 2-3 sentences — clear, direct, no marketing language
- Include a one-command setup path wherever possible
- Document every environment variable required to run the project
- Link to all other documentation files
- Include a project structure overview so AI can navigate the codebase
- Add a contributing section with branch naming, PR, and commit conventions
- Keep it accurate and treat it as a living document

### Structure Template

```markdown
# [Project Name]

[2-3 sentence description of what the project does and who it is for.]

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

---

## Tech Stack
- **Frontend**: [Framework + version]
- **Backend**: [Runtime + framework + version]
- **Database**: [DB + version]
- **Hosting**: [Platform]

See [TECH_STACK.md](./TECH_STACK.md) for complete dependency list.

---

## Project Structure

```
project-root/
├── app/                  # Next.js App Router pages and layouts
├── components/           # Reusable UI components
│   └── ui/               # Design system components
├── lib/                  # Utilities, helpers, API clients
├── prisma/               # Prisma schema and migrations
│   └── schema.prisma
├── server/               # Backend Express routes and middleware
│   ├── routes/
│   ├── middleware/
│   └── services/
├── public/               # Static assets
├── tests/                # Unit and integration tests
├── .env.example          # Environment variable template
├── README.md             # This file
├── PRD.md                # Product Requirements Document
├── APP_FLOW.md           # Application flow and navigation
├── TECH_STACK.md         # Technology stack and versions
├── FRONTEND_GUIDELINES.md # Design system and component library
├── BACKEND_STRUCTURE.md  # Database schema and API contracts
└── IMPLEMENTATION_PLAN.md # Step-by-step build sequence
```

---

## Getting Started

### Prerequisites
- Node.js [version] or higher
- [Database] running locally or connection string available
- [Other prerequisites]

### Installation

```bash
# 1. Clone the repository
git clone [repo-url]
cd [project-name]

# 2. Install dependencies
pnpm install

# 3. Copy environment variables
cp .env.example .env.local
# Edit .env.local with your values

# 4. Set up the database
pnpm db:migrate
pnpm db:seed   # Optional: seed development data

# 5. Start development server
pnpm dev
```

Visit `http://localhost:3000` to view the app.

---

## Environment Variables

| Variable              | Required | Description                        |
|-----------------------|----------|------------------------------------|
| `DATABASE_URL`        | Yes      | PostgreSQL connection string        |
| `JWT_SECRET`          | Yes      | 32+ character random secret         |
| `JWT_REFRESH_SECRET`  | Yes      | Separate secret for refresh tokens  |
| `AWS_ACCESS_KEY_ID`   | No       | S3 file storage (if used)           |
| `RESEND_API_KEY`      | No       | Email sending (if used)             |
| `NEXT_PUBLIC_API_URL` | Yes      | Backend API base URL                |
| `NODE_ENV`            | Yes      | development / production            |

See `.env.example` for the complete list with descriptions.

---

## Documentation

| Document                   | Description                                  |
|----------------------------|----------------------------------------------|
| [PRD.md](./PRD.md)         | Product requirements and success metrics      |
| [APP_FLOW.md](./APP_FLOW.md) | User flows, navigation map, screen inventory |
| [TECH_STACK.md](./TECH_STACK.md) | All dependencies with exact versions    |
| [FRONTEND_GUIDELINES.md](./FRONTEND_GUIDELINES.md) | Design system, tokens, components |
| [BACKEND_STRUCTURE.md](./BACKEND_STRUCTURE.md) | DB schema, API endpoints, auth   |
| [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) | Build phases and milestones    |

---

## Contributing

### Branch Naming
- `feature/[short-description]` — New features
- `fix/[short-description]` — Bug fixes
- `hotfix/[short-description]` — Urgent production fixes
- `docs/[short-description]` — Documentation updates

### Commit Convention
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add user authentication
fix: resolve race condition in session refresh
docs: update README with environment variables
```

### Pull Request Process
1. Create a branch from `develop`
2. Implement changes with tests
3. Run `pnpm lint && pnpm type-check && pnpm test`
4. Open PR against `develop` with description of changes
5. Request review from at least one team member

---

## License
[License type] — see [LICENSE](./LICENSE) for details.
```

### Sample AI Prompt for README Generation

```
Create a comprehensive README.md for [YOUR APP NAME].

Context:
- Project Name: [NAME]
- Description: [2-3 sentence plain-language description]
- Tech Stack: [List from TECH_STACK.md]
- Key Features: [List from PRD.md]

Generate a README.md with these sections:

1. HEADER — Project name and 2-3 sentence description. No marketing language.
2. TABLE OF CONTENTS — Links to all sections.
3. FEATURES — Bullet list from PRD.md P0 features.
4. TECH STACK — Short summary table. Link to TECH_STACK.md.
5. PROJECT STRUCTURE — ASCII tree of all top-level directories with purpose annotation.
6. GETTING STARTED
   - Prerequisites (Node version, DB, etc.)
   - Installation steps with exact commands
   - First run instructions
7. ENVIRONMENT VARIABLES — Table with all variables, whether required, and description.
   Never include actual secret values.
8. DOCUMENTATION TABLE — Links to all 6 other project documents with one-line descriptions.
9. CONTRIBUTING — Branch naming, commit convention (Conventional Commits), PR process.
10. LICENSE — License type and link.

CRITICAL REQUIREMENTS:
- Never include actual secret values in README
- All commands must be copy-pasteable
- Use exact version numbers from TECH_STACK.md
- Link to every documentation file
- Project structure must match actual file layout

OUTPUT FORMAT: Markdown with code blocks for commands, tables for env vars and docs.
```

---

## Document 1: PRD.md (Product Requirements Document)

### Purpose
Your contract with AI. Defines **what** you're building, **who** it's for, and **what
success looks like**. No ambiguity allowed.

### Best Practices
- Start with user goals and problems, not features
- Include explicit out-of-scope items to prevent scope creep
- Use SMART criteria for success metrics (Specific, Measurable, Achievable, Relevant, Time-bound)
- Keep it concise but comprehensive (modern PRDs are blog-post length, not 37-page docs)
- Make it a living document that evolves with the product
- Use clear, specific language — avoid vague terms
- Include user stories in "As a [user], I want [goal], so that [benefit]" format

### Structure Template

```markdown
# Product Requirements Document (PRD)

## 1. Product Overview
- **Project Title**: [Name]
- **Version**: 1.0
- **Last Updated**: [Date]
- **Owner**: [Name]

## 2. Problem Statement
[What user/business problem are you solving? Be specific.]

## 3. Goals & Objectives
### Business Goals
- [Goal 1 with metric]
- [Goal 2 with metric]

### User Goals
- [What users want to accomplish]

## 4. Success Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]
- [How you'll measure success]

## 5. Target Users & Personas
### Primary Persona: [Name]
- **Demographics**: 
- **Pain Points**: 
- **Goals**: 
- **Technical Proficiency**: 

### Secondary Persona: [Name]
[Same format]

## 6. Features & Requirements
### Must-Have Features (P0)
1. **[Feature Name]**
   - Description: [What it does]
   - User Story: As a [user], I want [goal] so that [benefit]
   - Acceptance Criteria:
     - [ ] [Specific, testable criterion]
     - [ ] [Specific, testable criterion]
   - Success Metric: [How you measure this feature's success]

2. [Repeat for each P0 feature]

### Should-Have Features (P1)
[Same format]

### Nice-to-Have Features (P2)
[Same format]

## 7. Explicitly OUT OF SCOPE
- [Thing 1 you will NOT build]
- [Thing 2 you will NOT build]
[This section is critical — prevents AI from adding features you never requested]

## 8. User Scenarios
### Scenario 1: [Name]
- **Context**: [When does this happen?]
- **Steps**: 
  1. [User action]
  2. [System response]
  3. [User action]
- **Expected Outcome**: [What success looks like]
- **Edge Cases**: [What could go wrong?]

## 9. Dependencies & Constraints
- **Technical Constraints**: [Platform limits, API restrictions, etc.]
- **Business Constraints**: [Budget, timeline, team size]
- **External Dependencies**: [Third-party services, APIs]

## 10. Timeline & Milestones
- **MVP**: [Date] — [Features included]
- **V1.0**: [Date] — [Features included]

## 11. Risks & Assumptions
### Risks
- [Risk 1 and mitigation strategy]

### Assumptions
- [Assumption 1 and validation plan]

## 12. Non-Functional Requirements
- **Performance**: [Load time, concurrent users]
- **Security**: [Authentication, data protection]
- **Accessibility**: [WCAG compliance level]
- **Scalability**: [Expected growth]

## 13. References & Resources
- [Links to research, competitor analysis, user interviews]
```

### Sample AI Prompt for PRD Generation

```
Create a comprehensive Product Requirements Document (PRD) for [YOUR APP IDEA].

Context:
- Target Users: [WHO]
- Main Problem: [WHAT PROBLEM]
- Unique Value: [WHY THIS SOLUTION]

Structure the PRD with these sections:

1. PROBLEM STATEMENT
Write a clear, specific problem statement that describes the user pain point or business need.

2. GOALS & OBJECTIVES
Define 3-5 SMART goals with specific, measurable targets.

3. SUCCESS METRICS
Identify 3-5 quantifiable metrics to measure success (e.g., "30% reduction in task completion time").

4. TARGET PERSONAS
Create 2 detailed user personas with:
- Demographics
- Pain points
- Goals
- Technical proficiency level

5. FEATURES & REQUIREMENTS
Organize features into three tiers:
- P0 (Must-Have): Core features required for MVP
- P1 (Should-Have): Important but not critical for launch
- P2 (Nice-to-Have): Future enhancements

For each feature, include:
- Clear description
- User story format: "As a [user], I want [goal] so that [benefit]"
- 3-5 acceptance criteria (specific, testable)
- Success metric

6. EXPLICITLY OUT OF SCOPE
List 5-10 things you will NOT build in this version. Be specific.

7. USER SCENARIOS
Create 3 detailed end-to-end scenarios showing:
- Context (when does this happen)
- Step-by-step user actions and system responses
- Expected outcomes
- Edge cases and error handling

8. NON-FUNCTIONAL REQUIREMENTS
Specify performance, security, accessibility, and scalability requirements.

9. DEPENDENCIES & CONSTRAINTS
List technical and business constraints, external dependencies (APIs, services).

10. TIMELINE
Define MVP and V1.0 milestone dates with included features.

CRITICAL REQUIREMENTS:
- Use specific, measurable criteria (not vague)
- Avoid technical implementation details
- Focus on WHAT to build, not HOW to build it
- Make every requirement testable
- Include edge cases and error states
- Be explicit about what's NOT included

OUTPUT FORMAT: Markdown document with clear headers and bullet points.
```

---

## Document 2: APP_FLOW.md (Application Flow & Navigation)

### Purpose
Maps every page, every user path, every decision point. Prevents AI from guessing
navigation patterns.

### Best Practices
- Start with user goals, not pages
- Document entry points explicitly (how users arrive)
- Show decision points and branching logic
- Include success paths AND error states
- Keep flows focused on single goals (one flow per task)
- Use visual flowchart standards (shapes have meaning)
- Document what triggers each flow

### Structure Template

```markdown
# Application Flow Documentation

## 1. Entry Points
### Primary Entry Points
- **Direct URL**: [What happens when user types URL]
- **Landing Page**: [What the user sees first]
- **Deep Links**: [From email, notifications, ads]
- **OAuth/Social Login**: [Third-party entry points]

### Secondary Entry Points
- **Search Engine**: [SEO landing pages]
- **Marketing Campaigns**: [Campaign-specific entry]

## 2. Core User Flows

### Flow 1: [Flow Name — e.g., "User Registration"]
**Goal**: [What user is trying to accomplish]
**Entry Point**: [Where flow starts]
**Frequency**: [How often this happens]

#### Happy Path
1. **Page: Landing Page**
   - Elements: [Hero section, CTA button]
   - User Action: Clicks "Sign Up"
   - Trigger: Navigate to registration page

2. **Page: Registration Form**
   - Elements: [Email input, Password input, Submit button]
   - User Actions:
     - Enters email
     - Enters password (with validation)
   - Validation:
     - Email format check
     - Password strength requirements
   - Trigger: Submits form

3. **System Action**: Creates user account

4. **Page: Email Verification**
   - Elements: [Verification message, Resend link]
   - User Action: Clicks verification link in email

5. **Page: Welcome Dashboard**
   - Elements: [Onboarding checklist, Quick actions]
   - Success State: User is logged in and onboarded

#### Error States
- **Invalid Email**
  - Display: Inline error message
  - Action: User corrects and resubmits

- **Email Already Exists**
  - Display: Modal with login link
  - Action: Redirect to login

- **Weak Password**
  - Display: Password strength indicator
  - Action: User strengthens password

#### Edge Cases
- User closes browser mid-registration → Save form data, show "Continue" on return
- Email verification link expires → Provide resend option
- User registers but doesn't verify → Send reminder after 24 hours

#### Exit Points
- Success: Dashboard (logged in)
- Abandonment: Close/navigate away
- Redirect: Login page if account exists

---

### Flow 2: [Flow Name]
[Same detailed structure]

## 3. Navigation Map

### Primary Navigation
```
Home
├── Products
│   ├── Category 1
│   │   └── Product Detail
│   │       ├── Add to Cart
│   │       └── Reviews
│   └── Category 2
├── Cart
│   ├── Checkout
│   │   ├── Shipping Info
│   │   ├── Payment
│   │   └── Order Confirmation
│   └── Continue Shopping → Products
├── Account
│   ├── Profile
│   ├── Orders
│   └── Settings
└── Support
```

### Navigation Rules
- **Authentication Required**: [Pages that require login]
- **Redirect Logic**: [When to redirect to login, when to show modal]
- **Back Button Behavior**: [Which pages preserve state]

## 4. Screen Inventory

### Screen: [Screen Name]
- **Route**: `/path/to/screen`
- **Access**: [Public/Authenticated/Admin]
- **Purpose**: [What user accomplishes here]
- **Key Elements**: 
  - [Element 1]
  - [Element 2]
- **Actions Available**:
  - [Action 1] → Leads to [Screen/State]
  - [Action 2] → Leads to [Screen/State]
- **State Variants**: [Loading, Empty, Error, Success]

## 5. Interaction Patterns

### Pattern: Form Submission
- Validation: Client-side (instant) + Server-side (on submit)
- Loading State: Disabled button, spinner
- Success: Redirect OR inline success message
- Error: Inline error messages, keep form data

### Pattern: Infinite Scroll
- Trigger: User scrolls to 80% of page
- Loading: Skeleton screens
- End: "No more items" message

## 6. Decision Points

### Decision: User Authentication Status
```
IF user is NOT logged in
THEN show: Login CTA
AND disable: Account features
ELSE IF user IS logged in
THEN show: Account menu
AND enable: Full features
```

## 7. Error Handling Flows

### 404 Not Found
- Display: Custom 404 page
- Actions: Search, Home link, Popular pages
- Log: 404 errors for fixing broken links

### 500 Server Error
- Display: Friendly error page
- Actions: Retry button, Support contact
- Fallback: Save user's work if possible

### Network Offline
- Display: Offline banner
- Actions: Queue actions for later
- Recovery: Auto-retry when online

## 8. Responsive Behavior

### Mobile-Specific Flows
- Navigation: Hamburger menu instead of top nav
- Forms: One field per screen
- Actions: Bottom sheet for selections

### Desktop-Specific Flows
- Navigation: Full menu visible
- Forms: Multi-column layouts
- Actions: Modals for quick actions

## 9. Animation & Transitions

### Page Transitions
- **Navigation**: Fade in/out (300ms)
- **Modal**: Slide up from bottom (200ms)
- **Drawer**: Slide from side (250ms)

### Micro-interactions
- **Button Click**: Scale(0.95) + Ripple
- **Form Focus**: Border highlight
- **Success**: Checkmark animation
```

### Sample AI Prompt for APP_FLOW Generation

```
Create comprehensive Application Flow documentation (APP_FLOW.md) for [YOUR APP NAME].

Context:
[Provide brief description of app]

Generate documentation with these sections:

1. ENTRY POINTS
List all ways users can enter the app:
- Direct URL access
- Deep links (email, notifications)
- OAuth/social login
- Search engines
- Marketing campaigns

2. CORE USER FLOWS
For each major user task, create a detailed flow:

Required Flows:
- User onboarding/registration
- Main feature usage (e.g., create post, make purchase, book appointment)
- Account management
- Error recovery

For EACH flow, document:

HAPPY PATH (Step-by-step):
- Page/Screen name
- UI elements present
- User actions (clicks, inputs)
- System responses
- Validation rules
- Next page/state
- Success criteria

ERROR STATES (What can go wrong):
- Invalid inputs (how they're handled)
- System errors (display and recovery)
- Timeout scenarios
- Offline behavior

EDGE CASES:
- User abandons flow
- User goes back
- Concurrent actions
- Session expiry

3. NAVIGATION MAP
Create a hierarchical tree showing:
- Main navigation structure
- Sub-pages and nesting
- Cross-links between sections
- Authentication requirements per page

4. SCREEN INVENTORY
For each unique screen/page, specify:
- URL/Route
- Access level (public/authenticated/admin)
- Purpose
- Key UI elements
- Available actions → where they lead
- State variants (loading, empty, error, success)

5. DECISION POINTS
Document every conditional in the flow using IF-THEN logic:
```
IF [condition]
THEN [action/display]
ELSE IF [condition]
THEN [action/display]
ELSE
THEN [default action]
```

6. ERROR HANDLING
Document flows for: 404, 500, network offline, permission denied, form validation failures.
For each: Display shown, user actions available, system recovery.

7. RESPONSIVE BEHAVIOR
Specify how flows differ on: Mobile, Tablet, Desktop.

8. ANIMATIONS & TRANSITIONS
Document: Page transitions (duration, easing), Modal/drawer behavior,
Loading states, Success animations.

CRITICAL REQUIREMENTS:
- Every user action must have a clear next step
- Document BOTH success and failure paths
- Include specific validation rules
- Specify error message wording
- Show state transitions explicitly
- Use consistent naming (match PRD.md features)

OUTPUT FORMAT: Markdown with clear headers, indented lists for hierarchy,
code blocks for decision logic.
```

---

## Document 3: TECH_STACK.md (Technology Stack)

### Purpose
Locks every dependency, tool, and version. Zero ambiguity on what to use.

### Best Practices
- Specify EXACT versions (not "latest")
- Document WHY each choice was made
- Include setup/installation instructions
- List compatibility requirements
- Track security considerations
- Maintain version control practices
- Document update/upgrade policies

### Structure Template

```markdown
# Technology Stack Documentation

## 1. Stack Overview
**Last Updated**: [Date]
**Version**: 1.0

### Architecture Pattern
- **Type**: [Monolithic/Microservices/Serverless]
- **Pattern**: [MVC/MVVM/JAMstack]
- **Deployment**: [Cloud/On-premise/Hybrid]

---

## 2. Frontend Stack

### Core Framework
- **Framework**: Next.js
- **Version**: 14.1.0
- **Reason**: Server-side rendering, file-based routing, built-in optimization
- **Documentation**: https://nextjs.org/docs
- **License**: MIT

### UI Library
- **Library**: React
- **Version**: 18.2.0
- **Reason**: Component-based architecture, large ecosystem
- **Documentation**: https://react.dev
- **License**: MIT

### State Management
- **Library**: Zustand
- **Version**: 4.4.7
- **Reason**: Lightweight, TypeScript-first, minimal boilerplate
- **Documentation**: https://github.com/pmndrs/zustand
- **License**: MIT
- **Alternatives Considered**: Redux (rejected: too verbose), Context API (rejected: performance)

### Styling
- **Framework**: Tailwind CSS
- **Version**: 3.4.1
- **Configuration**: Custom config at `tailwind.config.js`
- **Reason**: Utility-first, fast development, consistent design
- **Documentation**: https://tailwindcss.com/docs
- **License**: MIT

### Type Safety
- **Language**: TypeScript
- **Version**: 5.3.3
- **tsconfig**: Strict mode enabled
- **Reason**: Type safety, better IDE support, fewer runtime errors

### Form Handling
- **Library**: React Hook Form
- **Version**: 7.49.3
- **Validation**: Zod 3.22.4
- **Reason**: Performance, minimal re-renders, TypeScript support

### HTTP Client
- **Library**: Axios
- **Version**: 1.6.5
- **Interceptors**: Auth token injection, error handling
- **Reason**: Request/response interceptors, better error handling than fetch

### Routing
- **Built-in**: Next.js App Router
- **Version**: 14.1.0 (Next.js version)
- **Structure**: File-based routing with server components

---

## 3. Backend Stack

### Runtime
- **Platform**: Node.js
- **Version**: 20.11.0 LTS
- **Package Manager**: pnpm 8.14.1
- **Reason**: Performance, modern features, long-term support

### Framework
- **Framework**: Express.js
- **Version**: 4.18.2
- **Middleware**:
  - cors@2.8.5
  - helmet@7.1.0 (security headers)
  - morgan@1.10.0 (logging)
  - express-rate-limit@7.1.5
- **Reason**: Mature, flexible, large ecosystem

### Database
- **Primary**: PostgreSQL
- **Version**: 16.1
- **ORM**: Prisma 5.8.1
- **Connection Pooling**: PgBouncer
- **Reason**: ACID compliance, JSON support, mature

#### Schema Management
- **Migrations**: Prisma Migrate
- **Seeding**: Prisma Seed scripts
- **Backup Strategy**: Daily automated backups

### Caching
- **System**: Redis
- **Version**: 7.2.4
- **Client**: ioredis 5.3.2
- **Use Cases**: Session storage, API caching, rate limiting
- **TTL Strategy**: 1 hour for API cache, 7 days for sessions

### Authentication
- **Strategy**: JWT (JSON Web Tokens)
- **Library**: jsonwebtoken 9.0.2
- **Hashing**: bcrypt 5.1.1 (12 rounds)
- **Token Expiry**: Access (15 min), Refresh (7 days)
- **Storage**: HTTP-only cookies

### File Storage
- **Service**: AWS S3
- **SDK**: @aws-sdk/client-s3 3.490.0
- **CDN**: CloudFront
- **Reason**: Scalable, reliable, cost-effective

### Email Service
- **Provider**: Resend
- **Library**: resend 3.0.0
- **Templates**: React Email
- **Reason**: Developer-friendly, reliable delivery

---

## 4. DevOps & Infrastructure

### Version Control
- **System**: Git
- **Platform**: GitHub
- **Branch Strategy**:
  - `main` (production)
  - `develop` (staging)
  - `feature/*` (features)
  - `hotfix/*` (urgent fixes)

### CI/CD
- **Platform**: GitHub Actions
- **Workflows**:
  - PR checks (lint, type-check, tests)
  - Deploy to staging (on merge to develop)
  - Deploy to production (on merge to main)

### Hosting
- **Frontend**: Vercel
- **Backend**: Railway / Fly.io
- **Database**: Supabase / Railway
- **Reason**: Easy deployment, auto-scaling, edge network

### Monitoring
- **Error Tracking**: Sentry
- **Version**: @sentry/nextjs 7.99.0
- **Analytics**: Vercel Analytics
- **Logging**: Better-logging 4.1.0

### Testing
- **Unit Tests**: Vitest 1.2.0
- **Integration**: Supertest 6.3.4
- **E2E**: Playwright 1.41.1
- **Coverage Target**: 80%

---

## 5. Development Tools

### Code Quality
- **Linter**: ESLint 8.56.0
  - Config: eslint-config-next 14.1.0
- **Formatter**: Prettier 3.2.4
  - Config: .prettierrc.json
- **Git Hooks**: Husky 8.0.3
  - Pre-commit: Lint + Format
  - Pre-push: Tests

### IDE Recommendations
- **Editor**: VS Code
- **Extensions**:
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense
  - Prisma

---

## 6. Environment Variables

### Required Variables
```bash
# Database
DATABASE_URL="postgresql://..."
DIRECT_DATABASE_URL="postgresql://..." # For migrations

# Auth
JWT_SECRET="..." # 32+ character random string
JWT_REFRESH_SECRET="..."

# AWS S3
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_REGION="us-east-1"
AWS_BUCKET_NAME="..."

# Email
RESEND_API_KEY="..."
FROM_EMAIL="noreply@..."

# App
NEXT_PUBLIC_API_URL="http://localhost:3001"
NODE_ENV="development"
```

---

## 7. Package.json Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write .",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:e2e": "playwright test",
    "db:migrate": "prisma migrate dev",
    "db:generate": "prisma generate",
    "db:studio": "prisma studio",
    "db:seed": "ts-node prisma/seed.ts"
  }
}
```

---

## 8. Dependencies Lock

### Frontend Dependencies

```json
{
  "next": "14.1.0",
  "react": "18.2.0",
  "react-dom": "18.2.0",
  "typescript": "5.3.3",
  "tailwindcss": "3.4.1",
  "zustand": "4.4.7",
  "react-hook-form": "7.49.3",
  "zod": "3.22.4",
  "@hookform/resolvers": "3.3.4",
  "axios": "1.6.5",
  "lucide-react": "0.312.0",
  "clsx": "2.1.0",
  "tailwind-merge": "2.2.0"
}
```

### Backend Dependencies

```json
{
  "express": "4.18.2",
  "cors": "2.8.5",
  "helmet": "7.1.0",
  "morgan": "1.10.0",
  "express-rate-limit": "7.1.5",
  "jsonwebtoken": "9.0.2",
  "bcrypt": "5.1.1",
  "prisma": "5.8.1",
  "@prisma/client": "5.8.1",
  "ioredis": "5.3.2",
  "@aws-sdk/client-s3": "3.490.0",
  "resend": "3.0.0",
  "dotenv": "16.3.1"
}
```

### Dev Dependencies

```json
{
  "vitest": "1.2.0",
  "@testing-library/react": "14.1.2",
  "supertest": "6.3.4",
  "@playwright/test": "1.41.1",
  "eslint": "8.56.0",
  "prettier": "3.2.4",
  "husky": "8.0.3",
  "ts-node": "10.9.2"
}
```
```

### Sample AI Prompt for TECH_STACK Generation

```
Create a comprehensive Technology Stack document (TECH_STACK.md) for [YOUR APP NAME].

Context:
[List core technologies you want to use]

Generate a document with these sections:

1. STACK OVERVIEW
Define:
- Architecture pattern (e.g. Monolithic, Serverless)
- Core design patterns
- Deployment strategy

2. FRONTEND STACK
For each part of the frontend, specify:
- Library/Framework name
- EXACT version number
- Rationale for choice
- Documentation link
- Alternatives considered and why they were rejected

Include:
- Core Framework (e.g. Next.js, Vite)
- UI Library
- State Management
- Styling (e.g. Tailwind, CSS Modules)
- Type Safety (e.g. TypeScript)
- Form Handling
- HTTP Client

3. BACKEND STACK
For each part of the backend, specify:
- Runtime & Framework
- Database & ORM
- Caching system
- Authentication strategy
- File storage
- Email service

Include exact versions and rationale for every choice.

4. DEVOPS & INFRASTRUCTURE
Document:
- Version Control (Git provider, branching strategy)
- CI/CD platform and workflow
- Hosting providers for all layers
- Monitoring & logging tools
- Testing frameworks (Unit, Integration, E2E)

5. DEVELOPMENT TOOLS
List:
- Code quality tools (Linting, Formatting)
- Git hooks configuration
- Recommended IDE extensions

6. ENVIRONMENT VARIABLES
Provide a template block (.env.example style) with:
- All required variables
- Descriptions for each
- Never include actual secrets

7. PACKAGE.JSON SCRIPTS
Define the standard set of scripts required to:
- Build
- Develop
- Test
- Lint
- Deploy

8. DEPENDENCIES LOCK
Create three JSON blocks showing EXACT versions for:
- Frontend dependencies
- Backend dependencies
- Dev dependencies

CRITICAL REQUIREMENTS:
- Use exact versions (no ~ or ^)
- Provide technical rationale for every major choice
- Ensure all parts of the stack are compatible
- Focus on production-readiness (security, monitoring)
- Align with implementation phases

OUTPUT FORMAT: Markdown with clear headers and JSON/bash code blocks.
```

---

## Document 4: FRONTEND_GUIDELINES.md (Design System)

### Purpose
Style guide and component library. Zero guessing on how things look.

### Best Practices
- Define tokens before components
- Include accessibility requirements
- Document state variants (hover, active, disabled)
- Show layout patterns (grid, spacing)
- Maintain design consistency across elements
- Include component usage examples
- Define responsive design breakpoints

### Structure Template

```markdown
# Frontend Style & Component Guidelines

## 1. Visual Language

### Color Palette
#### Primary Colors
- **Primary-500**: `#3B82F6` (Main brand color)
- **Primary-600**: `#2563EB` (Hover states)
- **Primary-700**: `#1D4ED8` (Active states)

#### Semantic Colors
- **Success**: `#10B981`
- **Warning**: `#F59E0B`
- **Error**: `#EF4444`
- **Info**: `#3B82F6`

#### Neutral Colors
- **Gray-50**: `#F9FAFB` (Backgrounds)
- **Gray-900**: `#111827` (Main text)

### Typography
- **Primary Font**: 'Inter', sans-serif
- **Heading Font**: 'Outfit', sans-serif

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1      | 36px | 700    | 1.2         |
| H2      | 30px | 600    | 1.2         |
| Body    | 16px | 400    | 1.5         |
| Small   | 14px | 400    | 1.4         |

### Spacing System (8px Grid)
- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px

### Elevation & Shadows
- **sm**: 0 1px 2px 0 rgb(0 0 0 / 0.05)
- **md**: 0 4px 6px -1px rgb(0 0 0 / 0.1)

---

## 2. Core Components

### Button Component
#### Variants
- **Primary**: Brand color background, white text
- **Secondary**: Light gray background, dark text
- **Outline**: Border only, brand color text
- **Ghost**: No background, brand color text

#### States
- **Default**: Standard appearance
- **Hover**: 10% darker background
- **Active**: 20% darker background, subtle scale down
- **Disabled**: 50% opacity, `not-allowed` cursor
- **Loading**: Spinner icon, prevents clicks

#### Code Pattern (React/Tailwind)
```tsx
const Button = ({ variant = 'primary', size = 'md', isLoading, children, ...props }) => {
  // logic here
}
```

---

## 3. Layout Patterns
- **Container**: Max-width 1280px, centered
- **Grid**: 12-column system, 24px gutter
- **Card**: White background, md shadow, 8px border-radius

---

## 4. Accessibility (WCAG 2.1 AA)
- **Contrast**: Minimum 4.5:1 for normal text
- **Focus**: Visible focus rings on all interactive elements
- **Labels**: All form inputs must have associated labels
- **ARIA**: Use appropriate roles for complex components

---

## 5. Icons
- **Library**: Lucide React
- **Stroke Width**: 2px
- **Standard Size**: 20px for inline, 24px for standalone
```

---

## Document 5: BACKEND_STRUCTURE.md (Database & API)

### Purpose
Data contract. Defines **how** data is stored and **how** it is accessed.

### Best Practices
- Define schema before endpoints
- Document auth/security requirements for every route
- Match data types to application needs
- Include indexing and performance considerations
- Use descriptive naming for tables and fields
- Document API error responses
- Define data validation rules

### Structure Template

```markdown
# Backend & Database Architecture

## 1. Database Schema (PostgreSQL)

### Model: User
| Field         | Type      | Constraints           | Description              |
|---------------|-----------|-----------------------|--------------------------|
| id            | UUID      | Primary Key, Default  | Unique identifier        |
| email         | String    | Unique, Indexed       | User's email address     |
| password_hash | String    | Not Null              | Bcrypt hashed password   |
| name          | String    |                       | Full name                |
| created_at    | DateTime  | Default: Now          | Registration timestamp   |

### Model: Product
| Field       | Type      | Constraints   | Description           |
|-------------|-----------|---------------|-----------------------|
| id          | UUID      | Primary Key   | Unique identifier     |
| title       | String    | Indexed       | Product name          |
| price       | Decimal   | Not Null      | Price in USD          |
| stock       | Integer   | Default: 0    | Available quantity    |

### Relationships
- **User** has many **Orders** (1:N)
- **Order** has many **OrderItems** (1:N)
- **Product** belongs to **Category** (N:1)

---

## 2. API Design (REST)

### Base URL: `/api/v1`

### Authentication
- Header: `Cookie: access_token=...`
- Strategy: JWT in HTTP-only cookies

### Endpoints

#### User Management
- `POST /auth/register` - Create new account
- `POST /auth/login` - Authenticate and set cookie
- `GET /auth/me` - Get current session user

#### Products
- `GET /products` - List all products (with pagination)
- `GET /products/:id` - Get single product detail
- `POST /products` (Admin Only) - Create new product

---

## 3. Security Requirements
- **Input Validation**: Use Zod for all request bodies
- **Rate Limiting**: 100 requests per 15 minutes per IP
- **CORS**: Restricted to frontend domain only
- **Headers**: Helmet.js for security defaults
- **Access Control**: Role-based (User vs. Admin)
```

---

## Document 6: IMPLEMENTATION_PLAN.md

### Purpose
The checklist. Prevents "blank page" syndrome and keeps builds atomic.

### Best Practices
- Follow dependencies (Auth before Dashboard)
- Keep phases small and testable
- Include verification steps for each task
- Document state transitions clearly
- Align with technical and business goals
- Provide clear exit criteria for each phase
- Track dependencies between tasks

### Structure Template

```markdown
# Implementation Plan

## Phase 1: Foundation & Environment Setup
- [ ] Initialize project with Next.js, TypeScript, and Tailwind
- [ ] Configure ESLint, Prettier, and Husky hooks
- [ ] Set up PostgreSQL and Prisma
- [ ] Create basic folder structure
- [ ] **Verification**: Run `npm run dev` and `npx prisma db pull` successfully

## Phase 2: Authentication & User Management
- [ ] Implement JWT-based auth with HTTP-only cookies
- [ ] Create Login and Registration pages
- [ ] Set up Protected Routes middleware
- [ ] **Verification**: User can sign up, log in, and access protected `/dashboard`

## Phase 3: Core Feature: [Feature Name]
- [ ] Design database models for [Feature]
- [ ] Build API endpoints for CRUD operations
- [ ] Create frontend components for [Feature]
- [ ] **Verification**: [Step to verify feature works end-to-end]

## Phase 4: Styling & UI Polish
- [ ] Apply final Design System tokens
- [ ] Implement Skeleton states and loading UI
- [ ] Ensure mobile responsiveness across all pages

## Phase 5: Production & Deployment
- [ ] Set up CI/CD with GitHub Actions
- [ ] Configure environment variables in Vercel/Railway
- [ ] Run final security audit and performance tests
```

---

## Part 2: Security Audit & Remediation Guide

### 1. The 10-Point Security Checklist
Always run this audit before any deployment.

| Category             | Check                                                                 | Remediation Strategy                           |
|----------------------|-----------------------------------------------------------------------|------------------------------------------------|
| **Auth**             | Is bcrypt used for hashing with at least 12 rounds?                   | Refactor hash logic in `auth.service.js`       |
| **Auth**             | Are JWTs stored in LocalStorage? (LEAK RISK)                          | Move to HTTP-only, Secure, SameSite=Strict cookies |
| **Exposure**         | Are there hardcoded API keys or DB strings?                           | Move to `.env` and add to `.gitignore`         |
| **Injection**        | Are raw SQL queries used?                                             | Convert to Prisma ORM or parameterized queries  |
| **Injection**        | Is user input rendered directly in HTML (XSS)?                        | Sanitize with `dompurify` or use React defaults |
| **Access Control**   | Can a User access `/admin` or another user's data (IDOR)?              | Implement middleware checking `req.user.id`     |
| **Data Protection**  | Is PII encrypted at rest?                                             | Use field-level encryption for emails/phones    |
| **Configuration**    | Is Rate Limiting enabled on auth endpoints?                           | Add `express-rate-limit` to `/login` and `/join` |
| **Configuration**    | Are security headers (CSP, HSTS) missing?                             | Implement `helmet.js` in Express               |
| **Audit**            | Do dependencies have known vulnerabilities?                           | Run `npm audit fix` or `pnpm audit`            |

### 2. IDOR Prevention Pattern
Identify where a user can change an ID in an API call to access someone else's data.

**Wrong (Vulnerable):**
```javascript
// PUT /api/posts/:id
const post = await db.post.update({
  where: { id: req.params.id },
  data: { content: req.body.content }
});
```

**Right (Secure):**
```javascript
// PUT /api/posts/:id
const post = await db.post.update({
  where: { 
    id: req.params.id,
    userId: req.user.id // Always scope by current authenticated user
  },
  data: { content: req.body.content }
});
```

### 3. Secret Isolation Workflow
1. Run `grep -r "sk_\|key_\|secret_\|passwd" .` to find leaked secrets.
2. Replace with `process.env[VARIABLE_NAME]`.
3. Add variable to `.env.example`.
4. Rotate any keys that were previously committed to Git.
5. Use `git-filter-repo` to scrub history if secrets were pushed.

---

## Part 3: AI-Scaffolding Prompts

### The "All-in-One" Scaffold Prompt
Use this to generate the entire documentation suite for a new project.

```
Act as a Senior Lead Developer. I have a new app idea: [APP IDEA].

I need you to scaffold the 7 canonical project documents to form a complete AI-readable knowledge base. Use the following structured templates:

1. README.md: Getting started guide and project overview.
2. PRD.md: Product requirements and success metrics.
3. APP_FLOW.md: Navigation map and screen inventory.
4. TECH_STACK.md: Exact versions and technical rationale.
5. FRONTEND_GUIDELINES.md: Design tokens and component style guide.
6. BACKEND_STRUCTURE.md: DB schema and API contracts.
7. IMPLEMENTATION_PLAN.md: Step-by-step build sequence.

CRITICAL REQUIREMENTS:
- Do not use placeholders. Propose real technical choices.
- Ensure all 7 documents are consistent with each other.
- Follow the exact structures defined in the AI-First Documentation Guide.
- Include security best practices (bcrypt, HTTP-only, CSP) in the architecture.
- Focus on production-grade standards, not MVPs.

Output each document in a separate code block.
```

## Part 4: Auto-Remediation Workflow

### Task: Security Audit & Fix
1. **Analyze**: Use `grep` and file inspection to find security flaws from Part 2.
2. **Report**: List all findings with severity (High/Medium/Low).
3. **Fix**: Implement remediations one file at a time.
4. **Verify**: Run tests to ensure auth and access control still function.
