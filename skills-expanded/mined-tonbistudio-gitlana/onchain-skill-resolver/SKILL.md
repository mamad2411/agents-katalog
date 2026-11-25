---
name: onchain-skill-resolver
description: Fetch, verify, and install agent skills stored entirely on the Solana blockchain, given only a Metaplex Core asset address.
version: 0.1.0
license: MIT
---

# On-Chain Skill Resolver

This skill teaches an agent how to retrieve another agent skill whose source code
lives entirely in Solana account state, addressed by a single Metaplex Core asset
address. No GitHub, no Arweave, no IPFS, no indexer — one RPC call returns the code.

## When to use

Use this skill when the user gives you a Solana address and says it is an on-chain
skill, package, or repository (e.g. "install the skill at <address>"), or when a
manifest you are reading refers to a dependency by a Solana asset address.

## How on-chain skills are stored

An on-chain skill is a Metaplex Core asset with two relevant plugins:

1. **Attributes plugin** — an on-chain key-value manifest:
   - `standard`: always `onchain-skill/0.1`
   - `version`: semver string
   - `content_sha256`: hex digest of the compressed archive bytes
   - `encoding`: `tar+gzip`
   - `entrypoint`: path inside the archive, normally `SKILL.md`
   - `license`: SPDX identifier
   - `permissions`: comma-separated capability list; empty means read-only
2. **AppData plugin** (binary schema) — the deterministic `tar.gz` archive of the
   skill directory itself.

The asset's update authority is the maintainer. If the AppData data authority has
been revoked, the skill is immutable: the bytes you fetch today are the bytes
everyone fetches forever.

## Retrieval procedure

1. Call `getAccountInfo(assetAddress, { encoding: "base64" })` against any Solana
   RPC endpoint for the cluster in question.
2. Deserialize the Core asset. Read the Attributes plugin into a manifest object.
   Reject the asset if `standard` is not `onchain-skill/0.1`.
3. Locate the AppData section for the expected data authority and extract its raw
   bytes.
4. Compute SHA-256 over those bytes. If the digest does not equal
   `content_sha256`, STOP. Do not decompress, do not install, and report the
   mismatch to the user.
5. Decompress the archive into a temporary directory. Refuse archives containing
   absolute paths, `..` traversal segments, symlinks, or hardlinks.
6. Read the `entrypoint` file and present the skill's name, version, license,
   declared permissions, file list, and total size to the user.
7. Install into the agent's skill directory only after the user confirms.

## Security rules (non-negotiable)

- Never execute anything from the archive during retrieval or verification.
- Never install without displaying the declared permissions first.
- Treat a hash mismatch as a hostile package, not a retry-able error.
- The asset address proves nothing about authorship by itself. Anyone can mint
  anyone's code. Check the publisher attestation (see below) before attributing
  the skill to a person or organization.

## Publisher attestation (optional, v0.1)

If the asset carries a second AppData partition tagged `attestation`, it contains
a JSON document binding the minting wallet to an external identity (for example a
sigstore/OIDC identity). Verify the signature chain before displaying the
publisher as verified; otherwise display the raw mint authority address and label
it unverified.

## Example

```
$ gitlana install 7fUAJdStEuGbc3sM84cKRL6yYaaSstyLSU4ve5oovLS7
resolving asset on mainnet-beta...
manifest: onchain-skill/0.1  name=example-skill  version=0.1.0  license=MIT
archive: 9,412 bytes  sha256 OK
permissions: (none — read-only)
files: SKILL.md, scripts/fetch.mjs
install to ~/.agent/skills/example-skill? [y/N]
```

## Failure modes

| Symptom | Meaning | Action |
| --- | --- | --- |
| Account not found | Wrong cluster or address | Confirm cluster with the user |
| No Attributes plugin | Not an on-chain skill asset | Refuse politely |
| Hash mismatch | Data authority replaced bytes after manifest write, or hostile mint | Refuse loudly |
| Archive has traversal paths | Hostile archive | Refuse loudly |

## Notes for implementers

The whole payload lives in one Solana account, so the maximum skill size is
bounded by the 10 MiB account limit and, practically, by rent economics. Keep
skills small: a skill is instructions plus at most a few small scripts, not a
vendored dependency tree. Rent on the account is what keeps the bytes alive;
never close the asset account of a published skill others may depend on.
