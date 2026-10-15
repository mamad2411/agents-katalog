---
name: haedal-vehaedal
description: |
  Use when the user mentions staking HAEDAL, locking, extending lock, claiming rewards, decay, or operating VeHaedal on Haedal Protocol (a DeFi ecosystem on SUI).
  Trigger phrases: "stake haedal", "lock haedal", "extend lock", "claim rewards from haedal", "unlock/redeem haedal", "add to stake", "start decay", "stop decay", "vehaedal".
  This skill calls https://skillsapi.haedal.xyz/api/v1/vehaedal/* via curl POST. add_stake and claim_rewards* need only signerAddress (+ amount/periods); add_to_existing_stake, extend_existing_lock, start_decay, stop_decay, unstake_and_claim require vehaedalObj — fetch via get_vehaedal_list(address), present the list with current_amount/locked_amount/is_decaying/lock_end_time to the user, then use their chosen objectId. All amounts are human-readable. On HTTP 200 returns txBytes (base64); on non‑200 returns msg.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(curl:*), Bash(jq:*)
model: opus
license: MIT
metadata:
  author: haedal
  version: '0.1.0'
---

# Haedal VeHaedal

**Haedal Protocol** is a DeFi ecosystem on the [SUI](https://sui.io) blockchain. **VeHaedal** is its vote-escrowed governance token: lock HAEDAL for veHaedal to earn rewards and voting power; lock duration and optional decay affect reward rates. This skill calls the Haedal Skills API for add stake, extend lock, claim rewards, decay control, and unstake — no custom scripts required.

Call the VeHaedal HTTP APIs directly with curl.

**All numeric parameters are human‑readable amounts**: pass `amount` and similar quantity fields as human‑readable values, without multiplying by decimals. For example, to stake 20 tokens, simply send `"amount":"20"`.

## Querying veHaedal objects (get_vehaedal_list)

Several methods (add_to_existing_stake, extend_existing_lock, start_decay, stop_decay, unstake_and_claim) require a **`vehaedalObj`** — the object ID of an existing veHaedal position. When the user triggers one of these methods:

1. **Ask the user** whether they already have the veHaedal object ID. If yes, use it directly.
2. **If discovery is needed**: call **get_vehaedal_list** with the user's `address`. On HTTP 200 the response body is:
   ```json
   {
     "list": [
       {
         "objectId": "0x...",
         "fields": {
           "current_amount": "10000000000",
           "initial_amount": "10000000000",
           "is_decaying": true,
           "lock_end_time": "1803708378450",
           "lock_start_time": "1772258778450",
           "locked_amount": "10000000000",
           "original_lock_weeks": "52",
           "owner": "0x...",
           "remaining_lock_weeks_when_stopped_decay": "52",
           "token_type": { "fields": { "name": "...::haedal::HAEDAL" }, "type": "0x1::type_name::TypeName" }
         }
       }
     ]
   }
   ```
3. **Present the list to the user** in a readable format — show key fields such as `objectId`, `current_amount`, `locked_amount`, `is_decaying`, `original_lock_weeks`, `lock_end_time` for each entry.
4. **Let the user choose** which veHaedal object to operate on (or take the first entry if only one exists). Use the selected `objectId` as the `vehaedalObj` parameter for the subsequent call.

Flow summary: user triggers a method that requires `vehaedalObj` → ask if they have the object ID → if not, call get_vehaedal_list(address) → present the list → user selects one → take that `objectId` as `vehaedalObj` → call the target method.

## Base URL

`https://skillsapi.haedal.xyz/api/v1/vehaedal`

## Request body

| Method                   | Required fields                                | Notes |
|--------------------------|------------------------------------------------|-------|
| add_stake                | signerAddress, amount, lockWeeks, isDecaying   | Creates a new veHaedal position |
| get_vehaedal_list        | address                                        | Query veHaedal objects owned by this address; returns `list` of objects |
| add_to_existing_stake    | signerAddress, **vehaedalObj**, amount          | Requires an existing veHaedal object ID |
| extend_existing_lock     | signerAddress, **vehaedalObj**, additionalWeeks | Requires an existing veHaedal object ID |
| start_decay              | signerAddress, **vehaedalObj**                  | Requires an existing veHaedal object ID |
| stop_decay               | signerAddress, **vehaedalObj**                  | Requires an existing veHaedal object ID |
| unstake_and_claim        | signerAddress, **vehaedalObj**                  | Requires an existing veHaedal object ID |
| claim_rewards_v2         | signerAddress, periods                         | No object field needed |
| claim_rewards_v2_epoch_1 | signerAddress                                  | No object field needed |

## curl examples

**add_stake**

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/vehaedal/add_stake" \
  -H "Content-Type: application/json" \
  -d '{"signerAddress":"0xYOUR_ADDRESS","amount":"20","lockWeeks":4,"isDecaying":false}'
```

**get_vehaedal_list** (query veHaedal objects owned by an address, used to obtain vehaedalObj)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/vehaedal/get_vehaedal_list" \
  -H "Content-Type: application/json" \
  -d '{"address":"0xYOUR_ADDRESS"}'
```

**add_to_existing_stake** (requires vehaedalObj, obtainable from get_vehaedal_list → list[].objectId)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/vehaedal/add_to_existing_stake" \
  -H "Content-Type: application/json" \
  -d '{"signerAddress":"0xYOUR_ADDRESS","vehaedalObj":"0xOBJECT_ID","amount":"10"}'
```

**extend_existing_lock** (requires vehaedalObj)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/vehaedal/extend_existing_lock" \
  -H "Content-Type: application/json" \
  -d '{"signerAddress":"0xYOUR_ADDRESS","vehaedalObj":"0xOBJECT_ID","additionalWeeks":2}'
```

**start_decay** (requires vehaedalObj)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/vehaedal/start_decay" \
  -H "Content-Type: application/json" \
  -d '{"signerAddress":"0xYOUR_ADDRESS","vehaedalObj":"0xOBJECT_ID"}'
```

**stop_decay** (requires vehaedalObj)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/vehaedal/stop_decay" \
  -H "Content-Type: application/json" \
  -d '{"signerAddress":"0xYOUR_ADDRESS","vehaedalObj":"0xOBJECT_ID"}'
```

**unstake_and_claim** (requires vehaedalObj)

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/vehaedal/unstake_and_claim" \
  -H "Content-Type: application/json" \
  -d '{"signerAddress":"0xYOUR_ADDRESS","vehaedalObj":"0xOBJECT_ID"}'
```

**claim_rewards_v2**

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/vehaedal/claim_rewards_v2" \
  -H "Content-Type: application/json" \
  -d '{"signerAddress":"0xYOUR_ADDRESS","periods":["1","2"]}'
```

**claim_rewards_v2_epoch_1**

```bash
curl -s -w "\n%{http_code}" -X POST "https://skillsapi.haedal.xyz/api/v1/vehaedal/claim_rewards_v2_epoch_1" \
  -H "Content-Type: application/json" \
  -d '{"signerAddress":"0xYOUR_ADDRESS"}'
```

## Response

- **add_stake / add_to_existing_stake / extend_existing_lock / start_decay / stop_decay / unstake_and_claim / claim_rewards_v2 / claim_rewards_v2_epoch_1**: on HTTP 200, the body is `{"txBytes":"<base64>"}`; use `jq -r '.txBytes'` to extract it. On non‑200, use `jq -r '.msg'` to extract the error reason and return it to the user.
- **get_vehaedal_list**: on HTTP 200, the body is `{"list":[{"objectId":"...","fields":{...}}, ...]}`. Use `jq -r '.list'` to obtain the list, then take the desired entry's `objectId` as the `vehaedalObj` for subsequent calls.

## MoveAbort error codes

When a dry-run or build call fails with `MoveAbort(..., <code>)`, use the following mapping:

| Code | Constant Name | Description |
|------|---------------|-------------|
| 0 | `N/A` | `start_decay`: token is already in decaying state. `stop_decay` / `unstake_and_claim`: token is not in decaying state. |
| 1 | `EInvalidLockDuration` | Invalid lock duration, must be between 1 and 52 weeks |
| 2 | `EInvalidOwner` | Caller is not the owner of the veHAEDAL token |
| 3 | `ENoTokensToUnstake` | No tokens available to unstake (`unstaked amount` is 0) |
| 4 | `EInvalidAmount` | Invalid amount, must be greater than 0 |
| 5 | `ELockNotExpired` | Lock period has not expired yet |
| 6 | `ELockShouldBeExpired` | Lock period should be expired |
| 7 | `EMinStakeAmount` | Stake amount is below the minimum required |
| 8 | `EDataNotMatchProgram` | Pool version does not match the current program version |
| 9 | `ELockExpired` | Lock period has already expired |
