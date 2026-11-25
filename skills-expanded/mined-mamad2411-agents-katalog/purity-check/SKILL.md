---
name: purity-check
description: >
  Enforces functional-core purity rules: PURE-1 (no side effects in core/
  modules — no I/O, no clock, no RNG, no logging), PURE-2 (no ambient/global
  state reads in core), PURE-3 (mock-required-to-test signal — if a function
  needs a mock to test, it isn't pure and belongs in shell). Loaded by the
  conductor for write and review operations when core-layer code is in scope.
  Layer detection follows the conductor's Section 14.
version: "1.0.0"
last-reviewed: "2026-05-13"
languages: [typescript, python, go, rust, javascript]
changelog: "../../CHANGELOG.md"
tools: Read, Grep, Glob, Bash
model: opus
permissionMode: default
---

# Purity Check — Functional Core Enforcement

The functional core / impure shell pattern is the single biggest lever for
keeping AI-generated code testable and reasonable. Pure functions:
- Need no DI container, no mocks, no fixtures — only inputs and outputs.
- Are trivially testable: literal inputs, literal expected outputs.
- Don't decay under refactors (no hidden coupling to globals).
- Don't surprise readers (everything they read is in the signature).

This skill enforces purity *only on files in `core/`* (per the conductor's
Section 14 layer detection). Shell code is allowed to do I/O, read env vars,
and so on — that's its job.

---

## Rules

### PURE-1 — No Side Effects in Core
**Severity**: BLOCK | **Languages**: * | **Source**: CCC

**What it prohibits**: Files in `core/` (or legacy-fallback paths `domain/`,
`entities/`, `models/`) performing or importing:

- **I/O**: `fs.*`, `open(`, `pathlib.*`, network calls (`fetch`, `requests`,
  `httpx`, `axios`, `reqwest`), DB drivers (`pg`, `mysql2`, `sqlalchemy`,
  `mongoose`, `redis`, `pymongo`).
- **Frameworks**: HTTP framework imports (`express`, `fastapi`, `flask`,
  `nest`, `hapi`, `actix`), template engines, message brokers.
- **Clock/time**: `Date.now()`, `time.time()`, `time.Now()`, `Instant::now()`,
  `chrono::Utc::now()`.
- **Randomness**: `Math.random()`, `random.*`, `rand::*`, `crypto.randomBytes()`.
- **Logging**: `console.*`, `print(`, `logging.*`, `log.*` calls.

**Allowed in core**:
- Pure language stdlib: `Math`, `JSON.parse`, `json.loads`, string/array
  manipulation, collection types.
- Type-only imports (TypeScript `import type`, similar).
- Other core modules.

**Detection**:
1. For each file in `core/`: grep imports for the prohibited list.
2. Grep function bodies for calls to clock/RNG/logging functions.
3. Flag every match.

**agent_action**:
1. Cite: `PURE-1 (BLOCK): Side effect in core file: '{call}' at {file}:{line}.`
2. Identify the side effect (I/O, time, randomness, logging).
3. Propose: receive the result as a parameter from shell (e.g., `now: Date`,
   `random_seed: number`, `db_rows: Order[]`), or move this function to shell
   if the side effect is unavoidable.
4. DO NOT produce new core code containing the side effect.

**Bypass prohibition**: "It's just a log line" / "It's just `Date.now()`" →
That's exactly the kind of impurity that destroys testability. Receive the
time as a parameter; the shell call site is the place to read the clock.

---

### PURE-2 — No Ambient or Global State Reads in Core
**Severity**: WARN | **Languages**: * | **Source**: CCC

**What it prohibits**: Core code reading from process-level ambient state:
- `process.env.*` / `os.environ.*` / `std::env::var(`
- Module-level mutable globals (a `let counter = 0; export function inc() { counter++ }`)
- Thread-locals and request-scoped context singletons
- Service locators (`Container.get`, `ServiceLocator.resolve`) — overlaps
  with `arch-check`'s BOUND-3

**Why WARN, not BLOCK**: Sometimes module-level constants are legitimate
(`const PI = 3.14159`); sometimes "globals" are actually frozen data tables.
The rule needs human judgment.

**Detection**:
1. Grep core files for `process.env`, `os.environ`, `getenv`, `std::env::var`.
2. Look for module-level `let`/`var`/`mut` declarations of non-const types.
3. Identify thread-local accessors per language idiom.

**agent_action**:
1. Cite: `PURE-2 (WARN): Core reads ambient state '{name}' at {file}:{line}.`
2. Propose: read the value in shell at startup, pass it into the core function
   as an explicit parameter.

---

### PURE-3 — Mock-Required-to-Test Signal
**Severity**: INFO | **Languages**: * | **Source**: CCC

**What it surfaces**: A function in `core/` whose test file imports a mocking
library (jest mocks, `unittest.mock`, gomock, mockall, etc.). This rule
*reports*, not blocks — TEST-NO-MOCK-FOR-PURE in `test-check` is the BLOCK
version. PURE-3 is the lower-priority signal during write/refactor sessions
that a function's purity is in question.

**agent_action**:
1. Cite: `PURE-3 (INFO): Core function '{name}' has a test that imports mocks. Consider whether the dependencies should move to shell.`
2. Cross-reference with TEST-NO-MOCK-FOR-PURE if a review is also running.

---

Per-language detection patterns (I/O libraries, clock/RNG calls, mocking
libraries to recognise): see `references/{language}.md`.

Report schema: see `skills/conductor/shared-contracts.md`.

**Severity overrides**: `PURE-1`, `PURE-2`, `PURE-3` are paradigm-family
rules; a project may shift their severity (`BLOCK` / `WARN` / `INFO`) via
`.codex/config.json` `severity_overrides`. Defaults stay as documented
above. See conductor §7.1.
