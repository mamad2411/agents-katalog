---
name: haedal-hawal
description: |
  Use when the user mentions staking WAL, withdrawing hawal, claiming rewards, or operating haWAL on Haedal Protocol (a DeFi/LST protocol on SUI).
  Trigger phrases: “stake hawal”,"stake hawal", "withdraw hawal", "withdraw wal","instant withdraw hawal","instant withdraw wal","claim hawal rewards","claim wal rewards" .
  This skill calls https://skillsapi.haedal.xyz/api/v1/hawal/* via curl POST. On HTTP 200 returns txBytes (base64); on non‑200 returns msg.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(curl:*), Bash(jq:*)
model: opus
license: MIT
metadata:
  author: haedal
  version: '0.1.0'
---

# Haedal haWAL

**Haedal Protocol** is a DeFi ecosystem on the [SUI](https://sui.io) blockchain. **haWAL** is its liquid staking token (LST) for WAL: stake WAL to receive haWAL, earn staking rewards, and optionally choose validators. This skill calls the Haedal Skills API to perform stake, withdraw, instant withdraw, and claim operations via curl — no custom scripts required.

Call the haWAL HTTP APIs directly with curl.

**All numeric parameters are human‑readable amounts**: pass `amount` and similar quantity fields as human‑readable values, without multiplying by decimals. For example, to stake 20 tokens, simply send `"amount":"20"`.

## Validator when staking

Only the **stake** method requires a `validator` (validator node `node_id`):

- Passing **`0x0`** means "use the default validator".
- If the user **does not provide a validator**: show a reference list of validators and let the user choose. The user can respond with **index 1–10** or the **validator name**. Map this to the corresponding `node_id` from the table and include it in the request.
- The reference list is defined in [`references/validators.md`](references/validators.md) (mapping between name and node_id, indexed 1–10).

Typical flow: the user says "stake hawal" without specifying a validator → present 10 reference validators (index + name) → the user replies with "1" or "Nansen", etc. → use the corresponding `node_id` to call stake.

## Claiming rewards and NFTObj

The **claim** endpoint requires **address** and **NFTObj** (the NFT object ID that holds the rewards). When the user says "claim hawal rewards":

1. **Ask the user** whether they want help finding the object id (if the user already knows the NFTObj, you can send it directly).
2. **If discovery is needed**: call **get_unstake_tickets_list** with the user `address`. On HTTP 200 the response body is:
   ```json
   {
     "list": [
       {
         "objectId": "0x...",
         "type": "0x...::walstaking::UnstakeTicket",
         "version": "...",
         "fields": {
           "claim_epoch": 27,
           "claim_timestamp_ms": "1774364404744",
           "hawal_amount": "700000000000",
           "id": { "id": "0x..." },
           "unstake_timestamp_ms": "1772871784320",
           "wal_amount": "700635659164"
         }
       }
     ]
   }
   ```
3. **Present the list to the user** in a readable format — show key fields such as `objectId`, `hawal_amount`, `wal_amount`, `claim_epoch`, `claim_timestamp_ms` for each entry.
4. **If there are multiple entries in the list**: let the user choose which one to claim (or take the first entry if only one exists) and use that entry's `objectId` as NFTObj.
5. **Then call claim**: `POST /api/v1/hawal/claim` with body `{"address":"0x...","NFTObj":"<objectId from previous step>"}`.

Flow summary: the user says "claim hawal rewards" → ask whether to discover the object id → if yes, call get_unstake_tickets_list(address) → present the list with key details → user selects one → take the chosen `objectId` as NFTObj → call claim(address, NFTObj).

## Base URL

`https://skillsapi.haedal.xyz/api/v1/hawal`

## Request body

| Method                   | Required fields           | Notes |
|--------------------------|---------------------------|-------|
| stake                    | address, amount, validator | No object field |
| withdraw                 | address, amount           | No object field |
| withdraw_instant         | address, amount           | No object field |
| claim                    | address, **NFTObj**       | Requires NFT object ID, see the "Claiming rewards" flow above |
| get_unstake_tickets_list | address                   | Query the UnstakeTicket list for this address to obtain NFTObj |

## curl examples

**stake**

Pass `validator` as `0x0` to use the default validator, or use a node_id from [`references/validators.md`](references/validators.md) (user can choose by index 1–10 or by name).

```bash
# Use the default validator
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hawal/stake" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","amount":"100","validator":"0x0"}'

# Or specify an explicit validator node_id (for example Nansen)
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hawal/stake" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","amount":"100","validator":"0x7b3ba6de2ae58283f60d5b8dc04bb9e90e4796b3b2e0dea75569f491275242e7"}'
```

**withdraw**

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hawal/withdraw" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","amount":"100"}'
```

**withdraw_instant**

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hawal/withdraw_instant" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","amount":"100"}'
```

