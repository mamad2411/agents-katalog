---
name: brainstorm
description: Turn ideas into validated design specs through collaborative dialogue before implementation. Use when facing complex tasks with design decisions, multiple valid approaches, or multi-file changes.
allowed-tools: Read LS Grep Bash TodoWrite TodoRead Ask Write Skill
---

# Brainstorm

Help turn ideas into fully formed designs through natural collaborative dialogue.

## Hard Gate

Do NOT write any implementation code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY task regardless of perceived simplicity.

## Process

You MUST follow these steps in order. Use `TodoWrite` to create a checklist from these steps and track your progress.

### Step 1: Explore Project Context

Before asking questions, understand the current state:
- Read relevant files (`Read`), check current working directory structure (`LS`)
- Search for related code or topics: `Grep`
- Look for existing docs, README, CLAUDE.md, AGENT.md or design files

### Step 2: Ask Clarifying Questions

Ask questions **one at a time**. Do not batch multiple questions.

- Prefer multiple choice when possible — easier to answer than open-ended
- Focus on understanding: purpose, constraints, success criteria
- If the project is too large for a single spec, help decompose into sub-projects first

### Step 3: Propose 2-3 Approaches

Once you understand the requirements, propose 2-3 different approaches:

- Present each with clear trade-offs (pros/cons)
- Lead with your recommended option and explain why
- Keep descriptions concise — focus on the key differentiators

Ask the user which approach they prefer.

### Step 4: Present Design

Present the design section by section. After each section, ask the user if it looks right before moving to the next.

Scale each section to its complexity: a few sentences if straightforward, more detail if nuanced.

Sections to cover (as applicable):
- **Architecture** — components, their responsibilities, how they interact
- **Data flow** — what goes in, what comes out, how data moves between components
- **File changes** — which files to create or modify
- **Error handling** — what can go wrong and how to handle it
- **Testing strategy** — what to test and how

### Step 5: Write Design Doc

Save the validated design using `Write`:
- Path: `~/.cliver/temp/design/YYYY-MM-DD-<topic>-design.md`
- Include: goal, architecture, design decisions, detailed changes, what does NOT change

### Step 6: Self-Review

After writing the doc, review it yourself:

1. **Placeholder scan:** Any "TBD", "TODO", incomplete sections? Fix them.
2. **Internal consistency:** Do sections contradict each other?
3. **Scope check:** Is this focused enough for a single implementation plan?
4. **Ambiguity check:** Could any requirement be interpreted two ways? Pick one and make it explicit.

Fix any issues by rewriting the doc with `Write`.

### Step 7: User Reviews Spec

Ask the user to review the written spec:

> "Spec written to `<path>`. Please review it and let me know if you want any changes before we move to implementation planning."

Wait for the user's response. If they request changes, make them and re-run the self-review.

### Step 8: Transition to Planning

Once the user approves the spec, activate the planning skill:

> "Design approved. Now activating the planning skill to create an implementation plan."

Call `Skill(skill_name='write-plan')` to continue.

## Key Principles

- **One question at a time** — don't overwhelm with multiple questions
- **YAGNI** — remove unnecessary features from designs
- **Explore alternatives** — always propose 2-3 approaches before settling
- **Incremental validation** — present design, get approval, then move on
- **Follow existing patterns** — in existing codebases, explore the structure first and follow conventions
