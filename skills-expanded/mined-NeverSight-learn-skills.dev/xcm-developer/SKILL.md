---
name: xcm-developer
description: Configures XCM for parachains including barriers, asset transactors, location converters, fee handling, and cross-chain messaging. Use when working with XCM, cross-chain transfers, or xcm_config.rs files.
---

# XCM Developer

## 1. Purpose

Help developers configure XCM (Cross-Consensus Messaging) for parachain runtimes. Covers barrier setup, asset transactors, location conversion, fee handling, origin mapping, trust configuration, and testing XCM programs.

## 2. When to Use This Skill

- Creating or modifying `xcm_config.rs` for a parachain runtime
- Configuring XCM barriers (who can execute XCM)
- Setting up asset transactors (how assets are handled)
- Configuring location-to-account conversion
- Setting up reserve transfers or teleports
- Writing XCM programs or instructions
- Debugging XCM execution failures
- Configuring `pallet-xcm` in a runtime

## 3. Platform Detection

Look for these indicators:
- Files named `xcm_config.rs`
- `xcm_executor::Config` trait implementations
- `pallet_xcm::Config` implementations
- XCM types: `Location`, `Asset`, `Xcm`, `Instruction`
- Builder types from `xcm-builder` crate
- `cumulus_pallet_xcmp_queue` or `cumulus_pallet_xcm`

---

## 4. XCM Config File Structure

A typical `xcm_config.rs` follows this pattern:

```rust
use super::*; // imports from lib.rs
use xcm::latest::prelude::*;
use xcm_builder::*;
use xcm_executor::XcmExecutor;
use frame_support::{parameter_types, traits::{Everything, Nothing, Contains}};

// 1. Parameter types (locations, networks)
parameter_types! { ... }

// 2. Location-to-account converters
pub type LocationToAccountId = ( ... );

// 3. Asset transactors
pub type LocalAssetTransactor = FungibleAdapter< ... >;
pub type AssetTransactors = ( ... );

// 4. Origin converters
pub type XcmOriginToTransactDispatchOrigin = ( ... );

// 5. Barriers
pub type Barrier = TrailingSetTopicAsId< ... >;

// 6. Fee handling
pub type XcmRouter = WithUniqueTopic<( ... )>;

// 7. XcmConfig implementation
pub struct XcmConfig;
impl xcm_executor::Config for XcmConfig { ... }

// 8. pallet_xcm Config
impl pallet_xcm::Config for Runtime { ... }
```

---

## 5. Parameter Types

```rust
parameter_types! {
    // This chain's location relative to itself
    pub const RootLocation: Location = Location::here();

    // Relay chain location (parent)
    pub const RelayLocation: Location = Location::parent();

    // Network identity
    pub const RelayNetwork: Option<NetworkId> =
        Some(NetworkId::ByGenesis(WESTEND_GENESIS_HASH));

    // This chain's universal location (for global addressing)
    pub UniversalLocation: InteriorLocation =
        [GlobalConsensus(RelayNetwork::get().unwrap()), Parachain(ParachainInfo::parachain_id().into())].into();

    // Max assets that can be held in the XCM holding register
    pub const MaxAssetsIntoHolding: u32 = 64;

    // Max instructions in an XCM program
    pub const MaxInstructions: u32 = 100;

    // Treasury location on relay
    pub RelayTreasuryLocation: Location =
        (Parent, PalletInstance(18)).into(); // Treasury pallet index on relay

    // Fee asset for relay delivery
    pub FeeAssetId: AssetId = AssetId(RelayLocation::get());

    // Base delivery fee
    pub const BaseDeliveryFee: u128 = CENTS.saturating_mul(3);
}
```

---

## 6. Location-to-Account Conversion

Converts XCM `Location` to local `AccountId`:

```rust
pub type LocationToAccountId = (
    // Relay chain (parent) gets a preset sovereign account
    ParentIsPreset<AccountId>,

    // Sibling parachains get sovereign accounts based on para ID
    SiblingParachainConvertsVia<Sibling, AccountId>,

    // Direct AccountId32 mapping for same-network accounts
    AccountId32Aliases<RelayNetwork, AccountId>,

    // Hash-based conversion for complex locations
    HashedDescription<AccountId, DescribeFamily<DescribeAllTerminal>>,

    // External consensus locations (bridged chains)
    ExternalConsensusLocationsConverterFor<UniversalLocation, AccountId>,
);
```

### Converter Selection Guide

| Converter | When to Use |
|-----------|-------------|
| `ParentIsPreset` | Relay chain sovereign account |
| `SiblingParachainConvertsVia` | Sibling parachain sovereign accounts |
| `AccountId32Aliases` | Direct AccountId32 from same network |
| `AccountKey20Aliases` | Ethereum-style 20-byte accounts |
| `HashedDescription` | Complex locations (catch-all) |
| `GlobalConsensusConvertsFor` | External consensus roots (bridges) |
| `GlobalConsensusParachainConvertsFor` | External parachains (bridges) |

