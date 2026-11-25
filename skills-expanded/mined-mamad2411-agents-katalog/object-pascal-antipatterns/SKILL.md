---
name: object-pascal-antipatterns
description: Evidence-backed Object Pascal and Delphi smell review and refactoring guidance. Use when auditing or refactoring Object Pascal or Delphi for with-statement abuse, global state, memory and ownership errors, interface reference-counting pitfalls, exception swallowing, disabled compiler checks, untyped collections, thread misuse, UI reentrancy, string-built SQL, or framework leakage. Do not use for ordinary implementation, pattern selection, or test execution; use object-pascal-engineering, object-pascal-design-patterns, or object-pascal-testing-quality instead.
---

# Object Pascal Anti-Patterns

## Use When

Use for focused Object Pascal review or refactoring with code evidence and a
plausible maintenance, correctness, or security consequence. Route
implementation to
[`object-pascal-engineering`](../object-pascal-engineering/SKILL.md), positive
design choices to
[`object-pascal-design-patterns`](../object-pascal-design-patterns/SKILL.md), and
test lanes to
[`object-pascal-testing-quality`](../object-pascal-testing-quality/SKILL.md).

## Generated Material Boundary

Treat generated, vendored, IDE-owned, and dependency material (`.dfm`/`.lfm`/
`.fmx` form files, generated units, package output) as evidence, not refactoring
targets. Establish ownership before proposing changes; route dependency
provenance and executable package/component inputs to
[`dependency-supply-chain-review`](../dependency-supply-chain-review/SKILL.md).

## Language And Structure Smells

- **`with` abuse:** nested or long `with` blocks hide which object a member
  belongs to and break when a type gains a member. Qualify identifiers instead.
- **Global mutable state:** unit-level `var` in the `interface` section, or
  `class var` used as shared state, hides ownership and breaks isolation. Prefer
  injected dependencies or an `implementation`-section singleton with a clear
  accessor.
- **`goto`/labels and `Exit`/`Break`/`Continue` as control flow:** prefer
  structured branching; use `Exit` only for a clear early return.
- **`Variant` overuse:** `Variant` for ordinary typed data loses compile-time
  checking and hides conversions. Reserve it for COM/interop or genuinely dynamic
  boundaries.
- **`absolute` variables and inline `asm`:** obscure aliasing and portability;
  require a documented, justified reason.
- **`initialization`/`finalization` side effects:** network, filesystem, or
  process work at unit load time makes behavior order-dependent and untestable.
- **Circular `uses`:** a cycle between units signals a missing shared unit or a
  boundary that should be an interface.

## Memory And Ownership Smells

- **`.Free` without nil:** a freed field left non-nil invites double-free and
  use-after-free. Use `FreeAndNil` for owned fields.
- **Missing `try..finally`:** an exception between create and free leaks the
  resource. Wrap owned resources.
- **Freeing a non-owned object:** freeing an injected, shared, or
  collection-owned object causes double-free. Make ownership explicit.
- **`TObjectList<T>` ownership confusion:** `Create(False)` while assuming
  ownership (or the reverse) leaks or double-frees.
- **Manual `GetMem`/`FreeMem`/`Move`/`FillChar` on managed types:** bypasses
  reference counting and corrupts strings, dynamic arrays, and interfaces.
- **`PChar`/`PAnsiChar` casts of managed strings:** lifetime and encoding bugs;
  convert with `TEncoding` and keep the source alive.

## Interfaces And Components Smells

- **Mixing object and interface references:** holding a raw object reference to a
  `TInterfacedObject` past the last interface release is a use-after-free.
- **Circular interface references:** two objects holding interfaces to each other
  never reach zero and leak; break the cycle or use weak references.
- **`TComponent` and interfaces for the same lifetime:** double ownership causes
  double-free. Pick one owner.
- **`Supports`/`as` misuse:** unchecked casts raise at runtime; prefer `Supports`
  or an explicit interface query at the boundary.
- **Service locator:** a global registry or `Application`/`Screen` lookup used to
  fetch dependencies hides the real dependency graph.

## Exceptions And Errors Smells

- **Empty `except` blocks:** swallow failures silently. Handle, translate, or
  re-raise; comment any deliberate suppression.
- **`except on E: Exception do` catch-all:** hides programming errors and
  specific failure modes. Catch the narrowest type the boundary can handle.
- **`raise Exception.Create(...)` for control flow:** use typed exceptions and
  explicit result paths.
- **`Assert` for input validation:** assertions are disabled in release builds;
  validate untrusted input explicitly.
- **Error suppression via `{$WARNINGS OFF}`/`{$HINTS OFF}`:** blanket suppression
  hides real defects; address the warning or scope the directive narrowly with a
  reason.

## Concurrency And UI Smells

- **`Application.ProcessMessages`:** causes reentrancy and hidden state
  corruption; use `TThread.Queue`/`TTask` instead.
- **`TThread.Synchronize` from the main thread:** deadlocks. Use `Queue` or
  `ForceQueue`.
- **`TThread.Suspend`/`Resume`:** deprecated and deadlock-prone; use
  synchronization primitives.
- **`FreeOnTerminate` with `WaitFor`:** a race between termination and the wait.
- **Unbounded `TThreadedQueue<T>` or unbounded worker creation:** memory growth
  and CPU oversubscription.
- **`Sleep` on the UI thread:** freezes the application; move work off the main
  thread.
- **Shared mutable state without a lock:** data races; use `TMonitor`,
  `TCriticalSection`, or `TInterlocked`, or avoid sharing.

## Data, Strings, And I/O Smells

- **String-built SQL:** injection and quoting bugs. Use parameterized queries
  (`TFDQuery`/`TFDQuery.Params`, `TADOQuery.Parameters`).
- **`TDataSet` lifecycle errors:** iterating `Eof`/`Bof` without `Next`, or
  leaving datasets open, causes hangs and leaks. Own and close datasets
  explicitly.
- **Locale-dependent `Format`/`StrToFloat`/`FloatToStr`:** breaks under different
  regional settings. Pass a `TFormatSettings`.
- **`TDateTime` `Double` arithmetic:** timezone and precision bugs; use
  `System.DateUtils` and explicit timezone handling.
- **`TStrings` as a data structure:** index-based field access is brittle; use a
  typed record or class.
- **`ShortString`/`AnsiString`/`WideString` confusion:** encoding corruption at
  boundaries; convert explicitly.

## Build And Configuration Smells

- **Disabled range/overflow checks (`{$R-}`/`{$Q-}`):** hides arithmetic bugs;
  keep checks on unless a measured, documented reason exists.
- **`{$IFDEF}` spaghetti:** deeply nested conditional compilation is unreadable
  and untested; isolate platform differences behind a unit or interface.
- **Hand-edited generated project files:** changes are lost on regeneration;
  edit the maintained source.

## Refactoring Prompts

Ask what invariant, boundary, or observable behavior the code protects. Replace
`with` with qualified access, globals with injected dependencies, `.Free` with
`FreeAndNil`, string-built SQL with parameters, and `ProcessMessages` with
`TThread.Queue`. Keep changes small and migrate every caller.

## Reporting Rules

Report only evidence-backed findings: location, concrete path to failure or
maintenance cost, severity proportionate to impact, and a smallest safe
correction. Do not report style preference as a defect. Use
[`code-review`](../code-review/SKILL.md) and
[`review-verification-protocol`](../review-verification-protocol/SKILL.md) for
reported findings.
