---
name: devnet-debug
description: Debug a Kurtosis devnet that is not producing blocks. Iterates through logs → code correlation → fix → rebuild → retest until the chain advances.
---

# Devnet Debug Skill

Debug a stalled or misbehaving eth2030 Kurtosis devnet. Covers two distinct failure modes: **chain not advancing** (Engine API bugs) and **transactions not confirming** (RPC format bugs). Both require different debugging paths.

## Prerequisites

```bash
kurtosis engine start
docker build -t eth2030:local pkg/
```

## Step 0 — Boot and observe

```bash
cd pkg/devnet/kurtosis
./scripts/cleanup.sh eth2030-devnet
./scripts/run-devnet.sh full-feature   # or single-client for faster iteration

# Check if the devnet had boot
kurtosis enclave inspect eth2030-devnet # if return `No enclave found with identifier 'eth2030-devnet'`, means no devnet
```

## Step 1 — Classify the failure

Got the basic info for enclave:

```bash
kurtosis enclave inspect eth2030-devnet
```

It will show status,  Files Artifacts and User Services, Note key services for eth devnet:

- cl-{N}-{cltpye}-geth: cl nodes,  cltpye will depend on `cl_type` in config for kurtosis devnet
- el-{N}-geth-{cltpye}: el nodes, which is run by eth2030
- dora: a explorer for cl
- spamoor: send test tx

Run these three checks to pick the right debug path:

```bash
# 1. Block number advancing?
cast bn -r http://$(kurtosis port print eth2030-devnet el-1-geth-lighthouse rpc)

# 2. Spamoor confirming txs? (look for "0 tx confirmed" or error lines)
kurtosis service logs eth2030-devnet spamoor 2>&1 | grep -E "error|0 tx confirmed|receipts" | tail -20

# 3. CL verified on every slot?
kurtosis service logs eth2030-devnet cl-1-lighthouse-geth 2>&1 | grep -E "verified|error|ERROR" | tail -20
```

| Symptom | Debug path |
|---------|-----------|
| Block number = 0 | → [Path A] Engine API bugs |
| Block number advancing, spamoor errors | → [Path B] RPC format bugs |
| Block number advancing, spamoor OK, assertoor failures | → [Path C] Consensus / finality |

if some log not show can use `-n 3000` to show 3000 line, or use `-f` to follow:

```bash
 kurtosis service logs eth2030-devnet el-2-geth-lighthouse -h
Show logs for a service inside an enclave

Usage:
  kurtosis service logs [flags] enclave [service...]

Flags:
  -a, --all                  Gets all logs.
  -x, --all-services         Returns service log streams for all logs in an enclave
  -f, --follow               Continues to follow the logs until stopped
  -h, --help                 help for logs
  -v, --invert-match         Inverts the filter condition specified by either 'match' or 'regex-match'. Log lines NOT containing match/regex-match will be returned
      --match string         Filter the log lines returning only those containing this match. Important: match and regex-match flags cannot be used at the same time. You should either use one or the other.
  -n, --num uint32           Get the last X log lines. (default 200)
      --regex-match string   Filter the log lines returning only those containing this regex expression match (re2 syntax regex may be used, more here: https://github.com/google/re2/wiki/Syntax). This filter will always work but will have degraded performance for tokens. Important: match and regex-match flags cannot be used at the same time. You should either use one or the other.
```

for ports, we can see the services info from ```kurtosis enclave inspect eth2030-devnet```:

```
5de758969582   el-1-geth-lighthouse                             engine-rpc: 8551/tcp -> 127.0.0.1:32771       RUNNING
                                                                metrics: 9001/tcp -> http://127.0.0.1:32772   
                                                                rpc: 8545/tcp -> 127.0.0.1:32769              
                                                                tcp-discovery: 30303/tcp -> 127.0.0.1:32773   
                                                                udp-discovery: 30303/udp                      
                                                                ws: 8546/tcp -> 127.0.0.1:32770  
```

we can use this cmd to got rpc endpoint:

```bash
kurtosis port print eth2030-devnet el-1-geth-lighthouse metrics
http://127.0.0.1:32772
```

