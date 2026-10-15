---
name: runtime-configurator
description: Wires pallets into Substrate runtimes with construct_runtime!, parameter_types!, impl Config, feature flags, genesis config, and type aliases. Use when adding pallets to a runtime or configuring existing ones.
---

# Runtime Configurator

## 1. Purpose

Help developers wire FRAME pallets into Substrate runtimes correctly. This covers `construct_runtime!`, `parameter_types!`, `impl pallet::Config for Runtime`, Cargo.toml feature flags, genesis configuration, and the common type aliases that compose a runtime.

## 2. When to Use This Skill

- Adding a new pallet to an existing runtime
- Configuring `impl Config` for a pallet in a runtime
- Setting up `construct_runtime!` macro entries
- Declaring `parameter_types!` for runtime constants
- Propagating feature flags in runtime `Cargo.toml`
- Setting up genesis config for a pallet
- Configuring `Executive`, `SignedExtra`, or other runtime-level types
- Debugging runtime compilation errors related to pallet wiring

## 3. Platform Detection

Look for these indicators:
- `construct_runtime!` macro invocation
- `impl pallet_*::Config for Runtime` blocks
- `parameter_types!` declarations
- Runtime `Cargo.toml` with `frame-*` or `pallet-*` dependencies
- Files named `lib.rs` under `*/runtime/` directories

---

## 4. construct_runtime! Macro

### Basic Structure

```rust
construct_runtime!(
    pub struct Runtime {
        // System pallets (always first)
        System: frame_system = 0,
        ParachainSystem: cumulus_pallet_parachain_system = 1,
        Timestamp: pallet_timestamp = 3,
        ParachainInfo: parachain_info = 4,

        // Monetary
        Balances: pallet_balances = 10,
        TransactionPayment: pallet_transaction_payment = 11,

        // Governance
        Sudo: pallet_sudo = 15,

        // Collator support
        Authorship: pallet_authorship = 20,
        CollatorSelection: pallet_collator_selection = 21,
        Session: pallet_session = 22,
        Aura: pallet_aura = 23,
        AuraExt: cumulus_pallet_aura_ext = 24,

        // XCM
        XcmpQueue: cumulus_pallet_xcmp_queue = 30,
        PolkadotXcm: pallet_xcm = 31,
        CumulusXcm: cumulus_pallet_xcm = 32,
        MessageQueue: pallet_message_queue = 33,

        // Application pallets
        Multisig: pallet_multisig = 40,
        Proxy: pallet_proxy = 41,
        Utility: pallet_utility = 42,
    }
);
```

### Key Rules

- **Indices are stable**: Once assigned, never reuse or reorder. Indices encode into extrinsic addresses.
- **System must be index 0**: `frame_system` is always the first pallet.
- **Leave gaps**: Use gaps between groups (0, 10, 20, 30...) for future additions.
- **Multi-instance pallets**: Use `Instance1`, `Instance2`, etc.:
  ```rust
  Assets: pallet_assets::<Instance1> = 50,
  PoolAssets: pallet_assets::<Instance2> = 51,
  ```

---

## 5. parameter_types! Declarations

```rust
parameter_types! {
    pub const BlockHashCount: BlockNumber = 4096;
    pub const Version: RuntimeVersion = VERSION;
    pub RuntimeBlockLength: BlockLength =
        BlockLength::max_with_normal_ratio(5 * 1024 * 1024, NORMAL_DISPATCH_RATIO);
    pub RuntimeBlockWeights: BlockWeights =
        BlockWeights::with_sensible_defaults(
            Weight::from_parts(WEIGHT_REF_TIME_PER_SECOND.saturating_mul(2), u64::MAX),
            NORMAL_DISPATCH_RATIO,
        );
    pub const SS58Prefix: u16 = 42;
    pub const ExistentialDeposit: Balance = EXISTENTIAL_DEPOSIT;
    pub const MaxLocks: u32 = 50;
    pub const MaxReserves: u32 = 50;
    pub const MaxHolds: u32 = 64;
    pub const MaxFreezes: u32 = 64;
    pub const DepositBase: Balance = deposit(1, 88);
    pub const DepositFactor: Balance = deposit(0, 32);
    pub const MaxSignatories: u32 = 100;
}
```

