---
name: skills-matrix
title: Skills Matrix & Technical Architecture
description: "Use when understanding the complete technology stack, AI orchestration, HR domain coverage, skill module relationships, or core engineering principles for Malaysian workforce management."
user-invocable: false
metadata:
  domain: technical
  subdomain: architecture
  region: malaysia
  version: "2.0.0"
  outputs:
    - tech stack reference
    - agent capability mapping
    - skill module relationships
    - architectural decision records
---

# MyQMS Skills Matrix & Technical Architecture — April 2026

## Purpose

This skill provides a canonical, normalized inventory of the **MyQMS** platform's technical capabilities, AI orchestration architecture, HR domain coverage, and engineering principles. It serves as the master reference for understanding how 19 intent-skill modules, 15 specialist agents, and modern web technologies integrate to deliver Malaysian workforce management solutions.

## Use when

- Understanding the complete technology stack and dependencies
- Mapping AI agent capabilities to HR domains
- Identifying which skill module to enhance or extend
- Debugging cross-skill integration issues
- Onboarding developers to FWMS architecture
- Validating technology choices for new features
- Understanding multi-tenant data isolation requirements

## Do not use for

- Day-to-day payroll calculations (use payroll skill)
- Recruitment process guidance (use recruitment skill)
- Foreign worker visa processing (use foreign-worker-expatriate)
- LLM prompt engineering details (use vercel-ai-sdk skill)

## Relevant files

- `package.json` — Authoritative dependency versions
- `prisma/schema.prisma` — Data model source of truth
- `lib/orchestrator/` — Master agent routing logic
- `components/ai-elements/` — 45+ AI UI components
- `intent-skills/*/SKILL.md` — Individual skill definitions
- `.github/workflows/` — CI/CD automation

---

## 1. Technology Stack Matrix (April 2026)

### Core Engineering

| Domain | Category | Key Skills | Versions | Status |
|--------|----------|------------|----------|--------|
| **Languages** | Type System | TypeScript, JavaScript, SQL | TS (strict), ES2024, PostgreSQL | ✓ Active |
| **Web Platform** | Framework | Next.js App Router, React, Server Components | v16.2.1, v19.2.4, v18+ RSC | ✓ Active |
| **API & Type Safety** | RPC Layer | tRPC v11, Zod v4 | v11.16.0, v4.3.6 | ✓ Active |
| **Data Access** | ORM & DB | Prisma v7, PostgreSQL PG adapter | v7.6.0, v8.20.0 | ✓ Active |

### Frontend & UI

| Domain | Category | Key Skills | Versions | Status |
|--------|----------|------------|----------|--------|
| **Styling** | CSS Framework | Tailwind CSS v4 | v4.2.2 | ✓ Active |
| **UI Components** | Component Library | Radix UI (8 components), Lucide Icons | latest | ✓ Active |
| **Forms** | Form Management | React Hook Form, Hook Resolvers, Zod | v7.72.0, v5.2.2 | ✓ Active |
| **State Management** | Server State | TanStack Query v5 | v5.95.2 | ✓ Active |
| **Global State** | Client State | Redux Toolkit | latest | ✓ Active |
| **Animation** | Motion | Framer Motion, Motion library, Rive (WebGL2) | v12.38.0, v4.27.3 | ✓ Active |
| **Workflows** | Diagrams | XY Flow (React Flow v12) | v12.10.2 | ✓ Active |
| **Maps** | Geolocation | React Leaflet, Leaflet, MapLibre | v5.0.0, v1.9.4, v3+ | ✓ Active |

### Data & Documents