for example, u can use ```cast -r```;

```bash
cast block -r $(kurtosis port print eth2030-devnet el-1-geth-lighthouse rpc)  finalized
```

---

## Path A — Engine API: chain not advancing

### A1. Collect Engine API errors

```bash
# CL: what error code did Lighthouse receive?
kurtosis service logs eth2030-devnet cl-1-lighthouse-geth 2>&1 \
  | grep -E "error=|ERROR|invalid|WARN" | tail -40

# EL: what did eth2030 log for engine_ calls?
kurtosis service logs eth2030-devnet el-1-geth-lighthouse 2>&1 \
  | grep -E "engine_|WARN|ERROR" | tail -40
```

CL error code quick-reference:

| Code | Meaning | Likely fix |
|------|---------|-----------|
| `-38005` / `unsupported fork` | Wrong `GetPayloadVN` for active fork | Check fork detection in `engine/server.go` |
| `-38003` / `invalid payload` | Structural payload error | Header fields, null arrays, withdrawals nil |
| `-32602` / `invalid params` | JSON field wrong type (null vs []) | Audit every array in `GetPayloadByID` |
| `-32001` / `payload not found` | Payload deleted before CL fetched it | Remove delete-on-read from `GetPayloadByID` |
| `block hash mismatch` | Header rebuilt differently from builder | Missing `ParentBeaconRoot`, `RequestsHash`, or BAL hash |

### A2. Engine API lifecycle checklist

Each slot: `FCU(attrs)` → build → `getPayload` → `newPayload` → `FCU(no attrs)`

**getPayload JSON null vs [] checklist** — Go nil slice → JSON `null` → CL rejects:

```go
// Every array field must be non-nil even when empty:
Transactions  = make([][]byte, 0, len(txs))  // never nil
Withdrawals   = []*Withdrawal{}               // nil-guard before loop
BlobsBundle.Commitments/Proofs/Blobs = make([]hexBytes, len(in))
ExecutionRequests = [][]byte{}
```

**Withdrawals nil after decode** (Shanghai+ required):
```go
// WRONG: loop over nil gives nil result; fails block validator
var withdrawals []*types.Withdrawal
for _, w := range payload.Withdrawals { ... }

// CORRECT: preserve non-nil for empty arrays
withdrawals = make([]*types.Withdrawal, 0, len(payload.Withdrawals))
for _, w := range payload.Withdrawals { ... }
```

**Block hash mismatch — field checklist**:

Every optional header field shifts the RLP hash. When reconstructing from a
payload, always populate all fields the builder set:

| Field | Fork | Source |
|-------|------|--------|
| `UncleHash` | always | `types.EmptyUncleHash` |
| `Difficulty` | always | `new(big.Int)` (0 post-merge) |
| `TxHash` | always | `core.DeriveTxsRoot(txs)` |
| `WithdrawalsHash` | Shanghai+ | `core.DeriveWithdrawalsRoot(ws)` |
| `BlobGasUsed` | Cancun+ | `payload.BlobGasUsed` |
| `ExcessBlobGas` | Cancun+ | `payload.ExcessBlobGas` |
| `ParentBeaconRoot` | Cancun+ | separate `parentBeaconBlockRoot` param (NOT in payload) |
| `RequestsHash` | Prague+ | `types.ComputeRequestsHash(reqs)` from `executionRequests` param |
| `BlockAccessListHash` | Amsterdam+ | from BAL in payload extension |

**GetPayload fork gate bugs** — removing fork checks often fixes phantom rejections:
```go
// WRONG: IsPrague check on an Amsterdam payload
func (s *Server) GetPayloadV4(...) {
    if !s.chain.Config().IsPrague(blockTimestamp) { return nil, ErrUnsupportedFork }
}
// CORRECT: let the payload ID resolve to the right version; no extra fork gate needed
```

**Payload consumed on first read** — always fatal for fork-choice:
```go
// WRONG: CL calls getPayload twice (once to publish, once for newPayload)
p := s.payloads[id]
delete(s.payloads, id)  // BUG: second call returns nil → -32001

// CORRECT: remove the delete; expire via TTL or FCU
```

