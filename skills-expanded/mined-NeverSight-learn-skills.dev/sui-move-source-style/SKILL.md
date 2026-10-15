---
name: sui-move-source-style
description: Apply consistent Sui Move source organization, naming, visibility, abilities, signatures, `self` receiver naming, receiver and index syntax, direct UID access, pinned standard-library and framework reuse, macros, local-variable discipline, API vocabulary, documentation, and test-only conventions. Use when writing, simplifying, refactoring, or reviewing any `.move` source or test file.
---

# Sui Move Source Style

Make each file clearly communicate what it owns, who may change it, and how its state is created, updated, and retired, without requiring the reader to trace unrelated modules or call sites.

Target repository instructions, accepted design records, pinned toolchain behavior, and published compatibility commitments take precedence over this standard's examples.

## Order module sections

Use this order and omit empty sections:

1. module documentation and declaration;
2. grouped `use` declarations;
3. `// === Constants ===` or `// === Package Constants ===`;
4. `// === Errors ===` when the module defines error constants or macros;
5. `// === Public Types ===` or `// === Public Structs ===`;
6. `// === Private Initialization ===` when applicable;
7. `// === Public Functions ===`, subdivided by product operation in large modules;
8. `// === Public Aliases ===` when aliases materially improve the API;
9. `// === Package Functions ===`;
10. `// === Private Functions ===`;
11. `// === Test-Only Types ===` when needed, then `// === Test-Only Functions ===`.

Use title case. Group large public surfaces by domain operation, not only visibility.
Put module-local `#[error(code = N)]` `EUpperCamelCase: vector<u8>` constants
and a dedicated `errors.move` module's literal-returning error macros under
`// === Errors ===`. Do not use bare module-local `u64` error constants. Omit
the section when a module only raises fully qualified errors defined elsewhere.
Format function bodies as logical paragraphs, with one blank line between validation, derivation, mutation or transfer, emission, and return. Do not blank-line every statement or pad tiny helpers.

## Organize imports

- Consolidate imports from the same root address into one nested declaration per module. Do not repeat a root on separate lines; follow the repository's root ordering consistently.
- Do not import a member solely to shorten one call. Keep package error macros and one-off framework functions fully qualified; import members used repeatedly. Test modules may import ubiquitous `std::unit_test::{assert_eq, destroy}` helpers.
- Do not explicitly import Move 2024 implicit prelude modules such as `std::vector`, `std::option`, `sui::object`, `sui::transfer`, or `sui::tx_context`.
- Use aliases for clear receiver methods or real collisions, not to hide domain distinctions.

## Reuse pinned libraries before writing helpers

Before adding, replacing, or reviewing arithmetic, conversion, collection,
iteration, object, transfer, macro, or framework-wrapper logic, read
[Pinned library reuse](references/pinned-library-reuse.md) completely. Prefer
the pinned implementation when its semantics match; do not add a wrapper solely
to rename it.

## Name by domain meaning

- Use lower snake case for packages, modules, files, functions, variables, and package macros.
- Use UpperCamelCase for structs and enums.
- Use uppercase snake case for ordinary constants.
- Use `EUpperCamelCase` for named error constants.
- In a simple package, give every error declared and raised by one module an
  explicit `#[error(code = N)]` and descriptive `vector<u8>` message. Preserve
  existing codes. Reserve package-wide error macros for a numeric namespace
  deliberately shared by multiple modules.
- End durable authority objects in `Cap`.
- End ephemeral authorization proofs in `Witness`.
- Name linear handoffs and hot potatoes for their domain fact: `Request`, `Receipt`, `Payload`, `Price`, or `FlashLoan`.
- Name phantom type parameters for their role: `Asset`, `Quote`, `CoinType`, or `Venue`, not `T` when the role matters.
- Name fixtures for what they provide: `ClaimFixture`, `UpgradeFixture`.
- Name tests as behavioral facts: `constructor_rejects_zero_allocation`.
- Name event payloads as completed past-tense facts: `AdminGranted`, `FeesClaimed`.
- Include rounding direction in math names: `apply_down`, `mul_div_up`, `to_assets_down`.

## Keep visibility narrow

- Use `public fun` only for real transaction or composition surfaces.
- Use a non-public `entry` function only when an operation must be directly callable by transactions but intentionally unavailable to other Move packages. Keep it thin, place endpoint-specific delivery there, and use a `public` function when cross-package Move composition is intended.
- Use `public(package) fun` for cross-module package internals.
- Use plain `fun` for same-module implementation details.
- Keep public ABI minimal; an upgrade cannot erase old callable bytecode.
- Treat every existing public function signature as fixed across compatible
  upgrades, except for permitted relaxation of generic ability constraints.
