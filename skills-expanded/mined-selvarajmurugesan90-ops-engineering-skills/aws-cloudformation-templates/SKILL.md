---
name: aws-cloudformation-templates
description: >
  Authors and safely operates AWS CloudFormation templates (YAML/JSON),
  including stacks, change sets, nested and cross-stack references,
  StackSets for multi-account/multi-region deployment, and drift detection.
  Use when the user asks to "write a CloudFormation template for X,"
  "structure nested CloudFormation stacks," "deploy the same stack across
  AWS accounts/regions," "review a CloudFormation change set before
  applying," "detect/reconcile drift on a stack," or "migrate/compare
  CloudFormation with Terraform" for an AWS-native IaC choice.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# AWS CloudFormation Templates

## Purpose

CloudFormation is AWS's native infrastructure-as-code service: it declares
AWS resources in a YAML/JSON template, and AWS itself manages the create/
update/delete lifecycle as a stack, tracking resource state server-side
(no separate state file to store or lock). That server-side state is also
the main operational tradeoff versus a tool like Terraform — see
[infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md)
for the general "why IaC" case and Terraform's plan/state/module model.
CloudFormation trades Terraform's multi-cloud portability and local plan
files for deep native integration: no state backend to configure, native
rollback on failed updates, IAM-scoped stack permissions, and StackSets for
governed multi-account/multi-region rollout. Choose CloudFormation when the
workload is AWS-only and you want AWS to own the state and rollback
semantics; choose Terraform when you need multi-cloud consistency, a richer
module ecosystem, or a plan file reviewable outside the AWS console/CLI.

## When to use

- Provisioning AWS-only infrastructure where native rollback-on-failure and
  no external state backend are wanted.
- Structuring a large template into nested stacks or cross-stack exports so
  networking, IAM, and application layers can be owned/updated separately.
- Rolling the same template out to many AWS accounts and/or regions under
  central governance (landing zones, guardrail stacks, per-account
  baselines) via StackSets.
- Reviewing a change set before letting an update touch a shared or
  production stack.
- Detecting and reconciling drift after someone made a manual console
  change to a stack-managed resource.
- Deciding between CloudFormation and Terraform for a new AWS workload.

## Prerequisites & environment

