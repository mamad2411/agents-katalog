---
name: cdr
description: Build with Story Confidential Data Rails (CDR) — threshold-encrypted vaults on Story L1 with on-chain access control. Use when code touches @piplabs/cdr-sdk, allocates CDR vaults, uploads encrypted files to IPFS through CDR, or gates content behind Story license tokens or IP assets.
---

# Story CDR

Story Confidential Data Rails (CDR) is a threshold-encrypted vault system on Story L1. Data is encrypted client-side under a DKG public key produced by the validator network; decryption requires (a) a threshold of validators to participate and (b) on-chain read conditions to pass.

Use this skill whenever code touches `@piplabs/cdr-sdk`.

## Architecture

`CDRClient` exposes three sub-clients:

- **`observer`** — read-only chain queries (DKG public key, threshold, fees, vault state). No wallet required.
- **`uploader`** — allocate vaults, encrypt locally, write ciphertext on chain. Wallet required.
- **`consumer`** — submit a read request, gather partial decryptions from validators, combine them locally. Wallet required (sends the read tx).

Two API layers:

- **High-level**: `uploader.uploadCDR` / `consumer.accessCDR` for inline data; `uploader.uploadFile` / `consumer.downloadFile` for files.
- **Low-level**: `allocate` → `encryptDataKey` → `write`, and `read` → `collectPartials` → `decryptDataKey`.

Inline payloads are capped at ~1024 bytes on Aeneid. Larger payloads must use the file path (`uploadFile`), which AES-encrypts the body, ships it to a `StorageProvider` (Helia/IPFS recommended), and stores only the AES key under CDR.

## Required setup

The SDK is published only as source as of v0.1.1 — there is no npm release. Build it from source:

```bash
git clone https://github.com/piplabs/cdr-sdk.git --branch 0.1.1 --depth 1
cd cdr-sdk && pnpm install && pnpm build
```

Consume it with **pnpm**. The SDK declares `workspace:*` deps on `@piplabs/cdr-crypto` and `@piplabs/cdr-contracts` — npm and yarn cannot resolve this protocol via `file:`. Either include the SDK packages in a `pnpm-workspace.yaml` and reference `@piplabs/cdr-sdk: workspace:*`, or wait for an npm release.

Peer dependencies: `viem` v2.21+ is required. For files: `helia`, `@helia/unixfs`, `multiformats` and **Node 22+**.

Always call `await initWasm()` once before any encrypt/decrypt operation. Without it, encrypt/decrypt throw opaque WASM errors. In React, do this in a top-level effect or provider.

Network is `"testnet"` (Aeneid). Default RPC `https://aeneid.storyrpc.io`. Wallet must be funded with testnet IP.

```ts
import { CDRClient, initWasm } from "@piplabs/cdr-sdk";
await initWasm();

const publicClient = createPublicClient({ transport: http(RPC_URL) });
const walletClient = createWalletClient({ account, transport: http(RPC_URL) });
const client = new CDRClient({ network: "testnet", publicClient, walletClient });
```

For read-only use, omit `walletClient` — `observer` methods still work.

## Access conditions

Every vault has `writeConditionAddr` + `readConditionAddr` (each is either a contract or an EOA) and matching `writeConditionData` / `readConditionData` (ABI-encoded, condition-specific).

### Deployed contracts on Aeneid

There are exactly two condition contracts deployed:

| Contract | Address | Type | conditionData encoding |
|---|---|---|---|
| `OwnerWriteCondition` | `0x4C9bFC96d7092b590D497A191826C3dA2277c34B` | Write only | `address owner` |
| `LicenseReadCondition` | `0xC0640AD4CF2CaA9914C8e5C44234359a9102f7a3` | Read only | `(address licenseToken, address ipId)` |

`LicenseToken` lives at `0xFe3838BFb30B34170F00030B52eA4893d8aAC6bC`.

There is no deployed `OwnerReadCondition` or `OpenCondition`. Using `OwnerWriteCondition` as a read condition will revert the read tx, and vice versa.

### EOA-as-condition

The CDR precompile accepts a plain EOA in `writeConditionAddr` or `readConditionAddr` and gates the operation to that exact address. No condition contract is needed; pass `"0x"` for the corresponding `conditionData`. This is the canonical way to do owner-only reads on Aeneid.

The SDK's `Uploader.allocate()` runs a preflight that staticcalls `checkWriteCondition` / `checkReadCondition` on the address. EOAs have no code, so this throws `InvalidConditionContractError`. Pass `skipConditionValidation: true` to bypass.

`uploadCDR()` and `uploadFile()` do **not** expose `skipConditionValidation`. When using an EOA condition, drop to the lower-level path: `allocate(...)` → `encryptDataKey(...)` → `write(...)`. For files, also call `encryptFile()` (re-exported from the SDK) and `storage.upload()` directly before allocating.

