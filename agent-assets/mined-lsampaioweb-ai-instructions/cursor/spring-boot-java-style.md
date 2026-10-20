---
description: "Java coding style contract for imports, visibility, annotations, constants, records, method structure, JavaDoc, and mandatory verification after edits."
globs: "**/src/**/*.java"
alwaysApply: false
---

# Java Style Contract

## Formatting

- Use exactly two spaces per indentation level in every Java file. Never use tabs, and
  never use non-two-space indentation, regardless of what an IDE or generator produced by
  default.

## Imports

- Order imports in four groups, separated by exactly one blank line between groups,
  omitting any group that has no members:
  1. Static imports.
  2. `java.*` / `jakarta.*` standard/platform imports.
  3. Third-party imports (Spring, other framework, and library packages).
  4. Project-local imports.
- Import each type explicitly; wildcard imports are forbidden.
- Remove unused imports before finishing a file.

## Visibility and dependency injection

- Declare every field and helper method with the most restrictive visibility that
  satisfies its usage scope; default to `private`, expanding only when external access is
  required.
- Use constructor injection for every dependency; never use field injection or setter
  injection.
- Do not add `Objects.requireNonNull(...)` guards in constructors of classes that are
  instantiated exclusively by the framework's dependency injection container (services,
  repositories, controllers) - the container guarantees a non-null dependency graph and
  the check only adds boilerplate.
- Use `Objects.requireNonNull(...)` in constructors of classes that can be instantiated
  directly by arbitrary calling code outside of the DI container (for example
  configuration/properties holders built from parsed values, or public utility classes),
  where a null argument would otherwise fail confusingly downstream.
- Do not expose implementation details through public fields or helper methods unless
  they are part of a real API contract (e.g., a documented constant shared across
  classes).

## Annotation order

- Order class-level annotations as:
  1. Logging annotation (e.g., `@Slf4j`).
  2. Framework stereotype annotation (e.g., `@Service`, `@Repository`, `@Controller`,
     `@RestController`, `@Component`, `@ConfigurationProperties`).
  3. Lombok generation annotations other than the logging annotation (e.g.,
     `@RequiredArgsConstructor`).
  4. Behavioral/validation annotations (e.g., `@Validated`).
- Annotate every method that implements or overrides an interface/superclass method with
  `@Override`.
- Keep annotations directly attached to the declaration they annotate; never separate an
  annotation from its target with a blank line or comment.
- Do not use `@Data`, `@Builder`, `@AllArgsConstructor`, or `@NoArgsConstructor` on
  business classes (services, repositories, controllers). Lombok ownership of allowed
  annotations and record preference is in the Lombok contract.

## Constants

- Extract a string literal into a `private static final String` constant in
  `UPPER_SNAKE_CASE` whenever it is reused across methods, or whenever it is a
  message-resolution key (passed to an exception, a logging message helper, or an
  equivalent lookup) even if used only once, since these keys are part of the
  class's externalized-message contract.
- Prefer domain-specific constant names (e.g., `LOG_USER_UPDATING`,
  `ERROR_SORT_PROPERTY_INVALID`) over generic names (e.g., `MESSAGE`, `VALUE`).
- Place constants near the top of the class, immediately after any logger declaration.
- One-off literals with no reuse and no message-key role (e.g., a single SQL parameter
  name used once) may remain inline.

## Records

- Use Java records only for simple immutable data carriers: DTOs, domain/value models,
  configuration-properties holders, and small nested value types.
- Never declare a service, controller, repository, or other business-logic class as a
  record.

## Method structure

- Order members within a class as: fields/constants, constructor(s), public methods,
  package-private methods, private helper methods.
- Name helpers by intent, not by generic verbs; prefer names like `parseSortOptions()` or
  `getSupportedLocales()` over `build`, `compute`, `process`, or `handle`.
- Extract multi-statement logic, complex boolean conditions, or non-trivial collection
  construction into a named private helper when it improves readability; do not extract a
  helper purely to look structured when the logic is already clear inline.
- Add one blank line before a method's final `return` statement when the method body has
  preceding statements; omit the blank line when the method is a single-statement
  return.

## JavaDoc

- Add a JavaDoc `/** ... */` comment to every public and protected class, interface, and
  method.
- Start each summary with one concise sentence ending in a period.
- Add `@param`, `@return`, and `@throws` tags only when the contract is not already
  obvious from the method name, parameter names, and summary.
- Place the JavaDoc block immediately before the declaration, including before any
  annotations.
- Package-private and private members do not require JavaDoc, though a short comment is
  welcome when the intent is non-obvious.

## Expressions and flow control

- Use `var` only when the inferred type is unambiguous from the right-hand side.
- Use the ternary operator only for single-expression assignments; do not nest ternaries.
- Prefer early returns and guard clauses over deeply nested conditionals.
- Do not introduce APIs marked deprecated for removal; use the supported replacement
  available in the dependency versions resolved by the module's build.

## Mandatory verification after changes

- After creating or editing any Java file, compile the affected module
  (`mvn compile`, or `mvn test-compile` if test sources were touched) before considering
  the change complete. A "no errors in the editor" impression is not a substitute for an
  actual build.
- If any test source file was created or edited, or if a change could affect existing
  test behavior, run the module's tests (`mvn test`), not just `mvn compile`/
  `mvn test-compile`. Compiling only proves the code builds; it does not prove existing
  behavior still passes.
- When a test fails after a change, first determine whether the same test already failed
  before the change (for example, by checking against the previous committed state)
  before concluding the change caused the failure. Do not assume every post-change
  failure is a regression you introduced, and do not assume every failure is unrelated
  pre-existing noise either - verify.
- When a test is inherently environment-dependent (requires a running database,
  message broker, container runtime, or external network service that may not be
  available), and it fails for an environment/connectivity reason rather than an
  assertion failure, report it explicitly as "environment-dependent, not verified in this
  environment" rather than silently treating it as passing or silently ignoring it.
- Never delete, skip, or weaken a test merely to make a run pass.

## Forbidden

- Never use tabs or non-two-space indentation.
- Never use a wildcard import.
- Never use field or setter injection.
- Never declare a service, repository, or controller as a record.
- Never use `@Data`/`@Builder`/`@AllArgsConstructor`/`@NoArgsConstructor` on business
  classes (Lombok contract).
- Never leave a method that overrides/implements a supertype method without `@Override`.
- Never report a Java change as complete without compiling the affected module at least
  once.
