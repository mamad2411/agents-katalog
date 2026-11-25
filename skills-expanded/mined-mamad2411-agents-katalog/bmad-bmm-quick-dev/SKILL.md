---
name: bmad-bmm-quick-dev
description: >-
  Use this skill to implement small features or changes from a Quick Tech Spec
  file or direct user instructions, with autonomous execution followed by self-
  check and adversarial review. Invoke when the user says "implement this quick
  spec", "proceed with implementation of [spec]", or gives direct
  implementation instructions without a formal story. The skill determines
  execution mode (spec-file vs. direct instruction), gathers minimal context if
  needed, executes all tasks, runs a self-audit against acceptance criteria and
  patterns, invokes an adversarial review, and resolves findings interactively
  before finalizing. Input is a tech-spec file path or direct task description.
  Output is completed, tested code with resolved review findings. Unlike bmad-
  bmm-quick-dev-new-preview (which also handles planning/spec generation), this
  skill assumes a spec is already available or instructions are clear. Do not
  use for large multi-story features — use the full BMAD story workflow instead.
argument-hint: "Provide a path to a tech-spec file or direct task instructions."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Quick Dev

Implement a Quick Tech Spec for small changes or features.

## Outcome

Efficient implementation of tasks — either from a tech-spec or direct user instructions — through autonomous execution, self-check, adversarial review, and interactive finding resolution.

## Your Role

Elite full-stack developer executing tasks autonomously. Follow patterns, ship code, run tests. Every response moves the project forward. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- Read the entire step file before acting.
- Halt at checkpoints and wait for user input before proceeding.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`user_name`, `communication_language`, `user_skill_level`, `planning_artifacts`, `implementation_artifacts`, etc.).
2. Resolve:
   - `date` as system-generated current datetime
   - `project_context` = `**/project-context.md` (load if exists)

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Mode Detection](./steps/mode-detection.md) — Determine execution mode (tech-spec vs direct), handle escalation, set state variables
2. [Context Gathering](./steps/context-gathering.md) — Quick context gathering for direct mode (skipped for tech-spec mode)
3. [Execute](./steps/execute.md) — Implement all tasks, write code, run tests
4. [Self Check](./steps/self-check.md) — Audit implementation against tasks, tests, AC, and patterns
5. [Adversarial Review](./steps/adversarial-review.md) — Construct diff and invoke adversarial review skill
6. [Resolve Findings](./steps/resolve-findings.md) — Handle review findings interactively, apply fixes, finalize

## Halt Conditions

- HALT if no tech-spec file is provided and the user cannot provide direct implementation instructions after prompting — there is nothing to implement
- HALT if a provided tech-spec file path does not exist or is unreadable
- HALT if `bmad-core-config` fails and no `implementation_artifacts` or `planning_artifacts` path can be resolved
- HALT if adversarial review reveals critical findings (e.g., security vulnerabilities, broken core functionality) that the user refuses to address

## External Skill Dependencies

- `bmad-bmm-quick-spec` — Invoked if user chooses to plan first via quick-spec
- `bmad-core-advanced-elicitation` — Deep questioning and multi-perspective analysis
- `bmad-core-party-mode` — Collaborative brainstorming and ideation
- `bmad-core-review-adversarial-general` — Blind adversarial code review

## When to Use

Use this skill when:
- The user provides a quick tech spec and says "implement this quick spec" or "proceed with implementation of [quick tech spec]"
- The user gives direct implementation instructions without a formal spec
- A Quick Tech Spec file exists and is ready for autonomous implementation with adversarial self-review

## Boundaries

This skill should NOT:
- Be used for large multi-story features — it is for small, bounded changes; escalate to the full BMAD story workflow for anything requiring multiple stories
- Skip the self-check and adversarial review steps — implementation must be validated against tasks, acceptance criteria, and patterns before finalizing
- Escalate to the full BMAD story workflow automatically — only redirect the user to the PRD/story workflow if the user actively chooses it after being shown the option
- Proceed past checkpoints without halting to wait for user input
- Finalize code when the adversarial review surfaces unresolved critical findings — those must be addressed or explicitly accepted by the user before the workflow closes

