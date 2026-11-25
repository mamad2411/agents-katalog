---
name: workflow-orchestrator
description: >
  The main skill that orchestrates the entire development workflow. Manages the full process
  from backlog to deployment, invokes each agent in the proper order, and manages review
  points with the PO. Integrates with CI/DevOps skills to automate branch management,
  deployment, and environment configuration. Supports AI builder workflows for building full applications from a single prompt.
---

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

## 🔧 Skill Path and Project Configuration

> **Skill path variable**: `${CREW_SKILLS}` = `${CLAUDE_PLUGIN_ROOT}/skills`
> All skill references use the format `${CREW_SKILLS}/{skill-name}/SKILL.md`.

### ⛔ Phase -1: Project Initialization (crew-config.json)

> **Before starting the workflow, you must verify the existence of `crew-config.json`.**
> 1. Check if `crew-config.json` exists at the project root
> 2. **If not** → Run `${CREW_SKILLS}/project-init/SKILL.md` to create it
> 3. **If yes** → Read it, verify the configuration, and proceed
>
> Proceeding beyond Phase 0 without `crew-config.json` is **prohibited**.

```
Workflow Start
     │
     ▼
crew-config.json exists?
     │
     ├── NO → Run project-init → Create crew-config.json
     │                                    │
     └── YES ─────────────────────────────┘
                                          │
                                          ▼
                               Phase -0: Project Status Check
                                          │
                                          ▼
                               Phase 0: CI/DevOps Initialization
                                         ...
```

### Common Context to Pass to All Subagents

When running subagents for each Phase, the following must be included in the prompt:

```
## Project Configuration
Read the crew-config.json file and operate according to the project settings.
In particular, check the following settings:
- conventions.idStrategy: ID strategy
- backend/frontend frameworks and languages
- tools: package manager, linter, formatter
```

## ⛔ Key Principles

### 1. ⛔ Full Plan Disclosure Principle (No Omissions)
- **Show all Phases as a plan first** (regardless of backlog characteristics)
- Even if a step can be skipped, **include all steps in the plan**
- At the time of each Phase execution, **clearly state whether it will be skipped and the rationale**
- Proceed transparently so the user can understand the full workflow

#### Required Output at Workflow Start

```markdown
## 📋 Workflow Plan: {Backlog Title}

### Planned Execution Steps
| Phase | Step | Skill | Expected Output | Notes |
|-------|------|-------|-----------------|-------|
| -1 | Project Initialization | project-init | crew-config.json | One-time only |
| -0 | Project Status Check | - | Context info | Required |
| 0 | CI/DevOps Initialization | ci, devops | Branch, Environment | Required |
| 1a | User Story Generation | user-story-generator | user-stories.md | - |
| 1b | Wireframe Generation | wireframer | wireframes.md | - |
| 1c | PO Review #1 | - | Approval/Revision | Required |
| 2a | Tech Spec Writing | tech-lead | tech-spec.md | - |
| 2b | Test Case Writing | qa-tc | test-cases.md | - |
| 3a | Design Spec/Figma | product-designer | design-spec.md | - |
| 3b | Backend Tests | be-test | Test code | - |
| 3c | API Spec | be-spec | openapi.yaml | - |
| 4a | Backend Implementation | be-main | API implementation | - |
| 4b | Frontend Implementation | fe-main | UI implementation | - |
| 5a | E2E Test Writing+Execution | qa-e2e | E2E code + results | ⛔ Execution required |
| 5b | Bug Fixes | be-main, fe-main | Fix code | Conditional |
| 5c | PO Final Review | - | Approval/Revision | Required |
| 6 | CI/Deployment | ci | PR, Merge | Required |

> Skip decisions for each step will be communicated with rationale at execution time.
```

#### Required Output Format When Skipping a Step

```markdown
### ⏭️ Phase {N}: {Step Name} - Skipped

**Skip Rationale**:
- {Specific reason 1}
- {Specific reason 2}

**Impact Scope**: {Description of impact from skipping}

> Proceeding to next step: Phase {N+1}
```

#### Required Output Format When Executing a Step

```markdown
### ▶️ Phase {N}: {Step Name} - Executing

**Execution Reason**: {Why this step is necessary}
**Input**: {Input files/information to be used}
**Expected Output**: {Artifacts to be generated}
```

### 2. Sequential Execution Principle
- **Tasks with dependencies must never be executed in parallel**
- Each Phase must be executed only after the previous Phase is completed
- Tasks within Phase 3 are also executed sequentially based on dependencies (see details below)

#### ⚡ Leveraging Agent Teams for Parallel Execution

For steps that can be executed in parallel, use **Agent Teams' shared task list and teammate agents**:

```typescript
// ⛔ Wrong approach: Execute sequentially one by one
Task(product-designer, ...)  // Wait for completion
Task(be-test, ...)           // Wait for completion
Task(be-spec, ...)           // Wait for completion

// ✅ Correct approach: Create tasks via Agent Teams → Spawn teammate agents in parallel

// 1. Register tasks to the shared task list
TaskCreate({ subject: "Generate design spec", description: "..." })  // id: "1"
TaskCreate({ subject: "Generate backend tests", description: "..." }) // id: "2"
TaskCreate({ subject: "Generate API spec", description: "..." })      // id: "3"

// 2. Spawn teammate agents in parallel (each claims a task and works on it)
Task({ name: "designer", prompt: "Check TaskList and perform 'Generate design spec' task", run_in_background: true })
Task({ name: "be-tester", prompt: "Check TaskList and perform 'Generate backend tests' task", run_in_background: true })
Task({ name: "be-spec", prompt: "Check TaskList and perform 'Generate API spec' task", run_in_background: true })

// 3. Wait for all teammates to complete (monitor status via TaskList)
TaskList()  // Check if all tasks are completed
```

**Steps eligible for parallel execution**:
| Phase | Parallelizable Steps | Condition |
|-------|---------------------|-----------|
| Phase 3 | product-designer, be-test, be-spec | No mutual dependencies |
| Phase 4 | be-main, fe-main | Once the OpenAPI spec (Phase 3c) is finalized, both BE/FE can be implemented independently |

**Sequential execution steps** (managed via task dependencies):
- Phase 5: qa-e2e → bug fixes (test results needed)

### 3. ⛔ Design Skill Workflow (Figma Required!)
- **design-spec.md is always generated** (regardless of MCP connection status)
- **⛔ Figma design creation is mandatory when MCP is connected** (skipping is prohibited!)
- The only exceptions for skipping Figma creation:
  1. MCP (TalkToFigma) is not configured
  2. The user **explicitly** requests "spec only", "without Figma", etc.
- **Prohibited**: Skipping Figma creation for reasons like "it takes too long" or "it's too complex"
- fe-main references both design-spec.md and the Figma design

### 4. ⛔ CI Verification Required Principle (Workflow Exit Condition)
- **The workflow must not end until all GitHub Actions CI checks pass**
- After PR creation, always wait for CI completion with `gh pr checks --watch`
- On CI failure: fix errors → push again → re-run CI → verify CI passes
- **Merge is performed only after CI passes**
- Creating a PR and ending the workflow without CI verification is **prohibited**

