---
name: spec-driven-development-framework
description: Technical implementation guide for Spec-Driven Development (SDD) using the OpenSpec framework and compatible tools. Covers directory architecture, CLI lifecycle, delta specs, multi-agent configuration, and brownfield adoption. Use when implementing SDD in a codebase, configuring agent tools for spec-driven workflows, or migrating from ad-hoc prompting to structured development.
---

# Spec-Driven Development Framework

## Overview

Spec-Driven Development (SDD) moves AI coding away from unstructured, iterative chatting toward a disciplined engineering process where requirements are codified and verified before implementation. This skill provides the technical implementation guide for adopting SDD in real codebases using the OpenSpec framework and compatible tooling.

## When to Use

- Implementing SDD in a new or existing codebase
- Configuring Cursor, Claude Code, Windsurf, or RooCode for spec-driven workflows
- Migrating a team from ad-hoc prompting to structured development
- Building internal tools that generate or validate intent specifications
- Designing CI/CD pipelines that enforce spec-before-code policies

## Core Architecture

### The OpenSpec Directory Structure
```
openspec/
  specs/                    # Source of Truth
    auth/
      spec.md               # Current auth system logic and constraints
    billing/
      spec.md               # Current billing system logic and constraints
    ...
  changes/                  # Active Workspace
    feature-123/
      proposal.md           # Options, tradeoffs, recommendation
      tasks.md              # Checklist of implementation tasks
      design.md             # Architecture and interface decisions
      specs/                # Delta specs for this change
        auth-changes.md
        billing-changes.md
      archive/              # Completed artifacts merged here
```

### Key Design Principles
1. **Living Documentation:** Specs are plain Markdown files in version control, updated every time a feature merges
2. **Context Engineering:** Isolate changes into specific folders, feeding AI only relevant "delta" information
3. **Archive Model:** Once complete, temporary artifacts merge into the permanent spec and move to historical archive
4. **First-Class Citizens:** Specifications sit alongside source code, not in a separate wiki or document system

## The SDD Lifecycle (Technical)

### Step 1: Explore (`/opsx:explore` or equivalent)
**Purpose:** Discover without committing.
**Process:**
- AI reads the codebase to identify bottlenecks and architectural options
- Human defines the problem space and success criteria
- Output: Options analysis with tradeoffs, risks, and recommendations

**Tool Configuration:**
```json
{
  "command": "explore",
  "scope": "read-only",
  "output": "openspec/changes/{id}/proposal.md",
  "constraints": ["no-code-changes", "no-test-execution"]
}
```

### Step 2: Propose (`/opsx:proposal`)
**Purpose:** Scaffold the change and catch logic errors early.
**Process:**
- AI generates proposal.md with options, tasks.md with checklist, and design.md with architecture
- Human reviews for logic errors, missing edge cases, and architectural consistency
- Output: Approved or revised proposal

**Proposal Template:**
```markdown
# Proposal: {Feature Name}

## Objective
What problem are we solving and why?

## Options Considered
| Option | Pros | Cons | Risk |
|--------|------|------|------|
| A | ... | ... | ... |
| B | ... | ... | ... |

## Recommendation
Option {X} because ...

## Tasks
- [ ] Task 1: ...
- [ ] Task 2: ...

## Open Questions
1. ...
```

### Step 3: Refine
**Purpose:** Lock the "what" and "how" before any code is written.
**Process:**
- Human and AI iterate on design.md and specs/ until zero ambiguities remain
- Edge cases defined, constraints tightened, verification criteria established
- Output: Locked intent spec with explicit approval

**Lock Criteria:**
- All tasks have acceptance criteria
- All edge cases are documented with handling strategy
- All constraints are measurable
- Human has signed off with explicit "spec locked" comment

### Step 4: Apply (`/opsx:apply`)
**Purpose:** Execute against the locked spec.
**Process:**
- AI executes code changes, checking off tasks one by one
- Strictly constrained by agreed-upon specs
- Human monitors progress, intervenes on anomalies
- Output: Implemented feature matching the spec

**Apply Rules:**
- If AI discovers a spec ambiguity during apply, it stops and requests clarification
- No improvising beyond the spec without human approval
- Each task must be verifiable against its acceptance criteria

### Step 5: Archive (`/opsx:archive`)
**Purpose:** Maintain the Source of Truth.
**Process:**
- Completed specs merge into main /specs/ directory
- Change folder moves to archive or is deleted
- Documentation updated to reflect new system state
- Output: Updated living documentation + clean workspace

## Delta Specs

### Purpose
Traditional specs describe the entire system. Delta specs describe only what changes, dramatically reducing token usage and preventing catastrophic forgetting in long AI sessions.

### Format
```markdown
# Delta Spec: {Change ID}

## Scope
Files/modules affected: ...

## Current State
Brief description of how it works now (2-3 sentences)

## Desired State
Brief description of how it should work (2-3 sentences)

## Interface Changes
- Add: `function newMethod(args): ReturnType`
- Modify: `function existingMethod(args)` — change behavior to ...
- Remove: `function oldMethod(args)` — replace with ...

## Constraints
- Must not break existing API consumers
- Must maintain backward compatibility for 2 versions
- Must complete in < 100ms for 99th percentile

## Verification
- [ ] Unit test: ...
- [ ] Integration test: ...
- [ ] Manual check: ...
```