---

## Path B — RPC: chain advancing but spamoor fails

### B1. Understand spamoor's decode flow

Spamoor's "block X has 0 receipts, expected N" is almost never a receipt
storage problem. The real cause is almost always **transaction JSON decode
failure** upstream.

Spamoor flow (in `spamoor/txpool.go`):
1. `eth_getBlockByNumber(..., true)` → raw JSON block
2. For each tx: `json.Unmarshal(rawTx, &types.Transaction)` — failure → tx → `txSkipMap`
3. `eth_getBlockReceipts` → filter out receipts at `txSkipMap` indices
4. `len(filtered) != txCount` → "block X has 0 receipts, expected N"

**How to confirm**: call RPC directly and inspect tx fields:
```bash
curl -s -X POST http://$(kurtosis port print eth2030-devnet el-1-geth-lighthouse rpc) \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest",true],"id":1}' \
  | jq '.result.transactions[0] | keys'
# Must include: chainId, maxFeePerGas, maxPriorityFeePerGas for type-2 txs
# Missing any of these = "missing required field 'chainId' in transaction"
```

### B2. RPCTransaction required fields

go-ethereum `Transaction.UnmarshalJSON` has **strict required field checks** per tx type.
Missing any required field silently fails in spamoor's decode.

| Tx type | Required fields |
|---------|----------------|
| `0x0` legacy | `nonce`, `gasPrice`, `gas`, `value`, `input`, `v`, `r`, `s` |
| `0x1` access list | all type-0 + **`chainId`** |
| `0x2` EIP-1559 | `nonce`, `gas`, `value`, `input`, `v`, `r`, `s` + **`chainId`**, **`maxFeePerGas`**, **`maxPriorityFeePerGas`** |
| `0x3` blob | all type-2 + **`maxFeePerBlobGas`**, **`blobVersionedHashes`** |
| `0x4` set-code | all type-2 + **`authorizationList`** |

Complete `RPCTransaction` struct must include:

```go
type RPCTransaction struct {
    // always present
    Hash, Nonce, From, Value, Gas, GasPrice, Input, Type string
    V, R, S  string  // must use tx.RawSignatureValues(), NOT hardcoded "0x0"
    BlockHash, BlockNumber, TransactionIndex *string
    To *string
    // EIP-2930+ (types 1,2,3,4)
    ChainID    *string          `json:"chainId,omitempty"`
    AccessList []RPCAccessTuple `json:"accessList,omitempty"`
    // EIP-1559+ (types 2,3,4)
    MaxFeePerGas         *string `json:"maxFeePerGas,omitempty"`
    MaxPriorityFeePerGas *string `json:"maxPriorityFeePerGas,omitempty"`
    // EIP-4844 (type 3)
    MaxFeePerBlobGas    *string  `json:"maxFeePerBlobGas,omitempty"`
    BlobVersionedHashes []string `json:"blobVersionedHashes,omitempty"`
    // EIP-7702 (type 4)
    AuthorizationList []RPCAuthorization `json:"authorizationList,omitempty"`
}
```

### B3. Other RPC format bugs checklist

**Block responses** — missing fields break ethclient block parsing:
- Always: `sha3Uncles`, `nonce`, `mixHash`, `totalDifficulty`, `size`
- EIP-1559+: `baseFeePerGas`
- Shanghai+: `withdrawals` (emit `[]` not omitted), `withdrawalsRoot`
- Cancun+: `blobGasUsed`, `excessBlobGas`
- Cancun+: `parentBeaconBlockRoot`
- Prague+: `requestsHash`

**eth_getBlockReceipts** — must handle all parameter forms:
```
"latest" / "0x1a"             → string block tag / number
"0x<66 hex chars>"            → block hash (66-char string)
{"blockHash": "0x..."}        → object form (go-ethereum ethclient default)
{"blockNumber": "0x..."}      → object form with number
```