---

## 7. Asset Transactors

### Native currency (single fungible)

```rust
pub type FungibleTransactor = FungibleAdapter<
    Balances,                       // Currency implementation
    IsConcrete<RelayLocation>,      // Asset matcher - matches relay chain native token
    LocationToAccountId,            // Location converter
    AccountId,                      // AccountId type
    (),                             // Teleport checking account (() = no teleport tracking)
>;
```

### Multiple fungible assets

```rust
pub type FungiblesTransactor = FungiblesAdapter<
    Assets,                         // pallet-assets instance
    ConvertedConcreteId<            // Asset ID converter
        AssetIdForTrustBackedAssetsConvert<TrustBackedAssetsPalletLocation, Balance>,
        Balance,
        TruncatingDecimalConverterFor,
    >,
    LocationToAccountId,
    AccountId,
    LocalMint<                      // Teleport checking: track local mints
        parachains_common::impls::NonZeroIssuance<AccountId, Assets>,
    >,
    CheckingAccount,                // Account for tracking teleported assets
>;
```

### Composing multiple transactors

```rust
pub type AssetTransactors = (
    FungibleTransactor,         // Native token
    FungiblesTransactor,        // Trust-backed assets
    ForeignFungiblesTransactor, // Foreign assets
);
```

---

## 8. Origin Conversion

Maps XCM origins to runtime dispatch origins:

```rust
pub type XcmOriginToTransactDispatchOrigin = (
    // Sovereign account signed origin
    SovereignSignedViaLocation<LocationToAccountId, RuntimeOrigin>,

    // Relay chain as native relay origin
    RelayChainAsNative<RelayChainOrigin, RuntimeOrigin>,

    // Sibling parachain as native cumulus origin
    SiblingParachainAsNative<cumulus_pallet_xcm::Origin, RuntimeOrigin>,

    // Parent as superuser (root)
    ParentAsSuperuser<RuntimeOrigin>,

    // Direct AccountId32 signed origin
    SignedAccountId32AsNative<RelayNetwork, RuntimeOrigin>,

    // XCM origin passthrough
    XcmPassthrough<RuntimeOrigin>,
);
```

---

## 9. Barriers

Barriers determine which XCM messages are allowed to execute:

```rust
pub type Barrier = TrailingSetTopicAsId<
    DenyThenTry<
        DenyRecursively<DenyReserveTransferToRelayChain>,
        (
            // Allow local execution with weight credit
            TakeWeightCredit,

            // Allow known query responses
            AllowKnownQueryResponses<PolkadotXcm>,

            // Compute origin modifications before checking
            WithComputedOrigin<
                (
                    // Allow paid execution from anywhere
                    AllowTopLevelPaidExecutionFrom<Everything>,

                    // Allow unpaid execution from relay/system chains
                    AllowExplicitUnpaidExecutionFrom<(
                        ParentOrParentsPlurality,
                        Equals<RelayTreasuryLocation>,
                    )>,

                    // Allow version subscriptions
                    AllowSubscriptionsFrom<Everything>,

                    // Allow HRMP notifications from relay
                    AllowHrmpNotificationsFromRelayChain,
                ),
                UniversalLocation,
                ConstU32<8>,
            >,
        ),
    >,
>;
```

### Barrier Components

| Barrier | Purpose |
|---------|---------|
| `TakeWeightCredit` | Allow local XCM execution via extrinsics |
| `AllowTopLevelPaidExecutionFrom<T>` | Allow execution if paying fees |
| `AllowExplicitUnpaidExecutionFrom<T>` | Allow free execution from trusted origins |
| `AllowKnownQueryResponses<T>` | Allow responses to queries we sent |
| `AllowSubscriptionsFrom<T>` | Allow version subscription messages |
| `WithComputedOrigin<B, U, N>` | Re-evaluate barriers after origin modifications |
| `DenyThenTry<D, A>` | Deny first, then try allow filters |
| `DenyReserveTransferToRelayChain` | Block reserve transfers to relay |
| `TrailingSetTopicAsId<B>` | Extract topic from SetTopic instruction |

---

## 10. Trust Configuration

### Reserve assets (IsReserve)

```rust
// Trust relay chain as reserve for its native token
pub type TrustedReserves = (
    NativeAsset,  // Native asset from parent
    // Trust foreign assets from their registered reserve
    IsForeignConcreteAsset<FromSiblingParachain<parachain_info::Pallet<Runtime>>>,
);
```

### Teleported assets (IsTeleporter)

```rust
pub type TrustedTeleporters = (
    // Trust relay chain for teleporting its native token
    ConcreteAssetFromSystem<RelayLocation>,
);
```

