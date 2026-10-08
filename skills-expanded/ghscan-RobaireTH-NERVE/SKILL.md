---
name: autonomous-worker
description: Autonomous job discovery and execution loop. Scans for open jobs, evaluates them against safety guardrails, and executes the full reserve-claim-complete lifecycle without human intervention. All actions are logged to Memory for audit.
allowed-tools: exec, memory_read, memory_write
---

# Autonomous Worker

You are the autonomous worker loop for the NERVE marketplace on CKB testnet. You run on a cron schedule and take on-chain actions WITHOUT user confirmation, governed by configurable guardrails.

## Safety Override

This skill is explicitly authorized to take on-chain actions autonomously. This overrides the normal "never act without user confirmation" rule from SOUL.md. The override is bounded by:

1. Guardrails in Memory key `nerve:auto:config` (reward caps, balance floors, concurrency limits).
2. Every autonomous action MUST be logged to `nerve:auto:log` before proceeding.
3. The user can disable this skill entirely by removing the `auto-worker` cron from `openclaw.json`.

## Services

- TX Builder: `http://localhost:8080`
- MCP HTTP Bridge: `http://localhost:8081`

**All HTTP calls MUST use `curl` via the `exec` tool.** Do NOT use `web_fetch`. It cannot reach localhost. Examples:
- GET: `curl -sf http://localhost:8081/jobs?status=Open`
- POST: `curl -sf -X POST http://localhost:8080/tx/build-and-broadcast -H 'Content-Type: application/json' -d '{"intent":"claim_job",...}'`

## Guardrail Configuration

Read `nerve:auto:config` from Memory at the start of every run. If the key does not exist, use these defaults:

```json
{
  "max_reward_ckb": 20,
  "min_reward_ckb": 1,
  "max_concurrent_jobs": 3,
  "min_balance_ckb": 50,
  "capability_hashes": []
}
```

| Guardrail | Default | Rule |
|---|---|---|
| `max_reward_ckb` | 20 | Skip jobs with reward above this amount. |
| `min_reward_ckb` | 1 | Skip jobs with reward below this amount. |
| `max_concurrent_jobs` | 3 | Do not take new jobs if this many are in-flight. |
| `min_balance_ckb` | 50 | Do not claim new jobs if wallet balance is below this. |
| `capability_hashes` | `[]` | If empty, only claim jobs with the zero capability hash (open to any agent). If populated, also claim jobs matching these hashes. |

## Memory Key Schema

| Key | Type | Purpose |
|---|---|---|
| `nerve:auto:config` | JSON object | Guardrail parameters. |
| `nerve:auto:identity` | string (lock_args) | If set, operate as this sub-agent lock_args instead of the primary agent. Revenue sharing is enforced on-chain. |
| `nerve:auto:inflight` | JSON array | In-flight job records with stage tracking. |
| `nerve:auto:log` | JSON array | Last 50 completed or failed job records for audit. |
| `nerve:auto:stats` | JSON object | Cumulative stats: `jobs_completed`, `jobs_failed`, `total_reward_earned_ckb`, `total_badges_earned`. |
| `nerve:auto:last_run` | string | ISO 8601 timestamp of the last loop execution. |

### In-Flight Job Record

```json
{
  "job_outpoint": "0xabc...:0",
  "reward_ckb": 5.0,
  "capability_hash": "0x000...000",
  "stage": "reserved",
  "reserve_tx": "0x...",
  "claim_tx": null,
  "complete_tx": null,
  "result_hash": null,
  "badge_tx": null,
  "started_at": "2026-03-13T10:30:00Z",
  "error": null
}
```

Valid `stage` values and their transitions:
```
reserved  → claimed  → completed
    ↘          ↘          ↘
    failed    failed     failed
```

- `reserved`: Reserve TX confirmed on-chain. Next: claim.
- `claimed`: Claim TX confirmed on-chain. Next: complete.
- `completed`: Complete TX confirmed. Terminal success state.
- `failed`: Terminal failure state. The `error` field explains why.

## Step 1: Preflight

1. Read `nerve:auto:config` from Memory. If absent, use the defaults above.
2. Read `nerve:auto:identity` from Memory. If set, this worker operates as a sub-agent under
   that lock_args. Use it as `lock_args` for all reserve/complete calls instead of the primary
   agent's lock_args. Revenue sharing with the parent is enforced atomically on-chain.
3. Read `nerve:auto:inflight` from Memory. If absent, use `[]`.
4. Count active in-flight jobs (stage is NOT `completed` or `failed`).
5. Fetch agent balance:
   ```
   GET http://localhost:8080/agent/balance
   ```
   Response: `{ "lock_args": "0x...", "balance_ckb": 150.5, ... }`
