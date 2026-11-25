---
name: deploy-proxyware-fleet
description: Containerize and orchestrate modern DePIN bandwidth monetization light nodes (Grass, Dawn, Nodepay) with Solana/EVM wallet authentication, WebSocket telemetry, and uptime scoring. Use when scaling decentralized bandwidth monetization fleets, orchestrating residential DePIN nodes, or configuring proof-of-bandwidth telemetry.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Deploy Proxyware Fleet

Use this skill to containerize, orchestrate, and monitor modern Decentralized Physical Infrastructure Network (DePIN) bandwidth monetization nodes (Grass, Dawn, Nodepay), ensuring cryptographic security, strict resource limits, and high uptime yield.

## Legal & Compliance Notice

Decentralized bandwidth-sharing protocols (Grass, Dawn, Nodepay) allow residential internet users to monetize unused bandwidth. Deploying nodes on third-party networks, enterprise infrastructure, or commercial datacenters without explicit network authorization violates Acceptable Use Policies (AUP) and terms of service. This skill documents containerized node orchestration, telemetry monitoring, and wallet authentication mechanics only. Confirm you possess legitimate authorization for the residential network endpoints used. Any deployment intended to bypass platform geographical or network classification controls falls under `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role and requires explicit written authorization before execution.

## When to Use

- containerizing modern DePIN bandwidth monetization nodes (Grass / Wynd Network, Dawn, Nodepay, Gradient)
- authenticating DePIN light nodes via Solana (Ed25519) or EVM (Secp256k1) cryptographic wallet signatures
- orchestrating multi-node residential fleets with WebSocket telemetry and uptime monitoring (> 98%)
- enforcing strict cgroup CPU/memory caps and read-only container root filesystems to prevent host degradation
- tracking epoch rewards, points accrual, and node connection scoring across decentralized networks

## Example (DePIN Light Node Compose & Cryptographic Wallet Auth)

```yaml
# Docker Compose orchestrating DePIN light nodes with residential gateway routing
version: "3.8"
services:
  depin-grass-node:
    image: depin/grass-light-node:v2.4.0
    network_mode: "service:residential-gateway"
    read_only: true
    tmpfs:
      - /tmp:rw,size=512M
      - /dev/shm:rw,size=512M
    environment:
      - WALLET_PUBLIC_KEY=7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
      - NODE_SIGNATURE=3N8vKjW...Ed25519Signature...
      - TELEMETRY_WS_URL=wss://telemetry.wynd.network/v1
    deploy:
      resources:
        limits:
          cpus: "0.25"
          memory: 256M
```

```typescript
// Solana Ed25519 message signing for DePIN proof-of-bandwidth authentication
import { Keypair } from "@solana/web3.js";
import nacl from "tweetnacl";

export function generateNodeAuthSignature(keypair: Keypair, challengeNonce: string): string {
  const timestamp = Math.floor(Date.now() / 1000);
  const message = new TextEncoder().encode(`DePIN-Auth:${challengeNonce}:${timestamp}`);
  const signature = nacl.sign.detached(message, keypair.secretKey);
  return Buffer.from(signature).toString("base64");
}
```

```python
# Prometheus uptime exporter & WebSocket heartbeat monitor
import asyncio, websockets, json, time

async def monitor_depin_heartbeat(ws_url: str, auth_token: str):
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({"action": "authenticate", "token": auth_token}))
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get("type") == "ping":
                await ws.send(json.dumps({"type": "pong", "timestamp": time.time()}))
