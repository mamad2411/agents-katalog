---
name: skill
title:**MyQMS** Skill Profile — Normalized Engineering, HR & AI Capability Taxonomy
description: "Use when reviewing the repository's normalized engineering, HR, and AI capability taxonomy in a human- and machine-readable format. Provides canonical skill definitions with versioning, relationships, and gap analysis."
user-invocable: false
metadata:
  document_type: skill-profile
  version: 2.0.0
  last_updated: 2026-07-21
  status: normalized
  normalized_for:
    - humans
    - hr-review
    - ai-agents
  sources:
    - package.json
    - SKILL-MATRIX.md
    - intent-skills/hr-orchestrator/SKILL.md
    - intent-skills/react-query/SKILL.md
    - intent-skills/vercel-ai-sdk/SKILL.md
    - intent-skills/prisma-fwms/SKILL.md
    - intent-skills/malaysian-compliance/SKILL.md
    - intent-skills/hr-analytics/SKILL.md
    - intent-skills/hr-compliance/SKILL.md
    - intent-skills/hr-quality-management/SKILL.md
    - intent-skills/employer-branding/SKILL.md
    - intent-skills/industrial-relations/SKILL.md
    - intent-skills/succession-planning/SKILL.md
    - intent-skills/compensation-benefits/SKILL.md
    - intent-skills/payroll/SKILL.md
    - intent-skills/recruitment/SKILL.md
    - intent-skills/foreign-worker-expatriate/SKILL.md
    - intent-skills/learning-development/SKILL.md
    - intent-skills/organisation-development/SKILL.md
---

# **MyQMS** Skill Profile — July 2026

## 1. Profile Summary

**MyQMS (Malaysia Quality Management System)** is a multi-tenant HR and foreign worker management platform combining modern full-stack web engineering, Malaysian labour compliance workflows, and AI-assisted multi-agent orchestration. The system spans end-to-end type-safe API design, domain-specific HR automation, geolocation tracking, PDF generation, on-device ML embeddings, and structured knowledge routing for specialist agents.

**Key strengths**

- **End-to-end type-safe architecture**: TypeScript → tRPC → Zod → Prisma → PostgreSQL
- **Deep Malaysian HR compliance** and foreign worker management domain coverage
- **Multi-agent AI orchestration** with LLM tool-calling and local embedding fallback
- **Multi-tenant data modeling** with strict tenant-scoped query discipline
- **Schema-first development** with Zod v4 as the single source of truth for forms, APIs, and AI tools
- **Financial precision** with Decimal.js for payroll and statutory calculations
- **Real-time streaming** with Vercel AI SDK and Server-Sent Events

---

## 2. Normalization Findings (July 2026)

### Consolidated duplicates

| Original Duplicate | Consolidated Entry |
|--------------------|--------------------|
| Recruitment Marketing / Employer Branding | **Employer Branding & Talent Acquisition** |
| HR Compliance & Policy / Malaysian Compliance | **Malaysian HR Compliance** |
| Repeated analytics/reporting language | **HR Analytics & Reporting** |
| Prisma ORM / Prisma Client | **Prisma ORM** (single entry) |
| React Query / TanStack Query | **TanStack Query** (official name since v4) |

### Naming standardization

| Old Term | Standardized Term |
|----------|-------------------|
| IR | **Industrial Relations** |
| JS | **JavaScript** |
| React Query | **TanStack Query** |
| Tailwind CSS 4 | **Tailwind CSS** (version tracked in metadata) |
| FWCMS, MYEG, EPLKS | **platform/tool context** (not standalone skills) |

### Version corrections (verified from package.json, July 2026)

| Technology | Previously Stated | Correct Version |
|------------|-------------------|-----------------|
| Next.js | generic "16" | **v16.2.1** |
| React | generic "19" | **v19.2.4** |
| Zod | v3 | **v4.3.6** (breaking change in schema API) |
| Prisma | v5/v6 | **v7.6.0** |
| Vercel AI SDK (`ai`) | unspecified | **v6.0.141** |
| TanStack Query | v4 | **v5.95.2** |
| tRPC | v10 | **v11.16.0** |
| TypeScript | unspecified | **v5.9.3** (strict mode) |