- Treat every published struct or enum layout and ability set as fixed.
- Add a new function or type instead of changing a published one. When stored
  shape changes, provide an explicit authorized migration.
- Treat `init` as initial-publication-only because upgrades do not rerun it. Put post-upgrade setup in a named authorized migration or activation function.
- Keep struct fields private.
- Do not expose production getters, constructors, cleanup, or mutation solely for tests or frontend convenience.

## Assign abilities deliberately

- Give each type only the abilities its lifecycle requires.
- Use `key` only for values intended to become top-level owned or shared objects.
- Add `store` to a capability only when public transfer outside its defining module or nesting is intended.
- Avoid `copy` and `drop` on resources that must be consumed exactly once.
- Use `phantom` when the type parameter separates domains without a stored value.
- Move 2024 currently requires every struct type to be public. Do not confuse public type visibility with public authority: fields remain accessible only to the defining module, and constructors and operations should remain private or `public(package)` when external use is not intended.

## Order parameters

Use this order for public functions:

1. primary receiver or state object;
2. authorizing capability or witness;
3. other domain objects and values;
4. `Clock` or other framework reads;
5. `TxContext` last.

Use `&` for reads, `&mut` for actual mutation, and by value for resources the function consumes. Return newly created owned objects, coins, capabilities, and refunds. Transfer inside core only when delivery is the explicit endpoint contract.

Keep construction and publication separate when possible: `new` returns the owned value and `share` consumes it into shared state.

When a returned object has `key` but not `store`, provide its consuming sink in the defining module, such as `share(self)` for shared state or `keep(self, ctx)` for sender delivery. Do not strand a value that callers cannot transfer or share themselves.

## Decompose multi-phase transitions aggressively

- **Monolithic multi-phase transition:** One function mixes several independent
  protocol phases and forces reviewers to track multiple invariants and nested
  branches simultaneously.
- Keep the owner function as an ordered transition summary. Extract cohesive
  phases into domain-named private helpers.
- Treat two independently nameable phases, or one phase-specific nested branch,
  as a decomposition signal. Do not wait for a line-count threshold when
  extraction makes invariant boundaries visible.
- Let each helper own one phase, such as eligibility derivation, settlement
  preparation, accounting reconciliation, custody movement, or final cleanup.
  Give it the narrowest inputs and result that phase requires.
- Preserve validation, borrow, evaluation, abort, mutation, asset-movement, and
  emission order exactly when extracting. The owner function must still expose
  the complete protocol sequence at a glance.
- Keep extracted helpers private unless a real package or public caller needs
  them. Do not widen visibility for tests.
- Do not extract generic `handle_*`, `process_*`, pass-through, or arbitrary
  line-count helpers. Keep a phase inline when extraction would hide ordering,
  split one invariant across functions, or add indirection without reducing the
  reasoning surface.

## Use receiver syntax naturally

- Use dot syntax when the first parameter is the natural receiver: `market.supply(...)`, `cap.assert_market(...)`, `coin.into_balance()`.
- In the module that defines a type, name the natural-receiver first parameter
  `self` whenever adding or materially editing the function.
- Keep a role name for peer values of the same type or when `self` would obscure
  which value plays which role.
- Outside the defining module, name the parameter for its domain role.
- Constructors and genuinely static helpers have no `self`. The parameter name
  documents intent; dot syntax is determined by the first argument's type.
- Keep constructors and operations without a natural receiver module-qualified: `market::new(...)`, `curve::quote_buy(...)`.
- Add a module-local `use fun dependency::function as Type.method` when a pinned
  dependency exposes a natural receiver without receiver form.
- For a dependency type, keep the alias module-local. `public use fun` is legal
  only in the type's defining module; use it there only when it materially
  clarifies the external API.
- In tests, alias helpers with `use fun helper as Fixture.method`.

## Prefer canonical index syntax

- For new packages, set the stable `edition = "2024"` in `Move.toml`. In an existing package, follow its pinned edition and migrate deliberately; do not introduce an obsolete preview edition such as `2024.beta`.
- In Move 2024, prefer `&collection[index]`, `&mut collection[index]`,
  `collection[index]`, and indexed assignment over explicit `borrow` and
  `borrow_mut` calls when the collection exposes canonical index syntax.
