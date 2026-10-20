---
description: Phase Commit Workflow - Commit between phases as mandatory workflow
alwaysApply: false
tags: [git, workflow, phases, commits]
priority: 2
version: 1.0.0
---

# Phase Commit Workflow Rule

## 🔴 MANDATORY: Commit Between Phases

**ALL work MUST be committed between phases. Commits are created after each phase completion before proceeding to the next phase.**

---

## Core Requirements

### When to Commit

**Commits are created:**
1. **After Phase Completion**: When a major phase is completed (Phase 0.1, 0.2, 0.3, Phase 1, Phase 2, etc.)
2. **Before Next Phase**: Before starting work on the next phase
3. **Explicit User Request**: When user explicitly requests a commit

**Commits are NOT created:**
- During active phase work (unless user explicitly requests)
- After every file change
- Without completing a phase milestone

---

## Commit Message Format

### Standard Commit Message Structure

**Format:** Follow git-workflow.mdc rules with phase information

```
{PREFIX}: Phase {PHASE}: {TITLE}

- {Deliverable 1}
- {Deliverable 2}
- {Key achievement}

---
Produced By AI: Composer and Cursor IDE
```

**Examples:**

```
Feat: Phase 1: Foundation Setup Complete

- Created complete project structure
- Implemented all service interfaces and implementations
- Created Docker Compose configuration
- Added database migrations (Liquibase)
- Created embedding service (Python FastAPI)
- Added unit and integration test projects

---
Produced By AI: Composer and Cursor IDE
```

```
Docs: Phase 0.3: Implementation Specification Complete

- Complete project structure specified
- All service interfaces and implementations defined
- Docker configuration specified
- Database migrations defined

---
Produced By AI: Composer and Cursor IDE
```

---

## Commit Prefixes

**Use appropriate prefix based on phase content:**

- **Feat:** New features, major implementations (Phase 1, 2, 3, etc.)
- **Docs:** Documentation only (Phase 0.1, 0.2, 0.3, etc.)
- **Test:** Testing infrastructure (Phase 6.1, 6.2, etc.)
- **Refactor:** Code refactoring (if applicable)
- **Fix:** Bug fixes (if applicable)

---

## Workflow

### Phase Completion Workflow

**After completing a phase:**

1. **Review Phase Deliverables**
   - Verify all phase deliverables are complete
   - Check for any missing files or incomplete implementations

2. **Stage All Changes**
   ```bash
   git add -A
   ```

3. **Create Commit**
   ```bash
   git commit -m "Feat: Phase {PHASE}: {TITLE}

   - {Deliverable 1}
   - {Deliverable 2}
   - {Key achievement}

   ---
   Produced By AI: Composer and Cursor IDE"
   ```

4. **Create Version Tag** (if applicable)
   - Follow version-tagging.mdc rules
   - Create tag after commit

5. **Proceed to Next Phase**
   - Start next phase work
   - Do not commit during active phase work

---

## Phase-to-Commit Mapping

| Phase | Commit Prefix | Tag Version |
|-------|--------------|-------------|
| Phase 0.1 | Docs | v0.1.0 |
| Phase 0.2 | Docs | v0.2.0 |
| Phase 0.3 | Docs | v0.3.0 |
| Phase 0.4 | Docs | v0.4.0 |
| Phase 0.5 | Docs | v0.5.0 |
| Phase 1 | Feat | v1.0.0 |
| Phase 2 | Feat | v1.1.0 |
| Phase 3 | Feat | v1.2.0 |
| Phase 4 | Feat | v1.3.0 |
| Phase 5 | Feat | v1.4.0 |
| Phase 6 | Test/Feat | v1.5.0 |

---

## Integration with Version Tagging

**After committing a phase:**

1. **Commit phase work** (this rule)
2. **Create version tag** (version-tagging.mdc rule)
3. **Proceed to next phase**

**Tag is created AFTER commit, not before.**

---

## Remember

✅ **ALWAYS commit between phases** - No exceptions  
✅ **ALWAYS use proper commit message format** - Include phase number and deliverables  
✅ **ALWAYS stage all changes** - Use `git add -A` before commit  
✅ **ALWAYS create tag after commit** - Follow version-tagging.mdc  
✅ **NEVER commit during active phase work** - Only at phase completion  
✅ **NEVER skip commits between phases** - Each phase must be committed separately  
✅ **NEVER combine multiple phases** - One commit per phase

---

**Last Updated:** 2025-11-12  
**Version:** 1.0.0  
**Status:** MANDATORY  
**Priority:** HIGH
