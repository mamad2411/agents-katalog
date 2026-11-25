---
name: canary-release
description: Implement canary release strategy for gradual traffic shifting with automated promotion and rollback. Outputs traffic weight configuration, metric-based promotion gates, and rollback triggers.
argument-hint: [platform, traffic splitting method, metrics to monitor, rollback threshold]
allowed-tools: Read, Write, Bash
---

# Canary Release

A canary release gradually shifts traffic from the stable version to a new version — 1% → 5% → 25% → 100% — with automated gates that stop promotion if metrics degrade. It's safer than blue-green because impact is limited to a small user slice if something goes wrong.

## Process

1. **Deploy canary alongside stable** — same cluster, separate deployment.
2. **Start with minimal traffic** — 1-5% to canary.
3. **Define promotion gates** — metric thresholds that must hold before each step.
4. **Automate progression** — time-based + metric-gated steps.
5. **Rollback on threshold breach** — automatic, not manual.
6. **Full promotion** — 100% when all gates pass.

## Output Format

### Kubernetes + Argo Rollouts

```yaml
# k8s/rollout.yaml — Argo Rollouts canary strategy
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
  namespace: production
spec:
  replicas: 20
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:1.5.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            periodSeconds: 5
  
  strategy:
    canary:
      # Traffic routing via Istio VirtualService
      trafficRouting:
        istio:
          virtualService:
            name: myapp-vsvc
          destinationRule:
            name: myapp-destrule
            canarySubsetName: canary
            stableSubsetName: stable
      
      # Canary steps
      steps:
        - setWeight: 5       # 5% to canary
        - pause:
            duration: 5m     # Wait 5 minutes
        
        - analysis:          # Run analysis before proceeding
            templates:
              - templateName: canary-analysis
            args:
              - name: service-name
                value: myapp-canary
        
        - setWeight: 20      # 20% to canary
        - pause:
            duration: 10m
        
        - analysis:
            templates:
              - templateName: canary-analysis
            args:
              - name: service-name
                value: myapp-canary
        
        - setWeight: 50
        - pause:
            duration: 15m
        
        - setWeight: 100     # Full rollout
      
      # Automatic rollback triggers
      autoPromotionEnabled: false   # Manual approval for final step
      
      antiAffinity:
        requiredDuringSchedulingIgnoredDuringExecution: {}
---
# Prometheus-based analysis template
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: canary-analysis
  namespace: production
spec:
  args:
    - name: service-name
  
  metrics:
    - name: error-rate
      interval: 1m
      count: 5          # Must pass 5 consecutive checks
      successCondition: result[0] < 0.01   # <1% error rate
      failureLimit: 1
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{
              service="{{ args.service-name }}",
              status=~"5.."
            }[2m])) /
            sum(rate(http_requests_total{
              service="{{ args.service-name }}"
            }[2m]))
    
    - name: p99-latency
      interval: 1m
      count: 5
      successCondition: result[0] < 500    # <500ms p99
      failureLimit: 1
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            histogram_quantile(0.99,
              rate(http_request_duration_seconds_bucket{
                service="{{ args.service-name }}"
              }[2m])
            ) * 1000
    
    - name: success-rate
      interval: 1m
      count: 5
      successCondition: result[0] > 0.95   # >95% success
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{
              service="{{ args.service-name }}",
              status=~"2.."
            }[2m])) /
            sum(rate(http_requests_total{
              service="{{ args.service-name }}"
            }[2m]))
```

### Nginx + Lua Canary (Without Istio)

```nginx
# nginx/canary.conf
upstream stable {
    server stable-service:8080;
    keepalive 32;
}

upstream canary {
    server canary-service:8080;
    keepalive 32;
}

lua_shared_dict canary_state 1m;

init_by_lua_block {
    -- Default: 5% canary traffic
    ngx.shared.canary_state:set("canary_weight", 5)
}

server {
    listen 80;
    
    location / {
        access_by_lua_block {
            local weight = ngx.shared.canary_state:get("canary_weight") or 0
            local rand = math.random(100)
            
            -- Sticky: use cookie for consistent user experience
            local cookie = ngx.var.cookie_canary_slot
            if cookie == "canary" then
                ngx.var.upstream = "canary"
                return
            elseif cookie == "stable" then
                ngx.var.upstream = "stable"
                return
            end
            
            -- Route based on weight
            if rand <= weight then
                ngx.header["Set-Cookie"] = "canary_slot=canary; Path=/; Max-Age=3600"
                ngx.var.upstream = "canary"
            else
                ngx.header["Set-Cookie"] = "canary_slot=stable; Path=/; Max-Age=3600"
                ngx.var.upstream = "stable"
            end
        }
        
        set $upstream stable;
        proxy_pass http://$upstream;
        proxy_set_header X-Canary-Slot $upstream;
    }
    
    # Admin endpoint to adjust canary weight
    location /admin/canary {
        allow 10.0.0.0/8;  # Internal only
        deny all;
        
        content_by_lua_block {
            local weight = tonumber(ngx.var.arg_weight)
            if weight and weight >= 0 and weight <= 100 then
                ngx.shared.canary_state:set("canary_weight", weight)
                ngx.say("Canary weight set to " .. weight .. "%")
            else
                ngx.say("Invalid weight")
            end
        }
    }
}
```

