---
name: ci-cd-pipeline
description: Design continuous integration and deployment pipelines. Outputs stages, testing, artifact management, deployment strategies, and rollback procedures.
argument-hint: [tech stack, deployment targets, testing requirements]
allowed-tools: Read, Write, Bash
---

# CI/CD Pipeline Design

Design production-grade CI/CD pipelines that automate testing, building, and deployment while maintaining quality and safety. Not a basic GitHub Actions workflow — multi-stage pipelines, deployment strategies, quality gates, artifact management, and disaster recovery.

## Process

1. **Map deployment flow.** Code → Build → Test → Stage → Production.
2. **Define stages.** Lint, unit tests, integration tests, security scans, build artifacts.
3. **Set quality gates.** Test coverage ≥ 80%, no critical vulnerabilities, performance benchmarks.
4. **Choose deployment strategy.** Blue-green, canary, rolling, feature flags.
5. **Plan artifact management.** Docker images, versioning, retention policy.
6. **Add monitoring.** Deployment metrics, rollback triggers, smoke tests.
7. **Document rollback.** How to revert to last known good state.

## Output Format

### CI/CD Pipeline: [Application Name]

**Platform:** GitHub Actions / GitLab CI / Jenkins  
**Deployment Targets:** Staging, Production (AWS ECS)  
**Deployment Strategy:** Canary (10% → 50% → 100%)  
**Quality Gates:** 3 (Tests, Coverage, Security)  
**Rollback Time:** < 5 minutes (automated)

---

## Pipeline Stages

### Stage 1: Lint & Format Check
**Purpose:** Catch syntax errors, enforce code style  
**Duration:** 1-2 minutes  
**Fail Fast:** Yes (no point testing broken code)

```yaml
# GitHub Actions
lint:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - run: npm ci
    - run: npm run lint
    - run: npm run format:check
```

---

### Stage 2: Unit Tests
**Purpose:** Test individual functions/modules  
**Duration:** 2-5 minutes  
**Coverage Requirement:** ≥ 80%  
**Fail Fast:** Yes

```yaml
unit-tests:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
    - run: npm ci
    - run: npm test -- --coverage
    - name: Check coverage
      run: |
        COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
        if (( $(echo "$COVERAGE < 80" | bc -l) )); then
          echo "Coverage $COVERAGE% is below 80%"
          exit 1
        fi
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

### Stage 3: Integration Tests
**Purpose:** Test component interactions  
**Duration:** 5-15 minutes  
**Infrastructure:** Docker Compose (database, Redis, etc.)

```yaml
integration-tests:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:15
      env:
        POSTGRES_PASSWORD: test
      options: >-
        --health-cmd pg_isready
        --health-interval 10s
        --health-timeout 5s
        --health-retries 5
    redis:
      image: redis:7-alpine
  steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
    - run: npm ci
    - run: npm run test:integration
      env:
        DATABASE_URL: postgresql://postgres:test@postgres:5432/test
        REDIS_URL: redis://redis:6379
```

---

### Stage 4: Security Scan
**Purpose:** Detect vulnerabilities, secrets  
**Duration:** 2-5 minutes  
**Tools:** Trivy (containers), npm audit, git-secrets

```yaml
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    
    # Dependency vulnerabilities
    - run: npm audit --audit-level=high
    
    # Secret scanning
    - name: TruffleHog
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: main
    
    # Container scanning (if building Docker)
    - name: Build image
      run: docker build -t myapp:${{ github.sha }} .
    
    - name: Trivy scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: myapp:${{ github.sha }}
        severity: 'CRITICAL,HIGH'
        exit-code: 1  # Fail if vulnerabilities found
```

---

### Stage 5: Build Artifacts
**Purpose:** Create deployable artifacts  
**Duration:** 3-10 minutes  
**Outputs:** Docker image, versioned and tagged

```yaml
build:
  needs: [lint, unit-tests, integration-tests, security]
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to ECR
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:${{ github.sha }}
          123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest
        cache-from: type=registry,ref=myapp:buildcache
        cache-to: type=registry,ref=myapp:buildcache,mode=max