### Deposit Calculation Pattern

```rust
/// Calculate deposit amount based on number of items and bytes.
pub const fn deposit(items: u32, bytes: u32) -> Balance {
    items as Balance * 20 * CENTS + (bytes as Balance) * STORAGE_BYTE_FEE
}
```

---

## 6. Common Pallet Config Implementations

### frame_system

```rust
#[derive_impl(frame_system::config_preludes::ParaChainDefaultConfig)]
impl frame_system::Config for Runtime {
    type Block = Block;
    type BlockHashCount = BlockHashCount;
    type BlockLength = RuntimeBlockLength;
    type BlockWeights = RuntimeBlockWeights;
    type DbWeight = RocksDbWeight;
    type Nonce = Nonce;
    type Hash = Hash;
    type AccountId = AccountId;
    type Lookup = AccountIdLookup<AccountId, ()>;
    type AccountData = pallet_balances::AccountData<Balance>;
    type MaxConsumers = frame_support::traits::ConstU32<16>;
    type SS58Prefix = SS58Prefix;
    type OnSetCode = cumulus_pallet_parachain_system::ParachainSetCode<Self>;
    type Version = Version;
    type RuntimeEvent = RuntimeEvent;
    type RuntimeCall = RuntimeCall;
    type RuntimeOrigin = RuntimeOrigin;
    type RuntimeTask = RuntimeTask;
    type PalletInfo = PalletInfo;
    type SystemWeightInfo = weights::frame_system::WeightInfo<Runtime>;
}
```

### pallet_balances

```rust
impl pallet_balances::Config for Runtime {
    type MaxLocks = MaxLocks;
    type MaxReserves = MaxReserves;
    type ReserveIdentifier = [u8; 8];
    type Balance = Balance;
    type RuntimeEvent = RuntimeEvent;
    type DustRemoval = ();
    type ExistentialDeposit = ExistentialDeposit;
    type AccountStore = System;
    type WeightInfo = weights::pallet_balances::WeightInfo<Runtime>;
    type RuntimeHoldReason = RuntimeHoldReason;
    type RuntimeFreezeReason = RuntimeFreezeReason;
    type FreezeIdentifier = ();
    type MaxFreezes = MaxFreezes;
    type MaxHolds = MaxHolds;
}
```

### pallet_timestamp

```rust
impl pallet_timestamp::Config for Runtime {
    type Moment = u64;
    type OnTimestampSet = Aura;
    type MinimumPeriod = ConstU64<0>;  // 0 for async backing, SLOT_DURATION / 2 otherwise
    type WeightInfo = weights::pallet_timestamp::WeightInfo<Runtime>;
}
```

### pallet_transaction_payment

```rust
parameter_types! {
    pub const TransactionByteFee: Balance = 10 * MICROCENTS;
    pub const OperationalFeeMultiplier: u8 = 5;
}

impl pallet_transaction_payment::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type OnChargeTransaction =
        pallet_transaction_payment::FungibleAdapter<Balances, DealWithFees<Runtime>>;
    type OperationalFeeMultiplier = OperationalFeeMultiplier;
    type WeightToFee = WeightToFee;
    type LengthToFee = ConstantMultiplier<Balance, TransactionByteFee>;
    type FeeMultiplierUpdate = SlowAdjustingFeeUpdate<Self>;
}
```

### pallet_multisig

```rust
impl pallet_multisig::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type RuntimeCall = RuntimeCall;
    type Fungible = Balances;
    type DepositBase = DepositBase;
    type DepositFactor = DepositFactor;
    type MaxSignatories = MaxSignatories;
    type WeightInfo = weights::pallet_multisig::WeightInfo<Runtime>;
    type BlockNumberProvider = System;
}
```