| Domain | Category | Key Skills | Versions | Status |
|--------|----------|------------|----------|--------|
| **Serialization** | Data Layer | SuperJSON, Decimal.js, date-fns | v2.2.6, v10.6.0, latest | ✓ Active |
| **Charts** | Visualization | Recharts, Mermaid (via Streamdown) | v3.8.1, v10+ | ✓ Active |
| **PDF Generation** | Documents | React PDF, @react-pdf/renderer | v10.4.1, v4.3.2 | ✓ Active |
| **File Storage** | Cloud | Vercel Blob | v2.3.2 | ✓ Active |
| **Markdown** | Streaming | Streamdown (CJK, Code, Math, Mermaid) | v2.5.0 | ✓ Active |

### AI & LLM Stack

| Domain | Category | Key Skills | Versions | Status |
|--------|----------|------------|----------|--------|
| **AI SDK** | LLM Integration | Vercel AI SDK (ai + React + RSC) | v6.0.141, v3.0.143, v2.0.141 | ✓ Active |
| **Models** | Providers | OpenAI gpt-4o-mini, LangChain + Ollama | current | ✓ Active |
| **Embeddings** | On-Device ML | Xenova Transformers, TensorFlow.js | v2.17.2, v4.22.0 | ✓ Active |
| **Token Management** | Context | TokenLens | v1.3.1 | ✓ Active |
| **AI UI Components** | Chat Interface | 45+ ai-elements (Conversation, Message, PromptInput, Reasoning, etc.) | April 2026 | ✓ Active |

### DevOps & Security

| Domain | Category | Key Skills | Versions | Status |
|--------|----------|------------|----------|--------|
| **Authentication** | Auth | Jose, Environment-based Config | v6.2.2 | ✓ Active |
| **CLI/Search** | Command | cmdk | v1.1.1 | ✓ Active |
| **Platform** | Deployment | Node.js, Vercel, GitHub Actions | Node 20+, latest | ✓ Active |
| **CI/CD** | Automation | GitHub Actions workflows | latest | ✓ Active |

---

## 2. AI & Orchestration Stack (April 2026)

### Master Orchestrator Architecture

```
User Query → /api/hr-orchestrator → HR Director LLM → Tool Calling → Specialist Agent → Response
```

| Component | Location | Capability |
|-----------|----------|------------|
| **Orchestrator** | `lib/orchestrator/` | Routes to 15 specialist agents via tool-calling |
| **API Endpoint** | `/api/hr-orchestrator` | Streams responses, handles maxSteps, fallback logic |
| **Persona Injection** | Tool descriptions | Each agent gets persona-specific context |
| **Fallback Routing** | Keyword matching | When LLM unavailable, keyword-based routing activates |

### AI UI Components Library (45+ Components)

**Core Conversation Components**:
- `Conversation` + `ConversationContent` — Sticky-to-bottom message list with auto-scroll
- `Message` + `MessageContent` — Individual message rendering with role detection (user/assistant/system)
- `ConversationEmptyState` — Welcoming empty state with themed icon support
- `Agent` + `AgentHeader` — Agent container with model badges and status
- `PromptInput` — Advanced form input with file attachments and submit handling
- `Reasoning` — Streaming thought/reasoning display for chain-of-thought

**Specialized Components**:
- `artifact` — Code/output artifacts from agent execution
- `code-block` — Syntax-highlighted code with copy button
- `task` — Task representation with status tracking
- `tool` — Tool invocation display with parameters
- `plan` — Multi-step plan visualization
- `checkpoint` — Save/restore conversation state
- `connection` — Integration connection UI
- `workflow-node` — Node-based workflow editor
- Plus 30+ supporting components (buttons, cards, dialogs, etc.)

### Enhanced Specialist Agents (April 2026)