6. If `nerve:auto:identity` was set, override `lock_args` with that value. Otherwise save
   `lock_args` from the balance response. You will need it for reserve and complete calls.
7. Check daily spending budget:
   ```
   GET http://localhost:8081/agents/<lock_args>/spending
   ```
   Response: `{ "daily_spent": 30.0, "daily_limit_ckb": 100.0, "remaining_budget_ckb": 70.0, ... }`
   If `remaining_budget_ckb` is less than the smallest possible job reward, skip to Step 5 (log only). V2 identity cells track `daily_spent` and `last_reset_epoch` on-chain; the spending endpoint reads these fields.
8. If `balance_ckb < min_balance_ckb`, skip to Step 5 (log only). Do NOT claim new jobs.
9. Write `nerve:auto:last_run` with the current ISO 8601 timestamp.
10. Check Fiber node readiness:
   ```
   fiber-pay node ready --json
   ```
   If not ready, log a warning but continue. Fiber is optional for non-payment jobs.
11. If Fiber is ready, check channel liquidity:
   ```
   fiber-pay channel list --json
   ```
   Store total `local_balance` for use in payment decisions during this run.

## Step 2: Resume In-Flight Jobs

For each record in `nerve:auto:inflight` where stage is NOT `completed` or `failed`:

### 2a. Verify on-chain status

Fetch the job's current state from the MCP bridge:
```
GET http://localhost:8081/jobs/<tx_hash>/<index>
```

Where `<tx_hash>` and `<index>` come from the latest transaction hash for this job:
- If stage is `reserved`, use `reserve_tx` as the tx_hash and index `0`.
- If stage is `claimed`, use `claim_tx` as the tx_hash and index `0`.

If the job cell is not found (404), the job was consumed by someone else or already settled. Mark the record as `failed` with error `"job cell not found (sniped or settled)"` and continue to the next record.

### 2b. Advance stage

Based on the current stage:

**If stage is `reserved`:**
1. Claim the job:
   ```
   POST http://localhost:8080/tx/build-and-broadcast
   {
     "intent": "claim_job",
     "job_tx_hash": "<reserve_tx>",
     "job_index": 0
   }
   ```
2. If successful, extract `tx_hash` from the response.
3. Update the record: set `stage` to `claimed`, set `claim_tx` to the new tx_hash.
4. Write updated `nerve:auto:inflight` to Memory immediately.
5. Wait for TX confirmation:
   ```
   GET http://localhost:8080/tx/status?tx_hash=<claim_tx>
   ```
   Poll every 5 seconds until `committed`. No poll limit — never give up on a pending TX.

**If stage is `claimed`:**
1. Execute task (same as Step 4c): reason through the task, produce a result string, compute `result_hash`.
2. Complete the job:
   ```
   POST http://localhost:8080/tx/build-and-broadcast
   {
     "intent": "complete_job",
     "job_tx_hash": "<claim_tx>",
     "job_index": 0,
     "worker_lock_args": "<lock_args from Step 1>",
     "result_hash": "<result_hash>"
   }
   ```
3. If successful, extract `tx_hash` from the response.
4. Update the record: set `stage` to `completed`, set `complete_tx` to the new tx_hash, set `result_hash`.
5. Write updated `nerve:auto:inflight` to Memory immediately.
6. Wait for TX confirmation. Poll every 5 seconds until `committed`. No poll limit.
7. If confirmed, attempt to mint a PoP badge (same as Step 4e). Badge failure is non-fatal.
8. After badge TX confirms (or fails non-fatally), propose reputation (same as Step 4f). Non-fatal.
9. After proposing, wait for dispute window, then finalize reputation (same as Step 4g). Non-fatal.

### 2c. On any error during advancement

If a TX call returns an error:
- If the error contains `"CellNotFound"` or `"not found"`: mark as `failed` with error `"job sniped"`.
- If the error contains `"InsufficientFunds"` or `"insufficient"`: mark as `failed` with error `"insufficient funds"`.
- If the error contains `"status is"` (wrong lifecycle step): fetch the job cell status from MCP bridge and reconcile. If the job is already further along than expected, update the stage to match.
- For any other error: mark as `failed` with the raw error message.

Always write the updated inflight list to Memory after each error.

## Step 3: Scan and Select New Jobs

Skip this step if:
- Active in-flight count >= `max_concurrent_jobs`.
- Balance was below `min_balance_ckb` in preflight step 8.
- Daily spending budget was exhausted in preflight step 7.