### pallet_proxy

```rust
parameter_types! {
    pub const ProxyDepositBase: Balance = deposit(1, 40);
    pub const ProxyDepositFactor: Balance = deposit(0, 33);
    pub const AnnouncementDepositBase: Balance = deposit(1, 48);
    pub const AnnouncementDepositFactor: Balance = deposit(0, 66);
    pub const MaxProxies: u16 = 32;
    pub const MaxPending: u16 = 32;
}

impl pallet_proxy::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type RuntimeCall = RuntimeCall;
    type Currency = Balances;
    type ProxyType = ProxyType;
    type ProxyDepositBase = ProxyDepositBase;
    type ProxyDepositFactor = ProxyDepositFactor;
    type MaxProxies = MaxProxies;
    type MaxPending = MaxPending;
    type CallHasher = BlakeTwo256;
    type AnnouncementDepositBase = AnnouncementDepositBase;
    type AnnouncementDepositFactor = AnnouncementDepositFactor;
    type WeightInfo = weights::pallet_proxy::WeightInfo<Runtime>;
}
```

### pallet_utility

```rust
impl pallet_utility::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type RuntimeCall = RuntimeCall;
    type PalletsOrigin = OriginCaller;
    type WeightInfo = weights::pallet_utility::WeightInfo<Runtime>;
}
```

### pallet_session (for parachains)

```rust
impl pallet_session::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type ValidatorId = <Self as frame_system::Config>::AccountId;
    type ValidatorIdOf = pallet_collator_selection::IdentityCollator;
    type ShouldEndSession = pallet_session::PeriodicSessions<ConstU32<PERIOD>, ConstU32<OFFSET>>;
    type NextSessionRotation = pallet_session::PeriodicSessions<ConstU32<PERIOD>, ConstU32<OFFSET>>;
    type SessionManager = CollatorSelection;
    type SessionHandler = <SessionKeys as OpaqueKeys>::KeyTypeIdProviders;
    type Keys = SessionKeys;
    type WeightInfo = weights::pallet_session::WeightInfo<Runtime>;
}
```

### pallet_aura (for parachains)

```rust
impl pallet_aura::Config for Runtime {
    type AuthorityId = AuraId;
    type DisabledValidators = ();
    type MaxAuthorities = ConstU32<100_000>;
    type AllowMultipleBlocksPerSlot = ConstBool<true>;  // For async backing
    type SlotDuration = ConstU64<SLOT_DURATION>;
}
```

### pallet_collator_selection

```rust
parameter_types! {
    pub const Period: u32 = 6 * HOURS;
    pub const Offset: u32 = 0;
    pub const PotId: PalletId = PalletId(*b"PotStake");
}

impl pallet_collator_selection::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type Currency = Balances;
    type UpdateOrigin = CollatorSelectionUpdateOrigin;
    type PotId = PotId;
    type MaxCandidates = ConstU32<100>;
    type MinEligibleCollators = ConstU32<4>;
    type MaxInvulnerables = ConstU32<20>;
    type KickThreshold = Period;
    type ValidatorId = <Self as frame_system::Config>::AccountId;
    type ValidatorIdOf = pallet_collator_selection::IdentityCollator;
    type ValidatorRegistration = Session;
    type WeightInfo = weights::pallet_collator_selection::WeightInfo<Runtime>;
}
```

---

## 7. Runtime Type Aliases

