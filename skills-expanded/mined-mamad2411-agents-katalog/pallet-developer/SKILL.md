---
name: pallet-developer
description: Scaffolds, creates, and modifies FRAME pallets with proper structure, Config traits, storage items, dispatchables, events, errors, and tests. Use when building new pallets or modifying existing ones in the Polkadot SDK.
---

# Pallet Developer

## 1. Purpose

Help developers create well-structured FRAME pallets following Polkadot SDK conventions. Covers scaffolding new pallets, adding storage/dispatchables/events, setting up test infrastructure, and configuring Cargo.toml features.

## 2. When to Use This Skill

- Creating a new FRAME pallet from scratch
- Adding new storage items, dispatchables, events, or errors to an existing pallet
- Setting up the test mock runtime for a pallet
- Configuring `Cargo.toml` features for `std`/`runtime-benchmarks`/`try-runtime`
- Adding bounded types, HoldReason patterns, or fungible trait integration
- Refactoring pallets to use the `frame` umbrella crate

## 3. Platform Detection

Look for these indicators:
- `#[frame::pallet]` or `#[pallet::config]` macros
- `Cargo.toml` with `frame` dependency
- Files under `substrate/frame/` or `pallets/` directories
- `no_std` attribute with `extern crate alloc`

---

## 4. Pallet File Structure

```
substrate/frame/<pallet-name>/
    Cargo.toml              # Dependencies and features
    src/
        lib.rs             # Main pallet definition (macros)
        benchmarking.rs    # Benchmark definitions
        weights.rs         # Auto-generated weights
        tests.rs           # Unit tests with mock runtime
        migrations.rs      # Storage migrations (if needed)
        types.rs           # Custom type definitions (optional)
```

---

## 5. lib.rs Skeleton

```rust
//! # My Pallet
//! Description of what this pallet does.

#![cfg_attr(not(feature = "std"), no_std)]

mod benchmarking;
pub mod migrations;
mod tests;
pub mod weights;

extern crate alloc;
use alloc::{boxed::Box, vec, vec::Vec};
use frame::{
    prelude::*,
    traits::{
        fungible::{Inspect, InspectHold, Mutate, MutateHold},
        tokens::Precision,
    },
};
pub use weights::WeightInfo;

/// Re-export all pallet items.
pub use pallet::*;

/// The log target of this pallet.
pub const LOG_TARGET: &'static str = "runtime::my_pallet";

// Type aliases for readability
pub type BalanceOf<T> =
    <<T as Config>::Fungible as Inspect<<T as frame_system::Config>::AccountId>>::Balance;

#[frame::pallet]
pub mod pallet {
    use super::*;

    // ... pallet contents (see sections below) ...
}
```

---

## 6. Config Trait

```rust
#[pallet::config]
pub trait Config: frame_system::Config {
    /// The overarching event type.
    #[allow(deprecated)]
    type RuntimeEvent: From<Event<Self>> + IsType<<Self as frame_system::Config>::RuntimeEvent>;

    /// The overarching call type.
    type RuntimeCall: Parameter
        + Dispatchable<RuntimeOrigin = Self::RuntimeOrigin, PostInfo = PostDispatchInfo>
        + GetDispatchInfo
        + From<frame_system::Call<Self>>;

    /// The currency type, used for deposits.
    type Fungible: Inspect<Self::AccountId>
        + Mutate<Self::AccountId>
        + InspectHold<Self::AccountId, Reason: From<HoldReason>>
        + MutateHold<Self::AccountId, Reason: From<HoldReason>>;

    /// A configurable constant.
    #[pallet::constant]
    type DepositBase: Get<BalanceOf<Self>>;

    /// Maximum number of items.
    #[pallet::constant]
    type MaxItems: Get<u32>;

    /// Weight information for extrinsics in this pallet.
    type WeightInfo: weights::WeightInfo;

    /// Query the current block number.
    type BlockNumberProvider: BlockNumberProvider;
}
```

### Key Patterns

- Always extend `frame_system::Config`
- Use trait objects for loose coupling (e.g., `Fungible` trait, not `pallet_balances`)
- Mark configurable constants with `#[pallet::constant]`
- Include `WeightInfo` for benchmark-generated weights

---

