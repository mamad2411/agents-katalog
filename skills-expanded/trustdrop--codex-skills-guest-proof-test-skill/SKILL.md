---
name: guest-proof-test
description: Use when working on TrustDrop guest zk proof testing, including local execute, SP1 Prove Network Groth16 fixture generation, local Solidity wrapper tests, and Arbitrum Sepolia SP1 gateway preflight verification for VSS or VDD.
---

# Guest Proof Test

Use the project script instead of hand-writing proof commands:

```sh
guest/scripts/zk-proof-test.sh <vss|vdd> <execute|prove|local-contract|preflight|all>
```

## Stages

- `execute`: builds and runs the local SP1 execute path. No Prove Network request.
- `prove`: builds the EVM proof binary with `CARGO_BUILD_JOBS=1`, then requests a Groth16 proof from SP1 Prove Network and writes the fixture.
- `local-contract`: runs Foundry wrapper tests with mocked SP1 gateway calldata; this verifies public value decoding and binding hash logic.
- `preflight`: uses `cast call` against the official Arbitrum Sepolia SP1 Groth16 gateway with the current fixture; this verifies the proof on the test chain without sending a transaction.
- `all`: runs `execute`, `prove`, `local-contract`, then `preflight` in order. Use only when the user explicitly wants the full chain because `prove` may consume PROVE credit on success.

## Commands

VSS:

```sh
guest/scripts/zk-proof-test.sh vss execute
guest/scripts/zk-proof-test.sh vss prove
guest/scripts/zk-proof-test.sh vss local-contract
guest/scripts/zk-proof-test.sh vss preflight
```

VDD walrus_rslhve:

```sh
guest/scripts/zk-proof-test.sh vdd execute
guest/scripts/zk-proof-test.sh vdd prove
guest/scripts/zk-proof-test.sh vdd local-contract
guest/scripts/zk-proof-test.sh vdd preflight
```

## Environment

- `TRUSTDROP_ENV` defaults to `drop-script/.env`.
- `SP1_PRIVATE_KEY` is read from `TRUSTDROP_ENV` and mapped to `NETWORK_PRIVATE_KEY` for the SP1 SDK.
- Do not print private keys or `.env` values.
- `PROTOC` defaults to `/tmp/protoc-25.3/bin/protoc`.
- `CARGO_BUILD_JOBS` defaults to `1`.
- `ARBITRUM_SEPOLIA_RPC` or `ARBITRUM_SEPOLIA_RPC_URL` can override the default RPC.
- `VDD_RSLHVE_DATA_SIZE` defaults to `65536`.

## Rules

- Do not use `cargo run` for proof requests. The script builds first, then runs `target/debug/...`.
- If `prove` fails, diagnose and stop; do not blindly retry.
- Prefer `preflight` for real SP1 verifier checks. Local Foundry tests are wrapper tests, not authoritative chain verifier checks.
- VSS and VDD should be advanced serially unless the user explicitly requests parallel work.
