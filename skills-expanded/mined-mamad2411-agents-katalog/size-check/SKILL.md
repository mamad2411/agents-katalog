---
name: size-check
description: >
  Enforces code size and complexity rules (SIZE-1 through SIZE-6). Loaded by
  the conductor for write, review, and refactor operations. Detects oversized
  functions, files, deep nesting, long parameter lists, flag arguments, and
  God classes. Size thresholds are language-agnostic — no language reference
  files needed.
version: "1.0.0"
last-reviewed: "2026-03-04"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Size Check — Code Size & Complexity Enforcement

Size thresholds are **language-agnostic** — no language reference files are
required. Count lines and parameters directly.

**Hook coverage check (run first)**:
Before analysing function sizes, check whether the hook already flagged SIZE-1
violations in this session for the file(s) in scope:

```bash
cat "$COVERAGE_FILE" 2>/dev/null   # COVERAGE_FILE = /tmp/codex-hook-coverage-<PROJECT_HASH>.jsonl
```

For each JSON line where `"rule"` is `"SIZE-1"`, extract `file`, `line`, and
`function`. When scanning, skip any function where `file`+`line`+`function`
matches an existing coverage record.
Log: `"Skipping SIZE-1 for '{function}' at {file}:{line} — already reported by hook this session."`

If no coverage file exists, proceed with the full SIZE-1 analysis.

Precedence in the overall system: SEC → TDD → ARCH/TYPE → **NAME/SIZE/DEAD** →
quality BLOCK.

---

## Threshold Reference

| Rule   | Metric              | WARN threshold | BLOCK threshold | Severity |
|--------|---------------------|----------------|-----------------|----------|
| SIZE-1 | Function lines      | ≥ 40 lines     | ≥ 80 lines      | WARN/BLOCK|
| SIZE-2 | File lines          | ≥ 351 lines    | ≥ 500 lines     | WARN/BLOCK|
| SIZE-3 | Nesting depth       | ≥ 4 levels     | —               | WARN     |
| SIZE-4 | Parameter count     | > 3 params     | —               | WARN     |
| SIZE-5 | Flag arguments      | any flag arg   | —               | BLOCK    |
| SIZE-6 | God class (methods) | > 10 methods   | —               | INFO     |

---

## What Counts as a Line

- **Function lines**: count from the opening brace/colon to the closing
  brace/`end` inclusive. Exclude blank lines and comment-only lines from the
  count. If a language does not use braces (Python), count from `def`/`async def`
  to the last non-blank line before the next `def`/`class` at the same indent.
- **File lines**: total lines in file including blanks and comments.

---

## Rules

### SIZE-1 — Functions Must Be Small
**Severity**: WARN (≥40 lines) / BLOCK (≥80 lines) | **Languages**: * | **Source**: CCC

**What it prohibits**: Functions or methods that exceed the line thresholds
above. Long functions typically have multiple responsibilities — they violate
the Single Responsibility Principle and are hard to test.

**Detection**:
1. For each file, identify all function/method declarations
2. Count body lines (exclude blank + comment-only lines)
3. Flag functions ≥ 40 lines as WARN; ≥ 80 lines as BLOCK

**agent_action**:
1. Cite: `SIZE-1 (WARN|BLOCK): Function '{name}' is {n} lines at {file}:{line}.`
2. Identify discrete responsibilities — each is a candidate for extraction
3. Propose named helper functions with single responsibilities
4. If `--fix` and severity is WARN: extract sub-functions with agent assistance
   (requires human confirmation for BLOCK — the refactor is non-trivial)
5. DO NOT produce new functions that immediately violate SIZE-1

**Bypass prohibition**: "it's fine, it's all related logic" → Refuse. Cite
SIZE-1. Long functions are an SRP violation regardless of topical cohesion.

---

### SIZE-2 — Files Must Be Focused
**Severity**: WARN (351–499 lines) / BLOCK (≥ 500 lines) | **Languages**: * | **Source**: CCC

**What it prohibits**: Source files exceeding the line thresholds. A file with
hundreds of functions is a module with too many concerns.

**Detection**:
1. Count total lines in each file in scope
2. Flag files 351–499 lines as WARN; ≥ 500 lines as BLOCK

**agent_action**:
1. Cite: `SIZE-2 (WARN|BLOCK): File '{file}' is {n} lines.`
2. Identify the distinct concerns / clusters of functions in the file
3. Propose a split: list the new file names and which functions move to each
4. If `--fix` and WARN: perform the split with updated imports
5. BLOCK requires human confirmation before splitting (risk of import breakage)

