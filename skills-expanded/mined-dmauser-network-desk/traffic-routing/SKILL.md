# Skill: Traffic Routing Methods (`lb_traffic_routing`)

Configure traffic distribution and routing strategies across Azure, AWS, and GCP load balancers. Covers weighted distribution, priority/failover, geographic steering, latency-based routing, URL path-based routing, host-based routing, and session affinity.

---

## Routing Methods Overview

| Method | How It Works | Best For |
|---|---|---|
| **Round-robin** | Equal distribution across backends | Homogeneous backends, no preference |
| **Weighted** | Distribute by assigned weight ratio | Canary deployments, gradual rollouts |
| **Priority / Failover** | All traffic to primary; failover if unhealthy | Active-passive DR |
| **Geographic** | Route by client's geographic location | Data sovereignty, regional compliance |
| **Latency / Performance** | Route to lowest-latency endpoint | Global apps prioritizing UX |
| **URL path-based** | Route by URL path (`/api/*`, `/images/*`) | Microservices behind a single domain |
| **Host-based** | Route by `Host` header (`api.contoso.com` vs `web.contoso.com`) | Multi-tenant, multi-app on one LB |
| **Session affinity** | Stick client to same backend | Stateful apps (shopping carts, WebSocket) |

---

## Azure Routing Configuration

### Application Gateway v2 — Path & Host-Based Routing

```bash
# Path-based routing: /api/* → api-pool, /images/* → static-pool
az network application-gateway url-path-map create \
  --resource-group myRG \
  --gateway-name myAppGW \
  --name myPathMap \
  --default-address-pool defaultPool \
  --default-http-settings defaultSettings \
  --paths /api/* \
  --address-pool apiPool \
  --http-settings apiSettings \
  --rule-name apiRule

az network application-gateway url-path-map rule create \
  --resource-group myRG \
  --gateway-name myAppGW \
  --path-map-name myPathMap \
  --name staticRule \
  --paths "/images/*" "/css/*" "/js/*" \
  --address-pool staticPool \
  --http-settings staticSettings

# Multi-site (host-based) listener
az network application-gateway http-listener create \
  --resource-group myRG \
  --gateway-name myAppGW \
  --name apiListener \
  --host-name api.contoso.com \
  --frontend-port httpsPort \
  --ssl-cert myCert
```

### Application Gateway v2 — Session Affinity

```bash
# Cookie-based affinity (Application Gateway managed cookie)
az network application-gateway http-settings update \
  --resource-group myRG \
  --gateway-name myAppGW \
  --name mySettings \
  --cookie-based-affinity Enabled \
  --affinity-cookie-name ApplicationGatewayAffinity
```

### Azure Front Door — Weighted & Priority Routing

```bash
# Origin group with weighted routing (80/20 split)
az afd origin-group create \
  --resource-group myRG \
  --profile-name myFD \
  --origin-group-name myOriginGroup \
  --probe-path /healthz \
  --probe-protocol Https \
  --sample-size 4 \
  --successful-samples-required 3

az afd origin create --origin-group-name myOriginGroup --profile-name myFD \
  --resource-group myRG --name primary \
  --host-name primary.contoso.com --priority 1 --weight 80 --enabled-state Enabled

az afd origin create --origin-group-name myOriginGroup --profile-name myFD \
  --resource-group myRG --name canary \
  --host-name canary.contoso.com --priority 1 --weight 20 --enabled-state Enabled
```

### Traffic Manager — DNS-Based Global Routing

```bash
# Performance-based routing (lowest latency)
az network traffic-manager profile create \
  --resource-group myRG \
  --name myTM \
  --routing-method Performance \
  --unique-dns-name myapp

# Geographic routing
az network traffic-manager profile create \
  --resource-group myRG \
  --name myTMGeo \
  --routing-method Geographic \
  --unique-dns-name myapp-geo
```

**Traffic Manager routing methods:** Priority, Weighted, Performance, Geographic, MultiValue, Subnet.

---

## AWS Routing Configuration

### ALB — Path & Host-Based Routing

