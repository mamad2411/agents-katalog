# Claude Code — Global Clean Code Rules

Inspired by Robert C. Martin, Martin Fowler, Kent Beck, and Neal Ford.
These rules apply to every project, every language, every file.

---

## Non-Negotiable Rules

- **Cyclomatic complexity < 7** on every function or method (the Cyclomatic Complexity Threshold, per `DOMAIN_DICTIONARY.md`) — no exceptions
- **Unit test coverage ≥ 85%** of the lines each change adds or modifies, and every test able to fail (ADR-008)
- **Every external dependency** (DB, HTTP, filesystem, clock, queue) hides behind an interface
- **Models and factories** are always separate files following the naming convention
- **SOLID principles** apply at all times — one reason to change per class

---

## File Naming

All files follow: `name.type.extension` using the language's conventional casing.

| Language   | Convention  | Example                        |
|------------|-------------|--------------------------------|
| TypeScript | kebab-case  | `user-repository.interface.ts` |
| Go         | snake_case  | `user_repository.go`           |
| Python     | snake_case  | `user_repository.py`           |
| Java       | PascalCase  | `UserRepository.java`          |

### Type segments by language

**TypeScript:** `.interface.ts` · `.model.ts` · `.factory.ts` · `.service.ts` · `.controller.ts` · `.repository.ts` · `.enum.ts` · `.type.ts` · `.spec.ts` · `.fixture.ts`

**Go:** `_repository.go` · `_service.go` · `_factory.go` · `_handler.go` · `_test.go`

**Python:** `_repository.py` · `_service.py` · `_factory.py` · `_model.py` · `_enum.py` · `test_*.py` · `_fixture.py`

**Java:** `Repository.java` · `Service.java` / `ServiceImpl.java` · `Factory.java` · `Controller.java` · `Test.java` · `Fixture.java`

---

## Complexity

If complexity is approaching 7, apply in order:

1. Use early returns / guard clauses to flatten nesting
2. Extract inner logic into well-named private functions
3. Replace `if/else` chains with lookup tables or dispatch maps
4. Replace `switch` on type with polymorphism (Strategy, State)
5. Never exceed 2 levels of nesting in a single function

---

## Legacy Code & Refactoring

- When modifying untested or legacy code, identify a seam and write characterization tests that capture
  the current behavior before changing it, even when that behavior is flawed.
- Keep refactoring and behavior changes in separate commits, and finish each one — tests green, then
  cleaned up — before moving to the next change.

---

## Design Patterns

Apply Gang of Four patterns when they solve a real problem. Never apply them to look clever.

| Pattern   | When to use                                                    |
|-----------|----------------------------------------------------------------|
| Factory   | Object creation is complex or varies by type                   |
| Builder   | Object has many optional parameters                            |
| Strategy  | Behaviour varies by context; eliminates conditionals           |
| Observer  | Event-driven decoupling between producers and consumers        |
| Adapter   | Wrapping third-party or legacy dependencies                    |
| Decorator | Adding behaviour (logging, caching) without touching the class |
| Command   | Encapsulating operations; supporting undo/redo or queuing      |

---

## Models

- No database or HTTP logic inside models
- Computed properties and domain logic belong on the model
- Prefer immutability: `readonly` (TS) · value receiver (Go) · `frozen=True` (Python) · `record` (Java)
- Models are never responsible for their own persistence

## Factories

- Factories are the only place `new` is called on complex domain objects outside of tests
- One factory file per domain entity
- Static methods for named creation scenarios (`createAdmin`, `createGuest`, `newFromEvent`)

## Interfaces

- Define interfaces in the **consumer** package, not the provider
- Keep interfaces small — prefer many focused interfaces over one fat one
- Name interfaces for what they do, not what implements them: `UserRepository` not `IUserRepository`

---

## Testing

Follow **Arrange / Act / Assert** in every test. One concept per test.

- Mock all external dependencies — never touch real databases or networks in unit tests
- Use `create_autospec` (Python), `jest.Mocked<T>` (TS), table-driven tests (Go), `@Mock` (Java)
- Fixtures live in a dedicated `fixtures/` directory and are reused across specs
- Test names describe behaviour: `returns null when user does not exist` not `test_find_by_id_2`

---

## What Claude Must Flag

Flag these immediately with explanation and a suggested fix:

- Cyclomatic complexity >= 7
- Changed-line coverage below 85%, or a test that cannot fail
- Boolean parameter on a public method (split into two functions)
- File name not following `name.type.extension` convention
- Direct instantiation of an infrastructure dependency inside a service or model
- Missing interface for any external dependency
- Function longer than 20 lines without clear justification
- Magic number or string literal inside business logic
- Nesting deeper than 2 levels
- Class with more than one clear reason to change
- `new` called on a complex domain object outside a factory or test

---

## Context Awareness & Configuration Mastery

- **Environment Debugging**: When asked to fix PATH or environment configuration issues, immediately check shell config files (`.zshrc`, `.bashrc`, `.bash_profile`) rather than suggesting workarounds.
- **Communication Patterns**: When user references 'these changes' or 'that script' without context, check recent messages and working directory first before asking for clarification.
- **Project Structure**: For agent/configuration lookups, prioritize checking `.claude/`, `.cursor/`, `.gemini/` or `config/` directories first rather than searching todo files or past outputs.

---

## Git Commits

Conventional Commits format:

```
feat(scope):     add behaviour
fix(scope):      correct broken behaviour
refactor(scope): restructure without changing behaviour
test(scope):     add or update tests
chore(scope):    tooling, CI, dependencies
docs(scope):     documentation only
```

Subject line: imperative mood, under 72 characters, no trailing period.
Body: explain *why*, not *what*.

---

## Naming

- Functions and variables reveal intent: `isPaymentValid`, `calculateTax`, `activeUsers`
- Booleans: `is`, `has`, `can`, `should` prefix
- No abbreviations: write `configuration` not `cfg`, `manager` not `mgr`
- No generic names: `data`, `info`, `handler`, `manager` — be specific
- Functions do one thing; if you need `and` in the name, split it

---

*Full reference with language examples: `docs/clean-code-guidelines.docx`*
