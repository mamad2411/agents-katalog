---
name: code-cleanup
description: >
  This skill should be used when the user asks to "clean up code", "remove dead code",
  "fix imports", "flatten nesting", "simplify code", "strip slop", "tidy this file",
  "just fix it", or "clean this up without explaining". It applies mechanical cleanup
  transforms to AI-generated TypeScript/Node.js code through 10 ordered passes (dead code,
  nesting, abstractions, naming, comments, silent failures, duplicates, delegation boundary,
  performance, imports) plus mandatory verification. No report — just the cleaned code with
  REVIEW flags for uncertain changes.
version: 0.1.0
---

# Code Cleanup

Apply mechanical cleanup transforms to AI-generated TypeScript/Node.js code. No judgment calls — just deterministic fixes.

## Purpose

This is the **rewrite-only** sibling of `code-review`. No report, no analysis — just the cleaned code. Use it when you already know the code is sloppy and you want it fixed without commentary.

It applies a fixed set of mechanical transforms. If a transform can't preserve behavior with certainty, it skips it and flags it with an inline `// REVIEW:` comment for the human.

## SAFETY RULES (Read these FIRST — they override everything below)

These rules are ABSOLUTE. Every transform in the pipeline below is subject to them. If a rule and a transform conflict, the rule wins.

1. **NEVER change behavior.** Same inputs must produce same outputs. If you remove a try/catch, the function now throws instead of returning a default — that IS a behavior change. Don't do it. Flag it with `// REVIEW:` instead.
2. **NEVER remove or restructure error handling** — not try/catch blocks, not catch bodies, not error returns. Even if the error handling looks wrong (empty catch, catch-and-log, swallowed errors), KEEP IT and add a `// REVIEW:` comment explaining what's wrong. The human decides whether to change error behavior.
3. **NEVER delete or inline exported symbols, and NEVER remove, rename, or change the signature of any method on an exported class.** Other files depend on them. This means:
   - If an exported class has one method → do NOT convert it to a function. Flag with `// REVIEW:` instead.
   - If an exported class has a method (even a passthrough) → KEEP IT. Do not remove it.
   - If a method takes an interface parameter → do NOT change the parameter type or inline the interface.
   - Example: `export class Foo { getItems() { ... } }` — you MUST NOT remove `getItems`, even if it just wraps another method. Flag it: `// REVIEW: passthrough method`.
4. **NEVER remove imports that are used anywhere in the file.** Before removing an import, search for every reference to it in the file. If `createHash` is called in any function, the import stays. NEVER replace an import with `require()` — that changes module resolution behavior.
5. **NEVER remove functions you're not 100% sure are unused.** If the function could be called dynamically, flag it.
6. **NEVER let the parent do the subservice's job.** If a class delegates to a subclass or subservice, the parent must NOT perform work that falls within the subservice's domain of responsibility — even if the subservice doesn't currently do that work. This is not about duplication; it's about *whose concern it is*. The parent orchestrates (calls subservices); it does not execute domain logic that belongs downstream. If you see logic in the parent that belongs to a subservice's concern, flag it: `// REVIEW: this logic belongs in [SubServiceName] — consider moving it`. NEVER add, keep, or move subservice-domain logic INTO the parent during cleanup.
7. **Mark uncertainty.** Anywhere you're less than certain, use `// REVIEW:` comments.
8. **Flag performance issues** in Passes 7-8 — they are NOT optional. Sequential `await` in loops, O(n²) patterns, and duplicated logic MUST get `// REVIEW:` comments even if the code is otherwise clean.

## Transform Pipeline

Apply these in order. Each pass should be complete before moving to the next.

### Pass 1: Dead Code Removal

