---
name: verify
description: Check a file against a blockchain timestamp proof bundle on this machine, with no network call and no account, and explain in plain words what the proof establishes. Use when the user has a file and a proof JSON file and wants to know whether they match and when the file was anchored.
---

# Verify a file against its proof

Use the `verify-proof` MCP tools. Verification is pure computation on this machine: nothing is sent anywhere and no account is needed.

## Steps

1. Get the path of the file and of its proof JSON (often `<file name>.proof.json` next to the file). If the user only has a hash, use `verify_hash` with the hash and the proof JSON instead.
2. Call `verify_file` with `file_path` and `proof_path`.
3. If it verifies, report the chain, the transaction id and the anchor time, and give the block explorer link so the user can see the transaction themselves (for Polygon: `https://polygonscan.com/tx/<transaction id>`).
4. If it fails, say which check failed. A hash mismatch means this is not the anchored file: it was changed, even by one byte, or it is a different file.
5. If the user wants to know what the proof means, call `explain_proof` with the proof JSON and relay it in plain words.

## What a proof shows

- That a file with this exact SHA-256 fingerprint existed by the anchor time, and has not changed since.
- Not who made the file, not that its contents are true, and not a copyright registration.