### 5. Skippable Steps and Conditions

The table below defines the steps where skipping is **allowed** and the conditions.
**Steps not listed in the table cannot be skipped.**

| Step | Skip Condition | Example Rationale for Skipping |
|------|---------------|-------------------------------|
| 1a. User Stories | Existing user-stories.md already exists and no changes are needed | "The existing user-stories.md sufficiently covers the current backlog" |
| 1b. Wireframes | Backend-only backlog (no UI), or reusing existing wireframes.md | "This backlog is API-only with no UI changes" |
| 3a. Design/Figma | Backend-only backlog, or MCP not connected + explicit user request | "API-only backlog; UI design is unnecessary" |
| 3b. Backend Tests | Frontend-only backlog (no API changes) | "This backlog is UI-only with no API changes" |
| 3c. API Spec | Frontend-only backlog, or no additions needed to existing openapi.yaml | "Using the existing API as-is; no spec changes needed" |
| 4a. Backend Implementation | Frontend-only backlog | "UI-only backlog; backend implementation is unnecessary" |
| 4b. Frontend Implementation | Backend-only backlog | "API-only backlog; frontend implementation is unnecessary" |
| 5b. Bug Fixes | All E2E tests pass at 100% | "All E2E tests passed; no bug fixes needed" |

#### ⛔ Steps That Can Never Be Skipped

The following steps **cannot be skipped under any circumstances**:
- Phase -0: Project Status Check
- Phase 0: CI/DevOps Initialization
- Phase 1c: PO Review #1
- Phase 2a: Tech Spec Writing
- Phase 2b: Test Case Writing
- Phase 5a: E2E Tests
- Phase 5c: PO Final Review
- Phase 6: CI/Deployment

# Workflow Orchestrator

Orchestrates the entire development workflow from backlog to deployment.

## Input Modes

### Mode A: Single Backlog (Conventional)
```
"Develop the sign-up feature"
"Add the product search feature"
```
→ Start directly from Phase 0

### Mode B: Comprehensive Implementation Request (Full App Builder)
```
"Build me a shopping mall"
"Develop a blog platform"
"Build a team collaboration tool"
```
→ Decompose into backlogs first, then execute sequentially

### Input Classification Criteria

| Classification | Characteristics | Examples |
|---------------|----------------|----------|
| Single Backlog | Specific feature, single domain | "Login feature", "Comment feature" |
| Comprehensive Request | Entire product/service, multi-domain | "Build me XX", "XX platform" |

## Full App Builder Workflow

Full flow for comprehensive requests:

```
User: "Build me a shopping mall"
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase -1: Backlog Decomposition (backlog-decomposer)       │
├─────────────────────────────────────────────────────────────┤
│  1. Requirements analysis                                    │
│  2. Feature list derivation                                  │
│  3. Backlog decomposition + dependency analysis              │
│  4. MVP scope determination                                  │
│  5. Prioritized backlog list generation                      │
│                                                             │
│  Output: docs/project-backlog.md                            │
│       - BL-001: Initial project setup                        │
│       - BL-002: User authentication                          │
│       - BL-003: Product catalog                              │
│       - ...                                                 │
│                                                             │
│  ➜ PO Review: Approve backlog list                           │
└─────────────────────────────────────────────────────────────┘
           │ (Approved)
           ▼
┌─────────────────────────────────────────────────────────────┐
│  Sequential Backlog Execution Loop                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  for each backlog in backlog_list:                          │
│      │                                                      │
│      ├── ⚠️ Phase -0: Project Status Check (required each loop) │
│      │     └── Analyze current directory → pass context      │
│      ├── Phase 0: CI/DevOps Initialization                  │
│      ├── Phase 1: Planning (User Stories + Wireframes)       │
│      ├── ➜ PO Review                                        │
│      ├── Phase 2: Design (Tech Spec + TC)                    │
│      ├── Phase 3: Implementation Prep (Design + Tests + Spec)│
│      ├── Phase 4: Implementation (BE + FE)                   │
│      ├── Phase 5: QA (E2E + Bug Fixes)                       │
│      ├── ➜ PO Review                                        │
│      └── CI: Commit → PR → Merge                            │
│                                                             │
│      [Move to next backlog]                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
           │
           ▼
      All Complete
```

## Full Workflow Diagram

```
                          PO (Backlog)
                               │
                               ▼
                    ┌─────────────────────┐
                    │   CI: Branch Create  │ ◀── feature/{backlog-keyword}
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  DevOps: Env Check   │ ◀── Dependencies, server status
                    └──────────┬──────────┘
                               │
┌──────────────────────────────┼──────────────────────────────┐
│                              ▼                              │
│                   ┌─────────────────┐                       │
│                   │ User Story      │ ──▶ user-stories.md   │
│  Phase 1          │ Generator       │                       │
│  (Planning)       └────────┬────────┘                       │
│                            │                                │
│                            ▼                                │
│                   ┌─────────────────┐                       │
│                   │ Wireframer      │ ──▶ wireframes.md     │
│                   └────────┬────────┘                       │
│                            │                                │
│                            ▼                                │
│                   ┌─────────────────┐                       │
│                   │ PO Review #1    │                       │
│                   └────────┬────────┘                       │
└────────────────────────────┼────────────────────────────────┘
                             │ (Approved)
┌────────────────────────────┼────────────────────────────────┐
│                            ▼                                │
│                   ┌─────────────────┐                       │
│  Phase 2          │ Tech Lead       │ ──▶ tech-spec.md      │
│  (Design)         └────────┬────────┘                       │
│                            │                                │
│                            ▼                                │
│                   ┌─────────────────┐                       │
│                   │ QA-TC           │ ──▶ test-cases.md     │
│                   └────────┬────────┘                       │
└────────────────────────────┼────────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────┐
│                   ┌────────┴────┬────────────┐              │
│                   ▼             ▼            ▼              │
│  Phase 3       ┌────────┐ ┌────────┐ ┌────────┐            │
│  (Prep-Parallel)│Designer│ │BE-Test │ │BE-Spec │            │
│                └───┬────┘ └───┬────┘ └───┬────┘            │
│                    │          └────┬─────┘                  │
└────────────────────┼───────────────┼────────────────────────┘
                     │               │
┌────────────────────┼───────────────┼────────────────────────┐
│                    │               │                        │
│  Phase 4           │         ┌─────┴─────────┐             │
│  (Impl-Parallel)   │         ▼               ▼             │
│                    │   ┌──────────┐    ┌──────────┐        │
│                    │   │ BE-Main  │    │ FE-Main  │        │
│                    │   │ API Impl │    │ UI Impl  │        │
│                    │   └────┬─────┘    └────┬─────┘        │
│                    └────────┼───────────────┘              │
│                             │                              │
└─────────────────────────────┼──────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                          ▼                                  │
│  Phase 5          ┌──────────┐                              │
│  (QA)             │ QA-E2E   │ ──▶ E2E Tests                │
│                   └────┬─────┘                              │
│                        │                                    │
│                   Bugs found? ──▶ Fix ──▶ Retest (repeat)   │
│                        │                                    │
│                        ▼ (No bugs)                          │
│                   ┌─────────────────┐                       │
│                   │ PO Final Review │                       │
│                   └────────┬────────┘                       │
└────────────────────────────┼────────────────────────────────┘
                             │ (Final approval)
                             ▼
                    ┌─────────────────────┐
                    │ DevOps: Service Check│ ◀── Health check, build
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  CI: Auto Deploy     │ ◀── Commit → PR → Merge
                    └─────────────────────┘
```

