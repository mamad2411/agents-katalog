---
name: eng-router
description: Router and lifecycle orchestrator mapping all skills in ai-skills-pro. Use when organizing multi-stage development workflows, determining which skill to run next, or exploring available agent capabilities.
---

# AI Skills Router

The central dispatch map and lifecycle execution coordinator for the `ai-skills-pro` suite.

## Lifecycle Orchestrators (One-Command Autopilot)

For full-pipeline automation with state persistence and minimal human gates, invoke these orchestrator skills instead of stepping through stages manually:

| Orchestrator | Covers | Human Gates |
| :--- | :--- | :--- |
| `eng-enterprise-lifecycle` | Full feature development (13 stages, fast-path aware) | Brief sign-off, Plan plus whitelist sign-off, Push authorization |
| `eng-review-and-fix` | Review-to-green remediation loop (5 stages, 3-5 convergence passes) | None (auto-converge, min 3 / cap 5 passes) |
| `eng-review-and-ship` | Review-fix-verify-push delivery loop (8 stages, 3-5 review passes) | Push authorization (+ remote choice on multi-remote trees) |

**Safety & quality sub-skills** (invoked inside pipelines, also usable standalone): `eng-completion-gate` (three-state completion verdict), `eng-destructive-safety-gate` (two-confirm destructive ops), `eng-hardening-review` (data integrity + error handling deep audit), `eng-change-scope-funnel` (pre-edit whitelist contract).
| `eng-defect-lifecycle` | Bug fix loop (5 stages) | RCA sign-off |
| `eng-onboarding-audit-lifecycle` | Codebase health inspection (5 stages, read-only) | None |
| `eng-hotfix-emergency-lifecycle` | P0/P1 incident fast lane (5 stages) | Hotfix approval |
| `eng-release-ops-lifecycle` | Release & ops maintenance (5 stages) | Window approval |
| `eng-refactor-lifecycle` | Progressive refactoring (7 stages) | Plan sign-off |
| `prod-content-delivery-lifecycle` | Content deliverables (5 stages) | Brief sign-off |

---

## 5 Standard End-to-End Execution Pipelines

### Pipeline 1: Full Feature Development Lifecycle (新功能研发全链路)

> **Quick Execution**: To run this complete 10-stage pipeline automatically with state persistence, invoke `eng-enterprise-lifecycle`.

The standard sequential flow from initial requirement to verified production release:

```
Step 1: Requirements Alignment & Elicitation
        prod-briefing-loop (mandatory clarification gate & brief freezing)
           │
           ▼
        prod-create-prd (if conversational requirements need full PRD structuring)
           │
           ▼
Step 2: Specification Freeze (SDD)
        eng-spec
        ↳ Artifact: specs/<feature-name>/{requirements.md, design.md, checklist.md}
           │
           ▼
Step 3: Codebase Context & Architecture Exploration
        eng-prime-context ➔ eng-analyze-codebase
        ↳ Artifact: Codebase topology, conventions & dependency graph
           │
           ▼
Step 4: Implementation Planning
        eng-plan
        ↳ Artifact: .agents/plans/<feature-name>.md (ingests frozen spec)
           │
           ▼
Step 5: Step-by-Step Implementation
        eng-execute
        ↳ Implements tasks sequentially with per-step verification
           │
           ▼
Step 6: Quality Gate & Validation
        eng-validate
        ↳ Executes full test suite, linter, type checks & build
           │
           ▼
Step 7: Code Review & Security Audit
        eng-code-review (or eng-adversarial-audit / eng-multidimensional-audit for mission-critical paths)
        ↳ Artifact: Review findings & severity rankings
           │
           ▼
Step 8: Review Remediation (if findings exist)
        eng-review-fix ➔ re-run eng-validate
           │
           ▼
Step 9: Version Control & Delivery
        eng-git-commit (atomic conventional commits) ➔ eng-git-pr (PR with test evidence)
           │
           ▼
Step 10: Retrospective & Workflow Improvement
        prod-execution-report (delivery metrics) ➔ prod-system-review (process retrospective)
```

---

### Pipeline 2: Defect Investigation & Surgical Bugfix (缺陷诊断与精准修复闭环)

The rigorous hypothesis-driven debugging loop:

```
Step 1: Root Cause Analysis & Repro Loop
        eng-bugfix-rca
        ↳ Construct tight reproduction feedback loop (fails on bug)
        ↳ Artifact: .agents/rca/rca-<bug-id>.md
           │
           ▼
Step 2: Surgical Fix Implementation
        eng-bugfix-implement
        ↳ Apply minimal code changes to turn repro loop green
           │
           ▼
Step 3: Regression Prevention & Validation
        eng-validate
        ↳ Run full test suite to guarantee zero regressions
           │
           ▼
Step 4: Atomic Commit & PR
        eng-git-commit ➔ eng-git-pr
```

---

### Pipeline 3: Codebase Onboarding & Architecture Audit (代码库接手与架构巡检)

Rapid mental model construction and health analysis:

