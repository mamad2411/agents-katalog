---
name: ci-cd-advanced
description: Design advanced CI/CD patterns with deployment strategies, progressive delivery, and rollback automation. Outputs pipeline configs, canary deployments, and blue-green setups.
argument-hint: [deployment frequency, rollback requirements, team size]
allowed-tools: Read, Write, Bash
---

# Advanced CI/CD Patterns

Design production-grade CI/CD pipelines with deployment strategies. Not basic deploy scripts — canary releases, blue-green deployments, feature flags, and automatic rollbacks.

## Process

1. **Choose deployment strategy.** Blue-green, canary, rolling, recreate.
2. **Define stages.** Build, test, security scan, deploy, verify.
3. **Implement progressive delivery.** Gradual rollout with monitoring.
4. **Add safety checks.** Smoke tests, health checks, automatic rollback.
5. **Enable feature flags.** Decouple deploy from release.
6. **Configure environments.** Dev, staging, production pipelines.
7. **Monitor deployments.** Track success rate, deployment frequency, MTTR.

## Output Format

### CI/CD Pipeline: [Application]

**Strategy:** Canary deployment (10% → 50% → 100%)  
**Stages:** Build → Test → Scan → Deploy → Verify  
**Deployment Time:** 15 minutes (full rollout)  
**Rollback:** Automatic on health check failure  
**Deployment Frequency:** 20x/day

---

## Deployment Strategies

### Blue-Green Deployment

```
┌─────────────┐
│   Blue      │ ← Current version (v1.0)
│ Environment │   100% traffic
└──────┬──────┘
       │
┌──────▼──────┐
│Load Balancer│
└──────┬──────┘
       │
┌──────▼──────┐
│   Green     │ ← New version (v1.1)
│ Environment │   0% traffic (warming up)
└─────────────┘

1. Deploy v1.1 to Green
2. Run smoke tests on Green
3. Switch traffic to Green (instant cutover)
4. Keep Blue as rollback option
5. After stability, destroy Blue or use for next deploy
```

**Kubernetes Blue-Green:**
```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
      - name: app
        image: myapp:v1.0

---
# Green deployment (new)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
      - name: app
        image: myapp:v1.1

---
# Service (traffic routing)
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: myapp
    version: blue  # Switch to 'green' for cutover
  ports:
  - port: 80
```

**Cutover script:**
```bash
#!/bin/bash
# blue-green-cutover.sh

# Deploy green
kubectl apply -f deployment-green.yaml
kubectl rollout status deployment/app-green

# Smoke test
if ! curl -f http://app-green/health; then
  echo "Health check failed, aborting"
  exit 1
fi

# Switch traffic
kubectl patch service app -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor for 5 minutes
sleep 300

# Check error rate
ERROR_RATE=$(kubectl top pods | grep app-green | awk '{print $3}')
if [ "$ERROR_RATE" -gt "1" ]; then
  echo "High error rate, rolling back"
  kubectl patch service app -p '{"spec":{"selector":{"version":"blue"}}}'
  exit 1
fi

# Success, delete blue
kubectl delete deployment app-blue
```

---

### Canary Deployment

```
Step 1: 10% to canary
┌──────────────┐
│   Stable     │ ← 90% traffic
│   (v1.0)     │
└──────┬───────┘
       │
┌──────▼───────┐
│Load Balancer │
└──────┬───────┘
       │
┌──────▼───────┐
│   Canary     │ ← 10% traffic
│   (v1.1)     │
└──────────────┘

Step 2: Monitor metrics for 10 minutes
Step 3: If OK → 50% traffic
Step 4: If OK → 100% traffic
Step 5: Decommission stable
```

**Argo Rollouts (Kubernetes):**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 10   # 10% to canary
      - pause: {duration: 10m}  # Wait 10 min
      - setWeight: 50   # 50% to canary
      - pause: {duration: 10m}
      - setWeight: 100  # 100% to canary
      
      # Automatic rollback on metrics
      analysis:
        templates:
        - templateName: error-rate
        args:
        - name: service-name
          value: myapp
      
      # Traffic management
      trafficRouting:
        istio:
          virtualService:
            name: myapp-vsvc
  
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:v1.1
```

**Analysis Template:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: error-rate
    interval: 1m
    successCondition: result < 0.05  # < 5% error rate
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus:9090
        query: |
          sum(rate(http_requests_total{service="{{args.service-name}}",status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
```

---

### Rolling Deployment

```
Replace instances one-by-one

Instance 1: v1.0 → v1.1 ✓
Instance 2: v1.0 → v1.1 ✓
Instance 3: v1.0 → v1.1 ✓

Kubernetes default strategy
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1  # Max instances down at once
      maxSurge: 2        # Max extra instances during rollout
  template:
    spec:
      containers:
      - name: app
        image: myapp:v1.1
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## GitHub Actions Advanced Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix={{branch}}-
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run unit tests
        run: npm test
      
      - name: Run integration tests
        run: npm run test:integration
      
      - name: Security scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ needs.build.outputs.image-tag }}
          severity: 'CRITICAL,HIGH'

  deploy-canary:
    needs: [build, test]
    runs-on: ubuntu-latest
    environment: production-canary
    steps:
      - name: Deploy to Kubernetes (10%)
        run: |
          kubectl set image deployment/myapp-canary \
            app=${{ needs.build.outputs.image-tag }}
          kubectl rollout status deployment/myapp-canary
      
      - name: Wait for metrics
        run: sleep 600  # 10 minutes
      
      - name: Check error rate
        run: |
          ERROR_RATE=$(curl -s http://prometheus/api/v1/query?query=error_rate | jq '.data.result[0].value[1]')
          if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
            echo "Error rate too high: $ERROR_RATE"
            exit 1
          fi

  deploy-production:
    needs: deploy-canary
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp \
            app=${{ needs.build.outputs.image-tag }}
          kubectl rollout status deployment/myapp
      
      - name: Smoke test
        run: |
          curl -f https://api.example.com/health || exit 1
      
      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Deployed ${{ github.sha }} to production ✅"
            }
```