## 7. HoldReason Composite Enum

For pallets that hold funds:

```rust
/// A reason for holding funds.
#[pallet::composite_enum]
pub enum HoldReason {
    /// Funds held for a specific operation.
    MyOperation,
}
```

Used with:
```rust
T::Fungible::hold(&HoldReason::MyOperation.into(), &who, amount)?;
T::Fungible::release(&HoldReason::MyOperation.into(), &who, amount, Precision::BestEffort)?;
```

---

## 8. Pallet Struct and StorageVersion

```rust
/// The in-code storage version.
const STORAGE_VERSION: StorageVersion = StorageVersion::new(1);

#[pallet::pallet]
#[pallet::storage_version(STORAGE_VERSION)]
pub struct Pallet<T>(_);
```

---

## 9. Storage Items

### StorageValue

```rust
#[pallet::storage]
pub type SomeValue<T: Config> = StorageValue<_, u32, ValueQuery>;
```

### StorageMap

```rust
#[pallet::storage]
pub type Accounts<T: Config> = StorageMap<
    _,
    Blake2_128Concat,      // Hasher (safe for untrusted keys)
    T::AccountId,          // Key
    AccountData<BalanceOf<T>>,  // Value
>;
```

### StorageDoubleMap

```rust
#[pallet::storage]
pub type Multisigs<T: Config> = StorageDoubleMap<
    _,
    Twox64Concat,         // Hasher for key1 (fast, trusted keys)
    T::AccountId,         // Key1
    Blake2_128Concat,     // Hasher for key2 (safe for untrusted)
    [u8; 32],             // Key2
    Multisig<BlockNumberFor<T>, BalanceOf<T>, T::AccountId, T::MaxSignatories>,
>;
```

### Hasher Selection Guide

| Hasher | When to Use |
|--------|-------------|
| `Blake2_128Concat` | Default. Safe for user-controlled keys (accounts, hashes) |
| `Twox64Concat` | Fast. Use for keys you control (sequential indices, enum variants) |
| `Identity` | No hashing. Only for already-hashed keys |

---

## 10. Errors

```rust
#[pallet::error]
pub enum Error<T> {
    /// Threshold must be 2 or greater.
    MinimumThreshold,
    /// Call is already approved by this signatory.
    AlreadyApproved,
    /// Multisig operation not found in storage.
    NotFound,
    /// Only the original creator can cancel or update.
    NotOwner,
    /// There are too few signatories.
    TooFewSignatories,
    /// There are too many signatories.
    TooManySignatories,
}
```

One error variant per failure condition. Doc comments become the error message.

---

## 11. Events

```rust
#[pallet::event]
#[pallet::generate_deposit(pub(super) fn deposit_event)]
pub enum Event<T: Config> {
    /// A new operation has begun.
    NewMultisig {
        approving: T::AccountId,
        multisig: T::AccountId,
        call_hash: [u8; 32],
    },
    /// An operation has been executed.
    MultisigExecuted {
        approving: T::AccountId,
        timepoint: Timepoint<BlockNumberFor<T>>,
        multisig: T::AccountId,
        call_hash: [u8; 32],
        result: DispatchResult,
    },
}
```

Emit events after successful state changes:
```rust
Self::deposit_event(Event::NewMultisig { approving: who, multisig: id, call_hash });
```

---

## 12. Hooks

```rust
#[pallet::hooks]
impl<T: Config> Hooks<frame_system::pallet_prelude::BlockNumberFor<T>> for Pallet<T> {}
```

Available hooks: `on_initialize`, `on_finalize`, `on_idle`, `on_runtime_upgrade`, `integrity_test`.

---

## 13. Dispatchable Functions

```rust
#[pallet::call]
impl<T: Config> Pallet<T> {
    /// Description of the extrinsic.
    ///
    /// ## Complexity
    /// O(S + Z) where S is signatories and Z is call length.
    #[pallet::call_index(0)]
    #[pallet::weight(T::WeightInfo::my_extrinsic(param))]
    pub fn my_extrinsic(
        origin: OriginFor<T>,
        param: u32,
    ) -> DispatchResult {
        let who = ensure_signed(origin)?;

        // Validate
        ensure!(param > 0, Error::<T>::MinimumThreshold);

        // Write
        SomeValue::<T>::put(param);

        // Emit event
        Self::deposit_event(Event::SomethingHappened { who, value: param });

        Ok(())
    }
}
```