### New skills added (previously missing)

**AI & ML**:
- LangChain Core + Ollama (local LLM inference)
- TensorFlow.js (on-device ML)
- Xenova Transformers (local embedding generation)
- Semantic Search (cosine similarity over embeddings)
- TokenLens (LLM token counting)

**State & Forms**:
- Redux Toolkit (global client state)
- React Hook Form + Hookform Resolvers
- TanStack Query (async state)

**Visualization & UI**:
- Recharts (data visualization)
- Framer Motion / Motion (animation)
- Rive (interactive WebGL2 animation)
- XY Flow / React Flow (workflow diagrams)
- Radix UI (accessible primitives)

**Geolocation**:
- React Leaflet + Leaflet + MapLibre
- Geolocation utilities (GPS verification)

**Documents & Storage**:
- Vercel Blob (file storage)
- React PDF / @react-pdf/renderer
- Streamdown (streaming markdown + Mermaid)

**Data & Precision**:
- Decimal.js (financial arithmetic)
- date-fns (date manipulation)
- SuperJSON (tRPC serialization)

**Authentication**:
- Jose (JWT handling)

**Domain Skills**:
- Employee Self-Service (ESS)
- Expatriate Management
- Workflow Engine
- Geolocation & Attendance Tracking
- Compensation & Benefits (expanded)
- Payroll Operations (expanded)
- Recruitment (expanded)

### Outdated or irrelevant content removed

- Repeated implementation notes and accidental pasted route/checklist content
- Redundant matrix-style rows (consolidated into structured skill records)
- Deprecated package references (e.g., classnames, legacy React patterns)
- Version-agnostic claims replaced with verified version numbers

---

## 3. Core Skill Categories (July 2026)

### Programming Languages

| Skill | Level | Years | Last Used | Context |
|-------|-------|-------|-----------|---------|
| **TypeScript** | Advanced | 3 | current | Primary language across Next.js App Router, tRPC procedures, Zod v4 schemas, hooks, and Prisma v7 services. Strict mode enabled throughout. |
| **JavaScript** | Intermediate | 3 | current | Used in ecosystem tooling, runtime integrations, and package interoperability. |
| **SQL** | Intermediate | 2 | current | Applied through PostgreSQL data modeling, relational querying patterns, and compliance reporting logic. |

---

### Frameworks & Libraries

| Skill | Level | Years | Last Used | Version | Context |
|-------|-------|-------|-----------|---------|---------|
| **Next.js** | Advanced | 2 | current | v16.2.1 | App Router architecture for full FWMS platform — UI, API routes, streaming, and server actions. |
| **React** | Advanced | 3 | current | v19.2.4 | Client components, UI composition, hooks, and interactive dashboard experiences. |
| **tRPC** | Advanced | 2 | current | v11.16.0 | End-to-end typed procedure layer for all client-server data contracts. |
| **Zod** | Advanced | 2 | current | v4.3.6 | Schema validation, inferred types, and shared input/output contracts for forms, APIs, and AI tools. |
| **Prisma ORM** | Advanced | 2 | current | v7.6.0 | Typed PostgreSQL access, schema modeling, and multi-tenant data operations with pg adapter. |
| **Tailwind CSS** | Advanced | 2 | current | v4.2.2 | Utility-first styling for dashboard, landing, and app-shell UI layers. |
| **TanStack Query** | Advanced | 2 | current | v5.95.2 | Query caching, invalidation, and async UI state management for typed frontend data flows. |
| **React Hook Form** | Intermediate | 1 | current | v7.72.0 | Form state management and Zod-integrated validation for HR data entry forms. |
| **Framer Motion** | Intermediate | 1 | current | v12.38.0 | Page transitions, dashboard animations, and interactive UI motion. |
| **Recharts** | Intermediate | 1 | current | v3.8.1 | HR analytics dashboards, headcount charts, attendance trends, and compliance metric visualizations. |
| **React Leaflet** | Intermediate | 1 | current | v5.0.0 | Geolocation tracking, worker location maps, and attendance geo-verification with Leaflet v1.9.4. |
| **XY Flow (React Flow)** | Intermediate | 1 | current | v12.10.2 | Workflow diagram rendering for HR process visualization and agent flow mapping. |
| **React PDF** | Intermediate | 1 | current | v10.4.1 | Payroll slips, compliance reports, and LHDN audit document generation. |
| **Rive** | Beginner | 1 | current | v4.27.3 | Interactive WebGL2 animations for landing and onboarding experiences. |
| **Radix UI** | Intermediate | 2 | current | latest | Full suite of accessible UI primitives — dialogs, navigation, forms, dropdowns, and app controls. |