---

## Feature Flags Integration

```python
# feature_flags.py
from launchdarkly import LDClient, Config

ld_client = LDClient(config=Config(sdk_key='YOUR_SDK_KEY'))

def is_feature_enabled(feature_key, user_id):
    """Check if feature enabled for user"""
    
    user = {
        'key': user_id,
        'email': f'{user_id}@example.com'
    }
    
    return ld_client.variation(feature_key, user, default=False)

# Usage in app
@app.route('/api/new-feature')
def new_feature():
    user_id = request.headers.get('X-User-ID')
    
    if is_feature_enabled('new-checkout-flow', user_id):
        return new_checkout_flow()
    else:
        return old_checkout_flow()
```

**Gradual rollout:**
```
Day 1: Enable for 1% of users
Day 2: Monitor metrics, increase to 10%
Day 3: Increase to 50%
Day 4: Increase to 100%
```

---

## Automatic Rollback

```yaml
# GitLab CI with automatic rollback
deploy_production:
  stage: deploy
  script:
    - kubectl apply -f k8s/deployment.yaml
    - kubectl rollout status deployment/myapp
    
    # Smoke test
    - |
      if ! curl -f https://api.example.com/health; then
        echo "Health check failed, rolling back"
        kubectl rollout undo deployment/myapp
        exit 1
      fi
    
    # Monitor error rate for 5 minutes
    - |
      for i in {1..5}; do
        ERROR_RATE=$(curl -s http://prometheus/api/v1/query?query=error_rate | jq -r '.data.result[0].value[1]')
        if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
          echo "Error rate too high: $ERROR_RATE, rolling back"
          kubectl rollout undo deployment/myapp
          exit 1
        fi
        sleep 60
      done
  
  environment:
    name: production
    on_stop: rollback_production

rollback_production:
  stage: deploy
  script:
    - kubectl rollout undo deployment/myapp
  when: manual
  environment:
    name: production
    action: stop
```

---

## Multi-Environment Pipeline

```yaml
# Separate pipelines for each environment

.deploy_template: &deploy_template
  stage: deploy
  script:
    - helm upgrade --install myapp ./chart \
        --set image.tag=$CI_COMMIT_SHA \
        --set env=$ENVIRONMENT \
        --namespace $NAMESPACE

deploy_dev:
  <<: *deploy_template
  variables:
    ENVIRONMENT: dev
    NAMESPACE: development
  only:
    - branches
  except:
    - main

deploy_staging:
  <<: *deploy_template
  variables:
    ENVIRONMENT: staging
    NAMESPACE: staging
  only:
    - main
  when: on_success

deploy_production:
  <<: *deploy_template
  variables:
    ENVIRONMENT: production
    NAMESPACE: production
  only:
    - main
  when: manual  # Require approval
  needs:
    - deploy_staging
```

---

## Deployment Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Metrics
deployments_total = Counter(
    'deployments_total',
    'Total deployments',
    ['environment', 'status']  # success/failure
)

deployment_duration = Histogram(
    'deployment_duration_seconds',
    'Deployment duration',
    ['environment']
)

canary_error_rate = Gauge(
    'canary_error_rate',
    'Error rate during canary',
    ['version']
)

# Record deployment
def record_deployment(environment, success, duration):
    status = 'success' if success else 'failure'
    deployments_total.labels(environment=environment, status=status).inc()
    deployment_duration.labels(environment=environment).observe(duration)
```

**DORA Metrics Dashboard:**
```promql
# Deployment Frequency
rate(deployments_total{status="success"}[7d])

# Lead Time for Changes
# (time from commit to deploy)
histogram_quantile(0.95, deployment_duration_seconds_bucket)

# Change Failure Rate
sum(deployments_total{status="failure"})
/
sum(deployments_total)

# Mean Time to Recover (MTTR)
avg(time_to_recovery_seconds)
```

---

## Progressive Delivery with Flagger

```yaml
# Flagger canary with automated analysis
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  
  service:
    port: 80
  
  analysis:
    interval: 1m
    threshold: 10  # Max failed checks
    maxWeight: 50  # Max canary weight
    stepWeight: 10 # Increase by 10% each step
    
    metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99  # 99% success rate required
      interval: 1m
    
    - name: request-duration
      thresholdRange:
        max: 500  # p99 latency < 500ms
      interval: 1m
    
    webhooks:
    - name: load-test
      url: http://flagger-loadtester/
      timeout: 5s
      metadata:
        cmd: "hey -z 1m -q 10 -c 2 http://myapp-canary/"
```

## Rules

- Blue-green for zero-downtime critical systems — instant rollback, full testing before cutover.
- Canary for gradual risk mitigation — catch issues affecting <10% users before full rollout.
- Feature flags decouple deploy from release — ship code off, turn on for specific users.
- Smoke tests after every deploy — basic health check prevents broken deployments reaching users.
- Automatic rollback on metric degradation — error rate, latency thresholds trigger rollback.
- Separate pipelines for each environment — dev auto-deploys, staging gates production, production requires approval.
- Monitor deployments for 5-10 minutes — initial success doesn't mean stable, watch for delayed failures.
- Track DORA metrics (deployment frequency, lead time, MTTR, change failure rate) — measure CI/CD effectiveness.
- Progressive delivery with analysis templates — automated decision to proceed or rollback based on metrics.
- Keep previous version running during deploy — rolling updates, blue-green, or canary all maintain availability.
