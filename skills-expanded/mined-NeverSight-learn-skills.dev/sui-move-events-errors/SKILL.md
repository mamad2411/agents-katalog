---
name: sui-move-events-errors
description: Design replay-complete Sui Move events, minimal payloads, native-metadata boundaries, event identity and ordering, emitters, stable numeric errors, abort ownership, and diagnostic compatibility. Use when adding, compacting, changing, testing, indexing, or reviewing any Move event, payload field, error, guard, or transition's emitted facts.
---

# Sui Move Events and Errors

Treat events and aborts as published protocol interfaces, not incidental diagnostics.

Target repository instructions, accepted design records, pinned toolchain behavior, and published compatibility commitments take precedence over this standard's examples.

## Make events replay complete

From package publication onward, every economically relevant mutable fact promised to index must be reconstructible from the following durable sources, alone or in combination:

- native transaction effects and metadata;
- immutable published bytecode;
- historical contents of object versions referenced by creation effects, but only when durable archival access is guaranteed;
- the protocol event stream.

If these sources do not durably provide a required fact, emit the smallest primitive needed to reconstruct it. Before adding an event field, check the available transaction metadata, effects, and object content; do not duplicate a fact merely because it is absent from the inner Move struct.

- Emit each mutable setter, claim, accrual, distribution, trade, lifecycle transition, allocation, and migration settlement.
- Name payloads as completed facts in past tense.
- Emit only after final state and asset movement are known.
- Carry stable entity identity plus the primitive delta, old/new pair, or final snapshot required for replay.
- Include post-transition totals when the replay contract needs to detect gaps or resynchronize a promised aggregate.
- Record the exact economic inputs used when later global configuration can change historical interpretation.
- Reject no-op setter updates so every emitted old/new pair represents a real state transition.
- Do not emit derived display values that consumers can reproduce exactly.
- Do not add an application sequence, revision, nonce, schema tag, or action tag
  merely to order, paginate, classify, or detect gaps.
- Add a domain counter only when it is itself protocol state or when native
  order and payload type cannot sequence the transitions. Record that decision.
- Emit one authoritative event for one accounting mutation.

## Audit necessity event by event and field by field

- Name the new protocol fact each event commits. The payload type's occurrence
  is itself a fact.
- Remove the event only when both that occurrence and every field already come
  from native effects, transaction metadata, immutable bytecode, or the prior
  replay stream.
- Default package initialization to eventless when it only shares or delivers objects recorded by publication effects and initializes compiled constants. Keep a creation event when an ordinary function commits caller-supplied or deployer-selected values that can vary.
- Before publication, do not restate `ctx.sender()` as `buyer`, `seller`,
  `claimant`, `caller`, or another actor field. Consumers receive the sender in
  native event metadata.
- Keep an actor, attested identity, beneficiary, recipient, or refund address
  only when it can differ from the sender. Name it for that role and record why
  it differs.
- On a non-mutating fact, emit only what it newly commits, not current values of state it leaves unchanged and the prior stream already reconstructs.
- Keep a destroyed object's ID when it distinguishes a multi-instance entity or closes a keyed replay fact; omit it only when payload type and native metadata identify the entity uniquely.
- Bounded immutable inputs may live only in the created object's canonical content when the declared data-availability model makes that content durable.
- Preserve deliberate redundancy that lets consumers verify a fact or
  resynchronize a promised aggregate: delta plus final total, an old/new
  mutation pair, a complete required snapshot, or the identity and final value
  removed or delivered.
- A later compaction audit must not remove that deliberate redundancy.

## Design identity deliberately

- Carry identity for every multi-instance entity.
- Do not use the executing package version ID as an event-domain key. Compatible upgrades preserve existing Move type identity; partition a continuing event stream by its stable payload type and entity identity.
- A typed singleton mutation can omit its unchanging owner ID only when production creates exactly one instance, replay begins at publication, and the payload type partitions the stream.
- Keep old/new identity for root replacement or any transition that changes recognized singleton identity.
- Restore explicit identity when a later design permits replacement or multiple instances.
- Partition reducers by stable payload identity and process native Sui event order.

## Describe accounting precisely

