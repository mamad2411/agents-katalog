# Cursor AI Rules for this Project

## Authorship — NON-NEGOTIABLE

**Engin Atik is the sole author on ALL papers, documents, and publications.**

- NEVER add Claude, AI assistants, or any other entity as a co-author, contributor, or affiliate.
- NEVER reference Claude or AI as co-authoring in paper body text.
- Do not assume, suggest, or default to co-authorship. The user's decision is final.

---

## Session Start Rules

**CRITICAL: At the start of each session, read `docs/NEXT_SESSION.md`.**

This document contains:
- Current work in progress and implementation plans
- Architecture decisions and context from previous sessions
- Test plans and files to review
- Lessons learned and things NOT to do

**Always start by understanding what was happening before continuing.**

---

## Kleis Policy Engine (Formal Rules)

**Many rules that were previously in this file are now formalized in the Kleis
policy: `examples/policies/agent_policy.kleis`.**

The policy engine is a reasoning partner, not just a gatekeeper. Use these
MCP tools to interact with it:

| Tool | What it does |
|------|-------------|
| `check_action` | Check whether an action is allowed + get preconditions |
| `list_rules` | Show all loaded policy rules |
| `explain_rule` | Explain a specific rule in detail |
| `describe_schema` | Learn the full Kleis vocabulary: structures, functions, axioms |
| `evaluate` | Evaluate any Kleis expression or verify a proposition via Z3 |

**Rules now in Kleis policy (not repeated here):**
- Git push / force-push / production branch restrictions
- Server process management (lsof before starting servers, no pkill/killall)
- Dangerous command blocking (rm -rf, chmod 777, curl|sh, etc.)
- Quality gates before commit/push (fmt, clippy, test, link check)
- Parser preconditions (run tests + read grammar before editing)
- Evaluator/type/DAP preconditions (run relevant tests before editing)
- File creation rules (no loose .md in root, allowed directories)
- File deletion rules (protect src/, tests/, config)
- File edit rules (protect lock files, generated files)
- Documentation preconditions (read source before writing docs)
- Session start preconditions (read NEXT_SESSION.md, validate examples)

**Toggle enforcement:**
```bash
scripts/policy.sh on      # Enable policy MCP (alwaysApply: true)
scripts/policy.sh off     # Disable policy MCP (alwaysApply: false)
scripts/policy.sh status  # Show current state

scripts/theory.sh on      # Enable theory MCP (alwaysApply: true)
scripts/theory.sh off     # Disable theory MCP (alwaysApply: false)
scripts/theory.sh status  # Show current state
```

---

## The Philosophy of Kleis (Level 3)

**CRITICAL: Kleis is not a "math tool" or a "proof assistant."**

It's a **knowledge production substrate** built on a fundamental insight:

> *"Structure is the universal abstraction. Data is structure. Code is structure. Research is structure. Any domain that has notation, rules, and outputs fits the same pattern. Kleis provides the substrate."*

### The Three Levels

```
Level 3: PHILOSOPHY
  "Knowledge production has a universal structure.
   Any domain can be modeled as:
   Notation + Rules + Verification + Output.
   Kleis is the substrate for this universal pattern."

Level 2: ARCHITECTURE
  Solver abstraction, .kleist templates, structures,
  self-hosting types, Typst integration, Equation Editor

Level 1: IMPLEMENTATION
  Rust code, parser, Z3 bindings, LSP, DAP, Jupyter kernel
```

### The Universal Formula

| Component | Kleis Feature | Example Domains |
|-----------|---------------|-----------------|
| **Notation** | `.kleist` templates | Tensors, music notes, chemical formulas |
| **Rules** | `axiom` in structures | Bianchi identity, counterpoint, reaction rules |
| **Verification** | Solver backends (Z3, etc.) | Proof checking, rule validation |
| **Output** | Typst rendering | Papers, scores, diagrams |

### Before Implementing, Ask:

1. "How does this serve the philosophy?"
2. "What domain does this enable?"
3. "Is this Level 1 work supporting Level 2/3 goals?"

**From Einstein's equations to order-to-cash business rules — same platform, same abstraction.**

---

## DAP Debugger Context - CRITICAL

**REMINDER: Debugging is about Expression::Operation and its span. NOT about functions or substitution.**

### What Matters for Debugging

