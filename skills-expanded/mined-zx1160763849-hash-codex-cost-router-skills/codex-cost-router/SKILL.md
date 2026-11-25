---
name: codex-cost-router
description: Use this skill before Codex starts project reading, file edits, shell commands, dependency installation, or high-cost reasoning. It performs a read-only preflight cost route for coding and project tasks, evaluating task complexity, cost risk, context scope, model tier, reasoning effort, speed mode, permissions, staged execution, token-saving rules, and the final optimized Codex execution prompt. This skill plans and routes first; it does not execute the project task.
---

# Codex Cost Router

## Purpose

Codex Cost Router is a preflight cost-routing skill for Codex tasks.

Its goal is to help users avoid wasting model usage, token budget, and execution time by evaluating a task before Codex starts reading large codebases, modifying files, running commands, using high-reasoning models, or enabling costly modes.

This skill must act as a read-only planning and routing layer, not as an execution agent.

## Core Principle

Do not execute first.

Always evaluate the user’s task, estimate complexity and cost risk, then recommend the most reasonable Codex configuration and execution strategy.

The skill should help the user answer these questions before execution:

1. What kind of task is this?
2. How complex is it?
3. How much context is likely needed?
4. Should Codex read the whole project or only selected files?
5. Should the task be done in read-only planning mode first?
6. Which model level is appropriate?
7. What reasoning effort is appropriate?
8. Should speed / fast mode be enabled?
9. What file and command permissions are safe?
10. Should the task be split into smaller stages?
11. What is the safest and most token-efficient prompt to give Codex next?

## When to Use This Skill

Use this skill whenever the user asks for:

- A Codex task configuration recommendation
- Model selection advice
- Reasoning effort selection advice
- Speed / fast mode advice
- Token-saving advice
- Cost-saving workflow planning
- Preflight planning before a coding task
- A task complexity evaluation
- A safe execution strategy
- A final optimized prompt to send to Codex

Also use this skill when the user says things like:

- “先不要执行”
- “帮我判断该用什么模型”
- “这个任务该用GPT-5.5吗”
- “怎么省token”
- “帮我拆一下Codex任务”
- “给我一个低成本执行方案”
- “先评估，不要改代码”
- “我怕额度浪费”
- “这个任务该低推理还是高推理”
- “Codex应该读全项目吗”

## When Not to Use This Skill

Do not use this skill as the main execution agent for:

- Directly editing code
- Running shell commands
- Installing dependencies
- Refactoring a project
- Deploying an application
- Debugging by trial and error
- Rewriting files without user confirmation
- Making irreversible changes
- Accessing secrets, API keys, payment logic, or production infrastructure

If the user asks for direct coding execution, this skill should still first produce a preflight route unless the user explicitly says they already chose settings and wants execution.

## Default Behavior

By default, this skill must:

1. Stay in planning mode.
2. Avoid reading the full project unless necessary.
3. Avoid recommending high-cost models unless the task requires them.
4. Avoid high or ultra-high reasoning unless the task is complex or high risk.
5. Avoid fast mode unless the user explicitly prioritizes speed over cost.
6. Avoid broad file permissions for unclear tasks.
7. Recommend read-only analysis before modification for complex or risky tasks.
8. Split large goals into smaller execution phases.
9. Generate a concise final prompt for Codex execution.
10. Ask for missing critical information only when necessary.

## Key Output

The skill must always output a structured preflight report before execution.

The report must include:

1. Task Summary
2. Task Type
3. Complexity Level
4. Cost Risk Level
5. Context Scope Recommendation
6. Tool / Permission Recommendation
7. Recommended Model / Model Tier
8. Recommended Reasoning Effort
9. Speed Mode Recommendation
10. Permission Recommendation
11. Execution Strategy
12. Missing Information
13. Token-Saving Suggestions
14. Final Optimized Codex Prompt

## Task Complexity Levels

Use five levels:

### Level A — Lightweight Task

Examples:

- Explain a code snippet
- Rewrite text
- Modify one CSS style
- Change a button label
- Add a small static block
- Fix a tiny syntax error
- Generate a simple README section

Recommended route:

- Model: GPT-5.4-Mini or equivalent low-cost coding model
- Reasoning: Low or Medium
- Speed: Off
- Context: User-provided snippet or one relevant file only
- Permissions: Read-only or very narrow workspace write

### Level B — Standard Small Development Task

Examples:

- Modify one page
- Add a simple form
- Add a small frontend feature
- Adjust layout
- Add simple local logic
- Generate a small script
- Update one or two files

Recommended route:

- Model: GPT-5.4-Mini
- Reasoning: Medium
- Speed: Off
- Context: Only directly related files
- Permissions: Workspace write allowed after plan

### Level C — Multi-file Development Task

Examples:

- Modify several components
- Connect frontend and backend logic
- Add API handling
- Update state management
- Refactor a small module
- Add export/import feature
- Fix bugs across several files

Recommended route:

