---
name: spec-driven-review
description: Review the code quality of a spec-driven change. Checks readability, security, performance, and best practices before archiving.
version: 0.1.0
---

You are reviewing the code quality of a completed spec-driven change.

## Steps

1. **Select the change** — run `node {{SKILL_DIR}}/scripts/spec-driven.js modify` to list active changes. Ask which change to review. If already specified, use it.

2. **Confirm readiness** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js apply <name>
   ```
   If `remaining > 0`, stop — the change is not ready for review. Suggest `/spec-driven-apply` first.

3. **Load context** — read:
   - `.spec-driven/changes/<name>/proposal.md` — scope and unchanged behavior
   - `.spec-driven/changes/<name>/design.md` — approach and decisions
   - `.spec-driven/changes/<name>/tasks.md` — what was implemented
   - `.spec-driven/config.yaml` — project context and rules (including `test` rules and any `fileMatch` entries)

4. **Identify changed files** — from the completed tasks, determine which files were created or modified. Read each file fully.

5. **Review code quality** — for each changed file, check:
   - **Readability**: clear naming, reasonable function length, no unnecessary complexity
   - **Security**: no injection vulnerabilities, no hardcoded secrets, proper input validation at system boundaries
   - **Error handling**: appropriate error handling for external calls and user input; no swallowed errors
   - **Performance**: no obvious N+1 queries, unnecessary allocations, or blocking calls in async contexts
   - **Best practices**: follows the project's conventions (from config.yaml context), no dead code, no debug artifacts left behind

6. **Check test quality** — read the test files associated with this change:
   - Do tests cover the key scenarios from the delta specs?
   - Are tests independent and repeatable?
   - Do tests follow `rules.test` from config.yaml?

7. **Output a review report**:
   ```
   MUST FIX (blocks archive):
     - [list or "none"]

   SHOULD FIX (recommended):
     - [list or "none"]

   NITS (optional):
     - [list or "none"]
   ```

8. **Recommend next step**:
   - If MUST FIX issues: address them before archiving
   - If only SHOULD FIX: ask user if they want to address them or proceed
   - If clean: suggest `/spec-driven-archive <name>`

## Rules
- Read every changed file before commenting on it — never review code you haven't read
- Focus on real issues, not style preferences already handled by linters
- MUST FIX = security vulnerabilities, data loss risks, broken functionality
- SHOULD FIX = maintainability concerns, missing error handling, unclear logic
- NITS = naming suggestions, minor simplifications, documentation gaps
- Do not re-review code that was not changed by this change
- Respect config.yaml rules — violations of project rules are SHOULD FIX at minimum
