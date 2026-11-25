---
name: vulnhunter-solana
audience: specialist
description: Use when reviewing Solana program code for the account-model bug classes — unchecked account owner, absent signer, discriminator confusion, caller-controlled CPI seeds, PDA-derivation collision, SPL arithmetic overflow, close-and-reinitialize revival, and duplicate-account aliasing — the pattern census that stands in for absent scanners.
---

# vulnhunter-solana

Manual vulnerability pattern review for Solana Rust programs. Use this during
`solana-audit-flow`. There is **no Solana static-analysis step** — Slither has zero Solana
detectors (`slither --list-detectors` lists only EVM/Solidity checks, none for Solana), so any "slither Solana scan" is
a fabricated capability. Manual pattern matching is the primary coverage on Solana; the
automated Solana tooling is dynamic (anchor build warnings, litesvm/trident fuzzing), not
static taint analysis.

## High-priority vuln patterns

**1. Missing owner / program-id check (CRITICAL)**
Every account deserialized from instruction accounts must have its `owner` validated against the expected program ID. Pattern: `if account.owner != &expected_program_id { return Err(...) }`. Anchor's `#[account]` constraint handles this — but bare `AccountInfo` usage does not. Grep for `AccountInfo` without adjacent owner check.

**2. Missing signer check (HIGH)**
Privileged instructions must require `is_signer` on the authority account. Pattern: `if !authority.is_signer { return Err(ErrorCode::Unauthorized.into()) }`. Anchor's `Signer<'info>` type enforces this — but `AccountInfo` with manual check can omit it. Grep for privileged state mutations without `is_signer` guard.

**3. Account discriminator bypass (HIGH)**
Anchor programs use 8-byte discriminators at the start of account data to prevent type confusion. An attacker can pass a different account type that happens to deserialize without error if the discriminator is not validated. Verify `try_deserialize` is used (not `try_deserialize_unchecked`) for sensitive account types. Also check: can two different account types be interchanged via a crafted buffer?

**4. CPI signer / privilege escalation (CRITICAL)**
When making CPIs that require signing, the `invoke_signed` call must pass the correct `signer_seeds`. A bug where the caller-controlled account address matches a PDA derivation can allow privilege escalation. Pattern: verify `invoke_signed` uses program-controlled seeds, not caller-provided seeds, for authority PDAs.

**5. SPL token arithmetic overflow (HIGH in pre-checked code)**
SPL token math (amounts, decimals, fee calculation) must use `checked_*` arithmetic (`checked_add`, `checked_mul`, `checked_div`). Grep for arithmetic operators (`+`, `*`, `/`) directly on `u64` token amounts in pre-1.14 programs. Post-1.14, `overflow-checks = true` in `Cargo.toml` [profile.release] provides runtime protection; verify this is set.

**6. PDA derivation collision / seed manipulation (HIGH)**
Two different logical accounts can derive to the same PDA if seed inputs are insufficiently discriminated. Pattern: PDA seeds that include only user-controlled data (e.g., just a user public key) without a type discriminator can collide across account types. Verify seeds include a fixed type-specific prefix.

**7. Unchecked `AccountInfo.data` mutation (CRITICAL)**
Direct write to `account.data.borrow_mut()` bypasses Anchor's borsh serialization guarantees. Verify that data writes always go through `account.exit()` or Anchor's `Account::serialize` path.

**8. Rent-exempt check missing (LOW-MEDIUM)**
Accounts that fall below rent-exempt minimum can be garbage-collected by the runtime. Verify that account creation always includes the rent-exempt minimum lamport balance. Missing this is usually LOW severity unless it can be weaponized to force a denial-of-service.

## Order of ops

1. Grep the program source for `AccountInfo` usages. For each: verify owner check and signer check where required.
2. Grep for `invoke_signed` usages. For each: trace the `signer_seeds` derivation — are any seeds caller-controlled?
3. Grep for arithmetic operators on `u64`/`u128` token amounts. For each: confirm `checked_*` or `saturating_*` is used.
4. Review all `#[derive(Accounts)]` structs: for each `AccountInfo<'info>` field, check if an `Account<'info, T>` type with Anchor constraints would be more appropriate.
5. Review PDA seed construction: list all PDA seeds, confirm each includes a type prefix.

