---
name: substrate-reviewer
description: Systematic code review for FRAME pallets and Substrate runtimes following Polkadot SDK conventions. Checks for security issues, weight correctness, proper patterns, and common mistakes. Use when reviewing code or PRs.
---

# Substrate Reviewer

## 1. Purpose

Perform systematic code reviews of FRAME pallets and Substrate runtime code. Checks for security vulnerabilities, incorrect patterns, missing requirements, and deviations from Polkadot SDK conventions.

## 2. When to Use This Skill

- Reviewing a PR or code changes to a pallet
- Reviewing runtime configuration changes
- Pre-merge quality checks on Substrate code
- When the user asks to "review", "check", or "audit" code
- After writing code, as a self-review step

## 3. Platform Detection

Look for these indicators:
- FRAME pallet code (`#[pallet::*]` macros)
- Runtime configuration (`impl Config for Runtime`)
- Storage migrations
- Benchmark code
- XCM configuration

---

## 4. Review Process

When asked to review code, follow this systematic process:

### Step 1: Understand the Change
- Read the full diff or changed files
- Identify what the change is trying to accomplish
- Note which pallets and runtimes are affected

### Step 2: Run the Checklist (Section 5)
- Go through each category systematically
- Report findings with file:line references
- Classify by severity: CRITICAL, HIGH, MEDIUM, LOW, STYLE

### Step 3: Report Findings
Format findings as:

```
## Review Summary

### CRITICAL
- [file:line] Description of critical issue

### HIGH
- [file:line] Description of high issue

### MEDIUM
- [file:line] Description of medium issue

### LOW / STYLE
- [file:line] Description of style issue

### Positive
- Things done well worth noting
```

---

## 5. Review Checklist

### 5.1 Origin Checks (CRITICAL)

- [ ] Every dispatchable has an appropriate origin check
- [ ] `ensure_signed` is NOT used for privileged/admin operations
- [ ] Privileged operations use `ensure_root`, `EnsureOrigin`, or custom origin
- [ ] Origin type matches the operation's trust level:

```rust
// WRONG: Any user can call a privileged operation
pub fn force_set_value(origin: OriginFor<T>, value: u32) -> DispatchResult {
    let _who = ensure_signed(origin)?;  // <-- should be ensure_root
    SomeValue::<T>::put(value);
    Ok(())
}

// CORRECT: Only root/governance can call
pub fn force_set_value(origin: OriginFor<T>, value: u32) -> DispatchResult {
    ensure_root(origin)?;
    SomeValue::<T>::put(value);
    Ok(())
}
```

### 5.2 Arithmetic Safety (CRITICAL)

- [ ] No raw `+`, `-`, `*`, `/` on user-controlled values
- [ ] All arithmetic uses `checked_*`, `saturating_*`, or `defensive_saturating_*`
- [ ] Type conversions use `try_into()` or `saturating_into()`, not `as`
- [ ] No silent truncation in numeric conversions

```rust
// WRONG
let total = price * quantity;
let fee = amount / divisor;
let index = value as u32;

// CORRECT
let total = price.saturating_mul(quantity);
let fee = amount.checked_div(divisor).ok_or(Error::<T>::DivisionByZero)?;
let index: u32 = value.try_into().map_err(|_| Error::<T>::Overflow)?;
```

### 5.3 Panic Prevention (CRITICAL)

- [ ] No `unwrap()` in dispatchable code paths
- [ ] No `expect()` in dispatchable code paths
- [ ] No unchecked array/slice indexing (`arr[i]`)
- [ ] No `panic!()` or `unreachable!()` in runtime code
- [ ] If `unwrap()`/`expect()` is used with proof, comment ends with `; qed`
- [ ] Division operations check for zero divisor

```rust
// WRONG
let item = items[index];
let value = maybe_value.unwrap();

// CORRECT
let item = items.get(index).ok_or(Error::<T>::IndexOutOfBounds)?;
let value = maybe_value.ok_or(Error::<T>::NotFound)?;

// Acceptable with proof
let decoded = Decode::decode(&mut &data[..])
    .expect("data was encoded with same codec; qed");
```