**eth_sendRawTransaction** — must RLP-decode, not JSON-unmarshal:
```go
// WRONG: json.Unmarshal on a hex string
// CORRECT: bytes, _ := hex.DecodeString(rawHex[2:]); tx.DecodeRLP(bytes)
```

**Rate limiting** — `0` must mean unlimited:
```go
if limit > 0 && count > limit { return rateLimitedError }
```

**JSON-RPC 2.0 null result** — `result` field must always be present:
```go
// WRONG: nil result + omitempty → "result" field absent → spec violation
// CORRECT:
func successResponse(id json.RawMessage, result interface{}) *Response {
    if result == nil { result = json.RawMessage("null") }
    ...
}
```

### B4. Container networking bugs

**Bind addresses** — all servers must bind `0.0.0.0` in Docker, not `127.0.0.1`.
Default `127.0.0.1` silently works locally but breaks container-to-container
calls (ethereum-package, spamoor, assertoor, dora all connect from separate containers).

**`admin_nodeInfo` must be reachable on port 8545** — ethereum-package polls
this for up to 30 minutes waiting for a non-empty enode URL. If `admin_` is
only wired on a separate admin port, devnet startup stalls silently.

```bash
# Verify admin_ is routed on the standard RPC port
curl -s -X POST http://$(kurtosis port print eth2030-devnet el-1-geth-lighthouse rpc) \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"admin_nodeInfo","params":[],"id":1}' \
  | jq '.result.enode'
# Must be non-empty "enode://..." string
```

---

## Path C — Consensus / finality

These are normal in short devnet runs; only investigate if persisting after 5+ min:

| Symptom | Cause | Action |
|---------|-------|--------|
| `finalized_epoch: 0` | Need ≥ 3 epochs; at 2s slots = ~6 min | Wait |
| `Low peer count: 1` | 2-node devnet, each sees 1 peer | Normal |
| `check_consensus_reorgs: 0 epochs` | Not enough epochs elapsed | Wait |
| `NoPeersSubscribedToTopic` | Attestation subnet mesh forming | Normal |
| `404 on /eth/v1/beacon/headers/0x...` | Dora querying block not yet cached | Normal |

---

## Core state bugs (harder to spot)

These manifest as wrong behavior after the chain is running:

**`tx.Sender()` always nil** — sender cache is never populated unless you
explicitly recover the ECDSA signature after block insertion. Symptom:
`eth_getTransactionByHash` returns `from: "0x0000...0000"`.

**Typed-nil interface panic** — assigning a typed nil pointer to an interface
gives a non-nil interface value, but calling a method on it panics:
```go
var tracker *BALTracker = nil
var iface BALTrackerInterface = tracker  // iface != nil, but methods panic!
// CORRECT: if tracker != nil { iface = tracker }
```

**Txpool nonces not advancing** — after inserting a block, call
`txpool.SetHead(block)` so the pool evicts confirmed txs and advances pending
nonces. Without this, spamoor's second tx gets "nonce too low".

**Receipt / txlookup index miss** — in-memory index may miss receipts after
restart. Always implement rawdb fallback:
```go
func (b *Backend) GetReceipts(hash Hash) []*Receipt {
    if r := b.receiptCache[hash]; r != nil { return r }
    return rawdb.ReadReceipts(b.db, hash)
}
```

---

## Targeted logging (add temporarily, remove before merge)

```go
// Engine API: hash mismatch
slog.Warn("newPayload: hash mismatch",
    "computed", block.Hash(), "payload", payload.BlockHash,
    "parentBeaconRoot", parentBeaconRoot, "requestsHash", requestsHash)

// RPC: receipt lookup tracing
slog.Info("getBlockReceipts",
    "raw", string(raw), "blockHash", blockHash,
    "headerFound", header != nil, "receiptCount", len(receipts))
```

---

## Full debug cycle