- AWS CLI v2 and an IAM principal with the specific `cloudformation:*`
  actions needed (`CreateStack`, `CreateChangeSet`, `ExecuteChangeSet`,
  `DescribeStacks`, `DetectStackDrift`, etc.) plus permissions for every
  resource type the template provisions — CloudFormation executes as the
  calling principal by default, or as a dedicated **service role** if one
  is attached to the stack (recommended for least-privilege separation
  between "who can request a change" and "what the change is allowed to
  touch").
- Template format: YAML is preferred for authoring (supports comments,
  more concise intrinsic-function shorthand like `!Ref`/`!Sub`); JSON is
  fully equivalent and sometimes preferred for machine generation.
- `cfn-lint` installed for static template validation before any AWS call.
- For StackSets: an AWS Organizations setup (for service-managed
  permissions) or IAM roles (`AWSCloudFormationStackSetAdministrationRole`
  / `AWSCloudFormationStackSetExecutionRole`) pre-provisioned in target
  accounts for the self-managed permission model.
- Know which capabilities a template needs to acknowledge up front:
  `CAPABILITY_IAM` / `CAPABILITY_NAMED_IAM` (template creates IAM
  resources) and `CAPABILITY_AUTO_EXPAND` (template uses macros/nested
  transforms such as SAM) — deployments fail fast without these being
  explicitly passed, which is intentional friction so IAM-creating
  templates aren't applied unreviewed.

## Step-by-step guidance

1. **Author the template with parameters, not hardcoded values**, so the
   same template is reusable across environments:
   ```yaml
   AWSTemplateFormatVersion: "2010-09-09"
   Description: Application logging bucket with lifecycle policy

   Parameters:
     EnvironmentName:
       Type: String
       AllowedValues: [dev, staging, prod]
     RetentionInDays:
       Type: Number
       Default: 90

   Resources:
     LogsBucket:
       Type: AWS::S3::Bucket
       Properties:
         BucketName: !Sub "example-app-logs-${EnvironmentName}"
         LifecycleConfiguration:
           Rules:
             - Id: expire-logs
               Status: Enabled
               ExpirationInDays: !Ref RetentionInDays

   Outputs:
     BucketArn:
       Value: !GetAtt LogsBucket.Arn
       Export:
         Name: !Sub "${EnvironmentName}-app-logs-bucket-arn"
   ```
   The `Export` makes `BucketArn` consumable by other stacks via
   `Fn::ImportValue` — the basis of cross-stack references (step 3).

2. **Validate statically before touching AWS**:
   ```bash
   cfn-lint templates/logging-bucket.yaml
   aws cloudformation validate-template \
     --template-body file://templates/logging-bucket.yaml
   ```

3. **Split large templates into nested stacks, or use cross-stack exports**
   for looser coupling between independently-owned layers:
   ```yaml
   # root.yaml — nested stack (tight coupling, single deploy unit)
   Resources:
     NetworkStack:
       Type: AWS::CloudFormation::Stack
       Properties:
         TemplateURL: https://s3.amazonaws.com/<bucket>/network.yaml
         Parameters:
           EnvironmentName: !Ref EnvironmentName

     AppStack:
       Type: AWS::CloudFormation::Stack
       Properties:
         TemplateURL: https://s3.amazonaws.com/<bucket>/app.yaml
         Parameters:
           VpcId: !GetAtt NetworkStack.Outputs.VpcId
   ```
   Use **nested stacks** when the layers always deploy and version
   together (one owner, one release cadence). Use **cross-stack exports**
   (`Fn::ImportValue`) instead when layers are owned/updated by different
   teams on different cadences — an exported output can't be deleted or
   changed incompatibly while another stack still imports it, which
   CloudFormation enforces automatically and surfaces as a delete/update
   block, protecting the consumer.

4. **Never update a shared/production stack without reviewing a change
   set first**:
   ```bash
   aws cloudformation create-change-set \
     --stack-name app-logs-staging \
     --change-set-name update-retention-$(date +%Y%m%d%H%M) \
     --template-body file://templates/logging-bucket.yaml \
     --parameters ParameterKey=EnvironmentName,ParameterValue=staging \
                  ParameterKey=RetentionInDays,ParameterValue=30

   aws cloudformation describe-change-set \
     --stack-name app-logs-staging \
     --change-set-name update-retention-<timestamp>
   ```
   Read the `Changes` list: confirm each entry's `Action`
   (`Add`/`Modify`/`Remove`) and, for `Modify`, whether
   `Replacement: True` — a replacement means the resource is deleted and
   recreated (new physical ID), which matters a great deal for anything
   stateful (databases, buckets with data). Only after review:
   ```bash
   aws cloudformation execute-change-set \
     --stack-name app-logs-staging \
     --change-set-name update-retention-<timestamp>
   ```

5. **Roll the same template to many accounts/regions with a StackSet**
   instead of scripting per-account `create-stack` calls:
   ```bash
   aws cloudformation create-stack-set \
     --stack-set-name baseline-logging \
     --template-body file://templates/logging-bucket.yaml \
     --permission-model SERVICE_MANAGED \
     --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false \
     --capabilities CAPABILITY_NAMED_IAM

   aws cloudformation create-stack-instances \
     --stack-set-name baseline-logging \
     --deployment-targets OrganizationalUnitIds=<ou-id> \
     --regions us-east-1 eu-west-1 \
     --operation-preferences FailureTolerancePercentage=10,MaxConcurrentPercentage=25
   ```
   `SERVICE_MANAGED` permissions (via AWS Organizations) auto-provision the
   needed roles in member accounts; `SELF_MANAGED` requires the admin/
   execution roles to already exist in every target account.
   `FailureTolerancePercentage`/`MaxConcurrentPercentage` cap blast radius:
   a bad template stops rolling out after a bounded percentage of accounts
   fail, rather than plowing through the whole organization.

6. **Detect and reconcile drift** after any suspected manual change:
   ```bash
   aws cloudformation detect-stack-drift --stack-name app-logs-staging
   aws cloudformation describe-stack-resource-drifts \
     --stack-name app-logs-staging \
     --stack-resource-drift-status-filters MODIFIED DELETED
   ```
   For each `MODIFIED`/`DELETED` resource, decide: update the template to
   match reality (if the manual change should stick) or run an update to
   force the resource back to the template's declared state (if the
   manual change was unauthorized). CloudFormation does not auto-correct
   drift — detection is read-only and requires an explicit follow-up
   update.