### Key Patterns

- `#[pallet::call_index(N)]` -- sequential, never reuse indices
- `#[pallet::weight(...)]` -- use `T::WeightInfo::function_name(...)` from benchmarks
- Origin checks: `ensure_signed(origin)?`, `ensure_root(origin)?`, `T::ForceOrigin::ensure_origin(origin)?`
- Return `DispatchResult` (simple) or `DispatchResultWithPostInfo` (with actual weight)
- Pattern: validate -> write -> emit event

---

## 14. Type Definitions

For types stored in storage, derive the required traits:

```rust
#[derive(
    Clone,
    Eq,
    PartialEq,
    Encode,
    Decode,
    DecodeWithMemTracking,
    Default,
    Debug,
    TypeInfo,
    MaxEncodedLen,
)]
pub struct MyData<Balance, AccountId> {
    pub amount: Balance,
    pub owner: AccountId,
}
```

For bounded collections:
```rust
#[scale_info(skip_type_params(MaxApprovals))]
pub struct Multisig<BlockNumber, Balance, AccountId, MaxApprovals>
where
    MaxApprovals: Get<u32>,
{
    pub when: Timepoint<BlockNumber>,
    pub deposit: Balance,
    pub depositor: AccountId,
    pub approvals: BoundedVec<AccountId, MaxApprovals>,
}
```

---

## 15. Cargo.toml

```toml
[package]
name = "pallet-my-pallet"
version = "1.0.0"
authors.workspace = true
edition.workspace = true
license = "Apache-2.0"

[lints]
workspace = true

[dependencies]
codec = { workspace = true }
frame = { workspace = true, features = ["runtime"] }
scale-info = { features = ["derive"], workspace = true }
log = { workspace = true }

[dev-dependencies]
pallet-balances = { workspace = true, default-features = true }

[features]
default = ["std"]
std = [
    "codec/std",
    "frame/std",
    "log/std",
    "scale-info/std",
]
runtime-benchmarks = [
    "frame/runtime-benchmarks",
    "pallet-balances/runtime-benchmarks",
]
try-runtime = [
    "frame/try-runtime",
    "pallet-balances/try-runtime",
]
```

---

## 16. Test Mock Runtime

```rust
#![cfg(test)]

use super::*;
use crate as pallet_my_pallet;
use frame::{prelude::*, runtime::prelude::*, testing_prelude::*};

type Block = frame_system::mocking::MockBlockU32<Test>;

construct_runtime!(
    pub struct Test {
        System: frame_system,
        Balances: pallet_balances,
        MyPallet: pallet_my_pallet,
    }
);

#[derive_impl(frame_system::config_preludes::TestDefaultConfig)]
impl frame_system::Config for Test {
    type Block = Block;
    type AccountData = pallet_balances::AccountData<u64>;
}

#[derive_impl(pallet_balances::config_preludes::TestDefaultConfig)]
impl pallet_balances::Config for Test {
    type ReserveIdentifier = [u8; 8];
    type AccountStore = System;
    type RuntimeHoldReason = RuntimeHoldReason;
}

parameter_types! {
    pub static DepositBase: u64 = 1;
    pub static DepositFactor: u64 = 1;
}

impl Config for Test {
    type RuntimeEvent = RuntimeEvent;
    type RuntimeCall = RuntimeCall;
    type Fungible = Balances;
    type DepositBase = DepositBase;
    type DepositFactor = DepositFactor;
    type MaxItems = ConstU32<100>;
    type WeightInfo = ();
    type BlockNumberProvider = frame_system::Pallet<Test>;
}

pub fn new_test_ext() -> TestState {
    let mut t = frame_system::GenesisConfig::<Test>::default().build_storage().unwrap();
    pallet_balances::GenesisConfig::<Test> {
        balances: vec![(1, 10), (2, 10), (3, 10), (4, 5), (5, 2)],
        ..Default::default()
    }
    .assimilate_storage(&mut t)
    .unwrap();
    let mut ext = TestState::new(t);
    ext.execute_with(|| System::set_block_number(1));
    ext
}

#[test]
fn basic_test() {
    new_test_ext().execute_with(|| {
        assert_ok!(MyPallet::my_extrinsic(RuntimeOrigin::signed(1), 42));
        assert_eq!(SomeValue::<Test>::get(), 42);
    });
}
```

