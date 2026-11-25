---
name: scriptorium-templates
description: >-
  Reference guide for filling in all 8 scriptorium project templates: source-map, outline,
  style-guide, glossary, metaphor-registry, chapter-summary, checkpoint, and audit-log.
  Use when: setting up a new book project, filling out any template file, asking what goes in
  a specific template field, creating project configuration for a new technical book topic,
  or understanding the role of each shared resource file.
license: MIT
---

# Tech-Editorial: Template Reference Guide

## Setup Templates (Fill Before Phase 1)

### `source-map.md` — Codebase Map
Maps the target OSS project for Architect (#1) and Researcher (#3).

**Required fields**:
- Project name, version, and repository URL
- Top-level directory tree (2 levels minimum)
- Key entry points (main functions, init hooks, public APIs)
- Per-module descriptions (one sentence each)
- Technology stack (language, frameworks, build system)

**Example module entry**:
```markdown
## Module: packages/core/src/di
**Path**: `packages/core/src/di/`
**Purpose**: Angular's dependency injection container — token registration, provider resolution, injector hierarchy
**Key files**: injector.ts (root interface), r3_injector.ts (runtime impl), provider.ts (provider types)
**Entry points**: `inject()`, `createEnvironmentInjector()`, `EnvironmentInjector`
```

---

### `outline.md` — Chapter Outline
The structural blueprint for the entire book. Produced by Architect (#1), reviewed by Reader Advocate (#2).

**Required per chapter**:
- Chapter number and title
- 3-5 learning objectives (what the reader will understand after reading)
- Target reader level (beginner / intermediate / advanced)
- Key concepts introduced in this chapter
- Source files primarily covered
- Prerequisites (which prior chapters must be read first)
- Estimated word count

---

### `style-guide.md` — Writing Voice & Format Rules
The contract between Writer (#4) and Reviewer R3. Everything in here is enforced.

**Must define**:
- Target audience (e.g., "intermediate developers who know JavaScript but haven't read framework source code")
- Voice and tone (conversational vs. academic; use of "you" vs. passive voice)
- Code snippet rules (when inline vs. block; max lines without annotation; annotation style)
- Metaphor policy (types encouraged, types banned, guideline on ratio)
- Standard chapter structure (e.g., hook → problem → solution → deep-dive → summary → exercises)
- Sensitivity guidelines (no brand comparisons, no political content)
- Word count targets per chapter type (intro chapters vs. deep-dive chapters)

---

### `glossary.md` — Canonical Term Definitions
The single source of truth for every technical term used in the book. Updated by Orchestrator after each chapter.

**Format**:
```markdown
| Term | Definition | First Introduced | Source File Reference |
|------|-----------|-----------------|----------------------|
| Injector | A container that holds providers and resolves dependency tokens | Ch01 | packages/core/src/di/injector.ts:L23 |
| Token | A key used to look up a dependency in an injector | Ch01 | packages/core/src/di/injection_token.ts:L1 |
```

**Rule**: If a term is in the glossary, the Writer MUST use the exact definition given here, not a paraphrase.

---

### `metaphor-registry.md` — Metaphor & Analogy Log
Prevents R2 from flagging metaphor conflicts. Updated by Orchestrator when R2 reports new metaphors.

**Format**:
```markdown
| Metaphor | Concept Explained | Introduced | Chapters Used | Notes |
|---------|------------------|------------|---------------|-------|
| "Restaurant kitchen" | Dependency injection container | Ch01 | Ch01, Ch03 | Chef = provider, order = token |
| "Phone book" | Token-to-provider mapping | Ch01 | Ch01 | Do NOT reuse for router |
```

---

## Progress Tracking Templates (Maintained During Execution)

### `chapter-summary.md` — Chapter Memory
Filled by Orchestrator after each chapter completes Phase 3. This is the primary long-memory mechanism — Writer and R2 read this to ensure cross-chapter coherence.

**Fields per chapter**: chapter number + title, 3-sentence plot summary, key concepts introduced, new terms added to glossary, key metaphors used, open threads / forward references planted.

### `checkpoint.md` — Pipeline Progress Snapshot
Updated at major milestones. Contains the status matrix for all chapters × all steps.

**Format example**:
```markdown
| Chapter | Research | Draft | R1 | R2 | R3 | Reader | Final |
|---------|---------|-------|----|----|----|----|-------|
| Ch01 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ch02 | ✅ | ✅ | 🔄 | 🔄 | 🔄 | ⬜ | ⬜ |
| Ch03 | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
```

### `audit-log.md` — Decision & Incident Log
Record of all significant decisions, manual interventions, and exception handling during the project.

**Log entry format**:
```markdown
## 2025-01-20 Ch03 — R1 Critical Finding
**Type**: Review failure (R1 ❌ CRITICAL)
**Finding**: Writer described `inject()` as synchronous but source shows async fallback path
**Resolution**: Re-invoked Writer (#4) with R1 report as file pointer. v2 draft approved.
**Lesson**: Researcher must check async code paths explicitly in future research reports.
```
