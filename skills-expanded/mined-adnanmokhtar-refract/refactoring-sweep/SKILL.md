---
name: refactoring-sweep
description: Codifies the 10 Fowler-style refactoring closure verbs as detector + procedure pairs. Is the core apply-engine of /refactor (these 10 verbs ARE /refactor's closed vocabulary) and is also used by /optimize Phase 2 (tactical) and any /align-recheck run that hits the refactoring class. Each verb has a fingerprint (what triggers it), a procedure (how to apply it safely), and a verify step (what must stay green). Behaviour-preserving — refactoring NEVER changes observable output.
kind: skill
pack: code-quality
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: refactoring-sweep

## Purpose

Apply Fowler-style refactorings as closure verbs in /optimize and /align-recheck. Each verb is a small, named, behaviour-preserving transformation with a clear fingerprint and verification step. The skill does NOT invent refactorings; it operates from a closed vocabulary of 10 verbs.

## When to use

- **Core apply-engine of `/refactor`** — the 10 verbs below ARE `/refactor`'s closed vocabulary; `/refactor` dispatches this skill with `--target=<paths>` and the `refactorer` agent gates abstractions on top. See [`commands/refactor.md`](../../../../../commands/refactor.md).
- Dispatched by `/optimize` Phase 2 (tactical) when class = refactoring.
- Dispatched by `/align-recheck` when the finding's class = refactoring.
- NOT dispatched by `/align-fast`. That command dispatches align's own per-finding loop (`find-and-align`) over the closed 21-verb align vocabulary, which does not contain these 10 Fowler verbs; a row that wants one is mis-classified and `/align-fast` routes it to `/refactor`, which is where this skill runs.
- NOT for new code or features — refactoring operates on existing code only.

## The 10 closure verbs

**The numbers in the fingerprints below are fix triggers, not findings** (D-7). Each is a default — the project's configured linter value wins (`THR-FN-LEN`, `THR-COMPLEXITY` in `governance/thresholds.json`). A fingerprint says which verb fits a function someone already decided to change; it never makes a function a finding by itself (`precedents/code-quality.md` § 51). Which functions are worth changing comes from impact — `architectural-diagnosis` § 9 hotspots, a `/quality-audit` row, the finding that dispatched this skill.

### 1. extract-method

**Fingerprint**:
- Function ≥ 30 lines, OR
- Cyclomatic complexity ≥ 10, OR
- A block of 5+ lines doing distinct work that has its own narrative (and could be named).

**Procedure**:
1. Identify the contiguous block to extract.
2. Detect free variables (referenced but not defined locally) → these become parameters.
3. Detect mutations the block performs → if the block mutates outer state, either pass by reference (preferred for objects) OR return the new value and reassign.
4. Pick a verb-noun name (e.g., `validateOrderTotals`, `formatCustomerAddress`).
5. Move the block to a new method/function in the same file (private OR file-local).
6. Replace the original block with a call.
7. Run lint + typecheck + scoped tests.

**Verify**: tests green; coverage ≥ before; no public API changed.

**Example**:
```ts
// before — 45-line function doing 3 things
function processOrder(o: Order) {
  // 12 lines of validation
  // 18 lines of pricing
  // 15 lines of persistence
}
// after
function processOrder(o: Order) {
  validateOrder(o);
  const priced = priceOrder(o);
  return persistOrder(priced);
}
```

### 2. extract-class

**Fingerprint**:
- A class has ≥ 3 distinct responsibility clusters (group methods by what state they read/write).
- A subset of methods only operate on a subset of fields (data clump).

**Procedure**:
1. Identify the responsibility cluster + the field subset it operates on.
2. Create a new class containing those fields + methods.
3. Replace direct field access in the original class with delegation through the new class.
4. Update the original class's constructor to instantiate the new class.
5. Run tests.

**Verify**: tests green; original public API preserved (callers don't see the split).

### 3. extract-param-object

**Fingerprint**:
- Function with ≥ 5 parameters, OR
- 3+ parameters that always travel together across multiple call sites (e.g., `(start, end, granularity)` everywhere).

**Procedure**:
1. Define a struct/interface/dataclass for the parameter group.
2. Update the function signature to take the param object.
3. Update all call sites to construct the param object.
4. Run tests.

**Verify**: tests green; no behaviour change.

### 4. flatten-conditional

**Fingerprint**: nested conditional depth ≥ 3 levels (`if (a) { if (b) { if (c) { … } } }`).

**Procedure** (pick the right pattern per shape):
- **Guard clauses** (when each level is a precondition):
  ```ts
  // before
  function f(o) {
    if (o) {
      if (o.user) {
        if (o.user.active) { return doWork(o); }
      }
    }
  }
  // after
  function f(o) {
    if (!o) return;
    if (!o.user) return;
    if (!o.user.active) return;
    return doWork(o);
  }
  ```
- **Polymorphism** (when each branch handles a different type):
  ```ts
  // before
  if (kind === 'A') doA() else if (kind === 'B') doB() else doC();
  // after
  handlers[kind]();
  ```
- **Strategy/lookup** (when each branch is a different rule):
  ```ts
  const strategies = { A: doA, B: doB, C: doC };
  strategies[kind]();
  ```

**Verify**: tests green; cyclomatic complexity reduced.

### 5. move-to-module

**Fingerprint**: a function in module A operates exclusively on types/data owned by module B. Module A is the wrong home.

**Procedure**:
1. Identify the function and its dependencies.
2. Move the function to module B.
3. Update all import paths in the codebase (use codemod or grep+sed).
4. Run tests + typecheck.
5. Verify no cyclic dependency was introduced.

**Verify**: tests green; no new cycles in `_dep-graph.json`; consumers import from the right module.

### 6. replace-magic-with-constant

**Fingerprint**: literal numbers/strings repeated ≥ 2 times in the same file, OR a single magic value with non-obvious meaning (e.g., `if (status === 7)` where 7 means "shipped").

**Procedure**:
1. Pick a meaningful name (`SHIPPED_STATUS`, `MAX_RETRIES`, `DEFAULT_PAGE_SIZE`).
2. Define a constant at the appropriate scope (file-level for file-local; module-level for shared).
3. Replace all occurrences.
4. If the constant is project-wide, prefer the project's existing config / constants module.

**Verify**: tests green; behaviour identical.

### 7. replace-temp-with-query

**Fingerprint**: a local variable is assigned once from an expression, used once or twice immediately after, then discarded.

**Procedure**:
- If the expression is cheap and the temp adds no clarity → inline it.
- If the expression is expensive but used multiple times → leave it as is (don't refactor).
- If the temp is a "named result of a query" → consider extracting the expression as its own method instead.

**Verify**: tests green.

### 8. replace-loop-with-pipeline

**Fingerprint**: a manual `for` loop builds an array/object via push/assignment, when a pipeline (map/filter/reduce) would express the intent more directly.

**Procedure**:
- `for + push when condition` → `array.filter(condition).map(transform)`.
- `for + accumulator` → `array.reduce(...)`.
- `for + early return` → keep the loop OR use `array.find` / `array.some` / `array.every`.

**Verify**: tests green; performance check (pipelines can be slower for very hot paths — measure if hot).

### 9. rename

**Fingerprint**: a name is unclear:
- Single-letter (except `i` in tight loops, `e` in error handlers).
- Generic (`data`, `info`, `tmp`, `result`, `value`, `obj`, `item` — when a domain name exists).
- Misleading (`getUser` that returns multiple users; `isValid` that returns a number).
- Misspelled or grammatically wrong (`getUseres`, `is_actived`).

**Procedure**:
1. Pick the right name (verb-phrase for functions returning a value or doing work; noun-phrase for objects/data; `is_/has_/can_` for booleans).
2. Use the IDE's rename refactoring (or careful grep+sed).
3. Update tests + comments referencing the old name.
4. Run lint + typecheck.

**Verify**: tests green; no orphan references to old name.

### 10. encapsulate

**Fingerprint**: a public field is being mutated by external code; OR a mutable global is being read directly across modules.

**Procedure**:
1. Make the field private.
2. Add a getter (and setter if controlled mutation is allowed).
3. Update external mutations to go through the setter (or, better, through a domain method that names the operation).
4. Add invariant checks in the setter if relevant.
5. Run tests.

**Verify**: tests green; the field is no longer publicly mutable.

## Procedure (the skill's overall flow)

1. **Receive finding** with `class: refactoring`, `subclass: <verb>`, evidence `<path:line>`.
2. **Pre-flight**:
   - Working tree must be clean (or `--allow-dirty` set on the parent run).
   - Lint + typecheck green at HEAD.
   - Tests covering the affected file are green.
3. **Apply the verb's procedure** above.
4. **Verify**:
   - Lint green.
   - Typecheck green.
   - Scoped tests green.
   - Coverage ≥ before.
   - For `extract-method` / `extract-class` / `extract-param-object`: callers compile.
   - For `move-to-module`: no new cycles in `_dep-graph.json`.
   - For `rename`: no orphan references (grep the old name; should return zero hits).
5. **Commit** with message `refactor(<scope>): <verb> — <one-line description>`.
6. **Re-detect** the finding's fingerprint — should now return zero hits at the original location.

## Hard rules

- **Behaviour-preserving** — observable output of the affected functions is identical (same inputs → same outputs / side effects).
- **Net-lines** — slight + or - is allowed (refactoring is allowed to add a function definition); aim ≤ 0 over the run.
- **One verb per commit** — don't bundle (`extract-method` + `rename` in same commit is forbidden).
- **No new abstractions — and here is the line, because three verbs above create symbols.** `extract-class` creates a class, `extract-param-object` creates a struct/interface/dataclass, and `flatten-conditional`'s polymorphism/strategy sub-patterns create a handler set. Read literally, "no new symbols" would forbid the verbs this skill exists to apply, and the `refactorer` agent's auto-halt on "adds new symbols" would fire on every one of them. The rule the pack actually means:

  > **A symbol that is an EXTRACTION of code already present in the scope is permitted. A symbol that introduces a CONCEPT not already present halts.**

  The test is not "did a new name appear" — it is **"could a reader point at the lines this name now holds, in the pre-change code?"**

  | Permitted (extraction — the code was already there) | Halts (introduction — the concept is new) |
  |---|---|
  | `extract-method` — a block becomes a named function | A base class or interface invented so two types can share a signature |
  | `extract-class` — fields + the methods that touch them move out together | A `Repository`/`Service`/`Manager` layer the project does not have |
  | `extract-param-object` — a parameter list that already travels together gets a name | A value object with new invariants or validation the parameters did not enforce |
  | `flatten-conditional` → polymorphism — each existing branch body becomes a handler | A strategy registry, plugin point, or extension seam with no second implementation today |
  | `move-to-module` — a symbol relocates | A new utility namespace created to hold it |

  Two mechanical checks, both cheap: (1) the extracted body appears in the diff as a **move**, not as new logic — `git diff -M` should show it as relocated lines; (2) **net behaviour surface is unchanged** — no new branch, no new validation, no new default. If either fails, it is `introduce-abstraction`, which is an architectural verb owned by the `architectural-diagnosis` skill, not a refactoring verb. Halt and route it there.
- **No public API changes** — if a refactor would change a public symbol's signature/name, halt and surface as user-decision.
- **Re-detect after each fix** — fingerprint must disappear at the source location.

## Failure modes

- **Tests fail after refactor** → revert; mark the finding `halted` with reason; surface for user.
- **Public API would change** → halt; surface as user-decision (it's not behaviour-preserving in the contract sense).
- **An "extraction" that grew a branch** → the new symbol validates, defaults, or short-circuits something the original did not. That is not an extraction; it is a behaviour change wearing a refactoring verb's name. Revert, then decide whether the behaviour change is wanted on its own merits.
- **Refactor would introduce a cycle** → halt; the verb was wrong choice; suggest `decouple-cycle` (architectural) instead.
- **Performance regression detected** (hot-path refactor) → revert; mark `halted` with measurement evidence.

## Examples per verb

(See "The 10 closure verbs" section above; each verb has a worked example.)

## References

- `engineering-principles.md` (this pack) — the principles refactoring restores.
- `quality-principles.md` (this pack) — clean-code rules driven by these verbs.
- `architectural-diagnosis.md` — handles foundation moves (different scope).
- `align-discipline.md` — the closed-vocabulary discipline refactoring inherits from.