### 5.4 Weight Correctness (CRITICAL)

- [ ] Every dispatchable has a `#[pallet::weight(...)]` annotation
- [ ] Weights use `T::WeightInfo::function_name(...)` from benchmarks
- [ ] Weight parameters match the worst-case inputs
- [ ] Variable-cost operations properly parameterize weight
- [ ] `DispatchResultWithPostInfo` used when actual weight < worst case

```rust
// WRONG: Fixed weight for variable-cost operation
#[pallet::weight(10_000)]
pub fn process_items(origin: OriginFor<T>, items: Vec<u32>) -> DispatchResult { ... }

// CORRECT: Parameterized weight
#[pallet::weight(T::WeightInfo::process_items(items.len() as u32))]
pub fn process_items(origin: OriginFor<T>, items: BoundedVec<u32, T::MaxItems>) -> DispatchResult { ... }
```

### 5.5 Storage Safety (HIGH)

- [ ] `BoundedVec` used instead of `Vec` in storage
- [ ] `BoundedBTreeMap`/`BoundedBTreeSet` instead of unbounded collections
- [ ] Appropriate hasher for storage maps:
  - `Blake2_128Concat` for user-controlled keys (default, safe)
  - `Twox64Concat` for trusted/system keys (fast, not safe for user input)
  - `Identity` only for already-hashed keys
- [ ] `StorageVersion` bumped when storage layout changes
- [ ] No unbounded iteration in dispatchables

### 5.6 Validate-Write-Event Pattern (HIGH)

- [ ] All validation happens before storage writes
- [ ] Events emitted after successful state changes
- [ ] Pattern: validate -> mutate state -> emit event -> return Ok

```rust
pub fn do_something(origin: OriginFor<T>, value: u32) -> DispatchResult {
    let who = ensure_signed(origin)?;

    // 1. VALIDATE
    ensure!(value > 0, Error::<T>::InvalidValue);
    let existing = Storage::<T>::get(&who).ok_or(Error::<T>::NotFound)?;
    ensure!(existing.can_update(), Error::<T>::NotAllowed);

    // 2. WRITE
    Storage::<T>::mutate(&who, |v| v.value = value);

    // 3. EVENT
    Self::deposit_event(Event::ValueUpdated { who, value });

    Ok(())
}
```

### 5.7 Error Handling (HIGH)

- [ ] Specific error variants for each failure case (not generic `BadInput`)
- [ ] Error doc comments describe the condition
- [ ] `ensure!()` used for expected validation failures
- [ ] `defensive!()` used for "should never happen" assertions
- [ ] Errors don't leak sensitive information

### 5.8 Event Quality (MEDIUM)

- [ ] Events emitted for all significant state changes
- [ ] Events contain enough info for indexers/UIs
- [ ] Named fields (not positional) in event variants
- [ ] Events use `#[pallet::generate_deposit(pub(super) fn deposit_event)]`

### 5.9 Call Index Stability (MEDIUM)

- [ ] `#[pallet::call_index(N)]` on every dispatchable
- [ ] Indices are sequential and never reused
- [ ] No gaps unless indices were deprecated
- [ ] New functions get the next available index

### 5.10 Defensive Programming (MEDIUM)

- [ ] `defensive!()` for invariant violations that shouldn't happen
- [ ] `defensive_assert!()` for debug assertions
- [ ] `.defensive_unwrap_or()` when a fallback is appropriate
- [ ] Log errors at appropriate levels (error, warn, info)

```rust
// For situations that "should never happen" but we handle gracefully
let value = maybe_value.defensive_unwrap_or(default_value);

// For invariant checking
if actual != expected {
    defensive!("Invariant violated: actual != expected");
}
```

### 5.11 Feature Flags (MEDIUM)