---

## 11. Fee Handling

### Weight Trader

```rust
pub type Trader = (
    // Pay fees with native token
    UsingComponents<
        WeightToFee,           // Weight-to-fee conversion
        RelayLocation,         // Fee asset location
        AccountId,
        Balances,
        ToStakingPot<Runtime>, // Where fees go
    >,
    // Swap non-native assets for native to pay fees
    cumulus_primitives_utility::SwapFirstAssetTrader<
        RelayLocation,
        crate::AssetConversion,
        WeightToFee,
        crate::NativeAndAssets,
        (
            TrustBackedAssetsAsLocation<TrustBackedAssetsPalletLocation, Balance, xcm::latest::Location>,
            ForeignAssetsConvertedConcreteId,
        ),
        ResolveAssetTo<StakingPotAccountId<Runtime>, crate::NativeAndAssets>,
        AccountId,
    >,
);
```

### Fee Manager

```rust
type FeeManager = XcmFeeManagerFromComponents<
    WaivedLocations,                                    // Who doesn't pay fees
    SendXcmFeeToAccount<Self::AssetTransactor, TreasuryAccount>,  // Where fees go
>;
```

### Waived locations (no fees)

```rust
pub type WaivedLocations = (
    Equals<RootLocation>,           // This chain's root
    RelayOrOtherSystemParachains<   // System parachains
        AllSiblingSystemParachains,
        Runtime,
    >,
    Equals<RelayTreasuryLocation>,  // Relay treasury
);
```

---

## 12. XCM Router

```rust
pub type XcmRouter = WithUniqueTopic<(
    // Send to relay chain via UMP
    cumulus_primitives_utility::ParentAsUmp<
        ParachainSystem,
        PolkadotXcm,
        PriceForParentDelivery,
    >,
    // Send to sibling chains via XCMP
    XcmpQueue,
)>;
```

---

## 13. XcmExecutor Config

```rust
pub struct XcmConfig;
impl xcm_executor::Config for XcmConfig {
    type RuntimeCall = RuntimeCall;
    type XcmSender = XcmRouter;
    type XcmEventEmitter = PolkadotXcm;
    type AssetTransactor = AssetTransactors;
    type OriginConverter = XcmOriginToTransactDispatchOrigin;
    type IsReserve = TrustedReserves;
    type IsTeleporter = TrustedTeleporters;
    type UniversalLocation = UniversalLocation;
    type Barrier = Barrier;
    type Weigher = WeightInfoBounds<
        crate::weights::xcm::XcmWeight<RuntimeCall>,
        RuntimeCall,
        MaxInstructions,
    >;
    type Trader = Trader;
    type ResponseHandler = PolkadotXcm;
    type AssetTrap = PolkadotXcm;
    type AssetClaims = PolkadotXcm;
    type AssetLocker = ();
    type AssetExchanger = ();
    type SubscriptionService = PolkadotXcm;
    type PalletInstancesInfo = AllPalletsWithSystem;
    type MaxAssetsIntoHolding = MaxAssetsIntoHolding;
    type FeeManager = XcmFeeManagerFromComponents<
        WaivedLocations,
        SendXcmFeeToAccount<Self::AssetTransactor, TreasuryAccount>,
    >;
    type MessageExporter = ();
    type UniversalAliases = Nothing;
    type CallDispatcher = RuntimeCall;
    type SafeCallFilter = Everything;
    type Aliasers = Nothing;
    type TransactionalProcessor = FrameTransactionalProcessor;
    type HrmpNewChannelOpenRequestHandler = ();
    type HrmpChannelAcceptedHandler = ();
    type HrmpChannelClosingHandler = ();
    type XcmRecorder = PolkadotXcm;
}
```

---

## 14. pallet_xcm Config

```rust
impl pallet_xcm::Config for Runtime {
    type RuntimeEvent = RuntimeEvent;
    type Currency = Balances;
    type CurrencyMatcher = ();
    type SendXcmOrigin = EnsureXcmOrigin<RuntimeOrigin, LocalOriginToLocation>;
    type XcmRouter = XcmRouter;
    type ExecuteXcmOrigin = EnsureXcmOrigin<RuntimeOrigin, LocalOriginToLocation>;
    type XcmExecuteFilter = Everything;  // or Nothing to disable local execute
    type XcmExecutor = XcmExecutor<XcmConfig>;
    type XcmTeleportFilter = Everything;  // or specific asset filter
    type XcmReserveTransferFilter = Everything;
    type Weigher = WeightInfoBounds<
        crate::weights::xcm::XcmWeight<RuntimeCall>,
        RuntimeCall,
        MaxInstructions,
    >;
    type UniversalLocation = UniversalLocation;
    type RuntimeOrigin = RuntimeOrigin;
    type RuntimeCall = RuntimeCall;
    const VERSION_DISCOVERY_QUEUE_SIZE: u32 = 100;
    type AdvertisedXcmVersion = pallet_xcm::CurrentXcmVersion;
    type AdminOrigin = EnsureRoot<AccountId>;
    type TrustedLockers = ();
    type SovereignAccountOf = LocationToAccountId;
    type MaxLockers = ConstU32<8>;
    type MaxRemoteLockConsumers = ConstU32<0>;
    type RemoteLockConsumerIdentifier = ();
    type WeightInfo = crate::weights::pallet_xcm::WeightInfo<Runtime>;
    type AuthorizedAliasConsideration = ();
}
```

