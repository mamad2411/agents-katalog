---
name: gha-patterns
description: "GitHub Actions patterns: a complete container CI/CD pipeline, reusable workflows with OIDC, dependency caching, an expressions and contexts cheatsheet, self-hosted runners on Kubernetes with Actions Runner Controller, and workflow debugging techniques. Use when writing or debugging GitHub Actions workflows."
---

# GitHub Actions Patterns

Real workflow patterns: reusable workflows, OIDC auth, matrix builds, artifact caching, and security hardening.

## Complete CI/CD Pipeline for a Container App

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  packages: write          # Push to GHCR
  id-token: write          # OIDC for AWS
  security-events: write   # Upload SARIF scan results

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ─── Job 1: Test ──────────────────────────────────────────────────────
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: npm              # Built-in npm cache

      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage

      - uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  # ─── Job 2: Build and Scan ────────────────────────────────────────────
  build:
    needs: test
    runs-on: ubuntu-latest
    outputs:
      image-digest: ${{ steps.build.outputs.digest }}
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - name: Docker meta (tags and labels)
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=sha-
            type=semver,pattern={{version}}
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build image (no push yet)
        uses: docker/build-push-action@v5
        with:
          context: .
          load: true
          tags: ${{ env.IMAGE_NAME }}:scan
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Scan with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.IMAGE_NAME }}:scan
          format: sarif
          output: trivy.sarif
          severity: HIGH,CRITICAL
          exit-code: '1'
          ignore-unfixed: true

      - uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: trivy.sarif

      - name: Build and push (main only)
        id: build
        if: github.ref == 'refs/heads/main'
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ─── Job 3: Deploy (main branch only) ────────────────────────────────
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production       # Requires approval in GitHub UI
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ vars.AWS_DEPLOY_ROLE_ARN }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster prod-cluster \
            --service myapp \
            --force-new-deployment

          aws ecs wait services-stable \
            --cluster prod-cluster \
            --services myapp
```

## Reusable Workflow with OIDC

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-digest:
        required: true
        type: string
    secrets:
      aws-role-arn:
        required: true
    outputs:
      deployment-url:
        description: "Deployed service URL"
        value: ${{ jobs.deploy.outputs.url }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    outputs:
      url: ${{ steps.get-url.outputs.url }}
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.aws-role-arn }}
          aws-region: us-east-1

      - id: get-url
        run: echo "url=https://app.${{ inputs.environment }}.example.com" >> $GITHUB_OUTPUT
```

## Dependency Caching Patterns

```yaml
# Node.js: built-in setup-node cache
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: npm               # or yarn, pnpm
    cache-dependency-path: '**/package-lock.json'

# Python with pip
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: pip

# Custom cache key for complex scenarios
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/bin/
      ~/.cargo/registry/index/
      ~/.cargo/registry/cache/
      ~/.cargo/git/db/
      target/
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-cargo-

# Go modules
- uses: actions/cache@v4
  with:
    path: |
      ~/go/pkg/mod
      ~/.cache/go-build
    key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
    restore-keys: ${{ runner.os }}-go-
```

## Expressions and Contexts Cheatsheet

```yaml
# Context: github
${{ github.sha }}                    # Full commit SHA
${{ github.event.pull_request.number }}  # PR number
${{ github.ref_name }}               # Branch or tag name
${{ github.actor }}                  # User who triggered
${{ github.repository }}             # org/repo
${{ github.run_id }}                 # Unique run ID

# Context: env (set in env: block)
${{ env.MY_VAR }}

# Context: vars (organization/repo variables, non-secret)
${{ vars.DEPLOY_REGION }}

# Context: secrets
${{ secrets.MY_SECRET }}

# Context: needs (outputs from previous jobs)
${{ needs.build.outputs.image-digest }}

# Expressions
${{ github.ref == 'refs/heads/main' }}  # boolean
${{ contains(github.event.head_commit.message, '[skip ci]') }}
${{ startsWith(github.ref, 'refs/tags/v') }}
${{ format('{0}/{1}:{2}', env.REGISTRY, env.IMAGE_NAME, github.sha) }}

# Conditional steps
if: github.ref == 'refs/heads/main'
if: github.event_name == 'pull_request'
if: always()          # Run even if previous step failed
if: failure()         # Run only if a previous step failed
if: cancelled()       # Run only if workflow cancelled
```

## Self-Hosted Runner on Kubernetes (Actions Runner Controller)

```yaml
# Install ARC (Actions Runner Controller)
helm install arc \
  --namespace arc-system \
  --create-namespace \
  oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller

# Deploy ephemeral runner scale set
helm install arc-runner-set \
  --namespace arc-runners \
  --create-namespace \
  --set githubConfigUrl=https://github.com/myorg/myrepo \
  --set githubConfigSecret.github_token=${{ GITHUB_TOKEN }} \
  --set minRunners=1 \
  --set maxRunners=10 \
  oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set

# Use in workflow
jobs:
  my-job:
    runs-on: arc-runner-set  # Label matches Helm release name
```

## Workflow Debug Techniques

```bash
# Enable step debug logging
# Add secret: ACTIONS_STEP_DEBUG = true
# Add secret: ACTIONS_RUNNER_DEBUG = true

# Print all available contexts
- name: Dump contexts
  env:
    GITHUB_CONTEXT: ${{ toJson(github) }}
    RUNNER_CONTEXT: ${{ toJson(runner) }}
  run: |
    echo "GITHUB: $GITHUB_CONTEXT"
    echo "RUNNER: $RUNNER_CONTEXT"

# Check what files are in workspace
- run: find . -name "*.json" | head -20

# Inspect environment variables
- run: env | sort | grep -v SECRET
```