### Automated Promotion Script

```python
# scripts/canary_manager.py
import time
import httpx
import logging
from dataclasses import dataclass
from typing import Callable

logger = logging.getLogger(__name__)

@dataclass
class CanaryStage:
    weight_pct: int
    soak_minutes: int
    gates: list[dict]   # Each gate: {name, query, threshold, operator}

CANARY_PLAN = [
    CanaryStage(
        weight_pct=5,
        soak_minutes=10,
        gates=[
            {"name": "error_rate", "threshold": 0.01, "operator": "lt"},
            {"name": "p99_ms", "threshold": 500, "operator": "lt"},
        ]
    ),
    CanaryStage(
        weight_pct=25,
        soak_minutes=15,
        gates=[
            {"name": "error_rate", "threshold": 0.01, "operator": "lt"},
            {"name": "p99_ms", "threshold": 500, "operator": "lt"},
            {"name": "success_rate", "threshold": 0.95, "operator": "gt"},
        ]
    ),
    CanaryStage(
        weight_pct=50,
        soak_minutes=20,
        gates=[
            {"name": "error_rate", "threshold": 0.01, "operator": "lt"},
            {"name": "p99_ms", "threshold": 400, "operator": "lt"},
            {"name": "success_rate", "threshold": 0.97, "operator": "gt"},
        ]
    ),
    CanaryStage(weight_pct=100, soak_minutes=0, gates=[]),
]

class CanaryManager:
    def __init__(self, prometheus_url: str, set_weight_fn: Callable[[int], None]):
        self.prometheus = prometheus_url
        self.set_weight = set_weight_fn
    
    def query_metric(self, query: str) -> float:
        r = httpx.get(
            f"{self.prometheus}/api/v1/query",
            params={"query": query},
            timeout=10
        )
        result = r.json()["data"]["result"]
        if not result:
            return 0.0
        return float(result[0]["value"][1])
    
    def check_gate(self, gate: dict, canary_label: str) -> bool:
        queries = {
            "error_rate": f'sum(rate(http_requests_total{{slot="{canary_label}",status=~"5.."}}[5m])) / sum(rate(http_requests_total{{slot="{canary_label}"}}[5m]))',
            "p99_ms": f'histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{{slot="{canary_label}"}}[5m])) * 1000',
            "success_rate": f'sum(rate(http_requests_total{{slot="{canary_label}",status=~"2.."}}[5m])) / sum(rate(http_requests_total{{slot="{canary_label}"}}[5m]))',
        }
        
        query = queries.get(gate["name"])
        if not query:
            logger.warning(f"Unknown gate metric: {gate['name']}")
            return True
        
        value = self.query_metric(query)
        threshold = gate["threshold"]
        op = gate["operator"]
        
        if op == "lt":
            passed = value < threshold
        elif op == "gt":
            passed = value > threshold
        else:
            passed = False
        
        logger.info(f"Gate {gate['name']}: {value:.4f} {'<' if op=='lt' else '>'} {threshold} → {'✅ PASS' if passed else '❌ FAIL'}")
        return passed
    
    def run(self, canary_label: str = "canary"):
        logger.info("Starting canary rollout")
        
        for stage in CANARY_PLAN:
            logger.info(f"Setting canary weight to {stage.weight_pct}%")
            self.set_weight(stage.weight_pct)
            
            if stage.soak_minutes > 0:
                logger.info(f"Soaking for {stage.soak_minutes} minutes...")
                time.sleep(stage.soak_minutes * 60)
            
            # Check all gates
            all_passed = all(
                self.check_gate(gate, canary_label)
                for gate in stage.gates
            )
            
            if not all_passed:
                logger.error(f"Gate check failed at {stage.weight_pct}% — rolling back!")
                self.set_weight(0)  # All traffic back to stable
                raise RuntimeError(f"Canary rollback triggered at {stage.weight_pct}%")
            
            logger.info(f"All gates passed at {stage.weight_pct}% ✅")
        
        logger.info("Canary promotion complete — 100% traffic on new version")
```

## Rules

- **Start small** — 1-5% first; a bug affecting 1% is far better than one affecting 100%.
- **Sticky sessions** — route the same user to the same slot throughout their session.
- **Compare against stable, not absolute** — a canary error rate of 0.5% is fine if stable is 0.4%; alarming if stable is 0.1%.
- **Automated rollback, not manual** — humans are too slow; thresholds must trigger automatic rollback.
- **Enough volume before promoting** — statistical significance requires sufficient requests at each stage.
- **Isolate canary metrics** — label/tag canary traffic separately so you can measure it independently.
- **Never canary database migrations** — schema changes are not reversible; deploy them separately with backward compatibility.
- **Time + metrics gating** — don't promote based purely on time; metrics must also pass.
- **Communicate progress** — post to Slack/monitoring so the team knows where the rollout stands.
- **Keep stable at full scale** — don't shrink stable while canary ramps; you need rollback capacity.
