---
name: implement
description: 'Implement from a plan file or task description. Follows project patterns, runs build + tests. Use: /implement plans/task-name.md'
---

# /implement - Feature Implementation

Implement code following team standards and project patterns.

**Input:** Plan file path or task description via `$ARGUMENTS`

## Workflow

### Step 1: Understand the task

- If `$ARGUMENTS` references a plan file (e.g., `plans/task-name.md`), read it
- If no plan file specified, check `plans/` for an existing plan related to the task
- If the plan references a spec document, read it for exact details (DB schema, field names, validation rules, business rules, acceptance criteria)
  - **Images/Diagrams:** If the spec mentions diagrams, UI mockups, or contains image references that Notion MCP couldn't read:
    - Ask the user: "I see the spec references diagrams/images. Please share them so I can implement the design correctly."
    - Wait for user to attach images before proceeding
- If `$ARGUMENTS` contains a Notion link, read the ticket and its linked Document via Notion MCP
  - Apply same image handling as above if spec has images
- If just a description, use that directly
- **Before starting**: check if any plan items are already marked `[x]` (from a previous session). Skip completed items

### Step 2: Read project context and existing code

- Read `docs/code-standards.md` and `.claude/rules/stack-rules.md` for project patterns
- Read `docs/codebase-summary.md` for module inventory, auth architecture, and key patterns
- Identify existing code to use as reference implementation
- Read the files listed in the plan's "New files" and "Modified files" sections BEFORE making changes
- Check imports, dependencies, and module registration of affected modules

### Step 3: Implement

Follow the plan's "Implementation order" if specified. Otherwise:
1. Read `.claude/rules/stack-rules.md` for stack-specific implementation order
2. If no stack-rules.md, use this default: data layer → business logic → API/UI layer → tests

**Stack-specific patterns:**
Follow patterns from `.claude/rules/stack-rules.md`. This includes framework architecture, security patterns, and code conventions.

**Code quality:**

- try-catch on all async operations
- Proper error handling with appropriate exception types
- TypeScript types — no `any` unless justified
- Files under 500 lines
- kebab-case file names
- **Save progress incrementally**: After completing each checklist item from the plan, immediately mark it `[x]` in the plan file. Do NOT wait until the end

### Step 4: Write tests (MANDATORY — never skip)

**Rule: every file created or modified in Step 3 MUST have a corresponding unit test.**

- Check if the plan includes a "Tests" section — follow it
- For new services: write unit tests covering key business logic, edge cases, and error paths
- For new controllers: write tests covering endpoint routing and input validation
- **For React components (`.tsx`):** create `__tests__/[ComponentName].snapshot.test.tsx` minimum; add behavior tests for any logic in the component
- **For utility/helper functions:** unit test covering all cases and edge cases
- Use the `tester` agent to analyze what needs test coverage if unsure
- Follow existing test patterns in the codebase (check `*.spec.ts` or `__tests__/` in similar modules)

**Frontend additional rule:** If any `.tsx` component has inline logic (data transformation, filtering, formatting) — extract it to a utility function first, then test both the utility and the component.

### Step 5: Verify

Run the build/lint/test commands from `.claude/rules/stack-rules.md`:
- Lint fix
- Build/compile
- Run tests

- If build fails: read the compiler error, fix the specific issue, rebuild
- If tests fail: determine if it is a code bug or a test that needs updating for the new behavior, then fix
- If you cannot resolve a build or test failure after 2 attempts: use the `debugger` agent with the error output
- Do NOT proceed until lint, build, and tests all pass

### Step 6: Update progress

- If a plan file exists in `plans/`, ensure all completed items are marked with `[x]`
- If Notion ticket exists, update the checklist via Notion MCP

### Step 7: Handoff

Print the next step:
```
Next: /review
```
Do NOT commit directly. The `/review` skill will run lint, build, tests, and dispatch the code-reviewer agent.

## Rules

- Follow `.claude/rules/development-rules.md`
- Follow the plan's "New files" and "Modified files" sections exactly. Create new files only where the plan specifies. Modify existing files where specified
- Do NOT create enhanced/v2 copies of existing files. If the plan says to modify `deal.service.ts`, modify it in place
- Implement real code, never mock or simulate
- Run build after implementation to verify compilation
- Use `debugger` agent if stuck on a complex bug (cannot resolve after 2 attempts)
- Use `tester` agent for comprehensive test analysis
- **If the task cannot be completed in one session**: Ensure all completed items are marked in the plan file, run the build command from `.claude/rules/stack-rules.md` to verify partial work compiles, and inform the user which items remain. The next `/implement` invocation will resume from the first unchecked item
