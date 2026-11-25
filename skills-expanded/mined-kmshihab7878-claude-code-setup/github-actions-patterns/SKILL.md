---
name: github-actions-patterns
description: Production GitHub Actions CI/CD patterns for Python/TS monorepos with security scanning, testing, and deployment gates
triggers:
  - github actions
  - ci/cd
  - ci pipeline
  - continuous integration
  - workflow
  - deploy pipeline
---

# GitHub Actions Patterns

Production-ready CI/CD patterns for Python/TypeScript projects. Covers testing, security scanning, deployment gates, and cost optimization.

## Standard Python CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/ruff-action@v3

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - run: pip install pyright
      - run: pyright src/

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_coremind
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements*.txt') }}
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest tests/ --cov=src/coremind --cov-report=xml -v
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_coremind
      - uses: codecov/codecov-action@v4
        with:
          file: coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Gitleaks secret scan
        uses: gitleaks/gitleaks-action@v2
      - name: Trivy vulnerability scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          severity: HIGH,CRITICAL
          exit-code: 1
      - name: Semgrep SAST
        uses: semgrep/semgrep-action@v1
        with:
          config: auto
```

## Docker Build and Push

```yaml
  build:
    needs: [lint, typecheck, test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-arn: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1
      - uses: aws-actions/amazon-ecr-login@v2
        id: ecr
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.ecr.outputs.registry }}/coremind:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Terraform Plan on PR

```yaml
# .github/workflows/terraform.yml
name: Terraform
on:
  pull_request:
    paths: [terraform/**]

jobs:
  plan:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
        working-directory: terraform/
      - run: terraform plan -no-color -out=tfplan
        working-directory: terraform/
        id: plan
      - uses: actions/github-script@v7
        with:
          script: |
            const output = `#### Terraform Plan
            \`\`\`
            ${{ steps.plan.outputs.stdout }}
            \`\`\``;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });
```

## Cost Optimization Tips

- Use `concurrency` to cancel redundant runs
- Cache pip/npm dependencies aggressively
- Use `paths` filters to skip irrelevant workflows
- Use `ubuntu-latest` (cheapest runner)
- Use `act` locally to test before pushing: `act -j test`
- Use reusable workflows for shared patterns across repos

## Testing Locally with act

```bash
# Test the CI workflow locally
act -j test --secret-file .env.test

# List available workflows
act -l

# Run specific event
act pull_request
```