**get_unstake_tickets_list** (query the UnstakeTicket list that can be claimed, used to obtain NFTObj)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hawal/get_unstake_tickets_list" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS"}'
```

When the response status is 200, the body contains `{"list":[{"objectId":"...","type":"...","version":"...","fields":{...}}, ...]}`. Present key fields (`objectId`, `hawal_amount`, `wal_amount`, `claim_epoch`, `claim_timestamp_ms`) to the user, then use the selected `list[].objectId` as the **NFTObj** for the claim call.

**claim** (requires NFTObj, which can be obtained from get_unstake_tickets_list → list[].objectId)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hawal/claim" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","NFTObj":"0xOBJECT_ID_FROM_LIST"}'
```

## Response

- **stake / withdraw / withdraw_instant / claim**: on HTTP 200, the body is `{"txBytes":"<base64>"}`; use `jq -r '.txBytes'` to extract it. On non‑200, use `jq -r '.msg'` to return the error reason to the user.
- **get_unstake_tickets_list**: on HTTP 200, the body is `{"list":[{"objectId","type","version","fields":{...}}, ...]}`; use `jq -r '.list'` to obtain the list. Each entry's `fields` contains `hawal_amount`, `wal_amount`, `claim_epoch`, `claim_timestamp_ms`, `unstake_timestamp_ms`. Take the desired entry's `objectId` as the NFTObj for claim.

## MoveAbort error codes

When a dry-run or build call fails with `MoveAbort(..., <code>)`, use the following mapping:

| Code | Constant Name | Description |
|------|---------------|-------------|
| 1 | `EDataNotMatchProgram` | Data version does not match the current program version |
| 2 | `EStakeNotEnoughWal` | Stake amount is below the minimum staking threshold (1 WAL) |
| 3 | `EStakeNoHaWalMint` | Calculated haWAL mint amount is zero |
| 4 | `EUnstakeNormalTicketLocking` | Unstake ticket is still locked (claim epoch/time not reached) |
| 5 | `EUnstakeExceedMaxWalAmount` | Unstake WAL amount exceeds total available WAL |
| 6 | `EUnstakeNotZeroHawal` | Unstake input haWAL amount must not be zero |
| 7 | `EStakePause` | Staking is currently paused |
| 8 | `EUnstakePause` | Unstaking is currently paused |
| 9 | `EUnstakeNeedAmountIsNotZero` | Unstake process failed: remaining `need_amount` is not zero |
| 10 | `EClaimPause` | Claim is currently paused |
| 11 | `EValidatorCountNotMatch` | Provided validator count does not match existing validator count |
| 12 | `EValidatorNotFound` | Validator not found in the validator list |
| 13 | `EStakeActiveValidatorsNotFound` | No active validators found for staking |
| 14 | `EUnstakeOutOfRange` | Unstake timestamp is out of the valid epoch time range |
| 15 | `EStakeActiveValidatorsIsNull` | Active validators list is empty |
| 16 | `EUnstakeExceedMinWalAmount` | Unstake WAL amount is below the minimum staking threshold |
