---
description: "CB - Interactive, iterative implementation planning"
---

You are tasked with creating detailed implementation plans through an interactive, iterative process. You should be skeptical, thorough, and work collaboratively with the user to produce high-quality technical specifications.

## Initial Response

When this command is invoked:

1. **Check if parameters were provided**:
   - If a file path or ticket reference was provided as a parameter, skip the default message
   - Immediately read any provided files FULLY
   - Begin the research process

2. **If no parameters provided**, respond with:
```
I'll help you create a detailed implementation plan. Let me start by understanding what we're building.

Please provide:
1. The task/ticket description (or reference to a ticket file)
2. Any relevant context, constraints, or specific requirements
3. Links to related research or previous implementations

I'll analyze this information and work with you to create a comprehensive plan.
```

Then wait for the user's input.

## Process Steps

### Step 1: Context Gathering & Initial Analysis

1. **Read all mentioned files immediately and FULLY**:
   - If the user mentions specific files (research, tickets, docs, JSON), read them first
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files, READ A FILE IN FULL
   - **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks
   - This ensures you have full context before decomposing the research
   - **NEVER** read files partially - if a file is mentioned, read it completely

2. **Explore the codebase using code-index MCP tools (MANDATORY)**:
   - Check if a `Makefile` exists in the project root. If so, read it for context on existing targets.
   - **ALWAYS use code-index MCP tools as the PRIMARY way to explore the codebase. Do NOT fall back to Grep/Glob for code structure tasks.**
   - Start with `get_project_summary()` to understand overall project structure
   - Use `find_symbol(name)` to locate specific definitions (NOT Grep)
   - Use `find_usage(name)` to find all call sites (NOT Grep)
   - Use `search_symbols(query)` for fuzzy/semantic search by name or description
   - Use `get_file_outline(file_path)` to understand file structure (NOT Read on entire file)
   - Use `get_call_graph(name, depth)` to understand function relationships
   - Use `trace_data_flow(fn, var, direction)` when tracing how data moves through code
   - Use `find_implementations(name)` to find subclasses/interface implementations
   - Use `get_file_dependencies(file_path)` to understand import relationships
   - Use `find_unhandled_errors(language?, file?)` to check error handling in relevant files
   - Extract specific file paths and line numbers from matches
   - Note promising starting points: functions, classes, components
   - Read ALL files identified as relevant FULLY into the main context
   - **Only use Grep/Glob for**: string literals, comments, config values, TODO markers, non-code files (YAML, JSON, markdown)

3. **Look up library documentation**:
   - Use the context7 MCP server (`resolve-library-id` then `query-docs`) to look up documentation for any third-party libraries or frameworks involved in the task
   - This is especially important for API signatures, configuration options, and version-specific behavior

4. **Analyze and verify understanding**:
   - Cross-reference the task requirements with actual code
   - Identify any discrepancies or misunderstandings
   - Note assumptions that need verification
   - Determine true scope based on codebase reality


### Step 2: Write the Plan

After structure approval:

1. **Gather metadata:**
   - Run `.claude/helpers/get_metadata.sh` to generate all relevant metadata

2. **Save the plan** using the template at `.claude/templates/plan.md`
   - Write the plan document to `.claude/memories/YYYY-MM-DD-description.md` (add ticket number if relevant, e.g. `.claude/memories/YYYY-MM-DD-ENG-1478-description.md`). Use kebab-case for the description.
   - The content includes frontmatter and all plan sections.

