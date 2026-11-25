---
name: tpl-devops-github-actions-cicd
description: Template do pack (devops/01-github-actions-cicd.md). Orienta o agente em infra, deploy, CI/CD e operacao alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: devops/01-github-actions-cicd.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: GitHub Actions CI/CD Pipeline (Docker + ECR/DockerHub + Node.js/Python)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `devops/01-github-actions-cicd.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **CI/CD:** GitHub Actions
- **Containerization:** Docker + multi-stage builds
- **Registry:** AWS ECR (or DockerHub fallback)
- **Language:** Node.js 20 / Python 3.12
- **Testing:** Jest / Pytest
- **Linting:** ESLint + Prettier / Ruff + mypy
- **Deployment target:** ECS Fargate / EC2 / Lambda

---

## WORKFLOW STRUCTURE
```
.github/
└── workflows/
    ├── ci.yml           # Lint + test on every PR
    ├── build.yml        # Docker build + push on merge to main
    ├── deploy-staging.yml
    └── deploy-prod.yml  # Manual approval gate
```

---

## ARCHITECTURE RULES
1. **CI runs on every PR** — never merge code that hasn't passed lint + test.
2. **Build only on merge to main** — do not push images from feature branches.
3. **One image, multiple tags** — tag with `git sha` + `latest` + semver if tagged release.
4. **Secrets via GitHub Secrets only** — never hardcode credentials; use `${{ secrets.KEY }}`.
5. **Cache aggressively** — npm/pip dependencies and Docker layer cache cut 60–80% of runtime.
6. **Environment protection rules** — `production` environment requires 1 reviewer approval.
7. **Reusable workflows** — extract `build-and-push` into a callable workflow; call from deploy workflows.
8. **Fail fast, explicit** — use `fail-fast: true` in matrix, set `timeout-minutes` on every job.

---

## CI WORKFLOW — LINT + TEST

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

permissions:
  contents: read
  pull-requests: write

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci --prefer-offline

      - name: Run ESLint
        run: npm run lint

      - name: Run Prettier check
        run: npm run format:check

  test:
    name: Test
    runs-on: ubuntu-24.04
    needs: lint

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports: ['5432:5432']

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
        ports: ['6379:6379']

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci --prefer-offline

      - name: Run migrations
        run: npm run db:migrate
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/testdb

      - name: Run tests
        run: npm test -- --coverage --ci
        env:
          NODE_ENV: test
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

---

## BUILD + PUSH WORKFLOW

```yaml
# .github/workflows/build.yml
name: Build & Push

on:
  push:
    branches: [main]
  workflow_call:
    outputs:
      image-tag:
        description: "Full image URI with tag"
        value: ${{ jobs.build.outputs.image-tag }}

permissions:
  id-token: write   # OIDC for AWS auth (no long-lived keys)
  contents: read

jobs:
  build:
    name: Build & Push to ECR
    runs-on: ubuntu-24.04
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: ecr-login
        uses: aws-actions/amazon-ecr-login@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ steps.ecr-login.outputs.registry }}/my-app
          tags: |
            type=sha,prefix=,format=short
            type=raw,value=latest,enable={{is_default_branch}}
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            NODE_ENV=production
            BUILD_DATE=${{ github.event.head_commit.timestamp }}
            GIT_SHA=${{ github.sha }}
```

---

## DEPLOY WORKFLOW (WITH ENVIRONMENT PROTECTION)

```yaml
# .github/workflows/deploy-prod.yml
name: Deploy Production

on:
  workflow_dispatch:
    inputs:
      image-tag:
        description: 'Image SHA tag to deploy'
        required: true

jobs:
  deploy:
    name: Deploy to Production ECS
    runs-on: ubuntu-24.04
    environment:
      name: production        # Requires reviewer approval in GitHub settings
      url: https://myapp.com

    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_PROD_ROLE_ARN }}
          aws-region: us-east-1

      - name: Download task definition
        run: |
          aws ecs describe-task-definition \
            --task-definition my-app-prod \
            --query taskDefinition > task-def.json

      - name: Update image in task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: task-def.json
          container-name: app
          image: ${{ secrets.ECR_REGISTRY }}/my-app:${{ github.event.inputs.image-tag }}

      - name: Deploy ECS service
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: my-app-prod
          cluster: production
          wait-for-service-stability: true
```

---

## CACHING STRATEGIES

```yaml
# npm cache (set in setup-node above via cache: 'npm')
# Manual cache for pip:
- name: Cache pip
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ hashFiles('**/requirements*.txt') }}
    restore-keys: pip-

# Docker layer cache uses type=gha (GitHub Actions cache) in build-push-action
# This is the most effective: saves 2-4 min on typical Node builds.
```

---

## SECRETS MANAGEMENT RULES
```
- AWS auth: Use OIDC (aws-actions/configure-aws-credentials) — NEVER store ACCESS_KEY_ID
- DB passwords: GitHub Secrets only, never in workflow YAML values
- NPM_TOKEN: Set in org-level secrets, not repo-level, to share across repos
- Rotation: Rotate secrets every 90 days; use AWS Secrets Manager for app runtime secrets
```

---

## BRANCH PROTECTION (Settings → Branches → main)
```
✅ Require PR before merging
✅ Require 1 approving review
✅ Dismiss stale reviews on new commits
✅ Require status checks: lint, test
✅ Require branches to be up to date
✅ Restrict pushes to main (no direct push)
✅ Include administrators
```

---

## PYTHON VARIANT (pip + pytest)

```yaml
  test-python:
    runs-on: ubuntu-24.04
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - run: pip install -r requirements-dev.txt

      - name: Lint with Ruff
        run: ruff check .

      - name: Type check
        run: mypy app/ --ignore-missing-imports

      - name: Run tests
        run: pytest -v --cov=app --cov-report=xml
        env:
          ENVIRONMENT: test
```
