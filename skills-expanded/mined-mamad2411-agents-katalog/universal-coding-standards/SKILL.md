---
name: universal-coding-standards
description: Marcus Daley's universal coding standards and critical rules for access control, initialization, communication patterns, dependencies, comments, and error handling across all languages and frameworks.
user-invocable: false
---

# Universal Coding Standards

> Portable coding standards for AI agents, skill files, and cross-project consistency across ALL programming languages, frameworks, and platforms.

## Description

Defines the non-negotiable coding rules that apply to every project Marcus works on. Covers access control and encapsulation, initialization discipline, event-driven communication, dependency management, comment standards, error handling, and a comprehensive anti-patterns list. Language-specific guidance is provided for C++, C#, Python, TypeScript, Rust, Java, Go, and React.

## Prerequisites

- None -- these standards apply universally regardless of tooling

## Usage

These standards are auto-loaded context. When generating or reviewing code for Marcus, check every implementation against these rules before presenting it.

1. Before writing code, verify the implementation follows access control rules
2. Ensure all defaults are set at construction, no magic numbers/strings
3. Use event-driven communication, never polling
4. Minimize dependencies in declaration files
5. Write comments explaining WHY, not WHAT
6. Validate inputs at system boundaries, handle errors explicitly

### Prompt Pattern

```
Review this [language] code against Marcus's universal coding standards.
Check: access control, initialization, communication patterns, dependencies, comments, error handling.
Flag any violations and suggest fixes.
```

## Core Philosophy

### The 95/5 Rule

95% of code should be reusable across projects without modification. Only 5% should be project-specific configuration.

- **General**: Separate business logic from configuration. Core algorithms should be framework-agnostic where possible.
- **Web Dev**: Components reusable across pages/apps. API handlers decoupled from specific routes. Utility functions in shared libraries.
- **Game Dev**: Gameplay systems work regardless of specific game content. Data-driven design over hardcoded values.
- **Backend**: Service logic independent of transport layer (HTTP, gRPC, WebSocket). Database queries abstracted behind repository patterns.

### Quality Over Speed

Never suggest shortcuts, 'quick and dirty' solutions, or time-pressure language. This is portfolio work where architectural quality matters more than delivery speed. Refactoring is encouraged as a portfolio investment, not wasted time.

### Configuration-Driven Design

NEVER hardcode values that could change. Everything configurable must be driven by configuration files, environment variables, constructor parameters, or data stores.

| Context | Approach |
|---------|----------|
| Any language | Constants, config files, or environment variables instead of magic numbers/strings |
| Web dev | .env files, config objects, theme tokens. Never hardcode API URLs, colors, breakpoints |
| Game dev | Data assets, scriptable objects, config files. Never hardcode gameplay values |
| Backend | Environment variables, config services, feature flags. Never hardcode connection strings |

## Access Control & Encapsulation

**Severity: CRITICAL -- NEVER VIOLATE**

Every property and method should have the most restrictive access level that allows it to function correctly.

### Read-Only Public State

Runtime state that external code needs to read but should never modify directly (e.g., current health, auth status, connection state, cart total).

| Language | Implementation |
|----------|---------------|
| C++ | Getter functions or const references. UE5: VisibleAnywhere + BlueprintReadOnly |
| C# | `{ get; private set; }` properties |
| TypeScript | `readonly` keyword or getter-only properties |
| Python | `@property` decorator without setter |
| Java | Private field with public getter, no setter |
| Rust | `pub` for the getter, keep field private |

### Class-Level Configuration

Values configured once per class/type that apply to all instances (e.g., base damage for weapon type, default timeout, theme colors for variant).

| Language | Implementation |
|----------|---------------|
| C++ (UE5) | EditDefaultsOnly. Generally: constructor parameters or static config |
| TS/React | defaultProps, component-level constants, or theme tokens |
| Python | Class-level attributes set in `__init__` with defaults |
| General | Constructor parameters with sensible defaults |

### Instance-Level Configuration

Values that differ per instance, set at creation or deployment time (e.g., API endpoint URL, DB connection string, team ID).

