---
name: sui-move-security
description: Secure Sui Move transitions, authority, signed actions, replay controls, bounded state, arithmetic, asset custody, DeFi shares, rewards, staking, farms, lending, AMMs, adapters, time, oracles, randomness, pauses, versions, and upgrades. Use for any privileged, stateful, economic, cryptographic, shared-object, or external-integration Move change or review.
---

# Sui Move Security

Make invalid transitions unrepresentable where possible and reject the rest before mutation.

Target repository instructions, accepted design records, pinned toolchain behavior, and published compatibility commitments take precedence over this standard's examples.

Before code, name the assets and safety, conservation, liveness, and exit invariants; authorities and worst-case compromise; untrusted callers, composition, and dependencies; and required failure behavior.

For each public or entry function, same-PTB composition, and reachable
multi-transaction sequence, prove all three properties:

- A valid pre-state produces a valid post-state.
- An abort commits no partial effects.
- Returned objects, capabilities, witnesses, receipts, and other values cannot
  be recombined to violate an invariant.

Security is not established until every callable path and composition preserves
the package's safety, conservation, authority, liveness, and exit invariants.

Before any irreversible or state-gating transition, prove that every required
exit, settlement, cleanup, retry, cancellation, authority rotation, and
recovery operation remains reachable. Reject a transition that can leave
shared state permanently paused, locked, full, orphaned, version-incompatible,
or dependent on an unavailable capability, object, or external system. Permit
that outcome only for a deliberate terminal state with every obligation already
discharged.

## Fail fast and mutate last

Abort on the cheapest decisive condition. Exhaust checks available from current information before allocation, cryptography, dependency work, mutation, asset movement, or event construction. Use this order:

1. package version, pause, or an active seam lock;
2. cheap lifecycle, input, identity, deadline, and authorization checks, including rejection of identical type arguments for roles that must differ;
3. bounds, available-balance, and other economic checks that need no proposed value;
4. required read-only external data, signature work, deserialization, or expensive math;
5. compute each fallible proposed final value once before mutation, naming it when checks or later mutation reuse it;
6. validate all fallible postconditions, including minimum output and maximum input, against the proposed values;
7. mutate state and move assets;
8. emit the final-state event;
9. return owned values.

The numbered order applies when dependency calls are read-only or can be last.
A result-bearing composable handoff is a deliberate exception. Use this order:

1. finish every local check;
2. acquire the narrowest lock or issue a linear receipt;
3. interact;
4. validate exact receipts and balance deltas;
5. commit core state and asset movements;
6. clear the lock;
7. emit.

Do not postpone a check that could have preceded an effect or interaction.

Guard order is observable API. Test overlapping invalid conditions. Abort rollback does not justify avoidable late checks: early failure saves gas, preserves diagnostic precedence, and shrinks the reasoning surface.

Reject a setter whose new value equals the current value before mutation, with its own stable error, so every emitted old/new pair records a real transition. A non-mutating authorization or discovery fact may still emit the value it newly commits.

## Express authority with types

- Use a typed capability or witness instead of an address check for privileged operations.
- Inventory every authority constructor, issuance, transfer, share, receive, rotation, revocation, and destruction path. Prove each use is bound to the exact object and domain, and that abilities match intended custody.
- Verify a revocable cap against live registry state before issuing a drop-only witness.
- Let the concern-owning module validate that witness locally.
- Keep a global cap minimal. Store target IDs only in a deliberately per-instance cap.
- Separate root authority from routine administration.
- Use delayed, explicit, test-covered root rotation.
- Add cancellation or recipient acceptance when the threat model requires it.
- Before burning, renouncing, or irreversibly handing off the last root or
  upgrade authority, prove successor usability and required exit and recovery
  liveness.
- Never infer broad authority from unrelated object possession or transaction sender alone.
- Do not pass overlapping capabilities to one setter or transition.
- Give capability holders a production lifecycle for safe destruction or revocation when stranded objects are possible.
- Reject zero addresses for recipients and authorities unless the zero address has an explicit protocol meaning.
- For a permissionless irreversible transition, never take economic parameters
  from caller choice. Derive them from accepted stored policy, derived state, a sealed
  adapter type, or a compiled value that is itself the accepted immutable
  policy. Otherwise fail closed.

## If the contract verifies off-chain signatures

- Bind authorization to the exact action, actor or beneficiary, target object or original type, expiry, and any domain not already fixed by a dedicated key.
- Reject malformed or non-canonical messages before verification. Prevent replay, and make third-party submission fail harmlessly or produce only the approved effect.
- If one key spans actions, deployments, or networks, use explicit domain separation and document the shared compromise scope.

## Prevent replay with linearity

