---
name: tpl-devops-cloud-run-gcp
description: Template do pack (devops/07-cloud-run-gcp.md). Orienta o agente em infra, deploy, CI/CD e operacao alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: devops/07-cloud-run-gcp.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Google Cloud Run + Cloud Build + Artifact Registry + Cloud SQL

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `devops/07-cloud-run-gcp.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Runtime:** Google Cloud Run (fully managed, HTTP/gRPC)
- **CI/CD:** Cloud Build
- **Container Registry:** Artifact Registry
- **Database:** Cloud SQL (PostgreSQL 16) via VPC connector
- **Secrets:** Secret Manager (no env var secrets hardcoded)
- **Language:** Node.js 20 / Python 3.12
- **IaC:** Terraform (google provider ~> 5.x)

---

## ARCHITECTURE RULES
1. **Stateless containers only** — Cloud Run instances can be created/destroyed at any time. No local file state.
2. **Cold start budget: < 2s** — optimize image size, avoid heavy init. Use `min-instances` for latency-sensitive services.
3. **Secrets via Secret Manager** — never set secrets as Cloud Run env vars in the console or gcloud CLI literally; reference as secret versions.
4. **Least privilege service account** — each Cloud Run service has its own SA with only the roles it needs.
5. **VPC connector for Cloud SQL** — use Private IP + VPC connector; never expose Cloud SQL on public IP.
6. **Request concurrency = 80 (default)** — tune based on load tests; CPU-bound apps: lower to 10-20.
7. **Cloud Build triggers per branch** — `main` → deploy prod, `develop` → deploy staging, PRs → build+test only.
8. **Artifact Registry tag = git sha** — never deploy `latest`; always a specific, immutable tag.

---

## DOCKERFILE (OPTIMIZED FOR CLOUD RUN)

```dockerfile
# Dockerfile
FROM node:20-slim AS base
WORKDIR /app

# Install only production OS deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

# ---- Build stage ----
FROM base AS builder
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ---- Production stage ----
FROM base AS production
ENV NODE_ENV=production \
    PORT=8080

COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

COPY --from=builder /app/dist ./dist

# Cloud Run: container must listen on $PORT (default 8080)
EXPOSE 8080

# Non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser
USER appuser

# Cloud Run sends SIGTERM; respect it
STOPSIGNAL SIGTERM

CMD ["node", "dist/server.js"]

# Image size checklist:
# - Use -slim or -alpine base
# - Multi-stage: devDependencies NOT in prod image
# - .dockerignore: node_modules, .git, tests, docs
```

---

## .DOCKERIGNORE

```
node_modules
.git
.github
*.md
tests/
coverage/
.env
.env.*
dist/     # Rebuilt in Docker
*.log
```

---

## CLOUD BUILD PIPELINE

```yaml
# cloudbuild.yaml
steps:
  # Pull cache layer (if exists)
  - name: 'gcr.io/cloud-builders/docker'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        docker pull ${_REGION}-docker.pkg.dev/$PROJECT_ID/${_REPO}/app:cache || true

  # Build image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - build
      - --target=production
      - --cache-from=${_REGION}-docker.pkg.dev/$PROJECT_ID/${_REPO}/app:cache
      - --build-arg=BUILD_DATE=$(_DATE)
      - --build-arg=GIT_SHA=$COMMIT_SHA
      - -t=${_REGION}-docker.pkg.dev/$PROJECT_ID/${_REPO}/app:$COMMIT_SHA
      - -t=${_REGION}-docker.pkg.dev/$PROJECT_ID/${_REPO}/app:cache
      - .

  # Push image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', '--all-tags', '${_REGION}-docker.pkg.dev/$PROJECT_ID/${_REPO}/app']

  # Run tests in container
  - name: '${_REGION}-docker.pkg.dev/$PROJECT_ID/${_REPO}/app:$COMMIT_SHA'
    entrypoint: 'npm'
    args: ['test', '--', '--ci']
    env:
      - 'DATABASE_URL=$$DB_URL_TEST'
    secretEnv: ['DB_URL_TEST']

  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - run
      - deploy
      - my-app
      - --image=${_REGION}-docker.pkg.dev/$PROJECT_ID/${_REPO}/app:$COMMIT_SHA
      - --region=${_REGION}
      - --platform=managed
      - --service-account=my-app-sa@$PROJECT_ID.iam.gserviceaccount.com
      - --set-secrets=DATABASE_URL=my-app-db-url:latest,JWT_SECRET=my-app-jwt:latest
      - --vpc-connector=projects/$PROJECT_ID/locations/${_REGION}/connectors/my-connector
      - --vpc-egress=private-ranges-only
      - --min-instances=1
      - --max-instances=10
      - --memory=512Mi
      - --cpu=1
      - --concurrency=80
      - --timeout=30s
      - --no-allow-unauthenticated

substitutions:
  _REGION: us-central1
  _REPO: my-app-repo

availableSecrets:
  secretManager:
    - versionName: projects/$PROJECT_ID/secrets/my-app-db-url-test/versions/latest
      env: DB_URL_TEST

options:
  logging: CLOUD_LOGGING_ONLY
  machineType: E2_HIGHCPU_8