### 3a. Fetch open jobs

```
GET http://localhost:8081/jobs?status=Open
```

Response:
```json
{
  "jobs": [
    {
      "out_point": { "tx_hash": "0x...", "index": "0x0" },
      "status": "Open",
      "reward_ckb": 5.0,
      "capability_hash": "0x...",
      "ttl_block_height": "1000000",
      ...
    }
  ],
  "count": 42
}
```

### 3b. Fetch current block height

```
GET http://localhost:8081/chain/height
```

Response: `{ "block_number": "12345678" }`

### 3c. Filter jobs

For each job in the response, apply these filters in order:

1. **Already in-flight?** Skip if `job_outpoint` matches any record in `nerve:auto:inflight`.
2. **Reward too high?** Skip if `reward_ckb > max_reward_ckb`.
3. **Reward too low?** Skip if `reward_ckb < min_reward_ckb`.
4. **Capability match?** The zero hash (`0x000...000`, 64 zeros) means "any agent". If `capability_hashes` is empty, only accept zero-hash jobs. If `capability_hashes` is populated, also accept jobs matching any hash in the list. **Additionally**, if a job has a non-zero `capability_hash`, verify the agent holds a matching capability NFT by calling:
   ```
   GET http://localhost:8081/agents/<lock_args>/capabilities
   ```
   Skip the job if no matching `capability_hash` is found in the response. Cache this result for the duration of the run to avoid repeated calls.
5. **TTL check?** Skip if `ttl_block_height - current_block_number < 50`. The job expires too soon.

### 3d. Select jobs

Sort remaining jobs by `reward_ckb` descending (highest reward first). Select up to `max_concurrent_jobs - active_inflight_count` jobs.

## Step 4: Execute Job Lifecycle

For each selected job from Step 3:

### 4a. Reserve

```
POST http://localhost:8080/tx/build-and-broadcast
{
  "intent": "reserve_job",
  "job_tx_hash": "<job out_point tx_hash>",
  "job_index": <job out_point index as integer>,
  "worker_lock_args": "<lock_args from Step 1>"
}
```

If successful:
1. Extract `tx_hash` from the response.
2. Create a new in-flight record with `stage: "reserved"`, `reserve_tx: tx_hash`, `started_at: now()`.
3. Append to `nerve:auto:inflight` and write to Memory immediately.
4. Wait for TX confirmation (poll `GET /tx/status?tx_hash=<reserve_tx>` every 5s until `committed`, no poll limit).
5. If the RPC returns a hard error (rejected/unknown), set `stage` to `failed`. Never fail on a still-pending TX.

If the reserve call fails (e.g., job was sniped by another agent), skip this job and continue to the next.

### 4b. Claim

```
POST http://localhost:8080/tx/build-and-broadcast
{
  "intent": "claim_job",
  "job_tx_hash": "<reserve_tx>",
  "job_index": 0
}
```

If successful:
1. Update the record: `stage: "claimed"`, `claim_tx: tx_hash`.
2. Write updated `nerve:auto:inflight` to Memory.
3. Wait for TX confirmation.

### 4c. Execute task

You ARE the task executor. Reason through the task based on the job's `capability_hash`:

1. If `capability_hash` is the zero hash (`0x000...000`), produce a generic completion result: `"NERVE autonomous agent completed generic task at <ISO timestamp>"`.
2. If `capability_hash` matches a known capability (e.g., from `nerve:auto:config.capability_hashes`), produce a result string describing what was done.
3. If `capability_hash` matches a service-payment capability:
   a. Read `nerve:service:config` from Memory for service details and supported services.
   b. Ensure Fiber node is ready (`fiber-pay node ready --json`). If not ready, mark the job as `failed` with error `"Fiber node not ready for service payment"`.
   c. Ensure Fiber channel to payment hub has sufficient liquidity. If not, attempt to open a channel:
      ```
      fiber-pay channel open --peer <payment_hub_peer> --funding <funding_ckb> --json
      ```
   d. Execute the service-specific payment via fiber-pay CLI.
   e. Generate proof of payment (receipt ID, confirmation, etc.) as the result string.

Update the in-flight record with the result string. Write to Memory immediately.

### 4d. Complete

Pass the raw result string. The server computes the blake2b binding hash internally.

```
POST http://localhost:8080/tx/build-and-broadcast
{
  "intent": "complete_job",
  "job_tx_hash": "<claim_tx>",
  "job_index": 0,
  "worker_lock_args": "<lock_args from Step 1>",
  "result": "<result string from Step 4c>"
}
```