1. **Expression::Operation has a span field**
   - The span contains: line, column, file (Arc<PathBuf>)
   - This information comes from the PARSER when parsing Kleis source files
   - The parser populates span.file via `current_span()` which uses `current_file`

2. **When reporting to VS Code:**
   - The span already has ALL the location information
   - Extract it via `expr.get_span()` → `SourceLocation::from_span()`
   - Report this location in `on_eval_start`
   - VS Code uses this in the stack trace to show the correct file

3. **DO NOT get distracted by:**
   - ❌ Functions and function definitions
   - ❌ Substitution of parameters
   - ❌ `find_definition_line` or similar lookups
   - ❌ Tracking file paths separately from the Expression

4. **The span IS the source of truth**
   - Parser puts file path in span
   - Evaluator extracts span from Expression
   - Debug hook receives location from span
   - VS Code receives location from debug hook

**If debugging doesn't show the right file, check: Does the Expression's span have the correct file?**

### CRITICAL LESSON (Learned the Hard Way)

**Substitution does NOT modify spans. The span is just NUMBERS and a filename.**

The parser puts these numbers in the Expression. Nothing else changes them.
Substitution creates new expressions but PRESERVES the original span.

**If you find yourself writing code about:**
- "find_definition_line" → STOP. The span has the line.
- "on_function_enter" → STOP. Focus on Expression::Operation.
- "tracking which file we're in" → STOP. The span has the file.

The span. Has. Everything. Just. Use. It.

---

## Editor AST vs Kleis AST Architecture

**CRITICAL: There are TWO different ASTs in this project. Do not confuse them.**

### The Two ASTs

| AST Type | Created By | Location | Purpose |
|----------|-----------|----------|---------|
| **Editor AST** | JavaScript | `static/index.html` | Internal representation for Equation Editor |
| **Kleis AST** | Rust Parser | `src/kleis_parser.rs` | Language representation matching grammar |

**They are NOT the same thing.** The Editor AST is internal and can have richer structure.

