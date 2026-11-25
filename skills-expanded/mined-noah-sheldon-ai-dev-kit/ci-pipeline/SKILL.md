---
name: ci-pipeline
description: GitHub Actions, Jenkins pipelines, PR automation, and quality gates.
origin: AI Dev Kit
---

# CI Pipeline

Build, test, scan, and deploy with GitHub Actions, Jenkins, and PR automation.

## When to Use

- Writing or updating GitHub Actions workflows
- Creating Jenkins pipelines (declarative or scripted)
- Adding PR quality gates (tests, linting, coverage)
- Configuring branch protection and required checks
- Setting up deployment environments and promotion

## GitHub Actions

### Standard Python Workflow

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('**/requirements.txt') }}
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: pytest --cov=src --cov-report=xml --cov-fail-under=80
      - uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy src/
```

### Standard Next.js/TypeScript Workflow

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm test -- --coverage
      - run: npm run build
```

### Multi-Stage Deploy Workflow

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with:
          registry: ${{ secrets.ECR_REGISTRY }}
          username: ${{ secrets.AWS_ACCESS_KEY_ID }}
          password: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ secrets.ECR_REGISTRY }}/app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-and-push
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v3
      - run: kubectl set image deployment/app app=${{ secrets.ECR_REGISTRY }}/app:${{ github.sha }}

  deploy-prod:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: ArgoCD/argo-cd-actions@v1
        with:
          server: ${{ secrets.ARGOCD_SERVER }}
          token: ${{ secrets.ARGOCD_TOKEN }}
          application: app-prod
          command: sync
```

### Reusable Workflow

```yaml
# .github/workflows/test-python.yml
on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
      coverage-threshold:
        type: number
        default: 80

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=src --cov-report=xml --cov-fail-under=${{ inputs.coverage-threshold }}
```

```yaml
# Usage in another workflow
jobs:
  test-311:
    uses: ./.github/workflows/test-python.yml
    with:
      python-version: "3.11"
```

## Jenkins Pipeline

### Declarative Pipeline

```groovy
pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.12'
        COVERAGE_THRESHOLD = '80'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install') {
            steps {
                sh "python${PYTHON_VERSION} -m venv .venv"
                sh '.venv/bin/pip install -r requirements-dev.txt'
            }
        }

        stage('Lint') {
            steps { sh '.venv/bin/ruff check .' }
        }

        stage('Test') {
            steps {
                sh ".venv/bin/pytest --cov=src --cov-report=xml --cov-fail-under=${COVERAGE_THRESHOLD}"
            }
            post {
                always {
                    junit '**/test-results.xml'
                    cobertura coberturaReportFile: 'coverage.xml'
                }
            }
        }

        stage('Build') {
            steps {
                sh "docker build -t app:${BUILD_NUMBER} ."
                sh "docker tag app:${BUILD_NUMBER} ${ECR_REGISTRY}/app:${BUILD_NUMBER}"
                sh "docker push ${ECR_REGISTRY}/app:${BUILD_NUMBER}"
            }
        }

        stage('Deploy Staging') {
            when { branch 'main' }
            steps {
                sh "kubectl set image deployment/app app=${ECR_REGISTRY}/app:${BUILD_NUMBER}"
            }
        }
    }

    post {
        failure { slackSend(color: 'danger', message: "Build failed: ${env.BUILD_URL}") }
        success { slackSend(color: 'good', message: "Build passed: ${env.BUILD_URL}") }
    }
}
```

### Shared Library

```groovy
// vars/pythonTest.groovy
def call(Map config = [:]) {
    def version = config.get('pythonVersion', '3.12')
    def threshold = config.get('coverageThreshold', '80')

    stage('Python Test') {
        sh "python${version} -m venv .venv"
        sh '.venv/bin/pip install -r requirements-dev.txt'
        sh '.venv/bin/ruff check .'
        sh ".venv/bin/pytest --cov=src --cov-fail-under=${threshold}"
    }
}

// Usage in Jenkinsfile
@Library('pipelines@main') _
pipeline {
    stages {
        stage('Test') {
            steps {
                pythonTest(pythonVersion: '3.12', coverageThreshold: '80')
            }
        }
    }
}
```

## PR Quality Gates

### Branch Protection Rules

- Require pull request reviews (minimum 1)
- Require status checks to pass: `test (3.11)`, `test (3.12)`, `lint`, `build`
- Require signed commits (optional)
- Require branches to be up to date before merging
- Dismiss stale approvals on new commits

### PR Template

```markdown
## Summary
What changed and why.

## Test Plan
- [ ] Unit tests pass: `pytest`
- [ ] Coverage: `pytest --cov=src --cov-report=term-missing`
- [ ] Lint: `ruff check . && mypy src/`
- [ ] E2E: `npx playwright test`

## Screenshots (if UI)

## Migration Notes
Any database migrations, config changes, or manual steps.
```

## Deployment Environments

### Environment Promotion Flow

```
PR merged → build → test → scan → staging (auto) → approval → prod (manual)
```

### Environment Configuration in GitHub Actions

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ github.ref == 'refs/heads/main' && 'staging' || 'dev' }}
      url: ${{ github.ref == 'refs/heads/main' && 'https://staging.example.com' || 'https://dev.example.com' }}
    steps:
      - run: echo "Deploying to ${{ github.ref }}"
```

### Required Secrets per Environment

Each environment in GitHub Settings → Environments:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `DATABASE_URL`
- `ARGOCD_SERVER`
- `ARGOCD_TOKEN`

## Verification

- All workflows run on push and PR to main
- Coverage threshold enforced (80%+)
- No deployment without required environment approval
- Reusable workflows tested independently
- Jenkins shared library versioned and pinned
