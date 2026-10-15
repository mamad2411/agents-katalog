---
name: spec-writing-rules
description: Enforces clear, unambiguous, testable, FULL-STACK specification writing rules for Phase II web applications (Frontend + Backend + Auth + Database). Apply before any code is written.
allowed-tools: Read, Write
---

# Full-Stack Specification Writing Rules (Phase II)

## Purpose
This skill enforces a **strict spec-before-code discipline** for full-stack web applications.  
No frontend, backend, database, or authentication code may be written until a **complete, approved specification** exists.

This specification acts as a **binding contract** between:
- Frontend (Next.js)
- Backend (FastAPI)
- Authentication (JWT / Better Auth)
- Database (SQLModel + PostgreSQL)

---

## Core Principles

### 1. Specification-First Mandate
- **NEVER write frontend or backend code before the specification is approved**
- All APIs, UI flows, auth behavior, and data models must be defined first
- Specs must support **multi-user, authenticated systems**
- The specification is the single source of truth

---

## Mandatory Specification Structure (Phase II)

Every Phase-2 spec **MUST contain all sections below**.

---

### A. Overview
- **Purpose**: What problem does this system solve?
- **Scope**: What is included and explicitly excluded?
- **Target Users**: Authenticated users, roles (if any)
- **System Architecture**:
  - Frontend (Next.js App Router)
  - Backend (FastAPI)
  - Auth (JWT via Better Auth)
  - Database (Neon PostgreSQL)

---

### B. Functional Requirements

#### 1. Frontend Requirements
- Pages and routes (e.g. `/login`, `/tasks`)
- UI states (loading, empty, error)
- Auth flows (signup, signin, logout)
- API interaction behavior
- Client-side validation rules

#### 2. Backend / API Requirements
For **every endpoint**, define:
- HTTP method + path
- Required headers (Authorization: Bearer JWT)
- Request body schema
- Response schema
- Success status codes
- Error status codes (401, 403, 404, 422, 500)

#### 3. Authentication Requirements
- JWT issuance behavior
- Token expiry rules
- Unauthorized request handling
- User isolation rules (data ownership enforcement)

#### 4. Data Requirements
- Entities and fields
- Field types and constraints
- Ownership rules (user_id)
- Indexing expectations

---

### C. Non-Functional Requirements
- Security (JWT validation, user isolation)
- Performance expectations
- API consistency rules
- Error message clarity
- Environment variable usage (no hardcoded secrets)

---

### D. Constraints

#### Technical Constraints
- Next.js App Router only
- FastAPI + SQLModel only
- PostgreSQL via Neon
- JWT authentication mandatory

#### Architectural Constraints
- Frontend NEVER directly accesses DB
- Backend NEVER trusts user_id from URL without JWT validation
- Stateless backend auth

---

### E. Acceptance Criteria (CRITICAL)

Every feature must include:
- ✅ Happy-path scenario
- ❌ Unauthorized access scenario
- ❌ Cross-user access attempt
- ❌ Invalid payload scenario
- Edge cases (empty data, duplicates, limits)

Acceptance criteria must be **directly testable** by:
- API tests
- Manual UI testing
- Agent-based test-runner

---

## Specification Lifecycle

### Phase 1: Discovery
- Identify frontend + backend + auth needs
- Resolve ambiguity before writing spec

### Phase 2: Drafting
- Write all mandatory sections
- Define contracts clearly between layers

### Phase 3: Review
- User approval required
- No “TBD” allowed

### Phase 4: Lock
- Mark spec as APPROVED
- Only then code generation may begin

---

## Anti-Patterns (STRICTLY FORBIDDEN)

❌ Writing UI without API spec  
❌ Writing API without auth rules  
❌ Assuming frontend behavior  
❌ Mixing implementation code in specs  
❌ Skipping error cases  
❌ Using vague language (“should”, “maybe”)

---

## Quality Gate Checklist

Before approval, verify:
- [ ] Frontend + Backend + Auth covered
- [ ] Every API secured
- [ ] User data isolation defined
- [ ] JWT behavior specified
- [ ] Acceptance criteria are testable
- [ ] User explicitly approved spec

---

## Usage

Invoke this skill when:
1. Starting any Phase-2 feature
2. Writing API, auth, or UI specifications
3. Before generating backend or frontend code
4. Preparing specs for agentic implementation

---

## Success Criteria

A specification is complete when:
1. Backend and frontend can be built independently
2. No clarification is needed during coding
3. Auth and security behavior is explicit
4. Test-runner can validate it objectively
5. User has approved it
