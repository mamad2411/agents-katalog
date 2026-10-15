---
name: substrate-test-writer
description: Creates unit tests for FRAME pallets including mock runtime setup, ExtBuilder patterns, assertion helpers, event checking, and error testing. Use when writing or modifying pallet tests.
---

# Substrate Test Writer

## 1. Purpose

Help developers write comprehensive unit tests for FRAME pallets. Covers mock runtime setup, test helpers, assertion patterns, event verification, error testing, and balance/deposit checking.

## 2. When to Use This Skill

- Creating tests for a new pallet
- Adding test cases for new extrinsics or features
- Setting up a mock runtime (tests.rs or mock.rs)
- Writing negative tests (error condition verification)
- Testing storage state changes
- Verifying events are emitted correctly
- Testing deposit/hold/freeze behavior

## 3. Platform Detection

Look for these indicators:
- `#[cfg(test)]` blocks
- `construct_runtime!` in test context
- `new_test_ext()` or `ExtBuilder` patterns
- `assert_ok!`, `assert_noop!`, `assert_err!` macros
- Files named `tests.rs`, `mock.rs`, or under `tests/` directories

---

## 4. Mock Runtime Setup

### Minimal mock runtime

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
    pub static MaxItems: u32 = 100;
}

impl pallet_my_pallet::Config for Test {
    type RuntimeEvent = RuntimeEvent;
    type RuntimeCall = RuntimeCall;
    type Fungible = Balances;
    type DepositBase = DepositBase;
    type MaxItems = MaxItems;
    type WeightInfo = ();
    type BlockNumberProvider = frame_system::Pallet<Test>;
}
```

### Key patterns

- Use `u64` for `Balance` and `AccountId` in tests (simpler than real types)
- `parameter_types! { pub static ... }` allows changing values per test
- `type WeightInfo = ()` uses the zero-weight fallback implementation
- `#[derive_impl(...TestDefaultConfig)]` inherits sensible test defaults

---

## 5. Test State Builder

### Simple new_test_ext

```rust
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
```

### ExtBuilder pattern (for configurable tests)

```rust
pub struct ExtBuilder {
    balances: Vec<(u64, u64)>,
    deposit_base: u64,
    max_items: u32,
}

impl Default for ExtBuilder {
    fn default() -> Self {
        Self {
            balances: vec![(1, 100), (2, 100), (3, 100)],
            deposit_base: 1,
            max_items: 100,
        }
    }
}

impl ExtBuilder {
    pub fn balances(mut self, balances: Vec<(u64, u64)>) -> Self {
        self.balances = balances;
        self
    }

    pub fn deposit_base(mut self, deposit: u64) -> Self {
        self.deposit_base = deposit;
        self
    }

    pub fn build(self) -> TestState {
        DEPOSIT_BASE.with(|v| *v.borrow_mut() = self.deposit_base);
        MAX_ITEMS.with(|v| *v.borrow_mut() = self.max_items);

        let mut t = frame_system::GenesisConfig::<Test>::default().build_storage().unwrap();
        pallet_balances::GenesisConfig::<Test> {
            balances: self.balances,
            ..Default::default()
        }
        .assimilate_storage(&mut t)
        .unwrap();

        let mut ext = TestState::new(t);
        ext.execute_with(|| System::set_block_number(1));
        ext
    }
}
```

Usage:
```rust
#[test]
fn test_with_custom_config() {
    ExtBuilder::default()
        .balances(vec![(1, 1000)])
        .deposit_base(5)
        .build()
        .execute_with(|| {
            // test code
        });
}
```

---

## 6. Core Assertion Macros

### assert_ok!

```rust
// Assert a dispatchable succeeds
assert_ok!(MyPallet::do_something(RuntimeOrigin::signed(1), 42));

// Capture the return value
let result = assert_ok!(MyPallet::do_something(RuntimeOrigin::signed(1), 42));
```

### assert_noop!

```rust
// Assert a dispatchable fails WITH a specific error AND no state changes
assert_noop!(
    MyPallet::do_something(RuntimeOrigin::signed(1), 0),
    Error::<Test>::InvalidValue
);
```

**Important**: `assert_noop!` verifies that storage is unchanged. Use this for testing validation errors.

### assert_err!

```rust
// Assert a dispatchable returns an error (state MAY have changed)
assert_err!(
    MyPallet::do_something(RuntimeOrigin::signed(1), 0),
    Error::<Test>::InvalidValue
);
```

### assert_last_event / assert_has_event

```rust
// Check the last event emitted
System::assert_last_event(
    Event::SomethingDone { who: 1, value: 42 }.into()
);

// Check that a specific event exists in the block
System::assert_has_event(
    Event::SomethingDone { who: 1, value: 42 }.into()
);
```

---

## 7. Event Testing

### Check all events in order

```rust
#[test]
fn events_are_emitted_correctly() {
    new_test_ext().execute_with(|| {
        // Clear events from genesis
        System::reset_events();

        assert_ok!(MyPallet::do_something(RuntimeOrigin::signed(1), 42));

        let events = System::events();
        assert_eq!(events.len(), 1);
        assert_eq!(
            events[0].event,
            RuntimeEvent::MyPallet(Event::SomethingDone { who: 1, value: 42 })
        );
    });
}
```

### Helper function pattern

```rust
fn last_event() -> RuntimeEvent {
    System::events().pop().expect("Event expected").event
}

fn expect_event<E: Into<RuntimeEvent>>(e: E) {
    assert_eq!(last_event(), e.into());
}
```

---

## 8. Balance and Deposit Testing

### Check free balance

```rust
assert_eq!(Balances::free_balance(1), 90);  // After spending 10
```

