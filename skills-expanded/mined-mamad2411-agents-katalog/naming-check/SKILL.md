---
name: naming-check
description: >
  Enforces naming convention rules (NAME-1 through NAME-7, plus NAME-UL).
  Loaded by the conductor for write and review operations. Detects meaningless
  names, incorrect boolean prefixes, misleading names, abbreviations, naming
  inconsistencies, and (for files in `core/`) generic technical suffixes that
  drift away from ubiquitous language. Loads references/{language}.md for
  language-specific casing conventions before checking.
version: "1.0.0"
last-reviewed: "2026-03-04"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Naming Check — Naming Convention Enforcement

**First action**: Load `references/{language}.md` for the detected language to
get language-specific casing rules and tooling before checking.

Precedence in the overall system: SEC → TDD → ARCH/TYPE → **NAME/SIZE/DEAD** →
quality BLOCK.

---

## Anti-Pattern Reference

The following names are **always violations** of NAME-1 regardless of language:

| Category       | Banned names                                                    |
|----------------|-----------------------------------------------------------------|
| Generic nouns  | `data`, `info`, `result`, `value`, `item`, `object`, `thing`    |
| Temp vars      | `temp`, `tmp`, `var1`, `var2`, `x`, `y`, `z` (outside math)    |
| Flag vars      | `flag`, `check`, `done`, `found`, `status` (as booleans)        |
| Handler catch  | `e`, `err` (acceptable), `error` (acceptable — but not `e2`)    |
| Non-descriptive| `foo`, `bar`, `baz`, `test`, `stuff`, `misc`, `helper`          |

---

## Boolean Prefix Rules (NAME-2)

Boolean variables and functions returning booleans **must** use a predicate prefix:

| Allowed prefixes | Examples                                      |
|------------------|-----------------------------------------------|
| `is`             | `isActive`, `isLoggedIn`, `isValid`           |
| `has`            | `hasPermission`, `hasChildren`, `hasError`    |
| `should`         | `shouldRetry`, `shouldRefresh`                |
| `can`            | `canDelete`, `canEdit`, `canProceed`          |
| `will`           | `willExpire`, `willTimeout`                   |
| `did`            | `didChange`, `didLoad`, `didSucceed`          |

**Banned boolean names**: `active`, `enabled`, `valid`, `loaded`, `connected`
(these are adjectives lacking a predicate prefix — use `isActive`, `isEnabled`, etc.)

---

## Scope-Proportional Length Rule (NAME-4)

Name length must scale with identifier scope:

| Scope                   | Minimum length / guideline                             |
|-------------------------|--------------------------------------------------------|
| Loop counter (1–5 lines)| Single letter acceptable: `i`, `j`, `k`, `n`          |
| Local var (≤10 lines)   | 2–8 chars; must hint at domain concept                 |
| Function-scoped var     | ≥ 4 chars; clearly descriptive                         |
| Module/class member     | ≥ 6 chars; unambiguous in class context                |
| Public API / export     | Full descriptive name; no abbreviations (see NAME-5)   |

Single-letter names outside loops, or 1–2 char names in module scope, are NAME-4
violations.

---

## Test Naming Pattern (NAME-7)

All test functions must follow the pattern: `[subject]_[scenario]_[expected]`

```
# Python
def test_create_user_with_duplicate_email_raises_conflict_error(): ...

// TypeScript / JavaScript
it('createUser_withDuplicateEmail_raisesConflictError', () => { ... });

// Go
func TestCreateUser_WithDuplicateEmail_RaisesConflictError(t *testing.T) { ... }

// Rust
#[test]
fn create_user_with_duplicate_email_raises_conflict_error() { ... }
```

See language reference for exact casing of each segment.

---

## Rules

### NAME-1 — Meaningful, Intention-Revealing Names
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Identifiers that do not reveal intent. Covers variables,
functions, parameters, classes, modules, and files. Any name from the
anti-pattern table above is an automatic violation.

**Detection**:
1. Grep for anti-pattern names in variable/parameter/function declarations
2. For each: check whether it is used inside a math expression where single
   letters are conventional (geometry, algorithms) — if so, skip
3. Otherwise flag

**agent_action**:
1. Cite: `NAME-1 (BLOCK): Non-revealing name '{name}' at {file}:{line}.`
2. Propose a name derived from what the identifier actually holds or does
3. If `--fix`: replace the name at declaration and all call sites within `--scope`
4. DO NOT produce new code using a banned name

**Bypass prohibition**: "it's just a temp var", "everyone knows what x means"
→ Refuse. Cite NAME-1. Context is lost within hours.

---

### NAME-2 — Boolean Names Must Use Predicate Prefix
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Boolean variables or functions returning `bool` /
`boolean` / `bool` that do not start with a predicate prefix from the allowed
list above.

**Detection**:
1. Grep for `bool`/`boolean` type annotations and `-> bool` return types
2. Check function/variable name against the allowed prefix list
3. Flag names that are bare adjectives: `active`, `valid`, `enabled`, `loaded`

**agent_action**:
1. Cite: `NAME-2 (WARN): Boolean '{name}' missing predicate prefix at {file}:{line}.`
2. Propose prefixed name: `active` → `isActive`, `valid` → `isValid`
3. If `--fix`: rename at declaration and all usage sites within `--scope`

---

