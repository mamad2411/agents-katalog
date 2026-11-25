---
name: complete-cicd-pipeline-deployment-for-serverless-from-scratch
description: >
  Builds a complete CI/CD pipeline for a serverless (AWS Lambda-style)
  function from an empty repo — source checkout, zip/layer packaging (not
  a container image), SCA/SAST security gates, package upload, and a
  SAM/Serverless-Framework/CDK-style deploy step with alias-based canary
  traffic shifting, distinct from Kubernetes rollout mechanics. Use when
  the user asks to "build a full CI/CD pipeline for a Lambda function from
  scratch," "set up serverless CI/CD with canary traffic shifting," "wire
  SAM/Serverless Framework deploys into a pipeline," or "go from an empty
  repo to a function deployed with an alias-based canary."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cicd-tooling
  maturity: stable
---

# Complete CI/CD Pipeline Deployment for Serverless, From Scratch

## Purpose

A serverless pipeline's build artifact and deploy mechanics are both
fundamentally different from the Kubernetes and VM variants of this skill:
the build step produces a **zip archive or a set of Lambda layers**, not a
container image or a machine image, and the deploy step **is** the
pipeline's final action — there is no separate in-cluster operator to hand
off to. Traffic shifting during rollout is done via a **weighted alias**
pointing at two published function versions, not a Kubernetes Service
selector flip or a percentage-weighted `Rollout`/`Canary` CR. This skill
sequences source → zip/layer packaging → SAST/SCA → package upload → an
alias-based canary deploy into one coherent walkthrough; the individual
packaging and IAM mechanics are covered in depth elsewhere and only
sequenced here.

## When to use

- A new Lambda-based (or equivalent FaaS) service has no pipeline yet, and
  the team wants source-to-deployed-with-canary wired up in one pass.
- An existing serverless deploy is a manual `zip` + console upload, and the
  user wants it automated end-to-end with security gates and a safe
  traffic-shift rollout.
- The user wants to understand exactly how a serverless pipeline's
  packaging and rollout mechanics differ from a container/Kubernetes
  pipeline (the point most often gotten wrong when someone tries to reuse
  a Kubernetes pipeline template for a Lambda function).
- Standing up the SAST/SCA gate sequence specifically for a zip/layer
  build (function dependencies bundled directly into the package, not a
  separately-scanned base image).

## Prerequisites & environment

- A Git host and CI platform already available — examples below use
  GitHub Actions; the same shape applies to
  [azure-pipelines-yaml-and-multi-stage](../azure-pipelines-yaml-and-multi-stage/SKILL.md)
  or any equivalent platform.
- AWS credentials for CI scoped to deploy this one function (or function
  group) only — least-privilege, per
  [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md)
  — never a broad account-wide deploy role.
- A deploy framework chosen: AWS SAM, Serverless Framework, or CDK all
  wrap the underlying `CreateFunction`/`UpdateFunctionCode`/alias API
  calls; examples below use SAM (`sam build`/`sam deploy`) since it's the
  most directly AWS-native, with a Serverless Framework note where the
  shape differs.
- [aws-lambda-packaging-and-configuration](../../../serverless-and-alternative-compute/skills/aws-lambda-packaging-and-configuration/SKILL.md)
  already read for the packaging/IAM-role mechanics this pipeline
  automates — this skill sequences that packaging into CI, it does not
  re-explain zip-vs-container-image tradeoffs or memory/timeout tuning.
- SAST/SCA tooling chosen per
  [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md)
  and
  [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md).

## Step-by-step guidance

### Phase 1 — Source and trigger scoping

Standard PR/push trigger setup per
[ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md).