```bash
# Path-based rule: /api/* → api-target-group
aws elbv2 create-rule \
  --listener-arn arn:aws:elasticloadbalancing:... \
  --priority 10 \
  --conditions '[{"Field":"path-pattern","Values":["/api/*"]}]' \
  --actions '[{"Type":"forward","TargetGroupArn":"arn:aws:elasticloadbalancing:...api-tg"}]'

# Host-based rule: api.contoso.com → api-target-group
aws elbv2 create-rule \
  --listener-arn arn:aws:elasticloadbalancing:... \
  --priority 20 \
  --conditions '[{"Field":"host-header","Values":["api.contoso.com"]}]' \
  --actions '[{"Type":"forward","TargetGroupArn":"arn:aws:elasticloadbalancing:...api-tg"}]'

# Weighted target group forwarding (canary)
aws elbv2 create-rule \
  --listener-arn arn:aws:elasticloadbalancing:... \
  --priority 30 \
  --conditions '[{"Field":"path-pattern","Values":["/*"]}]' \
  --actions '[{
    "Type": "forward",
    "ForwardConfig": {
      "TargetGroups": [
        {"TargetGroupArn": "arn:...stable-tg", "Weight": 90},
        {"TargetGroupArn": "arn:...canary-tg", "Weight": 10}
      ],
      "TargetGroupStickinessConfig": {"Enabled": true, "DurationSeconds": 3600}
    }
  }]'
```

### ALB — Session Affinity (Stickiness)

```bash
# Application-level stickiness (app-generated cookie)
aws elbv2 modify-target-group-attributes \
  --target-group-arn arn:aws:elasticloadbalancing:... \
  --attributes Key=stickiness.enabled,Value=true \
               Key=stickiness.type,Value=app_cookie \
               Key=stickiness.app_cookie.cookie_name,Value=MYSESSIONID \
               Key=stickiness.app_cookie.duration_seconds,Value=86400
```

### Route 53 — DNS-Based Routing

- **Latency routing**: Routes to the region with lowest latency from the client.
- **Failover routing**: Active-passive with health checks.
- **Geolocation routing**: Routes by client continent/country/state.
- **Weighted routing**: Percentage-based split across endpoints.

---

## GCP Routing Configuration

### URL Map — Path & Host-Based

```bash
# Create URL map with path-based routing
gcloud compute url-maps create my-url-map \
  --default-service default-backend-service

gcloud compute url-maps add-path-matcher my-url-map \
  --path-matcher-name api-matcher \
  --default-service default-backend-service \
  --path-rules "/api/*=api-backend-service,/images/*=static-backend-service"

# Host rule for multi-site
gcloud compute url-maps add-host-rule my-url-map \
  --hosts="api.contoso.com" \
  --path-matcher-name api-matcher
```

### Traffic Splitting (Canary)

```bash
# Weighted traffic splitting (90/10)
gcloud compute url-maps edit my-url-map
# In the YAML editor, add:
# defaultRouteAction:
#   weightedBackendServices:
#   - backendService: projects/.../backendServices/stable
#     weight: 90
#   - backendService: projects/.../backendServices/canary
#     weight: 10
```

### Cloud DNS — Routing Policies

```bash
# Weighted routing via DNS
gcloud dns record-sets create myapp.contoso.com \
  --zone=my-zone --type=A --ttl=60 \
  --routing-policy-type=WRR \
  --routing-policy-data="0.8=10.0.1.1;0.2=10.0.2.1"

# Geolocation routing via DNS
gcloud dns record-sets create myapp.contoso.com \
  --zone=my-zone --type=A --ttl=60 \
  --routing-policy-type=GEO \
  --routing-policy-data="us-east1=10.0.1.1;europe-west1=10.0.2.1"
```

---

## Session Affinity Considerations

Session affinity (stickiness) reduces the benefit of load balancing. Use it only when necessary:

1. **Prefer stateless architectures** — externalize session state to Redis, DynamoDB, or a shared cache.
2. **Cookie-based** (L7) is preferred over **source-IP-based** (L4) — source IP can change (NAT, mobile roaming).
3. **Duration** should match the session timeout — not indefinite.
4. **Canary + stickiness** — combine weighted routing with sticky sessions so a user stays on the canary version for the full session.

---

## Common Routing Mistakes

1. **Missing default rule** — path-based routing without a catch-all returns 404/502 for unmatched paths.
2. **Priority conflicts** — rules evaluated in priority order; a low-priority catch-all before specific rules blocks them.
3. **DNS TTL too high for failover** — Traffic Manager / Route 53 failover is DNS-based; high TTL delays failover.
4. **Weighted routing without health checks** — traffic routed to unhealthy backends because no health check is configured.
5. **Session affinity with autoscaling** — sticky sessions prevent even distribution when new instances scale out.

**Analysis only — verify against vendor documentation before applying.**
