---
name: compiler-development
description: End-to-end compiler engineering covering lexing, resilient Pratt/recursive-descent parsing, AST arena allocation, bidirectional type systems, SSA-based IR, and register allocation.
---

# Compiler Development & Language Engineering

## 1. Purpose
Define, architect, and implement high-assurance programming language compilers, interpreters, and transpilers. Enforce rigorous conformance-first testing, resilient error-recovering parsing, immutable ASTs with accurate source spans, sound type checking and semantic analysis, SSA-form IR optimization passes, and ABI-compliant code generation.

---

## 2. Use When
- Developing language frontends (lexers, parsers, AST constructors, CST language servers).
- Engineering semantic analyzers, type inference engines (Hindley-Milner, Bidirectional), and borrow checkers.
- Designing intermediate representations (SSA CFG, 3-Address Code) and optimization passes.
- Building code generators targeting native machine code (x86_64, AArch64), WebAssembly, or LLVM IR.
- Implementing domain-specific languages (DSLs) or query language compilers.

---

## 3. Do Not Use When
- Simple text transformations or regular expression pattern matching adequately handled by standard scripts.
- General application business logic unrelated to programming language interpretation or compilation.
- Modifying UI layouts or CSS styles (use `design-system` or `ui-implementation`).

---

## 4. Required Context
Before implementing compiler pipelines, verify:
1. **Language Formal Grammar & Specification**: Lexical tokens, grammar rules (EBNF), operator precedence and associativity tables.
2. **Type System Specification**: Primitive types, composite types, subtyping rules, variance, and inference algorithms.
3. **Execution Model & Target ABI**: Tree-walking interpreter vs Bytecode VM vs Ahead-Of-Time (AOT) machine code / WebAssembly.
4. **Diagnostic & Error Budget**: Error resilience requirements (single error exit vs resilient recovery reporting multiple errors).

---

## 5. Procedure

### Step 1: Lexical Analysis & Token Streaming
1. Construct tokenizers that process UTF-8 source streams into structured token arrays.
2. Record complete source spans on every token: `FileId`, `start_byte`, `end_byte`, `line`, `col`.
3. Handle comments and whitespace as trivia if building language server tooling (Roslyn / rust-analyzer style), or filter cleanly for pure batch compilers.

### Step 2: Resilient Parsing & AST Construction
1. Use **Pratt Parsing** (Top-Down Operator Precedence) for expressions with complex operator precedence and associativity (infix, prefix, postfix, ternary).
2. Use **Recursive Descent** for structural grammar (declarations, statements, control flow blocks).
3. Implement error recovery synchronization: upon encountering a parse error, emit a structured diagnostic and skip tokens until reaching a synchronization boundary (`;`, `}`, `fn`, `let`, `return`) to continue parsing subsequent functions.
4. Allocate AST nodes in a contiguous memory `Arena` to ensure $O(1)$ teardown and maximum L1/L2 cache locality during traversals.

### Step 3: Semantic Analysis & Type Checking
1. Construct lexical symbol tables with parent scope linking for variable and type resolution.
2. Perform bidirectional type checking:
   - **Inference Mode**: $\Gamma \vdash e \Rightarrow \tau$ (synthesize type from expression).
   - **Checking Mode**: $\Gamma \vdash e \Leftarrow \tau$ (verify expression against expected context type).
3. Perform definite assignment analysis, unreachable code detection, and exhaustive pattern match checking.

### Step 4: High-Fidelity Diagnostic Engine
1. Never terminate with obscure or unlocated error messages.
2. Format diagnostics with:
   - Severity: Error, Warning, Note, Help.
   - Exact source file location with ANSI-highlighted source code snippets and underline carets (`^^^^`).
   - Actionable remediation advice or autofix suggestions.

### Step 5: Intermediate Representation (IR) & SSA Optimization
1. Lower the typed AST into a Control Flow Graph (CFG) of Basic Blocks in Static Single Assignment (SSA) form.
2. In SSA form, every variable is assigned exactly once, with $\phi$ (phi) functions placed at control flow join points.
3. Implement provably sound optimization passes:
   - Sparse Conditional Constant Propagation (SCCP).
   - Dead Code Elimination (DCE).
   - Common Subexpression Elimination (CSE) / Global Value Numbering (GVN).

### Step 6: Code Generation & ABI Compliance
1. Implement instruction selection using maximal munch or tree-rewriting patterns.
2. Allocate registers using Graph Coloring (Chaitin-Briggs) for AOT production, or Linear Scan (Poletto-Sarkar) for fast JIT compiles.
3. Adhere strictly to the target ABI: 16-byte stack alignment, callee-saved register preservation, and non-executable stack markers.

---

## 6. Decision Rules
1. **Resilient Parsing Over Early Aborts**: Parsers must never panic or exit on the first syntax error. They must recover at statement boundaries and report all discoverable errors in a single pass.
2. **Arena Allocation for AST Nodes**: Never use individual heap allocations (`malloc`, `new`) for individual AST nodes. Always allocate from an arena.
3. **Sound Optimization Invariant**: An optimization pass must never alter observable program behavior under any conforming execution. If an optimization cannot be proven sound, it must be disabled.
4. **Source Span Preservation**: Every AST node and IR instruction tracing back to source code must retain its original source span for diagnostics and debuginfo generation.

---

## 7. Evidence Required
- **Conformance Test Suite**: Test suite verifying 100% of grammar rules with nominal and negative test cases.
- **Diagnostic Snapshot Tests**: Automated tests asserting exact diagnostic error text and caret locations for invalid syntax.
- **Codegen / Execution Verification**: Test programs compiled by the pipeline execute and return expected exit codes and output streams.

---

## 8. Output Contract
A production compiler artifact must provide:
1. Lexer, Parser, and AST node definitions.
2. Semantic analyzer with type checking and symbol table resolution.
3. Diagnostic reporter with source snippet printing.
4. Comprehensive test suite covering syntax, semantics, and code generation.

---

## 9. Stop Conditions
- All language specification conformance tests pass.
- Diagnostic snapshots match golden references exactly.
- Zero memory leaks or crashes during compiler execution across invalid inputs.

---

## 10. Escalation Rules
- Escalate to Language Architect if grammar ambiguity (e.g. shift/reduce or reduce/reduce conflict) requires modifying language syntax rules.
- Escalate to Systems Lead if target platform ABI calling conventions conflict with external runtime linkers.
