---
name: ci-cd-automation
description: CI/CD automation standards — GitHub Actions, Azure Pipelines, deployment automation, testing gates, secrets management
globs: [".github/workflows/**", ".azure-pipelines/**", "**/*.yml", "**/*.yaml", "**/Jenkinsfile", "**/deploy/**"]
alwaysApply: false
---

# CI/CD Automation Standards

Continuous Integration/Continuous Deployment automates testing and deployment. Master GitHub Actions, Azure Pipelines, and deployment automation for reliable releases.

---

## GitHub Actions Workflows

**ALWAYS**:
- Trigger on: push to main/develop, PRs, tags for releases
- Use workflow matrix for multi-platform/version testing
- Cache dependencies (npm, NuGet, Python) to speed builds
- Separate jobs for different stages (lint, test, build, deploy)
- Require status checks on PRs before merge (protected branch)
- Use secrets (GITHUB_TOKEN, API keys) from GitHub Secrets
- Lock workflow action versions (not @latest)
- Run tests before deploy (fail fast)

**NEVER**:
- Store secrets in workflow files (use GitHub Secrets)
- Deploy without running tests
- Use @latest for actions (version inconsistency)
- Deploy on every push (use tags or manual trigger for production)

### ✅ GOOD GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
    tags: ['v*.*.*']
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Lint and security checks
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint code
        run: npm run lint
      
      - name: Security audit
        run: npm audit --audit-level=moderate

  # Run tests
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    strategy:
      matrix:
        node-version: [16, 18, 20]
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test -- --coverage
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unittests
          name: codecov-umbrella

  # Build Docker image
  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name == 'push' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache,mode=max

  # Deploy to staging
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop' && github.event_name == 'push'
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to staging
        run: |
          ./scripts/deploy.sh staging
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
          DEPLOYMENT_HOST: ${{ secrets.STAGING_HOST }}

  # Deploy to production (manual trigger)
  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    environment:
      name: production
      url: https://example.com
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Extract version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
      
      - name: Deploy to production
        run: |
          ./scripts/deploy.sh production --version=${{ steps.version.outputs.VERSION }}
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
          DEPLOYMENT_HOST: ${{ secrets.PROD_HOST }}
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
      
      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Production deployment: ${{ steps.version.outputs.VERSION }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}

  # Health check post-deploy
  health-check:
    needs: deploy-production
    runs-on: ubuntu-latest
    steps:
      - name: Check API health
        run: |
          for i in {1..30}; do
            curl -f https://example.com/health && exit 0
            echo "Attempt $i failed, retrying..."
            sleep 10
          done
          exit 1
```

---

## Azure Pipelines

**ALWAYS**:
- Use multi-stage pipelines (build, test, deploy stages)
- Use pipeline templates for reusability
- Trigger on: PRs, commits to main/develop, tags
- Require checks before production deployment (approval, test passing)
- Use variable groups for secrets (not inline)
- Archive build artifacts
- Deploy to stages in order: dev → staging → production

**NEVER**:
- Skip tests before deploy
- Use hardcoded credentials (use variable groups)
- Deploy on every commit (use tags or manual trigger for prod)

### ✅ GOOD Azure Pipelines Setup

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
    - main
    - develop
  tags:
    include:
    - v*

pr:
  branches:
    include:
    - main
    - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  buildConfiguration: 'Release'
  dotnetVersion: '7.0'

stages:
- stage: Build
  displayName: Build Stage
  jobs:
  - job: BuildDotNet
    displayName: Build .NET Application
    steps:
    - task: UseDotNet@2
      inputs:
        version: $(dotnetVersion)
    
    - task: DotNetCoreCLI@2
      displayName: Restore
      inputs:
        command: 'restore'
    
    - task: DotNetCoreCLI@2
      displayName: Build
      inputs:
        command: 'build'
        arguments: '--configuration $(buildConfiguration)'
    
    - task: DotNetCoreCLI@2
      displayName: Run Tests
      inputs:
        command: 'test'
        arguments: '--configuration $(buildConfiguration) /p:CollectCoverage=true'
    
    - task: PublishCodeCoverageResults@1
      inputs:
        codeCoverageTool: Cobertura
        summaryFileLocation: '$(Agent.TempDirectory)/**/coverage.cobertura.xml'
    
    - task: DotNetCoreCLI@2
      displayName: Publish
      inputs:
        command: 'publish'
        publishWebProjects: true
        arguments: '--configuration $(buildConfiguration) --output $(Build.ArtifactStagingDirectory)'
    
    - task: PublishBuildArtifacts@1
      displayName: Publish Artifacts
      inputs:
        artifactName: 'drop'

- stage: DeployStaging
  displayName: Deploy to Staging
  dependsOn: Build
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/develop')
  
  jobs:
  - deployment: DeployAppService
    displayName: Deploy to App Service
    environment: 'staging'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            inputs:
              azureSubscription: 'Azure Subscription'
              appType: 'webAppLinux'
              appName: 'app-staging'
              package: '$(Pipeline.Workspace)/drop'

- stage: DeployProduction
  displayName: Deploy to Production
  dependsOn: Build
  condition: startsWith(variables['Build.SourceBranch'], 'refs/tags/v')
  
  jobs:
  - deployment: ApprovalGate
    displayName: Approval Gate
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - script: echo "Approval required for production deployment"
  
  - deployment: DeployProduction
    displayName: Deploy to Production
    dependsOn: ApprovalGate
    environment: 'production'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureWebApp@1
            inputs:
              azureSubscription: 'Azure Subscription'
              appType: 'webAppLinux'
              appName: 'app-production'
              package: '$(Pipeline.Workspace)/drop'
          
          - task: AzureCLI@2
            displayName: Health Check
            inputs:
              azureSubscription: 'Azure Subscription'
              scriptType: bash
              scriptLocation: inlineScript
              inlineScript: |
                for i in {1..30}; do
                  if curl -f https://example.com/health; then
                    exit 0
                  fi
                  echo "Attempt $i failed, retrying..."
                  sleep 10
                done
                exit 1
```