| Agent | Domain | Key Capabilities | UI Enhancement |
|-------|--------|------------------|----------------|
| **Compliance** | Malaysian Laws | FOMEMA, levies, permits, EPF/SOCSO/EIS | Agent + Conversation elements, real-time validation |
| **Recruitment** | Talent Acquisition | JD creation, visa checks, screening | 5 interactive prompt badges, quick actions |
| **Payroll** | Compensation | Salary calc, EPF/SOCSO/PCB, payslips | Context panel, organized conversation layout |
| **Employee** | HR Relations | Onboarding, performance, training, ER/IR | Themed ConversationEmptyState |
| **Expat** | Immigration | Visa/permits, relocation, compliance | Reasoning component for step-by-step processing |
| **Analytics** | HR Metrics | Headcount, turnover, compliance reporting | Chart visualization with Recharts |
| **Industrial Relations** | Disputes | Domestic inquiry, dismissal, grievances | Workflow-node for process tracking |
| **Learning & Development** | Training | HRD Corp, career pathing, skills gap | Task component for training plans |

---

## 3. HR Domain Skill Modules (19 Intent-Skills)

Each module provides specialized guidance for a specific HR function, loadable on demand by the orchestrator.

| Module | Path | Primary Purpose | Applies To |
|--------|------|----------------|-------------|
| **Compensation & Benefits** | `intent-skills/compensation-benefits/` | Salary planning, allowances, total rewards | Payroll Agent, Analytics |
| **Employee Relations** | `intent-skills/employee-relations/` | Engagement, feedback, informal grievances | Employee Agent, ER/IR |
| **Employer Branding** | `intent-skills/employer-branding/` | EVP, recruitment marketing, culture | Recruitment Agent |
| **Foreign Worker / Expatriate** | `intent-skills/foreign-worker-expatriate/` | Visas, FOMEMA, levies, relocation | Expat Agent, Compliance |
| **HR Analytics** | `intent-skills/hr-analytics/` | Headcount, turnover, compliance reporting | Analytics Agent |
| **HR Compliance** | `intent-skills/hr-compliance/` | Employment Act, PDPA, statutory readiness | Compliance Agent |
| **HR Orchestrator** | `intent-skills/hr-orchestrator/` | Master routing, tool-calling patterns | Central dispatcher |
| **HR Quality Management** | `intent-skills/hr-quality-management/` | SOP audits, CAPA, service scorecards | Quality workflows |
| **Industrial Relations** | `intent-skills/industrial-relations/` | Domestic inquiry, dismissal, grievances | Employee Agent, IR |
| **Learning & Development** | `intent-skills/learning-development/` | Training needs, HRD Corp, career pathing | Employee Agent |
| **Malaysian Compliance** | `intent-skills/malaysian-compliance/` | Employment Act 1955, IR Act 1967, PDPA 2010 | All compliance |
| **Organisation Development** | `intent-skills/organisation-development/` | Org design, change management, leadership | Strategic HR |
| **Payroll** | `intent-skills/payroll/` | EPF/SOCSO/PCB, payslips, processing | Payroll Agent |
| **Prisma FWMS** | `intent-skills/prisma-fwms/` | Schema modeling, data access patterns | Backend layers |
| **React Query** | `intent-skills/react-query/` | useQuery, mutations, invalidation | Frontend data |
| **Recruitment** | `intent-skills/recruitment/` | Pipeline management, JDs, interviews, offers | Recruitment Agent |
| **Succession Planning** | `intent-skills/succession-planning/` | 9-box, leadership pipeline, retention risk | HR Analytics |
| **Talent Acquisition** | `intent-skills/talent-acquisition/` | Sourcing, screening, offer negotiation | Recruitment Agent |
| **Vercel AI SDK** | `intent-skills/vercel-ai-sdk/` | streamText, tool-calling, useChat patterns | Orchestrator, AI |

### Skill Module Relationships

```
HR Orchestrator (Central Router)
    ├── Core HR Operations
    │   ├── Payroll ←→ Compensation & Benefits
    │   ├── Recruitment ←→ Talent Acquisition ←→ Employer Branding
    │   └── Employee Relations ←→ Industrial Relations
    ├── Compliance & Legal
    │   ├── Malaysian Compliance ←→ HR Compliance
    │   └── Foreign Worker / Expatriate
    ├── Strategic HR
    │   ├── HR Analytics ←→ Succession Planning
    │   ├── Learning & Development ←→ Organisation Development
    │   └── HR Quality Management
    └── Technical Foundation
        ├── Prisma FWMS (data layer)
        ├── React Query (frontend state)
        └── Vercel AI SDK (LLM integration)
```

