---
name: dind-port-forwarding
description: "Expose Docker Compose service ports through a DinD container to the host machine using 3-layer forwarding: compose network → DinD container → host"
version: 1
created: 2026-05-16
updated: 2026-05-16
---
## When to Use

When running Docker Compose inside a DinD container and you need to expose compose service ports (e.g., Jaeger UI, API endpoints) to the host machine. This requires forwarding through 3 network layers: compose network → DinD container → tooling/host container → host browser/client.

## Procedure

### 1. Identify the ports you need to expose

Common observability/service ports:
- Jaeger UI: 16686
- OTLP gRPC: 4317
- OTLP HTTP: 4318
- Application API: 8000, 8080, etc.

### 2. Map ports from DinD container to host

When starting the DinD container, use `-p` to publish each port:

```bash
DIND_IMAGE="docker:dind"
DIND_NAME="x402-dind"

docker run -d \
    --name "$DIND_NAME" \
    --privileged \
    -p 16686:16686 \
    -p 4317:4317 \
    -p 4318:4318 \
    -e DOCKER_TLS_CERTDIR="" \
    "$DIND_IMAGE"
```

This makes `localhost:16686` on the host route to `DinD:16686`.

### 3. Map ports in docker-compose.yml (compose → DinD)

In the compose file inside DinD, expose the same ports from the target service:

```yaml
services:
  jaeger:
    image: jaegertracing/all-in-one:1.59
    networks: [internet, dmz, settlement]
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    ports:
      - "16686:16686"   # UI → DinD:16686 → host:16686
      - "4317:4317"     # gRPC → DinD:4317 → host:4317
      - "4318:4318"     # HTTP → DinD:4318 → host:4318
```

### 4. The 3-layer forwarding chain

The complete path for a request from host browser to Jaeger:

```
Host browser → localhost:16686
         ↓ (DinD -p 16686:16686)
DinD container:16686
         ↓ (compose ports: "16686:16686")
Jaeger container:16686
```

Each `-p` in the `docker run` and `ports:` in compose adds one hop. Both must match.

### 5. Add health checks using the forwarded ports

From inside the DinD container, services are reachable at `http://jaeger:16686`.
From the host, they're reachable at `http://localhost:16686`.

```bash
# Verify from host
curl -s http://localhost:16686/api/services | head -5

# Verify from inside DinD
docker exec "$DIND_NAME" curl -s http://jaeger:16686/api/services | head -5

# Or from test-runner container
docker exec "$DIND_NAME" docker exec test-runner python3 -c "
import httpx
r = httpx.get('http://jaeger:16686/api/services', timeout=5)
print(r.status_code, r.json().get('data', []))
"
```

### 6. Multiple service ports

To expose multiple services (e.g., both Jaeger and an API server):

```bash
docker run -d \
    --name "$DIND_NAME" \
    --privileged \
    -p 16686:16686 \   # Jaeger UI
    -p 4317:4317   \   # OTLP gRPC
    -p 4318:4318   \   # OTLP HTTP
    -p 8000:8000   \   # Seller API
    -p 5555:5555   \   # Debug/other
    -e DOCKER_TLS_CERTDIR="" \
    "$DIND_IMAGE"
```

## Pitfalls

- **Port conflicts**: If Podman (or another Docker daemon) already uses a port, you'll get "port already allocated". Check with `ss -tlnp | grep <port>` before starting DinD.
- **Port 2375 conflict**: Podman uses 2375 for its own daemon. Never publish this port from DinD.
- **Compose `ports` vs `expose`**: Use `ports` (host:container) to publish to DinD's network namespace. `expose` only makes ports available to other compose services, not to the DinD host.
- **Double mapping required**: You need BOTH the `docker run -p` flag AND the compose `ports:` directive. Missing either one breaks the chain silently.
- **Firewall/VPN interference**: Cloudflare WARP or similar VPNs may intercept `localhost` traffic. Test with `curl http://localhost:<port>` from the host.
- **Host port != container port**: You can remap (e.g., `-p 16687:16686` if 16686 is taken on host), but remember the mapping when accessing from browser.

## Verification

```bash
# 1. Check DinD is publishing the port
docker port "$DIND_NAME"
# Should show: 16686/tcp -> 0.0.0.0:16686

# 2. Check service is running inside compose
docker exec "$DIND_NAME" docker compose -f /workspace/docker-compose.yml ps

# 3. Reach Jaeger from inside DinD (container → container)
docker exec "$DIND_NAME" curl -s http://jaeger:16686/api/services

# 4. Reach Jaeger from host (3-hop chain complete)
curl -s http://localhost:16686/api/services

# 5. Browser test
echo "Jaeger UI: http://localhost:16686"
```