```bash
# 1. Start devnet
cd pkg/devnet/kurtosis
./scripts/cleanup.sh eth2030-devnet && ./scripts/run-devnet.sh full-feature

# 2. Check primary signals (30s after start)
sleep 30
cast bn -r http://$(kurtosis port print eth2030-devnet el-1-geth-lighthouse rpc)
kurtosis service logs eth2030-devnet spamoor 2>&1 | grep -E "error|confirmed" | tail -10
kurtosis service logs eth2030-devnet cl-1-lighthouse-geth 2>&1 | grep "verified\|ERROR" | tail -10

# 3. Path A: block = 0
kurtosis service logs eth2030-devnet el-1-geth-lighthouse 2>&1 | grep -E "engine_|WARN|ERROR" | tail -40

# 4. Path B: block > 0 but spamoor errors
kurtosis service logs eth2030-devnet spamoor 2>&1 | grep -E "error|receipt" | tail -20
curl -s -X POST http://$(kurtosis port print eth2030-devnet el-1-geth-lighthouse rpc) \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["latest",true],"id":1}' \
  | jq '.result.transactions[0] | keys'

# 5. Fix → compile → unit test → commit
cd pkg && go build ./... && go test ./rpc/... ./engine/... ./node/...

# 6. Rebuild + retest
docker build -t eth2030:local . -q
./scripts/cleanup.sh eth2030-devnet && ./scripts/run-devnet.sh full-feature
sleep 120
kurtosis service logs eth2030-devnet spamoor 2>&1 | grep -E "error|failed"
# clean = no output
```

## Known-good state checklist (2-minute run)

- [ ] `cast bn` > 40 (30+ blocks in 2 min at 2s slots)
- [ ] spamoor: `N total tx, N tx confirmed` every block, zero errors
- [ ] EL logs: zero `error` / `panic` lines
- [ ] CL logs: `(verified)` every slot, only `Low peer count` warnings
- [ ] assertoor: `check_clients_are_healthy` and `check_execution_sync_status` passing
- [ ] `finalized_epoch: 0` is OK under 5 minutes

---

## Metrics: reading EL node memory and health

### Discover ports

```bash
ENCLAVE=eth2030-devnet

# JSON-RPC (eth_blockNumber, eth_getBlock*, etc.)
EL_RPC=$(kurtosis port print $ENCLAVE el-1-geth-lighthouse rpc)

# Prometheus metrics (ETH2030_* counters + docker RSS)
EL_METRICS=$(kurtosis port print $ENCLAVE el-1-geth-lighthouse metrics)
# Output format: "http://127.0.0.1:<port>"

echo "RPC:     http://$EL_RPC"
echo "Metrics: $EL_METRICS/metrics"
```

### Available ETH2030 metrics

```bash
# Dump all ETH2030_ metrics
curl -s "$EL_METRICS/metrics" | grep "^ETH2030_"
```

| Metric name | Type | Meaning |
|-------------|------|---------|
| `ETH2030_chain_blocks_inserted` | counter | total blocks processed by EL |
| `ETH2030_chain_height` | gauge | current canonical head number |
| `ETH2030_chain_reorgs` | counter | number of chain reorgs detected |
| `ETH2030_engine_new_payload` | counter | newPayload calls handled |
| `ETH2030_engine_forkchoice_updated` | counter | FCU calls handled |
| `ETH2030_evm_executions` | counter | transactions executed through EVM |
| `ETH2030_evm_gas_used` | counter | total gas consumed |
| `ETH2030_rpc_requests` | counter | JSON-RPC requests received |
| `ETH2030_rpc_errors` | counter | JSON-RPC requests that returned error |
| `ETH2030_txpool_added` | counter | transactions added to pool |
| `ETH2030_txpool_dropped` | counter | transactions evicted from pool |
| `ETH2030_txpool_pending` | gauge | current pending tx count |
| `ETH2030_txpool_queued` | gauge | current queued tx count |

### Memory cost: two complementary views

**1 — Docker container RSS** (OS perspective, includes all mapped memory):

```bash
# Instantaneous RSS for both EL nodes
docker stats --no-stream --format "{{.Name}}\t{{.MemUsage}}" \
  | grep -E "el-[12]-geth"

# Example output:
# el-1-geth-lighthouse--<id>   58.6MiB / 31.26GiB
# el-2-geth-lighthouse--<id>   59.8MiB / 31.26GiB
```