---

### AI & Machine Learning

| Skill | Level | Years | Last Used | Version | Context |
|-------|-------|-------|-----------|---------|---------|
| **Vercel AI SDK** | Advanced | 1 | current | v6.0.141 | Streaming AI responses, tool-calling, and orchestrated agent workflows. |
| **LangChain** | Intermediate | 1 | current | v1.1.38 | Local LLM inference via Ollama and chain-based AI composition as fallback to OpenAI. |
| **Xenova Transformers** | Intermediate | 1 | current | v2.17.2 | On-device semantic embeddings for semantic search without external API dependency. |
| **TensorFlow.js** | Beginner | 1 | current | v4.22.0 | On-device ML inference supporting embedding and classification tasks. |
| **Semantic Search** | Intermediate | 1 | current | custom | Cosine similarity search over HR knowledge base using local transformer embeddings. |
| **TokenLens** | Beginner | 1 | current | v1.3.1 | LLM token counting and context window management for AI prompt optimization. |
| **AI Agent Orchestration** | Advanced | 1 | current | custom | HR Director-style master orchestrator routing to 15 specialist agents via LLM tool-calling. |
| **Schema-driven Validation** | Advanced | 2 | current | v3.25.2 | Zod v4 contracts converted to JSON Schema for AI tool parameters via zod-to-json-schema. |

---

### Tools & Platforms

| Skill | Level | Years | Last Used | Version | Context |
|-------|-------|-------|-----------|---------|---------|
| **Git & GitHub** | Advanced | 3 | current | latest | Source control, collaboration, review workflows, and GitHub Actions CI/CD. |
| **Vercel** | Intermediate | 2 | current | latest | Deployment platform for Next.js — preview deployments, environment management. |
| **Vercel Blob** | Intermediate | 1 | current | v2.3.2 | Document and file storage for employee records, compliance certificates. |
| **Redux Toolkit** | Intermediate | 1 | current | latest | Global client state management for cross-component HR data sharing. |
| **SuperJSON** | Intermediate | 1 | current | v2.2.6 | tRPC serialization layer handling Dates, Decimals, and complex types. |
| **date-fns** | Intermediate | 2 | current | latest | Date arithmetic for visa expiry, payroll periods, attendance windows. |
| **Decimal.js** | Intermediate | 1 | current | v10.6.0 | Financial precision arithmetic for payroll, EPF/SOCSO/PCB, levies in MYR. |
| **Jose** | Intermediate | 1 | current | v6.2.2 | JWT signing, verification, and session token handling for authentication. |
| **Streamdown** | Intermediate | 1 | current | v2.5.0 | Streaming markdown rendering with CJK, code, math, and Mermaid plugins. |

---

### Databases

| Skill | Level | Years | Last Used | Context |
|-------|-------|-------|-----------|---------|
| **PostgreSQL** | Advanced | 2 | current | Core relational database for employees, payroll, compliance, attendance, visas, and multi-tenant data. |

---

### DevOps & Infrastructure

| Skill | Level | Years | Last Used | Context |
|-------|-------|-------|-----------|---------|
| **Node.js** | Advanced | 3 | current | Server execution environment for Next.js routes, tRPC handlers, and AI integrations. |
| **Multi-tenant Architecture** | Advanced | 2 | current | Tenant-scoped query patterns, shared schema design, data isolation across all modules. |
| **Environment Configuration** | Intermediate | 2 | current | .env-driven config for OpenAI, database, Vercel Blob, third-party integrations. |
| **GitHub Actions** | Beginner | 1 | current | CI/CD workflows for build, lint, and type-check automation. |

