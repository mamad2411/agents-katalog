---
name: compose-multi-network-isolation
description: Set up Docker Compose environments with network segmentation (internet, DMZ, settlement) where services are multi-homed across trust boundaries and traffic only flows through designated gateways
version: 2
created: 2026-05-15
updated: 2026-05-15
---
## When to Use
When building a PoC or test environment where services need strict network isolation (e.g., buyer can reach facilitator but not settlement, settlement can't reach the internet). Use when you need per-network DNS control and the ability to simulate network failures.

## Procedure

### 1. Define isolated bridge networks with static subnets
```yaml
networks:
  internet:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.1.0/24
  facilitator-dmz:
    driver: bridge
  settlement-net:
    driver: bridge
```
Assign static subnets only to networks where you need fixed IPs (like the DNS server). Other networks can use default IPAM.

### 2. Add dnsmasq for static DNS resolution
```yaml
dns:
  image: andyshinn/dnsmasq:2.83
  networks:
    internet:
      ipv4_address: 172.28.1.2
  volumes:
    - ./infra/dnsmasq.conf:/etc/dnsmasq.conf:ro
  cap_add:
    - NET_ADMIN
```
dnsmasq config maps service names to their Docker network IPs or container names:
```
# Forward unknown queries to public DNS
server=8.8.8.8
server=1.1.1.1

# Static mappings for internet-segment services
address=/dns.x402.local/172.28.1.2
address=/seller.x402.local/172.28.1.10
address=/gateway.x402.local/172.28.1.20
address=/buyer.x402.local/172.28.1.30
address=/grafana.x402.local/172.28.1.40
address=/test-runner.x402.local/172.28.1.50

# Log DNS queries for debugging
log-queries
log-facility=-
```
**Key**: Must include `server=8.8.8.8` forwarding, otherwise containers can't resolve external hosts. Enable `log-queries` for debugging DNS issues.

### 3. Assign services to specific networks (not all networks)
```yaml
buyer:
  networks: [internet]
gateway:
  networks: [facilitator-dmz]
verifier:
  networks: [facilitator-dmz, settlement-net]  # bridge service
settlement:
  networks: [settlement-net]
```
This enforces isolation — a service can only reach other services on shared networks. Bridge services (like verifier) span multiple networks.

### 4. Point services at the DNS server via dnsmasq
```yaml
buyer:
  dns:
    - 172.28.1.2
  networks:
    internet:
      ipv4_address: 172.28.1.30
```
Only services on the internet segment need DNS. Services on isolated networks (DMZ, settlement) communicate via Docker's internal DNS using container names.

### 5. Route inter-network traffic through Toxiproxy
Place Toxiproxy on every network that needs bridging:
```yaml
toxiproxy:
  image: ghcr.io/shopify/toxiproxy:2.11.0
  command: ["toxiproxy-server", "-host", "0.0.0.0"]
  networks: [internet, facilitator-dmz]
```
Create proxies so that clients connect to `toxiproxy:18000` instead of `gateway:8000` directly.

### 6. Configure environment variables to use proxy endpoints
```yaml
seller:
  environment:
    # NOT http://gateway:8000 — that bypasses Toxiproxy
    X402_GATEWAY_URL: "http://toxiproxy:18000"
```

### 7. Bootstrap Toxiproxy configuration via init container
Create a Python setup script (`infra/setup-toxiproxy.py`) that:
- Retries connecting to Toxiproxy for up to 60 seconds (race condition with startup)
- Creates proxies mapping upstream services
- Applies toxics (latency, slow_close, etc.)

Run as a dedicated Dockerfile setup service:
```yaml
infra-setup:
  build:
    context: .
    dockerfile: infra/Dockerfile.setup
  networks: [internet]
  depends_on:
    toxiproxy:
      condition: service_started
  entrypoint: ["python", "/setup.py"]
```
Dockerfile:
```dockerfile
FROM python:3.12-slim
RUN pip install --no-cache-dir httpx
COPY infra/setup-toxiproxy.py /setup.py
```

### 8. Test Runner Pattern
```yaml
test-runner:
  build:
    context: .
    dockerfile: test-runner/Dockerfile
  networks:
    internet:
      ipv4_address: 172.28.1.50
  dns:
    - 172.28.1.2
  volumes:
    - ./tests:/tests:ro
  depends_on:
    - dns
    - toxiproxy
    - seller
```
Test runner Dockerfile — use `sleep infinity` so container stays alive:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir pytest httpx pytest-asyncio
COPY common/ /app/common/
RUN pip install --no-cache-dir /app/common/.
CMD ["sleep", "infinity"]
```
Run tests via:
```bash
docker exec x402-poc-test-runner-1 python -m pytest /tests/ -v -s
```

### 9. Prometheus DNS-Based Service Discovery
For monitoring services that use custom DNS (.local names):
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "x402-services"
    dns_sd_configs:
      - names: ["seller.x402.local", "gateway.x402.local"]
        type: A
        port: 8000
    metrics_path: /metrics
```
Prometheus must be on the same network as the DNS server to resolve `.local` names.

## Pitfalls
- **Services on different networks cannot communicate**: This is the whole point, but it's easy to forget. If a service needs to reach another, add a Toxiproxy bridge or put them on a shared network.
- **dnsmasq needs NET_ADMIN**: Add `cap_add: [NET_ADMIN]` or DNS won't work inside containers.
- **Static IPs require static subnets**: You can only use `ipv4_address` if the network has a configured `subnet` in `ipam.config`.
- **DNS caching**: Containers may cache DNS results. Restart or use short TTLs in dnsmasq config when debugging.
- **Toxiproxy must be on all bridged networks**: If Toxiproxy isn't on both source and destination networks, proxy traffic can't flow.
- **Toxiproxy `-host 0.0.0.0` is mandatory**: The default only binds admin API to 127.0.0.1, unreachable from other containers. Always add `command: ["toxiproxy-server", "-host", "0.0.0.0"]`.
- **Toxiproxy listen `0.0.0.0` in proxy creation**: Set `"listen": "0.0.0.0:PORT"`, not `127.0.0.1:PORT`.
- **Init container race condition**: `infra-setup` depends on `service_started` (not `healthy`), so it must include its own retry loop.
- **Test runner needs `sleep infinity`**: Don't run tests at build time. Keep the container alive for `docker exec` test runs.
- **Gateway IP `.1`**: Docker assigns `.1` as gateway on custom networks. Never use `.1` as a static container IP.

## Verification
1. `docker network ls` — shows all three networks
2. `docker exec buyer ping settlement` — should fail (different network)
3. `docker exec buyer curl http://toxiproxy:18000` — should succeed (routed through proxy)
4. `docker exec buyer nslookup seller.x402.local 172.28.1.2` — DNS resolves correctly
5. Add a Toxiproxy toxic and confirm the client experiences the simulated fault
6. `docker exec x402-poc-test-runner-1 python -m pytest /tests/ -v` — test runner works