**2 — Go runtime heap** (if `go_memstats_*` are exposed):

```bash
curl -s "$EL_METRICS/metrics" \
  | grep -E "^go_memstats_(alloc_bytes|heap_alloc|heap_inuse|heap_sys) "
```

**3 — Combined one-liner for repeated sampling**:

```bash
EL_METRICS=http://127.0.0.1:32928   # replace with actual port

watch -n 60 'echo "--- $(date -u) ---" && \
  docker stats --no-stream --format "{{.Name}}: {{.MemUsage}}" | grep el-1 && \
  curl -s $EL_METRICS/metrics | grep -E "^ETH2030_(chain_blocks_inserted|chain_height|evm_executions|rpc_requests) "'
```

### Block throughput and health spot-check

```bash
EL_RPC=127.0.0.1:32925      # replace with actual port
EL_METRICS=http://127.0.0.1:32928

# 1. Current chain head
cast bn -r http://$EL_RPC

# 2. Blocks processed vs head — mismatch indicates orphaned blocks
BLK_INS=$(curl -s $EL_METRICS/metrics | awk '/^ETH2030_chain_blocks_inserted /{print $2}')
CHAIN_HT=$(curl -s $EL_METRICS/metrics | awk '/^ETH2030_chain_height /{print $2}')
echo "blocks_inserted=$BLK_INS  chain_height=$CHAIN_HT"

# 3. RPC error rate (high rate = client compatibility issue)
RPC_REQ=$(curl -s $EL_METRICS/metrics | awk '/^ETH2030_rpc_requests /{print $2}')
RPC_ERR=$(curl -s $EL_METRICS/metrics | awk '/^ETH2030_rpc_errors /{print $2}')
echo "rpc_requests=$RPC_REQ  rpc_errors=$RPC_ERR"

# 4. EVM throughput
EVM_EX=$(curl -s $EL_METRICS/metrics | awk '/^ETH2030_evm_executions /{print $2}')
EVM_GAS=$(curl -s $EL_METRICS/metrics | awk '/^ETH2030_evm_gas_used /{print $2}')
echo "evm_executions=$EVM_EX  evm_gas_used=$EVM_GAS"
```

### 120-minute soak test with memory logging

Use the pre-built monitor script (requires a running devnet):

```bash
# After booting the devnet, start the monitor in background:
/project/eth2030/docs/plans/memory/monitor.sh &

# It writes every 60s to:
#   docs/plans/memory/memory_log.csv     — per-minute CSV
#   docs/plans/memory/monitor.log        — progress log
#
# After 120min it collects service logs and writes:
#   docs/plans/memory/error_report.md    — error summary
#   docs/plans/memory/el-1.log, cl-1.log, spamoor.log, ...
```

**CSV columns**: `minute, timestamp_utc, block, el1_docker_rss_raw, el1_docker_rss_mb,
el2_docker_rss_raw, el2_docker_rss_mb, el1_blocks_inserted, el1_chain_height,
el1_chain_reorgs, el1_engine_new_payload, el1_engine_fcu, el1_evm_executions,
el1_evm_gas_used, el1_rpc_requests, el1_rpc_errors, el2_blocks_inserted, el2_evm_executions`

### Memory leak diagnosis

If RSS grows unexpectedly, check these bounded caches (all tunable via CLI flags):

| Flag | Default | Controls |
|------|---------|---------|
| `--cache.block` | 256 | in-memory block cache entries |
| `--cache.receipts` | 128 | in-memory receipt cache entries |
| `--cache.state-snapshots` | 4 | `MemoryStateDB` deep-copies for reorg/payload |

```bash
# Reduce cache sizes to diagnose memory source:
docker run eth2030:local --cache.state-snapshots=1 --cache.block=64 ...

# Expected growth pattern after fixes:
# - ~0.9 MB/s per EL node under storagespam scenario (unavoidable: state grows)
# - Plateaus once block cache fills (~256 blocks × block_size)
# - Should NOT grow unboundedly (would indicate a new leak)
```