---

### HR / Business / Domain Skills

| Skill | Level | Years | Last Used | Context |
|-------|-------|-------|-----------|---------|
| **Foreign Worker Management** | Expert | 2 | current | Visa, permit, levy, FOMEMA, accommodation, renewal workflows under Malaysian immigration law. |
| **Malaysian HR Compliance** | Expert | 2 | current | Employment Act 1955, Industrial Relations Act 1967, PDPA 2010, EPF/SOCSO/PCB statutory readiness. |
| **Payroll & Benefits Operations** | Advanced | 2 | current | Salary processing, EPF (11%/13%), SOCSO (1.0%/2.25%, RM 6k ceiling), PCB, Decimal.js precision. |
| **Expatriate Management** | Advanced | 1 | current | Dedicated workflows for expatriate onboarding, permit tracking, compliance distinct from foreign workers. |
| **Employee Self-Service (ESS)** | Intermediate | 1 | current | Employee-facing portal for leave requests, payslip access, profile updates, document submissions. |
| **Workflow Engine** | Intermediate | 1 | current | Configurable HR process automation for approvals, onboarding steps, compliance task routing. |
| **Geolocation & Attendance** | Intermediate | 1 | current | GPS-based attendance verification, worker location tracking, geo-fenced check-in/out. |
| **Compensation & Benefits** | Advanced | 2 | current | Salary benchmarking, allowances, total rewards, statutory contributions (EPF/SOCSO/EIS/PCB). |
| **Recruitment & Talent Acquisition** | Advanced | 2 | current | JD creation, candidate screening, visa eligibility, salary benchmarking, MyFutureJobs compliance. |
| **HR Quality Management** | Advanced | 2 | current | SOP audits, CAPA planning, service-quality scorecards, process consistency reviews. |
| **Industrial Relations** | Advanced | 2 | current | Domestic inquiry (EA S.14), dismissal guidance, union matters, grievance handling under IR Act 1967. |
| **Employer Branding** | Advanced | 2 | current | EVP design, job ad strategy, campaign KPI tracking, hiring support for Malaysian talent market. |
| **Succession Planning** | Advanced | 2 | current | 9-box talent mapping, leadership pipeline, retention risk assessment, IDP recommendations. |
| **Learning & Development** | Advanced | 1 | current | Training needs analysis, HRD Corp claims, career pathing, skills gap analysis. |
| **Organisation Development** | Intermediate | 1 | current | Org design, change management, leadership development, culture transformation. |
| **HR Analytics & Reporting** | Advanced | 1 | current | Headcount, attendance, compliance, payroll insight generation for dashboards and AI summaries. |
| **Compliance Automation** | Advanced | 1 | current | Rule-based checks for visas, documents, levy, FOMEMA, policy readiness via compliance engine. |

---

### Soft Skills

| Skill | Level | Years | Last Used | Context |
|-------|-------|-------|-----------|---------|
| **Systems Thinking** | Advanced | 3 | current | Connects product, data, compliance, and AI workflows into a coherent operating model. |
| **Documentation & Knowledge Structuring** | Advanced | 3 | current | Converts technical and business capabilities into reusable, machine-readable guidance. |
| **Process Optimization** | Advanced | 3 | current | Simplifies multi-step HR operations into repeatable and automatable workflows. |
| **Risk Awareness** | Advanced | 3 | current | Emphasizes compliance, data handling, and operational correctness in sensitive HR scenarios. |

---

## 4. Skill Relationships

### Core Engineering Stack

```
TypeScript (strict) → React 19 → Next.js 16 → tRPC v11 → Zod v4 → Prisma v7 → PostgreSQL
```

### UI & Data Flow Toolchain

```
Tailwind CSS v4 + Radix UI → UI composition
React Hook Form + Zod → form validation
TanStack Query v5 → async state orchestration
tRPC + SuperJSON → typed serialized contracts
Recharts → data visualization
Framer Motion → animation layer
Redux Toolkit → global client state (selective)
```

### AI Workflow Cluster