Remove, in this order:
1. Unused imports — but VERIFY before removing: for each import you plan to remove, search the ENTIRE file for any reference to that symbol (in function bodies, type annotations, default values, etc.). If the symbol appears ANYWHERE, the import stays. When in doubt, keep the import.
2. Unused variables (assigned but never read)
3. Unused functions (defined but never called — verify across the file; if unsure, add `// REVIEW: possibly unused`)
4. Commented-out code blocks (>2 lines)
5. Console.log / console.debug statements
6. Redundant type assertions (`x as Type` where x is already that Type)
7. Empty catch blocks → replace with `// REVIEW: empty catch - intentional?`

### Pass 2: Flatten Nesting

For each function in the file:
1. Identify guard conditions (input validation, null checks, error conditions)
2. Move guard conditions to the top as early returns:
   ```typescript
   // Before
   function process(input: Input) {
     if (input) {
       if (input.isValid) {
         // ...50 lines of logic...
       } else {
         throw new Error('invalid');
       }
     } else {
       throw new Error('missing input');
     }
   }

   // After
   function process(input: Input) {
     if (!input) throw new Error('missing input');
     if (!input.isValid) throw new Error('invalid');

     // ...50 lines of logic (now at top level)...
   }
   ```
3. Convert nested ternaries to `if/else` or extracted variables
4. Convert `.then()` chains to `async/await` where the function is already async

### Pass 3: Inline Phantom Abstractions

**⚠️ GATE CHECK: Before inlining ANY class or method, check if the class is exported. If the class IS exported (directly or via an export statement), do NOT inline it, do NOT remove any of its methods, and do NOT change any method signatures. Instead, flag it with `// REVIEW:` and move on. Safety rule 3 overrides this entire pass for exported symbols.**

For non-exported classes and functions only:
- **Single-method classes** → convert to a standalone function
- **Wrapper functions** (only forward arguments to another function) → inline at call sites
- **Singleton utility classes** → convert to module-scoped functions
- **Factory functions that always return one type** → replace with direct construction
- **Passthrough generators** (async generator A that only yields from generator B with zero or trivial transform) → flag: `// REVIEW: passthrough generator`

- **Context Bag interfaces** (custom `Context`/`Options` type created to shuttle parent state to child classes) → flag: `// REVIEW: Context Bag — consider passing parent instance instead`

Only inline when the abstraction adds **zero logic**. If it adds even one condition, one transform, one default — keep it.

### Pass 4: Naming Fixes

Apply only **safe renames** (file-scoped, non-exported symbols). When renaming, ONLY change the variable name — do NOT change its type, wrapping, or initialization. `const data: any = {}` renamed to `const rowData: any = {}` is safe. `const data: any = {}` changed to `const rowData: Record<string, unknown> = {}` is a TYPE CHANGE, not a rename — don't do it.

Rename targets:
- `data` → name based on what the data contains (e.g., `userData`, `orderPayload`)
- `result` → name based on the operation (e.g., `parsedConfig`, `validationResult`)
- `temp` → name based on purpose or remove if only used once
- `item` in loops → name based on the collection (`users.map(user => ...)` not `users.map(item => ...)`)
- Boolean variables → add `is`/`has`/`should`/`can` prefix

For **exported symbols**, do NOT rename. Instead add: `// REVIEW: consider renaming — [suggestion]`

### Pass 5: Add Missing Comments

For each non-trivial exported function that lacks a top comment:
```typescript
/**
 * [One sentence: what this does and why]
 * [Optional: non-obvious decisions, constraints, or side effects]
 */
```

Rules:
- "Non-trivial" = more than 5 lines, or has branching logic, or has side effects
- Never restate the function name. `/** Gets a user */` above `getUser()` is useless.
- Focus on WHY it exists and any non-obvious behavior.
- If you can't infer the purpose, write: `/** REVIEW: purpose unclear — needs documentation */`

### Pass 6: Silent Failure Scan

For each try/catch block and error handling path:
1. Check if catch blocks return plausible defaults (`[]`, `null`, `{}`) instead of propagating — add `// REVIEW: silent failure — catch returns default instead of throwing`
2. Check if validation functions have actual validation logic (not always-true)
3. Check if error logging actually writes somewhere (not just formatting)
4. Check if safety guards were removed during AI refactoring — compare with types/interfaces to see if null checks are missing on nullable fields

