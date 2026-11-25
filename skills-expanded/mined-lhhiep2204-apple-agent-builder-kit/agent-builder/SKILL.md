---
name: agent-builder
description: "Use when: creating, refactoring, auditing, upgrading, or debugging Copilot custom agents, skills, instructions, prompts, or hooks for Apple platform software engineering and agile delivery workflows."
---

# Agent Builder

Consumers:
- `Agent Builder` in `.github/agents/agent-builder.agent.md` (conductor)
- `Apple Agent Generator` in `.github/agents/apple-agent-generator.agent.md` (artifact requirements, bundle shapes)
- `Apple Quality Auditor` in `.github/agents/apple-quality-auditor.agent.md` (audit standard, minimums)
- `Apple Codebase Analyzer` in `.github/agents/apple-codebase-analyzer.agent.md` (analysis template, workflow signals)
- `.github/instructions/agent-builder.instructions.md` (generation quality standards, file editing rules)

Use this skill to design and generate high-quality Copilot customization bundles for Apple platform projects. This is the single source of truth for the complete kit workflow, bundle shapes, and artifact behavioral requirements.

## Section Index

| Section | What it covers |
|---------|---------------|
| Use Cases | When to invoke this skill |
| Apple Scope | Platforms, fallback defaults, alignment rule |
| Operating Modes / Three Operating Flows | Discovery vs Fast, Greenfield vs Verify vs Extend |
| Default Behavior | Generation defaults, tool restrictions, alignment |
| Single-Session Completion Rule | Never abandon mid-workflow, vscode_askQuestions |
| Workflow | 6-phase standard flow, kit reference files, community skill discovery |
| Bundle Shapes | Single / Focused / Full Kit minimums |
| Artifact Requirements | Per-primitive rules: Agent, Skill, Instruction, Prompt, Hook, YAML Frontmatter |
| Generation Principles | 8 non-negotiable rules for every generated agent |
| Harness Engineering Alignment | Feedforward/feedback, control types, key patterns |
| Large Task Execution Pattern | Decomposition, chunked execution, persistence |
| Context Optimization Rules | Three-layer model, signal-to-noise, context budget |
| Bundle Evolution Guidance | Maintenance triggers table for generated project context instruction |
| Constitution Pattern | Structure, generation rules, Phase -1 gates |
| Spec-Driven Pipeline | 4-stage pipeline, templates, activation criteria |
| Separated Review Pipeline | 4-agent review, short-circuit, evidence standard |
| Handoffs Pattern | Frontmatter format, delegation rules |
| Evidence Standard | Labels, enforcement, flow |
| Bundle Evolution and Drift Detection | Ref to Bundle Evolution Guidance (same content) |
| Review Memory Promotion | Recurring findings → durable rules |
| Hooks Generation | Auto-format, lint, compile hooks |
| Generated File Marking | Marker placement rules |
| Cross-Session Persistence | Repo memory, session memory, progress format |

## Reference Assets

| Asset | Path | Purpose |
|-------|------|---------|
| Role catalog | `apple-role-catalog.md` | Default role names for generated agents |
| Primitive decision matrix | `primitive-decision-matrix.md` | Agent vs skill vs instruction vs prompt vs hook |
| Hook checklist | `hook-checklist.md` | 3-condition test before generating hooks |
| Copilot docs registry | `copilot-docs-registry.md` | Frontmatter allowlist, product behavior |
| Community skill registry | `community-skill-registry.md` | Swift community skills snapshot |
| Agent template | `agent-template.md` | Scaffold for generated agents |
| Skill template | `skill-template.md` | Scaffold for generated skills |
| Instruction template | `instruction-template.md` | Scaffold for generated instructions |
| Prompt template | `prompt-template.md` | Scaffold for generated prompts |
| Constitution template | `constitution-template.md` | Scaffold for generated constitutions |
| Spec / Plan / Tasks templates | `spec-template.md`, `plan-template.md`, `tasks-template.md` | Scaffolds for spec pipeline |
| Workflow asset template | `workflow-asset-template.md` | Scaffold for generated workflow assets |
| Audit rubric | `agent-audit-rubric.md` | Quick-reference checklist for auditor |
| Codebase analysis template | `apple-codebase-analysis-template.md` | Output structure for analyzer |

All template paths are relative to `.github/templates/agent-builder/`.

## Use Cases

- Create a new custom agent for Apple engineering or agile delivery
- Refactor or upgrade existing agent bundles
- Audit weak descriptions, frontmatter, or scopes
- Verify and improve an existing agent ecosystem
- Diagnose invocation failures for skills, instructions, prompts, or agents

## Apple Scope

iOS, iPadOS, macOS, visionOS, watchOS, and tvOS.