### NAME-3 — No Misleading Names
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Names that actively lie about what the identifier is or
does. Examples:
- A list named `accountList` that is actually a `Map`
- A function named `getUser` that has side effects (creates, deletes, etc.)
- A class named `Manager` or `Processor` or `Handler` (content-free nouns)
- A boolean named `isTrue`, `isFlag`, or other tautologies

**Detection**:
1. Check container names (`List`, `Map`, `Set`, `Array`, `Dict`) against actual type
2. Flag `get*` functions that contain write operations (INSERT, DELETE, update calls)
3. Flag class names ending in `Manager`, `Processor`, `Handler`, `Helper`,
   `Util`, `Utils`, `Misc`, `Common`

**agent_action**:
1. Cite: `NAME-3 (BLOCK): Misleading name '{name}' at {file}:{line}. Reason: {reason}.`
2. Propose an accurate name that reflects actual behaviour
3. For content-free class names: propose splitting into domain-specific classes
   with cohesive responsibilities

---

### NAME-4 — Scope-Proportional Name Length
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Names that are too short for their scope (module-level
single-letter) or excessively long without adding clarity (names > 50 chars
that repeat surrounding context).

**agent_action**:
1. Cite: `NAME-4 (WARN): Name '{name}' at {file}:{line} too short/long for its scope.`
2. Propose appropriately scoped alternative

---

### NAME-5 — No Abbreviations in Public APIs
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Abbreviations and acronyms in exported/public identifiers
that are not universally understood. Domain-standard acronyms (HTTP, URL, ID,
API, SQL, JSON, XML) are permitted. All others must be spelled out.

**Examples**:
- `usrNm` → `userName`
- `getProdCat` → `getProductCategory`
- `calcTtlPrc` → `calculateTotalPrice`
- `HTTP`, `URL`, `UserID`, `parseJSON` — permitted

**agent_action**:
1. Cite: `NAME-5 (WARN): Abbreviation in public identifier '{name}' at {file}:{line}.`
2. Propose fully-spelled-out name
3. If `--fix`: rename in all files within `--scope`

---

### NAME-6 — Consistent Naming Within a Domain Concept
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Using different names for the same concept in the same
codebase. Example: a user entity called `User` in one module, `Account` in
another, and `Member` in a third — all referring to the same domain concept.

**Detection** (heuristic — flag for human review):
1. Collect all entity/class names and exported function names in scope
2. Flag near-synonym clusters: `User`/`Account`/`Member`, `fetch`/`get`/`load`/`retrieve`
   used for the same type of operation, `create`/`add`/`insert`/`save` mixed for
   persistence writes

**agent_action**:
1. Cite: `NAME-6 (WARN): Inconsistent naming — '{name_a}' and '{name_b}' may refer to the same concept.`
2. Ask the author to confirm canonical name and propose a rename plan
3. Do not auto-rename without confirmation (ambiguous — requires human decision)

---

### NAME-7 — Test Functions Follow Subject_Scenario_Expected Pattern
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Test function names that do not follow the
`[subject]_[scenario]_[expected]` pattern, or that use vague descriptions like
`test1`, `testCase`, `itWorks`, `checkStuff`.

**Detection**:
1. Identify test files via language reference patterns (e.g., `*.test.ts`,
   `test_*.py`, `*_test.go`)
2. Grep test function declarations
3. Check each name against the three-part pattern

**agent_action**:
1. Cite: `NAME-7 (WARN): Test name '{name}' does not follow [subject]_[scenario]_[expected] pattern at {file}:{line}.`
2. Propose compliant name based on what the test actually validates

---

### NAME-UL — Ubiquitous Language in Core
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Vague, generic, technical suffixes on types and
functions that live in `core/` (per the conductor's Section 14 layer
detection). Core code should read in the language domain experts use.

**Banned suffixes/prefixes in core**:
- `Manager`, `Processor`, `Helper`, `Util`, `Utility`, `Utils`
- `Service` is allowed *only* if the name actually denotes a domain service
  (e.g., `PricingService`); banned when used as a generic suffix
  (`UserService`, `OrderService` covering arbitrary operations on the entity).
- `Handler` is **allowed** — HTTP handlers, event handlers, and command
  handlers are legitimate names at inbound boundaries. But `Handler` in core
  (away from inbound boundaries) is suspect.
- Generic verbs as function names: `process`, `handle`, `do`, `execute`,
  `perform` without a domain object (`processOrder` is fine, `process` alone
  is not).

**Why WARN, not BLOCK**: name choice is heuristic and codebase-specific. The
rule prevents the most common drift toward generic technical naming without
fighting genuine domain vocabulary that happens to look generic.

**Detection** (only on files in `core/`):
1. Grep type declarations for banned suffixes.
2. Grep function declarations for banned verb-only names.
3. Cross-reference with existing NAME-1 (generic nouns) and NAME-4 (banned
   abbreviations) to avoid double-counting.

**agent_action**:
1. Cite: `NAME-UL (WARN): '{name}' uses generic technical naming in core at {file}:{line}.`
2. Ask: what domain term does this represent? Propose the domain-aligned name.
3. Example: `OrderManager` → ask whether the domain calls this an `Order`
   itself (anemic name), an `OrderLifecycle`, a `Fulfillment`, a `PricingPolicy`,
   etc.
4. With `--fix`: never auto-rename — naming is a judgment call that requires
   domain context the agent doesn't have.

---

Report schema: see `skills/conductor/shared-contracts.md`.
