---
name: slop-detector
description: >
  This skill should be used when the user asks to "detect slop", "scan for AI patterns",
  "check for over-engineering", "find unnecessary code", "audit AI output", "quick quality check",
  "how bad is this code", "rate this code", or "score this file". It performs a fast diagnostic
  scan of AI-generated TypeScript/Node.js code producing a severity table and slop score.
  No rewrite — diagnosis only. Use for quick assessment before the full code-review skill.
version: 0.1.0
---

# Slop Detector

Fast, targeted scan for AI-generated code anti-patterns. No rewrite — just a diagnosis.

## Purpose

This is the lightweight sibling of `code-review`. It runs a focused anti-pattern scan and produces a severity-ranked issue list. No rewrite, no cleanup — just a clear-eyed diagnosis with line numbers.

Use this when you want to know **what's wrong** before deciding whether to fix it yourself or delegate to `code-review`.

## The Slop Taxonomy

AI coding agents produce a predictable set of failure patterns. These are documented, measured, and reproducible across Claude Code, Copilot, Cursor, and Codex. This skill checks for all of them.

### Category 1: Phantom Abstractions
Code structures that exist but serve no purpose. The AI created them because its training data is full of enterprise Java patterns.

**Signals:**
- Classes with one method → should be a function
- Functions that only call one other function with the same arguments → inline it
- Interfaces with one implementor and no polymorphic use → delete the interface
- Abstract base classes with one child → merge into the child
- Singleton patterns for stateless utilities → use module scope
- Factory functions that always return the same type → just use `new` or a literal
- "Service" / "Manager" / "Handler" / "Provider" / "Controller" suffix on a class with <3 methods
- **Passthrough generators**: `async *foo(p) { for await (const x of this.bar(p)) { yield x; } }` — if the only transform is trivial or absent, this method shouldn't exist
- **Context Bag**: Custom `Context` or `SharedState` interface created solely to pass parent state to child classes. The simpler pattern: pass `this` (the parent) directly when composing sub-services
- **Ceremony interface**: A dedicated `FooOptions` type with 2-3 fields used by exactly one function — just use inline parameters

**Severity: 🟡 Important**

### Category 2: Prophetic Engineering
Code that solves problems the codebase will never have. The AI optimizes for generality because it doesn't know your roadmap.

**Signals:**
- Generic type parameters used with only one concrete type
- Configuration objects for values that are hardcoded everywhere else
- Plugin/extension systems with zero plugins
- Event emitter patterns where the emitter has one listener
- Strategy patterns with one strategy
- Optional parameters that are always passed the same value
- "Options" objects with one field

**Severity: 🟡 Important**

### Category 3: The Walking Dead
Code that compiles but does nothing. The AI generates it because removal requires understanding, and generation is cheaper.

**Signals:**
- Imports not referenced anywhere in the file
- Variables assigned then never read
- Functions defined then never called (check across files)
- Catch blocks that are empty or just `console.error` with no re-throw
- Type assertions that match the already-inferred type (`x as string` when x is already string)
- Commented-out code blocks (>2 lines)
- `console.log` / `console.debug` statements
- TODO/FIXME/HACK comments with no issue tracker reference

**Severity: 🔴 Critical (dead code) / 🔵 Minor (leftover logs)**

### Category 4: The Monolith Instinct
AI agents don't decompose proactively. They dump entire multi-step workflows into a single function or class. The result works but is unreadable and untestable. When the user forces decomposition, the AI reaches for cargo-cult patterns (Context interfaces, factories, abstract bases) instead of the simplest structural fix.

**Signals (undecomposed monolith):**
- A single function handling fetch → parse → transform → persist
- Methods >50 lines with multiple distinct logical phases
- A class mixing I/O, parsing, business logic, and error handling
- Files where you scroll to follow control flow

**Signals (badly decomposed — the AI was told to split):**
- New `Context`/`SharedState` interface created to shuttle state (should just pass `this`)
- Abstract class introduced where composition works
- More new types/interfaces than new classes (ceremony > structure)
- Factory for objects constructed once
- Event/pub-sub where direct calls suffice

**Severity: 🟡 Important**

### Category 5: The Nesting Instinct
Deeply nested control flow. The AI generates it because it models code as a tree, not a pipeline.

**Signals:**
- If/else chains deeper than 2 levels
- Nested ternary operators
- `.then().then().then()` chains (should be async/await)
- Callback nesting (callback hell)
- Nested `try/catch` blocks
- Switch inside switch
- `if` inside `for` inside `if` — any 3-level nesting

**Severity: 🟡 Important**

### Category 6: The Identity Crisis
Naming that hides intent. The AI picks generic names because it doesn't understand your domain.

**Signals:**
- Single-letter variables outside of loop counters or lambda parameters
- `data`, `result`, `response`, `item`, `temp`, `val`, `info`, `stuff`, `obj` as variable names
- Functions named with nouns instead of verbs: `userValidation()` instead of `validateUser()`
- Boolean variables without `is`/`has`/`should`/`can` prefix
- Acronyms or abbreviations that aren't universally understood
- Same concept named differently in different files (inconsistency)

**Severity: 🟡 Important**

### Category 7: Error Amnesia
Error handling that pretends errors don't happen, or handles them in ways that hide information.

**Signals:**
- Empty catch blocks: `catch (e) {}`
- Catch-and-log-only: `catch (e) { console.error(e) }` with no re-throw or recovery
- Generic catch without adding context: `catch (e) { throw e }` (adds nothing)
- Try/catch wrapping an entire function body
- No error handling on file I/O, network calls, or JSON.parse
- Mixing error handling patterns (sometimes throw, sometimes return null, sometimes callback)

