---
name: deploy-mmo-infrastructure
description: Deploy and manage proxy pools (Residential/4G) with dynamic health probes and Anti-Detect Browser orchestration enforcing automated warmup state machines. Use when deploying a new MMO operation, expanding to new ad accounts, or migrating proxy infrastructure.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Deploy MMO Infrastructure

Use this skill to provision isolated proxy and browser-profile infrastructure for Make Money Online (MMO) operations, featuring dynamic proxy health probes and automated account warmup state machines.

## Legal & Compliance Notice

Anti-detect browsers and fingerprint normalization exist in a grey zone: using them to manage multiple legitimate accounts is common practice, but using them specifically to evade a platform's fraud, ownership, or ad-review detection is a ToS violation on most ad and affiliate platforms and can carry account or payment-processor consequences beyond the immediate operation. This skill documents proxy/browser provisioning mechanics only. Anonymity and isolation techniques used to protect legitimate multi-account operations are in scope for default execution; techniques whose specific purpose is to defeat a platform's ad review, moderation, or account-integrity system fall under `REVIEW-SYSTEM LOCK` in the `mmo-engineer` role and require explicit written user authorization plus Security Engineer review before implementation.

## When to Use

- deploying a new MMO operation from scratch with dedicated residential proxy endpoints
- implementing active proxy health probes with latency thresholds (p95 < 1200ms) and IP fraud scoring
- orchestrating account warmup pipelines via a formal 7-stage Finite State Machine
- expanding to new ad accounts requiring strict 1:1 profile-to-IP affinity and zero ASN overlap
- migrating proxy infrastructure or automating failover across residential/4G pools

## Example (Dynamic Health Probe & Warmup Finite State Machine)

```python
# Proxy Health Probe & Fraud Scoring Verification
import requests, time

def probe_proxy_health(proxy_url: str) -> dict:
    proxies = {"http": proxy_url, "https": proxy_url}
    t0 = time.perf_counter()
    r = requests.get("https://api.ipdata.co?api-key=SECRET", proxies=proxies, timeout=5)
    latency_ms = (time.perf_counter() - t0) * 1000
    data = r.json()
    fraud_score = data.get("threat", {}).get("fraud_score", 0)
    is_datacenter = data.get("threat", {}).get("is_datacenter", False)
    
    # Enforce p95 latency < 1200ms and IP fraud score <= 25
    healthy = (latency_ms < 1200) and (fraud_score <= 25) and (not is_datacenter)
    return {"healthy": healthy, "latency_ms": latency_ms, "fraud_score": fraud_score, "ip": data.get("ip")}
```

```yaml
# Docker Compose with dedicated residential proxy sidecar and tmpfs mounts
version: "3.8"
services:
  browser_profile:
    image: camoufox/stealth:latest
    network_mode: "service:proxy_tunnel"
    read_only: true
    tmpfs:
      - /tmp:rw,size=2G
      - /dev/shm:rw,size=2G
    environment:
      - PROFILE_ID=prof-us-east-401
      - WARMUP_STATE=PASSIVE_BROWSING
  proxy_tunnel:
    image: wireguard/client:latest
    cap_add: [NET_ADMIN]
    environment:
      - PROXY_ENDPOINT=res-pool-node7.provider.com:1080
      - FRAUD_THRESHOLD=25
```

```typescript
// Automated Warmup Finite State Machine (FSM)
export enum WarmupState {
  INITIALIZING = "INITIALIZING",
  PASSIVE_BROWSING = "PASSIVE_BROWSING",       // Days 1-2: Top 500 sites, read news
  COOKIE_ACCUMULATION = "COOKIE_ACCUMULATION", // Days 3-4: E-commerce, pixel collection
  INTERACTIVE_AUTH = "INTERACTIVE_AUTH",       // Day 5: Social OAuth & email validation
  ACTIVE_WARMUP = "ACTIVE_WARMUP",             // Days 6-7: Low-velocity platform likes/scrolls
  PRODUCTION_READY = "PRODUCTION_READY",       // Day 8+: Full automation & campaign ops
  QUARANTINE = "QUARANTINE"                    // Triggered on checkpoint/captcha loop
}
```

## Core Rules

- **ANONYMITY-LOCK**: Validate that origin datacenter IP is fully masked before allowing any traffic through provisioned infrastructure. Zero WebRTC or DNS leaks permitted.
- **ISOLATION-LOCK**: Prevent proxy IP reuse across isolated profiles. Never map the same IP or residential session to unrelated business operations or ad accounts.
- **1:1-PROFILE-IP-AFFINITY**: Maintain strict 1:1 binding between Account ID, Browser Profile ID, and Residential Proxy Session. Never switch proxy subnets or ASNs during an active session — mid-session ASN switches trigger immediate platform fraud graph alerts.
- **DYNAMIC-PROXY-HEALTH-PROBES**: All proxy gateways MUST undergo continuous health probing: measure p95 latency (< 1200ms threshold), query IPQS/Scamalytics for fraud scores (reject score > 25), and detect unexpected exit IP rotation. Automatically rotate to standby pool on probe failure.
- **ZERO-HOST-DNS-LEAK**: All DNS resolution MUST occur remotely on the proxy exit node (SOCKS5 with remote DNS or HTTP CONNECT). Reject any setup where host DNS queries resolve via datacenter nameservers.
- **K8S-EGRESS-LOCKDOWN**: For Kubernetes-based fleets, enforce Cilium or Calico Egress Gateway policies that force all pod outbound traffic through dedicated static proxy gateways or sidecar SOCKS5/HTTP tunnel containers. Direct pod internet egress is strictly forbidden.
- **WARMUP-FSM-LIFECYCLE**: Ad accounts MUST progress sequentially through the 7-stage automated warmup FSM (`INITIALIZING` -> `PASSIVE_BROWSING` -> `COOKIE_ACCUMULATION` -> `INTERACTIVE_AUTH` -> `ACTIVE_WARMUP` -> `PRODUCTION_READY` -> `QUARANTINE`). Any platform checkpoint or CAPTCHA failure triggers immediate transition to `QUARANTINE`.

