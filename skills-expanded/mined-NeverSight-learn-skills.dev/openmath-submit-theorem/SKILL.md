---
name: openmath-submit-theorem
description: Submits proofs or theorem solutions to the OpenMath platform. Use when the user wants to commit a proof hash or reveal a Lean/Rocq proof for a specific OpenMath theorem ID on the Shentu network.
version: v1.0.1
---

# OpenMath Submit Theorem

## Instructions

Two-stage submission on Shentu: (1) generate and broadcast proof hash via authz; (2) after hash lock, generate and broadcast proof detail. Default: authz + feegrant from `prover_address` (the user's OpenMath Wallet Address). Config: `openmath-env.json` is auto-discovered only from `./.openmath-skills/openmath-env.json` or `~/.openmath-skills/openmath-env.json`; override with `--config` or `OPENMATH_ENV_CONFIG`. Shentu chain/RPC settings come from `SHENTU_CHAIN_ID` and `SHENTU_NODE_URL` or built-in defaults, not from `openmath-env.json`. The skill always uses `--keyring-backend os` for local key lookups and generated submission commands. Direct signer fallback: `generate_submission.py --mode direct`.

### First-run gate

If `openmath-env.json` is missing from both `./.openmath-skills/openmath-env.json` and `~/.openmath-skills/openmath-env.json`, or if the config exists but is missing `prover_address`, `agent_address`, or `agent_key_name`, **do not proceed**. Follow [references/init-setup.md](references/init-setup.md), then validate:

```bash
python3 scripts/check_authz_setup.py --config .openmath-skills/openmath-env.json
```

Require `Status: ready` before any submission. Repeat on each new machine or workspace.

This gate is mandatory for scripts that advance the submission flow. `generate_submission.py` must not produce authz submission commands until `check_authz_setup.py` returns `Status: ready`. Read-only status polling via `query_submission_status.py` is exempt.

### Workflow checklist

- [ ] **Env**: `openmath-env.json` exists in `./.openmath-skills/` or `~/.openmath-skills/`, and `check_authz_setup.py` reports `Status: ready`.
- [ ] **Stage 1 (Commit)**: Run `generate_submission.py hash <theoremId> <proofPath> <proverKeyOrAddress> <proverAddr>` only after the first-run gate passes; run the emitted proofhash generation and `shentud tx authz exec proofhash.json ... --fee-granter <prover-address>`.
- [ ] **Wait**: 5–10 s, then `query_submission_status.py tx <txhash> --wait-seconds 6`. Confirm proof in `PROOF_STATUS_HASH_LOCK_PERIOD` and record `proof_id`.
- [ ] **Stage 2 (Reveal)**: Run `generate_submission.py detail <proofId> <proofPath> <proverKeyOrAddress>` only after the first-run gate passes; run the emitted proofdetail generation and `shentud tx authz exec proofdetail.json ... --fee-granter <prover-address>`. Do not wait for hash lock expiry.
- [ ] **Verify**: Wait 5–10 s, then `query_submission_status.py theorem <theoremId> --wait-seconds 6`. Confirm theorem reaches `THEOREM_STATUS_PASSED`.

### Scripts

| Script | Command | Use when |
|--------|---------|----------|
| Authz readiness | `python3 scripts/check_authz_setup.py --config .openmath-skills/openmath-env.json` | Before first submission and when changing env; validates CLI, keys, RPC, authz, feegrant. |
| Stage 1 commands | `python3 scripts/generate_submission.py hash <theoremId> <proofPath> <proverKeyOrAddress> <proverAddr>` | Generating proofhash.json and broadcast command for commit. In authz mode, refuses to continue until the first-run gate passes. |
| Stage 2 commands | `python3 scripts/generate_submission.py detail <proofId> <proofPath> <proverKeyOrAddress>` | Generating proofdetail.json and broadcast command for reveal (use proof_id from Stage 1). In authz mode, refuses to continue until the first-run gate passes. |
| Query tx | `python3 scripts/query_submission_status.py tx <txhash> [--wait-seconds 6]` | After broadcast to confirm inclusion. |
| Query theorem | `python3 scripts/query_submission_status.py theorem <theoremId> [--wait-seconds 6]` | Final status check. |
| Proof hash (debug) | `python3 scripts/calculate_proof_hash.py <theoremId> <proverAddress> <proofContentOrFile>` | Standalone hash check; normally used by generate_submission. |
| Install shentud | `python3 scripts/ensure_shentud.py` | When shentud is missing or broken. |

`submission_config.py` loads and validates only the identity/authz fields in `openmath-env.json` from `./.openmath-skills/` or `~/.openmath-skills/` (unless `--config` / `OPENMATH_ENV_CONFIG` is set). Chain/RPC settings come from `SHENTU_CHAIN_ID` and `SHENTU_NODE_URL`.

### Notes

- **Authz**: Default flow uses `shentud tx authz exec` with `--fee-granter <prover-address>`. For direct signer use `--mode direct` on `generate_submission.py`.
- **Block wait**: After each broadcast wait ~5–10 s before querying.

## References

Load when needed (one level from this file):

- **[references/init-setup.md](references/init-setup.md)** — Config-first env setup; handles both missing config files and existing configs missing the OpenMath Wallet Address or agent identities.
- **[references/openmath-env.example.json](references/openmath-env.example.json)** — Template for `openmath-env.json`.
- **[references/submission_guidelines.md](references/submission_guidelines.md)** — Hashing, authz execution, and status verification in detail.
- **[references/authz_setup.md](references/authz_setup.md)** — Manual authz grants and feegrant fallback.
- **[references/authz-submit-config.example.json](references/authz-submit-config.example.json)** — Legacy config shape reference; auto-discovery now uses `openmath-env.json` only.