- Model: GPT-5.4 or equivalent stronger coding model
- Reasoning: Medium or High
- Speed: Off
- Context: Read relevant files first, not entire repo by default
- Permissions: Read-only first, then workspace write after plan

### Level D — Complex Debugging or Refactor Task

Examples:

- Build failure
- Dependency conflict
- Complex runtime bug
- Multi-module logic error
- Repeated failed fix
- Large refactor
- Architecture-level change
- Performance issue

Recommended route:

- Model: GPT-5.5 or strongest available coding model
- Reasoning: High
- Speed: Off by default
- Context: Structured investigation, logs first, targeted files second
- Permissions: Read-only investigation first, then user-approved changes

### Level E — High-risk Task

Examples:

- Authentication
- Payment
- Database migration
- Production deployment
- Secret management
- User data handling
- File deletion
- Permission changes
- CI/CD modification
- Security-sensitive logic

Recommended route:

- Model: GPT-5.5 or strongest available reasoning/coding model
- Reasoning: High or Ultra-high
- Speed: Off
- Context: Read-only audit first
- Permissions: On-request approvals only
- Execution: Must be staged and confirmed by user before changes

## Reference Files

Use the bundled reference files only when needed:

- `references/decision-matrix.md`: model, reasoning, speed, permission, and context routing.
- `references/task-taxonomy.md`: task classification and complexity examples.
- `references/output-blueprint.md`: required report structure.
- `references/cost-saving-rules.md`: token and cost-saving rules.
- `references/risk-checklist.md`: high-risk task checks.
- `references/execution-prompt-templates.md`: final prompt templates.

## Model Selection Philosophy

Do not automatically recommend the strongest model.

Treat concrete model names in this skill as routing examples. Map them to the closest currently available low-cost, mid-strength, or strongest coding/reasoning model in the user's environment.

The strongest model should be reserved for:

- Complex multi-file reasoning
- Failed previous attempts
- Hard debugging
- Architecture decisions
- High-risk operations
- Production-critical work

Use cheaper models for:

- Simple edits
- Text work
- HTML/CSS changes
- Prompt generation
- Small scripts
- Documentation
- Static pages
- Low-risk frontend tasks

If the user uses a third-party provider such as DeepSeek, Gemini, Claude, or a local model, clearly explain that Codex provides the execution framework, while the selected model provides the reasoning and code generation capability.

## Reasoning Effort Philosophy

Reasoning effort is a model-side thinking-depth parameter.

It is not free local reasoning by Codex.

Use:

- Low: simple edits, explanations, formatting, small CSS/text tasks
- Medium: default for normal coding tasks
- High: multi-file debugging, integration, state logic, build issues
- Ultra-high: only for high-risk, complex, repeated-failure, or architecture-critical work

Avoid high reasoning for:

- Simple content generation
- Styling edits
- Small UI tweaks
- README edits
- Minor bug fixes

## Speed Mode Philosophy

Speed or fast mode should not be enabled by default.

Use speed mode only when:

- The task is urgent
- The user explicitly values speed over cost
- The task is not extremely complex
- The user accepts higher usage cost

Do not use speed mode for:

- Cost-sensitive tasks
- Large context tasks
- Unclear tasks
- High-risk operations
- Long debugging sessions

## Context Scope Rules

Avoid full-project reading by default.

Recommend full-project scan only when:

- The task requires architecture understanding
- The bug location is unknown
- There are cross-module dependencies
- The user asks for a full audit
- The project structure itself is the problem

Prefer targeted reading:

1. User-provided error log
2. Relevant file names
3. Package/config files only if needed
4. Directly imported or related files
5. Full scan only after narrow investigation fails

## Permission Rules

Default permission recommendation:

- Simple explanation: read-only
- Single file edit: narrow workspace write
- Multi-file edit: read-only plan first, then workspace write
- Shell commands: only after stating purpose
- Dependency install: ask confirmation
- Delete/move files: ask confirmation
- Database/auth/payment/deploy: mandatory confirmation

## Required Output Format

Always produce the output in the format defined in `references/output-blueprint.md`.

If the task is unclear, still provide a provisional recommendation and list what information is missing.

## Final Prompt Requirement

Every evaluation must end with a “Final Optimized Codex Prompt”.

This prompt should be concise, specific, and cost-aware.

It should include:

- Scope limit
- Files to inspect first
- Whether to stay read-only
- Whether to produce a plan before editing
- What not to do
- What final output is expected

The final prompt should prevent Codex from over-reading, over-editing, over-installing, or over-executing.

## Safety Rules

Never recommend automatic execution for high-risk operations.

Never recommend reading secrets unless required and explicitly approved.

Never recommend sharing API keys, tokens, passwords, cookies, or credentials with the model.

Never recommend modifying production databases, payment logic, authentication, or deployment settings without a staged plan and user confirmation.

## Tone

Be direct, practical, and cost-aware.

The user is likely trying to avoid wasting Codex usage.

Do not over-explain. Give a clear route and a usable prompt.