### Phase 2 — Package as a zip/layer, not a container image

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: |
          pip install -r requirements.txt -t package/
          cp -r src/* package/
          cd package && zip -r ../function.zip . -x '*.pyc'
      - uses: actions/upload-artifact@v4
        with: { name: function-package, path: function.zip }
```
There is no Dockerfile, no base-image choice, and no multi-stage build
here — contrast directly with Phase 2 of the Kubernetes variant of this
skill. Shared/common dependencies used across multiple functions become a
separately-versioned **Lambda layer** (its own zip, published once, mounted
at `/opt` on every consuming function) rather than a shared base image
layer, per
[aws-lambda-packaging-and-configuration](../../../serverless-and-alternative-compute/skills/aws-lambda-packaging-and-configuration/SKILL.md).

### Phase 3 — SAST and SCA gates, scoped to a much larger transitive surface

Function dependency trees bundled directly into the zip (all of
`node_modules`/site-packages, not just what a slim container runtime
image would carry) are frequently the largest attack-surface component of
a serverless package — scan the packaged dependency tree, not just the
application's own source:
```yaml
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: semgrep ci --config p/owasp-top-ten --baseline-commit "${{ github.event.pull_request.base.sha }}"
  sca:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with: { name: function-package }
      - run: |
          unzip function.zip -d unpacked/
          trivy fs --severity CRITICAL,HIGH --exit-code 1 unpacked/
```
Scanning the *unpacked, fully-resolved* package (after `pip install -t`/
`npm ci --omit=dev`) rather than only the top-level `requirements.txt`/
`package.json` is what catches vulnerable transitive dependencies that
ended up bundled into the deployed artifact.

### Phase 4 — Upload the package as a build artifact

```bash
aws s3 cp function.zip s3://payments-api-artifacts/${GITHUB_SHA}/function.zip
```
SAM/Serverless Framework typically wrap this upload internally as part of
`sam deploy`/`serverless deploy`; shown explicitly here since the
artifact-upload step is itself part of what differs from a container
pipeline's registry push.

### Phase 5 — Deploy via SAM/Serverless Framework, publishing a new version

```bash
sam build
sam deploy \
  --stack-name payments-api \
  --s3-bucket payments-api-artifacts \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset
```
`sam deploy` (via CloudFormation) publishes a new immutable Lambda
**version** on each deploy — versions, not the mutable `$LATEST`, are what
aliases and traffic-shifting target, per
[aws-lambda-packaging-and-configuration](../../../serverless-and-alternative-compute/skills/aws-lambda-packaging-and-configuration/SKILL.md).

### Phase 6 — Canary traffic shift via a weighted alias — not a Kubernetes rollout

This is the serverless-specific rollout mechanic: instead of a Service
selector flip or a percentage-weighted `Rollout` CR routing between pods,
Lambda shifts a percentage of **invocations** between two published
function *versions* under one alias, either via SAM's built-in
`AutoPublishAlias`/`DeploymentPreference` (which wraps CodeDeploy) or
directly with CodeDeploy's Lambda traffic-shifting hooks — the same
CodeDeploy engine covered for EC2/ECS in
[aws-codepipeline-and-codedeploy](../aws-codepipeline-and-codedeploy/SKILL.md),
applied to its Lambda deployment type instead:
```yaml
# template.yaml (SAM)
Resources:
  PaymentsApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      AutoPublishAlias: prod
      DeploymentPreference:
        Type: Canary10Percent5Minutes
        Alarms:
          - !Ref PaymentsApiErrorAlarm
        Hooks:
          PreTraffic: !Ref PreTrafficHookFunction
          PostTraffic: !Ref PostTrafficHookFunction
```
`Canary10Percent5Minutes` shifts 10% of invocations to the new version for
5 minutes, running `PreTraffic`/`PostTraffic` Lambda hook functions to
validate before/after each shift, and **automatically rolls back** to the
prior version if `PaymentsApiErrorAlarm` (a CloudWatch alarm on error
rate) fires during the canary window — no cluster, no pods, no Service
object involved anywhere in this mechanism.

### Phase 7 — Verify

```bash
aws lambda get-alias --function-name payments-api --name prod
aws cloudwatch describe-alarms --alarm-names payments-api-error-rate
```
Confirm the alias's `RoutingConfig.AdditionalVersionWeights` has returned
to empty (fully cut over) or that a rollback reverted `FunctionVersion`
back to the prior value, depending on outcome.

## Best practices

- Scan the fully resolved, unpacked deployment package (Phase 3), not just
  the top-level manifest — a serverless zip bundles its entire dependency
  tree directly, unlike a container image where OS-level and
  application-level dependencies are scanned as separate layers.
- Publish immutable versions on every deploy and target aliases in every
  downstream integration (API Gateway, EventBridge rule, another
  function's invoke permission) — never point anything at `$LATEST` in
  production, mirroring the immutable-tag discipline in
  [container-build-and-release](../../../devops/skills/container-build-and-release/SKILL.md)
  but for function versions instead of image tags.
- Attach a real CloudWatch alarm (error rate, duration, throttles) to the
  `DeploymentPreference`'s `Alarms` list — a canary with no alarm attached
  will complete the traffic shift on a timer regardless of whether the new
  version is actually healthy.
- Keep the CI deploy role scoped to exactly the functions/stacks it
  manages (`lambda:UpdateFunctionCode`, `cloudformation:*` on the specific
  stack ARN) — never a broad `lambda:*`/`iam:*` role "to make SAM deploy
  work."
- Use `PreTraffic`/`PostTraffic` hook functions for real smoke tests
  (invoke the new version directly, verify output) rather than leaving
  them as no-op stubs — an empty hook that always returns success defeats
  the canary's safety purpose.

## Common pitfalls

- **Symptom:** The team copies a Kubernetes-style pipeline template,
  builds a Docker image for the function, and pushes it to a container
  registry — then can't figure out why the Lambda deploy step fails.
  **Fix:** Lambda supports container-image packaging as an alternative
  (per
  [aws-lambda-packaging-and-configuration](../../../serverless-and-alternative-compute/skills/aws-lambda-packaging-and-configuration/SKILL.md)),
  but it's a deliberate choice for large/native dependencies, not the
  default — for a typical function, package as zip/layer (Phase 2) and
  deploy via `UpdateFunctionCode`/SAM rather than assuming every workload
  needs a container image and registry push.

- **Symptom:** A "canary" deploy shifts 10% of traffic as configured, but
  five minutes later 100% of traffic is on the new version regardless of
  whether it's actually healthy.
  **Fix:** No alarm was attached to `DeploymentPreference.Alarms` (or the
  alarm's metric/threshold doesn't actually reflect this function's error
  rate) — CodeDeploy's Lambda traffic shift completes on a timer by
  default; attach and verify a real, function-specific CloudWatch alarm
  so a bad canary is caught and rolled back automatically.

- **Symptom:** The SCA scan only checks `requirements.txt`/`package.json`
  and reports "no vulnerabilities," but the actual deployed zip (after
  `pip install -t package/`) contains a vulnerable transitive dependency
  that never showed up in the scan.
  **Fix:** Scan the *unpacked, fully-resolved* deployment package (Phase
  3) after the install/bundle step, not just the top-level manifest —
  this is the serverless-specific version of the "scan lockfiles, not
  manifests" guidance in
  [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md),
  made more consequential because the entire dependency tree ships inside
  one artifact with no separate layer boundary to scan independently.

- **Symptom:** A downstream integration (an API Gateway stage, an
  EventBridge rule) was pointed directly at `$LATEST` "temporarily," and a
  routine deploy immediately breaks it in production with no canary
  protection at all.
  **Fix:** `$LATEST` has no alias/version indirection and therefore no
  traffic-shifting or rollback path — repoint every downstream integration
  at the `prod` alias (Phase 6) before the next deploy, treating a
  `$LATEST`-pointed integration as a standing risk, not a temporary
  convenience.

## Worked example

**Scenario:** `payments-webhook`, a Python Lambda function invoked via API
Gateway, gets its first full pipeline: PR-time SAST/SCA on the packaged
dependency tree, zip build, and a SAM deploy with a 10%/5-minute canary
gated on an error-rate alarm.

```yaml
name: ci-cd
on:
  pull_request: { branches: [main] }
  push: { branches: [main] }

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          pip install -r requirements.txt -t package/
          cp -r src/* package/
          cd package && zip -r ../function.zip .
      - uses: actions/upload-artifact@v4
        with: { name: function-package, path: function.zip }

  sca:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with: { name: function-package }
      - run: |
          unzip -q function.zip -d unpacked/
          trivy fs --severity CRITICAL,HIGH --exit-code 1 unpacked/

  deploy:
    needs: sca
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/setup-sam@v2
      - run: sam build
      - run: sam deploy --stack-name payments-webhook --no-confirm-changeset --capabilities CAPABILITY_IAM
```
`template.yaml`'s `DeploymentPreference: Canary10Percent5Minutes` (Phase
6) shifts 10% of API Gateway-routed invocations to the new version,
watches `PaymentsWebhookErrorAlarm`, and either completes the cutover to
100% after 5 clean minutes or automatically reverts the `prod` alias to
the prior version — no Kubernetes object, pod, or Service involved at any
point in the rollout.

## Cross-references

- [aws-lambda-packaging-and-configuration](../../../serverless-and-alternative-compute/skills/aws-lambda-packaging-and-configuration/SKILL.md) — zip/layer packaging and IAM execution-role mechanics used in Phase 2/5.
- [aws-codepipeline-and-codedeploy](../aws-codepipeline-and-codedeploy/SKILL.md) — the underlying CodeDeploy traffic-shifting engine Phase 6's canary uses, shown there for EC2/ECS.
- [sast-integration](../../../devsecops/skills/sast-integration/SKILL.md) and [software-composition-analysis-sca](../../../devsecops/skills/software-composition-analysis-sca/SKILL.md) — Phase 3's scan mechanics, applied here to a packaged zip.
- [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md) — vendor-neutral stage/gate concepts this pipeline implements.
- [cloud-iam-hardening](../../../cloud/skills/cloud-iam-hardening/SKILL.md) — least-privilege scoping for the CI deploy role and function execution role.
- [complete-cicd-pipeline-deployment-for-kubernetes-from-scratch](../complete-cicd-pipeline-deployment-for-kubernetes-from-scratch/SKILL.md) and [complete-cicd-pipeline-for-vm-based-workloads-from-scratch](../complete-cicd-pipeline-for-vm-based-workloads-from-scratch/SKILL.md) — the same source-to-deploy shape for a fundamentally different build artifact and deploy mechanism.