### Canonical patterns

**Owner-only read/write** (the SDK doesn't ship this out of the box on Aeneid; build it with EOA-as-read-condition):

```ts
import { encodeAbiParameters, toHex } from "viem";
import { uuidToLabel } from "@piplabs/cdr-sdk";

const OWNER_WRITE_CONDITION = "0x4C9bFC96d7092b590D497A191826C3dA2277c34B";
const owner = walletClient.account.address;

const { uuid } = await client.uploader.allocate({
  updatable: false,
  writeConditionAddr: OWNER_WRITE_CONDITION,
  writeConditionData: encodeAbiParameters([{ type: "address" }], [owner]),
  readConditionAddr: owner,         // EOA — gates reads to this exact wallet
  readConditionData: "0x",
  skipConditionValidation: true,    // EOA has no code; skip preflight
});

const globalPubKey = await client.observer.getGlobalPubKey();
const ciphertext = await client.uploader.encryptDataKey({
  dataKey: new TextEncoder().encode(secret),
  globalPubKey,
  label: uuidToLabel(uuid),
});

await client.uploader.write({
  uuid,
  accessAuxData: "0x",
  encryptedData: toHex(ciphertext.raw),
});

const { dataKey } = await client.consumer.accessCDR({
  uuid,
  accessAuxData: "0x",
  timeoutMs: 120_000,
});
```

**License-gated read** (uses both deployed contracts; works with `uploadCDR` directly):

```ts
const writeCondData = encodeAbiParameters([{ type: "address" }], [owner]);
const readCondData = encodeAbiParameters(
  [{ type: "address" }, { type: "address" }],
  ["0xFe3838BFb30B34170F00030B52eA4893d8aAC6bC", ipId],
);

const { uuid } = await client.uploader.uploadCDR({
  dataKey,
  globalPubKey,
  updatable: false,
  writeConditionAddr: "0x4C9bFC96d7092b590D497A191826C3dA2277c34B",
  writeConditionData: writeCondData,
  readConditionAddr:  "0xC0640AD4CF2CaA9914C8e5C44234359a9102f7a3",
  readConditionData: readCondData,
  accessAuxData: "0x",
});

// On read, accessAuxData carries the license token id(s) the reader holds.
const accessAuxData = encodeAbiParameters(
  [{ type: "uint256[]" }],
  [[BigInt(licenseTokenId)]],
);
const { dataKey } = await client.consumer.accessCDR({ uuid, accessAuxData, timeoutMs: 120_000 });
```

To mint a license token (Story core SDK): wrap IP→WIP via `storyClient.wipClient.deposit({ amount })`, approve `RoyaltyModule` (`0xD2f60c40fEbccf6311f8B47c4f2Ec6b040400086`) via `wipClient.approve`, then `storyClient.license.mintLicenseTokens({ licensorIpId, licenseTermsId, amount })`. Use `chainId: "aeneid"` when constructing `StoryClient`.

### Other condition encoders

The SDK exposes helpers in `conditions`: `ownerOnly`, `tokenGate`, `merkle`, `custom`, `open`. These produce `{ address, conditionData }` pairs but do not include addresses — pass the contract address yourself. They are convenience wrappers around `encodeAbiParameters`.

## Common failure modes

- **`initWasm` not called** → opaque "wasm not initialized" failures.
- **Inline data > 1024 bytes** → use `uploadFile`.
- **`InvalidConditionContractError` on an EOA condition** → pass `skipConditionValidation: true` and drop to the lower-level allocate path.
- **`read` reverts** → verifying the read condition contract implements `checkReadCondition` for the supplied data, or that the EOA gating matches the caller. `OwnerWriteCondition` is write-only; using it as `readConditionAddr` always reverts.
- **License read missing `accessAuxData`** → encode the token id(s) as `uint256[]`.
- **Helia on Node < 22** → upgrade Node, or use a different `StorageProvider` (Storacha, Synapse, gateway-backed IPFS).
- **Edge runtime (Vercel edge / Cloudflare workers)** → not supported. Use Node.js or browser.
- **Missing `walletClient`** → observer-only mode. Any `uploader` or `consumer` call throws.
- **`workspace:*` install error from npm/yarn** → switch the consuming project to pnpm.

Aeneid is testnet — not production-grade confidentiality. Don't put real secrets in.

## Reference

- Overview: https://docs.story.foundation/developers/cdr-sdk/overview
- Setup: https://docs.story.foundation/developers/cdr-sdk/setup
- Encrypt/decrypt: https://docs.story.foundation/developers/cdr-sdk/encrypt-and-decrypt
- IP asset / license vaults: https://docs.story.foundation/developers/cdr-sdk/ip-asset-vaults
- Advanced config: https://docs.story.foundation/developers/cdr-sdk/advanced-configuration
- SDK reference: https://docs.story.foundation/sdk-reference/cdr/overview
