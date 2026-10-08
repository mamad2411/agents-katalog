# PoD Sablier Payroll Port

Port Sablier payroll user-story tests to PoD (`sablier-payroll-pod/`) with minimal story edits.

## When to use

- Implementing or debugging `sablier-payroll-pod/`
- Iterating on `PayrollCampaignFacade`, `PrivatePayrollCoti`, or `test/lib`
- After changes, run `npm run test:sablier-payroll-pod` (or PEI alias `npm run test:pod-payroll-port`)

## AVAX vs COTI

| Chain | Contracts | Responsibility |
|-------|-----------|----------------|
| Hardhat (AVAX surrogate) | `PayrollCampaignFacade`, `PayrollVault`, `PodClaimStore`, `PodErc20Mintable` | Sablier API (`itUint256` amounts), encrypted pool ledger, pToken payout, inbox outbound |
| simCOTI | `PrivatePayrollCoti`, `PodErc20CotiMother` | Encrypted roster verify, garbled pToken state |
| Privacy Portal | **Test infra only** | Corporate treasury seed / `mint` top-ups — **payroll contracts never call portal** |

## Sim MPC parity (iteration 7)

- Inject `simCOTI` precompile on **both** `cotiViem` and `sepoliaViem` (`mpc-test-utils` setup paths)
- Register users on both chains via `registerUserOnDualSim` (employer, facade, admin/cotiOwner)
- Facade `validateCiphertext` / `checkedSubWithOverflowBit` run on AVAX surrogate same as COTI

## Funding model (iteration 7)

1. **Treasury seed** — `seedCorporateTreasury(employer)` once per scenario (portal → employer pToken)
2. **Campaign fund** — employer encrypted `token.transfer(facade)` + balance sync + `ackPoolCredit(itUint256)` + facade ETH
3. **Story `mint`** — treasury top-up via portal to employer (not direct to facade)
4. **Claim payout** — encrypted `payoutTo(itUint256)` after COTI verify

`ackPoolCredit`: employer signs IT for funded amount; facade stores network-key ct via `offBoard(validateCiphertext(it))` in `_poolBalanceCt`.

## Private amounts (iteration 6–7)

- **API**: `claim(index, recipient, itUint256 amount, proof)` — stories still pass plaintext `amount`; `campaign-facade.ts` builds ITs
- **Registration**: `registerLeaf(index, recipient, amountCommitment)` — no `registeredAmount` on facade
- **Events**: `ClaimInstant` emits `amountCommitment`, not plaintext; `Clawback` has no amount field
- **Verify**: COTI `verifyAndCredit` compares encrypted claimed vs registered amount
- **Pool**: `_deductPool` on claim/clawback — on-chain S22 underfund (`InsufficientPoolBalance`)

## Merkle (PoD)

```
inner = keccak256(abi.encode(index, recipient, amountCommitment))
leaf  = keccak256(bytes.concat(inner))
amountCommitment = keccak256(abi.encode(ctUint256))
```

## Async claim path

1. **Fund** — treasury encrypted pToken transfer + `ackPoolCredit` IT + facade ETH + balance sync
2. **Prepare** — claimant `PodClaimStore.submitPayload` with verify IT + payout IT + `proofHandle`
3. **Claim tx** — facade `validateCiphertext` + `_deductPool` → merkle/recipient checks → vault `requestPayout` → `ClaimInstant` (commitment only)
4. **Mine payroll** — COTI `verifyAndCredit` → vault `payoutTo(itUint256)`
5. **Mine pToken** — `mineAfterPayoutTransfer`
6. **Sync** — `tokenAdapter.syncAccount` for decrypted story balances

### IT signing

- **COTI verify**: claimant `buildVerifyItAmount` → inbox `batchProcessRequests`
- **Claim calldata**: claimant `buildClaimItAmount` → facade `claim`/`claimTo` selector
- **Pool credit**: employer `buildAckPoolIt` → facade `ackPoolCredit` selector
- **Register**: `PrivatePayrollCoti` + `registerLeaf(...)` selector
- **pToken payout / clawback**: `buildPayoutItAmount` per facade; clawback also needs `buildClaimItAmount` with `clawback` selector for `_deductPool`

## Test lib map

| File | Role |
|------|------|
| `portal-setup.ts` | Deploy portal + pToken; `seedCorporateTreasury`, `portalDepositTo` |
| `pod-scenario.ts` | Treasury seed, `fundFacade` via pToken + `ackPoolCredit`, dual sim registration |
| `pod-token-adapter.ts` | Story ERC20 API; `mint` = treasury top-up; facade transfer → encrypted fund |
| `campaign-facade.ts` | Plaintext→IT wrapper, payload + double mine |
| `pod-backend.ts` | `buildVerifyItAmount`, `buildClaimItAmount`, `buildPayoutItAmount`, `buildAckPoolIt` |
| `async.ts` | `mineAfterPayoutClaim` + `mineAfterPayoutTransfer` |

## Do not

- Edit `sablier-payroll/` (frozen Phase 1)
- Route campaign funding through Privacy Portal (treasury → pToken transfer only)
- Snapshot raw `balanceOf` ct into `_poolBalanceCt` (user-key ct breaks `onBoard`)

## References

- Gap reports: `sablier-payroll-pod/docs/iterations/ITERATION_01_GAPS.md` … `ITERATION_07_GAPS.md`