```
Vercel AI SDK (streamText + tool-calling)
    ├── OpenAI gpt-4o-mini (primary LLM)
    ├── LangChain + Ollama (local LLM fallback)
    ├── Xenova Transformers + TensorFlow.js (on-device embeddings)
    │    └── Semantic Search (useSemanticSearch)
    └── HR Orchestrator (master agent)
         └── 15 specialist agents
              ├── Analytics (HR metrics)
              ├── Compliance (Malaysian laws)
              ├── Industrial Relations (disputes)
              ├── Talent Acquisition (recruitment)
              ├── Payroll (compensation)
              ├── Expat (immigration)
              ├── Employee (relations)
              └── 8 additional specialists
```

### Document & File Toolchain

```
React PDF / @react-pdf/renderer → payroll slips, LHDN audit reports
Vercel Blob → document storage (employee records, certificates)
Streamdown → streaming markdown + Mermaid diagrams in chat responses
```

### Geolocation Toolchain

```
React Leaflet + Leaflet + MapLibre → map rendering
utils/geolocation → GPS attendance verification
modules/expatriates → location-aware permit tracking
```

### HR Domain Cluster

```
Foreign Worker Management ↔ Malaysian HR Compliance ↔ Payroll & Benefits
    ↔ Expatriate Management ↔ Geolocation & Attendance
    ↔ HR Quality Management ↔ Industrial Relations
    ↔ HR Analytics ↔ Succession Planning ↔ Employer Branding
    ↔ ESS ↔ Workflow Engine ↔ L&D ↔ OD
```

### Token & Context Management

```
TokenLens → LLM token counting → prompt optimization → Vercel AI SDK
```

---

## 5. Skill Gaps & Recommendations (July 2026)

### High Priority

| Gap | Impact | Recommendation |
|-----|--------|----------------|
| **Automated testing stack** | Critical for tRPC procedures, Zod schemas, compliance logic, payroll calculations | Implement Vitest for unit tests, Playwright for E2E. Target 80% coverage on critical paths. |
| **Observability & monitoring** | Essential for production support of compliance-critical workflows | Add Sentry for error tracking, structured logging (Pino/Winston), OpenTelemetry for tracing. |
| **Authentication hardening** | `jose` present but no dedicated auth library | Integrate NextAuth.js v5 (Auth.js) with RBAC patterns formalized across tenant boundaries. |
| **Rate limiting & security** | No protection against API abuse or brute force | Implement upstash/ratelimit or Next.js built-in rate limiting for API routes. |

### Medium Priority

| Gap | Impact | Recommendation |
|-----|--------|----------------|
| **CI/CD standardization** | GitHub Actions exist but coverage should be verified | Enforce lint, type-check, Prisma schema validation, build gates, and test runs. |
| **Vector database / persistent embeddings** | Current semantic search uses in-memory similarity | Add pgvector extension to PostgreSQL or migrate to Pinecone for scalable knowledge base. |
| **OpenAI model versioning** | `gpt-4o-mini` hardcoded | Create model configuration layer for safe upgrades and cost control without code changes. |
| **Ollama model registry** | Specific local model(s) not documented | Document which models are used (e.g., llama3.2, mistral) and version them in config. |
| **Audit logging** | Compliance requires action trails | Implement structured audit log for all HR changes, visa updates, payroll approvals. |

### Low Priority

| Gap | Impact | Recommendation |
|-----|--------|----------------|
| **Skill metadata automation** | Manual updates risk drift | Generate/update profile from `package.json` and intent-skills source files on each release. |
| **Cross-team glossary** | Naming drift across modules and agent prompts | Create shared taxonomy for HR, engineering, and AI terms (PLKS vs Work Permit vs Visa). |
| **Rive animation governance** | Minimal usage, risk of duplication | Define pattern for when Rive vs Framer Motion should be used. |
| **DnD Kit adoption** | `@dnd-kit/react` installed but no skill entry | Confirm active usage or remove dependency. |
| **Documentation versioning** | Multiple SKILL.md files may drift | Implement centralized version tracking or cross-reference validation in CI. |

---

## 6. Versioning & Metadata