timeout: '1200s'
```

---

## CLOUD BUILD TRIGGER (gcloud)

```bash
# Create trigger: deploy on push to main
gcloud builds triggers create cloud-source-repositories \
  --name="deploy-main" \
  --repo="my-app" \
  --branch-pattern="^main$" \
  --build-config="cloudbuild.yaml" \
  --region=us-central1 \
  --substitutions="_REGION=us-central1,_REPO=my-app-repo"

# Staging trigger (develop branch)
gcloud builds triggers create cloud-source-repositories \
  --name="deploy-staging" \
  --repo="my-app" \
  --branch-pattern="^develop$" \
  --build-config="cloudbuild.staging.yaml" \
  --region=us-central1
```

---

## IAM — LEAST PRIVILEGE SERVICE ACCOUNT

```bash
# Create dedicated SA for Cloud Run service
gcloud iam service-accounts create my-app-sa \
  --display-name="My App Cloud Run SA" \
  --project=$PROJECT_ID

SA="my-app-sa@$PROJECT_ID.iam.gserviceaccount.com"

# Access Cloud SQL via Cloud SQL Auth Proxy (preferred over direct connection)
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA" \
  --role="roles/cloudsql.client"

# Access Secret Manager secrets
gcloud secrets add-iam-policy-binding my-app-db-url \
  --member="serviceAccount:$SA" \
  --role="roles/secretmanager.secretAccessor"

# Read from GCS bucket (if needed)
gcloud storage buckets add-iam-policy-binding gs://my-app-uploads \
  --member="serviceAccount:$SA" \
  --role="roles/storage.objectUser"

# NEVER grant: roles/owner, roles/editor, roles/iam.admin
```

---

## MINIMUM INSTANCES STRATEGY
```
min-instances: 0  →  Free tier, cold starts acceptable (dev/batch jobs)
min-instances: 1  →  Paid idle, eliminates cold starts (APIs, webhooks)
min-instances: 2  →  Zero-downtime deployments (traffic splits during rollout)
min-instances: N  →  Pre-warmed for predictable traffic spikes (set via scheduler)

Cost rule: 1 min-instance ≈ $5-15/month (512Mi/1CPU).
For latency SLO < 500ms P99: always set min-instances >= 1.
```

---

## VPC CONNECTOR FOR CLOUD SQL

```bash
# Create VPC connector
gcloud compute networks vpc-access connectors create my-connector \
  --region=us-central1 \
  --subnet=my-connector-subnet \
  --subnet-project=$PROJECT_ID \
  --min-throughput=200 \
  --max-throughput=1000

# Cloud SQL: ensure private IP, remove public IP
gcloud sql instances patch my-instance \
  --no-assign-ip \
  --network=projects/$PROJECT_ID/global/networks/my-vpc

# In app: use private IP (no Cloud SQL Auth Proxy needed with private IP)
# DATABASE_URL=postgresql://user:pass@10.x.x.x:5432/mydb
```

---

## SECRET MANAGER

```bash
# Create secrets
echo -n "postgresql://user:pass@10.x.x.x:5432/mydb" | \
  gcloud secrets create my-app-db-url --data-file=-

echo -n "$(openssl rand -hex 32)" | \
  gcloud secrets create my-app-jwt --data-file=-

# Update secret (creates new version)
echo -n "new-value" | gcloud secrets versions add my-app-db-url --data-file=-

# In cloudbuild.yaml (via --set-secrets):
# DATABASE_URL=my-app-db-url:latest
# Injected as env var at Cloud Run startup — value fetched at deploy time
```

---

## CLOUD RUN DEPLOY (MANUAL GCLOUD)

```bash
# Full deploy with all production settings
gcloud run deploy my-app \
  --image=us-central1-docker.pkg.dev/$PROJECT_ID/my-app-repo/app:$GIT_SHA \
  --platform=managed \
  --region=us-central1 \
  --service-account=my-app-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-secrets="DATABASE_URL=my-app-db-url:latest,JWT_SECRET=my-app-jwt:latest" \
  --vpc-connector=my-connector \
  --vpc-egress=private-ranges-only \
  --min-instances=1 \
  --max-instances=20 \
  --memory=512Mi \
  --cpu=1 \
  --cpu-boost \                         # Extra CPU during cold start
  --concurrency=80 \
  --timeout=60s \
  --set-env-vars="NODE_ENV=production,OTEL_SERVICE_NAME=my-app" \
  --allow-unauthenticated \             # Public API; remove for internal
  --traffic=100                         # Send 100% to new revision immediately
```

---

## HEALTH CHECK ENDPOINT

```typescript
// Required for Cloud Run — responds before serving real traffic
app.get('/healthz', (req, res) => {
  // Minimal check — do NOT query DB here (Cloud Run routes traffic after this)
  res.status(200).json({ status: 'ok', timestamp: Date.now() })
})

app.get('/healthz/ready', async (req, res) => {
  // Deeper check for readiness: DB connectivity
  try {
    await db.query('SELECT 1')
    res.status(200).json({ status: 'ready' })
  } catch (err) {
    res.status(503).json({ status: 'not_ready', error: String(err) })
  }
})
```
