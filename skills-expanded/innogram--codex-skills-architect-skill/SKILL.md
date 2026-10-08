---
name: architect
description: System architecture decisions for NestJS projects. Use when designing new features, choosing patterns, evaluating scalability/security, or making technology choices. Triggers on "design", "architect", "should I use", "which pattern", "scalability", "security design".
phase: planning
flow-next: api-designer
flow-alternatives: [writing-plans, coder]
related: [brainstorming, api-designer]
---

# Architect

## Overview

Make system architecture decisions for NestJS projects following Layered Architecture principles (Controller/Service/Repository).

## Generated File Naming Convention (MANDATORY)

**ANY file created by this skill MUST be prefixed with `architect-`.**
Predefined output (`architect-architecture.md`) already follows this convention.
Any additional ad-hoc files (summaries, notes, diagrams) MUST also follow this rule:
- ✅ `architect-decision-log.md`
- ❌ `DECISION_LOG.md`

## Decision Trees

### Where to Place New Code?

```
New functionality needed
        │
        ├── Business domain specific?
        │   └── YES → modules/<module>/
        │
        ├── Cross-cutting infrastructure?
        │   └── YES → shared/
        │
        └── External service integration?
            └── YES → shared/integrations/ or module-specific
```

### Which Pattern to Use?

```
Operation type?
        │
        ├── HTTP Request handling?
        │   └── Controller
        │
        ├── Business logic?
        │   └── Service
        │
        ├── Data access?
        │   └── Repository
        │
        └── Utility/helper function?
            └── Static utility or shared service
```

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│ Presentation Layer (Controllers, DTOs)                   │
├─────────────────────────────────────────────────────────┤
│ Service Layer (Business Logic)                           │
├─────────────────────────────────────────────────────────┤
│ Data Access Layer (Repositories, Entities)               │
└─────────────────────────────────────────────────────────┘
```

## Dependency Rules

```
✅ ALLOWED:
Controller → Service → Repository
Any layer → shared utilities

❌ NOT ALLOWED:
Repository → Service
Service → Controller
```

## Module Structure

```
modules/<module>/
├── <module>.module.ts
├── <module>.controller.ts
├── <module>.service.ts
├── <module>.repository.ts    # Only if database is used
├── dto/
│   ├── create-<module>.dto.ts
│   └── update-<module>.dto.ts
└── entities/                  # Only if database is used
    └── <module>.entity.ts
```

## Key Decisions

### Entity Relationships

| Relationship | Implementation | When |
|--------------|---------------|------|
| One-to-One | `@OneToOne` + FK | Rarely, usually merge entities |
| One-to-Many | `@OneToMany` + `@ManyToOne` | Common parent-child |
| Many-to-Many | `@ManyToMany` + junction table | Tags, categories |

### Transaction Boundaries

| Scenario | Transaction? | How |
|----------|-------------|-----|
| Single write | No (implicit) | Direct repository call |
| Multiple related writes | Yes | Service method with @Transaction |
| Read operation | No | Repository call |

### Security Considerations

- [ ] Authentication required?
- [ ] Authorization rules?
- [ ] Input validation?
- [ ] Rate limiting?
- [ ] Audit logging?
- [ ] Data encryption?

### Scalability Considerations

- [ ] Database indexing strategy?
- [ ] Caching opportunities?
- [ ] Async processing needed?
- [ ] Horizontal scaling requirements?

## Quick Reference

| Decision | Answer |
|----------|--------|
| New business entity | Entity + Repository + Service + Controller |
| External API integration | Shared integration service |
| Shared utilities | shared/ directory |
| Feature flag | Configuration service |
| Background job | Queue + worker pattern |
| Real-time updates | WebSockets or SSE |

---

## Final Output (MANDATORY)

**Before presenting next steps, you MUST update the living specification:**

### Living Specification Update Process

1. **Read project context:**
   - Read `specs/MANIFEST.md` to understand the project overview
   - This is the entry point for all specifications

2. **Read existing architecture:**
   - If `specs/architect-architecture.md` exists, read it to understand existing architecture
   - If it doesn't exist, you'll create it using the structure from `../../../spec-desc.md`

3. **Get task number:**
   - If coming from previous skills, use the task number from context (e.g., "TASK-001")
   - Task number should be included in all section headers

4. **Update architect-architecture.md:**
   - **If file doesn't exist:** Create using the structure template from spec-desc.md
   - **If file exists:** Append new sections with `### [TASK-N] Feature Name` prefix
   - Include date in section: `### [TASK-001] User Authentication (2026-01-22)`
   - Document:
     - Module placement decisions
     - Pattern choices with rationale
     - Entity relationships
     - Security considerations
     - Scalability considerations
     - Key architectural decisions

5. **Update MANIFEST.md if needed:**
   - Update "Last Updated" date for architect-architecture.md entry
   - Add new modules to "Key Decisions" section if applicable
   - Update "Tech Stack" if new technologies are introduced

**Example section in architect-architecture.md:**
```markdown
### [TASK-001] User Authentication (2026-01-22)

**Module:** `modules/auth/`

**Pattern:** Layered Architecture with JWT tokens

**Entities:**
- User (id, email, passwordHash, createdAt)

**Security:**
- bcrypt for password hashing
- JWT with 15min expiry
- Refresh token rotation

**Scalability:**
- Stateless authentication
- Redis for token blacklist
```

This incremental update ensures living documentation that grows with the project.

---

## Next Steps

After updating specs/architect-architecture.md and specs/MANIFEST.md, STOP and present these options:

**Next by flow:** [[/api-designer]] `[TASK-{N} context]` - Design REST APIs based on the architecture. See [[moc-planning]] for phase context.

**Pass to next skill:** Include the task number in your context summary (e.g., "TASK-001: Authentication architecture documented")

**Alternatives:**
- [[/writing-plans]] `[TASK-{N} context]` - Create implementation plan if APIs are already defined.
- [[/coder]] `[TASK-{N} context]` - Start implementation if architecture is simple and clear.
