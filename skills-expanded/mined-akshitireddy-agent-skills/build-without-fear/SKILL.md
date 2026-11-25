---
name: build-without-fear
description: Design a complete subsystem when requested or when recurring defects require explicit state, ownership, and recovery.
---

# Build Without Fear

Build the system required by the requested behavior. Base architectural depth
on observed failure modes and supported product states. Code size is neither
a target nor a constraint. Keep routine component changes focused.

## Start from the state space

Identify the dimensions relevant to this subsystem:

- lifecycle states, transitions, interruptions, retries, cancellation and teardown;
- success, loading, empty, stale, partial, error, fallback and recovery states;
- input methods, timing orders, re-entrancy, rapid repetition and concurrency;
- platform, renderer, device, accessibility and reduced-capability variants;
- persisted, cached, derived, live and presentation state;
- ownership boundaries and which subsystem is authoritative at each instant.

Represent relevant invariants through types, state machines, or contracts as
useful. Avoid boolean piles whose combinations are accidental.

## Prefer a subsystem over patches

When evidence shows several bugs share a boundary, repair its ownership or
transitions coherently. Replace it only when a focused correction is inadequate.
Choose the modules the subsystem needs from concerns such as:

1. domain types and invariants;
2. state machine or coordinator;
3. preparation and preload stages;
4. runtime execution;
5. interruption, retry and recovery;
6. adapters for frameworks or platforms;
7. diagnostics and inspectable status;
8. cleanup and resource ownership;
9. compatibility and migration paths.

Keep business rules separate from framework adapters. Expose the operation
states callers actually need to distinguish, such as queued, failed, cancelled,
or completed.

## Write explicit code

- Prefer exhaustive discriminated unions and total switches.
- Prefer named policies and tables over unexplained constants.
- Prefer separate preparation, commit and cleanup phases.
- Prefer idempotent operations and monotonic generations over timing guesses.
- Prefer bounded queues, caches and instance pools with documented eviction.
- Prefer a full scene/snapshot/model description over scattered DOM/CSS patches.
- Prefer comments that explain ordering, ownership and failure modes.
- Preserve extension points for plausible product variants already visible in the
  codebase; do not invent unrelated features merely to increase size.

Implementation size should follow the actual state space. Avoid filler, unused
abstractions, and speculative architecture. Every additional line should
cover a real state, make ownership explicit, improve craft, or make failure
recoverable.

## Handle temporal bugs as transactions

For animation, audio, rendering and UI transitions, treat each operation as a
transaction:

1. prepare every resource and destination state;
2. validate readiness and choose a declared fallback;
3. atomically enter the transition;
4. update only transition-owned presentation state;
5. atomically commit the destination;
6. release obsolete resources after the first committed presentation opportunity;
7. ignore late work using generation tokens or abort signals.

Never use an arbitrary delay as the primary correctness mechanism. If a resource
can be late, represent that fact and decide what the product shows while it is late.

Do not accept a handful of screenshots or one Playwright gesture as proof of a
temporal fix. Those probes can alias past a short fault and headless scheduling
can change the behavior. Use them to inspect named phases, but combine them with
code-level ordering/resource-readiness analysis and repeated normal, rapid and
interrupted interaction. A user's repeatable observation in the real app
outweighs an automated non-reproduction.

## Finish the implementation

Before stopping, reread the request and account for every item. Report any
possibility deliberately excluded and why. Run only the level of verification the
user permits; if verification is restricted, do not substitute stronger claims
than the evidence supports.