---

## Deployment Automation

**ALWAYS**:
- Use Infrastructure as Code (Terraform/CloudFormation/Bicep)
- Implement blue-green deployments (zero downtime)
- Use health checks to verify deployment success
- Implement rollback mechanism (quick recovery if issues)
- Run smoke tests post-deployment
- Gradually roll out (canary, rolling updates)
- Monitor metrics during deployment

**NEVER**:
- Direct SSH into production servers
- Manual copy-paste deployments
- Deploy without health checks
- Skip rollback testing

### ✅ GOOD Deployment Script

```bash
#!/bin/bash
# scripts/deploy.sh

set -e  # Exit on any error

ENVIRONMENT=$1
VERSION=${2:-latest}

echo "Deploying version $VERSION to $ENVIRONMENT"

# 1. Build artifact
echo "Building application..."
docker build -t app:$VERSION .

# 2. Push to registry
echo "Pushing to registry..."
docker push registry.example.com/app:$VERSION

# 3. Blue-green deployment
echo "Starting blue-green deployment..."

# Current (blue)
CURRENT_DEPLOYMENT="app-blue"
# New (green)
NEW_DEPLOYMENT="app-green"

# Deploy green
kubectl set image deployment/$NEW_DEPLOYMENT \
  app=registry.example.com/app:$VERSION \
  --record

# Wait for rollout
echo "Waiting for deployment..."
kubectl rollout status deployment/$NEW_DEPLOYMENT -n $ENVIRONMENT --timeout=5m

# Health check
echo "Health checking..."
for i in {1..30}; do
  if curl -f http://app-green:3000/health; then
    echo "Health check passed"
    break
  fi
  echo "Attempt $i failed, retrying..."
  sleep 5
done

# Switch traffic (blue → green)
echo "Switching traffic..."
kubectl patch service app -n $ENVIRONMENT -p '{"spec":{"selector":{"deployment":"green"}}}'

# Smoke tests
echo "Running smoke tests..."
npm run smoke-test

# Monitor
echo "Monitoring metrics..."
sleep 60
# Check error rates, latency
kubectl top pods -n $ENVIRONMENT

echo "Deployment complete!"

# Rollback function
rollback() {
  echo "Rolling back to previous version..."
  kubectl patch service app -n $ENVIRONMENT -p '{"spec":{"selector":{"deployment":"blue"}}}'
  echo "Rollback complete"
}

# Trap errors
trap rollback ERR
```

---

## Secrets Management

**ALWAYS**:
- Store secrets in Secret Manager (AWS Secrets Manager, Azure Key Vault)
- Never commit secrets to git (.env in .gitignore)
- Rotate secrets regularly (90 days)
- Use temporary credentials (STS, managed identity)
- Audit secret access (CloudTrail, audit logs)
- Use different secrets per environment

**NEVER**:
- Hardcode secrets in code
- Share secrets across teams
- Commit .env files
- Log secrets in output

### ✅ GOOD Secrets Setup

```yaml
# GitHub Actions with secrets
env:
  AWS_REGION: us-east-1
  AWS_ROLE_ARN: ${{ secrets.AWS_ROLE_ARN }}

steps:
  - name: Configure AWS credentials
    uses: aws-actions/configure-aws-credentials@v2
    with:
      role-to-assume: ${{ env.AWS_ROLE_ARN }}
      aws-region: ${{ env.AWS_REGION }}
  
  - name: Get secret from AWS Secrets Manager
    run: |
      API_KEY=$(aws secretsmanager get-secret-value \
        --secret-id prod/api-key \
        --query SecretString --output text)
      echo "::add-mask::$API_KEY"
      echo "API_KEY=$API_KEY" >> $GITHUB_ENV

# Azure Pipelines with variable groups
variables:
  - group: ProductionSecrets  # Variable group in Azure DevOps

steps:
  - task: AzureKeyVault@2
    inputs:
      azureSubscription: 'Azure Subscription'
      keyVaultName: 'prod-kv'
      secretsFilter: '*'
      runnerContext: 'Agent'
```

---

## CI/CD Security Checklist

- [ ] GitHub Actions: Status checks on PRs, secrets in Secrets, workflow versions pinned
- [ ] Azure Pipelines: Approval gates, variable groups, RBAC
- [ ] Tests: Unit, integration, security tests in pipeline
- [ ] Deployment: Blue-green, health checks, rollback mechanism
- [ ] Artifacts: Signed, versioned, uploaded to secure registry
- [ ] Secrets: External storage, rotated, access audited
- [ ] Monitoring: Alerts on deployment failure, post-deploy metrics
- [ ] Audit: All changes logged, deployment history tracked

---

## Summary

Good CI/CD automation:
1. **Automated** — Tests, builds, deploys without manual steps
2. **Gated** — Tests pass before merge, approvals before production
3. **Fast** — Cached dependencies, parallel jobs
4. **Safe** — Blue-green deployments, health checks, rollback
5. **Observable** — Logs, metrics, alerts on failures
6. **Secure** — Secrets managed, audit trails, least privilege

Master GitHub Actions/Azure Pipelines for reliable automated deployments.
