---
name: object-pascal-design-patterns
description: Object Pascal and Delphi design-pattern guidance. Use when choosing or reviewing interfaces, factories, adapters, repositories, value objects, records, observers/events, decorators, strategies, commands, builders, state machines, dependency injection, resource ownership, or VCL/FMX/LCL presentation patterns in Object Pascal or Delphi. Do not use for ordinary Object Pascal implementation, test-lane execution, or smell-focused review; use object-pascal-engineering, object-pascal-testing-quality, or object-pascal-antipatterns instead.
---

# Object Pascal Design Patterns

## Use When

Use for deliberate Object Pascal pattern selection or review where types,
ownership, and boundaries affect maintainability. Use
[`object-pascal-engineering`](../object-pascal-engineering/SKILL.md) to implement
the chosen design,
[`object-pascal-testing-quality`](../object-pascal-testing-quality/SKILL.md) for
test execution, and
[`object-pascal-antipatterns`](../object-pascal-antipatterns/SKILL.md) for
smell-focused review.

## Selection Rules

Choose the smallest pattern that encodes an actual invariant, ownership boundary,
or substitution seam. Prefer concrete collaborators until multiple
implementations or an external boundary justify an interface. Do not introduce a
pattern only to mirror framework vocabulary. Match the repository's existing
Delphi/FPC dialect and framework; do not assume a Delphi-only feature exists in
FPC mode.

## Patterns To Prefer

- **Value object:** an immutable `record` (or a class with a private constructor
  and read-only properties) for validated, comparable concepts. Use `record`
  operators (`Implicit`, `Explicit`, `Equal`) for conversions and equality.
- **Enum + `case`:** finite states as a scoped enum with an exhaustive `case`,
  rather than string or integer state codes.
- **Factory:** a class function or a dedicated factory class when creation has
  validation, normalization, or multiple meaningful entry paths. Use virtual
  constructors or a class-reference (`class of T`) for polymorphic creation.
- **Builder:** a fluent builder for objects with many optional parts; keep the
  built object valid by default.
- **Interface + constructor injection:** small behavior-oriented interfaces owned
  by their consumer, injected through constructors at external boundaries.
- **Adapter:** wrap a host, framework, filesystem, HTTP, or vendor API behind an
  interface the domain owns.
- **Repository:** an interface with collection-like persistence behavior, with a
  data-access adapter behind it. Keep SQL and provider types out of the domain.
- **Strategy:** an interface, a method pointer (`TMethod`), or an anonymous
  method (`TProc`/`TFunc<T>`) for interchangeable algorithms.
- **Observer:** `TNotifyEvent`-style events or a multicast event list for
  one-to-many notification; unsubscribe explicitly to avoid dangling references.
- **Decorator:** interface delegation that adds behavior without changing the
  wrapped contract.
- **Command:** an interface with `Execute` (or a `TProc`) for queued, undoable, or
  deferred operations.
- **Template method:** a non-virtual public method calling `virtual`/`abstract`
  steps; prefer composition when the variation is not a true algorithm skeleton.
- **State:** state objects behind an interface when transitions carry behavior;
  an enum + `case` when they do not.
- **Null object:** a no-op implementation of an interface instead of `nil` checks
  scattered through callers.
- **RAII:** `try..finally` for owned resources, or an interface whose
  implementation releases the resource in its destructor.
- **Unit of work / transaction scope:** one owner opens, commits or rolls back,
  and cleans up a transaction.
- **Producer/consumer:** `TThreadedQueue<T>` with a bounded size for cross-thread
  handoff; **future:** `IFuture<T>` for deferred results.

## Delphi-Specific Mechanics

- **Interface lifetime:** a `TInterfacedObject` descendant frees itself when its
  last interface reference is released. Do not also free it manually, and do not
  hold a raw object reference past the last interface release. Use
  `TComponent`/`TObjectList` ownership for component trees, not interfaces.
- **Aggregation and delegation:** `TAggregatedObject`/`TContainedObject` support
  interface delegation; use them deliberately and document the inner/outer
  lifetime.
- **Component composition:** `TComponent` ownership, `TFrame` composition, and
  `TCollection`/`TCollectionItem` model parent/child trees. Prefer these over
  hand-rolled parent pointers in UI code.
- **Collections:** `TList<T>`, `TObjectList<T>`, `TDictionary<TKey,TValue>`,
  `TQueue<T>`, `TStack<T>`, `TThreadedQueue<T>`, `TThreadList<T>`. Choose
  ownership (`OwnsObjects`) explicitly.
- **Events:** `TNotifyEvent` and typed event method pointers for observer seams;
  keep handlers small and unsubscribe on teardown.
- **Singletons:** a unit-level variable in the `implementation` section, or a
  `class var` with a class function accessor, is the idiomatic Delphi singleton.
  Prefer constructor injection over a global singleton for testability.
- **DI containers:** if the repository uses Spring4D or another container, follow
  its registration and lifetime conventions; do not add a container for a small
  project that constructor injection already serves.

## Presentation Patterns

- **MVC/MVP/MVVM:** keep VCL/FMX/LCL forms and frames as thin views; put
  presentation logic in a presenter/view-model that does not reference the form
  type. Bind through events or a binding library the repository already uses.
- **Data modules:** keep data-access components in `TDataModule` units and expose
  typed operations, not raw datasets, to the rest of the application.
- **Form inheritance:** use it for shared layout, not for shared behavior; prefer
  frames or composition for reusable behavior.

## Testing Seams

Test pure policy directly. Substitute external adapters at interfaces, not
arbitrary internals. Verify transactions, retries, and resource cleanup at
integration boundaries where their observable contracts exist. Prefer constructor
injection so a test can supply a fake without a global registry.

## Review Checklist

- Does the pattern encode a named invariant or external boundary?
- Are interfaces small and owned by their consumer?
- Is construction valid by default and state transition explicit?
- Is I/O outside value objects and pure policy?
- Is resource, interface, and transaction ownership singular and testable?
- Does the design work in the repository's actual dialect (Delphi vs FPC) and
  framework?

## Common Mistakes

Avoid service bags, generic repository wrappers, inheritance trees used only for
reuse, DTOs that leak framework or dataset types, events with hidden side effects,
singletons used as service locators, and abstraction before multiple real callers
require it.
