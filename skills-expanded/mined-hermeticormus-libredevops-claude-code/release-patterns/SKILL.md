---
name: release-patterns
description: "Release patterns: ArgoCD ApplicationSets across clusters, semantic-release with image builds in GitHub Actions, blue/green on ECS with an ALB, .releaserc configuration, and a rollback runbook. Use when automating releases or preparing a rollback."
---

# Release Management Patterns

GitOps with ArgoCD, Argo Rollouts, semantic versioning, Helm OCI, and blue/green deployments.

## ArgoCD ApplicationSet (Multi-Cluster)

```yaml
# Deploy same app to all production clusters
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: payment-api
  namespace: argocd
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            environment: production
  template:
    metadata:
      name: "payment-api-{{name}}"
    spec:
      project: production-apps
      source:
        repoURL: https://github.com/org/helm-charts
        targetRevision: HEAD
        path: charts/payment-api
        helm:
          valueFiles:
            - "values-{{metadata.labels.region}}.yaml"
      destination:
        server: "{{server}}"
        namespace: production
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## GitHub Actions: Semantic Release + Image Build

```yaml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write        # For git tag
      packages: write        # For GitHub Packages
      id-token: write        # For OIDC (ECR auth)
    outputs:
      version: ${{ steps.semantic.outputs.new_release_version }}
      published: ${{ steps.semantic.outputs.new_release_published }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0     # Full history for semantic-release

      - name: Semantic Release
        id: semantic
        uses: cycjimmy/semantic-release-action@v4
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  build-push:
    needs: release
    if: needs.release.outputs.published == 'true'
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/github-actions-ecr
          aws-region: us-east-1

      - name: Login to ECR
        id: ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ steps.ecr.outputs.registry }}/payment-api:${{ needs.release.outputs.version }}
            ${{ steps.ecr.outputs.registry }}/payment-api:latest
          cache-from: type=registry,ref=${{ steps.ecr.outputs.registry }}/payment-api:buildcache
          cache-to: type=registry,ref=${{ steps.ecr.outputs.registry }}/payment-api:buildcache,mode=max

  deploy:
    needs: [release, build-push]
    if: needs.release.outputs.published == 'true'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Update Helm values for GitOps
        run: |
          # Update image tag in Helm values file (ArgoCD picks this up)
          sed -i "s/tag: .*/tag: \"${{ needs.release.outputs.version }}\"/" \
            charts/payment-api/values-production.yaml
          git config user.email "actions@github.com"
          git config user.name "GitHub Actions"
          git add charts/payment-api/values-production.yaml
          git commit -m "chore: deploy payment-api v${{ needs.release.outputs.version }}"
          git push
```

## Blue/Green with AWS ALB and ECS

```hcl
# ECS blue/green with CodeDeploy
resource "aws_ecs_service" "app" {
  name            = "payment-api"
  cluster         = aws_ecs_cluster.prod.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 3

  deployment_controller {
    type = "CODE_DEPLOY"  # Enables blue/green
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.blue.arn
    container_name   = "app"
    container_port   = 8080
  }

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }
}

resource "aws_codedeploy_deployment_group" "app" {
  app_name              = aws_codedeploy_app.app.name
  deployment_group_name = "production"
  service_role_arn      = aws_iam_role.codedeploy.arn

  deployment_config_name = "CodeDeployDefault.ECSCanary10Percent5Minutes"
  # Options: ECSAllAtOnce, ECSLinear10PercentEvery1Minutes, ECSCanary10Percent5Minutes

  blue_green_deployment_config {
    deployment_ready_option {
      action_on_timeout    = "CONTINUE_DEPLOYMENT"
      wait_time_in_minutes = 0
    }
    terminate_blue_instances_on_deployment_success {
      action                           = "TERMINATE"
      termination_wait_time_in_minutes = 5  # Keep blue for 5min after green is healthy
    }
  }

  load_balancer_info {
    target_group_pair_info {
      prod_traffic_route { listener_arns = [aws_lb_listener.https.arn] }
      target_group { name = aws_lb_target_group.blue.name }
      target_group { name = aws_lb_target_group.green.name }
    }
  }

  auto_rollback_configuration {
    enabled = true
    events  = ["DEPLOYMENT_FAILURE", "DEPLOYMENT_STOP_ON_ALARM"]
  }

  alarm_configuration {
    alarms  = [aws_cloudwatch_metric_alarm.error_rate.name]
    enabled = true
  }
}
```

## .releaserc (semantic-release config)

```json
{
  "branches": [
    "main",
    {"name": "beta", "prerelease": true},
    {"name": "alpha", "prerelease": true}
  ],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    ["@semantic-release/changelog", {
      "changelogFile": "CHANGELOG.md"
    }],
    ["@semantic-release/git", {
      "assets": ["CHANGELOG.md", "package.json"],
      "message": "chore(release): ${nextRelease.version} [skip ci]"
    }],
    "@semantic-release/github"
  ]
}
```

## Rollback Runbook

```bash
# 1. Check current Helm release state
helm history payment-api -n production

# 2. View what changed
helm diff rollback payment-api 3 -n production

# 3. Rollback
helm rollback payment-api 3 -n production --wait

# 4. Verify
kubectl rollout status deployment/payment-api -n production
kubectl get pods -n production -l app=payment-api

# 5. Argo Rollouts: abort canary and rollback
kubectl argo rollouts abort payment-api -n production
kubectl argo rollouts undo payment-api -n production

# 6. ArgoCD: rollback to previous sync
argocd app history payment-api
argocd app rollback payment-api $PREV_SYNC_ID
```