---

## 15. Custom Location Filters

```rust
pub struct ParentOrParentsPlurality;
impl Contains<Location> for ParentOrParentsPlurality {
    fn contains(location: &Location) -> bool {
        matches!(location.unpack(), (1, []) | (1, [Plurality { .. }]))
    }
}

pub struct FellowshipEntities;
impl Contains<Location> for FellowshipEntities {
    fn contains(location: &Location) -> bool {
        matches!(
            location.unpack(),
            (1, [Parachain(COLLECTIVES_ID), Plurality { id: BodyId::Technical, .. }])
        )
    }
}
```

---

## 16. Common XCM Programs

### Reserve transfer native token

```rust
let assets: Assets = (Parent, amount).into();
let dest: Location = (Parent, Parachain(sibling_id)).into();
let beneficiary: Location = AccountId32 { network: None, id: recipient.into() }.into();

// Via pallet_xcm extrinsic
PolkadotXcm::limited_reserve_transfer_assets(
    origin,
    Box::new(dest.into()),
    Box::new(beneficiary.into()),
    Box::new(assets.into()),
    0,  // fee_asset_item
    WeightLimit::Unlimited,
)?;
```

### Teleport native token

```rust
PolkadotXcm::limited_teleport_assets(
    origin,
    Box::new(dest.into()),
    Box::new(beneficiary.into()),
    Box::new(assets.into()),
    0,
    WeightLimit::Unlimited,
)?;
```

### Manual XCM construction

```rust
let xcm = Xcm(vec![
    WithdrawAsset(assets.clone()),
    BuyExecution { fees: fees_asset, weight_limit: WeightLimit::Unlimited },
    DepositAsset {
        assets: Wild(All),
        beneficiary: beneficiary_location,
    },
]);
```

---

## 17. Key Location Patterns

```rust
// Relay chain
Location::parent()                              // (1, [])

// Sibling parachain
Location::new(1, [Parachain(1000)])             // (1, [Parachain(1000)])

// Account on this chain
Location::new(0, [AccountId32 { network: None, id }])

// Account on relay chain
Location::new(1, [AccountId32 { network: None, id }])

// Account on sibling parachain
Location::new(1, [Parachain(1000), AccountId32 { network: None, id }])

// Pallet instance on this chain
Location::new(0, [PalletInstance(50)])

// Asset on this chain's pallet-assets instance
Location::new(0, [PalletInstance(50), GeneralIndex(asset_id)])

// External chain (via bridge)
Location::new(2, [GlobalConsensus(Rococo), Parachain(1000)])
```

---

## 18. Formatting (Mandatory Final Step)

After all code changes are complete, you MUST run these formatting checks:

```bash
cargo +nightly fmt --all -- --check
# If fails: cargo +nightly fmt --all

# For Cargo.toml changes:
taplo format --check --config .config/taplo.toml <path/to/changed/Cargo.toml>
```

---

## 19. Checklist

When configuring XCM:

**Location Setup**
- [ ] `UniversalLocation` correctly identifies this chain
- [ ] `RelayNetwork` set to correct genesis hash
- [ ] `RelayLocation` is `Location::parent()`

**Barriers**
- [ ] `TakeWeightCredit` included (for local execution)
- [ ] `AllowTopLevelPaidExecutionFrom` for general execution
- [ ] Unpaid execution restricted to trusted origins only
- [ ] `WithComputedOrigin` wraps barriers that need modified origins

**Asset Transactors**
- [ ] Native token transactor configured
- [ ] Asset matchers use correct locations
- [ ] Checking accounts set up for teleport tracking

**Trust**
- [ ] `IsReserve` correctly lists reserve pairs
- [ ] `IsTeleporter` correctly lists teleport pairs
- [ ] Reserve/teleport filters match actual trust relationships

**Fees**
- [ ] Trader configured for fee payment
- [ ] Fee manager routes fees correctly
- [ ] Waived locations include system chains

For detailed XCM builder component reference, see [XCM_BUILDER_REFERENCE.md](resources/XCM_BUILDER_REFERENCE.md).