```

## Core Rules

- **DEPIN-PROTOCOL-LOCK**: Deploy exclusively modern Decentralized Physical Infrastructure Network (DePIN) protocols (Grass, Dawn, Nodepay, Gradient). Deprecate legacy centralized proxyware (Honeygain, EarnApp) due to pervasive datacenter blacklisting and negligible yield.
- **CRYPTOGRAPHIC-WALLET-AUTH**: Node authentication MUST utilize asymmetric cryptographic signatures (Ed25519 for Solana, Secp256k1 for EVM). Never store or inject raw private keys into container environments; pass public addresses and delegated session-scoped signatures.
- **UPTIME-AND-TELEMETRY**: Maintain persistent WebSocket/gRPC telemetry connections with ping/pong heartbeats to preserve uptime scores > 98%. Drops below 95% trigger score penalties and reduced epoch reward allocations.
- **RESIDENTIAL-IP-ROUTING**: DePIN nodes MUST route outbound traffic through verified residential or mobile ISP connections. Datacenter IP blocks (AWS, Hetzner, OVH) are automatically flagged and blacklisted by DePIN scorekeepers.
- **CONTAINER-EPHEMERAL-DISKS**: Container root filesystems MUST be mounted read-only (`readOnlyRootFilesystem: true`) with volatile caches placed on `tmpfs` mounts (`/tmp` and `/dev/shm`, minimum 512 MiB) to prevent disk space exhaustion.
- **RESOURCE-LOCK**: Enforce strict cgroup limits (CPU <= 0.25 cores, memory <= 256 MiB per container) to protect the host machine from resource starvation when scaling fleets.
- **REMOTE-DNS-LOCK**: Remote DNS resolution MUST be enforced on the residential proxy gateway via SOCKS5 or WireGuard tunnel. Never resolve DNS queries using local datacenter host nameservers.

## Suggested Process

1. **Cryptographic Keypair & Sign-In Setup**: Generate dedicated operational wallet keypairs (Solana Ed25519). Generate session authorization signatures off-chain using the challenge nonces provided by the DePIN network gateway.
2. **Container Image Hardening**: Build minimal Docker containers wrapping DePIN light node clients. Enforce non-root execution (`USER 1001`), read-only root filesystems, and tmpfs mounts.
3. **Network Gateway Binding**: Wire container network namespaces to residential VPN/proxy gateways (WireGuard or SOCKS5 sidecars). Verify zero IP leaks and confirm the public IP is classified as Residential ISP.
4. **Telemetry & Uptime Monitoring**: Deploy a Prometheus/Grafana exporter scraping WebSocket connection status, ping latency, and epoch score metrics. Configure alert thresholds for uptime dips below 98%.
5. **Epoch Reward Tracking**: Integrate automated tracking scripts that query DePIN REST/GraphQL APIs daily to record accumulated points, tier rankings, and token claims.

## Checklist

- [ ] Node configuration uses modern DePIN protocols (Grass, Dawn, Nodepay).
- [ ] Wallet authentication uses Ed25519/Secp256k1 cryptographic signatures (no private keys in containers).
- [ ] Nodes route strictly through residential or mobile IP connections (zero datacenter IP routing).
- [ ] Read-only root filesystem (`readOnlyRootFilesystem: true`) configured on all containers.
- [ ] `tmpfs` volumes configured for `/tmp` and `/dev/shm` (minimum 512 MiB).
- [ ] CPU (<= 0.25) and memory (<= 256 MiB) limits explicitly enforced in Compose/Kubernetes.
- [ ] Remote DNS resolution verified on residential gateway (no host DNS leak).
- [ ] WebSocket telemetry active with connection uptime score verified > 98%.
- [ ] Epoch reward accrual and point balance monitoring operational.
- [ ] Host disk space and cgroup memory consumption validated under full load.

## Output Contracts

When the DePIN fleet deployment is finalized or updated for handoff, emit:

- **`contracts/schemas/deployment-plan.json`** capturing the DePIN fleet size, node wallet public keys, residential network topology, resource limits, and rollback path.
- Markdown summary of fleet performance, uptime metrics, epoch reward accrual, and compliance boundaries.

Skip emission for local single-node test runs that do not cross role boundaries.

## Failure Modes

- **DePIN node disconnect & uptime slash**: WebSocket connection drops unnoticed, slashing epoch point multipliers. Mitigation: implement automated watchdog daemon that restarts container upon 3 consecutive missed heartbeats.
- **Datacenter IP disqualification**: Node routes through unverified datacenter IP; DePIN network zeroes points. Mitigation: run IP fraud score probe pre-flight; verify residential classification before node connects.
- **Container memory leak**: Headless Chromium engine or Node process inside container leaks memory until host crashes. Mitigation: enforce strict 256MB cgroup hard limits with auto-restart policy.
- **Cryptographic signature expiration**: Ephemeral session signature expires, causing unauthorized 401 responses. Mitigation: automate periodic signature renewal using a sealed key manager.
- **Host disk bloat**: Accumulated temporary socket files fill disk. Mitigation: enforce read-only container rootfs with ephemeral `tmpfs` mounts.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Wallet private keys must never be exposed or stored in container environment variables; use public keys and delegated cryptographic signatures only.
- **ASI04 Supply Chain**: DePIN node images and packages must be verified against official protocol repositories and SHA-256 digests; avoid untrusted community node images.
- **ASI05 RCE Guard**: Never construct node launch arguments, WebSocket URLs, or environment variables from unauthenticated network messages.
- **ASI07 Inter-Agent Communication**: DePIN node configurations and telemetry statistics must be emitted via `contracts/schemas/deployment-plan.json` for infrastructure monitoring.
- **ASI09 Human-Agent Trust Exploitation**: Clearly articulate DePIN token volatility, network slashing risks, and residential bandwidth usage; do not promise guaranteed passive yields.

## Related Skills

- **deploy-mmo-infrastructure**: Provision the core residential proxy gateways and network tunnels powering the DePIN fleet.
- **setup-deployment**: Generic cloud container orchestration and service lifecycle management.
- Companion reference: `references/depin-bandwidth-monetization-node-specs.md`
- Companion example: `examples/docker-compose-depin-light-node-fleet.yaml`
