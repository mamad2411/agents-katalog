---
name: feature-flag
description: Create, enable, disable, or list feature flags backed by AWS AppConfig. Generates the CDK construct, backend isFlagEnabled() utility, and frontend useFlag() React hook. Usage — /feature-flag <create|enable|disable|list> [flag-name] [--env staging|prod]
argument-hint: "<create|enable|disable|list> [flag-name] [--env staging|prod]"
arguments:
  - name: subcommand
    description: "create, enable, disable, or list"
  - name: flag
    description: "Flag name in kebab-case (e.g. new-checkout-flow)"
  - name: env
    description: "Target environment: staging or prod (default: staging)"
user-invocable: true
stack: cloud/aws
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(aws *)
  - Bash(gh *)
  - Bash(find *)
  - Bash(ls *)
  - Bash(grep *)
  - Bash(npm *)
---

# Feature Flag

Parse `$ARGUMENTS[0]` as subcommand, `$ARGUMENTS[1]` as flag name (kebab-case), `--env` as environment.

Feature flags use **AWS AppConfig** — zero extra SaaS cost, IAM-controlled, real-time updates without redeploy.

---

## `/feature-flag create <flag-name>`

### Step 1 — Bootstrap AppConfig infrastructure (once per project)

Check if AppConfig CDK construct exists:

```bash
grep -r 'AppConfig\|appconfig' infra/ --include='*.ts' | head -5
```

If not yet set up, append to the appropriate stack (usually `infra/lib/api-stack.ts` or a new `FlagsStack`):