### Token Efficiency
Using delta specs instead of full requirement docs can reduce tokens per request by 60–80% in large codebases.

## Multi-Agent Configuration

### AGENTS.md
Standardized configuration file for tool-agnostic agent behavior:
```markdown
# AGENTS.md

## Project Context
- Language: TypeScript
- Framework: Next.js
- Testing: Vitest + Playwright
- Style: Conventional Commits, ESLint strict

## Spec-Driven Rules
1. Read openspec/specs/ before proposing changes
2. Create delta spec in openspec/changes/ before applying code
3. Update openspec/specs/ after archiving
4. Never modify code without a locked spec

## Verification Requirements
- All changes must have passing tests
- All changes must update relevant specs
- All changes must include manual verification steps
```

### Tool-Specific Slash Commands
| Tool | Explore Command | Propose Command | Apply Command | Archive Command |
|------|----------------|-----------------|---------------|-----------------|
| Claude Code | `/explore` | `/propose` | `/apply` | `/archive` |
| Cursor | `@opsx-explore` | `@opsx-propose` | `@opsx-apply` | `@opsx-archive` |
| Windsurf | `/explore` | `/propose` | `/apply` | `/archive` |
| RooCode | `/opsx:explore` | `/opsx:proposal` | `/opsx:apply` | `/opsx:archive` |

## Brownfield Adoption

### Phase 1: Documentation (Week 1)
- Generate current-state specs for critical subsystems
- Do not change code; only document what exists
- Priority: auth, billing, API contracts, data models

### Phase 2: Pilot Change (Week 2–3)
- Select a low-risk bug fix or feature enhancement
- Run full SDD lifecycle: explore → propose → refine → apply → archive
- Evaluate friction points and adjust templates

### Phase 3: Integration (Week 4–6)
- Add spec validation to CI/CD (check that changes/ has corresponding spec)
- Train team on delta spec writing
- Establish "no spec, no merge" policy for new features

### Phase 4: Scale (Month 2+)
- Generate specs automatically from existing code for legacy modules
- Create spec templates for common change types
- Measure and optimize: spec writing time vs. rework reduction

## CI/CD Integration

### Spec Validation Gate
```yaml
# .github/workflows/spec-check.yml
name: Spec Validation
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for delta spec
        run: |
          if git diff --name-only origin/main | grep -q "^openspec/changes/"; then
            echo "✓ Delta spec found"
          else
            echo "✗ No delta spec found for code changes"
            exit 1
          fi
      - name: Verify spec completeness
        run: |
          # Custom script checking for Objective, Outcomes, Constraints, Edge Cases, Verification
          python scripts/validate_spec.py openspec/changes/
```

### Archive Automation
```yaml
# Post-merge: auto-archive completed changes
- name: Archive completed specs
  if: github.event.pull_request.merged == true
  run: |
    python scripts/archive_spec.py --pr ${{ github.event.pull_request.number }}
    git add openspec/specs/
    git commit -m "docs: archive specs from PR #${{ github.event.pull_request.number }}"
```

## A-Tech Applications

### A-Coder (IDE)
- **SDD Mode:** Toggle that enforces explore → propose → refine → apply → archive flow
- **Delta Spec Generator:** Auto-create delta spec from selected code changes
- **Spec Validator:** Inline linting for spec completeness (five required elements)
- **Archive Assistant:** One-click archive after PR merge
- **Brownfield Scanner:** Generate current-state specs from existing codebase

### Be Practical (Playbooks)
- **"SDD in 30 Days"** implementation roadmap for existing teams
- **"Delta Spec Cookbook"** — templates for 20 common change types
- **"CI/CD for Specs"** — GitHub Actions, GitLab CI, and custom scripts
- **"Migrating from Vibe Coding to SDD"** — change management guide

### Builder's Club
- **OpenSpec contribution:** Community extensions and templates
- **Brownfield rescue squad:** Help members adopt SDD in legacy projects
- **Spec review exchange:** Peer review of specs before agent execution
- **Automation showcase:** Scripts and tools that make SDD frictionless

## Measurement Framework

| Metric | Definition | Target |
|--------|-----------|--------|
| Spec coverage | % of code changes with corresponding delta spec | ≥ 90% |
| Spec-to-code accuracy | % of accepted specs that require zero post-apply revision | ≥ 80% |
| Cycle time | Median time from explore to archive | ≤ 3 days |
| Rework rate | % of merged changes requiring post-merge fixes | ≤ 10% |
| Documentation freshness | % of specs current with code (≤ 7 days drift) | ≥ 95% |

## Cross-References
- See `ai-agents-and-workflows/intent-engineering-spec-driven` for the strategic discipline of intent engineering
- See `developer-experience-and-flow/orchestrator-engineer-mindset` for team transformation and training
- See `developer-experience-and-flow/supervisory-engineering-work` for the new work category of verification and direction

## Sources
- Jonathan Soh / Fission AI — OpenSpec Framework (LinkedIn, 2026)
- Pathmode — "Intent Engineering: The Discipline That Replaced Prompt Engineering" (pathmode.io, 2026)
- Anthropic — "2026 Agentic Coding Trends Report" (resources.anthropic.com)
- Siu Fai Chui — Codetape: semantic trace recording for AI-assisted development (LinkedIn, 2026)