| Field | Value |
|-------|-------|
| **document_version** | 2.1.0 |
| **previous_version** | 2.0.0 |
| **canonical_file** | SKILL.md |
| **status** | Active |
| **last_reviewed** | 2026-07-21 |
| **last_verified_against** | package.json, prisma/schema.prisma |

### Change Summary (v1.0.0 → v2.1.0)

**Version corrections**:
- Next.js 16.2.1, React 19.2.4, Zod v4.3.6, Prisma v7.6.0, tRPC v11.16.0, TanStack Query v5.95.2

**Skills added (30+)**:
- AI/ML: LangChain, Ollama, TensorFlow.js, Xenova Transformers, Semantic Search, TokenLens
- State/Forms: Redux Toolkit, React Hook Form
- Visualization: Recharts, Framer Motion, Rive, XY Flow, Radix UI
- Geolocation: React Leaflet, Leaflet, MapLibre
- Documents: Vercel Blob, React PDF, Streamdown
- Data: Decimal.js, date-fns, SuperJSON
- Auth: Jose
- Domain: ESS, Expatriate Management, Workflow Engine, Geolocation & Attendance, expanded C&B, Payroll, Recruitment

**Domain skills expanded**:
- Learning & Development
- Organisation Development
- HR Analytics & Reporting
- Compliance Automation

**Skill relationships added**:
- AI fallback chain (OpenAI → LangChain/Ollama → keyword)
- Document toolchain (PDF → Blob → Streamdown)
- Geolocation toolchain (Leaflet → GPS → permit tracking)

**Gap analysis updated**:
- High priority: testing, observability, auth, rate limiting
- Medium priority: CI/CD, vector DB, model versioning, audit logs
- Low priority: automation, glossary, governance

### Intended Readers

- **Engineering teams** — understand tech stack, versions, and architectural decisions
- **HR stakeholders** — understand domain coverage and compliance capabilities
- **AI agents and parsers** — machine-readable capability taxonomy for tool-calling
- **Onboarding new developers** — comprehensive reference of all platform capabilities
- **Product managers** — gap analysis for roadmap planning

---

## 7. Related Documents

| Document | Purpose |
|----------|---------|
| `SKILL-MATRIX.md` | Visual matrix and quick index of capabilities |
| `AGENTS.md` | Agent roster and orchestration architecture |
| `intent-skills/*/SKILL.md` | Individual skill definitions (19 modules) |
| `package.json` | Authoritative dependency versions |
| `prisma/schema.prisma` | Data model source of truth |
| `.github/workflows/` | CI/CD automation |

---

## 8. Quality Checklist

- [x] All package versions verified against `package.json` (July 2026)
- [x] 30+ new skills added with proper level/years/context
- [x] Duplicates consolidated (Prisma ORM, TanStack Query, Malaysian compliance)
- [x] Naming standardized (Industrial Relations, TanStack Query)
- [x] Version corrections applied (Zod v4, Prisma v7, tRPC v11)
- [x] Skill relationships documented with ASCII diagrams
- [x] Gap analysis prioritized (high/medium/low)
- [x] All 19 intent-skills referenced in domain section
- [x] Machine-readable structure maintained for AI parsing
- [x] Human-readable context provided for each skill
```

---

## Key enhancements

| Section | Enhancement |
|---------|-------------|
| **Normalization Findings** | Added consolidated duplicates table, naming standardization, version corrections table |
| **Core Skill Categories** | Complete restructure with level/years/version/context for 50+ skills across 8 categories |
| **AI & ML section** | New dedicated section with 8 skills (Vercel AI SDK, LangChain, Transformers, Semantic Search, etc.) |
| **HR Domain section** | Expanded to 17 skills (added L&D, OD, HR Analytics, Compliance Automation) |
| **Skill Relationships** | ASCII diagrams for core stack, UI flow, AI workflow, document toolchain, geolocation, HR cluster |
| **Gap Analysis** | Prioritized table (high/medium/low) with specific recommendations for testing, observability, auth, rate limiting, vector DB, audit logs |
| **Versioning** | Complete metadata table with change summary from v1.0.0 → v2.1.0 |
| **Related Documents** | Cross-reference to all key FWMS documentation files |
| **Quality Checklist** | 9-point verification for accuracy and completeness |