---
name: azure-focused-net-developer
description: >
  Specialized job search and career skill for an Azure-focused .NET developer
  actively seeking work. Use whenever applying for, researching, or preparing
  for roles involving ASP.NET Core, C#, Azure, or cloud-native .NET development.
  Trigger for job postings mentioning .NET, C#, ASP.NET Core, Azure Functions,
  EF Core, REST APIs, microservices, or Azure cloud services. Also trigger for
  AZ-204 certification prep, .NET interview questions, Azure architecture
  interviews, or positioning skills for cloud developer roles.
---

# Azure-Focused .NET Developer — Job Search Skill

> **ATS keywords + skill summary**: `skills-summary.md` — load for resume/cover letters.
> **Cert status + differentiators**: `profile-facts.md` — load before any positioning or gap work.
> **Portfolio projects**: `github-repos.md` — load when a JD asks for hands-on project evidence.
> **Interview prep**: `interview-prep.md` — load when preparing for a specific interview stage.

---

## Core Stack (quick reference)

| Layer | Technologies |
|---|---|
| Cloud | Azure · Functions · Serverless · App Services · Azure Monitor · Entra ID |
| Backend | ASP.NET Core · C# · .NET · EF Core · REST APIs · Microservices · DDD |
| Frontend | Angular · React · Bootstrap |
| DevOps | Docker · Kubernetes · GitHub Actions · CI/CD · Azure DevOps |
| AI | GitHub Copilot (enterprise, agents, CI/CD, security) · Prompt Engineering |
| Scripting | Python · PowerShell |

---

## Workflow 1 — Job Posting Analysis

Parse exact versions/services → match against stack above → flag gaps using
known genuine gaps from `profile-facts.md` → check `github-repos.md` for
portfolio evidence that elevates course-level skills → identify differentiators
→ rate fit: **Strong / Good / Stretch** + one-line rationale.

For full structured output → use the **gap-analysis-job-description** skill.

---

## Workflow 2 — Resume Tailoring

Extract ATS keywords → map to experience + course credentials + portfolio projects
→ edits by section:

- **Summary**: lead with Azure + .NET; include cert status from `profile-facts.md`
- **Skills**: list Azure services explicitly, not just "cloud"
- **Experience**: measurable impact; inject missing keywords naturally
- **Certs**: learning platform path completions as evidence
- **Portfolio**: reference GitHub projects as applied evidence where relevant

For DOCX output → use the **create-a-cover-letter-and-tailored-resume** skill.

---

## Workflow 3 — Cover Letter

→ Use the **create-a-cover-letter-and-tailored-resume** skill.

---

## Workflow 4 — Interview Preparation

Load `interview-prep.md` → tailor to specific role and stage.

Key areas for .NET / Azure roles:
- ASP.NET Core middleware pipeline and DI patterns
- EF Core: migrations, N+1, AsNoTracking
- Azure Functions: trigger types, bindings, Durable Functions
- App Service vs Functions vs Container Apps trade-offs
- Azure AD / Entra ID: managed identities, RBAC, app registrations
- Resilience: retry policies, circuit breakers, health checks
- System design: file processing pipeline, multi-tenant SaaS API, notification system

---

## Workflow 5 — Certification Prep

Map domain coverage using the AZ-204 Domain Coverage table in `skills-summary.md`
→ identify gaps → suggest courses or MS Learn modules → generate practice scenario
questions for weak areas.

**AZ-204 domains:**
- Compute (Functions, App Service, containers) — 25–30%
- Storage (Blob, Cosmos DB, caching) — 15–20%
- Security (Key Vault, managed identities, AD) — 15–20%
- Monitor + optimize — 10–15%
- Connect + consume (Service Bus, Event Grid, APIM) — 20–25%

Check `profile-facts.md` for exam deadlines and current cert status.

---

## Workflow 6 — Remote / Location Positioning

Remote-first. Flag US-only postings (visa/sponsorship required). Note timezone
compatibility for any time-zone-specific requirements. Job boards: LinkedIn ·
Indeed · Workopolis · Government of Canada Job Bank.

---

## Key Differentiators to Surface per JD

Load `profile-facts.md` for the full list. Common anchors for .NET/Azure roles:

| JD mentions | Surface this |
|---|---|
| Legacy modernization / migration | [N] employers, [N] separate migration projects |
| SQL Server / T-SQL / SSIS | [N]+ years production; quantified performance improvement story |
| TDD / unit testing | xUnit + Moq in production; NUnit at prior employer |
| Azure / cloud | Cert status + [N] Azure courses + [N] hands-on labs |
| GitHub Copilot / AI tooling | [N] courses: enterprise, agents, CI/CD, security |
| Full-stack | ASP.NET Core + Angular in production, same codebase, same employer |

---

## ATS Keywords by Role Type

### Senior .NET / Full-Stack
`C# · ASP.NET Core · .NET Core · Entity Framework Core · REST API · Angular ·
TypeScript · RxJS · SQL Server · T-SQL · Azure DevOps · GitLab · Docker ·
GitHub Actions · xUnit · TDD · Agile · Scrum · CI/CD`

### Azure / Cloud Developer
`Azure Functions · Azure App Service · Azure Monitor · Azure AD · Entra ID ·
Managed Identities · Serverless · AZ-204 · AZ-900 · Service Bus · Cosmos DB ·
Key Vault · Azure Storage · Container Apps · GitHub Actions · Docker`

### SQL / Data Focus
`SQL Server · T-SQL · Stored Procedures · SSIS · SSRS · Query Optimization ·
Indexing · ETL · Data Pipeline · SSAS · Performance Tuning`
