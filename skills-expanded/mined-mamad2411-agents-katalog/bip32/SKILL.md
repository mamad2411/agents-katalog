---
name: bip32
description: "Guide for Hierarchical Deterministic (HD) key derivation using the bip32 crate. Use this skill whenever the user wants to: derive child keys from a master seed; convert a bip32::XPrv to an Alloy PrivateKeySigner for EVM chains; derive Solana Ed25519 keypairs from a seed; understand hardened vs unhardened derivation paths; or implement BIP44 for multiple blockchains (Ethereum m/44'/60'/0'/0/n, Solana m/44'/501'/n'/0'). Make sure to use this skill when the user mentions HD wallets, BIP32, SLIP-10, key derivation, child keys, or managing multi-chain accounts from a single mnemonic."
---

# BIP32 HD Key Derivation (Multi-Chain)

The `bip32` crate natively supports Secp256k1 (Ethereum/EVM). For Ed25519 (Solana), the `solana-sdk` provides native SLIP-10 derivation functions. From a single master 64-byte seed, you can securely derive accounts for both ecosystems based on standard BIP-44 paths.

## Dependency Setup

```toml
[dependencies]
bip32 = { version = "0.5", features = ["secp256k1", "mnemonic"] }
alloy-signer-local = "2.0" # For EVM mapping
solana-sdk = "4.0"         # For Solana SLIP-10 mapping
solana-derivation-path = "3"  # For Solana derivation path parsing
rand_core = { version = "0.6", features = ["std"] }  # Required by bip32 for Mnemonic
```

## Core Patterns at a Glance

### 1. Master Seed Generation

Generate a master seed from a mnemonic, or parse an existing one from environment variables.

```rust
use bip32::Mnemonic;

// Generate new 24-word mnemonic
let mnemonic = Mnemonic::random(&mut rand_core::OsRng, Default::default());
let seed = mnemonic.to_seed(""); // 64-byte seed array
```

### 2. Deriving EVM Keys (Alloy)

EVM standardizes on the path `m/44'/60'/0'/0/n` (where the final index `n` is unhardened). The `bip32` crate handles this directly.

```rust
use bip32::{XPrv, DerivationPath};
use alloy_signer_local::PrivateKeySigner;
use std::str::FromStr;

pub fn derive_eth(seed: &[u8; 64], index: u32) -> PrivateKeySigner {
    // Parse the Ethereum derivation path
    let path: DerivationPath = format!("m/44'/60'/0'/0/{}", index).parse().unwrap();
    
    // Derive the child Extended Private Key (XPrv) from seed and path
    let child_xprv = XPrv::derive_from_path(seed, &path).unwrap();
    
    // Convert to Alloy PrivateKeySigner
    // child_xprv.private_key() provides the 32-byte secret scalar
    let private_key_bytes = child_xprv.private_key().to_bytes();
    PrivateKeySigner::from_slice(&private_key_bytes).unwrap()
}
```

### 3. Deriving Solana Keys (solana-sdk)

Solana uses Ed25519 with SLIP-10 hardened derivation. The standard path is `m/44'/501'/n'/0'`. **Do not use the `bip32` crate for this**—instead, use `solana_sdk` directly, passing the exact same 64-byte master seed.

```rust
use solana_sdk::signature::{Keypair, keypair_from_seed_and_derivation_path};

pub fn derive_sol(seed: &[u8; 64], index: u32) -> Keypair {
    // Note the single quotes indicating hardened derivation at every level
    let derivation_path = format!("m/44'/501'/{}'/0'", index);
    
    // Use from_absolute_path_str which handles the "m/" prefix
    use solana_derivation_path::DerivationPath as SolanaDerivationPath;
    let path = SolanaDerivationPath::from_absolute_path_str(&derivation_path).unwrap();
    solana_sdk::signer::keypair::keypair_from_seed_and_derivation_path(seed, Some(path)).unwrap()
}
```

### 4. Architecture Pattern for MQ Workers

In a distributed environment (like an Apalis MQ worker pool), you inject the 64-byte master seed as shared `Data<<TT>` and dynamically derive the key based on the database index `n` only when an active job executes. The database only stores `n`, never private keys.

```rust
use alloy_signer_local::PrivateKeySigner;
use solana_sdk::signature::Keypair;

#[derive(Clone)]
pub struct KdfConfig {
    pub seed: [u8; 64],
}

impl KdfConfig {
    pub fn get_evm_signer(&self, n: u32) -> PrivateKeySigner {
        derive_eth(&self.seed, n)
    }
    
    pub fn get_sol_signer(&self, n: u32) -> Keypair {
        derive_sol(&self.seed, n)
    }
}
```