## When to pivot

- **Program is not Anchor:** apply the same patterns manually but via raw `solana_program` primitives. Owner checks are explicit `if account.owner != &program_id`. Signer checks are `if !account.is_signer`. There is no struct-level constraint validation.
- **Program is very large (> 5k LOC):** focus on CPI-adjacent code and privileged instruction handlers first; those have the highest attack surface density.

## Anti-patterns

- Do NOT report a "missing signer check" on accounts where the signer constraint is enforced at the Anchor struct level (`Signer<'info>`) and verified — only flag bare `AccountInfo` without manual check.
- Do NOT flag arithmetic as a finding if `overflow-checks = true` is confirmed in the release profile AND the code is post-1.14.
- Do NOT cite any Solana static-analysis detector (slither has none); if a step calls for one, it is stale — use manual review + dynamic fuzzing instead.

## Example

Grepping for missing owner checks in an Anchor program:

```bash
# Pattern 1: find bare AccountInfo usages
rg "AccountInfo<'info>" programs/ --type rust -n

# Pattern 3: find unchecked arithmetic on u64 token amounts
rg "[^a-z](\+|\*|/)[^=]" programs/ --type rust -n | grep -v "checked_"

# Pattern 4: find invoke_signed calls
rg "invoke_signed" programs/ --type rust -n
```

## Recording (chrono-vault)

The task packet's injected memory contract owns the exact call shape, sequence, and fields - see
`wirework-reflect`. Do not copy a `record(...)` example or add fields (including `source_task`) from
memory; the server binds them, and a baked example violates the run's authenticated schema. Memory is
best-effort telemetry and never gates the work. What is worth recording here is the task-specific
outcome: patterns checked, findings per pattern, AccountInfo/invoke_signed usage totals.

## Additional account / lifecycle / value classes
These extend the patterns above; the checklist duplicated the owner/signer/discriminator/CPI/PDA/arithmetic/rent classes already covered, so only the genuinely-additive classes are folded here.

- **Account substitution / missing relationship constraint (HIGH).** Beyond owner+discriminator, verify the *relationships* between accounts are enforced: `has_one`, `constraint = x.authority == user.key()`, "this vault belongs to this config", "the mint matches". Without them an attacker swaps in *their* vault / *their* token account while every individual account still passes its own owner check.
- **`close` / re-initialization revival (CRITICAL).** A closed account must have its lamports drained **and** its data zeroed / reassigned. Otherwise a closed account can be revived or re-initialized (reinit attack) into a privileged state.
- **Sysvar spoofing on native programs (MEDIUM–HIGH).** On non-Anchor programs, clock/rent and other sysvars passed as `AccountInfo` can be spoofed; verify the account key against the real sysvar id before trusting its data.
- **Duplicate mutable accounts / aliasing (HIGH).** The same account passed as two different `AccountInfo` params (aliasing) can defeat a balance/invariant check that assumes they are distinct. Reject or account for aliasing on mutable params.
- **Invariant preservation across EVERY path (CRITICAL for vaults/DEX/lending).** The 1:1 backing / collateralization / k-invariant must hold across fees, refunds, AND gas/rent reimbursement. Historical: gas-reimbursement drawn from the vault broke a bridge's 1:1 backing.
- **Swap direction / parity / slippage.** Can direction, price, or fee be manipulated (stale oracle, attacker-set rate, missing `min_out` slippage bound)?

Extra tooling beyond the flow's defaults: `cargo-geiger` (unsafe census), `cargo-fuzz` / trident (fuzz instruction handlers), `cargo-audit` (dependency CVEs). Related: [[known-advisory-backport-check]].