7. **Treat stack deletion as destructive by default.**
   > **Warning:** `aws cloudformation delete-stack` deletes every resource
   > in the stack unless that resource's `DeletionPolicy` is set to
   > `Retain` or `Snapshot` — for a stateful resource (RDS instance, EBS
   > volume, S3 bucket with data) the default is to delete the underlying
   > data along with the stack. Before deleting any stack beyond a
   > scratch/dev environment: confirm `DeletionPolicy: Retain` (or
   > `Snapshot` for RDS/EBS) is set on every stateful resource, confirm
   > independent backups exist, and consider `--retain-resources` on a
   > targeted per-resource basis if only part of the stack should go away.
   ```yaml
   RetentionInDays: !Ref RetentionInDays
   AppDatabase:
     Type: AWS::RDS::DBInstance
     DeletionPolicy: Snapshot   # takes a final snapshot before deletion
     UpdateReplacePolicy: Snapshot
   ```

## Best practices

- Pin `AWSTemplateFormatVersion` and keep one resource's logical ID stable
  across template revisions — renaming a logical ID is treated as
  delete-old/create-new, not a rename, even if the underlying properties
  are identical.
- Use `Fn::Sub` and `Fn::GetAtt` over string concatenation for
  cross-resource references so CloudFormation can infer the dependency
  graph automatically; only fall back to explicit `DependsOn` when no
  attribute reference exists to express the ordering.
- Keep IAM policies embedded in the template scoped to specific resource
  ARNs (using `!GetAtt`/`!Ref` to the resource being granted access, not
  `Resource: "*"`), and require `CAPABILITY_NAMED_IAM` review by a human
  or a policy gate whenever a template creates or modifies IAM.
- Store templates and parameter files in version control, and drive
  `create-change-set`/`execute-change-set` from CI so every stack update
  has a reviewable diff and an audit trail, mirroring the plan-review gate
  described in
  [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md).
- Prefer many small, single-purpose stacks (network, data, app) over one
  monolithic template — smaller blast radius per update, faster change
  sets, and independent update cadences.
- Tag every stack (`aws cloudformation create-stack --tags Key=...`) so
  cost allocation and ownership are traceable; CloudFormation propagates
  stack-level tags to every resource that supports tagging.
- For anything needing OS-level configuration on top of provisioned
  compute (installing packages, managing config files, running services),
  don't fight CloudFormation's `UserData`/`cfn-init` for that — hand off
  to [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md)
  once the instance/AMI exists, and let CloudFormation own provisioning
  only.

## Common pitfalls