| Language | Implementation |
|----------|---------------|
| C++ (UE5) | EditInstanceOnly. Generally: constructor injection or setter-once patterns |
| Web | Environment variables, .env files, runtime config objects |
| General | Dependency injection, factory methods, builder patterns |

### BANNED: Unrestricted Access

NEVER expose mutable state without controlled access. Creates confusion about who modifies what, leads to bugs where multiple systems modify the same state without coordination.

Bad examples:
- C++ UE5: EditAnywhere (ambiguous class vs instance editing)
- JS/TS: Exporting mutable objects without encapsulation
- Python: Public mutable attributes without property decorators
- Any: Global mutable state accessible from anywhere

## Initialization Rules

**Severity: CRITICAL -- NEVER VIOLATE**

### All Defaults at Construction

ALL default values must be set at the point of construction/initialization, not scattered throughout the codebase.

| Language | Where to Set Defaults |
|----------|----------------------|
| C++ | Constructor initialization list exclusively. Never in header declarations |
| C# | Constructor or field initializers. Prefer constructor for complex defaults |
| TypeScript | Constructor or default parameter values. Avoid defaults in lifecycle methods |
| Python | `__init__` method with explicit defaults. Never mutable default arguments |
| Rust | Default trait implementation or builder pattern |
| React | Default props or default parameter values in function components |

### No Magic Numbers or Strings

Extract to named constants, config values, or enum members.

- Bad: `if (retryCount > 3)` or `if (status === 'active')`
- Good: `if (retryCount > MAX_RETRY_ATTEMPTS)` or `if (status === UserStatus.Active)`

### Initialize at Declaration

Initialize all variables at declaration when possible. Prevents use-before-initialization bugs.

## Communication Patterns

**Severity: CRITICAL -- NEVER VIOLATE**

Systems communicate through events/callbacks/delegates (Observer pattern), NEVER through polling.

### Event-Driven Communication

| Language | Implementation |
|----------|---------------|
| C++ (UE5) | DECLARE_DYNAMIC_MULTICAST_DELEGATE with BlueprintAssignable |
| C++ (general) | std::function callbacks, signals/slots, or observer interfaces |
| C# | Events and delegates, or IObservable<T> |
| TypeScript | EventEmitter, RxJS Observables, custom event bus, or React context with useReducer |
| Python | Signals (Django/Qt), callbacks, or observer pattern implementations |
| Rust | Channels (mpsc), callbacks, or trait-based observer pattern |
| React | State lifting, context + reducers, or state management libraries (Zustand, Redux) |
| Web | CustomEvent, EventTarget, WebSocket messages, Server-Sent Events |

### BANNED: Polling

- Bad: `setInterval(() => { if (dataChanged()) updateUI(); }, 100)`
- Good: `dataStore.on('change', (newData) => updateUI(newData))`

### Decouple Producers from Consumers

The system broadcasting a state change should not know or care who is listening. Enables adding new listeners without modifying the broadcaster.

### Clean Up Subscriptions

Always pair subscribe with unsubscribe in lifecycle.

| Language | Cleanup Location |
|----------|-----------------|
| C++ (UE5) | Unbind delegates in EndPlay or NativeDestruct |
| React | Return cleanup function from useEffect |
| JavaScript | removeEventListener in cleanup/teardown |
| C# | Unsubscribe in Dispose or destructor |

## Dependency Management

**Severity: CRITICAL -- NEVER VIOLATE**

### Minimize Interface Dependencies

Every unnecessary dependency cascades to all consumers, increasing build times and coupling.

| Language | Approach |
|----------|----------|
| C++ | Forward declarations in headers, full includes only in .cpp. `.generated.h` MUST be last include in UE5 headers |
| TypeScript | Import only what you use. Prefer `import type { X }` for type-only imports |
| Python | Avoid circular imports. Use `TYPE_CHECKING` guard for type-hint-only imports |
| Java | Minimize wildcard imports. Import specific classes |
| General | Depend on abstractions (interfaces/protocols), not concrete implementations |

### Dependency Injection Over Hard-Coded Instantiation

- Bad: `class OrderService { private db = new PostgresDB(); }`
- Good: `class OrderService { constructor(private db: Database) {} }`

### Composition Over Inheritance