## CI/DevOps Integration

### At Backlog Start (CI Skill Integration)

Automatically executed before workflow start:

```bash
# 1. Check repo rules (.claude/repo-rules.md existence)
#    If absent, analyze repo and generate rules via CI skill

# 2. Sync main branch to latest
git checkout main
git pull origin main

# 3. Create feature branch
git checkout -b feature/{backlog-keyword}

# 4. Push branch to remote (set up tracking)
git push -u origin feature/{backlog-keyword}

# 5. Environment check (DevOps skill)
#    - Dependency installation status
#    - Service readiness
```

### At Backlog Completion (CI Skill Integration)

Automatically executed after PO final approval:

```bash
# 1. Run lint and tests
npm run lint
npm test

# 2. Commit changes (following repo rules)
git add .
git commit -m "feat({backlog-keyword}): {description}

- {Changes summary}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 3. Push to remote
git push origin feature/{backlog-keyword}

# 4. Create PR
gh pr create --title "feat({backlog-keyword}): {description}" \
  --body "## Summary
- {Changes summary}

## Test Plan
- {Test plan}

🤖 Generated with [Claude Code](https://claude.com/claude-code)"

# ⚠️ 5. Verify GitHub Actions CI checks pass (required - skipping prohibited!)
# Wait until all CI checks pass
gh pr checks {pr-number} --watch --fail-fast

# 5-1. If CI fails, fix and push again
# On CI failure, fix errors, re-commit/push, and re-run step 5

# 5-2. Final CI status check
gh pr view {pr-number} --json statusCheckRollup --jq '.statusCheckRollup[].state'
# Verify all checks are "SUCCESS"

# 6. ⚠️ Squash Merge only after CI passes (merging without CI pass is prohibited!)
gh pr merge {pr-number} --squash --delete-branch
```

> **⛔ Required**: If CI checks do not pass, **never** merge. On CI failure, fix errors, push again, and verify CI passes.

## Workflow Steps

### Phase -0: Project Status Check (Required at start of each backlog loop) ⚠️

**Purpose**: Assess the current project state before each backlog implementation to maintain context and ensure continuity with previous backlogs.

| Check Item | Action | Result |
|-----------|--------|--------|
| 1. Service Context Check | Read service context definition from `docs/project-backlog.md` | Service type, domain keywords, implementation constraints |
| 2. Directory Structure Analysis | Run `ls -la`, check main folder structure | Current project structure summary |
| 3. Identify Implemented Features | Check previous backlog completion status, scan existing code | List of already implemented features |
| 4. Dependency Check | Analyze `package.json`, `requirements.txt`, etc. | List of installed dependencies |
| 5. Current Backlog Context | Check current backlog's service context field | Implementation notes |

**Pass check results to**: All subsequent Phases as context

```markdown
## Current Project Status (Phase -0 Results)

### Service Context
- **Service Type**: {Extracted from project-backlog.md}
- **Domain Keywords**: {Extracted from project-backlog.md}
- **Implementation Constraints**: {Extracted from project-backlog.md}

### Project Status
- **Current Directory Structure**:
  ```
  {ls result summary}
  ```
- **Completed Backlogs**: BL-001, BL-002, ... (completed)
- **Currently Implementing**: BL-{N}: {Backlog title}
- **Key Existing Files**:
  - src/... (existing implementation code)
  - docs/... (existing documents)

### Current Backlog Implementation Guidelines
- **Service Context**: {Current backlog's service_context field}
- **Implementation Notes**: {Current backlog's implementation_note field}
- **Usage Examples**: {Current backlog's usage_example field}

> ⚠️ Implementation that deviates from this context is prohibited.
```

### Phase 0: Initialization (CI/DevOps)

| Step | Skill | Skill File | Task |
|------|-------|-----------|------|
| 0a | ci | `${CREW_SKILLS}/ci/SKILL.md` | Repo analysis and rule generation (one-time only) |
| 0b | ci | `${CREW_SKILLS}/ci/SKILL.md` | Feature branch creation |
| 0c | devops | `${CREW_SKILLS}/devops/SKILL.md` | Environment check and dependency verification |

### Phase 1: Planning

| Step | Skill | Skill File | Input | Output |
|------|-------|-----------|-------|--------|
| 1 | user-story-generator | `${CREW_SKILLS}/user-story-generator/SKILL.md` | Backlog | user-stories.md |
| 2 | wireframer | `${CREW_SKILLS}/wireframer/SKILL.md` | user-stories.md | wireframes.md |
| 3 | PO Review | - | User stories + wireframes | Approval/Revision request |

### Phase 2: Design

| Step | Skill | Skill File | Input | Output |
|------|-------|-----------|-------|--------|
| 4 | tech-lead | `${CREW_SKILLS}/tech-lead/SKILL.md` | user-stories.md + wireframes.md | tech-spec.md |
| 5 | qa-tc | `${CREW_SKILLS}/qa-tc/SKILL.md` | tech-spec.md | test-cases.md (GWT format) |

> **Important**: Refer to `${CREW_SKILLS}/qa-tc/SKILL.md` to write all test cases in **Given-When-Then** format.

### Phase 3: Implementation Preparation

| Step | Skill | Skill File | Input | Output |
|------|-------|-----------|-------|--------|
| 6a | **product-designer** | `${CREW_SKILLS}/product-designer/SKILL.md` | wireframes.md + tech-spec.md | **design-spec.md + Figma** |
| 6b | be-test | `${CREW_SKILLS}/be-test/SKILL.md` | test-cases.md + tech-spec.md | Test code (GWT format) |
| 6c | be-spec | `${CREW_SKILLS}/be-spec/SKILL.md` | tech-spec.md | docs/openapi.yaml |

> **⛔ When running product-designer, you must read and follow `${CREW_SKILLS}/product-designer/SKILL.md`!**
> 0. ✅ Checked for `figma-guidelines.md`? (If present, follow the rules!)
> 1. ✅ design-spec.md generation complete?
> 2. ✅ Checked TalkToFigma with `claude mcp list`?
> 3. ✅ If MCP is available, Figma design creation complete? (**Skipping prohibited!**)
> 4. ✅ Figma link added to design-spec.md?
>
> **⛔ Prohibited**: Generating only design-spec.md and skipping Figma design (when MCP is available)
> **⛔ Prohibited**: Ignoring figma-guidelines.md and using arbitrary design tokens
>
> **be-test**: Refer to `${CREW_SKILLS}/be-test/SKILL.md` and write in **Given-When-Then** format.

