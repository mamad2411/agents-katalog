---
name: anchor
description: Anchor a file's SHA-256 hash on Polygon through ProofLedger, giving a dated proof anyone can check that this exact file existed by now, then save the proof bundle next to the file. Use when the user wants to timestamp, anchor or prove the existence of a file, document, build artifact or release.
---

# Anchor a file with ProofLedger

Use the `verify-proof` MCP tools. The file is hashed on this machine; only its SHA-256 hash is sent to ProofLedger, plus the file name unless the user asks to keep it private.

## Steps

1. Confirm which file or files to anchor. Each proof counts toward the user's monthly API allowance (the free plan includes 100 a month), so anchor what was asked for, not whole folders by default.
2. One file: call `create_proof` with the path. Pass `send_filename: false` if the user does not want the name sent. Several files (up to 100): call `create_proofs_batch`; file names double as the proofs' own ids, so re-running on unchanged files returns their existing proofs. If a file changed but kept its name, the batch returns its old proof, which will not match the new file: anchor that file with `create_proof` instead, or rename it.
3. If the tool answers that there is no API key, show the user the steps it returns (a free key, no card) and stop there. The key belongs in the `PROOFLEDGER_API_KEY` environment variable of the shell that starts the agent (Claude Code, Cursor); a new session picks it up. Never ask the user to paste the key into the chat.
4. Report the proof id, the certificate link and the verification link from the tool's answer.
5. The Polygon anchor usually lands within a minute. Check with `get_proof_status`. Once it reads anchored, call `save_proof_bundle` with the proof id and an `output_path` next to the file, named `<file name>.proof.json`. With the bundle saved, anyone can check the file later without ProofLedger, using the `verify` skill or `verify-proof verify <file> --proof <bundle>`.

## What to tell the user

- A proof shows that a file with this exact SHA-256 fingerprint existed by the anchor time, and that the file has not changed since.
- It does not show who made the file, and it is not a copyright registration.
- Do not describe the file as "verified by ProofLedger". The proof is a dated record on a public chain, not an endorsement.
