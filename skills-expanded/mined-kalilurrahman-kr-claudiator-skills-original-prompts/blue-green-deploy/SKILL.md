---
name: blue-green-deploy
description: Implement blue-green deployment strategy for zero-downtime releases with instant rollback capability. Outputs infrastructure configuration, traffic switching scripts, health check validation, and rollback procedures.
argument-hint: [infrastructure platform, load balancer type, database migration strategy, rollback SLA]
allowed-tools: Read, Write, Bash
---

# Blue-Green Deployment

Blue-green deployment maintains two identical production environments. One (blue) serves live traffic; the other (green) receives the new version. Traffic switches instantly when green is validated — and rollback is equally instant.

## Process

1. **Provision green environment** — identical to blue, scaled to full production capacity.
2. **Deploy new version to green** — application code, config, dependencies.
3. **Run database migrations** — must be backward compatible (both blue and green must work during switch).
4. **Validate green** — health checks, smoke tests, synthetic traffic.
5. **Switch traffic** — update load balancer/DNS to point at green.
6. **Monitor** — watch error rates, latency, business metrics for 15-30 minutes.
7. **Decommission blue** — after confidence period, scale down old environment.
8. **On failure: flip back to blue** — rollback in seconds, not minutes.

## Output Format

### Kubernetes Blue-Green

```yaml
# k8s/blue-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  namespace: production
  labels:
    app: myapp
    slot: blue
    version: "1.4.2"
spec:
  replicas: 10
  selector:
    matchLabels:
      app: myapp
      slot: blue
  template:
    metadata:
      labels:
        app: myapp
        slot: blue
        version: "1.4.2"
    spec:
      containers:
        - name: myapp
          image: myapp:1.4.2
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            periodSeconds: 10
---
# k8s/green-deployment.yaml — new version
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
  namespace: production
  labels:
    app: myapp
    slot: green
    version: "1.5.0"
spec:
  replicas: 10   # Same scale as blue
  selector:
    matchLabels:
      app: myapp
      slot: green
  template:
    metadata:
      labels:
        app: myapp
        slot: green
        version: "1.5.0"
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
            initialDelaySeconds: 10
            periodSeconds: 5
---
# k8s/service.yaml — the traffic switch
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: production
spec:
  selector:
    app: myapp
    slot: blue    # ← Change this to switch traffic
  ports:
    - port: 80
      targetPort: 8080
```

```bash
#!/bin/bash
# scripts/blue-green-switch.sh

set -euo pipefail

NAMESPACE="production"
SERVICE="myapp"
NEW_SLOT="${1:-green}"   # Default: promote green

# Determine current and new slot
CURRENT_SLOT=$(kubectl get service $SERVICE -n $NAMESPACE \
  -o jsonpath='{.spec.selector.slot}')

echo "Current: $CURRENT_SLOT → Switching to: $NEW_SLOT"

# Validate new slot is ready
echo "Validating $NEW_SLOT deployment..."
kubectl rollout status deployment/myapp-$NEW_SLOT -n $NAMESPACE --timeout=5m

# Check all pods are ready
READY=$(kubectl get deployment myapp-$NEW_SLOT -n $NAMESPACE \
  -o jsonpath='{.status.readyReplicas}')
DESIRED=$(kubectl get deployment myapp-$NEW_SLOT -n $NAMESPACE \
  -o jsonpath='{.spec.replicas}')

if [ "$READY" != "$DESIRED" ]; then
  echo "❌ Not all pods ready: $READY/$DESIRED"
  exit 1
fi

# Run smoke tests against new slot before switching
echo "Running smoke tests against $NEW_SLOT..."
NEW_SLOT_IP=$(kubectl get pods -n $NAMESPACE -l slot=$NEW_SLOT \
  -o jsonpath='{.items[0].status.podIP}')

if ! curl -sf "http://$NEW_SLOT_IP:8080/health/ready" > /dev/null; then
  echo "❌ Smoke test failed"
  exit 1
fi

echo "✅ Smoke tests passed. Switching traffic..."

# Atomic traffic switch
kubectl patch service $SERVICE -n $NAMESPACE \
  -p "{\"spec\":{\"selector\":{\"slot\":\"$NEW_SLOT\"}}}"

echo "✅ Traffic switched to $NEW_SLOT"
echo "Monitor: kubectl logs -l slot=$NEW_SLOT -n $NAMESPACE --tail=50 -f"
echo "Rollback: $0 $CURRENT_SLOT"
```