---

## 17. Defensive Programming

### `ensure!()` for validation

```rust
ensure!(!other_signatories.is_empty(), Error::<T>::TooFewSignatories);
ensure!(other_signatories.len() < max_sigs, Error::<T>::TooManySignatories);
```

### `defensive!()` for non-fatal assertions

```rust
let released = T::Fungible::release(
    &HoldReason::MultisigOperation.into(), &who, excess, Precision::BestEffort,
)?;
if released != excess {
    defensive!(
        "Failed to release full amount. (Requested, Actual): ",
        (excess, released)
    );
}
```

### Safe arithmetic

```rust
// Use saturating ops (clamp at bounds)
value.saturating_add(other)
value.saturating_sub(other)

// Use checked ops (return None on overflow)
value.checked_add(other).ok_or(Error::<T>::Overflow)?

// Never use raw +, -, *, / on user-controlled values
```

### BoundedVec instead of Vec

```rust
// In storage: always use BoundedVec
pub approvals: BoundedVec<AccountId, MaxApprovals>,

// Inserting with bounds checking
m.approvals.try_insert(pos, who.clone())
    .map_err(|_| Error::<T>::TooManySignatories)?;
```

### No panics in dispatchables

```rust
// Bad: unwrap() panics
let value = storage.get(key).unwrap();

// Good: return error
let value = storage.get(key).ok_or(Error::<T>::NotFound)?;

// If unwrap is truly safe, add proof comment:
Decode::decode(&mut TrailingZeroInput::new(entropy.as_ref()))
    .expect("infinite length input; no invalid inputs for type; qed")
```

---

## 18. Formatting (Mandatory Final Step)

After all code changes are complete, you MUST run these formatting checks and fix any issues:

### Rust Formatting
```bash
# Check formatting
cargo +nightly fmt --all -- --check

# If the check fails, auto-format:
cargo +nightly fmt --all
```

### TOML Formatting (only if Cargo.toml files were modified)
```bash
# Check formatting — only run on Cargo.toml files that were actually changed
taplo format --check --config .config/taplo.toml <path/to/changed/Cargo.toml>

# If the check fails, auto-format the specific files:
taplo format --config .config/taplo.toml <path/to/changed/Cargo.toml>
```

**Important**: Only format TOML files that were modified as part of this task. Do NOT run taplo on the entire workspace — if it triggers on crates we are not working on, we should not change them.

---

## 19. Checklist

When creating or modifying a pallet:

**Structure**
- [ ] `#![cfg_attr(not(feature = "std"), no_std)]` at top
- [ ] `extern crate alloc` for `Vec`, `Box`, etc.
- [ ] Module declarations for benchmarking, tests, weights, migrations
- [ ] `pub use pallet::*` for re-exports

**Config**
- [ ] Extends `frame_system::Config`
- [ ] `RuntimeEvent` type included
- [ ] Constants marked with `#[pallet::constant]`
- [ ] `WeightInfo` type for benchmarks
- [ ] Trait objects for loose coupling (not concrete pallets)

**Storage**
- [ ] Appropriate hasher per key type
- [ ] `BoundedVec` instead of raw `Vec`
- [ ] `StorageVersion` set and tracked

**Dispatchables**
- [ ] Sequential `#[pallet::call_index(N)]`
- [ ] Weight annotations using `T::WeightInfo::*`
- [ ] Proper origin checks
- [ ] Pattern: validate -> write -> emit event
- [ ] No panics (`unwrap`, `expect`, array indexing)

**Cargo.toml**
- [ ] `std` feature with all dependency std features
- [ ] `runtime-benchmarks` feature propagated
- [ ] `try-runtime` feature propagated

For detailed patterns and templates, see [PALLET_STRUCTURE_REFERENCE.md](resources/PALLET_STRUCTURE_REFERENCE.md) and [CONFIG_PATTERNS.md](resources/CONFIG_PATTERNS.md).
