---
name: migration-author
description: Guides creation of storage migrations for FRAME pallets, covering both multi-block SteppedMigration and single-block VersionedMigration patterns. Includes cursor-based iteration, weight metering, try-runtime hooks, and runtime registration. Use when storage layout changes require data migration.
---

# Migration Author

## 1. Purpose

Help write safe, tested storage migrations that transform on-chain data when pallet storage layouts change. Migrations are critical -- incorrect migrations can brick a chain or corrupt state.

## 2. When to Use This Skill

- Changing a storage item's type (e.g., adding/removing fields, changing Balance type)
- Converting from deprecated traits (e.g., `Currency` to `Fungible`)
- Removing old storage items and refunding deposits
- Renaming or restructuring storage items
- Any change that requires transforming existing on-chain data

## 3. Platform Detection

Look for these indicators:
- `StorageVersion` in pallet definition
- `OnRuntimeUpgrade` trait implementations
- `SteppedMigration` trait implementations
- `migrations.rs` files in pallet `src/` directories
- `#[storage_alias]` attributes
- `try-runtime` feature in `Cargo.toml`

---

## 4. Choosing Migration Type

### Multi-Block: `SteppedMigration`

Use when:
- The data set is large or unbounded (iterating all storage entries)
- Migration may exceed a single block's weight limit
- Requires cursor-based resumption across blocks

Registered with `pallet_migrations` in the runtime.

### Single-Block: `VersionedMigration` + `UncheckedOnRuntimeUpgrade`

Use when:
- The data set is small and bounded
- Migration fits within a single block
- Simple transformations (remove old storage, update a value)

Registered in the runtime's `Executive` migrations tuple.

---

## 5. Multi-Block SteppedMigration Pattern

From `substrate/frame/multisig/src/migrations.rs`:

```rust
use crate::*;
use frame::prelude::*;

pub mod v2 {
    use super::*;
    use frame::{
        deps::frame_support::{
            migrations::{MigrationId, SteppedMigration, SteppedMigrationError},
            weights::WeightMeter,
        },
        traits::ReservableCurrency,
    };

    const PALLET_MIGRATIONS_ID: &[u8; 15] = b"pallet-multisig";

    pub struct LazyMigrationV1ToV2<T, OldCurrency>(core::marker::PhantomData<(T, OldCurrency)>);

    impl<T, OldCurrency> SteppedMigration for LazyMigrationV1ToV2<T, OldCurrency>
    where
        T: Config,
        OldCurrency: ReservableCurrency<T::AccountId, Balance = BalanceOf<T>>,
    {
        type Cursor = BoundedVec<u8, ConstU32<256>>;
        type Identifier = MigrationId<15>;

        fn id() -> Self::Identifier {
            MigrationId { pallet_id: *PALLET_MIGRATIONS_ID, version_from: 1, version_to: 2 }
        }

        fn step(
            mut cursor: Option<Self::Cursor>,
            meter: &mut WeightMeter,
        ) -> Result<Option<Self::Cursor>, SteppedMigrationError> {
            let required = T::WeightInfo::v2_migration_step(T::MaxSignatories::get());

            // Check minimum weight before starting
            if meter.remaining().any_lt(required) {
                return Err(SteppedMigrationError::InsufficientWeight { required });
            }

            // Resume from cursor or start fresh
            let mut iter = if let Some(ref last_key) = cursor {
                Multisigs::<T>::iter_from(last_key.to_vec())
            } else {
                Multisigs::<T>::iter()
            };

            // Process entries until weight runs out
            loop {
                if meter.try_consume(required).is_err() {
                    break;
                }

                if let Some((multisig_account, call_hash, multisig_data)) = iter.next() {
                    // --- Perform the migration for this entry ---
                    if !multisig_data.deposit.is_zero() {
                        let depositor = &multisig_data.depositor;
                        let deposit = multisig_data.deposit;

                        let remaining = OldCurrency::unreserve(depositor, deposit);
                        let to_hold = deposit.saturating_sub(remaining);
                        if !to_hold.is_zero() {
                            if let Err(err) = T::Fungible::hold(
                                &HoldReason::MultisigOperation.into(),
                                depositor,
                                to_hold,
                            ) {
                                log!(error, "Migration: Failed to hold: {:?}", err);
                            }
                        }
                    }

                    // Update cursor for resumption
                    let raw_key =
                        Multisigs::<T>::hashed_key_for(&multisig_account, &call_hash);
                    cursor = Some(BoundedVec::try_from(raw_key).unwrap_or_else(
                        |mut raw_key| {
                            raw_key.truncate(256);
                            BoundedVec::try_from(raw_key)
                                .expect("truncated to bound; qed")
                        },
                    ));
                } else {
                    // No more entries -- migration complete
                    return Ok(None);
                }
            }

            // Ran out of weight, return cursor to resume next block
            Ok(cursor)
        }
    }
}
```

### Key Elements