- **Symptom:** A change set shows `Replacement: True` for a resource that
  should just update in place.
  **Fix:** Some properties are immutable and force replacement (e.g.
  changing an RDS engine version incompatibly, or an S3 bucket's `Name`).
  Check the resource type's CloudFormation docs for which properties
  require replacement, and if replacement is unavoidable for a stateful
  resource, plan the swap explicitly (snapshot/restore, blue-green cutover)
  rather than letting the change set execute unreviewed.

- **Symptom:** `aws cloudformation update-stack` fails with `Export
  ... cannot be deleted as it is in use by <other-stack>`.
  **Fix:** This is CloudFormation protecting a cross-stack reference —
  find every consumer with
  `aws cloudformation list-imports --export-name <name>` and update or
  remove those consumers' imports first before the exporting stack can
  change or remove that output.

- **Symptom:** A stack sits in `UPDATE_ROLLBACK_FAILED` and no further
  updates are accepted.
  **Fix:** A resource failed to roll back automatically (often a
  permissions issue during rollback, or a resource modified outside
  CloudFormation mid-update). Use
  `aws cloudformation continue-update-rollback`, optionally with
  `--resources-to-skip` for the specific logical IDs that can't roll back
  cleanly, then reconcile those resources' actual state against the
  template afterward.

- **Symptom:** `detect-stack-drift` reports resources as `MODIFIED` even
  though nobody touched the console.
  **Fix:** Some AWS-managed background processes (e.g. automatic minor
  version patching on managed services) change attributes CloudFormation
  considers drift. Confirm whether the drifted property is one your
  template intentionally leaves unmanaged; if so, exclude it from drift
  concern in the runbook rather than chasing false positives every cycle.

- **Symptom:** A StackSet operation stops partway through with some
  account/region instances `FAILED` and others `SUCCEEDED`.
  **Fix:** Check `FailureTolerancePercentage` — a low tolerance stops the
  rollout deliberately to cap blast radius. Inspect
  `describe-stack-instance` for the failed target's reason (often a
  missing execution role in a newly-added account), fix that specific
  account, then re-run the operation only against the failed instances
  rather than the whole set.

## Worked example

**Scenario:** Deploy a baseline "application logging bucket" stack to
`staging` first via a reviewed change set, then promote the same template
to every account in an AWS Organizations OU via StackSets.

`templates/logging-bucket.yaml` (as shown in step 1), plus a parameter
file per environment, `params/staging.json`:
```json
[
  { "ParameterKey": "EnvironmentName", "ParameterValue": "staging" },
  { "ParameterKey": "RetentionInDays", "ParameterValue": "30" }
]
```

Stage 1 — single-account review and apply:
```bash
cfn-lint templates/logging-bucket.yaml

aws cloudformation create-change-set \
  --stack-name app-logs-staging \
  --change-set-name initial-deploy \
  --template-body file://templates/logging-bucket.yaml \
  --parameters file://params/staging.json

aws cloudformation describe-change-set \
  --stack-name app-logs-staging --change-set-name initial-deploy
# Reviewer confirms: 1 resource to Add (LogsBucket), no Modify/Remove.

aws cloudformation execute-change-set \
  --stack-name app-logs-staging --change-set-name initial-deploy

aws cloudformation wait stack-update-complete --stack-name app-logs-staging
```

Stage 2 — org-wide rollout once staging is validated:
```bash
aws cloudformation create-stack-set \
  --stack-set-name baseline-logging \
  --template-body file://templates/logging-bucket.yaml \
  --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=true,RetainStacksOnAccountRemoval=false \
  --parameters ParameterKey=EnvironmentName,ParameterValue=prod \
               ParameterKey=RetentionInDays,ParameterValue=90

aws cloudformation create-stack-instances \
  --stack-set-name baseline-logging \
  --deployment-targets OrganizationalUnitIds=ou-example-12345678 \
  --regions us-east-1 eu-west-1 \
  --operation-preferences FailureTolerancePercentage=10,MaxConcurrentPercentage=25

aws cloudformation list-stack-instances --stack-set-name baseline-logging
```
Six months later, a drift check confirms nothing was hand-edited:
```bash
aws cloudformation detect-stack-drift --stack-name app-logs-staging
aws cloudformation describe-stack-resource-drifts \
  --stack-name app-logs-staging \
  --stack-resource-drift-status-filters MODIFIED DELETED
# Empty result: no drift.
```

## Cross-references

- [infrastructure-as-code-terraform](../../../devops/skills/infrastructure-as-code-terraform/SKILL.md)
- [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md)
- [python-automation-scripting-for-ops](../python-automation-scripting-for-ops/SKILL.md)