```

---

### Stage 6: Deploy to Staging
**Purpose:** Test in production-like environment  
**Duration:** 2-5 minutes  
**Auto-Deploy:** On merge to `main`

```yaml
deploy-staging:
  needs: build
  runs-on: ubuntu-latest
  environment: staging
  steps:
    - name: Deploy to ECS
      run: |
        aws ecs update-service \
          --cluster myapp-staging \
          --service myapp \
          --force-new-deployment \
          --task-definition myapp:${{ github.sha }}
    
    - name: Wait for deployment
      run: |
        aws ecs wait services-stable \
          --cluster myapp-staging \
          --services myapp
    
    - name: Smoke tests
      run: |
        curl -f https://staging.myapp.com/health || exit 1
        curl -f https://staging.myapp.com/api/version || exit 1
```

---

### Stage 7: Deploy to Production
**Purpose:** Ship to users  
**Duration:** 10-30 minutes (canary rollout)  
**Trigger:** Manual approval + smoke tests pass

```yaml
deploy-production:
  needs: deploy-staging
  runs-on: ubuntu-latest
  environment:
    name: production
    url: https://myapp.com
  steps:
    # Canary deployment: 10% → 50% → 100%
    
    - name: Deploy to 10% of traffic
      run: |
        aws ecs update-service \
          --cluster myapp-prod \
          --service myapp-canary \
          --task-definition myapp:${{ github.sha }} \
          --desired-count 1  # 1 out of 10 instances
    
    - name: Wait 5 minutes, monitor metrics
      run: sleep 300
    
    - name: Check error rate
      run: |
        ERROR_RATE=$(curl -s "https://api.datadog.com/api/v1/query?query=sum:myapp.errors{*}.as_rate()" | jq '.series[0].pointlist[-1][1]')
        if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
          echo "Error rate $ERROR_RATE exceeds threshold, rolling back"
          exit 1
        fi
    
    - name: Deploy to 50%
      run: |
        aws ecs update-service \
          --cluster myapp-prod \
          --service myapp-canary \
          --desired-count 5
    
    - name: Wait 5 minutes
      run: sleep 300
    
    - name: Deploy to 100%
      run: |
        aws ecs update-service \
          --cluster myapp-prod \
          --service myapp \
          --task-definition myapp:${{ github.sha }} \
          --force-new-deployment
```

---

## Deployment Strategies

### Blue-Green Deployment

**How It Works:**
1. Spin up new environment (Green) with new version
2. Run smoke tests on Green
3. Switch load balancer from Blue to Green
4. Keep Blue running for 1 hour (quick rollback)
5. Terminate Blue

**Pros:** Zero downtime, instant rollback  
**Cons:** 2x infrastructure cost during deployment

**Implementation (AWS):**
```bash
# Deploy green environment
aws ecs create-service \
  --cluster prod \
  --service-name myapp-green \
  --task-definition myapp:v2.0.0

# Wait for healthy
aws ecs wait services-stable --cluster prod --services myapp-green

# Switch traffic (ALB target group swap)
aws elbv2 modify-listener \
  --listener-arn arn:aws:elasticloadbalancing:... \
  --default-actions TargetGroupArn=arn:...myapp-green...

# Wait 1 hour for rollback window
sleep 3600

# Terminate blue
aws ecs delete-service --cluster prod --service myapp-blue
```

---

### Canary Deployment

**How It Works:**
1. Deploy new version to 10% of servers
2. Monitor error rate, latency for 5-10 minutes
3. If metrics good, deploy to 50%
4. Monitor again
5. Deploy to 100%

**Pros:** Gradual risk reduction, early detection  
**Cons:** Longer deployment time, complex rollback

**Traffic Split (Nginx):**
```nginx
upstream myapp {
    server 10.0.1.1 weight=90;  # Old version
    server 10.0.1.2 weight=10;  # Canary (new version)
}
```

---

### Rolling Deployment

**How It Works:**
1. Update 1 instance at a time
2. Wait for health check pass
3. Move to next instance
4. Repeat until all updated

**Pros:** No extra infrastructure, gradual  
**Cons:** Mixed versions running, slower

**Implementation (Kubernetes):**
```yaml
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1  # Max 1 down at a time
      maxSurge: 1        # Max 1 extra during update
```

---

### Feature Flags (Dark Launch)

**How It Works:**
1. Deploy new code to all servers (disabled)
2. Enable for 10% of users via feature flag
3. Monitor metrics
4. Gradually increase to 100%

**Pros:** Fastest deployment, easy rollback (just toggle flag)  
**Cons:** Requires feature flag system

**Example (LaunchDarkly):**
```javascript
const showNewUI = await launchDarkly.variation('new-ui', user, false);