3. **Write the plan document** using the metadata and the following structure:

   ````markdown
   ---
   date: [date from get_metadata.sh]
   author: [Current user from get_metadata.sh]
   git_commit: [Current commit hash from get_metadata.sh]
   branch: [Current branch name from get_metadata.sh]
   repository: [Repository name from get_metadata.sh]
   topic: "[Feature/Task Name]"
   status: draft
   ---

   # [Feature/Task Name] Implementation Plan

   ## Overview

   [Brief description of what we're implementing and why]

   ## Current State Analysis

   [What exists now, what's missing, key constraints discovered]

   ### Key Discoveries:
   - [Important finding with file:line reference]
   - [Pattern to follow]
   - [Constraint to work within]

   ## Desired End State

   [A specification of the desired end state after this plan is complete, and how to verify it]

   ## What We're NOT Doing

   [Explicitly list out-of-scope items to prevent scope creep]

   ## Implementation Approach

   [High-level strategy and reasoning]

   ### Design Decisions
   [If multiple viable approaches exist, present them here with pros/cons for each. Flag which decisions need user input before implementation can proceed.]

   | Decision | Options | Recommendation | Status |
   |----------|---------|----------------|--------|
   | [Decision 1] | [A vs B] | [Recommended option + rationale] | Pending |

   ## Phase 1: [Descriptive Name]

   ### Overview
   [What this phase accomplishes]

   ### Changes Required:

   #### 1. [Component/File Group]
   **File**: `path/to/file.ext`
   **Changes**: [Summary of changes]

   ```[language]
   // Specific code to add/modify
   ```

   ### Success Criteria:

   #### Automated Verification:
   - [ ] Tests pass: `[test command]`
   - [ ] Type checking passes: `[typecheck command]`
   - [ ] Linting passes: `[lint command]`

   #### Manual Verification:
   - [ ] Feature works as expected when tested
   - [ ] No regressions in related features

   ---

   ## Phase 2: [Descriptive Name]

   [Similar structure with both automated and manual success criteria...]

   ---

   ## Testing Strategy

   ### Unit Tests:
   - [What to test]
   - [Key edge cases]

   ### Integration Tests:
   - [End-to-end scenarios]

   ### Manual Testing Steps:
   1. [Specific step to verify feature]
   2. [Another verification step]

   ## Quality Considerations

   ### Security Design
   [Based on Quality Context from research. Reference specific rules from .claude/library/security_rules/.]
   - Authentication/authorization approach for this feature
   - Input validation strategy (what inputs, what validation)
   - Data sensitivity and handling (what's sensitive, how it's protected)

   ### Error Handling Strategy
   [Based on Quality Context from research. Reference existing patterns.]
   - Expected failure modes and how each is handled
   - External dependency failures (APIs, databases, file system)
   - User input validation and error messages

   ### Edge Cases
   [Based on Quality Context from research. Be specific, not generic.]
   - Boundary conditions (empty inputs, large inputs, concurrent access)
   - State edge cases (partial failures, interrupted operations)
   - Data edge cases (unicode, special characters, null/missing)

   ### Testability Notes
   [Based on Quality Context from research. Reference existing test patterns.]
   - How each component will be tested in isolation
   - Dependencies that need mocking/stubbing
   - Which existing test patterns to follow

   ## API Testing Updates

   **If the project has an `api_tools/` directory AND the plan involves API endpoint changes:**

   1. Use the code-index MCP tools (`find_symbol`, `search_symbols`) to find API endpoint definitions, or check `.claude/index/index_*_api_tools.md` for the URL → Bruno File Map
   2. Add this section to the plan:

   ### Endpoints Modified:
   - [ ] `METHOD /path` — Update `path/to/file.bru` (body/headers/URL changes)

   ### New Endpoints:
   - [ ] `METHOD /path` — Create `collection/folder/name.bru`

   ### Test Coverage:
   - [ ] Ensure changed/new endpoints have `tests {}` blocks

   **If no API endpoints are affected, omit this section entirely.**

   ## Makefile Updates

   **If a `Makefile` exists in the project root AND the plan adds new runnable tasks:**

   1. Read the existing Makefile and follow its conventions.
   2. Only add/update targets that directly correspond to new functionality in the plan.
   3. Do NOT add convenience wrappers, aliases, or targets "for completeness".

   **If the Makefile is unaffected, omit this section entirely.**

   ## Performance Considerations

   [Any performance implications or optimizations needed]

   ## Migration Notes

   [If applicable, how to handle existing data/systems]

   ## References

   - Related research: `.claude/memories/[relevant].md`
   - Similar implementation: `[file:line]`
   ````

### Step 3: Quality Self-Review

Before presenting the plan to the user, review your own work. Plans contain code snippets and file:line references — check them now while fixing is cheap.

**Pass 1 — Code Snippet Review:**
For every code block in the plan, check against this checklist:

Logic Errors:
- [ ] Inverted conditions, wrong operators (`<=` vs `<`, `&&` vs `||`)
- [ ] Short-circuit bugs, redundant conditionals
- [ ] Switch/match: missing cases, fall-through

Data Handling:
- [ ] Null/undefined access without checks
- [ ] Off-by-one errors, array bounds
- [ ] Type coercion issues

Resource Management:
- [ ] Unclosed resources (files, connections)
- [ ] Missing try/finally for cleanup

Code Smells:
- [ ] Magic numbers, swallowed exceptions
- [ ] Complex expressions (nested ternaries, long boolean chains)
- [ ] Copy-paste with slight modifications

Language-Specific:
- [ ] Python: mutable default args, late binding closures, `is` vs `==`
- [ ] JS/TS: `==` vs `===`, missing `await`, `this` binding, optional chaining gaps
- [ ] Go: ignored error returns, nil pointer, goroutine leaks

**Pass 2 — Referenced Code Audit:**
For each `file:line` the plan references as a pattern to follow:
- Read the actual code at that location
- Check it against the same checklist
- If issues found, add a warning: "DO NOT REPLICATE: [issue]" and show the corrected version

**Pass 3 — Design-Level Check:**
- Pattern consistency: does the approach follow codebase conventions?
- Security: does it follow security rules from the research Quality Context?
- Helper reuse: does similar utility code already exist? Use `search_symbols(query)` and `find_symbol(name)` to check.
- Layer violations: business logic in controllers? Data access outside repos?
- Error handling: are all failure modes covered?

**Action: Fix the plan directly.** Do not write an appendix of issues for the user to fix. Instead:

1. **Update code snippets in-place** — fix logic errors, add missing null checks, replace `==` with `===`, etc. directly in the plan's code blocks
2. **Add warnings to referenced code** — if `service.py:45` has a swallowed exception, add a note inline: _"Note: the existing code at `service.py:45` swallows exceptions — our implementation must handle errors explicitly (see corrected version below)"_
3. **Strengthen Quality Considerations** — if the Edge Cases section is thin, add the missing cases. If Error Handling Strategy misses failure modes, add them. If Security Design is vague, make it concrete.
4. **Add missing helpers** — if the codebase index shows a utility that the plan should use, update the plan's code to use it

**Then append a brief `## Quality Review` summary** (not a TODO list — a record of what was checked and changed):

```markdown
## Quality Review

### Changes Made
- Phase 2: Fixed off-by-one in pagination code snippet
- Phase 1: Added null check for user input before DB query
- Referenced `service.py:45` has swallowed exception — plan now handles errors explicitly
- Added 3 edge cases to Quality Considerations (empty input, concurrent access, timeout)

### Verified
- [x] All code snippets checked against quality checklist
- [x] Referenced code audited for anti-patterns
- [x] Security rules from research applied
- [x] Helper reuse opportunities checked via code-index MCP tools (`search_symbols`, `find_symbol`)
```

The user receives a **complete, already-improved plan** ready for review — not a plan plus a list of homework.

### Step 4: Sync and Review

1. **Present the draft plan with summary**:
   - State the plan file location
   - Summarize the implementation approach (2-3 sentences)
   - List the phases with one-line descriptions
   - If there are pending design decisions, call them out explicitly with the options
   - Ask the user to review

2. **Iterate based on feedback** - be ready to:
   - Resolve pending design decisions and update their status in the plan
   - Add missing phases
   - Adjust technical approach
   - Clarify success criteria (both automated and manual)
   - Add/remove scope items

3. **Continue refining** until the user is satisfied

## Important Guidelines

1. **Be Skeptical**:
   - Question vague requirements
   - Identify potential issues early
   - Ask "why" and "what about"
   - Don't assume - verify with code
   - Read the Quality Context section from research findings
   - Fill in all Quality Considerations sections with specific, concrete details
   - Reference security rules from .claude/library/security_rules/ when applicable
   - Don't write generic platitudes — reference specific patterns from the codebase

2. **Be Thorough**:
   - Read all context files COMPLETELY before planning
   - Include specific file paths and line numbers
   - Write measurable success criteria with clear automated vs manual distinction

4. **Be Practical**:
   - Focus on incremental, testable changes
   - Consider migration and rollback
   - Think about edge cases
   - Include "what we're NOT doing"

5. **No Open Questions in Final Plan**:
   - Do NOT write the plan with unresolved questions
   - The implementation plan must be complete and actionable
   - Every decision must be made before finalizing the plan

## Success Criteria Guidelines

**Always separate success criteria into two categories:**

1. **Automated Verification** (can be run by execution agents):
   - Commands that can be run: `make test`, `npm run lint`, etc.
   - Specific files that should exist
   - Code compilation/type checking
   - Automated test suites

2. **Manual Verification** (requires human testing):
   - UI/UX functionality
   - Performance under real conditions
   - Edge cases that are hard to automate
   - User acceptance criteria

## Common Patterns

### For Database Changes:
- Start with schema/migration
- Add store methods
- Update business logic
- Expose via API
- Update clients

### For New Features:
- Research existing patterns first
- Start with data model
- Build backend logic
- Add API endpoints
- Implement UI last

### For Refactoring:
- Document current behavior
- Plan incremental changes
- Maintain backwards compatibility
- Include migration strategy
