# Shared Skills

**Available to all roles across all stages.**

**Global rules for story/task content:** [../templates/AUTHORING_STANDARDS.md](../templates/AUTHORING_STANDARDS.md) (ADO-ready PRD lift, no invention, non-redundancy, traceability).

---

## Quick Reference

| Skill | Purpose | Cost | Roles |
|-------|---------|------|-------|
| **story-generator** | Master Story from PRD (feature-level) | 600–1200 | All |
| **sprint-story-generator** | Sprint Story from Master + scope | 600–800 | All |
| **tech-story-generator** | Tech Story (implementation SSoT, design-aligned) | 800–1200 | TL / Architect |
| **tech-task-generator** | Task files from Sprint (+ Tech Story) | 400–600 | All |
| **secrets-detector** | Secrets/credentials only (atomic) | 400 | All |
| **code-review** | Multi-file code review against checklist | 1000 | All |
| **test-matrix** | Generate test scenarios from AC | 600 | All |
| **prd-reviewer** | PRD gap analysis + feasibility | 900 | All |
| **adr-generator** | Architecture decision records | 700 | All |
| **dependency-graph** | Map service/module dependencies | 500 | All |

---

## Included Skills

### story-generator/ (Master only)

**Input**: PRD content + section IDs; **Output**: Master Story per **`templates/story-templates/master-story-template.md`** (includes 📎 PRD lift + 🎨 UI).  
For sprint scope → **sprint-story-generator**; for implementation spec → **tech-story-generator**; for tasks → **tech-task-generator**.

```bash
sdlc skills invoke story-generator \
  --type=master \
  --prd-file=docs/prd.md \
  --role=product
```

**Output Context**:
- Product: Full story with business context + priorities
- Backend: API contracts + data model implications
- Frontend: UI flows + component requirements
- QA: Acceptance criteria + test scenarios

### code-review/

Perform structured code review across multiple files.

**Input**: Code files (git diff, PR, or file list)  
**Output**: Line-by-line feedback + summary report  
**Token Cost**: 1000 tokens  

```bash
sdlc skills invoke code-review \
  --files=src/**/*.java \
  --stack=java \
  --role=backend
```

**Checks**:
- Code style + naming conventions
- Security (OWASP, injection attacks)
- Performance (N+1, loops, algorithms)
- Test coverage + error handling
- Architecture alignment

### test-matrix/

Generate comprehensive test scenarios from AC.

**Input**: Acceptance criteria (Gherkin format)  
**Output**: Test matrix with happy path, edge cases, errors  
**Token Cost**: 600 tokens  

```bash
sdlc skills invoke test-matrix \
  --ac-file=stories/US-123-ac.md \
  --role=qa
```

**Output Variants**:
- QA: Full test matrix + automation notes
- Backend: Error paths + edge cases for API
- Frontend: UI state transitions + validation

### prd-reviewer/

Analyze PRD for gaps and feasibility.

**Input**: PRD document  
**Output**: Gap report + missing sections + risk assessment  
**Token Cost**: 900 tokens  

```bash
sdlc skills invoke prd-reviewer \
  --prd-file=docs/prd.md \
  --role=product
```

**Checks**:
- All 14 required sections present
- User personas defined
- Success metrics measurable
- Dependencies clear
- Feasibility risks flagged

### adr-generator/

Create Architecture Decision Records.

**Input**: Design decision context  
**Output**: ADR with context, options, decision, consequences  
**Token Cost**: 700 tokens  

```bash
sdlc skills invoke adr-generator \
  --title="Use Redis for session caching" \
  --context="..." \
  --role=backend
```

### dependency-graph/

Map cross-team and cross-service dependencies.

**Input**: Codebase or architecture doc  
**Output**: Dependency graph + critical paths + blockers  
**Token Cost**: 500 tokens  

```bash
sdlc skills invoke dependency-graph \
  --codebase=src/ \
  --role=tpm
```

---

## Chaining Skills

Output from one skill can feed into next:

```bash
# Step 1: Generate PRD
sdlc skills invoke prd-reviewer --prd-file=prd.md --role=product
# Output: prd-reviewed.md

# Step 2: Generate stories from reviewed PRD
sdlc skills invoke story-generator \
  --prd-file=prd-reviewed.md \
  --type=master \
  --role=product
# Output: story-001.md, story-002.md, ...

# Step 3: Generate test matrix from stories
sdlc skills invoke test-matrix \
  --ac-file=story-001.md#acceptance-criteria \
  --role=qa
# Output: test-matrix-001.md
```

---

## Role-Agnostic Design

All shared skills accept any role but tailor output:

```bash
# Product views: Full AC with business context
sdlc skills invoke story-generator --role=product ...

# Backend views: API contracts + data model focus
sdlc skills invoke story-generator --role=backend ...

# QA views: Test scenarios + edge cases focus
sdlc skills invoke story-generator --role=qa ...
```

No code duplication. Single agent, context-sensitive output.

---

## Discovery

```bash
# List shared skills
sdlc skills list --category=shared

# Show skill details
sdlc skills show story-generator

# Find skills by tag
sdlc skills list --tag=story
```

---

## Token Budgets

Shared skill invocations count against your **daily/sprint budget**:

| Skill | Daily Impact | Sprint Impact |
|-------|--------------|---------------|
| story-generator | 1200 tokens | 1200 tokens per story |
| code-review | 1000 tokens | 1000 per file set |
| test-matrix | 600 tokens | 600 per story |
| prd-reviewer | 900 tokens | 900 per PRD |
| adr-generator | 700 tokens | 700 per ADR |
| dependency-graph | 500 tokens | 500 per graph |

---

## When to Use Each Skill

| Stage | Recommended Skills |
|-------|-------------------|
| 01-Intake | dependency-graph |
| 02-PRD Review | prd-reviewer |
| 03-Pre-grooming | prd-reviewer |
| 04-Grooming | story-generator |
| 05-System Design | adr-generator, dependency-graph |
| 06-Design Review | code-review (design review) |
| 07-Task Breakdown | story-generator (sprint stories) |
| 08-Implementation | code-review |
| 09-Code Review | code-review |
| 10-Test Design | test-matrix |
| 11-Test Execution | test-matrix (validation) |
| 12-Commit/Push | code-review (final) |
| 13-Documentation | adr-generator (runbooks) |
| 14-Release Signoff | dependency-graph (rollback check) |
| 15-Summary/Close | prd-reviewer (retrospective) |

---

## See Also

- **All Skills**: Run `sdlc skills list`
- **Skill Registry**: `skills/MANIFEST.json`
- **Agent Capability Matrix**: `agents/CAPABILITY_MATRIX.md`
- **Token Budgets**: `rules/token-optimization.md`