### AWS Blue-Green (ALB Target Groups)

```python
# scripts/aws_blue_green.py
import boto3
import time
import sys

def switch_traffic(
    load_balancer_arn: str,
    listener_arn: str,
    new_target_group_arn: str,
    rollback_target_group_arn: str,
    health_check_url: str,
):
    elbv2 = boto3.client('elbv2')
    
    print(f"Validating new target group...")
    # Wait for new targets to be healthy
    waiter = elbv2.get_waiter('target_in_service')
    waiter.wait(
        TargetGroupArn=new_target_group_arn,
        WaiterConfig={'Delay': 10, 'MaxAttempts': 30}
    )
    print("✅ New targets healthy")
    
    # Get current rule
    rules = elbv2.describe_rules(ListenerArn=listener_arn)['Rules']
    default_rule = next(r for r in rules if r['IsDefault'])
    rule_arn = default_rule['RuleArn']
    
    print("Switching traffic...")
    elbv2.modify_rule(
        RuleArn=rule_arn,
        Actions=[{
            'Type': 'forward',
            'TargetGroupArn': new_target_group_arn,
        }]
    )
    
    print("✅ Traffic switched. Monitoring for 60 seconds...")
    
    # Post-switch health monitoring
    import httpx
    errors = 0
    for i in range(12):  # 12 × 5s = 60s
        time.sleep(5)
        try:
            r = httpx.get(health_check_url, timeout=5)
            if r.status_code != 200:
                errors += 1
                print(f"  ⚠️  Health check returned {r.status_code}")
            else:
                print(f"  ✅ Health check OK ({i+1}/12)")
        except Exception as e:
            errors += 1
            print(f"  ❌ Health check failed: {e}")
    
    if errors > 2:
        print(f"❌ {errors} health check failures — rolling back!")
        elbv2.modify_rule(
            RuleArn=rule_arn,
            Actions=[{
                'Type': 'forward',
                'TargetGroupArn': rollback_target_group_arn,
            }]
        )
        print("✅ Rolled back to previous version")
        sys.exit(1)
    
    print("✅ Blue-green switch successful")


if __name__ == "__main__":
    switch_traffic(
        load_balancer_arn=os.environ["ALB_ARN"],
        listener_arn=os.environ["LISTENER_ARN"],
        new_target_group_arn=os.environ["GREEN_TG_ARN"],
        rollback_target_group_arn=os.environ["BLUE_TG_ARN"],
        health_check_url="https://api.example.com/health",
    )
```

### Database Migration Strategy

```sql
-- Blue-green requires BACKWARD COMPATIBLE migrations
-- Both blue (old) and green (new) run simultaneously during switch

-- ✅ SAFE: Add nullable column (old version ignores it)
ALTER TABLE orders ADD COLUMN discount_code VARCHAR(50) NULL;

-- ✅ SAFE: Add index (non-blocking in Postgres with CONCURRENTLY)
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);

-- ❌ UNSAFE: Drop column (old version still reads it)
-- ALTER TABLE orders DROP COLUMN old_field;
-- → Do in a LATER deploy, after old version is fully gone

-- ❌ UNSAFE: Rename column (old version uses old name)
-- ALTER TABLE orders RENAME COLUMN user_id TO customer_id;
-- → Add new column, backfill, dual-write, then drop old in next deploy

-- Migration phases for rename:
-- Deploy N:   Add new column, dual-write in code
-- Deploy N+1: Read from new column, stop writing old
-- Deploy N+2: Drop old column
```

## Rules

- **Green must match blue's scale** — don't validate on 1 replica then switch to receive 100% of traffic.
- **Database migrations must be backward compatible** — both slots run simultaneously during the switch window.
- **Automated rollback** — if post-switch health checks fail, flip back without human intervention.
- **Keep blue alive for 30+ minutes** — don't tear down old environment until you're confident in new.
- **Traffic switch ≠ deployment** — deploy to green first, validate, then switch separately.
- **Monitor during and after switch** — error rate and latency changes are your primary signals.
- **Test rollback regularly** — practice rollback in staging so it's not the first time in production.
- **Session/state during switch** — stateless services switch cleanly; sticky sessions complicate the picture.
