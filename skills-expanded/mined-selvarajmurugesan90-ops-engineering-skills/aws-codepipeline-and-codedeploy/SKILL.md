---
name: aws-codepipeline-and-codedeploy
description: >
  Designs AWS CodePipeline stage/action structure and integrates it with
  CodeDeploy deployment groups and appspec.yml for EC2/on-prem, ECS, or
  Lambda deploys. Use when the user asks to "set up CodePipeline," "add a
  CodeDeploy deployment group," "write an appspec.yml," "wire CodePipeline
  to CodeDeploy," "troubleshoot a stuck/failed CodePipeline action," or
  "add a manual approval action before an AWS deploy."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cicd-tooling
  maturity: stable
---

# AWS CodePipeline and CodeDeploy

## Purpose

AWS CodePipeline orchestrates a release as a sequence of **stages**, each
containing one or more **actions** (source, build, test, approval, deploy)
that can run in parallel within a stage, while **CodeDeploy** handles the
actual deployment mechanics — rolling out a new revision to EC2/on-prem
instances, an ECS service, or a Lambda function according to a
**deployment group**'s configuration and an `appspec.yml`'s lifecycle
hooks. This skill covers the CodePipeline stage/action JSON/YAML structure
and how it integrates with CodeDeploy specifically — not the generic
pipeline-design concepts covered in
[ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md),
which apply here too but aren't repeated.

## When to use

- Standing up a new CodePipeline for an application already built
  elsewhere (or with a CodeBuild stage) that needs to deploy via
  CodeDeploy.
- Writing or debugging an `appspec.yml` whose lifecycle hooks
  (`BeforeInstall`, `AfterInstall`, `ApplicationStart`, `ValidateService`)
  aren't firing in the expected order, or a hook script exits non-zero.
- Configuring a CodeDeploy deployment group's deployment configuration
  (in-place vs. blue/green, `CodeDeployDefault.OneAtATime` vs. percentage-
  based) for EC2/on-prem, or the equivalent ECS/Lambda traffic-shifting
  options.
- Adding a manual approval action to a CodePipeline before a production
  deploy stage.
- Diagnosing a CodePipeline execution stuck or failed at a specific stage/
  action, or a CodeDeploy deployment that failed a lifecycle hook or
  health check.

## Prerequisites & environment

- An AWS account with IAM permissions to create/manage CodePipeline
  pipelines, CodeDeploy applications/deployment groups, and (for EC2/on-
  prem deploys) an IAM instance profile on target instances allowing the
  CodeDeploy agent to pull deployment bundles from S3.
