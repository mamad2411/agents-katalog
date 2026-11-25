---
name: synthetic
description: Set up and manage CloudWatch Synthetics canary — continuous read-only health checks running every minute in production. Usage — /synthetic <setup|status|pause|resume>
argument-hint: "setup | status | pause | resume [--env prod|staging]"
arguments:
  - name: subcommand
    description: "'setup' to create canary CDK construct, 'status' to check last runs, 'pause' to stop, 'resume' to restart"
user-invocable: true
stack: cloud/aws
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(aws *)
  - Bash(node *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(date *)
  - Bash(ls *)
---

# Synthetic Monitoring

Parse `$ARGUMENTS[0]` as `setup` | `status` | `pause` | `resume` (default: `status`).
Parse `--env` (default: `prod`).

CloudWatch Synthetics canaries are Node.js scripts that run on a schedule inside AWS, hitting your endpoints just like a real user. A failed canary triggers a CloudWatch alarm — catching outages before users report them.

---

## `/synthetic setup`

### Step 1 — Understand what to monitor

```bash
# What public endpoints should always respond?
grep -rn "router\.get\b" src/routes/ 2>/dev/null | grep -v ':id' | head -10

# Is there an existing canary?
aws synthetics describe-canaries --query 'Canaries[].Name' --output text 2>/dev/null
```

Show the user a proposed canary plan:
> **Proposed canary checks (every 1 minute):**
> 1. `GET /health` → expect 200, body `{"status":"ok"}`
> 2. `GET /api/v1/products` → expect 200 (public endpoint)
> 3. Frontend home page → expect page title, no error text
>
> Shall I proceed with these? (yes / add more / change)

Wait for confirmation before writing any files.

---

### Step 2 — Create the canary script

Create `infra/canary/canary.js` (CloudWatch Synthetics Node.js runtime format):

```js
// infra/canary/canary.js
// CloudWatch Synthetics canary — runs every minute in AWS
// Read-only: never mutates state

const synthetics = require('Synthetics')
const log        = require('SyntheticsLogger')

const BASE_URL = process.env.BASE_URL   // injected from CDK EnvironmentVariables

async function checkHealth() {
  const res = await synthetics.executeHttpStep('GET /health', {
    hostname: new URL(BASE_URL).hostname,
    path:     '/health',
    method:   'GET',
    protocol: 'https:',
    port:     443,
  }, async (response) => {
    const body = await new Promise((resolve) => {
      let data = ''
      response.on('data', chunk => data += chunk)
      response.on('end', () => resolve(data))
    })
    const json = JSON.parse(body)
    if (response.statusCode !== 200) throw new Error(`/health returned ${response.statusCode}`)
    if (json.status !== 'ok') throw new Error(`/health body: ${body}`)
    log.info('/health OK')
  })
}

async function checkApiProducts() {
  await synthetics.executeHttpStep('GET /api/v1/products', {
    hostname: new URL(BASE_URL).hostname,
    path:     '/api/v1/products',
    method:   'GET',
    protocol: 'https:',
    port:     443,
  }, async (response) => {
    if (response.statusCode !== 200) {
      throw new Error(`/api/v1/products returned ${response.statusCode}`)
    }
    log.info('/api/v1/products OK')
  })
}

async function checkFrontend() {
  const page = await synthetics.getPage()
  await page.goto(`${BASE_URL}/`, { waitUntil: 'domcontentloaded', timeout: 10000 })
  const title = await page.title()
  if (!title) throw new Error('Home page has no title')

  const body = await page.content()
  if (body.includes('Internal Server Error') || body.includes('Application error')) {
    throw new Error('Frontend shows error page')
  }
  log.info('Frontend home page OK')
}

exports.handler = async () => {
  await checkHealth()
  await checkApiProducts()
  await checkFrontend()
}
```

---

### Step 3 — Add canary CDK construct to MonitoringStack

Append to `infra/lib/monitoring-stack.ts`:

```ts
import * as synthetics from 'aws-cdk-lib/aws-synthetics'
import * as s3 from 'aws-cdk-lib/aws-s3'
import * as iam from 'aws-cdk-lib/aws-iam'
import * as path from 'path'

// ─── CloudWatch Synthetics Canary ─────────────────────────────────────────────

// S3 bucket for canary artefacts (screenshots, HAR files on failure)
const canaryBucket = new s3.Bucket(this, 'CanaryArtifacts', {
  bucketName: `${projectName}-${env}-canary-artifacts`,
  lifecycleRules: [{
    expiration: cdk.Duration.days(30),   // keep 30 days of screenshots
  }],
  removalPolicy: cdk.RemovalPolicy.DESTROY,
  autoDeleteObjects: true,
  encryption: s3.BucketEncryption.S3_MANAGED,
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
})

// IAM role for canary execution
const canaryRole = new iam.Role(this, 'CanaryRole', {
  assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
  managedPolicies: [
    iam.ManagedPolicy.fromAwsManagedPolicyName('CloudWatchSyntheticsFullAccess'),
  ],
  inlinePolicies: {
    CanaryS3: new iam.PolicyDocument({
      statements: [new iam.PolicyStatement({
        actions: ['s3:PutObject', 's3:GetObject'],
        resources: [`${canaryBucket.bucketArn}/*`],
      })],
    }),
  },
})

// The canary itself
const canary = new synthetics.Canary(this, 'HealthCanary', {
  canaryName: `${projectName}-${env}-health`,
  schedule: synthetics.Schedule.rate(cdk.Duration.minutes(1)),
  runtime: synthetics.Runtime.SYNTHETICS_NODEJS_PUPPETEER_6_2,
  test: synthetics.Test.custom({
    code: synthetics.Code.fromAsset(path.join(__dirname, '../../canary')),
    handler: 'canary.handler',
  }),
  artifactsBucketLocation: { bucket: canaryBucket },
  role: canaryRole,
  environmentVariables: {
    BASE_URL: `https://${domainParam.valueAsString}`,  // SSM or CfnParameter
  },
  // Keep 30 days of run history
  successRetentionPeriod: cdk.Duration.days(30),
  failureRetentionPeriod: cdk.Duration.days(30),
})

// CloudWatch alarm — fires when canary fails 2 consecutive runs
const canaryAlarm = new cloudwatch.Alarm(this, 'CanaryFailed', {
  alarmName: `${projectName}-${env}-canary-failed`,
  metric: new cloudwatch.Metric({
    namespace: 'CloudWatchSynthetics',
    metricName: 'Failed',
    dimensionsMap: {
      CanaryName: canary.canaryName,
    },
    statistic: 'Sum',
    period: cdk.Duration.minutes(2),
  }),
  threshold: 1,
  evaluationPeriods: 2,          // 2 consecutive failed runs
  comparisonOperator: cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
  alarmDescription: 'Canary check failed — environment may be down',
  treatMissingData: cloudwatch.TreatMissingData.BREACHING,  // missing data = problem
})

// Wire to existing alert SNS topic
canaryAlarm.addAlarmAction(new actions.SnsAction(alertTopic))
canaryAlarm.addOkAction(new actions.SnsAction(alertTopic))   // notify on recovery too
```

---

### Step 4 — Deploy the canary

```bash
ENV=prod
cd infra
npx cdk deploy MonitoringStack --require-approval never

echo "=== Verifying canary created ==="
aws synthetics describe-canaries \
  --query 'Canaries[?contains(Name, `health`)].{Name:Name,Status:Status.State}' \
  --output table
```

---

### Step 5 — Confirm first run

```bash
# Wait for first run (canaries start within ~30 seconds of creation)
sleep 90

aws synthetics get-canary-runs \
  --name "$(node -p "require('./package.json').name")-${ENV}-health" \
  --query 'CanaryRuns[0].{Status:Status.State,Reason:Status.StateReason,Duration:Timeline.Duration}' \
  --output table
```

> **Canary setup complete:**
> - Name: `<project>-prod-health`
> - Schedule: every 1 minute
> - Checks: /health · /api/v1/products · frontend home
> - Artefacts: s3://<project>-prod-canary-artifacts/
> - Alert: SNS → <alert-topic>
>
> First run: ✅ PASSED (1.2s)

---

## `/synthetic status`

Show the last N canary runs and current alarm state:

```bash
ENV=prod
PROJECT=$(node -p "require('./package.json').name")
CANARY_NAME="${PROJECT}-${ENV}-health"

echo "=== Last 10 canary runs ==="
aws synthetics get-canary-runs \
  --name "$CANARY_NAME" \
  --query 'CanaryRuns[:10].{Time:Timeline.Started,Status:Status.State,Duration:Timeline.Duration,Reason:Status.StateReason}' \
  --output table

echo "=== Canary alarm state ==="
aws cloudwatch describe-alarms \
  --alarm-names "${PROJECT}-${ENV}-canary-failed" \
  --query 'MetricAlarms[0].{State:StateValue,Reason:StateReason,Updated:StateUpdatedTimestamp}' \
  --output table
```

Present a compact summary:

> **Synthetic monitor status — `prod`**
>
> | Run | Time | Result | Duration |
> |---|---|---|---|
> | Latest | 14:02 UTC | ✅ PASSED | 1.1s |
> | -1 | 14:01 UTC | ✅ PASSED | 0.9s |
> | -2 | 14:00 UTC | ✅ PASSED | 1.0s |
>
> Alarm: ✅ OK — no incidents in last 10 runs
>
> Last failure: (none in last 10 runs)

If any runs are FAILED:
> ⚠️ **Failures detected.** Check canary screenshots:
> `aws s3 ls s3://<project>-prod-canary-artifacts/ --recursive | grep screenshot`

---

## `/synthetic pause`

Stop the canary (e.g., during a planned maintenance window):

```bash
PROJECT=$(node -p "require('./package.json').name")
CANARY_NAME="${PROJECT}-${ENV}-health"

aws synthetics stop-canary --name "$CANARY_NAME"
echo "⏸  Canary paused: $CANARY_NAME"
echo "Resume with: /synthetic resume --env ${ENV}"
```

---

## `/synthetic resume`

```bash
PROJECT=$(node -p "require('./package.json').name")
CANARY_NAME="${PROJECT}-${ENV}-health"

aws synthetics start-canary --name "$CANARY_NAME"
echo "▶️  Canary resumed: $CANARY_NAME"
```

---

## Adding a new canary check

When a new critical endpoint is added (via `/dev-code`), update `infra/canary/canary.js`:

```js
// Add to exports.handler:
async function checkNewEndpoint() {
  await synthetics.executeHttpStep('GET /api/v1/<resource>', {
    hostname: new URL(BASE_URL).hostname,
    path:     '/api/v1/<resource>',
    method:   'GET',
    protocol: 'https:',
    port:     443,
  }, async (response) => {
    if (![200, 401].includes(response.statusCode)) {
      throw new Error(`/api/v1/<resource> returned unexpected ${response.statusCode}`)
    }
    log.info('/api/v1/<resource> OK')
  })
}
```

Then redeploy MonitoringStack: `npx cdk deploy MonitoringStack`

---

## Canary vs smoke — when to use which

| | `/test-smoke` | `/synthetic` |
|---|---|---|
| **When** | On demand — immediately after deploy | Continuous — every 1 minute, always running |
| **Trigger** | Manual / CI post-deploy step | Automated — CloudWatch alarm fires on failure |
| **Scope** | Broader (more checks, some with retries) | Minimal (critical paths only, fast) |
| **Failure action** | Rollback recommendation in terminal | CloudWatch alarm → SNS → PagerDuty/Slack |
| **Cost** | Free (local Playwright) | ~$0.0012 per run (~$1.73/month at 1/min) |

**Related skills — apply together:**
- `test-smoke` — run `/test-smoke` immediately post-deploy; `/synthetic` runs continuously
- `slo` — canary failures contribute to SLO error budget burn
- `validate` — combine: smoke (immediate) + synthetic (ongoing) + validate (1h, 24h)
- `deploy` — canary alarm can trigger automated rollback via SNS → Lambda
- `monitoring` — synthetic alarms live alongside Lambda/DynamoDB/API Gateway alarms in the same MonitoringStack