---

## 4. HR Domain Coverage Map

### Foreign Worker & Expatriate Management
- **Scope**: Visa strategies, permit tracking, FOMEMA/EPLKS integration, relocation assistance, levy management
- **Modules**: Foreign Worker/Expatriate, Malaysian Compliance, Compensation & Benefits
- **Agents**: Expat Agent, Compliance Agent
- **2026 Updates**: Services quota tightened to 4:1, MyFutureJobs threshold RM 5,000

### Malaysian HR Compliance
- **Scope**: Employment Act 1955, Industrial Relations Act 1967, PDPA 2010, statutory checklists
- **Modules**: HR Compliance, Malaysian Compliance, Industrial Relations
- **Agents**: Compliance Agent, Employee Agent
- **2026 Updates**: PDPA fines increased to RM 1 million, salary range disclosure mandatory

### Payroll & Benefits Operations
- **Scope**: Salary processing, EPF (employee 11%, employer 13%), SOCSO (1.0%/2.25%, ceiling RM 6,000), PCB, Decimal precision
- **Modules**: Payroll, Compensation & Benefits
- **Agents**: Payroll Agent, Analytics
- **2026 Updates**: EPF cap RM 605, SOCSO/EIS ceiling RM 6,000

### Recruitment & Talent Acquisition
- **Scope**: JD creation, candidate screening, visa eligibility, salary benchmarking, MyFutureJobs compliance
- **Modules**: Recruitment, Talent Acquisition, Employer Branding, Learning & Development
- **Agents**: Recruitment Agent, Employee Agent
- **2026 Updates**: Services quota 4:1, MyFutureJobs threshold RM 5,000

### Employee Relations & Industrial Relations
- **Scope**: Onboarding, performance management, training, domestic inquiries, grievance handling, dismissal procedures
- **Modules**: Employee Relations, Industrial Relations, Learning & Development
- **Agents**: Employee Agent, ER/IR workflows

### HR Quality & Continuous Improvement
- **Scope**: SOP audits, service quality scorecards, CAPA (Corrective & Preventive Action), process consistency
- **Modules**: HR Quality Management
- **Agents**: Quality management workflows

### Geolocation & Attendance Tracking
- **Scope**: GPS-based check-in/check-out, worker location tracking, geo-fenced verification
- **Modules**: Foreign Worker/Expatriate (location context)
- **Components**: React Leaflet + `utils/geolocation`
- **Status**: Integrated with expatriate and attendance workflows

---

## 5. Core Engineering Principles

### Type Safety End-to-End

```
Zod (schema source) → TypeScript inference → tRPC endpoints → React hooks → UI components
```

- Single source of truth for validation across all layers
- Forms, API contracts, and AI tool parameters share same Zod schemas
- `zod-to-json-schema` auto-generates OpenAI tool definitions

### Multi-Tenant Architecture

```typescript
// All database queries MUST be scoped by tenantId
const employees = await prisma.employee.findMany({
  where: { tenantId: currentTenantId }
});
```

- Strict Prisma query discipline enforced across all data layers
- Compliance-critical: foreign worker and expatriate records isolated per tenant
- No cross-tenant data leakage permitted

### Schema-Driven Validation

- **Zod v4** as canonical validator for:
  - Form validation (React Hook Form + zod resolver)
  - API request/response validation (tRPC + Zod)
  - AI tool input/output validation
- Auto-generates JSON Schema for OpenAI tool definitions
- Enables runtime type checking and parsing

### Streaming & Real-Time Architecture