- Prefer consuming a unique authorization resource over storing `claimed: bool` or a parallel nonce.
- Validate first, consume the resource, construct the result, emit the final-state event, then return the result.
- Use non-copyable, non-droppable payloads for migration, flash, or settlement handoffs.
- Require the exact sealed witness type to redeem a cross-package handoff.
- When admitting a witness by `TypeName`, reject primitive and vector types and prove its constructor is sealed in the approved module; `TypeName` alone cannot prove construction rights.
- Treat events as index facts, never replay guards.
- For a repeatable signed operation, consume a nonce, digest, or linear authorization exactly once and define bounded storage, eviction, and cleanup. Permit intentional replay only when it is documented and safe.

## Bound state and work

- Bound every persistent collection with a named protocol constant, and record the reachable maximum plus intentional slack.
- Bound every loop whose input can grow on chain.
- Check duplicates before consuming capacity.
- Define behavior at capacity. When bounded work is optional, prefer a safe liveness-preserving fallback over aborting the user's primary transition.
- Test empty, full, first-over-capacity, duplicate, removal, and re-addition cases.
- Avoid public inputs that cause unbounded deserialization, iteration, event size, or dynamic-field growth.
- Keep pending work and retry state bounded and explicitly releasable.

## Defend time, prices, and randomness

- Enforce every invariant on chain. Treat each public function as directly callable and PTB-composable; an SDK, UI, or expected transaction shape is never authority.
- Use the canonical immutable `Clock` for near-real-time security decisions. Define units and inclusive or exclusive deadline semantics, and reject stale or impossible future timestamps where relevant; epoch-start time is only a coarse source.
- When execution can change between signing and inclusion, bind the transition to user- or signer-approved maximum input, minimum output, and deadline. Never assume favorable transaction ordering.
- Before economic use, validate oracle source and feed identity, original type, pair, units or exponent, valid range, update time and freshness, confidence or deviation, liquidity assumptions, and whether a caller can select among historical updates. Define fail-closed or bounded fallback behavior.
- Never derive economic randomness from object IDs, sender, `Clock`, or
  transaction data.
- For `sui::random`:
  - keep the economic endpoint private `entry`;
  - create `RandomGenerator` inside the consuming module;
  - obey post-random PTB restrictions;
  - balance resource use across outcomes;
  - use commit-reveal with inputs fixed before reveal when atomic abort
    selection remains unsafe.

## Load DeFi guidance when applicable

For shares, vaults, liquid staking, farms, rewards, AMMs, lending,
liquidations, or other DeFi accounting, read
[DeFi security](references/defi-security.md) completely before designing,
changing, or reviewing the transition. Apply it with this skill's invariant,
fail-fast, custody, oracle, and external-seam rules.

## Preserve conservation and custody

Write and test one operation-specific identity per asset type, never a mixed-unit equation, derived from:

```text
assets in = assets out + reserves + accrued fees + pending custody + explicitly burned amount
```

- Keep reserves, fees, pending burns, allocations, residuals, and claims separate when their owner or terminal treatment differs.
- For every admitted asset, document its original type, mint and supply
  authority, deny, pause, or action restrictions, units, and authoritative
  balance delta.
- Reject an asset whose controls can break mandatory settlement or exit
  invariants unless an accepted admission decision records and bounds that risk
  explicitly.
- Use actual balances as authority, never event-only counters or SDK previews.
- Reconcile after every operation and multi-operation sequence.
- Make burn, disposal, refund, fee, residual, and rounding treatment explicit.
- Do not call disposal a burn unless native supply authority confirms destruction.
- Reject unexpected residuals or clamps that could conceal a broken invariant.

## Defend external seams

- Perform every locally available check before external reads, calls, or asset handoffs.
- Validate returned object identity, original type, package, pair, tier, units, amounts, actual balance deltas, liquidity, price deviation, freshness, and residual bounds.
- Keep external dependency and failure surfaces in adapters, not core.
- Do not cargo-cult an EVM reentrancy guard onto ordinary statically resolved Move calls. Threat-model PTB composition and flash, hot-potato, or explicit callback-like handoffs; lock only the smallest shared seam until exact receipt and repayment validation completes.
- Do not support an external venue whose required payment or custody model violates core invariants.
- Verify deployed bytecode and ABI; a local link stub proves type compatibility only.

## Define pause behavior

- Define pause scope exactly and preserve user exits and mandatory settlement
  unless the design explicitly rejects them.
- Let emergency authority reduce risk, not seize, reprice, or rewrite user
  accounting.

## Load upgrade guidance when applicable

Before changing or reviewing publication, upgrades, package-capability custody,
operational versioning, shared-state migration, or dependency relinking, read
[Upgrade security](references/upgrade-security.md) completely. Also read it
when old and new package versions can both reach shared protocol state changed
by the task.

## Protect sensitive material

- Keep secrets, private transaction material, and deployment credentials out
  of source, logs, fixtures, and summaries.