```
Step 1: Project Grounding
        eng-prime-context (inspect tech stack, conventions, dependencies)
           │
           ▼
Step 2: Topology & Coupling Analysis
        eng-analyze-codebase (map circular dependencies, design patterns)
           │
           ▼
Step 3: Security & Concurrency Audit
        eng-adversarial-audit (first-principles vulnerability scan)
           │
           ▼
Step 4: Baseline Health Verification
        eng-validate (check linter, tests, and build status)
```

---

### Pipeline 4: DevOps & Infrastructure Hardening (运维与服务器加固)

Autonomous operations and server security:

```
Container Maintenance:
  eng-docker-update ➔ Image digest diff ➔ Zero-downtime recreation ➔ Health check probe

Server Security Hardening:
  eng-linux-security ➔ Port-scan detection ➔ Automated firewall rate-limits & IP banning
```

---

### Pipeline 5: Visual Reverse Engineering & UI Implementation (视觉逆向与UI落地)

From web interface or design target to production code:

```
Step 1: Style & Token Extraction
        vis-reverse-ui (extract computed styles, layout structures, CSS variables)
           │
           ▼
Step 2: Component Specification
        eng-spec (define UI props, slots, responsive breakpoints)
           │
           ▼
Step 3: Implementation & Validation
        eng-plan ➔ eng-execute ➔ eng-validate

Standalone Fast Lane (requirements straight to product):
        vis-product-web ➔ product analysis ➔ IA ➔ design system ➔ data-driven UI ➔ motion ➔ responsive ➔ self-reviewed runnable code

Adaptive Product Design Suite (ideas, screenshots, live URLs to reviewable prototypes):
        vis-product-design ➔ get-context ➔ ideate / image-to-code / url-to-code / audit ➔ design-qa ➔ share
```

---

### Specialized & Standalone Capability Lanes

| Domain | Skill | Purpose & Handoff |
| :--- | :--- | :--- |
| **Cognitive Core** | `cog-axiom` | Ground architectural decisions and formal engineering principles (immutable reference, no workflow) |
| **Visual Stylization** | `vis-anime-stylize` | 2D Anime portrait stylization and cel-shaded prompt compilation |
| **Visual Stylization** | `vis-vtp-3d` | 3D feature-animation character portrait translation (VTP-3D-01 protocol) |
| **Project Setup** | `prod-project-init` | Tech stack detection and automated local onboarding / development guide generation |
| **Context Management** | `prod-compress-context` | Compact active session state and create resumable context checkpoints |
| **Session Operations** | `prod-export-session` | Export session history, tool telemetry, and created artifacts into structured markdown |
| **Prompt Engineering** | `prod-prompt-enhancer` | Zero-conversation standalone prompt optimization and hardening |
| **Market Research** | `prod-mine-keywords` | 7-day breakout AI search keyword discovery and micro-SaaS opportunity mining |

---

## Strict Handoff Contracts

| Current Phase | Produced Artifact | Mandatory Next Step | Invocation Instruction |
| :--- | :--- | :--- | :--- |
| `prod-briefing-loop` | Frozen Brief Contract | `prod-create-prd` / `eng-spec` | Call the Skill tool with `"prod-create-prd"` or `"eng-spec"` |
| `prod-create-prd` | `PRD.md` | `eng-spec` | Call the Skill tool with `"eng-spec"` |
| `eng-spec` | `specs/<feature>/` | `eng-plan` | Call the Skill tool with `"eng-plan"` |
| `eng-plan` | `.agents/plans/<feature>.md` | `eng-execute` | Call the Skill tool with `"eng-execute"` |
| `eng-execute` | Code changes | `eng-validate` | Call the Skill tool with `"eng-validate"` |
| `eng-validate` | Passing tests | `eng-code-review` / `eng-adversarial-audit` | Call the Skill tool with `"eng-code-review"` |
| `eng-code-review` | Review findings | `eng-review-fix` | Call the Skill tool with `"eng-review-fix"` |
| `eng-review-fix` | Patched code | `eng-validate` (Re-verify) | Call the Skill tool with `"eng-validate"` |
| `eng-bugfix-rca` | `rca-<bug-id>.md` | `eng-bugfix-implement` | Call the Skill tool with `"eng-bugfix-implement"` |
| `eng-bugfix-implement` | Fix applied | `eng-validate` | Call the Skill tool with `"eng-validate"` |
| `eng-validate` (Post-fix) | All green | `eng-git-commit` | Call the Skill tool with `"eng-git-commit"` |

---

## Operating Protocol for Agents

1. **Check Preconditions**: Before starting any skill, verify that its input artifact exists. If missing, backtrack to the predecessor skill.
2. **Execute In Sequence**: Do not jump from `eng-spec` directly to code without `eng-plan`. Do not jump from `eng-execute` directly to commit without `eng-validate`.
3. **Explicit Tool Calls**: When transitioning phases, call the Skill tool with the exact skill name.
---

## Checkable Completion Criteria

- [ ] Selected next skill matches the current pipeline stage and its precondition artifact exists.
- [ ] Pipeline sequence respected: no jumps past validation, review, or authorization gates.
- [ ] Stage transitions performed via explicit Skill tool invocations with exact skill names.