### Phase 4: Implementation - ⚡ Parallel Execution

| Step | Skill | Skill File | Input | Output |
|------|-------|-----------|-------|--------|
| 7 | be-main | `${CREW_SKILLS}/be-main/SKILL.md` | Test code + docs/openapi.yaml | API implementation |
| 8 | fe-main | `${CREW_SKILLS}/fe-main/SKILL.md` | design-spec.md + Figma + docs/openapi.yaml | UI + API integration |

> **⚡ Parallel Execution**: Since both BE/FE generate types from the OpenAPI spec (`npm run api:generate`), once the API spec (Phase 3c) is finalized, they can be implemented independently. Spawn be-main and fe-main **simultaneously**.
> **Important**: Refer to `${CREW_SKILLS}/fe-main/SKILL.md` and reference both design-spec.md and the Figma design.

### Phase 5: QA & Deployment

| Step | Skill | Skill File | Task |
|------|-------|-----------|------|
| 9 | qa-e2e | `${CREW_SKILLS}/qa-e2e/SKILL.md` | ⛔ E2E test writing + **execution** + bug report |
| 10 | fe-main/be-main | Respective skill files | Bug fixes (iterative) |
| 11 | PO Final Review | - | Final approval |
| 12 | devops | `${CREW_SKILLS}/devops/SKILL.md` | Service health check and build verification |
| 13 | ci | `${CREW_SKILLS}/ci/SKILL.md` | Commit → Push → PR creation |
| **14** | **ci** | `${CREW_SKILLS}/ci/SKILL.md` | **⚠️ Wait for GitHub Actions CI to pass (required!)** |
| **15** | **ci** | `${CREW_SKILLS}/ci/SKILL.md` | **Squash Merge after CI passes** |

> **⛔ Important (qa-e2e)**: Refer to `${CREW_SKILLS}/qa-e2e/SKILL.md`:
> 1. Write E2E test code in **Given-When-Then** format
> 2. **⛔ Tests must be executed** (npx playwright test) - skipping is prohibited!
> 3. Analyze test results and, on failure, **generate a bug report**
> 4. Writing test code only without executing it is **prohibited**

> **⛔ CI Verification Required Principle** (refer to `${CREW_SKILLS}/ci/SKILL.md`):
> - In step 14, you must wait for GitHub Actions completion with `gh pr checks --watch`
> - On CI failure, fix errors, push again, and re-run step 14
> - **Do not proceed to step 15 (merge) until all CI checks pass**
> - Merging or ending the workflow without CI verification is prohibited

## Usage

### Starting a Workflow

```
Examples:
- "Start developing the 'sign-up feature' backlog"
- "Start workflow: product search feature"
```

> **Automatic execution**: The CI skill creates the feature branch and the DevOps skill checks the environment.

### Initial Repo Setup (One-time)

```
Examples:
- "Set up CI for this repo"
- "Analyze this repo and generate rules"
```

> **Generated files**: `.claude/repo-rules.md`, `.claude/commit-template.md`, `.claude/pr-template.md`

### Resume from a Specific Step

```
Examples:
- "Resume from Phase 3"
- "Proceed from the QA step"
```

### Status Check

```
Examples:
- "Show me the current workflow status"
- "Which step has been completed?"
```

### Manual Deployment

```
Examples:
- "Commit the work so far and create a PR"
- "Merge the PR"
```

## Agent Skill Summary

| Skill Name | Role | Skill File (Must read and follow!) |
|------------|------|-----------------------------------|
| **backlog-decomposer** | Comprehensive request → Backlog decomposition | `${CREW_SKILLS}/backlog-decomposer/SKILL.md` |
| **ci** | Git workflow automation | `${CREW_SKILLS}/ci/SKILL.md` |
| **devops** | Environment configuration and deployment | `${CREW_SKILLS}/devops/SKILL.md` |
| user-story-generator | Backlog → User stories | `${CREW_SKILLS}/user-story-generator/SKILL.md` |
| wireframer | User stories → Wireframes | `${CREW_SKILLS}/wireframer/SKILL.md` |
| tech-lead | Tech spec + scenario writing (UUID PK required) | `${CREW_SKILLS}/tech-lead/SKILL.md` |
| **qa-tc** | **Test case writing (GWT format)** | `${CREW_SKILLS}/qa-tc/SKILL.md` |
| **product-designer** | **design-spec.md + Figma (required if MCP available!)** | `${CREW_SKILLS}/product-designer/SKILL.md` |
| **be-test** | **Backend test code (GWT format, UUID)** | `${CREW_SKILLS}/be-test/SKILL.md` |
| be-spec | OpenAPI spec (UUID PK required) | `${CREW_SKILLS}/be-spec/SKILL.md` |
| be-main | API development (UUID PK required) | `${CREW_SKILLS}/be-main/SKILL.md` |
| **fe-main** | **Frontend (design-spec + Figma reference)** | `${CREW_SKILLS}/fe-main/SKILL.md` |
| **qa-e2e** | **E2E test writing + ⛔ Execution required!** | `${CREW_SKILLS}/qa-e2e/SKILL.md` |

> **⛔ Required**: At each step, the corresponding skill file must be **read first** and its instructions followed.

> **GWT Format**: All test-related skills (qa-tc, be-test, qa-e2e) write test cases and test code in **Given-When-Then** format.
>
> **⛔ qa-e2e Execution Required**: qa-e2e must **execute the tests** after writing the test code and verify results. Writing test code only and terminating is prohibited.

> **⛔ Design Workflow (Required!)**:
> - product-designer **always** generates design-spec.md
> - **Figma design creation is required when MCP (TalkToFigma) is connected!** (skipping prohibited)
> - Figma skip allowed only when: MCP is not configured, or the user explicitly requests "spec only"
> - fe-main references both design-spec.md and the Figma design

## Document Structure

```
{project}/
├── .claude/                      # Repo-specific rules (generated by CI skill)
│   ├── repo-rules.md            # Commit/lint/branch rules
│   ├── commit-template.md       # Commit message template
│   └── pr-template.md           # PR template
├── docs/
│   ├── openapi.yaml             # ⚠️ API spec (project-wide - single file)
│   └── bl-{NNN}-{backlog-keyword}/ # Per-feature directory (e.g., bl-010-share-link)
│       ├── user-stories.md
│       ├── wireframes.md
│       ├── tech-spec.md
│       ├── test-cases.md
│       ├── design-spec.md
│       └── bug-reports/
├── src/
├── tests/
└── e2e/
```