Composition is more flexible, avoids deep hierarchies, easier to test and reuse. Inheritance is appropriate only when there's a genuine 'is-a' relationship with substantial shared behavior.

## Comment Standards

Explain WHY (design decisions), not WHAT (obvious syntax). Write for future developers.

### Comment Syntax by Language

| Language | Inline | API Documentation |
|----------|--------|-------------------|
| C++ | `//` only. NEVER `/* */` (reads as AI generated) | Doxygen-style if needed |
| Python | `#` for inline | Docstrings (triple quotes) for function/class docs |
| JS/TS | `//` for inline | JSDoc `/** */` only for function/class API docs |
| C# | `//` for inline | XML doc comments `///` for public API |
| Rust | `//` for inline | `///` for doc comments on public items |

### Good Comment Candidates

- Why a particular algorithm or data structure was chosen over alternatives
- Business rules that aren't self-evident from the code
- Workarounds for framework/library bugs with links to issues
- Performance considerations that influenced the implementation
- Edge cases the code specifically handles and why

### File Header Standard (Required)

Every source file must have a header:

```
// FileName.ext
// Developer: Marcus Daley
// Date: [Creation Date]
// Purpose: [Brief description of file/class purpose and usage]
```

Adapt comment syntax to the language (`#` for Python, `//` for JS/TS/C++/C#/Rust/Go).

## Error Handling

### Validate at Boundaries

Validate inputs at system boundaries (API endpoints, user input, external data). Internal code can assume validated data.

### Null/Undefined Checks

In unsafe languages (C++, C#, Java), check before every pointer/reference dereference. In TypeScript, use strict null checks. In Rust, the type system handles this. In Python, check for None at boundaries.

### Typed Error Handling

| Language | Approach |
|----------|----------|
| TypeScript | Return Result types or typed errors. Avoid `catch(e: any)` |
| Rust | `Result<T, E>` with custom error types. `?` operator for propagation |
| Python | Specific exception types. Never bare `except:` |
| Go | Return `(value, error)` tuples. Check errors explicitly |
| C++ | Consider `std::optional`, `std::expected`, or return codes alongside exceptions |

### Fail Fast

If something is wrong, error immediately with a clear message rather than continuing with bad data.

## Anti-Patterns (NEVER Do)

| Anti-Pattern | Use Instead |
|-------------|-------------|
| Unrestricted mutable public state | Controlled access through getters/setters, readonly, encapsulated state |
| Default values scattered across codebase | All defaults in constructors/initializers in one location |
| Polling loops to detect state changes | Event-driven Observer pattern |
| Importing everything in declaration files | Forward declarations, type-only imports, minimal dependencies |
| Hardcoded config values (magic numbers, URLs, colors) | Named constants, config files, env vars, data-driven design |
| Direct cross-system calls (tight coupling) | Events, dependency injection, interfaces, mediator pattern |
| Block comments for code explanation | Line comments explaining WHY. Block only for API docs |
| Comments explaining WHAT code does | Comments explaining WHY (design decisions, trade-offs) |
| Modifying shared/global build config for project needs | Project-level config files |
| 'Quick and dirty' solutions | Quality-first approach with proper architecture exploration |
| Global mutable state (god objects) | Scoped state, dependency injection, context providers |
| Catching and swallowing errors silently | Handle explicitly, log, propagate when appropriate |
| Committing secrets or .env files | .gitignore, environment variables, secret management |

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| applies_to | all languages | Which languages/frameworks these rules cover |
| severity_level | critical | Rules marked CRITICAL are never violated |
| file_headers | required | Every source file gets a standard header |

## File Structure

```
universal-coding-standards/
  SKILL.md              # This skill definition
  README.md             # Quick-start guide
  resources/
    access-control.md   # Detailed access control examples
    anti-patterns.md    # Extended anti-patterns with code samples
```

## Notes

- These standards are derived from AAA studio practices taught by Nick Penney at Full Sail University, generalized for universal software engineering.
- The 95/5 Rule is the cornerstone: build reusable systems, not one-off solutions.
- When in doubt about any rule, the answer is: use the most restrictive, most explicit, most event-driven approach.
