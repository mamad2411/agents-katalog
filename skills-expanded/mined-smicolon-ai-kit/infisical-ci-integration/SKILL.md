---
name: infisical-ci-integration
description: This skill activates when configuring CI/CD pipelines, writing GitHub Actions workflows, GitLab CI configs, Dockerfiles, Kubernetes manifests, or serverless deployment configs that need secret injection. It provides patterns for integrating Infisical into build and deployment pipelines.
---

# Infisical CI/CD Integration

Patterns for integrating Infisical secret injection into CI/CD pipelines and deployment targets.

## GitHub Actions

### Standard Pattern

```yaml
- name: Install Infisical CLI
  run: |
    curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | sudo -E bash
    sudo apt-get update && sudo apt-get install -y infisical

- name: Authenticate
  run: |
    infisical login --method=universal-auth \
      --client-id=${{ secrets.INFISICAL_UNIVERSAL_AUTH_CLIENT_ID }} \
      --client-secret=${{ secrets.INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET }}
  env:
    INFISICAL_DISABLE_UPDATE_CHECK: "true"

- name: Run with secrets
  run: infisical run --env=production -- npm run build
```

### Multi-Environment Deploy

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    steps:
      # ... install + auth steps ...
      - run: infisical run --env=staging -- npm run deploy

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      # ... install + auth steps ...
      - run: infisical run --env=production -- npm run deploy
```

### Export as Environment Variables

When tools need env vars directly (not via `infisical run`):

```yaml
- name: Export secrets
  run: |
    infisical export --env=production --format=dotenv >> $GITHUB_ENV
```

## GitLab CI

### Standard Pattern

```yaml
variables:
  INFISICAL_DISABLE_UPDATE_CHECK: "true"

.infisical-setup:
  before_script:
    - curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | bash
    - apt-get update && apt-get install -y infisical
    - infisical login --method=universal-auth
        --client-id=$INFISICAL_UNIVERSAL_AUTH_CLIENT_ID
        --client-secret=$INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET

build:
  extends: .infisical-setup
  script:
    - infisical run --env=production -- npm run build
```

### GitLab OIDC Integration

```yaml
deploy:
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://app.infisical.com
  script:
    - infisical login --method=oidc
        --machine-identity-id=$MACHINE_IDENTITY_ID
    - infisical run --env=production -- npm run deploy
```

## Docker Patterns

### Runtime Injection (Preferred)

```dockerfile
# Install CLI in the image
FROM node:20-alpine
RUN apk add --no-cache curl bash && \
    curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.rpm.sh' | bash && \
    apk add infisical

COPY . .
RUN npm ci

# Inject at runtime via entrypoint
CMD ["infisical", "run", "--env=production", "--", "node", "server.js"]
```

Run with credentials:
```bash
docker run \
  -e INFISICAL_UNIVERSAL_AUTH_CLIENT_ID=... \
  -e INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET=... \
  -e INFISICAL_DISABLE_UPDATE_CHECK=true \
  myapp
```

### Build-Time Export (When Needed)

```dockerfile
FROM node:20-alpine AS builder
RUN apk add --no-cache curl bash && \
    curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.rpm.sh' | bash && \
    apk add infisical

ARG INFISICAL_UNIVERSAL_AUTH_CLIENT_ID
ARG INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET
ENV INFISICAL_DISABLE_UPDATE_CHECK=true

RUN infisical login --method=universal-auth \
    --client-id=$INFISICAL_UNIVERSAL_AUTH_CLIENT_ID \
    --client-secret=$INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET

COPY . .
RUN infisical run --env=production -- npm run build

# Clean image - no CLI, no secrets
FROM node:20-alpine
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### Docker Compose

```yaml
services:
  app:
    build: .
    environment:
      - INFISICAL_UNIVERSAL_AUTH_CLIENT_ID=${INFISICAL_UNIVERSAL_AUTH_CLIENT_ID}
      - INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET=${INFISICAL_UNIVERSAL_AUTH_CLIENT_SECRET}
      - INFISICAL_DISABLE_UPDATE_CHECK=true
    command: infisical run --env=production -- node server.js
```

Or inject before compose:
```bash
infisical run --env=dev -- docker compose up
```

## Kubernetes Patterns

### Native Kubernetes Auth

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      serviceAccountName: infisical-sa
      containers:
        - name: app
          image: myapp:latest
          env:
            - name: INFISICAL_MACHINE_IDENTITY_ID
              value: "<machine-identity-id>"
            - name: INFISICAL_DISABLE_UPDATE_CHECK
              value: "true"
          command: ["infisical", "run", "--method=kubernetes", "--env=production", "--", "node", "server.js"]
```

### Init Container Pattern

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      initContainers:
        - name: fetch-secrets
          image: infisical/cli:latest
          command:
            - sh
            - -c
            - |
              infisical login --method=kubernetes \
                --machine-identity-id=$MACHINE_IDENTITY_ID
              infisical export --env=production > /secrets/.env
          env:
            - name: MACHINE_IDENTITY_ID
              value: "<machine-identity-id>"
          volumeMounts:
            - name: secrets
              mountPath: /secrets
      containers:
        - name: app
          image: myapp:latest
          command: ["sh", "-c", "source /secrets/.env && node server.js"]
          volumeMounts:
            - name: secrets
              mountPath: /secrets
              readOnly: true
      volumes:
        - name: secrets
          emptyDir:
            medium: Memory
```

## Serverless Patterns

### Vercel

```bash
# Export secrets to Vercel environment
infisical export --env=production --format=dotenv | while IFS='=' read -r key value; do
  vercel env add "$key" production <<< "$value"
done
```

### AWS Lambda

```bash
# Update Lambda env vars
infisical export --env=production --format=json | \
  aws lambda update-function-configuration \
    --function-name myfunction \
    --environment "Variables=$(cat)"
```

### Cloudflare Workers

```bash
# Set wrangler secrets
infisical export --env=production --format=dotenv | while IFS='=' read -r key value; do
  echo "$value" | wrangler secret put "$key"
done
```

## Security Best Practices

1. **Separate identities per environment** - staging CI should NOT access production
2. **Minimal scope** - grant only the environments and folders needed
3. **Set `INFISICAL_DISABLE_UPDATE_CHECK=true`** in all CI environments
4. **Never log secrets** - use `--silent` flag when listing secrets in CI
5. **Rotate credentials** on a schedule (90 days recommended)
6. **Use OIDC** when available (GitLab, GitHub) to avoid long-lived credentials
7. **Never bake secrets** into Docker image layers
8. **Use memory-backed volumes** for Kubernetes secret files (`emptyDir.medium: Memory`)