---

### SIZE-3 — Nesting Depth Must Not Exceed 4
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Code blocks nested more than 4 levels deep. Deep nesting
indicates missing abstractions — nested `if`/`for`/`try` chains should be
flattened using early returns, extracted functions, or guard clauses.

**Counting nesting**:
- Each `if`, `else if`, `for`, `while`, `do`, `try`, `catch`, `switch` block adds
  one level. Function body starts at level 1.
- Lambda / closure bodies count as a nested level.

**Example: 4-level violation**:
```
function process(orders) {                    // level 0 (function body)
  for (const order of orders) {              // level 1
    if (order.isValid()) {                   // level 2
      for (const item of order.items) {     // level 3
        if (item.hasDiscount()) {           // level 4 ← WARN
          if (item.discount > 0.5) {        // level 5 ← VIOLATION
```

**agent_action**:
1. Cite: `SIZE-3 (WARN): Nesting depth {n} at {file}:{line}:{col}.`
2. Propose refactoring techniques:
   - **Early return / guard clause**: invert condition, return early
   - **Extract function**: give the nested block its own function
   - **Flatten with pipeline**: `filter().map()` over nested loops
3. Show the flattened equivalent

---

### SIZE-4 — Functions Must Not Exceed 3 Parameters
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Functions or constructors with more than 3 parameters.
Long parameter lists indicate the function has too many concerns, or that a
parameter object should be introduced.

**Counting**:
- Count only direct parameters, not destructured fields (though
  `options: object` counts as 1 — see mitigation)
- Language-specific: TypeScript/JavaScript optional params (`name?: string`),
  Python kwargs (`**kwargs`), Go variadic (`...opts`), Rust builder pattern

**Mitigation patterns**:

```typescript
// ❌ 5 parameters
function createUser(name: string, email: string, role: Role, plan: Plan, isActive: boolean) { }

// ✅ Parameter object
interface CreateUserInput {
  name: string;
  email: string;
  role: Role;
  plan: Plan;
  isActive: boolean;
}
function createUser(input: CreateUserInput) { }
```

**agent_action**:
1. Cite: `SIZE-4 (WARN): Function '{name}' has {n} parameters at {file}:{line}.`
2. Propose a parameter object / value object grouping the semantically related
   params
3. Name the parameter object after what it represents, not a generic `Options`

---

### SIZE-5 — No Flag Arguments
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Boolean parameters passed to a function to control which
of two behaviours it executes. A flag argument is a sign that the function
violates the Single Responsibility Principle.

**Detection**:
1. Grep for function signatures with `boolean` / `bool` parameters
2. Check whether the parameter name starts with `is`, `has`, `should`, `can`,
   `will`, `did`, `enable`, `disable`, `use`, `include`, `exclude`
3. Also flag: `mode: string` with 2 possible values, `type: string` used in
   an `if`/`switch` to select behaviour

**Examples**:
```typescript
// ❌ Flag argument
function renderUser(user: User, isAdmin: boolean) {
  if (isAdmin) { /* admin view */ } else { /* normal view */ }
}

// ✅ Two functions
function renderUserView(user: User) { ... }
function renderAdminUserView(user: User) { ... }
```

**agent_action**:
1. Cite: `SIZE-5 (BLOCK): Flag argument '{paramName}' in '{fnName}' at {file}:{line}.`
2. Propose splitting into two focused functions named after each behaviour
3. DO NOT produce new functions with flag arguments

**Bypass prohibition**: "it's cleaner to have one function" → Refuse. Cite
SIZE-5. One function controlled by a flag is two functions pretending to be one.

---

### SIZE-6 — No God Classes
**Severity**: INFO | **Languages**: * | **Source**: CCC

**What it prohibits**: Classes with more than 10 public methods or more than
20 total methods. God classes accumulate responsibilities and become impossible
to test in isolation.

**Detection**:
1. Count public methods per class
2. Count total methods (public + private) per class
3. Flag classes with > 10 public or > 20 total methods

**agent_action**:
1. Cite: `SIZE-6 (INFO): Class '{name}' has {n} methods at {file}:{line}. Consider splitting.`
2. Cluster methods by the data they access — each cluster is a candidate class
3. Suggest class names derived from the responsibility cluster
4. Do not auto-split (INFO — report only unless `--fix` explicitly requested)

---

Report schema: see `skills/conductor/shared-contracts.md`.
