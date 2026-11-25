---
name: ast-transformation
description: Programmatic syntax tree transformation, automated codemods, macro expansion, hygienic rewrites, and lossless CST trivia preservation.
---

# AST Transformation & Automated Codemods Contract

## 1. Purpose
Design, implement, and audit automated Abstract Syntax Tree (AST) and Concrete Syntax Tree (CST) transformations, codemods, macro expansions, and syntactic desugaring. Enforce source-span fidelity, comment and whitespace (trivia) preservation, hygienic variable scoping, and strictly idempotent rewrites.

---

## 2. Use When
- Developing automated migration codemods (e.g. upgrading component APIs, framework versions, or language features).
- Building linter auto-fixers, static refactoring tools, and code formatters.
- Implementing procedural macros, syntactic desugaring passes, or compile-time code generators.
- Performing large-scale automated code modernizations across repositories with zero semantic degradation.

---

## 3. Do Not Use When
- Performing naive text-based string replacements or regex substitution across source files where syntax context matters.
- Simple non-code data file transformations (JSON/YAML normalization).
- Authoring standard application business logic without code manipulation.

---

## 4. Required Context
Before implementing AST transformations, verify:
1. **Target Language & AST Schema**: Language specification and parser toolchain (e.g., Python `ast`, Babel / `@babel/traverse`, `ts-morph`, `syn`/`quote` in Rust, `tree-sitter`).
2. **Trivia Preservation Policy**: Lossless CST requirement (must preserve comments and spacing in unmodified code blocks).
3. **Scope & Hygiene Invariants**: Identification of identifier collisions, shadowing, and unbound variables introduced by the rewrite.
4. **Idempotence Constraint**: Confirm that re-applying the transform to an already transformed file produces zero changes ($T(T(x)) = T(x)$).

---

## 5. Procedure

### Step 1: Parse to Lossless Syntax Representation
1. Parse source code into a syntax tree preserving source trivia (comments, whitespace, formatting) whenever formatting preservation is required.
2. Maintain parent pointers or scope stacks during tree traversal to enable contextual analysis (e.g., checking if a variable is defined in an enclosing function).

### Step 2: Query & Pattern Matching
1. Identify target node patterns using structural queries rather than fragile manual traversal:
   - Match node kind (e.g., `CallExpression`, `FunctionDeclaration`).
   - Match callee / identifier identity.
   - Match argument count, types, and keyword parameters.
2. Filter false positives by validating scope: verify the matched identifier resolves to the expected library import rather than a local shadow variable.

### Step 3: Hygienic Rewrite Execution
1. Construct replacement AST nodes or text-diff edits:
   - For macro expansions and introduced variables, generate unique, hygienic identifiers (`gensym`) to avoid capturing or shadowing user variables.
   - Update import statements: insert newly required imports and prune unused deprecated imports.
2. Prefer emitting narrow text-range diffs (`[start_byte, end_byte] -> replacement_string`) over pretty-printing the entire file from scratch. This guarantees 100% preservation of git blame and existing code styles outside the transformed site.

### Step 4: Validate Idempotence
1. Apply the transformation to candidate source: $S_1 = T(S_0)$.
2. Apply the transformation again to the output: $S_2 = T(S_1)$.
3. Assert that $S_2 \equiv S_1$. If $S_2 \ne S_1$, the transformation is non-idempotent and constitutes a defect.

### Step 5: Semantic & Syntactic Verification
1. Parse the transformed code back into an AST to verify syntax validity.
2. Run project type checkers and test suites against the transformed codebase.
3. Compare golden before/after test snapshots.

---

## 6. Decision Rules
1. **Strict Idempotence Invariant**: A codemod or AST transform must be strictly idempotent:
   $$T(T(\text{code})) = T(\text{code})$$
2. **Preserve Surrounding Formatting**: Never reformat untouched functions or files. Only modify the specific AST nodes or byte spans targeted by the rule.
3. **Hygienic Identification**: Any newly injected local variable must use collision-free naming (e.g. prefixed with `__prumo_` or generated via scope analysis).
4. **No Partial or Corrupted Writes**: If an AST transform encounters an unparseable construct or unexpected AST structure, it must skip the file, report a warning, and make zero mutations to disk.

---

## 7. Evidence Required
- **Idempotency Proof**: Automated test verifying $T(T(x)) == T(x)$ across nominal and edge cases.
- **Syntax Validation**: Output passes language parser with 0 syntax errors.
- **Golden Snapshot Tests**: Before/after `.input` and `.output` diffs asserting exact intended code rewrites.

---

## 8. Output Contract
A production AST transformation artifact must provide:
1. AST visitor / transformer module implementing the rewrite rules.
2. Unit tests with golden snapshot fixtures covering positive and negative cases.
3. Automated verification script executing idempotence assertions.

---

## 9. Stop Conditions
- All golden snapshot tests match expected output.
- Idempotence is verified across all test suites.
- Transformed files pass static analysis and unit testing without errors.

---

## 10. Escalation Rules
- Escalate to Lead Architect if a codemod cannot safely disambiguate polymorphic API calls without full-program type inference.
- Escalate to Security Officer if an AST transformation injects dynamic code execution paths or modifies security-sensitive headers.
