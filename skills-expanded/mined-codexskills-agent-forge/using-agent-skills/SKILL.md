# Using Agent Skills

## Description
Meta-skill that governs how all other skills are discovered and invoked. Use when starting a session or when you need to discover which skill applies to the current task.

## Purpose

This meta-skill is the entry point for the agent-forge system. It tells agents how to:
1. Discover which skills exist in the project
2. Determine which skill to use for a given task
3. Resolve conflicts when multiple skills could apply
4. Initialize a session with the right context
5. Follow shared operating rules across all skills

## Skill Discovery

### Discovery Order
When an agent starts a session, it should:
1. Scan `skills/` directory for all `SKILL.md` files
2. Read each skill's description field to understand its purpose
3. Build a mental map of available capabilities
4. Trigger the correct skill(s) for the current task

### Directory Structure
```
skills/
  ci-cd-and-automation/
    SKILL.md
  deprecation-and-migration/
    SKILL.md
  documentation-and-adrs/
    SKILL.md
  shipping-and-launch/
    SKILL.md
  using-agent-skills/          ← this skill
    SKILL.md
```

### Skill Metadata
Each SKILL.md must include:
- **Description**: One-paragraph summary of when to use this skill
- **Core Philosophy**: The guiding principle behind the skill's approach
- **Principles**: Key rules and patterns the skill enforces
- **Usage**: How to invoke the skill in practice

### Trigger Keywords
Skills should define trigger keywords in their descriptions. For example:
- CI/CD: "set up CI", "pipeline", "GitHub Actions", "deploy", "quality gate"
- Deprecation: "deprecate", "migrate", "sunset", "remove", "backward compat"
- Documentation: "ADR", "documentation", "doc review", "API docs"
- Shipping: "launch", "release", "rollout", "rollback", "deploy to production"

## Shared Operating Rules

These rules apply to ALL skills in the agent-forge system:

### Rule 1: Prefer Existing Patterns
Before writing new code, search the codebase for existing patterns. Match style, conventions, and idioms. Do not introduce new frameworks or patterns without an ADR.

### Rule 2: Write Tests
Every code change must include tests. Test behavior, not implementation. Follow the project's testing patterns (see `references/testing-patterns.md`).

### Rule 3: Document Decisions
Significant decisions must be recorded as ADRs (see `documentation-and-adrs` skill). If a decision is hard to reverse, write an ADR.

### Rule 4: Ship Safely
Use feature flags for risky changes. Follow the staged rollout process (see `shipping-and-launch` skill). Always have a rollback plan.

### Rule 5: Delete Code
Code is liability. Remove dead code, commented-out code, and unnecessary abstractions. See `deprecation-and-migration` for structured removal.

### Rule 6: Review Before Merge
Every change must be reviewed. Use the `code-reviewer` agent persona for structured reviews. No blind merges.

### Rule 7: Fail Fast
Prefer early failure over silent errors. Add assertions, validate inputs, and crash on invalid states.

### Rule 8: No Guessing
If you don't know something, search the codebase, check documentation, or ask. Do not fabricate APIs, functions, or behaviors.

## Conflict Resolution

When multiple skills could apply to a task, resolve conflicts in this order:

### Priority Matrix
1. **Safety** (shipping-and-launch, security references)
2. **Correctness** (test-driven-development, code-reviewer)
3. **Clarity** (documentation-and-adrs, code-simplification)
4. **Performance** (performance-optimization, performance-checklist)
5. **Velocity** (ci-cd-and-automation, incremental-implementation)

### Resolution Process
1. Identify all skills relevant to the task
2. Check for direct conflicts (e.g., "add more code" vs "delete code")
3. Apply the priority matrix: safety > correctness > clarity > performance > velocity
4. If still ambiguous, ask the user for clarification
5. Document the resolution in comments or ADR

### Handling Overlapping Skills
- When skills overlap (e.g., both `test-driven-development` and `incremental-implementation` apply), apply both
- Use the higher-priority skill's constraints first
- Combine principles where they don't conflict
- Flag contradictions to the user

## Session Initialization

### New Project Setup
1. Scan for existing `agent-forge/` structure
2. Check which skills are present
3. Read the project README and setup guide
4. Initialize with context: project type, language, frameworks
5. Load all applicable skills

### Existing Project Work
1. Read any active ADRs for recent decisions
2. Check `.claude/commands/` for project-specific commands
3. Load the skill(s) matching the user's request
4. Apply shared operating rules
5. Begin work with the first applicable principle

### Resetting Context
When switching between unrelated tasks:
1. Unload current skill context
2. Clear any task-specific state
3. Load skills for the new task
4. Verify the new task's constraints

## Skill Development Guidelines

### Creating a New Skill
1. Create a directory under `skills/` with a descriptive name
2. Write `SKILL.md` with all required sections:
   - Description (one paragraph)
   - Core Philosophy (one sentence)
   - Principles (numbered list with explanations)
   - Usage (how to invoke)
3. Add trigger keywords to the description
4. Test the skill by running through a scenario
5. Add references if needed in `references/`

### Skill Quality Standards
- Minimum 150 lines of substantive content
- Real, actionable guidance (not generic advice)
- Code examples where applicable
- Templates for common tasks
- Clear scope definition

### Skill Versioning
Skills are versioned by directory name:
```
skills/
  ci-cd-and-automation/     ← current version
  ci-cd-and-automation-v1/  ← archived version
```

Breaking changes to a skill should create a new version directory.

## Usage
Load this meta-skill at the start of every session. Use it to discover available skills, apply shared operating rules, resolve conflicts between skills, and initialize proper context for the task at hand.