### Three-Rung Ladder Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ RUNG 1: Equation Editor (JavaScript in static/index.html)       │
│   User clicks button → generates Editor AST                     │
│   Uses SEMANTIC operation names: 'gamma', 'riemann', 'index_mixed' │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ RUNG 2: Kleis Renderer (Rust: src/render.rs)                    │
│   Editor AST → visual output (per target)                       │
│   • Typst target: uses template keyed by 'gamma' → Γ^λ_{μν}    │
│   • LaTeX target: uses template keyed by 'gamma'                │
│   • Kleis target: outputs xAct notation → Γ(λ, -μ, -ν)          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ RUNG 3: Kleis Language (src/kleis_parser.rs, grammar, Z3)       │
│   Kleis text → parsed to Kleis AST → verified/evaluated         │
│   Example: "Γ(λ, -μ, -ν)" parses to function call with negate() │
└─────────────────────────────────────────────────────────────────┘
```

### Key Rules

1. **Editor AST uses semantic operation names** — `gamma` NOT `Γ`
2. **xAct notation belongs in Kleis text output only** — NOT in Editor AST
3. **Changing Editor AST requires updating ALL renderers** (5 targets + server + tests)
4. **Templates are keyed by semantic names** — if you change to symbols, rendering breaks

---

## Z3 and Equation Editor Performance Rules

**CRITICAL: The Equation Editor MUST NOT hang waiting for Z3.**

### What Works vs What Hangs

| Operation | Method | Result |
|-----------|--------|--------|
| **Evaluate** `nth([1,2,3], 1)` | Z3 + ∀ axioms | ❌ HANGS |
| **Evaluate** `nth([1,2,3], 1)` | Inline Rust expansion | ✅ Fast |
| **Verify** `g(μ,ν) = g(ν,μ)` satisfiable? | Z3 + ∀ axioms | ✅ Fast |

**Architecture Decision:**
Axioms are for VERIFICATION ("is this true?"), not EVALUATION ("what is 2+2?").
For evaluation, Rust computes directly and tells Z3 the answer.

---

## Type System Rules

**CRITICAL: Follow ADR-014 (Hindley-Milner Type System) and ADR-016 (Operations in Structures).**

### Rule: Maintain Type System Integrity (ADR-014)

**The type system must follow Hindley-Milner principles.**

**Core Principles:**

1. **Constraint-based inference** - Generate constraints, then unify
2. **Principal types** - Always infer the most general type
3. **No shortcuts** - Don't bypass unification or constraint solving
4. **Context threading** - Pass `context_builder` through call chain

**When modifying type inference:**
1. Always generate constraints — don't hardcode results
2. Always delegate operations — use `context_builder.infer_operation_type()`
3. Always thread context — pass `context_builder` through recursive calls
4. Always unify — let the solver determine types

### Rule: No Hardcoding Types (ADR-016)

**Types and operations MUST be defined in Kleis structures, NOT hardcoded in Rust.**

**Key Files:**
- `src/type_inference.rs` - Core HM algorithm
- `src/type_context.rs` - Type registry and queries
- `src/type_checker.rs` - Combines inference + registry
- `stdlib/*.kleis` - Type definitions (source of truth)

**Exceptions:** Built-in primitives only (Scalar, basic arithmetic).
Everything else must be defined in `stdlib/*.kleis` structures.

---

## Refactoring and Code Quality Rules

**CRITICAL: No shortcuts, no technical debt, no half-measures.**

### Rule: Actually Use What You Build

When implementing abstractions or refactoring:
- **Test the abstraction immediately** - Don't just build it, USE it
- **Remove old code** - Delete it entirely, don't leave it "just in case"
- **Run full test suite** - Not just unit tests, run ALL tests (`cargo test`, not `--lib`)
- **Verify through tests** - Tests must exercise the new code path

### Rule: Remove Dead Code Systematically

**Process:**
1. Comment out old code (to see what breaks)
2. Run `cargo check` - see compilation errors
3. Fix each error by using new abstraction
4. Verify with `cargo test` (ALL tests!)
5. Delete old code completely (don't leave commented out)
6. Run quality gates (fmt, clippy, test)

**Don't guess - Let the compiler tell you.**

### Rule: Think Through Architecture

**Before implementing, ask:**
1. "What if the feature is disabled?" — Check `#[cfg(not(feature = "..."))]` case
2. "What state belongs where?" — Backend state vs. high-level state
3. "Can this be misused?" — Abstraction boundaries clear?

### Rule: No "Practical Workarounds" for Real Bugs

**If you catch yourself writing "workaround," "for now," or "the practical approach is,"
STOP. That is a signal you are avoiding the actual fix.**

- A bug in import resolution is not solved by "run from a different directory"
- A bug in repo detection is not solved by "use absolute paths"
- A missing feature is not solved by "set an environment variable"

**Fix the root cause. The "workaround" is the shortcut.**

**The Architect's Motto:**
"No shortcuts for getting a clean build or saving time. Don't make tests lenient. If you're about to change or delete tests, ask first."

---

## Read Code Before Writing Documentation

**CRITICAL: Read the actual code before documenting or describing it.**

Claude tends to generate plausible-sounding documentation without first reading the implementation.

**Before writing documentation for any component:**
1. **Read the source file(s)** using `read_file` or `grep`
2. **Understand the actual API** - method signatures, types, return values
3. **Note what's implemented vs planned** - check for TODOs, feature flags
4. **Then write** documentation that matches what exists

**"Claude is learning to read before writing."**

---

## Parser Development Rules

**CRITICAL: Parser changes must align with formal grammar.**

**Grammar files (source of truth):**
- `docs/grammar/kleis_grammar_v05.ebnf` - EBNF specification
- `docs/grammar/Kleis_v05.g4` - ANTLR4 grammar
- `docs/grammar/kleis_grammar_v05.md` - Human-readable explanation

**Process:** Read relevant grammar section → verify change matches spec → if deviation needed, document why → test with grammar examples → update grammar docs if spec changed.

---

## Documentation Organization Rules

**When creating documentation during a session:**

1. **Combine overlapping content** - Review documents for redundancy
2. **Organize into subdirectories** - `docs/session-YYYY-MM-DD/` for session work
3. **Session archival** - Move to `docs/archive/sessions/` after ~2 weeks
4. **Keep docs/ root clean** - Only last 2-3 active sessions + permanent docs

**Cleanup checklist before ending session:**
- [ ] Consolidate overlapping documents
- [ ] Move session-specific docs to session folder
- [ ] Delete obsolete/temporary documents
- [ ] Update docs/README.md
- [ ] Archive sessions older than 2 weeks

---

## General Guidelines

- Follow user instructions carefully
- Ask for clarification when uncertain
- Be respectful of the user's workflow and preferences