- Distinguish pending custody, native burn, transfer to an irrecoverable address, refund, and returned residual.
- Include asset deltas and post-accrual totals when reconciliation requires both.
- Include the applied fee or policy input if configuration can change later.
- Document deliberately non-indexable facts, such as current ownership of a freely transferable capability, and direct consumers to native object or transaction data.
- Before publication, keep reducers and field tests synchronized with every
  payload field change.
- After publication, compatible upgrades cannot add, remove, rename, reorder,
  or retype fields of an existing payload struct, or change its abilities. Add
  a new payload type instead.
- Treat that replacement, and any change in an existing field's meaning or
  event-emission semantics, as an indexing ABI migration.

## Centralize event construction

The envelope provides one stable outer event namespace for the package lineage.
Indexers can subscribe to the envelope's defining module and inspect its type
argument to discover payload types added by later package versions. A separate
package has a different envelope identity and must be indexed separately.

When the package standard uses an envelope:

```move
public struct Event<T: copy + drop>(T) has copy, drop;

public(package) fun emit_event<T: copy + drop>(payload: T) {
    sui::event::emit(Event(payload));
}
```

- Keep payload types and package-only named emitters in `events.move`.
- Let only `events_wrapper` call `sui::event::emit` directly.
- Let transition modules mutate first and call the descriptive emitter afterward.
- Do not pack the same payload ad hoc at several call sites.
- Keep test-only collection, unwrap, and `<event>_fields` helpers out of production bytecode.
- If a package intentionally uses direct native events, keep the schema/emitter/replay discipline. Do not add a wrapper only for uniform appearance.

## Keep errors descriptive and stable

In a simple package, define an error in the same module that raises it. Use an
explicit clever-error code and a descriptive byte-string message:

```move
#[error(code = 1)]
const EInvalidRecipient: vector<u8> = b"Recipient must not be the zero address.";

public fun set_recipient(recipient: address) {
    assert!(recipient != @0x0, EInvalidRecipient);
    // ...
}
```

- Require `#[error(code = N)]` on every error constant declared and raised in
  the same module.
- Give it an `EUpperCamelCase` name and a descriptive `vector<u8>` value that
  states the failed condition.
- Do not use bare module-local `u64` error constants.
- Preserve every existing numeric code and meaning when converting an error to
  this form. The explicit code is an unsigned 8-bit value; treat an out-of-range
  published legacy code as a compatibility conflict requiring an explicit
  decision, never as permission to renumber it silently.
- Keep the constant beside the invariant-owning code under `// === Errors ===`.

Use literal-returning package macros only when multiple modules deliberately
share one package-wide numeric namespace:

```move
// errors.move
// === Errors ===
macro public(package) fun invalid_recipient(): u64 { 1 }

// invariant-owning module
assert!(recipient != @0x0, protocol::errors::invalid_recipient!());
```

- Keep the registry append-only after publication.
- Never reuse a retired code or change a published meaning.
- Maintain one map from number to macro, raising module, and stable meaning.
- Define matching `#[test_only]` `EUpperCamelCase` constants when attributes or structural tooling need named codes.
- Do not introduce an `errors.move` registry for a simple package whose errors
  are declared and raised by their invariant-owning modules.
- Keep `errors.move` diagnostic-only: no state, authority, assertions, abort wrappers, or generic validators.

## Raise errors where invariants live

- Place fully qualified `assert!(condition, protocol::errors::name!())` in the module that owns the invariant.
- Use a typed `assert_*` helper only when it inspects private domain representation or deliberately composes owned guards.
- Reject helpers that accept only a precomputed boolean and hide the error and guard position.
- Preserve the raising module as part of error semantics.
- Test exact abort code and exact `location`.
- Test precedence when several guards can fail.
- Add only a narrow lint suppression when the pinned compiler requires one for error macro expansion, with adjacent rationale.

## Compatibility gate

- Treat payload types, fields, wrappers, error numbers, error meanings, raising
  modules, and guard precedence as published API.
- Before publication, make any compaction a deliberate one-time decision.
- After publication, append new errors or add new payload types. Do not silently
  reinterpret existing interfaces.
- Adding emission only to upgraded code does not make a stream replay-complete
  while callers can still use an old package version. Gate old mutators through
  an accepted operational version transition before promising complete replay.