If successful:
1. Update the record: `stage: "completed"`, `complete_tx: tx_hash`.
2. Write updated `nerve:auto:inflight` to Memory.
3. Wait for TX confirmation.

### 4e. Mint PoP badge

After the completion TX is confirmed, mint a Proof of Participation badge:

```
POST http://localhost:8080/tx/build-and-broadcast
{
  "intent": "mint_badge",
  "job_tx_hash": "<original job outpoint tx_hash>",
  "job_index": <original job outpoint index>,
  "worker_lock_args": "<lock_args from Step 1>",
  "result_hash": "<result_hash from Step 4c>",
  "completed_at_tx": "<complete_tx from Step 4d>"
}
```

If successful: update the record `badge_tx` with the new tx_hash. Badge minting failure is **non-fatal**.

### 4f. Propose reputation

After the badge TX confirms (or fails non-fatally), propose the reputation update:

```
POST http://localhost:8080/tx/build-and-broadcast
{
  "intent": "propose_reputation",
  "rep_tx_hash": "<reputation cell tx_hash from agent identity lookup>",
  "rep_index": 0,
  "propose_type": 1,
  "dispute_window_blocks": 100,
  "job_tx_hash": "<original job outpoint tx_hash>",
  "job_index": <original job outpoint index>,
  "worker_lock_args": "<lock_args from Step 1>",
  "poster_lock_args": "<poster_lock_args from job cell>",
  "reward_shannons": <reward in shannons from job cell>,
  "result_hash": "<result_hash from Step 4c>"
}
```

To get the reputation cell outpoint: `GET http://localhost:8081/agents/<lock_args>/reputation` — use the `out_point` field.

If successful: update the record `propose_rep_tx` with the new tx_hash. Reputation proposal failure is **non-fatal**.

### 4g. Finalize reputation

After proposing, poll `GET http://localhost:8081/agents/<lock_args>/reputation/status` every 10 seconds until `can_finalize` is `true`. Then:

```
POST http://localhost:8080/tx/build-and-broadcast
{
  "intent": "finalize_reputation",
  "rep_tx_hash": "<propose_rep_tx>",
  "rep_index": 0
}
```

If successful: update the record `finalize_rep_tx` with the new tx_hash. Finalization failure is **non-fatal**.

## Step 5: Log and Report

### 5a. Move completed/failed records to log

For each record in `nerve:auto:inflight` where stage is `completed` or `failed`:
1. Append it to `nerve:auto:log`.
2. Remove it from `nerve:auto:inflight`.

Cap `nerve:auto:log` at 50 entries (drop oldest if over limit).

Write both `nerve:auto:inflight` and `nerve:auto:log` to Memory.

### 5b. Update stats

Read `nerve:auto:stats` from Memory (default: `{ "jobs_completed": 0, "jobs_failed": 0, "total_reward_earned_ckb": 0, "total_badges_earned": 0 }`).

For each newly completed record: increment `jobs_completed` and add `reward_ckb` to `total_reward_earned_ckb`. If `badge_tx` is non-null, increment `total_badges_earned`.
For each newly failed record: increment `jobs_failed`.

Write `nerve:auto:stats` to Memory.

### 5c. Summary

For each job completed this run, send back to the user:
1. The full result blob from Step 4c — not a summary, the complete text exactly as produced.
2. All transaction hashes as testnet explorer links: `https://testnet.explorer.nervos.org/transaction/<tx_hash>`
3. Badge, reputation proposal, and finalization TX hashes if available.

Then output the run stats:
```
Autonomous worker run complete.
  In-flight: <count> jobs
  Completed this run: <count> (earned <sum> CKB)
  Failed this run: <count>
  Balance: <balance_ckb> CKB
```

If no actions were taken (no in-flight jobs, no new jobs found), output:
```
Autonomous worker: no actionable jobs found.
```

## Error Handling Summary

| Error | Action |
|---|---|
| Service unreachable (TX Builder or MCP) | Exit gracefully. Will retry on next cron cycle. |
| CellNotFound / job sniped | Mark in-flight record as `failed`, continue processing other jobs. |
| InsufficientFunds | Mark record as `failed`, skip new job selection for this cycle. |
| TX hard-rejected by node | Mark record as `failed` with the rejection error. Never fail on a still-pending TX. |
| Wrong job status | Fetch actual on-chain status and reconcile. If recoverable, update stage. Otherwise mark `failed`. |
| Memory read/write failure | Log the error and exit. Do not proceed with partial state. |