- The **CodeDeploy agent** installed and running on target EC2/on-prem
  instances (not needed for ECS or Lambda deployment types, which use
  CodeDeploy's native integration instead).
- A CodePipeline service role with permission to invoke each stage's
  action provider (CodeCommit/GitHub/S3 for source, CodeBuild for build,
  CodeDeploy for deploy) — least-privilege scoped per action, not a single
  account-wide admin role.
- An S3 artifact bucket (CodePipeline's default artifact store, or a
  specified one) that all pipeline stages can read/write to pass build
  output between stages.
- For blue/green EC2 deployments: an Elastic Load Balancer (ALB/CLB)
  already provisioned and referenced in the deployment group config.

## Step-by-step guidance

1. **Model the pipeline as stages of parallelizable actions**, not one
   flat list — actions within a stage can run in parallel via
   `runOrder`, while stages themselves execute sequentially:
   ```json
   {
     "pipeline": {
       "name": "checkout-api-pipeline",
       "roleArn": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/codepipeline-service-role",
       "artifactStore": { "type": "S3", "location": "codepipeline-artifacts-<AWS_ACCOUNT_ID>" },
       "stages": [
         {
           "name": "Source",
           "actions": [{
             "name": "Source",
             "actionTypeId": { "category": "Source", "owner": "AWS", "provider": "CodeStarSourceConnection", "version": "1" },
             "configuration": { "ConnectionArn": "arn:aws:codestar-connections:<REGION>:<AWS_ACCOUNT_ID>:connection/<CONNECTION_ID>", "FullRepositoryId": "org/checkout-api", "BranchName": "main" },
             "outputArtifacts": [{ "name": "SourceOutput" }]
           }]
         },
         {
           "name": "Build",
           "actions": [{
             "name": "Build",
             "actionTypeId": { "category": "Build", "owner": "AWS", "provider": "CodeBuild", "version": "1" },
             "configuration": { "ProjectName": "checkout-api-build" },
             "inputArtifacts": [{ "name": "SourceOutput" }],
             "outputArtifacts": [{ "name": "BuildOutput" }]
           }]
         },
         {
           "name": "ApproveProduction",
           "actions": [{
             "name": "ManualApproval",
             "actionTypeId": { "category": "Approval", "owner": "AWS", "provider": "Manual", "version": "1" },
             "configuration": { "CustomData": "Approve deploy of build ${env.CODEBUILD_RESOLVED_SOURCE_VERSION} to production" }
           }]
         },
         {
           "name": "Deploy",
           "actions": [{
             "name": "Deploy",
             "actionTypeId": { "category": "Deploy", "owner": "AWS", "provider": "CodeDeploy", "version": "1" },
             "configuration": { "ApplicationName": "checkout-api", "DeploymentGroupName": "checkout-api-production" },
             "inputArtifacts": [{ "name": "BuildOutput" }]
           }]
         }
       ]
     }
   }
   ```
   The `ApproveProduction` stage blocks pipeline progress until a human
   approves/rejects in the console or via `aws codepipeline
   put-approval-result` — this is CodePipeline's equivalent of a GitHub
   Actions protected `environment:` or GitLab `when: manual`.

2. **Write `appspec.yml` to define the deployment's file mapping and
   lifecycle hooks** (EC2/on-prem example — the revision bundle's root):
   ```yaml
   version: 0.0
   os: linux
   files:
     - source: /
       destination: /opt/checkout-api
   permissions:
     - object: /opt/checkout-api
       owner: appuser
       group: appuser
       mode: "755"
   hooks:
     BeforeInstall:
       - location: scripts/stop_service.sh
         timeout: 60
     AfterInstall:
       - location: scripts/install_deps.sh
         timeout: 300
     ApplicationStart:
       - location: scripts/start_service.sh
         timeout: 60
     ValidateService:
       - location: scripts/health_check.sh
         timeout: 120
   ```
   Hooks run strictly in this order (`BeforeInstall` → `AfterInstall` →
   `ApplicationStart` → `ValidateService`, plus `ApplicationStop`/
   `BeforeBlockTraffic`/`AfterBlockTraffic`/`BeforeAllowTraffic`/
   `AfterAllowTraffic` for load-balanced deployments) — a hook script must
   exit `0` for the deployment to proceed to the next hook.

3. **Choose the deployment type and configuration deliberately.** For
   EC2/on-prem, in-place `CodeDeployDefault.OneAtATime` is safest for
   stateful services but slowest; percentage-based
   (`CodeDeployDefault.HalfAtATime`,
   `CodeDeployDefault.AllAtOnce`) trades safety for speed. Blue/green
   (`deploymentType: BLUE_GREEN`) provisions a new instance set behind the
   load balancer and shifts traffic only after `ValidateService` passes,
   giving an automatic rollback path if validation fails:
   ```json
   {
     "applicationName": "checkout-api",
     "deploymentGroupName": "checkout-api-production",
     "deploymentConfigName": "CodeDeployDefault.OneAtATime",
     "autoScalingGroups": ["checkout-api-asg"],
     "loadBalancerInfo": { "elbInfoList": [{ "name": "checkout-api-alb-tg" }] },
     "deploymentStyle": { "deploymentType": "BLUE_GREEN", "deploymentOption": "WITH_TRAFFIC_CONTROL" },
     "blueGreenDeploymentConfiguration": {
       "terminateBlueInstancesOnDeploymentSuccess": { "action": "TERMINATE", "terminationWaitTimeInMinutes": 30 }
     }
   }
   ```

4. **For ECS deployments**, CodeDeploy uses `appspec.yml` referencing the
   task definition and container, with CodePipeline's `ECS` deploy
   provider (blue/green via CodeDeploy) or the simpler native `ECS`
   provider (rolling update, no CodeDeploy):
   ```yaml
   version: 0.0
   Resources:
     - TargetService:
         Type: AWS::ECS::Service
         Properties:
           TaskDefinition: "<TASK_DEFINITION_ARN>"
           LoadBalancerInfo:
             ContainerName: "checkout-api"
             ContainerPort: 8080
   ```

5. **Wire automatic rollback on deployment failure** at the deployment
   group level rather than relying on someone to notice and manually roll
   back:
   ```json
   "autoRollbackConfiguration": {
     "enabled": true,
     "events": ["DEPLOYMENT_FAILURE", "DEPLOYMENT_STOP_ON_ALARM"]
   }
   ```
   Pair with a CloudWatch alarm (`DEPLOYMENT_STOP_ON_ALARM`) tied to a
   real health metric (error rate, latency) so a deployment that passes
   `ValidateService` but degrades under real traffic still triggers
   rollback.

6. **Scope IAM roles per action/service, not one shared admin role** — the
   CodePipeline service role needs only `codebuild:StartBuild`,
   `codedeploy:CreateDeployment`, `s3:*Object` on the artifact bucket, etc.,
   scoped to the specific resources it orchestrates; the CodeDeploy
   service role and the EC2 instance profile are separate roles with their
   own narrower scopes.

7. **Verify a stuck pipeline execution's specific failed action** via
   `aws codepipeline get-pipeline-state --name <pipeline>` and the
   CodeDeploy deployment's event log
   (`aws deploy get-deployment --deployment-id <id>`) rather than only
   looking at the pipeline's overall red/green status — the actual error
   (a failed hook script, an IAM permission denial, a health check
   timeout) is in the deployment's lifecycle event detail, not the
   pipeline summary.

## Best practices

- Put a manual **Approval** action immediately before any production
  `Deploy` action, and route its notification (via SNS) to the actual
  on-call/release channel — an approval stage nobody sees defeats the
  purpose.
- Always enable `autoRollbackConfiguration` for production deployment
  groups; a deployment with no rollback path turns a bad release into an
  extended incident instead of an automatic recovery.
- Use blue/green (or ECS/Lambda's native traffic-shifting) for anything
  where a bad deploy causes user-facing errors before you can react
  manually — in-place `AllAtOnce` should be reserved for low-risk,
  easily-recoverable services.
- Keep `appspec.yml` hook scripts idempotent and fast-failing (exit
  non-zero immediately on a real problem) — a hook that hangs blocks the
  whole deployment until its `timeout` is hit.
- Store deployment configuration (deployment group settings, alarm ARNs)
  as infrastructure-as-code (CloudFormation/CDK/Terraform) alongside the
  pipeline definition, not as manually-clicked console configuration that
  can't be diffed in a PR.
- Tag pipeline artifacts and CodeDeploy revisions with the source commit
  SHA so a running deployment is traceable back to exactly which commit
  produced it, mirroring the traceability guidance in
  [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md).

## Common pitfalls

- **Symptom:** A CodePipeline execution shows "Failed" on the `Deploy`
  stage with no further detail in the pipeline console view.
  **Fix:** Pull the specific CodeDeploy deployment's event log
  (`aws deploy get-deployment-instance` / the CodeDeploy console's
  deployment details) — the actual cause (a specific `appspec.yml` hook
  script exiting non-zero, a health check failing, an instance not
  running the CodeDeploy agent) is only visible there, not in the
  pipeline's stage-level status.

- **Symptom:** A deployment "succeeds" per CodeDeploy but the application
  is actually broken for users.
  **Fix:** The `ValidateService` hook is likely missing or too shallow
  (e.g. just checking the process is running, not that it responds
  correctly); write a real health check that exercises a meaningful
  endpoint, and pair it with `DEPLOYMENT_STOP_ON_ALARM` auto-rollback tied
  to a post-deploy CloudWatch alarm so problems caught only under real
  traffic still trigger rollback.

- **Symptom:** A blue/green EC2 deployment leaves the old ("blue") instance
  set running indefinitely, doubling infrastructure cost.
  **Fix:** Set `blueGreenDeploymentConfiguration.terminateBlueInstancesOnDeploymentSuccess`
  with an explicit `action: TERMINATE` and a reasonable
  `terminationWaitTimeInMinutes`, rather than leaving it at
  `KEEP_ALIVE` indefinitely by default/oversight.

- **Symptom:** The pipeline's IAM service role has broad
  `codedeploy:*`/`s3:*` permissions "to make it work," and a compromised
  pipeline execution can affect resources far outside its intended scope.
  **Fix:** Scope the CodePipeline and CodeDeploy service roles to the
  specific applications/deployment groups/buckets they orchestrate, using
  resource ARNs rather than wildcards — treat an overly broad pipeline
  role as a real security finding, not a convenience shortcut.

- **Symptom:** Someone manually triggers `aws deploy create-deployment`
  directly against production, bypassing the pipeline's approval stage
  entirely, and there's no record of who approved it or why.
  **Fix:** This is a destructive/dangerous action if used to skip an
  intended approval gate — restrict direct `codedeploy:CreateDeployment`
  IAM permission on production deployment groups to the pipeline's own
  service role, so a production deploy can only happen through the
  pipeline (and its approval stage), not by a human or script calling the
  API directly.

## Worked example

**Scenario:** A checkout service deploys to an EC2 Auto Scaling Group
behind an ALB, using CodePipeline (source → build → manual approval →
blue/green CodeDeploy) with automatic rollback on failed health checks.

Pipeline stage sequence (as JSON stage array, abbreviated to the deploy
portion):
```json
{
  "name": "Deploy",
  "actions": [{
    "name": "BlueGreenDeploy",
    "actionTypeId": { "category": "Deploy", "owner": "AWS", "provider": "CodeDeploy", "version": "1" },
    "configuration": {
      "ApplicationName": "checkout-api",
      "DeploymentGroupName": "checkout-api-production-bg"
    },
    "inputArtifacts": [{ "name": "BuildOutput" }]
  }]
}
```

Deployment group (created via CloudFormation, abbreviated):
```yaml
CheckoutApiDeploymentGroup:
  Type: AWS::CodeDeploy::DeploymentGroup
  Properties:
    ApplicationName: checkout-api
    DeploymentGroupName: checkout-api-production-bg
    DeploymentConfigName: CodeDeployDefault.ECSAllAtOnce
    ServiceRoleArn: !GetAtt CodeDeployServiceRole.Arn
    AutoScalingGroups: [!Ref CheckoutApiAsg]
    DeploymentStyle:
      DeploymentType: BLUE_GREEN
      DeploymentOption: WITH_TRAFFIC_CONTROL
    BlueGreenDeploymentConfiguration:
      TerminateBlueInstancesOnDeploymentSuccess:
        Action: TERMINATE
        TerminationWaitTimeInMinutes: 15
    AutoRollbackConfiguration:
      Enabled: true
      Events: [DEPLOYMENT_FAILURE, DEPLOYMENT_STOP_ON_ALARM]
    AlarmConfiguration:
      Enabled: true
      Alarms:
        - Name: checkout-api-5xx-rate-high
```

`appspec.yml` in the build artifact:
```yaml
version: 0.0
os: linux
files:
  - source: /
    destination: /opt/checkout-api
hooks:
  AfterInstall:
    - location: scripts/install_deps.sh
      timeout: 300
  ApplicationStart:
    - location: scripts/start_service.sh
      timeout: 60
  ValidateService:
    - location: scripts/health_check.sh
      timeout: 120
```
`scripts/health_check.sh` curls `/healthz` and exits non-zero on a
non-200 response, so a bad build fails `ValidateService` before traffic
ever shifts to the new ("green") instance set, and the pre-existing
`checkout-api-5xx-rate-high` CloudWatch alarm triggers automatic rollback
if errors spike shortly after traffic does shift.

## Cross-references

- [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md) — vendor-neutral stage/gate/rollback concepts this pipeline implements in AWS-specific terms.
- [github-actions-centralized-reusable-workflows](../github-actions-centralized-reusable-workflows/SKILL.md) — comparable centralized-pipeline pattern if the build stage is migrated off CodeBuild to GitHub Actions while keeping CodeDeploy for the deploy stage.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) — where to place scan actions relative to the manual approval and deploy stages here.