- [ ] `#![cfg_attr(not(feature = "std"), no_std)]` at crate root
- [ ] `extern crate alloc` for `Vec`, `Box`, etc.
- [ ] Benchmarking code gated with `#[cfg(feature = "runtime-benchmarks")]`
- [ ] Test code gated with `#[cfg(test)]`
- [ ] Try-runtime code gated with `#[cfg(feature = "try-runtime")]`
- [ ] All three features (`std`, `runtime-benchmarks`, `try-runtime`) propagated in `Cargo.toml`

### 5.12 Config Trait (MEDIUM)

- [ ] Uses trait objects, not concrete pallets (`type Fungible` not `type Currency = Balances`)
- [ ] Constants use `#[pallet::constant]`
- [ ] `WeightInfo` type included
- [ ] Modern traits used (fungible, not Currency)

### 5.13 Documentation (LOW)

- [ ] Pallet-level `//!` doc comment explaining purpose
- [ ] Doc comments on public types and functions
- [ ] Complexity annotations on dispatchables (`/// ## Complexity`)
- [ ] Error variant doc comments

---

## 6. Common Anti-Patterns

### Unbounded iteration
```rust
// WRONG: Iterates all storage entries
for (key, value) in MyMap::<T>::iter() {
    // ... unbounded work
}

// CORRECT: Use bounded iteration or pagination
let items = MyMap::<T>::iter().take(T::MaxItems::get() as usize);
```

### Missing deposit refund on removal
```rust
// WRONG: Data removed but deposit not returned
MyStorage::<T>::remove(&who);

// CORRECT: Return deposit when removing
let data = MyStorage::<T>::take(&who).ok_or(Error::<T>::NotFound)?;
T::Fungible::release(&HoldReason::MyOp.into(), &data.depositor, data.deposit, Precision::BestEffort)?;
```

### Trusting user-provided length
```rust
// WRONG: User controls Vec length, no bound
pub fn process(origin: OriginFor<T>, data: Vec<u8>) -> DispatchResult { ... }

// CORRECT: Bounded input
pub fn process(origin: OriginFor<T>, data: BoundedVec<u8, T::MaxDataLen>) -> DispatchResult { ... }
```

### Incorrect weight for conditional paths
```rust
// WRONG: Always charges max weight even when taking the cheap path
#[pallet::weight(T::WeightInfo::expensive_path())]
pub fn maybe_expensive(origin: OriginFor<T>, flag: bool) -> DispatchResult {
    if flag {
        // expensive path
    } else {
        // cheap path
    }
    Ok(())
}

// CORRECT: Return actual weight consumed
#[pallet::weight(T::WeightInfo::expensive_path())]
pub fn maybe_expensive(origin: OriginFor<T>, flag: bool) -> DispatchResultWithPostInfo {
    if flag {
        // expensive path
        Ok(().into())
    } else {
        // cheap path - refund unused weight
        Ok(Some(T::WeightInfo::cheap_path()).into())
    }
}
```

---

## 7. Runtime Configuration Review

When reviewing runtime changes:

- [ ] New pallet added to all three feature flags in `Cargo.toml`
- [ ] `construct_runtime!` index is unique and follows convention
- [ ] `parameter_types!` values are reasonable (not too large/small)
- [ ] `impl Config` types are correct for the runtime context
- [ ] `WeightInfo` points to actual benchmark weights
- [ ] `spec_version` incremented if logic changed
- [ ] Genesis config updated if needed

---

## 8. Migration Review

When reviewing migrations:

- [ ] Old storage layout defined with `#[storage_alias]`
- [ ] `StorageVersion` incremented
- [ ] Weight properly accounted for
- [ ] `pre_upgrade` / `post_upgrade` hooks present
- [ ] Error cases log rather than panic
- [ ] Migration registered in runtime

---

## 9. Formatting (Mandatory Final Step)

After all code changes are complete, you MUST run:

```bash
cargo +nightly fmt --all -- --check
# For Cargo.toml changes:
taplo format --check --config .config/taplo.toml <path/to/changed/Cargo.toml>
```