**Fallback defaults** (used only when the analyzer cannot determine the project's actual stack): Swift 6, strict concurrency, SwiftUI-first, UIKit/AppKit fallback when required, Swift Testing + XCTest UI tests.

**Alignment rule**: The analyzer's codebase findings always override these fallback defaults. If the project uses Swift 5.9, actor isolation only where explicitly adopted, UIKit-primary architecture, or XCTest without Swift Testing — generated agents must align to the project's actual technology profile, not the latest available.

## Operating Modes

**Discovery Mode** — requirements incomplete, overloaded, or inconsistent. Run adaptive interview until target workflow, scope, and quality bar are clear. Offer 2-3 architecture options when tradeoffs matter. Continue until confidence ≥ 95%.

**Fast Mode** — user has clear target and constraints. Confirm only missing facts that change the design. Move quickly into analysis → generation → auditing.

## Three Operating Flows

### Flow A: Greenfield — No agents exist
1. Clarify → 2. Analyze project → 3. Generate full bundle → 4. Audit → 5. Revise until PASS

### Flow B: Verify and Improve — Agents already exist
Triggered during Flow A when existing agents are detected, or invoked directly via `/generate-workflow-agents` when user wants to verify and improve an existing ecosystem.
1. Scan ecosystem → 2. Evaluate each agent → 3. Fix weak agents, fill gaps → 4. Audit → 5. Revise until PASS

### Flow C: Extend or Verify — Add new agent, or verify an existing one
Triggered via `/add-agent` prompt:
- **Extend (create)**: Clarify new workflow → Analyze project + existing agents → Generate new agent (no overlap) → Audit (ecosystem coherence) → Revise until PASS
- **Verify (single agent)**: Collect target files → Analyze ecosystem context → Evaluate against audit rubric → Fix findings → Re-audit until PASS

## Default Behavior

- Operating mode selection: see Operating Modes above
- If user chooses wrong primitive, offer 2-3 better options
- Generate files in English. Prefer portable designs unless user requests repo-locked.
- Multi-agent architecture when quality depends on distinct phases
- Hard audit gate for non-trivial bundles
- Do not declare `tools` or `mcp-servers` in frontmatter by default (keeps all tools accessible). Include explicit MCP tool preference guidance for agents that interact with external services.
- Align to project's actual technology profile — never assume latest defaults when codebase shows otherwise
- When invoked directly: confidence ≥ 95% before generation
- When invoked via prompt: skip confidence interview, analyze directly

## Single-Session Completion Rule

The entire bundle must be generated within a single continuous session. Never abandon the workflow or leave generation incomplete.

- **Start to finish in one session**: Once generation begins, continue through analyze → generate → audit → revise → deliver without stopping.
- **Structured clarification**: When user input is genuinely needed, use `vscode_askQuestions` with 2-4 options and a recommended default. This keeps the session alive. Never write questions as plain response text — that ends the session. For low-risk ambiguity, continue with an explicit provisional assumption.
- **Audit failures**: When the auditor returns `REVISE`, fix every finding and re-audit in the same session. When `BLOCKED`, ask the missing questions immediately, wait for answers, then resume.
- **Error recovery**: If a tool fails, try alternatives within the same session. Escalate to the user only when no automated recovery is possible.
- **Completion behavior**: After finishing all tasks, use `vscode_askQuestions` to ask the user whether additional updates are needed. Do not self-terminate — only end the session when the user explicitly decides to stop.

This rule applies to the kit itself and to generated orchestrator agents.

## Workflow

### Standard User-Facing Phases

1. Analyze the codebase
2. Assess the project and choose bundle architecture
3. Ask targeted follow-up only if needed (auto-skip when possible)
4. Generate or update the bundle
5. Audit and iterate until PASS
6. Deliver the final result

Internal setup work (reading skill files, loading templates, scanning existing files) stays inside these phases, not as extra top-level steps.

### Kit Reference Files

The kit maintains one persistent reference file read by the generator during generation:

- `.github/templates/agent-builder/copilot-docs-registry.md` — Copilot product behavior: frontmatter rules, primitives, tool behavior, hook behavior, instruction precedence. Updated by `Apple Copilot Docs Refresher` during kit maintenance. Authoritative input — does not need fetching each run.

Apple platform domain knowledge comes from the target project's codebase analysis (source files, config, tests, resources, entitlements, migration signals). When signal is thin, use cautious fallback assumptions and mark explicitly.

### Community Skill Discovery (Registry-Backed, MCP-Enriched)

During the analysis phase, the analyzer discovers community agent skills relevant to the target project's tech stack using a two-layer approach: a persistent registry snapshot as baseline, enriched with live data when MCP GitHub is available.

#### Kit Reference File

- `.github/templates/agent-builder/community-skill-registry.md` — Persistent snapshot of the `twostraws/Swift-Agent-Skills` directory with all categories, skill repos, content file paths, match criteria, and extracted knowledge summaries. Updated by `Apple Copilot Docs Refresher` during kit maintenance. The analyzer reads this as a reliable baseline that is always available regardless of MCP access.

#### Runtime Behavior

- **Timing**: After Technology Alignment Profile is determined, during analysis phase
- **Baseline**: Always read `community-skill-registry.md` first — full category listing and pre-extracted knowledge
- **Fallback chain**: MCP live + registry (best) → web fetch + registry (good) → registry only (acceptable). Never skip entirely.
- **Deep crawl**: When MCP GitHub available, read actual SKILL.md content files from matching sub-repos (not just directory README) to extract patterns, anti-patterns, deprecated API warnings, and edge cases
- **Output**: Community Skill Discovery Results section in analysis — discovery method, registry date, matched categories, deep-crawl status, extracted knowledge, per-agent-role recommendations
- **Generator consumption**: Embed specific knowledge in generated agents for matching tech stack + recommend users install community skills. Project-specific patterns override community guidance on conflict (note conflicts explicitly).
- **Staleness**: If snapshot >30 days old, note staleness so user can refresh before major generation

### 1. Clarify the Outcome

Collect only facts that materially change architecture: target users, tasks, inputs/outputs, domain, autonomy level, tool restrictions, quality bar, Apple platforms, framework constraints, delivery roles.

Clarification protocol:
- **Low-risk ambiguity**: Continue with an explicit provisional assumption.
- **High-risk ambiguity**: Use `vscode_askQuestions` per the Single-Session Completion Rule.
- Never stop the workflow entirely after asking a question.

### 2. Model the Workflow

Define: primary role, boundaries, non-goals, decision points, failure modes, artifacts. For Apple bundles: platform coverage, concurrency/lifecycle/testing expectations grounded in the project's actual technology profile from the analyzer — not kit fallback defaults.

### 3. Choose Primitives

Apply `.github/templates/agent-builder/primitive-decision-matrix.md`. Quick reference:

| Need | Primitive |
|------|-----------|
| Dedicated persona, context isolation | agent |
| Reusable repeatable workflow | skill |
| Always-on standards for matching files | instruction |
| Compact user-facing entry point | prompt |
| Deterministic enforcement | hook (validate with `hook-checklist.md` first) |

For linting tools: prefer instructions + agent validation steps over hooks. Add a hook only when: (1) team wants deterministic blocking, (2) tool reliably available everywhere, (3) false positives rare. See `hook-checklist.md`.

### 4. Build the Bundle

Use scaffold templates from `.github/templates/agent-builder/`:

| Artifact | Template |
|----------|----------|
| agent | `agent-template.md` |
| skill | `skill-template.md` |
| instruction | `instruction-template.md` |
| prompt | `prompt-template.md` |
| workflow asset | `workflow-asset-template.md` |
| constitution | `constitution-template.md` |
| spec / plan / tasks | `spec-template.md`, `plan-template.md`, `tasks-template.md` |

Pick roles from `apple-role-catalog.md`. Replace every `<...>` placeholder with project-grounded content.

**For `/generate-workflow-agents`, default to a full workflow kit:**
- `copilot-instructions.md` — workspace-level instructions automatically loaded by Copilot for all interactions. If the target project already has one, update it to integrate with the generated agent ecosystem while preserving existing relevant content. If the target project does not have one, create it. Content: concise project overview, technology stack, core conventions, agent ecosystem guide (available agents, primary prompt entry points, how to invoke), and cross-references to detailed instructions.
- Project context instruction (`<prefix>-project-context.instructions.md` with `applyTo: "**"`) for detailed project facts (architecture, domain glossary, extended conventions, bundle evolution guidance). Supplements `copilot-instructions.md` with depth that would be too verbose for the workspace-level file.
- Conductor + specialist agents with project-derived file prefix
- Multiple focused skills: delivery workflow (mandatory) + domain-specific (testing, investigation, review)
- Multiple narrow instructions: implementation conventions + test conventions at minimum
- Optional business-domain assets when project complexity warrants them (domain map, domain-scoped instructions, or a reusable business-rules workflow)
- At least 3 prompts: primary delivery + spec entry + secondary
- At least 2 templates/checklists for recurring hand-offs
- Explicit hook decision
- Bidirectional cross-references: agents reference skills, skills list their agents, templates are referenced by at least one file
- Intermediate working files deleted before finalizing
- Dirty worktree: preserve unrelated edits, stop only for direct path conflicts

**Naming rule**: Use a project-derived file prefix for generated files.

### 5. Validate Before Finalizing

Run `.github/templates/agent-builder/agent-audit-rubric.md`. Key checks:
- Cross-reference integrity (no orphaned templates or skills, bidirectional linking)
- Delivery workflow skill present
- `copilot-instructions.md` present (created or updated) with workspace-level content
- Project context instruction file present, no intermediate files left
- Frontmatter valid with discoverable descriptions
- Roles clear, goals explicit, output contracts defined
- Apple platform scope explicit

### 6. Audit and Revise

Send to auditor. If `REVISE`, patch every finding (major and minor) and re-audit. Do not accept or skip minor findings — all must be resolved before PASS. If `BLOCKED`, ask the missing questions. Repeat until PASS with zero open findings.

## Bundle Shapes

### Single: narrow single workflow
- 1 prompt + 1 agent or skill

### Focused: meaningful but focused workflow
- 1 agent + 1 skill + 1 prompt + optional instruction + 1 template

### Full Kit: Apple delivery workflows (default for `/generate-workflow-agents`)
- `copilot-instructions.md` — workspace-level instructions (created or updated)
- Project context instruction (`<prefix>-project-context.instructions.md`, `applyTo: "**"`) for detailed project facts
- Constitution (`<prefix>-constitution.md`) — immutable governance rules and Phase -1 gates
- Conductor + 9+ non-conductor agents (5 core delivery + 4 review pipeline)
- 5+ skills (delivery workflow + spec pipeline + domain-specific)
- 3+ instructions (implementation + testing + path-scoped)
- 3+ prompts (primary delivery + spec entry + secondary)
- 3+ templates for recurring hand-offs (including spec/plan/tasks)
- Explicit hook decision (SwiftLint/SwiftFormat auto-format, xcodebuild compile-check when warranted)
- Handoffs in frontmatter for all delegating agents
- Evidence standard embedded in agents + constitution
- Drift detection guidance in bundle evolution section
- Review memory promotion guidance in orchestrator

Full specification and minimums table in `apple-quality-auditor.agent.md`.

Every project receives the full bundle. Small projects benefit from the same agent capabilities as large ones — the agents adapt their behavior to context, but no agent roles, governance artifacts, or pipeline features are withheld based on project size.

## Artifact Requirements

### Agent
- Mission, use-when, non-goals, decision rules, output contract
- Collaboration model: inputs consumed, outputs produced, hand-off criteria, auto-return vs escalation
- **All agents**: use `vscode_askQuestions` for clarification (per Single-Session Completion Rule), anti-patterns list, structured output contract, explicit MCP tool preference for external services. Evidence standard: every business-rule claim backed by code/doc evidence, user confirmation, or labeled `[ASSUMPTION]` / `[NEEDS CLARIFICATION]`.
- **All agents with handoffs**: `handoffs:` in YAML frontmatter with label and prompt for each delegation target.
- **Implementor**: pre-impl checklist (trace flow, confirm rules, check duplication, scope files), incremental implementation (data → business → API), verify-fix loop (build → targeted tests → lint, max 3 retries). Lint `--strict` when configured. Use analyzer-detected simulator destination. Full test suite only when high-risk. Follow Large Task Execution Pattern for complex work. Phase -1 constitutional gates before implementation.
- **Code Review Orchestrator**: multi-stage pipeline with short-circuit. Stage 0: context gathering. Stage 1: Functional Review (BLOCKER → REJECT immediately). Stage 2: Technical Review. Stage 3 (conditional): Platform Review (Apple-specific, only for Swift/SwiftUI/UIKit files). Combined severity-driven verdicts.
- **Functional Reviewer**: business correctness only. AC ↔ Test ↔ Code traceability. Adversarial edge-case analysis. Evidence-backed findings with confidence level. BLOCKER stops pipeline.
- **Technical Reviewer**: technical quality only. API compatibility, migration safety, domain boundaries, NFR compliance, performance. Does NOT verify business requirements.
- **Platform Reviewer**: Apple-specific concerns. Memory management, UI thread safety, SwiftUI recomposition, concurrency correctness, accessibility, platform capabilities. Conditional trigger.
- **Investigator**: structured as-is/to-be analysis producing a **repository impact map**: file list with changes, real symbol names, dependency-ordered groups, human confirmation checkpoint. Output optimized for agent legibility (tables/lists, not prose).
- **Business-heavy bundles**: when business domain artifacts exist, BA/Investigator maintain them; Implementor/Reviewer consult before changing business logic.
- **Orchestrator**: intent-based auto-routing, confirmation checkpoint between investigation and implementation, micro-change lane, reviewer conflict resolution, inter-agent iteration loops (implement → test → review → repeat). Planning lane for complex tasks (>10 files, >3 modules, or migration): decompose → persist plan → `manage_todo_list` → sequential execution. Harness awareness: track recurring failures, suggest harness improvements. Context management: persist progress per phase, compact when large. Single-session completion rule: never abandon mid-workflow, use `vscode_askQuestions` for clarification (per Single-Session Completion Rule including completion behavior).

### YAML Frontmatter Generation
- `agents` field MUST use inline JSON-style array syntax with exact agent display names: `agents: ["Name A", "Name B"]` — NEVER use block list syntax (`- item`) and NEVER use filenames
- `description` field MUST be a double-quoted string with concrete trigger phrases
- `name` field MUST be an unquoted string matching the intended display name
- Prompt files MUST use `agent` field (not `mode`) for routing to a specific agent: `agent: "Agent Display Name"`
- Only emit frontmatter keys listed in the "Supported Frontmatter Keys" table in `copilot-docs-registry.md`. The allowlist is maintained during kit maintenance — never assume a key is valid without checking. Any unlisted key causes editor diagnostics and must not be emitted.
- Do not emit `tools` or `mcp-servers` unless explicitly requested
- All generated files in the same bundle MUST use identical YAML formatting conventions

### Skill
- Repeatable workflow with decision criteria and validation checks
- State which agents use it (bidirectional linking mandatory)
- Delivery workflow skill is always mandatory minimum for full kits
- Create domain-specific skills (testing, investigation, review) when they serve multiple agents
- Encode specific workflow steps, decision trees, and validation checklists — not generic advice

**Domain knowledge placement decision** — when the analyzer finds Apple domain knowledge for a technology area (SwiftUI, UIKit, persistence, concurrency, testing, accessibility, security, capabilities, etc.), place it as follows:

| Signal | Where to put the knowledge |
|--------|---------------------------|
| Domain is heavily used in the project AND multiple agents need it (e.g., implementor + reviewer both need SwiftUI patterns) | Create a dedicated domain skill |
| Domain is used in the project but only one agent needs it | Embed directly in that agent's instructions |
| Domain knowledge is a small set of conventions (< 10 rules) | Embed in the relevant instruction file (`applyTo` the matching path pattern) |
| Domain is lightly used or the project barely touches it | Skip — do not create a skill or bloat instructions for thin signal |
| Domain signal is thin or unknown | Prefer omission or an explicit uncertainty note over prescriptive guidance |

Do not generate one skill per detected Apple technology area. Create a domain skill only when it earns its place through multi-agent reuse and strong project signal from the analyzer.

### Business Knowledge Persistence
- Always capture the minimum shared business context in the project context instruction: domain glossary, key business rules, lifecycle states, and invariants.
- For projects with richer business complexity, choose the lightest primitive that preserves shared understanding:
	- project context instruction only: small apps or products whose business rules fit in a concise summary
	- domain-scoped instructions: business rules that map cleanly to specific paths or modules
	- reusable workflow asset or domain map: multiple domains, lifecycle-heavy workflows, or cross-domain dependencies that several agents must reference
	- business-domain skill: only when multiple agents reuse the same repeatable business-analysis workflow or interpretation process
- If a bundle includes a business domain registry, domain map, domain-scoped instructions, or a business-domain skill, Business Analyst, Investigator, Implementor, Code Reviewer, and Dev Orchestrator must reference it explicitly in their collaboration inputs or decision rules.
- Do not generate a dedicated business-domain artifact when the project's business context fits cleanly in the project context instruction and the normal planning/investigation assets.
- Do not add a dedicated kit subagent for business-domain modeling by default. The analyzer extracts business context, and the generator decides how to persist it. Add an extra specialization only when business-domain synthesis becomes a distinct workflow with materially different failure modes.

### Instruction
- Narrow `applyTo` scope, single convention domain
- Separate files for distinct domains (implementation, testing, UI, data layer)
- Avoid duplicating the entire skill body

### Prompt
- Short, discoverable, route to the right agent
- At least 2: primary delivery + secondary entry point
- Make the default workflow lane obvious
- Frontmatter MUST use `agent` field (not `mode`) for routing to a specific agent

### Hook
- Only when deterministic enforcement is truly needed and safe
- Validate against `hook-checklist.md` first

## Generation Principles

Non-negotiable principles every generated agent must encode. These are the behavioral floor for all generated agents, regardless of role.

1. **Understand before changing** — Trace existing code paths, data flow, and callers before modifying anything. Never assume; verify.
2. **Confirm business logic** — Identify business rules before writing code. Ask when rules are ambiguous, not after the implementation is wrong.
3. **No duplicate validation across layers** — Check for existing validation before adding new checks. Each rule enforced in exactly one layer.
4. **Respect module boundaries** — Do not reach across architectural boundaries. Use established interfaces and dependency patterns.
5. **Clarify before acting on ambiguity** — When intent or requirements are unclear, use `vscode_askQuestions` per the Single-Session Completion Rule. Never guess silently.
6. **Verify before claiming completion** — Run the project's actual build, test, and lint commands. Do not claim success without evidence.
7. **Prefer simplicity** — Choose the simplest correct solution. Avoid premature abstraction, unnecessary indirection, or speculative generalization.
8. **Explain decisions and report outcomes** — State what was done, why, and what changed. Include evidence of verification in completion reports.

The generator must embed these principles in every generated agent's instructions. The auditor must verify their presence.

## Harness Engineering Alignment

Generated agents must follow harness engineering principles — designing the environment for reliable execution.

### Control Types

| Type | Role | Examples |
|------|------|---------|
| **Feedforward (Guides)** | Context before action to increase correct first output | Architecture docs, coding conventions, implementation notes with file paths |
| **Feedback (Sensors)** | Checks after action to enable self-correction | Build commands, test suites, linters, AI code review |

Within each: **Computational** (deterministic, fast — linters, type checkers, tests) vs **Inferential** (semantic, non-deterministic — AI review, LLM-as-judge).

### Key Patterns
- **Repository impact map**: Investigator output grounded in actual code — real file paths, symbol names, dependency-ordered change groups. Human checkpoint before implementation.
- **Execution plan persistence**: Complex work persists plans to session memory. Plans include goal, phases, status, decisions, blockers. Read at each phase start.
- **Agent legibility**: Inter-agent outputs use structured formats (tables, lists) over prose. Consistent parseable hand-off formats.
- **Steering loop**: Recurring issues → fix the harness (instructions, conventions, linter rules), not just individual outputs. Orchestrator tracks and flags.

## Large Task Execution Pattern

For complex, multi-step tasks (large migrations, major refactors, cross-module changes), generated agents must follow this pattern:

### 1. Decomposition
- Break into ordered phases based on dependency analysis, each independently verifiable (build + tests pass)
- Identify dependencies between phases and estimate scope (files, modules, risk)

### 2. Execution
- Execute one phase at a time — never the entire task in a single pass
- After each phase: validate (build → test → lint), update plan status, compact context if needed
- If a phase fails, fix within that phase before proceeding

### 3. Context Persistence
- **When**: >5 files, >3 modules, >3 steps, >20 changes, or non-obvious decisions
- **How**: Session memory for task notes, `manage_todo_list` for progress, one file per concern
- **Compaction**: Summarize completed phases into structured notes. Read progress notes at phase start.
- Cross-session (>50 files, >5 modules): repo memory or project files for durable state

### 4. Completion
- Full build + full test suite + lint
- Structured report: phases, files changed per phase, validation evidence, remaining risks
- Clean up intermediate session memory files

## Context Optimization Rules

Rules for efficient context usage in generated agents and artifacts.

### Signal-to-Noise Discipline
- Generated agents produce concise, phase-bounded outputs — not restate upstream context
- Hand-offs between agents prefer delta summaries with file and line references over repeated full-context prose
- Static rules belong in instructions and skills (loaded once), not duplicated across every agent's instructions

### Three-Layer Context Model
Generated bundles distribute context efficiently across three layers (plus a workspace-level foundation):

**Foundation**: `copilot-instructions.md` — Workspace-level instructions automatically loaded by Copilot for all interactions. Concise project overview, technology stack, core conventions, agent ecosystem guide (available agents, prompt entry points, how to invoke). Target 40-80 lines. This is the entry point for anyone using Copilot in the project.

1. **Project context instruction** (`<prefix>-project-context.instructions.md`, `applyTo: "**"`) — Detailed project facts: architecture, extended conventions, domain glossary, bundle evolution guidance. Supplements `copilot-instructions.md` with depth. Keep concise but thorough.
2. **Path-scoped instructions** — Narrow, file-pattern-scoped rules. Loaded only when matching files are active. Keep single-purpose.
3. **Agent instructions** — Role-specific workflows, decision rules, and output contracts. Loaded only when the agent is invoked. Do not repeat what instructions or skills already cover.

Do not duplicate content between `copilot-instructions.md` and the project context instruction — the workspace-level file is the brief overview and agent guide, the project context instruction is the deep reference.

### Context Budget Guidance for Generated Project Context Instruction
- Target length: 80-150 lines for typical projects. Exceed only when genuine complexity demands it.
- Include: project overview, architecture summary, technology stack, key conventions, domain glossary, quality expectations.
- Exclude: role-specific workflows (belongs in agents), file-pattern rules (belongs in path-scoped instructions), repeatable processes (belongs in skills).
- Every line must earn its place — if a fact only matters for one role, put it in that agent's instructions instead.

## Bundle Evolution Guidance

The generated project context instruction must include a brief maintenance guidance section. The generator must include this in every generated project context instruction. Content:

| Trigger | Action |
|---------|--------|
| Architecture changes, framework migrations, consistently wrong outputs | Update affected agents |
| Recurring agent corrections (≥3 same issue) | Extract into instruction (`applyTo` scoped) — this is the **steering loop** |
| New convention for specific file patterns | Add path-scoped instruction |
| Instruction violated repeatedly despite documentation | Promote to mechanical enforcement (linter, structural test, hook) |
| Agents reference removed files, deprecated APIs, abandoned conventions | Drift — update affected agents. Check after major refactors, dependency upgrades, quarterly. |
| Growing duplication, inconsistent naming, boundary violations | Entropy — improve feedforward controls |

## Constitution Pattern

Generated bundles must include a `<prefix>-constitution.md` instruction file (`applyTo: "**"`) that defines immutable governance rules for the project. The constitution is the highest-authority document in the generated bundle — it overrides any agent-specific instruction when they conflict.

### Structure

| Article | Content |
|---------|---------|
| Preamble | Bundle identity and purpose |
| I: Scope & Boundaries | Coverage and exclusions |
| II: Evidence Standard | Code/doc evidence, `[ASSUMPTION]`/`[NEEDS CLARIFICATION]` labels |
| III: Review Pipeline | Multi-stage review, short-circuit, verdict authority |
| IV: Change Governance | Blast-radius assessment, mandatory checkpoints |
| V: Specification Discipline | Spec-driven pipeline requirements |
| VI: Context Persistence | Session memory, progress tracking |
| VII: Escalation | When/how to escalate to human |
| Phase -1 Gates | **Simplicity** (simplest approach?), **Duplication** (reuse existing?), **Business Logic** (rules verified?), **Impact** (blast radius acceptable?) |

### Generation Rules
- The generator produces the constitution from project analysis — not a generic template
- Constitution articles reference actual project conventions, not placeholder guidance
- The constitution is an instruction file, not an agent — it has no workflow, just rules
- All generated agents must include a note acknowledging the constitution
- The auditor must verify constitution presence and that agents reference it

## Spec-Driven Pipeline

Generated bundles must include a spec-driven pipeline that normalizes feature work through structured specification before implementation begins.

### Pipeline Stages

| Stage | Input → Output | Key Sections |
|-------|---------------|--------------|
| 1. Refine User Input | Raw request → structured goal/anchor/constraints | Completeness check, ambiguity resolution, AC extraction |
| 2. Specify Feature | Structured goal → `specs/<id>/spec.md` | Problem, Scope/Non-Goals, AC (testable), Domain Rules, Edge Cases, Dependencies, Constraints |
| 3. Plan Implementation | Spec → `specs/<id>/plan.md` | Architecture Approach, File Changes (dependency-ordered), Risk, Test Strategy, Rollback |
| 4. Generate Tasks | Plan → `specs/<id>/tasks.md` | Per-task: description, files, validation, complexity, dependencies. Feed into `manage_todo_list` |

### Spec Workspace
Feature specs live in `specs/<feature-id>/` (`spec.md`, `plan.md`, `tasks.md`). Living documents — updated as implementation reveals constraints. Archive or delete after merge.

### When to Activate
- **Always**: >3 files, cross-module, business logic changes, shared/core code
- **Skip**: trivial changes (typos, config, single-file fixes)
- Orchestrator decides based on complexity assessment

### Generated Assets
Skills: Refine-User-Input, Specify-Feature, Plan-Implementation, Generate-Tasks. Templates: `spec-template.md`, `plan-template.md`, `tasks-template.md`.

### Template Cross-Reference Requirements

Generated spec pipeline templates are useless unless the skills that produce specs/plans/tasks reference them by path. The generator must wire:

- Specify-Feature skill must reference `.github/templates/<prefix>/spec-template.md` as its output structure
- Plan-Implementation skill must reference `.github/templates/<prefix>/plan-template.md` as its output structure
- Generate-Tasks skill must reference `.github/templates/<prefix>/tasks-template.md` as its output structure
- Investigation skill (if it has a report template) must reference `.github/templates/<prefix>/investigation-report-template.md`
- At minimum, each generated template must have ≥1 inbound reference from a skill or agent

## Separated Review Pipeline

Generated bundles must include a multi-stage review pipeline replacing the single Code Reviewer.

### Pipeline Structure

| Stage | Agent | Focus | Short-Circuit |
|-------|-------|-------|---------------|
| 0 | Code Review Orchestrator | Context gathering, route to reviewers | — |
| 1 | Functional Reviewer | Business correctness, AC traceability | BLOCKER → REJECT immediately |
| 2 | Technical Reviewer | Architecture, performance, security | — |
| 3 | Platform Reviewer (conditional) | Apple-specific: memory, concurrency, SwiftUI | Only when Swift/SwiftUI/UIKit files changed |

### Short-Circuit Rule
The Functional Reviewer runs first. If any **BLOCKER** severity finding is raised (broken business logic, AC violation, data integrity issue), the review pipeline **REJECT**s immediately — Technical and Platform reviews do not run. This prevents wasting review cycles on code that is fundamentally wrong from a business perspective.

### Evidence Standard in Reviews
Every finding requires: code anchor (file + line), evidence type (per Evidence Standard section), severity (blocker/major/minor/suggestion), and concrete fix suggestion.

### When to Generate Separated Review
- Always generate the full 4-agent pipeline (Code Review Orchestrator + Functional Reviewer + Technical Reviewer + Platform Reviewer)
- Platform Reviewer is conditionally triggered — only runs when changed files include Swift/SwiftUI/UIKit code

## Handoffs Pattern

Generated agents must declare explicit delegation targets in YAML frontmatter using the `handoffs` field. This replaces implicit delegation through prose instructions and enables Copilot to offer delegation buttons in the UI.

### Frontmatter Format
```yaml
handoffs:
  - agent: "Test Specialist"
    label: "Generate Tests"
    prompt: "Generate unit tests for the implementation I just completed"
  - agent: "Code Review Orchestrator"
    label: "Review Changes"
    prompt: "Review the changes I made for business correctness and technical quality"
```

### Rules
- Every agent that delegates to other agents MUST declare handoffs
- Orchestrators have handoffs to all agents they can route to
- Specialist agents have handoffs back to the orchestrator (for escalation/completion)
- Handoff prompts must be specific enough to provide context for the receiving agent
- `label` is the user-facing button text — keep it short and action-oriented
- `agent` must be the exact display name (same as used in `agents` frontmatter)
- Handoffs supplement `agents` frontmatter — both must be present

## Evidence Standard

| Label | Meaning |
|-------|---------|
| (no label) | Code/doc-backed (default) |
| `[USER-CONFIRMED]` | User explicitly confirmed |
| `[ASSUMPTION]` | Reasonable inference, not verified |
| `[NEEDS CLARIFICATION]` | Cannot determine — must ask or investigate |

Enforcement: Investigators mark uncertain findings as `[ASSUMPTION]`. Implementors verify before coding. Reviewers challenge unverified assumptions. Orchestrators track resolution. The constitution Article II codifies this for the project.

## Bundle Evolution and Drift Detection

See Bundle Evolution Guidance above. The same table content applies to both the generated project context instruction and the kit's own drift detection checks.

## Review Memory Promotion

Recurring review findings (≥3 same issue type) trigger promotion to durable rules:

1. Draft instruction-level rule or checklist item
2. Validate: actionable, specific, not already covered
3. Promote: convention violations → path-scoped instruction; test gaps → testing instruction; boundary violations → project context instruction
4. If violations persist after promotion → escalate to mechanical enforcement (linter, hook)

## Hooks Generation

| Hook | Trigger | Tool | When |
|------|---------|------|------|
| Auto-format | `postToolUse` (file edit) | SwiftFormat | `.swiftformat` or Package.swift dependency detected |
| Lint check | `postToolUse` (file edit) | SwiftLint | `.swiftlint.yml` present |
| Compile check | `postToolUse` (file edit) | `xcodebuild build` | Xcode project, compile-on-save beneficial |

Rules: only when tool is already configured, deterministic (no false positives), compile hooks use analyzer-detected scheme/destination. Document recommendation when not generating.

## Generated File Marking

Every generated file includes `<!-- Generated by Apple Agent Builder Kit -->` immediately after the YAML frontmatter closing `---`. Never before frontmatter (breaks YAML). Preserved during updates.

**Scope**: Files generated for target consumer projects only. Kit's own internal files (this repository's `.github/` content) are excluded.

## Cross-Session Persistence

For tasks exceeding a single session (~50+ files, 5+ modules, multi-phase migrations): use repo memory or project files (`specs/<task-id>/progress.md`) for durable state. Session memory is within-session only. End each session with structured progress: completed phases, status, remaining, decisions, blockers.
- Start each session: read progress to re-ground context