```rust
/// Block type as expected by the runtime.
pub type Block = generic::Block<Header, UncheckedExtrinsic>;

/// BlockId type as expected by the runtime.
pub type BlockId = generic::BlockId<Block>;

/// Unchecked extrinsic type.
pub type UncheckedExtrinsic =
    generic::UncheckedExtrinsic<Address, RuntimeCall, Signature, SignedExtra>;

/// Signed extra fields for transactions.
pub type SignedExtra = (
    frame_system::CheckNonZeroSender<Runtime>,
    frame_system::CheckSpecVersion<Runtime>,
    frame_system::CheckTxVersion<Runtime>,
    frame_system::CheckGenesis<Runtime>,
    frame_system::CheckEra<Runtime>,
    frame_system::CheckNonce<Runtime>,
    frame_system::CheckWeight<Runtime>,
    pallet_transaction_payment::ChargeTransactionPayment<Runtime>,
    cumulus_primitives_storage_weight_reclaim::StorageWeightReclaim<Runtime>,
    frame_metadata_hash_extension::CheckMetadataHash<Runtime>,
);

/// Executive type combining all runtime components.
pub type Executive = frame_executive::Executive<
    Runtime,
    Block,
    frame_system::ChainContext<Runtime>,
    Runtime,
    AllPalletsWithSystem,
    Migrations,
>;
```

---

## 8. Cargo.toml Feature Flags

### Runtime Cargo.toml pattern

```toml
[features]
default = ["std"]
std = [
    "codec/std",
    "frame-executive/std",
    "frame-support/std",
    "frame-system/std",
    "frame-system-rpc-runtime-api/std",
    "pallet-balances/std",
    "pallet-multisig/std",
    "pallet-timestamp/std",
    "pallet-transaction-payment/std",
    "pallet-transaction-payment-rpc-runtime-api/std",
    "sp-api/std",
    "sp-block-builder/std",
    "sp-core/std",
    "sp-runtime/std",
    "sp-std/std",
    # ... every dependency must propagate std
]
runtime-benchmarks = [
    "frame-benchmarking/runtime-benchmarks",
    "frame-support/runtime-benchmarks",
    "frame-system/runtime-benchmarks",
    "pallet-balances/runtime-benchmarks",
    "pallet-multisig/runtime-benchmarks",
    "pallet-timestamp/runtime-benchmarks",
    "sp-runtime/runtime-benchmarks",
    # ... every pallet must propagate
]
try-runtime = [
    "frame-executive/try-runtime",
    "frame-support/try-runtime",
    "frame-system/try-runtime",
    "pallet-balances/try-runtime",
    "pallet-multisig/try-runtime",
    "pallet-timestamp/try-runtime",
    "sp-runtime/try-runtime",
    # ... every pallet must propagate
]
```

### Critical Rule

**Every pallet added to the runtime must appear in ALL THREE feature lists** (`std`, `runtime-benchmarks`, `try-runtime`). Missing features cause cryptic compilation errors.

---

## 9. derive_impl Presets

Modern runtimes use `derive_impl` to inherit sensible defaults:

```rust
// For parachain runtimes
#[derive_impl(frame_system::config_preludes::ParaChainDefaultConfig)]
impl frame_system::Config for Runtime { ... }

// For standalone chain runtimes
#[derive_impl(frame_system::config_preludes::SolochainDefaultConfig)]
impl frame_system::Config for Runtime { ... }

// For test runtimes
#[derive_impl(frame_system::config_preludes::TestDefaultConfig)]
impl frame_system::Config for Test { ... }

// For pallet-balances
#[derive_impl(pallet_balances::config_preludes::TestDefaultConfig)]
impl pallet_balances::Config for Test { ... }
```

---

## 10. Weights Integration

### Import weight modules

```rust
mod weights;

// In Config implementations:
type SystemWeightInfo = weights::frame_system::WeightInfo<Runtime>;
type WeightInfo = weights::pallet_multisig::WeightInfo<Runtime>;
```

### Weight file structure

```
runtime/src/weights/
    mod.rs              # pub mod declarations
    frame_system.rs
    pallet_balances.rs
    pallet_multisig.rs
    ...
```

### weights/mod.rs

