---
name: cdk
description: AWS CDK standards — stack structure, construct patterns, environment config, security defaults, deployment. Load when writing or reviewing CDK infrastructure code.
user-invocable: false
stack: cloud/aws
paths:
  - "infra/**"
  - "cdk/**"
  - "**/*stack*.ts"
  - "**/*Stack*.ts"
---

Full standards in [cdk.md](cdk.md). Always-on summary:

**Stack structure:** one stack per logical boundary (ApiStack, FrontendStack, DatabaseStack, AuthStack). Share via SSM or stack outputs — not cross-stack references.

**Construct rules:**
- L2 constructs always (never L1 CfnXxx unless no L2 exists)
- Removal policy: `RETAIN` for databases in prod, `DESTROY` for ephemeral resources
- Always tag: `environment`, `project`, `owner`

**Security defaults:**
- Lambda: no wildcard IAM (`*`) — grant specific actions on specific resources
- S3: `blockPublicAccess: BlockPublicAccess.BLOCK_ALL`
- API Gateway: auth required on every route except `/health`
- Secrets: SSM SecureString or Secrets Manager — never stack parameters

**cdk-nag (always on):**
- Add `Aspects.of(app).add(new AwsSolutionsChecks({ verbose: true }))` to every `bin/app.ts`
- Install: `npm install -D cdk-nag`
- Catches IAM wildcards, public S3, missing PITR, deprecated runtimes at `cdk synth` — before any deploy
- Every `NagSuppressions` call must include a `reason` string

**Never:**
- `--require-approval never` in prod CI without explicit env gate
- Hard-code account IDs or region strings — use `Stack.of(this).account`
- `cdk destroy` in CI on non-ephemeral environments
- Suppress a cdk-nag rule without a written justification


**Related skills — apply together:**
- `security` — IAM least-privilege, S3 block public access, Cognito auth on every route
- `monitoring` — CloudWatch alarms and EMF metrics are CDK constructs in MonitoringStack
- `database-nosql` — DynamoDB table construct, GSI, and removal policy live in DatabaseStack
- `pipeline` — `cdk deploy` runs behind the environment approval gate in GitHub Actions