## Suggested Process

1. **Proxy Pool Provisioning**: Connect residential, mobile (4G/5G), and ISP proxy networks. Configure automated rotation endpoints with sticky session support (minimum 30-minute session stickiness).
2. **Health Probe Integration**: Implement background health probe workers that monitor p95 latency (< 1200ms), detect exit IP changes, and check Scamalytics/IPQS fraud scores. Wire automatic failover triggers to secondary provider pools.
3. **Environment Orchestration**: Stand up Docker/Terraform or Kubernetes environments hosting Anti-Detect Browser profiles or headless C++ patched engines (Camoufox). Enforce sidecar proxy tunnels and remote DNS resolution.
4. **Automated Warmup FSM Execution**: Attach the automated warmup orchestrator to new profiles. Execute passive browsing, cookie harvesting across high-trust commercial domains, and gradual engagement rate expansion over 7 days.
5. **Leak & Quarantine Audit**: Verify remote DNS resolution, test WebRTC stun/turn bindings, and inspect quarantine alerts before declaring profiles `PRODUCTION_READY`.

## Checklist

- [ ] Residential and mobile proxy endpoints configured with sticky sessions.
- [ ] Dynamic proxy health probes active: p95 latency < 1200ms and IP fraud score <= 25.
- [ ] Automatic failover mechanism switches unhealthy proxies to standby pool within 5s.
- [ ] 1:1 IP-to-Profile binding enforced; no subnet sharing across isolated accounts.
- [ ] Remote DNS leak test passed — zero host datacenter nameserver exposure.
- [ ] WebRTC ICE candidates bound strictly to proxy IP.
- [ ] Automated Warmup FSM configured with all 7 discrete states and transition rules.
- [ ] Checkpoint / CAPTCHA failure automatically routes accounts to `QUARANTINE`.
- [ ] Kubernetes Egress Gateway (Cilium/Calico) forces all container traffic through proxy sidecars.
- [ ] Encrypted profile state persistence configured for S3/MinIO with volatile cache on `tmpfs`.

## Output Contracts

When the infrastructure change is consumed by an infra agent, a release pipeline, or a cross-role handoff, emit:

- **`contracts/schemas/deployment-plan.json`** capturing the proxy topology, health probe metrics, warmup state machine status, network posture, and rollback path.
- Markdown summary of infrastructure topology, proxy health benchmarks, and compliance boundaries.

Skip emission for local sandbox experiments that do not cross role boundaries.

## Failure Modes

- **Proxy latency degradation**: Residential proxy p95 latency spikes > 2500ms, causing browser automation timeouts. Mitigation: health probe detects latency spike and triggers automated failover to alternate residential pool.
- **Dirty IP assignment**: Proxy provider assigns an IP with fraud score > 50 or datacenter tag, causing immediate login challenge. Mitigation: reject IP during health probe pre-flight before profile launch.
- **Premature warmup promotion**: Moving an account from `PASSIVE_BROWSING` directly to `PRODUCTION_READY` triggers platform anomaly detection. Mitigation: enforce immutable FSM day and interaction quota gates.
- **Mid-session ASN shift**: Rotating proxy resets IP to a different ASN during active account session, triggering fraud flag. Mitigation: configure sticky sessions with sticky IP pinning per profile.
- **Host DNS resolver leakage**: System queries local cloud provider DNS, revealing server identity. Mitigation: configure SOCKS5 remote DNS resolution in browser engine args.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: Proxy gateway credentials and platform account tokens are scoped to the infrastructure runtime; never store plaintext credentials in repository files.
- **ASI04 Supply Chain**: Anti-detect browser images, proxy daemons, and container base images must be pinned to verified SHA-256 digests; audit upstream packages.
- **ASI05 RCE Guard**: Never construct infrastructure configurations, AT modem commands, or proxy routing tables from unsanitized external web content.
- **ASI07 Inter-Agent Communication**: Infrastructure specifications and probe health results must be emitted via `contracts/schemas/deployment-plan.json` for validation by downstream operators.
- **ASI09 Human-Agent Trust Exploitation**: Do not present proxy pools as infallible; surface proxy rotation risks and platform fraud scores transparently.

## Related Skills

- **deploy-proxyware-fleet**: Orchestrate decentralized bandwidth monetization nodes on provisioned network infrastructure.
- **setup-deployment**: Generic CI/CD and cloud deployment workflows outside MMO performance environments.
- Companion reference: `references/proxy-pool-rotation-and-anti-detect-specs.md`
- Companion example: `examples/proxy-health-probe-and-rotation-daemon.py`
