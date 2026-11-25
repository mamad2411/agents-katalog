---
name: registry-patterns
description: "Container registry patterns: ECR lifecycle policies in Terraform, Trivy scanning in GitHub Actions, optimized multi-stage Dockerfiles and .dockerignore, Cosign verification with the Kubernetes policy controller, image tag strategy, and SBOM generation with Syft. Use when securing or maintaining a container image supply chain."
---

# Registry Patterns

Container registry patterns: ECR lifecycle policies, Trivy scanning in CI, Cosign keyless signing, multi-arch builds.

## ECR Lifecycle Policy (Terraform)

```hcl
resource "aws_ecr_repository" "app" {
  name                 = "myapp"
  image_tag_mutability = "IMMUTABLE"   # Prevents tag overwrite -- critical for prod

  image_scanning_configuration {
    scan_on_push = true   # Triggers AWS Inspector scan on push
  }

  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = aws_kms_key.ecr.arn
  }
}

resource "aws_ecr_lifecycle_policy" "app" {
  repository = aws_ecr_repository.app.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Expire untagged images after 7 days"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "days"
          countNumber = 7
        }
        action = { type = "expire" }
      },
      {
        rulePriority = 2
        description  = "Keep last 20 semver tags"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 20
        }
        action = { type = "expire" }
      },
      {
        rulePriority = 3
        description  = "Keep last 5 SHA tags"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["sha-"]
          countType     = "imageCountMoreThan"
          countNumber   = 5
        }
        action = { type = "expire" }
      }
    ]
  })
}

# Cross-region replication for DR
resource "aws_ecr_replication_configuration" "main" {
  replication_configuration {
    rule {
      destination {
        region      = "us-west-2"
        registry_id = data.aws_caller_identity.current.account_id
      }
      repository_filter {
        filter      = "myapp"
        filter_type = "PREFIX_MATCH"
      }
    }
  }
}
```

## Trivy in GitHub Actions CI

```yaml
# .github/workflows/build.yml
name: Build and Scan
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read
  security-events: write   # For SARIF upload to GitHub Security tab
  id-token: write          # For OIDC Cosign signing

jobs:
  build-scan-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/GHADeployRole
          aws-region: us-east-1

      - name: Login to ECR
        id: ecr-login
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build image (no push yet)
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          load: false
          push: false
          cache-from: type=gha
          cache-to: type=gha,mode=max
          tags: ${{ steps.ecr-login.outputs.registry }}/myapp:${{ github.sha }}
          outputs: type=docker,dest=/tmp/myapp.tar

      - name: Load image for scanning
        run: docker load -i /tmp/myapp.tar

      - name: Scan with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ steps.ecr-login.outputs.registry }}/myapp:${{ github.sha }}
          format: sarif
          output: trivy-results.sarif
          severity: HIGH,CRITICAL
          exit-code: '1'           # Fail build on HIGH/CRITICAL
          ignore-unfixed: true     # Skip vulns with no fix available

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: trivy-results.sarif

      - name: Push to ECR
        if: github.ref == 'refs/heads/main'
        uses: docker/build-push-action@v5
        id: build-push
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ${{ steps.ecr-login.outputs.registry }}/myapp:${{ github.sha }}
            ${{ steps.ecr-login.outputs.registry }}/myapp:main-latest
          cache-from: type=gha

      - name: Sign image with Cosign (keyless)
        if: github.ref == 'refs/heads/main'
        run: |
          cosign sign --yes \
            ${{ steps.ecr-login.outputs.registry }}/myapp@${{ steps.build-push.outputs.digest }}
        env:
          COSIGN_EXPERIMENTAL: "1"
```

## Optimized Multi-Stage Dockerfile

```dockerfile
# syntax=docker/dockerfile:1.6

# Stage 1: Dependencies (cached separately from source)
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
# BuildKit cache mount: npm cache survives across builds
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Stage 2: Build (includes devDependencies)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN npm run build

# Stage 3: Runtime (minimal, no build tools)
FROM node:20-alpine AS runner
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 --ingroup nodejs nextjs

# Copy only production artifacts
COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000
ENV PORT=3000 \
    NODE_ENV=production

# Use exec form (PID 1, receives signals correctly)
ENTRYPOINT ["node", "dist/server.js"]
```

## .dockerignore Optimization

```
# .dockerignore
# Prevent large/sensitive directories from entering build context
node_modules/
.git/
.github/
dist/
build/
coverage/
.env
.env.*
!.env.example     # Keep the example file
*.log
.DS_Store
Thumbs.db

# Test files not needed in image
**/*.test.ts
**/*.spec.ts
**/__tests__/
jest.config.*
.eslintrc*
.prettierrc*
docs/
```

## Cosign Verification in Kubernetes (Policy Controller)

```yaml
# Sigstore Policy Controller: enforce signed images in production namespace
apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: require-signed-images
spec:
  images:
    - glob: "123456789.dkr.ecr.us-east-1.amazonaws.com/**"
  authorities:
    - keyless:
        url: https://fulcio.sigstore.dev
        identities:
          - issuer: https://token.actions.githubusercontent.com
            subjectRegExp: "https://github.com/myorg/.*"
```

## Image Tag Strategy

```
Production deployments: immutable tag
├── Semver release: v1.2.3  (from git tag)
├── SHA pinned:     sha-a1b2c3d  (from git commit)
└── Never: latest, main, branch names (mutable)

Staging/dev deployments: mutable OK
├── Branch: main-latest, feature-xyz-latest
└── PR preview: pr-123-latest
```

## SBOM Generation with Syft

```bash
# Generate SBOM during build
syft packages myapp:latest \
  --output cyclonedx-json=sbom.json \
  --output spdx-json=sbom.spdx.json

# Attach SBOM as OCI artifact alongside image
cosign attach sbom \
  --sbom sbom.spdx.json \
  --type spdx \
  myregistry/myapp:v1.2.3

# Scan SBOM with Grype (faster than full image scan after first build)
grype sbom:./sbom.json --fail-on high
```
