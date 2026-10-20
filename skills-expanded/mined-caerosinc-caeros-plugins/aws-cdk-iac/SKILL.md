---
name: aws-cdk-iac
description: Author AWS infrastructure with CDK v2 and CloudFormation, including project setup, construct levels, Mixins, express deploys, diff discipline, and stateful-resource safety. Use when the user is writing or reviewing IaC for AWS.
---

# AWS CDK v2 and CloudFormation

CDK v2 is the only supported CDK line: one library, `aws-cdk-lib`, plus
`constructs`. The CLI (`aws-cdk`) versions independently of the library.

```bash
npm install -g aws-cdk
mkdir my-app && cd my-app
cdk init app --language typescript   # also: python, java, csharp, go
cdk bootstrap aws://ACCOUNT_ID/us-east-1   # once per account/region
```

Core loop: `cdk synth` (emit CloudFormation), `cdk diff` (compare to
deployed), `cdk deploy`, `cdk destroy`. During development, `cdk watch`
hot-swaps supported resources (Lambda code, ECS images) without a full
CloudFormation deploy: never use hotswap against production.

## Construct levels

- **L1** (`Cfn*`): raw CloudFormation, 1:1 with resource schemas.
- **L2**: curated classes with sane defaults, `grant*()` methods, and
  `metric*()` helpers. Prefer these.
- **L3 / patterns**: multi-resource abstractions (`aws-ecs-patterns`, etc.).
- **Mixins** (GA 2026, in `aws-cdk-lib`): composable capabilities you apply
  to existing L1/L2/custom constructs instead of switching construct class.

Escape hatch when an L2 lacks a property:

```ts
const cfnBucket = bucket.node.defaultChild as s3.CfnBucket;
cfnBucket.addPropertyOverride("AnalyticsConfigurations", [...]);
```

## Deploy speed and validation (2026)

- `cdk deploy --express`: CloudFormation express mode, up to 4x faster
  stack operations, no template changes needed.
- Pre-deployment validation now runs by default on `cdk deploy` and
  `cdk validate`, with construct-level tracing in the report. Fix findings
  before they become mid-deploy rollbacks.

## Patterns that keep stacks maintainable

- One stack per deployment boundary (network, data, app), wired with typed
  props, not `Fn.importValue` strings. CDK generates cross-stack exports
  automatically when you pass constructs between stacks.
- Pin environments explicitly: `new AppStack(app, "AppProd", { env:
  { account: "111111111111", region: "us-east-1" } })`. Env-agnostic stacks
  cannot do context lookups (VPC, AZs).
- Context lookups cache into `cdk.context.json`: commit it, and refresh
  deliberately with `cdk context --reset KEY` when the environment changes.

## Safety rules

- **Logical ID stability**: renaming a construct or moving it in the tree
  changes its logical ID, which CloudFormation treats as delete + create.
  Never refactor IDs on stateful resources without `cdk diff` proving no
  replacement.
- **Stateful resources**: set `removalPolicy: RemovalPolicy.RETAIN` (or
  `SNAPSHOT`) on databases, buckets, and tables. Many L2s default to RETAIN
  but verify per construct.
- Run `cdk diff` in CI and require human review when the diff includes
  `[-]` (destroy) or replacement markers on stateful types.
- Bootstrap stack drift: a too-old bootstrap version fails deploys with a
  clear version error, fix with `cdk bootstrap` re-run per account/region.

## Raw CloudFormation, when you must

Prefer CDK, but for handwritten templates: validate with `cfn-lint`
(`pip install cfn-lint`), deploy via change sets so you can review first:

```bash
aws cloudformation deploy --template-file t.yaml --stack-name s \
  --capabilities CAPABILITY_NAMED_IAM --no-execute-changeset
aws cloudformation describe-change-set --change-set-name ... # review
```

`cdk migrate --stack-name existing-stack` converts a deployed stack or
template into a CDK app when adopting CDK incrementally.

Authoritative docs: https://docs.aws.amazon.com/cdk/v2/guide/ (the
`aws-knowledge` MCP server in this plugin searches them live).