- Bare `collection[index]` dereferences and copies the element, so it requires
  the element type to have `copy`.
- Pass each index argument exactly as the annotated accessor declares it: use `collection[key]` for a key taken by value and `collection[&key]` for a key taken by reference.
- Add `#[syntax(index)]` to a custom type only when indexing is its canonical,
  unsurprising public lookup API.
- Annotated accessors must be public and defined in the type's module. Do not
  widen a package-only API merely to obtain bracket syntax, and do not hide
  insertion, settlement, authorization, or other surprising work behind it.
- When defining both immutable and mutable index accessors, keep their type parameters, constraints, subject type, index parameters, and return type identical except for reference mutability.

## Read object identity directly

- Inside a type's defining module, prefer its directly accessible UID field: `self.id.to_inner()`, `value.id.to_inner()`, or `id.to_inner()` after unpacking. Take the ID before sharing, transferring, or unpacking when it is needed afterward.
- Keep `object::id(value)` for generic `key` parameters, framework or external objects, and types defined in another module whose UID field is inaccessible.
- Do not add an ID getter merely to replace `object::id`; add one only when identity is a real part of the defining module's consumer-facing interface.

## Use locals deliberately

- **Redundant single-use temporary:** A local that merely names a pure
  expression for one later use, whether as an argument, condition, arithmetic
  operand, or return value.
- Inline that local only when its name adds no domain meaning and moving the
  expression preserves borrow lifetime, evaluation order, abort order, and
  mutation order.
- Use count alone never proves redundancy.
- Keep a local when it is reused, names a unit or protocol role, freezes pre-mutation state for a later event, separates validation from mutation, narrows a borrow, or makes nontrivial arithmetic auditable.
- Never inline across a mutation or external call when the later read could observe different state. Do not recompute a proposed value after mutation merely to reduce locals.
- Construct a unit witness, one-off wrapper, direct getter, or immediate return at the call site when no intermediate invariant needs a name.
- Let assertion helpers validate. Do not make them return an unchanged read solely to save the owning transition from reading and naming its own pre-state.
- Do not add a pass-through parameter solely to relay or return a value unchanged; another module should receive it only when that module validates, transforms, consumes, or stores it.
- A witness, marker, or capability used for type-level authority is not unused.
  Keep it as `_` or a meaningful `_role` name.
- Remove an unread parameter from private code and from a signature already
  changing for another reason.
- Otherwise, do not churn a published or intentionally uniform forwarding
  signature merely to drop it. Keep the parameter anonymous and document the
  compatibility reason only when it is not obvious.

## Infer generic arguments when clear

- Omit generic arguments that the compiler can infer.
- When only some arguments must remain explicit, use `_` for those fixed
  unambiguously by a value argument, receiver, or expected result:
  `dynamic_object_field::exists_with_type<_, Capability>(&self.id, CapabilityKey<Capability>())`.
- Keep a type argument explicit when inference fails or its spelling
  communicates domain meaning that the expression does not.
- Verify partial inference with the repository's pinned compiler. `_` is an
  expression-level type placeholder, not a type permitted in function
  signatures, constant types, or datatype fields.

## Use precise API vocabulary

- Use `new` for the module's primary constructor.
- Use descriptive constructors when variants matter: `new_cancelable`, `new_irrevocable`, `new_kinked`.
- Name reads exactly for the domain value returned.
- Use `is_*` and `has_*` for predicates.
- Reserve `into_*` for a real type conversion and name its destination.
- Use `destroy` when a consuming wrapper deletes itself and releases contents.
- Store `Balance` inside objects and accept or return `Coin` at public asset boundaries unless a different custody model is deliberate.
- Use the exact domain verb for a mutation: `grant_admin`, `claim_fees`, `begin_migration`.
- Reject vague production names such as `fields`, `parts`, `data`, `info`, `handle`, and `process` unless one is the precise domain term.
- Permit `<event>_fields` only as a narrow test-only payload snapshot convention.

## Document the contract

- Document public types, functions, invariants, hard bounds, rounding, and irreversible effects.
- Explain the authority and consumption semantics of capabilities, witnesses, and hot potatoes.
- Put all test constructors, malformed-value seams, field snapshots, and mutation hooks at the end with `#[test_only]`.
- Use a narrow lint suppression only after reproducing the warning under the pinned compiler. Put the rationale adjacent to it.