- **Next.js App Router** server components for progressive rendering
- **Vercel AI SDK** `streamText` for real-time LLM response streaming
- **TanStack Query** for optimistic UI updates and cache management
- **Server-Sent Events (SSE)** for long-running processes

### Fallback & Robustness Strategy

| Layer | Primary | Fallback 1 | Fallback 2 |
|-------|---------|------------|------------|
| **LLM** | OpenAI gpt-4o-mini | LangChain + Ollama (local) | Keyword-based routing |
| **Embeddings** | Xenova Transformers (on-device) | API-based embeddings | N/A |
| **Agent Routing** | LLM tool-calling | Keyword matching | Default agent |
| **Database** | PostgreSQL (primary) | Read replica | Connection pool retry |

### Decimal Precision Requirement

**CRITICAL**: All monetary values MUST use `Decimal` type from Prisma:

```typescript
// ✅ Correct
const salary = new Decimal(3500.50);
const total = new Decimal(epf).plus(new Decimal(socso));

// ❌ Never use number/float for money
const salary: number = 3500.50; // Floating point errors!
```

---

## 6. Canonical References

### Documentation Files

| File | Purpose | Version |
|------|---------|---------|
| `SKILL.md` | Comprehensive, normalized skill profile | v2.0.0 |
| `AGENTS.md` | Agent roster and orchestration architecture | v2.0.0 |
| `SKILL-MATRIX.md` | Visual matrix and quick index (this file) | v2.0.0 |
| `README.md` | Project overview and setup instructions | latest |

### Intent-Skills Directory

All skills located in `intent-skills/*/SKILL.md`:
- Task-specific, loadable skill documents
- Referenced by agent system via tool descriptions
- Invoked on intent-match by HR Director orchestrator

### Key External Resources

| Resource | Location | Use |
|----------|----------|-----|
| Package dependencies | `package.json` | Authoritative version source |
| Environment config | `.env.local` / `.env` | Runtime secrets (OpenAI, DB) |
| Data model | `prisma/schema.prisma` | Database schema source of truth |
| CI/CD | `.github/workflows/` | GitHub Actions automation |
| Component library | `components/ai-elements/` | 45+ AI UI components |

---

## 7. April 2026 Updates Summary

| Area | Update |
|------|--------|
| **AI UI Components** | Added 45+ ai-elements (Conversation, Message, Reasoning, PromptInput, etc.) |
| **Agent Enhancements** | All 5 primary agents now use new UI components |
| **Orchestrator** | Improved fallback routing, persona injection |
| **Technology Versions** | Updated all dependencies to April 2026 stable releases |
| **Skill Modules** | 19 intent-skills fully documented with relationships |
| **HR Domain Coverage** | Added geolocation & attendance tracking section |
| **Compliance Updates** | Reflected March 2026 statutory changes across all modules |

---

## Quality Checklist

- [ ] Technology stack versions match `package.json`
- [ ] All 19 intent-skill modules documented
- [ ] Agent capabilities mapped to HR domains
- [ ] Multi-tenant isolation principle stated
- [ ] Decimal precision requirement emphasized
- [ ] Fallback strategy documented
- [ ] April 2026 updates highlighted
- [ ] Cross-references to other skills accurate
- [ ] Compliance with Malaysian regulations noted
```

---

## Key enhancements

| Section | Enhancement |
|---------|-------------|
| **Technology Stack** | Added AI UI Components row (45+ components), updated all versions to April 2026 |
| **AI Orchestration** | New detailed section with orchestrator architecture, 45+ component library, enhanced agents table |
| **Skill Modules** | Complete 19-module table with relationships diagram, 2026 updates for each domain |
| **HR Coverage Map** | Added 2026 statutory updates to each domain (Services quota 4:1, PDPA fines, etc.) |
| **Engineering Principles** | Enhanced fallback strategy table, Decimal precision requirement |
| **April 2026 Updates** | New summary table of all recent enhancements |
| **Quality Checklist** | Added compliance and cross-reference checks |