### Check held balance

```rust
use frame::traits::fungible::InspectHold;

let held = Balances::balance_on_hold(
    &pallet_my_pallet::HoldReason::MyOperation.into(),
    &1,
);
assert_eq!(held, 5);
```

### Check total balance

```rust
use frame::traits::fungible::Inspect;

assert_eq!(Balances::total_balance(&1), 100);  // free + held
```

### Check reserved balance (legacy)

```rust
use frame::traits::ReservableCurrency;
assert_eq!(Balances::reserved_balance(1), 5);
```

---

## 9. Storage State Testing

### Check storage values

```rust
// StorageValue
assert_eq!(SomeValue::<Test>::get(), 42);

// StorageMap
assert!(Accounts::<Test>::contains_key(1));
assert_eq!(Accounts::<Test>::get(1), Some(expected_data));

// StorageDoubleMap
assert!(Multisigs::<Test>::contains_key(account, call_hash));
```

### Check storage was cleared

```rust
assert!(!Accounts::<Test>::contains_key(1));
assert_eq!(SomeValue::<Test>::get(), 0); // ValueQuery default
```

---

## 10. Testing Error Conditions

### Test specific errors

```rust
#[test]
fn fails_with_insufficient_balance() {
    new_test_ext().execute_with(|| {
        assert_noop!(
            MyPallet::transfer(RuntimeOrigin::signed(1), 2, 1000),
            Error::<Test>::InsufficientBalance
        );
    });
}
```

### Test origin restrictions

```rust
#[test]
fn root_only_operation_rejects_signed() {
    new_test_ext().execute_with(|| {
        assert_noop!(
            MyPallet::force_set(RuntimeOrigin::signed(1), 42),
            DispatchError::BadOrigin
        );
    });
}

#[test]
fn root_only_operation_succeeds_with_root() {
    new_test_ext().execute_with(|| {
        assert_ok!(MyPallet::force_set(RuntimeOrigin::root(), 42));
    });
}
```

### Test unsigned rejection

```rust
#[test]
fn rejects_unsigned() {
    new_test_ext().execute_with(|| {
        assert_noop!(
            MyPallet::do_something(RuntimeOrigin::none(), 42),
            DispatchError::BadOrigin
        );
    });
}
```

---

## 11. Block Progression

### Advance to a specific block

```rust
fn run_to_block(n: u64) {
    while System::block_number() < n {
        if System::block_number() > 1 {
            System::on_finalize(System::block_number());
        }
        System::set_block_number(System::block_number() + 1);
        System::on_initialize(System::block_number());
        MyPallet::on_initialize(System::block_number());
    }
}
```

Usage:
```rust
#[test]
fn test_time_based_behavior() {
    new_test_ext().execute_with(|| {
        assert_ok!(MyPallet::start_something(RuntimeOrigin::signed(1)));
        run_to_block(10);
        // Check behavior after 10 blocks
    });
}
```

---

## 12. Testing with Multiple Calls

```rust
#[test]
fn full_workflow_test() {
    new_test_ext().execute_with(|| {
        // Step 1: Create
        assert_ok!(MyPallet::create(RuntimeOrigin::signed(1), 42));
        assert!(Storage::<Test>::contains_key(1));

        // Step 2: Update
        assert_ok!(MyPallet::update(RuntimeOrigin::signed(1), 43));
        assert_eq!(Storage::<Test>::get(1).unwrap().value, 43);

        // Step 3: Cannot update from wrong account
        assert_noop!(
            MyPallet::update(RuntimeOrigin::signed(2), 44),
            Error::<Test>::NotOwner
        );

        // Step 4: Delete
        assert_ok!(MyPallet::delete(RuntimeOrigin::signed(1)));
        assert!(!Storage::<Test>::contains_key(1));

        // Step 5: Verify deposit returned
        assert_eq!(Balances::free_balance(1), 100); // Full balance restored
    });
}
```

---

## 13. Benchmark Test Suite

In `benchmarking.rs`, always include:

```rust
impl_benchmark_test_suite!(
    MyPallet,
    crate::tests::new_test_ext(),
    crate::tests::Test,
);
```

This generates tests that verify all benchmarks execute successfully.

---

## 14. Test Naming Conventions

```rust
#[test]
fn create_works() { ... }           // Happy path

#[test]
fn create_fails_if_exists() { ... } // Error condition

#[test]
fn create_emits_event() { ... }     // Event verification

#[test]
fn create_charges_deposit() { ... } // Economic behavior

#[test]
fn create_root_only() { ... }       // Origin restriction

#[test]
fn cancel_returns_deposit() { ... } // Cleanup behavior
```

---

## 15. Formatting (Mandatory Final Step)

After all code changes are complete:

```bash
cargo +nightly fmt --all -- --check
# If fails: cargo +nightly fmt --all
```

---

## 16. Checklist

Before finalizing tests:

**Setup**
- [ ] Mock runtime has all required pallets
- [ ] `derive_impl(TestDefaultConfig)` used for standard configs
- [ ] Genesis state includes necessary balances/data
- [ ] Block number set to 1 in `new_test_ext()`

**Coverage**
- [ ] Happy path test for every dispatchable
- [ ] Error test for every `Error` variant
- [ ] Origin restriction tests (signed, root, unsigned)
- [ ] Event emission verified for state-changing operations
- [ ] Deposit/hold/balance changes verified

**Quality**
- [ ] `assert_noop!` used for validation errors (proves no state change)
- [ ] `assert_ok!` for successful calls
- [ ] Storage state verified after operations
- [ ] Tests are independent (no test ordering dependencies)
- [ ] Descriptive test names following convention
