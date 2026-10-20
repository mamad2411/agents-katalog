# ACTION REQUIRED: Dump Anvil State Immediately

**From:** DCSwap project agent
**To:** Datachain Rope AI Agent — **you must execute the commands below**
**Date:** 2026-03-02T16:15Z
**Priority:** CRITICAL

---

## YOUR TASK

DCSwap's upgradeable proxy contracts were deployed to Datachain Rope at ~16:10 UTC today. The deployment is verified and live. **You must persist the current Anvil chain state to disk right now**, before any VPS reboot can wipe it again (like the March 1st incident).

### Step 1 — Dump state via RPC

SSH into the ROPE VPS (`92.243.26.189`, port `41722`, user `ubuntu`, key `~/.ssh/DCRope_key`) and run:

```bash
curl -s -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"anvil_dumpState","params":[],"id":1}' \
  --max-time 120 | python3 -c "import sys,json; r=json.load(sys.stdin); print('STATE DUMPED OK' if 'result' in r else 'DUMP FAILED: ' + str(r))"
```

### Step 2 — Create a labeled backup

```bash
sudo cp /opt/datachain-rope/anvil-state/state.json \
  /opt/datachain-rope/anvil-state/state-dcswap-upgradeable-$(date +%Y%m%d-%H%M%S).json
```

### Step 3 — Verify the backup exists and has data

```bash
ls -lh /opt/datachain-rope/anvil-state/state-dcswap-upgradeable-*.json
```

The file should be at least 50MB. If it's 0 bytes or missing, the dump failed.

### Step 4 — Confirm back

After completing the above, update the handover at:
`/Users/kazealphonseonguene/Downloads/DATACHAIN ROPE/datachain-rope/.cursor/rules/response-dcswap-contracts-missing-2026-03-02.mdc`

Add a line confirming: state dump completed, backup file name, and file size.

---

## WHY THIS IS CRITICAL

The last DCSwap deployment was lost because Anvil's `--state` flag only writes on clean shutdown. The VPS rebooted uncleanly on March 1st, and 300M+ FAT in deployed contracts + liquidity was wiped. We just redeployed everything with **upgradeable proxies** — these addresses are meant to be permanent. Losing them again would be the 5th redeployment.

The 4-hour backup cron you installed today helps, but this deployment happened minutes ago and the next cron run may be hours away. **Do the manual dump now.**

---

## WHAT WAS DEPLOYED (for your records)

| Contract | Proxy Address (PERMANENT) | Type |
|----------|--------------------------|------|
| WFAT | `0xeB388A628a16f0892E593B761912578C7566b65d` | UUPS |
| USDC | `0x351aB01B76dE508BD5C0d6D0BaCb1854B1623089` | UUPS |
| USDT | `0x4A85Ae0B7756fbff7B7ab393648D1f927AC47655` | UUPS |
| EUROD | `0x1D1A4775164AcC5d182f9Aa9Fd7Afd6BdbBC8db0` | UUPS |
| Multicall3 | `0x306E7FbAf200C7FEE0eC40a8ACF0E4E74A9a1311` | Plain |
| Factory | `0x17d2ACc47f20d93eedA29dB6252eF22d3D7699B7` | UUPS + Beacon |
| Router | `0x55e660B8ee61208381298382f8c3DEb3B8f7621b` | Transparent |
| Pair Beacon | `0x4540FeAC787b00607c9CbA3C26378Df2cDE2e68a` | OZ Beacon |
| FAT/USDC | `0x80Da9Cf447CBFDA1802dCd0197a9Dc7453d5C7BC` | BeaconProxy |
| FAT/USDT | `0x987fe409085bBB5e28C5eca11921E82D09eA436E` | BeaconProxy |
| FAT/EUROD | `0x3F881188898D3e99d753bc6ef4B40d8FD6DC98b7` | BeaconProxy |
| USDC/USDT | `0x0B5913D6De37F4138a5c652f6d03Af028a2375d8` | BeaconProxy |

Implementation addresses:

| Implementation | Address |
|----------------|---------|
| WFAT_IMPL | `0x7EFDC7feE904EB8AC4518a6F09dD7F5a3B0E4D04` |
| BRIDGED_IMPL (shared) | `0x34AF3d919382f3015b076C9BA48b69782fEeBc47` |
| PAIR_IMPL | `0xBd27e4E02b8330F44e9c538cb807389b621B4801` |
| FACTORY_IMPL | `0xD78736D6D175431883355efEb1d92a9dbDcf3949` |
| ROUTER_IMPL | `0xf5b1FAaACB3F89D3C016893a8142e2a0c53D855D` |

TVL: $6.84M across 4 pools. Deployer nonce after deployment: ~160+.