if (showNewUI) {
  return <NewUI />;
} else {
  return <OldUI />;
}
```

---

## Quality Gates

### Gate 1: Test Coverage
```yaml
- name: Enforce coverage
  run: |
    if [ $(cat coverage/coverage-summary.json | jq '.total.lines.pct') -lt 80 ]; then
      echo "Coverage below 80%"
      exit 1
    fi
```

### Gate 2: Performance Benchmarks
```yaml
- name: Performance test
  run: |
    # Run load test
    artillery run load-test.yml --output report.json
    
    # Check p95 latency
    P95=$(cat report.json | jq '.aggregate.latency.p95')
    if [ $P95 -gt 500 ]; then
      echo "P95 latency $P95ms exceeds 500ms threshold"
      exit 1
    fi
```

### Gate 3: Security Scan
```yaml
- name: Block on critical vulnerabilities
  run: npm audit --audit-level=critical
```

---

## Artifact Management

### Docker Image Versioning

**Tags:**
- `myapp:v1.2.3` — Semantic version
- `myapp:1a2b3c4` — Git commit SHA
- `myapp:latest` — Latest production
- `myapp:staging` — Latest staging

**Retention Policy:**
- Keep last 10 production versions
- Delete staging images after 30 days
- Keep all tags for current major version

---

## Rollback Procedures

### Automated Rollback (Error Rate Spike)

```yaml
- name: Monitor error rate
  run: |
    sleep 300  # Wait 5 minutes post-deploy
    
    ERROR_RATE=$(fetch_error_rate_from_datadog)
    
    if [ $ERROR_RATE > 0.05 ]; then
      echo "Error rate $ERROR_RATE exceeds 5%, rolling back"
      
      # Rollback to previous version
      aws ecs update-service \
        --cluster prod \
        --service myapp \
        --task-definition myapp:${{ env.PREVIOUS_VERSION }}
      
      # Notify team
      curl -X POST $SLACK_WEBHOOK \
        -d '{"text":"Auto-rollback triggered due to high error rate"}'
      
      exit 1
    fi
```

### Manual Rollback

```bash
# Find last good version
aws ecs list-task-definitions --family myapp --sort DESC

# Rollback
aws ecs update-service \
  --cluster prod \
  --service myapp \
  --task-definition myapp:v1.2.2  # Last known good
```

---

## Environment Configuration

### Environment Variables by Stage

| Variable | Dev | Staging | Production |
|----------|-----|---------|------------|
| LOG_LEVEL | debug | info | warn |
| DATABASE_URL | local | staging-db | prod-db (read replica) |
| REDIS_URL | localhost | staging-redis | prod-redis-cluster |
| SENTRY_ENV | development | staging | production |

**Implementation:**
```yaml
deploy-staging:
  environment: staging
  env:
    LOG_LEVEL: info
    DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}

deploy-production:
  environment: production
  env:
    LOG_LEVEL: warn
    DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
```

---

## Monitoring & Observability

### Deployment Metrics

Track these during deployment:
- Error rate (errors / total requests)
- Request latency (p50, p95, p99)
- Request volume
- CPU/memory usage
- Database query time

**Alert Thresholds:**
- Error rate > 1% → Investigate
- Error rate > 5% → Auto-rollback
- P95 latency > 2x baseline → Investigate

---

## Complete GitHub Actions Example

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  IMAGE_NAME: myapp

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v3
      - uses: docker/setup-buildx-action@v2
      - uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          push: true
          tags: 123456.dkr.ecr.us-east-1.amazonaws.com/myapp:${{ github.sha }}

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy
        run: |
          aws ecs update-service \
            --cluster staging \
            --service myapp \
            --force-new-deployment

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://myapp.com
    steps:
      - name: Canary deployment
        run: ./scripts/canary-deploy.sh ${{ github.sha }}
```

## Rules

- Every commit must pass all tests before merging (no "fix in next commit").
- Production deployments require manual approval gate — no auto-deploy to prod.
- Rollback procedure must be tested quarterly — if you can't roll back in 5 minutes, fix the process.
- Docker images must be tagged with Git SHA for traceability.
- Quality gates are blocking — if coverage < 80%, deployment fails.
- Monitor error rate for 5 minutes post-deploy before calling success.
- Keep last 10 production versions for quick rollback.
- Secrets must never be in code or CI config — use GitHub Secrets, AWS Secrets Manager, or Vault.
- Deployment strategy must match risk tolerance: Canary for user-facing, blue-green for critical, rolling for internal.
- Every deployment must include smoke tests (health endpoint, critical API call).
