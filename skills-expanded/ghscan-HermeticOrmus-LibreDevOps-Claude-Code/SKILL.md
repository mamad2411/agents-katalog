# GitLab CI Patterns

DAG pipelines, merge request pipelines, security scanning, environment deployments, and shared templates.

## Complete .gitlab-ci.yml for a Node.js App

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - security
  - deploy

default:
  image: node:20-alpine
  cache:
    key:
      files: [package-lock.json]
    paths: [.npm/]
  interruptible: true   # Cancel running pipeline when new push comes

variables:
  DOCKER_BUILDKIT: "1"
  DOCKER_HOST: tcp://docker:2376
  DOCKER_TLS_VERIFY: "1"
  DOCKER_CERT_PATH: "$DOCKER_TLS_CERTDIR/client"

# ─── BUILD STAGE ─────────────────────────────────────────────────────

build-app:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build
        --build-arg BUILDKIT_INLINE_CACHE=1
        --cache-from $CI_REGISTRY_IMAGE:cache
        --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
        --tag $CI_REGISTRY_IMAGE:cache
        .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:cache
  rules:
    - if: $CI_COMMIT_BRANCH
    - if: $CI_COMMIT_TAG

# ─── TEST STAGE (DAG: starts when build-app finishes) ────────────────

test-unit:
  stage: test
  needs: [build-app]
  script:
    - npm ci --cache .npm
    - npm test -- --coverage
  artifacts:
    reports:
      junit: test-results.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    expire_in: 7 days
  coverage: '/Statements\s*:\s*(\d+\.?\d*)%/'
  rules:
    - if: $CI_COMMIT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

# Runs in parallel with test-unit (no deps on each other)
lint:
  stage: test
  needs: []           # Start with build stage, no dependency on build-app
  script:
    - npm ci --cache .npm
    - npm run lint
    - npm run type-check
  rules:
    - if: $CI_COMMIT_BRANCH
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

# ─── SECURITY STAGE ───────────────────────────────────────────────────

include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml

container_scanning:
  variables:
    CS_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  needs: [build-app]   # Override template to require build first

# ─── DEPLOY STAGE ─────────────────────────────────────────────────────

deploy-review:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.review.example.com
    on_stop: stop-review
    auto_stop_in: 1 week
    deployment_tier: development
  needs:
    - job: build-app
    - job: test-unit
  script:
    - kubectl set image deployment/myapp app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n review-$CI_COMMIT_REF_SLUG
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

stop-review:
  stage: deploy
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  script:
    - kubectl delete namespace review-$CI_COMMIT_REF_SLUG
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual

deploy-staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
    deployment_tier: staging
  needs:
    - job: build-app
    - job: test-unit
    - job: container_scanning
  script:
    - kubectl set image deployment/myapp app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n staging
    - kubectl rollout status deployment/myapp -n staging
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy
  environment:
    name: production
    url: https://example.com
    deployment_tier: production
  needs:
    - job: deploy-staging
  script:
    - kubectl set image deployment/myapp app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n production
    - kubectl rollout status deployment/myapp -n production
  when: manual   # Require manual click in GitLab UI
  rules:
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/
```

## Shared Templates Pattern

```yaml
# ci/templates/docker.yml (in same repo or separate template project)
.docker-build:
  image: docker:24
  services:
    - docker:24-dind
  variables:
    DOCKER_BUILDKIT: "1"
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

.docker-build-push:
  extends: .docker-build
  script:
    - docker build
        --cache-from $CI_REGISTRY_IMAGE:cache
        --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
        .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

# Usage:
build:
  extends: .docker-build-push
  stage: build
```

## Merge Request Pipeline Configuration

```yaml
# Use GitLab MergeRequest-Pipelines workflow template
# This disables branch pipelines for branches with open MRs
include:
  - template: Workflows/MergeRequest-Pipelines.gitlab-ci.yml

# Now use rules with merge_request_event:
test:
  script: npm test
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# MR-only jobs
code-quality:
  script: npm run quality-report
  artifacts:
    reports:
      codequality: gl-code-quality-report.json
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

## Dynamic Child Pipelines

```yaml
# Parent: generate child pipeline based on changed files
generate-pipeline:
  stage: build
  script:
    - |
      if git diff --name-only $CI_MERGE_REQUEST_DIFF_BASE_SHA | grep -q "^frontend/"; then
        cat ci/frontend-pipeline.yml >> generated-pipeline.yml
      fi
      if git diff --name-only $CI_MERGE_REQUEST_DIFF_BASE_SHA | grep -q "^backend/"; then
        cat ci/backend-pipeline.yml >> generated-pipeline.yml
      fi
  artifacts:
    paths: [generated-pipeline.yml]
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

trigger-child:
  stage: test
  needs: [generate-pipeline]
  trigger:
    include:
      - artifact: generated-pipeline.yml
        job: generate-pipeline
    strategy: depend   # Wait for child pipeline to complete
```

## GitLab CI Environment Variables Reference

```yaml
# Predefined variables used in pipelines
CI_COMMIT_SHA           # Full commit hash
CI_COMMIT_SHORT_SHA     # Short hash (8 chars)
CI_COMMIT_BRANCH        # Current branch (not set for MRs)
CI_COMMIT_TAG           # Tag name (only in tag pipelines)
CI_COMMIT_REF_SLUG      # Branch/tag as URL-safe slug
CI_DEFAULT_BRANCH       # Repo default branch (main/master)
CI_PIPELINE_SOURCE      # push/web/schedule/merge_request_event
CI_MERGE_REQUEST_IID    # MR number (only in MR pipelines)
CI_PROJECT_PATH         # org/repo
CI_REGISTRY             # GitLab Container Registry URL
CI_REGISTRY_IMAGE       # $CI_REGISTRY/$CI_PROJECT_PATH
CI_REGISTRY_USER        # Auth user for registry
CI_REGISTRY_PASSWORD    # Auth token for registry
CI_ENVIRONMENT_NAME     # Name of the environment being deployed to
CI_ENVIRONMENT_URL      # URL of the environment
CI_JOB_TOKEN            # Short-lived job token (read-only git access)
```