This pass does NOT fix silent failures — it only flags them with `// REVIEW:` because fixing them requires understanding the intended behavior.

### Pass 7: Duplicate Detection

For each non-trivial function (>5 lines):
1. Search the file for near-identical logic blocks
2. If two blocks share >70% of their logic, flag: `// REVIEW: duplicated logic — consider extracting shared function`
3. Check if a function re-implements a method already available from an imported library
4. Check for copied error handling boilerplate that should be a shared handler

### Pass 7b: Delegation Boundary Check

For each class that has injected dependencies (constructor parameters that are services/subclasses):
1. For each method in the parent class, ask: "Whose job is this logic? The parent's or a subservice's?" The test is responsibility, not duplication — even if the subservice doesn't currently do this work, if the work falls within the subservice's domain, it's misplaced.
2. If the parent performs domain-level work (formatting, validation, transformation, data assembly, business rules) that falls within a subservice's concern, flag it: `// REVIEW: leaky delegation — this logic belongs in [SubServiceName]`
3. If the parent directly manipulates data that the subservice is responsible for (instead of calling the subservice), flag it: `// REVIEW: bypassed delegation — call [SubServiceName] instead of doing this directly`
4. Do NOT move or refactor the code — only flag it. The human decides where logic belongs.

This pass catches misplaced responsibility: logic in the parent that should live in a subservice, regardless of whether the subservice already implements it.

### Pass 8: Performance Quick Scan

Flag (do not fix — performance changes can alter behavior):
1. `await` inside `for`/`forEach` loops → `// REVIEW: sequential awaits — consider Promise.all for parallelization`
2. Nested loops on large collections → `// REVIEW: O(n²) — consider using Map/Set for lookup`
3. String concatenation in loops → `// REVIEW: consider array.join() for performance`
4. Repeated expensive computations → `// REVIEW: consider memoizing this value`

### Pass 9: Import Cleanup

1. Remove all unused imports
2. Sort remaining imports: external packages first, then internal (relative) imports, separated by a blank line
3. Prefer named imports over namespace imports when <4 items are used

## Output Format

Output the cleaned file. At the top, add a brief comment block:

```typescript
/**
 * Cleanup applied:
 * - Removed N unused imports
 * - Inlined N abstractions
 * - Flattened N nested blocks
 * - Added N method comments
 * - Removed N lines of dead code
 * - Flagged N silent failure risks
 * - Flagged N duplicate logic blocks
 * - Flagged N leaky delegation concerns
 * - Flagged N performance concerns
 * - Total: N items flagged for human review (search "REVIEW:")
 */
```

## Pass 10: Verification (MANDATORY — run before emitting output)

Before producing the final output, compare your cleaned code against the original file and verify ALL of these:

**10a. Export check:** List every `export` from the original file. Every exported name (function, class, variable, type) must still exist in your output with the SAME name and SAME type signature. If any exported symbol was removed, renamed, or changed from class to function — UNDO that change now.

**10b. Error handling check:** List every `try/catch` block from the original file. Every single one must still be present in your output. If you removed a try/catch (even an empty one), put it back and add `// REVIEW:` instead. The catch body may be annotated but NEVER deleted.

**10c. Import check:** For every import in your output, verify it is used. For every import you removed, verify it is NOT used anywhere in the output. If you removed an import but a function still references it — RESTORE the import.

If any check fails, fix the output before emitting it.

## Boundaries

- Production code only. Skip test files.
- TypeScript/Node.js only. Don't apply to config files, JSON, YAML, etc.
- One file at a time. For multi-file cleanup, the user should invoke this skill per file or use `code-review` for architectural analysis.
- Don't split files. Don't change the module boundary. Work within the existing file.
