# AGENTS.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
- If requirements conflict (e.g., durability vs latency, correctness vs speed), name the conflict explicitly. Never average conflicting requirements into something that satisfies neither.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

When fixing a bug, fix the root cause, not the symptom. Find where the defect actually lives:
- Grep every caller of the function you touch; a report names a symptom, and patching only the path the ticket mentions leaves sibling callers still broken.
- If the shared function is wrong, fix it once - do not scatter per-caller guards.
- If one caller is wrong, fix that caller - do not add defensive handling to a correct shared function.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Read Before You Write

**Understand adjacent code before changing it. "Looks orthogonal" is a dangerous assumption.**

Before adding code to any file:
- Read the file's exports and public API.
- Read the immediate callers of the function you're modifying.
- Check shared utilities in the same module.
- If you're unsure why code is structured a certain way, ask before writing.

## 6. Fail Visibly, Not Silently

**Silent skips are failures. Surface uncertainty instead of hiding it.**

- "Completed" is wrong if anything was silently skipped.
- "Tests pass" is wrong if any test was skipped.
- Default to surfacing uncertainty. When in doubt, over-communicate what you're unsure about.
- If a required input, file, or tool is missing (or a step is impossible under the stated constraints), do NOT fabricate it to make a check pass. Report what is missing and what you need.

## 7. Reuse Before Writing

**Before writing new code, check in order:**
1. Does it already exist in this codebase? Reuse it - do not re-implement it yourself, even with the standard library. (If the existing helper is itself the bug, fix it once - see Rule 3.)
2. Does the standard library cover it? Use it.
3. Only then: write the minimum code that works.

## 8. Use Available Editing Tools

**Follow the current harness's tool surface; do not assume a shell patch helper exists.**

- Use the native file-editing tools exposed by the current environment. In pi, use `edit` for precise replacements and `write` for new files or complete rewrites.
- Do not run `apply_patch` as a shell command unless `command -v apply_patch` confirms that executable is available.
- If the harness exposes `apply_patch` as a dedicated tool rather than a command, invoke it only through that tool interface.