**Severity: 🔴 Critical**

### Category 8: Comment Theater
Comments that perform documentation without achieving it.

**Signals:**
- `// increment counter` above `counter++`
- `// returns the user` above `return user`
- `// constructor` above `constructor()`
- JSDoc that repeats parameter names without adding meaning: `@param name - the name`
- Stale comments that contradict the current code
- Missing comments on functions that have non-obvious behavior or side effects
- No top-of-method comment on complex exported functions

**Severity: 🔵 Minor (noise comments) / 🟡 Important (missing critical comments)**

### Category 9: Type System Cosplay (TypeScript-specific)
Using TypeScript's type system in ways that add complexity without adding safety.

**Signals:**
- `any` used more than once in a file
- `as` type assertions that could be replaced with proper typing or type guards
- Redundant type annotations: `const x: string = "hello"`
- Overly complex mapped/conditional types that could be simplified
- Generic types with >2 type parameters
- `!` non-null assertion without an accompanying comment explaining why it's safe
- Union types that should be discriminated unions (no discriminant field)

**Severity: 🟡 Important**

### Category 10: The Trojan Output
Code that appears to work but silently produces wrong or fake results. The most dangerous category — it passes tests and visual inspection. IEEE Spectrum (2026) documented this as a growing failure mode where AI removes safety checks or creates plausible-looking fake output.

**Signals:**
- Catch blocks that return plausible defaults (`[]`, `null`, `{}`, `0`) instead of propagating errors
- Validation functions that always return `true` or have no-op validation logic
- API wrappers that return mock-shaped data on failure instead of throwing
- Functions that log errors but continue as if nothing happened
- Safety guards from original code removed by AI during "refactoring"
- Permission/auth checks that are structurally present but evaluate to no-op
- Error messages formatted but never delivered to any output

**Severity: 🔴 Critical**

### Category 11: The Clone Army
AI generates by predicting tokens, not by understanding your codebase. It will re-implement logic that already exists. GitClear measured an 8x increase in code clones since 2021, and refactoring activity dropped from 25% to under 10% of all changes.

**Signals:**
- Near-identical functions in different files (same logic, different names)
- Utility functions that duplicate an already-imported library's functionality
- Copied error handling boilerplate (should be a shared handler)
- Re-implemented standard library methods (`Array.prototype.flatMap`, etc.)
- Duplicated type definitions across modules
- Multiple functions differing only in one parameter (should be one parameterized function)

**Severity: 🟡 Important**

### Category 12: The Speed Trap
AI optimizes for correctness, not runtime efficiency. CodeRabbit found excessive I/O operations are 8x more common in AI-generated code.

**Signals:**
- `await` inside `for` loops (should be `Promise.all`)
- Nested loops creating O(n²)+ complexity
- N+1 query patterns (fetching related data one-by-one in a loop)
- String concatenation inside loops (should be array + join)
- Loading full datasets into memory (should stream or paginate)
- Repeated computation of expensive values (should memoize)
- Synchronous file I/O in async contexts

**Severity: 🟡 Important (🔴 if in hot path)**

### Category 13: The Phantom Import
1 in 5 AI code samples references libraries or methods that don't exist. AI also regularly uses deprecated APIs from older training data.

**Signals:**
- Imports of npm packages that don't exist
- Method calls that don't match the installed version's API
- Deprecated Node.js APIs (`url.parse()`, `new Buffer()`, etc.)
- Browser-only APIs used in Node.js (or vice versa)
- Incorrect method signatures (wrong parameter count or order)
- References to removed TypeScript compiler options

**Severity: 🔴 Critical (will crash at runtime)**

## Completeness Check (MANDATORY)

After your initial scan, you MUST do a second pass. Walk through the file function-by-function and check each one against this list. If you find a match, it MUST appear in your findings table — even if it overlaps with another finding.

**For EACH function, check:**
1. Is the entire function body wrapped in a single try/catch? → **Error Amnesia** finding.
2. Does it have a doc comment? If it's exported, >5 lines, and has no doc comment → **Comment Theater** finding ("missing comment on complex exported function").
3. Are there comments that literally restate the next line of code? (e.g., `// increment counter` above `counter++`) → **Comment Theater** finding, even if the surrounding code is also flagged for other reasons.

**For EACH variable declaration, check:**
4. Does it have a redundant type annotation? (`const x: string = "hello"`) → **Type System Cosplay** finding.
5. Is it assigned but never read? → **Walking Dead** finding, even if it looks intentional (e.g., `const debug = process.env.DEBUG`).

**For EACH console.log/console.debug:**
6. Flag it → **Walking Dead** finding. `console.log` is not a logging strategy.

## Output Format

```markdown
## Slop Scan: [filename]

**Verdict**: [CLEAN | MINOR SLOP | MODERATE SLOP | HEAVY SLOP]

**Score**: X/10 (10 = pristine, 1 = rewrite from scratch)

### Findings

| # | Line | Category | Signal | Severity | One-line fix |
|---|------|----------|--------|----------|--------------|
| 1 | 14   | Phantom Abstraction | Single-method class | 🟡 | Inline as function |
| 2 | 42   | Walking Dead | Unused import | 🔴 | Delete |
| ... | | | | | |

### Recommendation
[One of: "Ship it", "Quick cleanup needed", "Needs code-review skill", "Consider rewriting"]
```

## Boundaries

- This skill **diagnoses only**. It does not rewrite code.
- If the user wants fixes applied, suggest they use the `code-review` skill.
- Do not flag stylistic preferences that aren't in the anti-pattern list.
- Do not flag test files.
- Do not flag code that is ugly but correct and coherent — "works and is clear" passes this scan.
