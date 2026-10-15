---
name: haedal-hasui
description: |
  Use when the user mentions staking SUI, withdrawing, claiming rewards, or operating haSUI on Haedal Protocol (a DeFi/LST protocol on SUI).
  Trigger phrases: "haedal","stake sui"，"stake hasui", "withdraw hasui", "withdraw sui"，"instant withdraw hasui", "instant withdraw sui", "claim hasui rewards","claim sui rewards".
  This skill calls https://skillsapi.haedal.xyz/api/v1/hasui/* via curl POST. On HTTP 200 returns txBytes (base64); on non‑200 returns msg.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(curl:*), Bash(jq:*)
model: opus
license: MIT
metadata:
  author: haedal
  version: '0.1.0'
---

# Haedal haSUI

**Haedal Protocol** is a DeFi ecosystem on the [SUI](https://sui.io) blockchain. **haSUI** is its liquid staking token (LST): stake native SUI to receive haSUI, earn staking rewards, and optionally choose validators. This skill calls the Haedal Skills API to perform stake, withdraw, instant withdraw, and claim operations via curl — no custom scripts required.

Call the haSUI HTTP APIs directly with curl.

**All numeric parameters are human‑readable amounts**: pass `amount` and other quantity fields as human‑readable values, without multiplying by decimals. For example, to stake 20 tokens, simply send `"amount":"20"`.

## Validator when staking

Only the **stake** method requires a `validator` (validator node `node_id`):

- Passing **`0x0`** means "use the default validator".
- If the user **does not provide a validator**: show a reference list of validators and let the user choose. The user can respond with **index 1–5** or the **validator name**. Map this to the corresponding `node_id` in the table and include it in the request.
- The reference list is defined in [`references/validators.md`](references/validators.md) (mapping between name and node_id, indexed 1–5).

Typical flow: the user says "stake hasui" without specifying a validator → present 5 reference validators (index + name) → the user replies with "1" or "Ankr", etc. → use the corresponding `node_id` to call stake.

## Claiming rewards and NFTObj

The **claim** endpoint requires **address** and **NFTObj** (the NFT object ID that holds the rewards). When the user says "claim hasui rewards":

1. **Ask the user** whether they want help finding the object id (if the user already knows the NFTObj, you can send it directly).
2. **If discovery is needed**: call **get_unstake_tickets_list** with the user `address`. On HTTP 200 the response body is:
   ```json
   {
     "list": [
       {
         "objectId": "0x...",
         "type": "0x...::staking::UnstakeTicket",
         "version": "...",
         "fields": {
           "claim_epoch": "646",
           "claim_timestamp_ms": "1737135496590",
           "id": { "id": "0x..." },
           "st_amount": "1000000000",
           "sui_amount": "1045887315",
           "unstake_timestamp_ms": "1737085604741"
         }
       }
     ]
   }
   ```
3. **Present the list to the user** in a readable format — show key fields such as `objectId`, `st_amount`, `sui_amount`, `claim_epoch`, `claim_timestamp_ms` for each entry.
4. **If there are multiple entries in the list**: let the user choose which one to claim (or take the first entry if only one exists) and use that entry's `objectId` as NFTObj.
5. **Then call claim**: `POST /api/v1/hasui/claim` with body `{"address":"0x...","NFTObj":"<objectId from previous step>"}`.

Flow summary: the user says "claim hasui rewards" → ask whether to discover the object id → if yes, call get_unstake_tickets_list(address) → present the list with key details → user selects one → take the chosen `objectId` as NFTObj → call claim(address, NFTObj).

## Base URL

`https://skillsapi.haedal.xyz/api/v1/hasui`

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

Pass `validator` as `0x0` to use the default validator, or use a node_id from [`references/validators.md`](references/validators.md) (user can choose by index 1–5 or by name).

```bash
# Use the default validator
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hasui/stake" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","amount":"100","validator":"0x0"}'

# Or specify an explicit validator node_id (for example Haedal Protocol)
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hasui/stake" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","amount":"100","validator":"0xc8a57a7ae3b814afc15a907d963a288454b2c0f1a323fd556cb2d56d85a94583"}'
```

**withdraw**

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hasui/withdraw" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","amount":"100"}'
```

**withdraw_instant**

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hasui/withdraw_instant" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","amount":"100"}'
```

**get_unstake_tickets_list** (query the UnstakeTicket list that can be claimed, used to obtain NFTObj)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hasui/get_unstake_tickets_list" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS"}'
```

When the response status is 200, the body contains `{"list":[{"objectId":"...","type":"...","version":"...","fields":{...}}, ...]}`. Present key fields (`objectId`, `st_amount`, `sui_amount`, `claim_epoch`, `claim_timestamp_ms`) to the user, then use the selected `list[].objectId` as the **NFTObj** for the claim call.

**claim** (requires NFTObj, which can be obtained from get_unstake_tickets_list → list[].objectId)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/hasui/claim" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS","NFTObj":"0xOBJECT_ID_FROM_LIST"}'
```

## Response

- **stake / withdraw / withdraw_instant / claim**: on HTTP 200, the body is `{"txBytes":"<base64>"}`; use `jq -r '.txBytes'` to extract it. On non‑200, use `jq -r '.msg'` to return the error reason to the user.
- **get_unstake_tickets_list**: on HTTP 200, the body is `{"list":[{"objectId","type","version","fields":{...}}, ...]}`; use `jq -r '.list'` to obtain the list. Each entry's `fields` contains `st_amount`, `sui_amount`, `claim_epoch`, `claim_timestamp_ms`, `unstake_timestamp_ms`. Take the desired entry's `objectId` as the NFTObj for claim.

## MoveAbort error codes

When a dry-run or build call fails with `MoveAbort(..., <code>)`, use the following mapping:

| Code | Constant Name | Description |
|------|---------------|-------------|
| 1 | `EDataNotMatchProgram` | Data does not match the program |
| 2 | `EStakedSuiRewardsNotMatched` | Staked SUI rewards do not match |
| 3 | `EInvalidStakeParas` | Invalid staking parameters |
| 4 | `EStakeNotEnoughSui` | Not enough SUI to stake |
| 5 | `EStakeNoStsuiMint` | No stSUI minted during staking |
| 6 | `EUnstakeNormalTicketLocking` | Normal unstake ticket is still in locking period |
| 7 | `EUnstakeNotEnoughSui` | Not enough SUI to fulfill unstake |
| 8 | `EUnstakeExceedMaxSuiAmount` | Unstake amount exceeds the max SUI amount |
| 9 | `EUnstakeInstantNoServiceFee` | Instant unstake requires a service fee (fee not set) |
| 10 | `(EUnstakeNotEnoughStakedSui)` | Commented out: not enough staked SUI for unstake |
| 11 | `EUnstakeNotZeroStSui` | Unstake stSUI amount must not be zero |
| 12 | `EStakePause` | Staking is paused |
| 13 | `EUnstakePause` | Unstaking is paused |
| 14 | `(EReservedForClaim)` | Commented out: reserved for claim |
| 15 | `(ENoMinStakingThreshhold)` | Commented out: no minimum staking threshold met |
| 16 | `EUnstakeNeedAmountIsNotZero` | Unstake `need_amount` must not be zero |
| 17 | `EClaimPause` | Claiming is paused |
| 18 | `EValidatorCountNotMatch` | Validator count does not match |
| 19 | `EValidatorNotFound` | Validator not found |
| 20 | `EInjectRewardsTooLow` | Injected rewards amount is too low |