> **⚠️ OpenAPI Spec Path**: Unified as `docs/openapi.yaml` (matches fe-main's orval configuration)

## PO Checkpoints

### Checkpoint 1: Planning Review (After Phase 1)

```markdown
## Review Targets
- docs/{backlog-keyword}/user-stories.md
- docs/{backlog-keyword}/wireframes.md

## Review Items
1. Do the user stories meet the requirements?
2. Are there any missing features?
3. Is the screen flow appropriate?

## Result
- Approved → Proceed to Phase 2
- Revision needed → Rework the relevant step
```

### Checkpoint 2: Final Approval (After Phase 5)

```markdown
## Review Targets
- Running application
- E2E test results

## Review Items
1. Are the features working correctly?
2. Does the UI match the design?
3. Are there any critical bugs?

## Result
- Approved → Proceed with CI auto-deployment
- Revision needed → Rework with the relevant agent
```

## Agent Teams Execution

> **⚠️ Prerequisite**: Agent Teams feature must be enabled
> - Set `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"` in `env` of `~/.claude/settings.json`
> - The workflow orchestrator operates as the **team leader**
> - Each skill execution is spawned as a **teammate agent**

### Agent Teams Core Concepts

| Concept | Description |
|---------|-------------|
| **Team Leader** | The workflow-orchestrator itself. Creates tasks, spawns teammates, monitors progress |
| **Teammate** | An independent agent spawned via `Task`. Claims shared tasks and performs work |
| **Shared Task List** | Managed via `TaskCreate`/`TaskList`/`TaskGet`/`TaskUpdate` |
| **Task Dependencies** | Order managed via `addBlockedBy`/`addBlocks` (e.g., Phase 4) |
| **Inter-teammate Communication** | Results passed via shared task list description/metadata |

### Team Leader Workflow Pattern

```typescript
// 1. Create task (register to shared list)
TaskCreate({
  subject: "Phase N: {task name}",
  description: "Includes skill file, I/O, context information",
  activeForm: "Performing {task name}"
})

// 2. Spawn teammate agent
Task({
  subagent_type: "general-purpose",
  name: "{role-name}-agent",
  prompt: "Check TaskList for '{task name}' task and perform it. ...",
  run_in_background: true  // For parallel execution
})

// 3. Monitor progress
TaskList()  // Check overall status
TaskGet({ taskId: "1" })  // Check individual task details

// 4. Move to next Phase after confirming completion
```

### Phase -1: Backlog Decomposition Execution (For Comprehensive Requests)

```typescript
// 1. Create task
TaskCreate({
  subject: "Phase -1: Backlog Decomposition",
  description: `
    Refer to ${CREW_SKILLS}/backlog-decomposer/SKILL.md and perform the task.

    ## User Request
    {Original user request}

    ## Project Information
    - Project root: {project path}
    - Existing codebase: {yes/no}

    ## Output
    docs/project-backlog.md

    ## ⚠️ Important Guidelines: Maintaining Service Context
    1. **Service context definition required**: The "Service Context Definition" section must be written
       - Specify service type, domain keywords, target users, core value, implementation constraints
    2. **Include service domain in backlog titles**: All backlog titles must include core service keywords
       - ❌ "Project creation and management"
       - ✅ "AI Service Builder: AI service project creation"
    3. **Include context fields in each backlog**:
       - Service context
       - Implementation notes
       - Usage examples
    4. **Context test**: The service should be identifiable from the backlog title alone

    ## Existing Guidelines
    1. Analyze the request and derive the necessary feature list
    2. Determine MVP scope
    3. Decompose and prioritize backlogs
    4. Include dependency diagram
  `,
  activeForm: "Decomposing backlogs"
})

// 2. Spawn teammate agent
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  name: "backlog-decomposer",
  prompt: "Check TaskList and perform the 'Phase -1: Backlog Decomposition' task. Check details with TaskGet before starting. Mark as completed with TaskUpdate when done.",
  description: "Backlog decomposition"
})
```

### Input Classification Logic

```python
def classify_input(user_input: str) -> str:
    """
    Classify user input and determine the appropriate workflow

    Returns:
        "single_backlog" | "comprehensive_request"
    """
    # Comprehensive request keywords
    comprehensive_keywords = [
        "build me", "develop", "platform", "service", "system",
        "app", "application", "website", "site"
    ]

    # Single backlog keywords
    single_keywords = [
        "feature", "add", "fix", "improve", "bug", "modify",
        "login", "sign-up", "search", "filter", "button"
    ]

    # Classification logic
    has_comprehensive = any(k in user_input for k in comprehensive_keywords)
    has_single = any(k in user_input for k in single_keywords)

    # Comprehensive + specific = single (e.g., "Build me a login feature")
    if has_single:
        return "single_backlog"
    elif has_comprehensive:
        return "comprehensive_request"
    else:
        return "single_backlog"  # Default
```

### Sequential Backlog Execution Loop (Agent Teams)

```typescript
// Read backlog list and service context from docs/project-backlog.md
const backlogFile = parseBacklogFile("docs/project-backlog.md");
const serviceContext = backlogFile.serviceContext;
const backlogList = backlogFile.backlogs;

for (let i = 0; i < backlogList.length; i++) {
    const backlog = backlogList[i];
    console.log("=== Backlog " + (i+1) + "/" + backlogList.length + ": " + backlog.title + " ===");

    // ⚠️ Phase -0: Project Status Check (required each loop)
    // Create task → spawn teammate → wait for completion
    TaskCreate({
        subject: "Phase -0: Project Status Check (" + backlog.id + ")",
        description: "... (detailed check items)",
        activeForm: "Checking project status"
    });
    Task({
        name: "project-inspector",
        prompt: "Perform the Phase -0 task from TaskList...",
        subagent_type: "general-purpose",
        model: "haiku"
    });
    // Use the result as project_state after completion

    // Phase 0: Branch creation (first backlog only)
    if (i === 0) {
        TaskCreate({ subject: "Phase 0a: CI Branch Creation", ... });
        TaskCreate({ subject: "Phase 0c: DevOps Environment Check", ... });
        Task({ name: "ci-agent", ... });
        Task({ name: "devops-agent", ... });
    }

    // ⚠️ Before Phase 3: Pre-collect Figma channel name
    // Teammate agents cannot interact with the user, so this must be collected in advance
    let figmaChannelName = null;
    if (backlog.hasUiComponents) {
        figmaChannelName = collectFigmaChannelIfNeeded();
    }

    // Phase 1-5: Execute Agent Teams workflow
    // For each Phase:
    // 1. Register tasks with TaskCreate (including dependencies)
    // 2. Spawn teammate agents with Task
    // 3. Monitor progress with TaskList
    // 4. Move to next Phase after confirming all tasks are completed
    executeBacklogWithAgentTeams({
        backlog,
        projectState,
        figmaChannel: figmaChannelName,
        serviceContext
    });

    // Commit (after each backlog is completed)
    TaskCreate({ subject: "Commit: feat(" + backlog.keyword + "): " + backlog.title, ... });
    Task({ name: "ci-commit-agent", ... });

    console.log("=== Backlog " + backlog.title + " completed ===");
}

// Final: PR creation → CI verification → Merge (⛔ CI verification required!)
TaskCreate({ subject: "Phase 6: CI Auto Deploy", ... });
Task({ name: "ci-deploy-agent", ... });
// ⚠️ ci-deploy-agent performs Squash Merge only after all CI checks pass
```

### Figma Channel Name Collection Function (Required Before Phase 3)

```python
def collect_figma_channel_if_needed() -> str | None:
    """
    Pre-collect the Figma channel name before entering Phase 3.
    Background agents cannot interact with the user, so this must be collected in advance.

    Returns:
        str: Figma channel code (e.g., "ABC123")
        None: No MCP or user chose to skip Figma
    """
    # 1. Check MCP connection
    mcp_list = Bash(command="claude mcp list")
    has_figma_mcp = "TalkToFigma" in mcp_list.output

    if not has_figma_mcp:
        print("⚠️ TalkToFigma MCP is not configured.")
        print("   Only design-spec.md will be generated.")
        return None

    # 2. Request Figma channel name from user
    response = AskUserQuestion(
        questions=[{
            "question": "Please enter the channel code displayed in the Figma plugin. A 6-digit code is shown when you run the plugin in Figma. (e.g., ABC123)",
            "header": "Figma Channel",
            "options": [
                {
                    "label": "Enter channel code",
                    "description": "Enter the channel code confirmed in the Figma plugin"
                },
                {
                    "label": "Skip Figma design",
                    "description": "Generate only design-spec.md without Figma design"
                }
            ],
            "multiSelect": False
        }]
    )

    if response.selected == "Skip Figma design":
        print("⚠️ Skipping Figma design generation per user request.")
        return None

    # 3. Return channel code
    channel_code = response.custom_input  # Value entered by user via "Other"
    print(f"✅ Figma channel code: {channel_code}")
    return channel_code
```

> **⚠️ Important**: This function must be executed **before** calling `execute_single_backlog_workflow()`.
> The channel name must be included in the prompt when product-designer runs in the background during Phase 3.

### Phase -0: Project Status Check Execution

```typescript
// 1. Create task
TaskCreate({
  subject: "Phase -0: Project Status Check",
  description: `
    ## Project Status Check

    Analyze the current project state before each backlog implementation to collect context.

    ### 1. Service Context Check
    Read the "Service Context Definition" section from docs/project-backlog.md and extract:
    - Service type, domain keywords, target users, core value, implementation constraints

    ### 2. Current Directory Structure Analysis
    Run ls -la from the project root to understand the structure

    ### 3. Identify Implemented Features
    - Check previous backlog completion status
    - Check docs/{previous-backlog}/ folders
    - Scan existing code in src/

    ### 4. Dependency Check
    - Read package.json or requirements.txt

    ### 5. Current Backlog Context Check
    Current backlog: {Current backlog ID}: {Backlog title}

    ### Output
    Output the check results in a structured format for subsequent Phases
  `,
  activeForm: "Checking project status"
})

// 2. Spawn teammate agent (status check runs sequentially - results needed by other Phases)
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  name: "project-inspector",
  prompt: "Check TaskList and perform the 'Phase -0: Project Status Check' task. Check details with TaskGet. When done, mark as completed with TaskUpdate and update the description with collected context information.",
  description: "Project status check"
})
```

### CI Skill Execution (Branch Creation)

```typescript
TaskCreate({
  subject: "Phase 0a: CI Branch Creation",
  description: `
    Refer to ${CREW_SKILLS}/ci/SKILL.md and perform the task.
    1. If .claude/repo-rules.md does not exist in the current repo, analyze and generate it
    2. Create feature/{backlog-keyword} branch from main branch
    3. Push to remote
    Backlog keyword: {backlog-keyword}
  `,
  activeForm: "Creating CI branch"
})

Task({
  subagent_type: "general-purpose",
  name: "ci-agent",
  prompt: "Check TaskList and perform the 'Phase 0a: CI Branch Creation' task. Check details with TaskGet before starting. Mark as completed with TaskUpdate when done.",
  description: "CI: Branch creation"
})
```

### DevOps Skill Execution (Environment Check)

```typescript
TaskCreate({
  subject: "Phase 0c: DevOps Environment Check",
  description: `
    Refer to ${CREW_SKILLS}/devops/SKILL.md and perform the task.
    1. Check development environment (Node.js, Python, Docker, etc.)
    2. Verify dependency installation status
    3. Verify service readiness
    If issues are found, provide resolution guidance
  `,
  activeForm: "Checking development environment"
})

Task({
  subagent_type: "general-purpose",
  name: "devops-agent",
  prompt: "Check TaskList and perform the 'Phase 0c: DevOps Environment Check' task. Check details with TaskGet before starting. Mark as completed with TaskUpdate when done.",
  description: "DevOps: Environment check"
})
```

### Default Skill Execution Pattern (Teammate Agent)

```typescript
// 1. Leader creates task
TaskCreate({
  subject: "Phase {N}: {skill-name} - {task title}",
  description: `
    ## ⛔ Step 1: Read the Skill File (Required!)
    First, read the ${CREW_SKILLS}/{skill-name}/SKILL.md file.
    You must follow all instructions, principles, and constraints in the skill file.

    ## ⛔ Step 2: Perform the Task Following Skill File Instructions
    Perform the task following the workflow, output format, and mandatory principles defined in the skill file.

    ## ⚠️ Project Context (Must follow)
    {Full project_state content collected in Phase -0}

    ### Service Context
    - Service Type: {service_type}
    - Domain Keywords: {domain_keywords}
    - Implementation Constraints: {implementation_constraints}

    ### Current Backlog Implementation Guidelines
    - Service Context: {current_backlog.service_context}
    - Implementation Notes: {current_backlog.implementation_note}
    - Usage Examples: {current_backlog.usage_example}

    > ⚠️ Implementation that deviates from the above context is prohibited.

    ## Task Information
    Skill file: ${CREW_SKILLS}/{skill-name}/SKILL.md
    Backlog keyword: {backlog-keyword}
    Input: docs/{backlog-keyword}/{input-file}.md
    Output: docs/{backlog-keyword}/{output-file}.md
  `,
  activeForm: "Performing {skill-name}"
})

// 2. Set dependencies if needed
TaskUpdate({ taskId: "{currentTaskID}", addBlockedBy: ["{precedingTaskID}"] })

// 3. Spawn teammate agent
Task({
  subagent_type: "general-purpose",
  name: "{skill-name}-agent",
  prompt: `Check TaskList and perform the 'Phase {N}: {skill-name}' task.
    Check details with TaskGet, then perform the task following the instructions in the description.
    ⛔ You must read the skill file (${CREW_SKILLS}/{skill-name}/SKILL.md) first.
    When done, update status to completed with TaskUpdate.`,
  description: "{skill-name} execution",
  run_in_background: false  // false for sequential, true for parallel
})
```

> **⛔ Required**: All teammate agents must read the task's description via `TaskGet`, **read the corresponding SKILL.md first**, and follow its instructions.
> Performing work without reading the skill file is prohibited.

### ⛔ product-designer Skill Execution (Figma Required!)

> **⚠️ Important**: Before executing this skill, you must complete the "Before Phase 3: Pre-collect Figma Channel Name" step!
> Teammate agents cannot interact with the user, so the channel name must be **collected in advance** and included in the task description.

```typescript
// Pre-collected Figma channel name variable (collected before Phase 3)
// figmaChannelName: string | null

// 1. Create task (including Figma channel information)
TaskCreate({
  subject: "Phase 3a: product-designer - design-spec + Figma",
  description: `
    ## ⛔⛔⛔ Step 1: Read the Skill File (Required!) ⛔⛔⛔
    First, read the ${CREW_SKILLS}/product-designer/SKILL.md file.

    ## ⚠️ Figma Channel Information (Pre-collected from workflow)
    // If figmaChannelName exists:
    //   Channel code: {figmaChannelName}
    //   ⛔ When creating Figma design, you must first connect to the channel with join_channel.
    //   > Note: Do not ask the user for the channel name again.
    // If figmaChannelName is null:
    //   Figma skip requested - generate only design-spec.md.

    ## ⛔⛔⛔ Step 2: Follow the Skill File Checklist ⛔⛔⛔
    ### Step 0: Check figma-guidelines.md (Required!)
    ### Step 1: Generate design-spec.md (Required)
    ### Step 2: Create Figma Design (Required if channel info provided!)
    ### Step 3: Add Figma link to design-spec.md

    ## Task Information
    Skill file: ${CREW_SKILLS}/product-designer/SKILL.md
    Backlog keyword: {backlog-keyword}
    Input: docs/{backlog-keyword}/wireframes.md, docs/{backlog-keyword}/tech-spec.md
    Output: docs/{backlog-keyword}/design-spec.md + Figma design (if channel provided)
  `,
  activeForm: "Generating design spec + Figma"
})

// 2. Spawn teammate agent (run_in_background: true for parallel execution in Phase 3)
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  name: "designer-agent",
  prompt: `Check TaskList and perform the 'Phase 3a: product-designer' task.
    Check details (including Figma channel info) with TaskGet before starting.
    ⛔ You must read ${CREW_SKILLS}/product-designer/SKILL.md first.
    When done, update status to completed with TaskUpdate.`,
  run_in_background: true,
  description: "product-designer: design-spec + Figma"
})
```

> **⛔ Note**: Verify before/after running product-designer:
>
> **Before execution (before Phase 3):**
> 1. Have you checked if MCP (TalkToFigma) is connected?
> 2. If MCP is available, have you **pre-collected** the Figma channel name from the user?
> 3. Have you included the channel name in the task description?
>
> **After execution (check with TaskList):**
> 1. Is the task status completed?
> 2. Has the design-spec.md file been generated?
> 3. If a channel name was provided, has the Figma design also been created? (**Skipping prohibited!**)

### CI Skill Execution (Auto Deploy) ⚠️ Mandatory CI Verification Included

```typescript
// 1. Create task
TaskCreate({
  subject: "Phase 6: CI Auto Deploy",
  description: `
    ## ⛔ Step 1: Read the Skill File (Required!)
    First, read the ${CREW_SKILLS}/ci/SKILL.md file.

    ## ⛔ Step 2: Perform Deployment Following Skill File Instructions
    PO final approval complete. Proceed with auto deployment:
    1. Run lint and tests
    2. Commit changes (following .claude/repo-rules.md rules)
    3. Push to remote
    4. Create PR

    ⛔ Required: GitHub Actions CI Verification (skipping prohibited!)
    5. gh pr checks --watch --fail-fast
    6. Check CI status → verify all checks are SUCCESS
    7. Squash Merge only after all CI passes

    Skill file: ${CREW_SKILLS}/ci/SKILL.md
    Backlog keyword: {backlog-keyword}
    Changes summary: {description}
  `,
  activeForm: "CI/CD deployment in progress"
})

// 2. Spawn teammate agent
Task({
  subagent_type: "general-purpose",
  name: "ci-deploy-agent",
  prompt: `Check TaskList and perform the 'Phase 6: CI Auto Deploy' task.
    Check details with TaskGet before starting.
    ⛔ You must read ${CREW_SKILLS}/ci/SKILL.md first.
    ⛔ Do not mark as completed until all CI checks pass.
    When done, update status to completed with TaskUpdate.`,
  description: "CI: Auto deploy (CI verification required)"
})
```

> **⛔ Note**: When running the CI teammate agent:
> 1. The `${CREW_SKILLS}/ci/SKILL.md` file must be read first
> 2. It must wait until GitHub Actions pass
> 3. Skipping CI verification and marking the task as completed is prohibited

### ⚠️ Before Phase 3: Pre-collect Figma Channel Name (Required!)

> **Important**: Background agents cannot interact with the user, so the Figma channel name **must** be collected before entering Phase 3.

```typescript
// Check Figma MCP and collect channel name before Phase 3 starts
let figmaChannelName = null;

// 1. Check MCP connection
const mcpList = await Bash({ command: "claude mcp list" });
const hasFigmaMCP = mcpList.includes("TalkToFigma");

if (hasFigmaMCP) {
  // 2. Request Figma channel name from user (using AskUserQuestion)
  const response = await AskUserQuestion({
    questions: [{
      question: "Please enter the channel code displayed in the Figma plugin. (e.g., ABC123)",
      header: "Figma Channel",
      options: [
        { label: "Enter channel code", description: "Enter the channel code confirmed in the Figma plugin" },
        { label: "Skip Figma", description: "Generate only design-spec.md without Figma design" }
      ],
      multiSelect: false
    }]
  });

  if (response.answer === "Enter channel code") {
    figmaChannelName = response.customInput;  // Channel name entered by user
  }
  // If "Skip Figma" is selected, figmaChannelName remains null
}

// 3. Pass channel name to Phase 3 tasks
console.log("Figma channel: " + (figmaChannelName || "Not used"));
```

### Parallel Execution (Phase 3) - Agent Teams Parallel Teammate Spawning

The three tasks in Phase 3 are executed using **Agent Teams' shared task list + parallel teammate agents**.
Sequential execution is inefficient and prohibited.

```typescript
// Notify user at Phase 3 start
console.log("### ▶️ Phase 3: Implementation Preparation - Agent Teams Parallel Execution");
console.log("The following 3 tasks will be executed simultaneously via teammate agents:");
console.log("- 3a. designer-agent: design-spec.md + Figma");
console.log("- 3b. be-test-agent: Backend test code");
console.log("- 3c. be-spec-agent: docs/openapi.yaml");

// Step 1: Register 3 tasks to the shared task list
TaskCreate({
  subject: "Phase 3a: product-designer - design-spec + Figma",
  description: `
    Refer to ${CREW_SKILLS}/product-designer/SKILL.md and perform the task.
    // If figmaChannelName exists: ⚠️ Figma channel code: {figmaChannelName} - Figma design creation required!
    // If figmaChannelName is null: Skip Figma - generate only design-spec.md
    Backlog keyword: {backlog-keyword}
    Input: docs/{backlog-keyword}/wireframes.md, docs/{backlog-keyword}/tech-spec.md
    Output: docs/{backlog-keyword}/design-spec.md
  `,
  activeForm: "Generating design spec"
});  // → taskId: "3a"

TaskCreate({
  subject: "Phase 3b: be-test - Backend test code",
  description: `
    Refer to ${CREW_SKILLS}/be-test/SKILL.md and perform the task.
    Backlog keyword: {backlog-keyword}
    Input: docs/{backlog-keyword}/test-cases.md, docs/{backlog-keyword}/tech-spec.md
    Output: Test code (GWT format)
  `,
  activeForm: "Generating backend tests"
});  // → taskId: "3b"

TaskCreate({
  subject: "Phase 3c: be-spec - API Spec",
  description: `
    Refer to ${CREW_SKILLS}/be-spec/SKILL.md and perform the task.
    Backlog keyword: {backlog-keyword}
    Input: docs/{backlog-keyword}/tech-spec.md
    Output: docs/openapi.yaml
  `,
  activeForm: "Generating API spec"
});  // → taskId: "3c"

// Step 2: Spawn 3 teammate agents in parallel (must use run_in_background: true)
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  name: "designer-agent",
  prompt: `Check TaskList and perform the 'Phase 3a: product-designer' task.
    Read the description with TaskGet and follow skill file instructions.
    When done, TaskUpdate(status: "completed").`,
  run_in_background: true,
  description: "Design spec generation"
});

Task({
  subagent_type: "general-purpose",
  model: "haiku",
  name: "be-test-agent",
  prompt: `Check TaskList and perform the 'Phase 3b: be-test' task.
    Read the description with TaskGet and follow skill file instructions.
    When done, TaskUpdate(status: "completed").`,
  run_in_background: true,
  description: "Backend test generation"
});

Task({
  subagent_type: "general-purpose",
  model: "haiku",
  name: "be-spec-agent",
  prompt: `Check TaskList and perform the 'Phase 3c: be-spec' task.
    Read the description with TaskGet and follow skill file instructions.
    When done, TaskUpdate(status: "completed").`,
  run_in_background: true,
  description: "API spec generation"
});

// Step 3: Leader monitors all teammates via TaskList
console.log("⏳ Waiting for 3 teammate agents to complete...");
// Periodically check TaskList to verify all Phase 3 tasks are completed
// Or wait for each teammate's completion via TaskOutput

// Step 4: Verify results
TaskList();  // Check all Phase 3 task statuses
console.log("✅ Phase 3 complete");
```

### Parallel Execution (Phase 4) - BE/FE Simultaneous Implementation

The be-main and fe-main tasks in Phase 4 are executed **in parallel**.
Once the OpenAPI spec (Phase 3c) is finalized, both BE and FE can generate types and implement independently.

> **Rationale**: Since both BE/FE generate types from `docs/openapi.yaml` (`npm run api:generate`),
> there is no need to wait for each other's implementation once the API spec is finalized.

```typescript
// Notify user at Phase 4 start
console.log("### ▶️ Phase 4: Implementation - BE/FE Parallel Execution");
console.log("OpenAPI spec is finalized, so BE/FE will run simultaneously:");
console.log("- 4a. be-main-agent: Backend API implementation");
console.log("- 4b. fe-main-agent: Frontend UI implementation");

// Step 1: Create tasks (no dependencies - parallel)
TaskCreate({
  subject: "Phase 4a: be-main - Backend API Implementation",
  description: `
    Refer to ${CREW_SKILLS}/be-main/SKILL.md and perform the task.
    Input: Test code + docs/openapi.yaml
    Output: API implementation code
  `,
  activeForm: "Implementing backend API"
});  // → taskId: "4a"

TaskCreate({
  subject: "Phase 4b: fe-main - Frontend UI Implementation",
  description: `
    Refer to ${CREW_SKILLS}/fe-main/SKILL.md and perform the task.
    Input: design-spec.md + Figma + docs/openapi.yaml
    Output: UI + API integration code
  `,
  activeForm: "Implementing frontend UI"
});  // → taskId: "4b"

// ⚠️ No dependencies - both BE/FE can independently generate types from the OpenAPI spec

// Step 2: Spawn BE/FE teammate agents in parallel (run_in_background: true)
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  name: "be-main-agent",
  prompt: `Check TaskList and perform the 'Phase 4a: be-main' task.
    ⛔ You must read ${CREW_SKILLS}/be-main/SKILL.md first.
    When done, TaskUpdate(status: "completed").`,
  run_in_background: true,
  description: "Backend API implementation"
});

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  name: "fe-main-agent",
  prompt: `Check TaskList and perform the 'Phase 4b: fe-main' task.
    ⛔ You must read ${CREW_SKILLS}/fe-main/SKILL.md first.
    Reference both design-spec.md and the Figma design.
    When done, TaskUpdate(status: "completed").`,
  run_in_background: true,
  description: "Frontend UI implementation"
});

// Step 3: Leader monitors all teammates via TaskList
console.log("⏳ Waiting for BE/FE teammate agents to complete...");
// Periodically check TaskList to verify all Phase 4 tasks are completed

// Step 4: Verify results
TaskList();  // Check all Phase 4 task statuses
console.log("✅ Phase 4 complete");
```

> **⛔ Note**: Do not execute Phase 3 and Phase 4 tasks sequentially.
> Phase 3: The three tasks have no mutual dependencies, so teammate agents must be spawned in parallel.
> Phase 4: Once the OpenAPI spec is finalized, both BE/FE can implement independently, so spawn them in parallel.

### Model Selection

| Skill | Recommended Model | Reason |
|-------|-------------------|--------|
| **backlog-decomposer** | **sonnet** | **Complex analysis and decomposition** |
| ci | haiku | Command execution |
| devops | haiku | Environment check |
| user-story-generator | sonnet | Creative writing |
| wireframer | haiku | Structured output |
| tech-lead | sonnet | Architecture complexity |
| qa-tc | haiku | Pattern-based |
| product-designer | sonnet | MCP utilization |
| be-test / be-spec | haiku | Pattern-based |
| be-main / fe-main | sonnet | Business logic |
| qa-e2e | haiku | Pattern-based |

## References

- **Agent Teams Documentation**: https://code.claude.com/docs/en/agent-teams
- **Backlog Decomposition Skill**: [${CREW_SKILLS}/backlog-decomposer/SKILL.md](${CREW_SKILLS}/backlog-decomposer/SKILL.md)
- CI Skill: [${CREW_SKILLS}/ci/SKILL.md](${CREW_SKILLS}/ci/SKILL.md)
- DevOps Skill: [${CREW_SKILLS}/devops/SKILL.md](${CREW_SKILLS}/devops/SKILL.md)
- Agent Dependencies: [references/agent-dependencies.md](references/agent-dependencies.md)

### Agent Teams Tool Summary

| Tool | Role | Used By |
|------|------|---------|
| `TaskCreate` | Register tasks to the shared task list | Leader (orchestrator) |
| `TaskList` | Query all task statuses | Leader + Teammates |
| `TaskGet` | Query task details | Teammates (pre-work check) |
| `TaskUpdate` | Update task status/dependencies | Leader + Teammates |
| `Task` | Spawn teammate agent | Leader |

> **Configuration**: Requires `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"` in `env` of `~/.claude/settings.json`