- **Cursor**: `BoundedVec<u8, ConstU32<256>>` stores the last processed key for resumption
- **Identifier**: `MigrationId<N>` with `pallet_id`, `version_from`, `version_to`
- **Weight checking**: `meter.remaining().any_lt(required)` before starting, `meter.try_consume(required)` per iteration
- **Iterator resumption**: `StorageMap::iter_from(last_key.to_vec())`
- **Return values**: `Ok(None)` = complete, `Ok(Some(cursor))` = continue next block
- **Error handling**: Log errors, don't panic -- continue migration even if individual entries fail

---

## 6. Single-Block Migration Pattern

### Using VersionedMigration wrapper

```rust
use frame_support::migrations::VersionedMigration;
use frame_support::traits::UncheckedOnRuntimeUpgrade;

pub mod v1 {
    use super::*;

    pub struct InnerMigrateV0ToV1<T: Config>(PhantomData<T>);

    impl<T: Config> UncheckedOnRuntimeUpgrade for InnerMigrateV0ToV1<T> {
        fn on_runtime_upgrade() -> Weight {
            // Perform migration logic
            let count = OldStorage::<T>::drain().count() as u64;
            T::DbWeight::get().reads_writes(count + 1, count + 1)
        }
    }

    /// Wrapped migration with automatic version checking.
    pub type MigrateV0ToV1<T> = VersionedMigration<
        0,              // version_from
        1,              // version_to
        InnerMigrateV0ToV1<T>,
        Pallet<T>,
        <T as frame_system::Config>::DbWeight,
    >;
}
```

### Using OnRuntimeUpgrade directly (with manual version checks)

From `substrate/frame/multisig/src/migrations.rs`:

```rust
pub mod v1 {
    use super::*;

    #[frame::storage_alias]
    type Calls<T: Config> = StorageMap<
        Pallet<T>,
        Identity,
        [u8; 32],
        (OpaqueCall<T>, <T as frame_system::Config>::AccountId, BalanceOf<T>),
    >;

    pub struct MigrateToV1<T, OldCurrency>(core::marker::PhantomData<(T, OldCurrency)>);

    impl<T: Config, OldCurrency> OnRuntimeUpgrade for MigrateToV1<T, OldCurrency>
    where
        OldCurrency: ReservableCurrency<T::AccountId, Balance = BalanceOf<T>>,
    {
        fn on_runtime_upgrade() -> Weight {
            let current = Pallet::<T>::in_code_storage_version();
            let onchain = Pallet::<T>::on_chain_storage_version();

            if onchain > 0 {
                return T::DbWeight::get().reads(1);
            }

            let mut call_count = 0u64;
            Calls::<T>::drain().for_each(|(_call_hash, (_data, caller, deposit))| {
                OldCurrency::unreserve(&caller, deposit);
                call_count.saturating_inc();
            });

            current.put::<Pallet<T>>();

            T::DbWeight::get().reads_writes(
                call_count.saturating_add(1),
                call_count.saturating_mul(2).saturating_add(1),
            )
        }
    }
}
```

---

## 7. Storage Alias for Old Layouts

Use `#[storage_alias]` to define the old storage layout:

```rust
use frame::prelude::*;

mod v0 {
    use super::*;

    // Old storage map with different value type
    #[frame::storage_alias]
    pub type MyStorage<T: Config> = StorageMap<
        Pallet<T>,
        Blake2_128Concat,
        <T as frame_system::Config>::AccountId,
        OldValueType,
    >;
}
```

This lets you read old data before writing it in the new format.

---

## 8. StorageVersion Tracking

### In the pallet definition

```rust
/// The in-code storage version.
const STORAGE_VERSION: StorageVersion = StorageVersion::new(2);

#[pallet::pallet]
#[pallet::storage_version(STORAGE_VERSION)]
pub struct Pallet<T>(_);
```

### Checking versions in migrations

```rust
let current = Pallet::<T>::in_code_storage_version();  // What the code expects
let onchain = Pallet::<T>::on_chain_storage_version();  // What's on chain

if onchain > 0 {
    log!(info, "Migration already applied");
    return T::DbWeight::get().reads(1);
}

// After migration:
current.put::<Pallet<T>>();  // Update on-chain version
```

---

## 9. try-runtime Hooks

Verify migrations with `pre_upgrade` and `post_upgrade`:

```rust
#[cfg(feature = "try-runtime")]
fn pre_upgrade() -> Result<Vec<u8>, TryRuntimeError> {
    use codec::Encode;

    // Collect state before migration for verification
    let mut depositor_totals: BTreeMap<Vec<u8>, BalanceOf<T>> = BTreeMap::new();
    let mut entry_count: u64 = 0;

    for (_multisig, _call_hash, multisig_data) in Multisigs::<T>::iter() {
        if !multisig_data.deposit.is_zero() {
            let depositor_key = multisig_data.depositor.encode();
            depositor_totals
                .entry(depositor_key)
                .and_modify(|total| *total = total.saturating_add(multisig_data.deposit))
                .or_insert(multisig_data.deposit);
            entry_count += 1;
        }
    }

    Ok((depositor_totals, entry_count).encode())
}

#[cfg(feature = "try-runtime")]
fn post_upgrade(state: Vec<u8>) -> Result<(), TryRuntimeError> {
    use codec::Decode;
    use frame::traits::fungible::InspectHold;

    let (depositor_totals, entry_count): (BTreeMap<Vec<u8>, BalanceOf<T>>, u64) =
        Decode::decode(&mut &state[..]).expect("pre_upgrade provides valid state; qed");

    // Verify each depositor has the expected hold
    for (depositor_key, expected_hold) in depositor_totals.iter() {
        let depositor: T::AccountId = Decode::decode(&mut &depositor_key[..])
            .expect("depositor was encoded correctly; qed");
        let actual_hold =
            T::Fungible::balance_on_hold(&HoldReason::MultisigOperation.into(), &depositor);
        ensure!(actual_hold >= *expected_hold, "Hold amount insufficient");
    }

    Ok(())
}
```

### Pattern

1. `pre_upgrade`: Capture state that should be preserved (totals, counts, specific values)
2. Run migration
3. `post_upgrade`: Verify the state was correctly transformed

---

## 10. Logging

Use the pallet's `log!` macro pattern:

```rust
pub const LOG_TARGET: &'static str = "runtime::multisig";

#[macro_export]
macro_rules! log {
    ($level:tt, $patter:expr $(, $values:expr)* $(,)?) => {
        log::$level!(
            target: crate::LOG_TARGET,
            concat!("[{:?}] ", $patter),
            <frame_system::Pallet<T>>::block_number() $(, $values)*
        )
    };
}

// Usage in migration:
log!(info, "Migration v1 to v2 complete");
log!(warn, "Could not fully unreserve deposit for {:?}", depositor);
log!(error, "Failed to hold {:?}: {:?}", amount, err);
```

---

## 11. Runtime Registration

### For SteppedMigration (multi-block)

Register in `pallet_migrations::Config`:

```rust
impl pallet_migrations::Config for Runtime {
    type Migrations = (
        pallet_multisig::migrations::v2::LazyMigrationV1ToV2<Runtime, Balances>,
        // ... other stepped migrations
    );
}
```

### For OnRuntimeUpgrade (single-block)

Register in the `Executive` type or migrations tuple:

```rust
type Migrations = (
    pallet_multisig::migrations::v1::MigrateToV1<Runtime, Balances>,
    // ... other single-block migrations
);

pub type Executive = frame_executive::Executive<
    Runtime,
    Block,
    frame_system::ChainContext<Runtime>,
    Runtime,
    AllPalletsWithSystem,
    Migrations,  // <-- listed here
>;
```

---

## 12. Benchmarking Migration Steps

```rust
#[benchmark]
fn v2_migration_step(s: Linear<2, { T::MaxSignatories::get() }>) -> Result<(), BenchmarkError> {
    // Setup: create a storage entry to migrate
    // ...

    #[block]
    {
        // The actual migration step logic
        let mut iter = Multisigs::<T>::iter();
        let (account, hash, data) = iter.next().ok_or("no entry")?;
        // ... migration logic ...
        let _raw_key = Multisigs::<T>::hashed_key_for(&account, &hash);
    }

    // Verify
    Ok(())
}
```

Add the benchmark to `WeightInfo` so migrations can check weight:

```rust
pub trait WeightInfo {
    // ... other weights ...
    fn v2_migration_step(s: u32) -> Weight;
}
```

---

## 13. Formatting (Mandatory Final Step)

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

## 14. Checklist

Before finalizing a migration:

**Structure**
- [ ] Old storage layout defined with `#[storage_alias]`
- [ ] `StorageVersion` incremented in pallet (`const STORAGE_VERSION`)
- [ ] Migration type chosen appropriately (stepped vs single-block)

**Correctness**
- [ ] All old data is correctly transformed to new format
- [ ] Deposits/reserves/holds are correctly converted
- [ ] No data loss during migration
- [ ] Error cases handled gracefully (log, don't panic)

**Weight**
- [ ] Weight properly accounted for (reads + writes per entry)
- [ ] Weight meter checked before each step (for stepped migrations)
- [ ] Benchmark exists for migration step

**Testing**
- [ ] `pre_upgrade` captures state for verification
- [ ] `post_upgrade` verifies migration correctness
- [ ] `#[cfg(feature = "try-runtime")]` gating on try-runtime hooks

**Integration**
- [ ] Migration registered in runtime configuration
- [ ] Cursor handles resumption correctly (for stepped migrations)
- [ ] Version guard prevents re-running completed migrations

For detailed reference implementations, see [STEPPED_MIGRATION_REFERENCE.md](resources/STEPPED_MIGRATION_REFERENCE.md) and [VERSIONED_MIGRATION_REFERENCE.md](resources/VERSIONED_MIGRATION_REFERENCE.md).
