---
name: advertisement-dox
description: Return validated shareable capability advertisements.
---

# Advertisement DOX

## Allowed operations

- `ADVERTISEMENT_INDEX`
- `ADVERTISEMENT_DOCUMENTS`

## Procedure

1. Accept only the versioned request in `contracts/advertisement-protocol.md` from an authenticated trusted peer.
2. Read only this machine's `advertisement/AGENTS.md`, `advertisement/manifest.json`, and manifest-indexed capability JSON files.
3. For index requests, return `not_modified` when known revision and digest match; otherwise attach the manifest and advertisement contract.
4. For document requests, require the current revision and exact manifest IDs.
5. Reject absolute paths, `..`, globs, unknown IDs, private-tree requests, unsupported versions, and unauthenticated callers.
6. Return revision and digest with every response.
7. Never synthesize or promote a capability while serving a read request.

## Forbidden output

Secrets, usernames, home paths, local evidence content, raw observations, private skills, failures, chain-of-thought, and unindexed files.