```ts
// infra/lib/flags-stack.ts
import * as appconfig from 'aws-cdk-lib/aws-appconfig'
import * as iam from 'aws-cdk-lib/aws-iam'

export class FlagsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: FlagsStackProps) {
    super(scope, id, props)

    const app = new appconfig.CfnApplication(this, 'App', {
      name: `${props.projectName}-flags`,
    })

    const env = new appconfig.CfnEnvironment(this, 'Env', {
      applicationId: app.ref,
      name: props.environment,   // 'staging' | 'prod'
    })

    // Feature flags config profile — freeform JSON
    const profile = new appconfig.CfnConfigurationProfile(this, 'FlagsProfile', {
      applicationId: app.ref,
      name: 'feature-flags',
      locationUri: 'hosted',
      type: 'AWS.AppConfig.FeatureFlags',
    })

    // Initial hosted config version — all flags off by default
    const initialConfig = new appconfig.CfnHostedConfigurationVersion(this, 'InitialFlags', {
      applicationId: app.ref,
      configurationProfileId: profile.ref,
      content: JSON.stringify({ flags: {}, values: {}, version: '1' }),
      contentType: 'application/json',
    })

    // Allow Lambda execution roles to read flags
    // Grant in ApiStack: flagsReader.grantRead(apiLambda.role!)
    const flagsReader = new iam.PolicyStatement({
      actions: [
        'appconfig:StartConfigurationSession',
        'appconfig:GetLatestConfiguration',
      ],
      resources: [`arn:aws:appconfig:${this.region}:${this.account}:application/${app.ref}/*`],
    })

    // Outputs for other stacks
    new cdk.CfnOutput(this, 'AppId', { value: app.ref, exportName: `${props.projectName}-flags-app-id` })
    new cdk.CfnOutput(this, 'EnvId', { value: env.ref, exportName: `${props.projectName}-flags-env-id` })
    new cdk.CfnOutput(this, 'ProfileId', { value: profile.ref, exportName: `${props.projectName}-flags-profile-id` })
  }
}
```

### Step 2 — Create backend utility (once per project)

Create `src/lib/flags.ts` if it doesn't exist:

```ts
// src/lib/flags.ts
import {
  AppConfigDataClient,
  StartConfigurationSessionCommand,
  GetLatestConfigurationCommand,
} from '@aws-sdk/client-appconfigdata'
import { logger } from './logger'

const client = new AppConfigDataClient({ region: process.env.AWS_REGION ?? 'us-east-1' })

// Cache config in Lambda memory between invocations (TTL: 30s)
let cachedToken: string | undefined
let cachedFlags: Record<string, boolean> = {}
let cacheExpiry = 0

async function fetchFlags(): Promise<Record<string, boolean>> {
  const now = Date.now()
  if (now < cacheExpiry && cachedToken) {
    const res = await client.send(new GetLatestConfigurationCommand({ ConfigurationToken: cachedToken }))
    if (res.Configuration && res.Configuration.length > 0) {
      const data = JSON.parse(Buffer.from(res.Configuration).toString())
      cachedFlags = parseFlags(data)
    }
    cachedToken = res.NextPollConfigurationToken
    cacheExpiry = now + (res.NextPollIntervalInSeconds ?? 30) * 1000
    return cachedFlags
  }

  // Start a new session
  const session = await client.send(new StartConfigurationSessionCommand({
    ApplicationIdentifier: process.env.APPCONFIG_APP_ID!,
    EnvironmentIdentifier: process.env.APPCONFIG_ENV_ID!,
    ConfigurationProfileIdentifier: process.env.APPCONFIG_PROFILE_ID!,
    RequiredMinimumPollIntervalInSeconds: 30,
  }))
  cachedToken = session.InitialConfigurationToken!
  return fetchFlags()
}

function parseFlags(data: Record<string, unknown>): Record<string, boolean> {
  const flags: Record<string, boolean> = {}
  const values = (data.values as Record<string, { enabled: boolean }>) ?? {}
  Object.entries(values).forEach(([key, val]) => {
    flags[key] = val.enabled === true
  })
  return flags
}

export async function isFlagEnabled(flagName: string, fallback = false): Promise<boolean> {
  try {
    const flags = await fetchFlags()
    return flags[flagName] ?? fallback
  } catch (err) {
    logger.warn({ flagName, err }, 'Feature flag fetch failed — using fallback')
    return fallback
  }
}
```

Install SDK if needed:
```bash
npm install @aws-sdk/client-appconfigdata
```

### Step 3 — Create frontend hook (once per project)

Create `src/hooks/useFlag.ts` if it doesn't exist:

```ts
// src/hooks/useFlag.ts
import { useQuery } from '@tanstack/react-query'
import { apiClient } from '../lib/api'

interface FlagsResponse {
  flags: Record<string, boolean>
}

// Backend exposes a /api/v1/flags endpoint (read-only, cached)
// Do NOT call AppConfig directly from the frontend — it would expose AWS credentials
async function fetchFlags(): Promise<Record<string, boolean>> {
  const res = await apiClient.get<FlagsResponse>('/api/v1/flags')
  return res.data.flags
}

export function useFlag(flagName: string, fallback = false): boolean {
  const { data } = useQuery({
    queryKey: ['feature-flags'],
    queryFn: fetchFlags,
    staleTime: 30_000,   // Re-fetch every 30s
    gcTime: 60_000,
    throwOnError: false,
  })
  return data?.[flagName] ?? fallback
}

// Usage:
// const isNewCheckoutEnabled = useFlag('new-checkout-flow')
// if (!isNewCheckoutEnabled) return <OldCheckout />
// return <NewCheckout />
```

Add the flags endpoint to the backend:

```ts
// src/controllers/flags.controller.ts
import { asyncHandler } from '../lib/async-handler'
import { ok } from '../lib/response'
import { isFlagEnabled } from '../lib/flags'

// GET /api/v1/flags — returns all flag values (no auth required, flags are not secrets)
export const getFlags = asyncHandler(async (req, res) => {
  // List all known flags — add new flag names here when you create them
  const FLAG_NAMES = [
    '<flag-name>',
    // add more flags here
  ]

  const flags: Record<string, boolean> = {}
  await Promise.all(
    FLAG_NAMES.map(async name => {
      flags[name] = await isFlagEnabled(name)
    })
  )

  ok(res, { flags })
})
```

### Step 4 — Register the new flag

Add the specific flag to AppConfig via the AWS console or CLI:

```bash
# Get IDs from CDK outputs
APP_ID=$(aws cloudformation describe-stacks \
  --stack-name FlagsStack \
  --query "Stacks[0].Outputs[?OutputKey=='AppId'].OutputValue" \
  --output text)

# Add flag via CLI (starts disabled)
# Note: AppConfig Feature Flags format requires the GUI for first setup;
# for subsequent flags, the hosted config JSON is updated directly

echo "Flag '<flag-name>' created — currently DISABLED in all environments."
echo "To enable: /feature-flag enable <flag-name> --env staging"
```

Also add the flag name to the `FLAG_NAMES` array in `flags.controller.ts`.

---

## `/feature-flag enable <flag-name> --env <env>`

```bash
ENV=${env:-staging}
APP_ID=$(aws ssm get-parameter --name "/<project>/$ENV/appconfig/app-id" --query Parameter.Value --output text)
ENV_ID=$(aws ssm get-parameter --name "/<project>/$ENV/appconfig/env-id" --query Parameter.Value --output text)
PROFILE_ID=$(aws ssm get-parameter --name "/<project>/$ENV/appconfig/profile-id" --query Parameter.Value --output text)

# Get current config
CURRENT=$(aws appconfig get-configuration \
  --application "$APP_ID" \
  --environment "$ENV_ID" \
  --configuration "$PROFILE_ID" \
  --client-id cli /tmp/flags.json && cat /tmp/flags.json)

# Toggle flag on
echo "$CURRENT" | node -e "
const d = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'))
d.values = d.values || {}
d.values['<flag-name>'] = { enabled: true }
console.log(JSON.stringify(d, null, 2))
" > /tmp/updated-flags.json

# Deploy updated config
aws appconfig create-hosted-configuration-version \
  --application-id "$APP_ID" \
  --configuration-profile-id "$PROFILE_ID" \
  --content-type 'application/json' \
  --content fileb:///tmp/updated-flags.json \
  --query 'VersionNumber' --output text
```

Confirm:
> ✅ Flag `<flag-name>` **enabled** in `<env>`.
> Takes effect within 30 seconds (AppConfig poll interval).
> No redeploy required.

---

## `/feature-flag disable <flag-name> --env <env>`

Same as enable but sets `enabled: false`. Always confirm before disabling in prod.

> ⚠️ Disabling `<flag-name>` in **production** will immediately hide the feature for all users.
> Confirm? (yes / no)

---

## `/feature-flag list`

```bash
# List all known flags and their status per environment
for ENV in staging prod; do
  echo "=== $ENV ==="
  aws appconfig get-configuration ... | node -e "
  const d = JSON.parse(...)
  Object.entries(d.values||{}).forEach(([k,v]) => console.log(v.enabled?'✅':'🔴', k))
  "
done
```

**Related skills — apply together:**
- `security` — the `/api/v1/flags` endpoint must not expose sensitive flag names that reveal unreleased features to competitors
- `cdk` — FlagsStack follows the same stack boundary and SSM export patterns
- `validate` — after enabling a flag, run `/validate <issue>` to confirm the feature is working
- `dev-code` — wrap every new feature in `if (await isFlagEnabled('<flag>'))` from day one, remove the flag after validation
