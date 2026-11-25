---
name: deploy-staging
description: Use this skill when deploying a completed feature to staging for smoke-testing and verification before a production release — the deploy-to-staging workflow that builds, deploys to a staging environment, runs smoke tests, and verifies.
disable-model-invocation: true
argument-hint: [service-name]
---

# Deploy to Staging

Structured workflow for deploying to staging environment. Builds the application, deploys, runs smoke tests, and verifies the deployment.

## 0. Detect controller / preview-env tooling — route first

Before running an imperative `helm upgrade` / `kubectl apply` against staging, check whether the cluster has a controller-driven flow.

| Marker | Implication |
|---|---|
| `Application` / `Kustomization` CRDs (Argo CD / Flux) | Push manifest changes to the staging git path; controller reconciles. See `/deploy-production` Step 0a for details. |
| `ApplicationSet` with `pullRequest` generator | Argo CD per-PR ephemeral environments — staging deploy creates a per-PR namespace automatically on PR open. |
| `vcluster` config or Loft `Space` CRDs | [Loft / vCluster](https://www.vcluster.com) — virtual ephemeral staging clusters per branch. |
| `tilt.yaml` (root) | [Tilt](https://tilt.dev) — local dev loop; staging usually still flows through Argo CD/Flux. |

Use the cloud-platforms skill for platform-specific kubectl/helm context (GKE/AKS/EKS).

For supply-chain integrity — staging is the natural validation gate for image signing (Cosign sign + verify), SBOM generation (Syft → CycloneDX), and SLSA provenance attestation. If the project ships any of these in CI, verify they ran successfully on the staging artefact before promoting to production.

## 1. Pre-Deployment Checks

### 1a. Verify Branch State

```
// turbo
git branch --show-current
```

```
// turbo
git status --short
```

- Working directory must be clean
- Branch should be `main` or a release branch

### 1b. Run Tests

Invoke `/run-tests` sub-workflow. All tests must pass before deploying.

### 1c. Identify Deployment Method

Read `CLAUDE.md` and project config to determine:

| Signal | Method |
|---|---|
| `Dockerfile` + K8s manifests | Container → Kubernetes |
| `Dockerfile` + `docker-compose` | Container → Docker Compose |
| Helm charts | Container → Helm |
| Terraform | Infrastructure as Code |
| Serverless config (serverless.yml, SAM) | Serverless deployment |
| Static site (Next.js, Vite) | CDN / static hosting |
| Platform config (Netlify, Vercel, Railway) | Platform deployment |

## 2. Build

Build the application artifact:

| Stack | Command |
|---|---|
| Node.js | `npm run build` or `pnpm build` |
| Java | `./mvnw clean package -DskipTests` |
| Python | `docker build -t <image>:<tag> .` |
| Go | `go build -o bin/app ./cmd/api` |
| .NET | `dotnet publish -c Release` |

### Container Build (if applicable)

```
docker build -t <registry>/<image>:<tag> .
```

Tag with git SHA or version:
```
docker tag <image> <registry>/<image>:<git-sha>
```

## 3. Deploy to Staging

**⚠️ Present deployment plan and request APPROVE before executing.**

### 3a. Kubernetes / Helm

```
helm upgrade --install <release> <chart> \
  -n staging \
  -f values-staging.yaml \
  --set image.tag=<tag> \
  --dry-run
```

After APPROVE:
```
helm upgrade --install <release> <chart> \
  -n staging \
  -f values-staging.yaml \
  --set image.tag=<tag>
```

### 3b. Docker Compose

```
docker compose -f docker-compose.staging.yml up -d
```

### 3c. Platform (Netlify, Vercel, etc.)

Follow platform-specific CLI or git-based deployment.

## 4. Verify Deployment

### 4a. Health Check

```
// turbo
kubectl get pods -n staging -o wide
```

Or curl health endpoint:
```
curl -s <staging-url>/health
```

### 4b. Smoke Tests

Run critical path smoke tests:
- Application starts and responds
- Health endpoint returns 200
- Authentication flow works
- Core API endpoints respond correctly
- Database connectivity verified

### 4c. Monitor Logs

```
// turbo
kubectl logs -n staging -l app=<app-name> --tail=50
```

Check for errors, warnings, or unexpected behavior in the first 2–5 minutes.

## 5. Memory Write (L4)

Append a deploy event to `.ai-skills-memory/runs.jsonl` per `memory-discipline.md` retention rules:

```json
{"ts": "<ISO8601>", "event": "deploy", "env": "staging", "service": "<name>", "version": "<tag>", "method": "k8s|helm|docker|platform", "status": "success|fail", "duration_ms": N, "rollback": false}
```

## 6. Summary

```
## Staging Deployment Summary
- **Version**: [version/tag]
- **Branch**: [branch name]
- **Environment**: staging
- **Method**: [K8s/Helm/Docker/Platform]
- **Build**: [success/fail]
- **Deploy**: [success/fail]
- **Health check**: [pass/fail]
- **Smoke tests**: [pass/fail]
- **Staging URL**: [url]
- **Next steps**: [QA testing / production deploy]
```

If all checks pass, suggest:
- Run full QA testing on staging
- When ready: `/deploy-production`

## Integration

- **Preceded by**: `/pre-commit`, `/create-pr` (code ready)
- **Followed by**: `/deploy-production`
- **Roles**: `Agent(devops-engineer)`, `Agent(devops-architect)` (deployment strategy design)
- **Memory writes**: L4 `runs.jsonl` (deploy event per Step 5)