```rust
pub mod frame_system;
pub mod pallet_balances;
pub mod pallet_multisig;
// ... one module per benchmarked pallet
```

---

## 11. RuntimeVersion

```rust
#[sp_version::runtime_version]
pub const VERSION: RuntimeVersion = RuntimeVersion {
    spec_name: alloc::borrow::Cow::Borrowed("my-parachain"),
    impl_name: alloc::borrow::Cow::Borrowed("my-parachain"),
    authoring_version: 1,
    spec_version: 1_000_000,
    impl_version: 0,
    apis: RUNTIME_API_VERSIONS,
    transaction_version: 1,
    system_version: 1,
};
```

- **spec_version**: Increment on any logic change. This triggers runtime upgrades.
- **transaction_version**: Increment when extrinsic format changes.

---

## 12. Adding a New Pallet - Step by Step

1. **Add dependency** to runtime `Cargo.toml`:
   ```toml
   [dependencies]
   pallet-my-pallet = { workspace = true }
   ```

2. **Add to feature flags** (std, runtime-benchmarks, try-runtime):
   ```toml
   std = ["pallet-my-pallet/std", ...]
   runtime-benchmarks = ["pallet-my-pallet/runtime-benchmarks", ...]
   try-runtime = ["pallet-my-pallet/try-runtime", ...]
   ```

3. **Add parameter_types!** for any constants the pallet needs.

4. **Implement Config**:
   ```rust
   impl pallet_my_pallet::Config for Runtime {
       type RuntimeEvent = RuntimeEvent;
       // ... other types
       type WeightInfo = weights::pallet_my_pallet::WeightInfo<Runtime>;
   }
   ```

5. **Add to construct_runtime!** with a unique index:
   ```rust
   MyPallet: pallet_my_pallet = 50,
   ```

6. **Add weight module** if benchmarks exist:
   ```rust
   // In weights/mod.rs
   pub mod pallet_my_pallet;
   ```

7. **Add genesis config** if the pallet has one (in genesis_config_presets.rs).

8. **Increment spec_version** in `RuntimeVersion`.

---

## 13. Formatting (Mandatory Final Step)

After all code changes are complete, you MUST run these formatting checks and fix any issues:

### Rust Formatting
```bash
cargo +nightly fmt --all -- --check
# If the check fails, auto-format:
cargo +nightly fmt --all
```

### TOML Formatting (only if Cargo.toml files were modified)
```bash
taplo format --check --config .config/taplo.toml <path/to/changed/Cargo.toml>
# If the check fails, auto-format the specific files:
taplo format --config .config/taplo.toml <path/to/changed/Cargo.toml>
```

---

## 14. Checklist

When adding a pallet to a runtime:

**Cargo.toml**
- [ ] Pallet added as dependency
- [ ] `std` feature includes `pallet-name/std`
- [ ] `runtime-benchmarks` feature includes `pallet-name/runtime-benchmarks`
- [ ] `try-runtime` feature includes `pallet-name/try-runtime`

**Runtime Config**
- [ ] `parameter_types!` declared for all constants
- [ ] `impl pallet::Config for Runtime` complete
- [ ] `WeightInfo` type points to benchmarked weights (or `()` for dev)
- [ ] `RuntimeEvent` type included
- [ ] `RuntimeHoldReason` / `RuntimeFreezeReason` if pallet uses holds/freezes

**construct_runtime!**
- [ ] Pallet listed with unique index
- [ ] Index follows numbering convention (gaps between groups)
- [ ] Multi-instance pallets use `<InstanceN>`

**Integration**
- [ ] Weight module added to `weights/mod.rs`
- [ ] Genesis config added if needed
- [ ] `spec_version` incremented
- [ ] Compiles with `SKIP_WASM_BUILD=1 cargo check -p <runtime>`

For detailed Config patterns per pallet, see [COMMON_CONFIGS.md](resources/COMMON_CONFIGS.md).
