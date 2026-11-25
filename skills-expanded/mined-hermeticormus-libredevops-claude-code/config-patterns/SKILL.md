---
name: config-patterns
description: "Configuration patterns: SSM Parameter Store hierarchy and IAM access, Kubernetes ConfigMaps and Secrets, Unleash feature flags and rollout sequence, config schema validation, and Consul Template for dynamic config. Use when structuring application config or rolling out feature flags."
---

# Config Patterns

Configuration management patterns with SSM Parameter Store, Consul, feature flags, and schema validation.

## SSM Parameter Store Hierarchy

```
/myapp/
├── dev/
│   ├── database/url        (SecureString)
│   ├── database/pool_size  (String: "10")
│   ├── redis/url           (String)
│   └── features/           (StringList or JSON)
├── staging/
│   └── ...
└── prod/
    ├── database/url        (SecureString, KMS key: alias/myapp-prod)
    ├── database/pool_size  (String: "50")
    └── api/stripe_key      (SecureString)
```

```bash
# Write parameters with KMS encryption
aws ssm put-parameter \
  --name "/myapp/prod/database/url" \
  --value "postgresql://app:$(pass show db/prod)@db.prod.example.com:5432/myapp" \
  --type SecureString \
  --key-id "alias/myapp-prod" \
  --overwrite

# Read all parameters for an environment
aws ssm get-parameters-by-path \
  --path "/myapp/prod" \
  --recursive \
  --with-decryption \
  --output json | jq '.Parameters | map({(.Name | split("/") | last): .Value}) | add'

# Read single parameter
aws ssm get-parameter \
  --name "/myapp/prod/database/url" \
  --with-decryption \
  --query 'Parameter.Value' \
  --output text

# Copy parameters between environments
aws ssm get-parameters-by-path --path /myapp/staging --recursive --with-decryption \
  | jq -r '.Parameters[] | "aws ssm put-parameter --name \(.Name | sub("staging";"prod")) --value \"\(.Value)\" --type \(.Type) --overwrite"' \
  | bash
```

```python
# Python: Load all env config from SSM at startup
import boto3
import os

def load_ssm_config(path_prefix: str) -> dict:
    ssm = boto3.client('ssm', region_name='us-east-1')
    params = {}
    paginator = ssm.get_paginator('get_parameters_by_path')
    for page in paginator.paginate(
        Path=path_prefix,
        Recursive=True,
        WithDecryption=True
    ):
        for p in page['Parameters']:
            key = p['Name'].replace(path_prefix, '').lstrip('/').replace('/', '_').upper()
            params[key] = p['Value']
    return params

# On startup: load into environment
config = load_ssm_config(f"/myapp/{os.environ['ENV']}")
os.environ.update(config)
```

## IAM Policy for SSM Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadAppConfig",
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters",
        "ssm:GetParametersByPath"
      ],
      "Resource": "arn:aws:ssm:us-east-1:ACCOUNT:parameter/myapp/prod/*"
    },
    {
      "Sid": "DecryptSecureStrings",
      "Effect": "Allow",
      "Action": "kms:Decrypt",
      "Resource": "arn:aws:kms:us-east-1:ACCOUNT:key/KEY_ID",
      "Condition": {
        "StringEquals": {
          "kms:EncryptionContext:PARAMETER_ARN": "arn:aws:ssm:us-east-1:ACCOUNT:parameter/myapp/prod/*"
        }
      }
    }
  ]
}
```

## Kubernetes ConfigMap and Secret

```yaml
# Non-sensitive config as ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: production
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  MAX_WORKERS: "8"
  REDIS_HOST: "redis.production.svc.cluster.local"
  # Structured config as JSON
  feature_config.json: |
    {
      "newCheckout": false,
      "maxRetries": 3,
      "timeoutSeconds": 30
    }
---
# Deployment: mount ConfigMap as env + file
spec:
  containers:
    - name: app
      envFrom:
        - configMapRef:
            name: myapp-config
      volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
  volumes:
    - name: config
      configMap:
        name: myapp-config
        items:
          - key: feature_config.json
            path: feature_config.json
```

## Feature Flag Patterns with Unleash

```yaml
# Unleash self-hosted via Docker Compose
version: "3.8"
services:
  unleash:
    image: unleashorg/unleash-server:latest
    ports: ["4242:4242"]
    environment:
      DATABASE_URL: "postgres://unleash:password@db/unleash"
      SECURESESSION: "true"
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: unleash
      POSTGRES_USER: unleash
      POSTGRES_PASSWORD: password
    healthcheck:
      test: [CMD-SHELL, pg_isready -U unleash]
      interval: 5s
```

```python
# Python Unleash client with gradual rollout
from UnleashClient import UnleashClient

client = UnleashClient(
    url="https://unleash.internal.example.com",
    app_name="myapp",
    custom_headers={'Authorization': os.environ['UNLEASH_API_KEY']}
)
client.initialize_client()

# Percentage rollout evaluation
def process_checkout(user_id: str, cart: dict):
    context = {"userId": user_id, "properties": {"plan": user.plan}}

    if client.is_enabled("new-checkout-flow", context):
        return new_checkout_handler(cart)
    else:
        return legacy_checkout_handler(cart)
```

```javascript
// LaunchDarkly Node.js SDK
const LaunchDarkly = require('@launchdarkly/node-server-sdk');

const ldClient = LaunchDarkly.init(process.env.LAUNCHDARKLY_SDK_KEY);

// Wait for SDK to initialize (do this once at startup)
await ldClient.waitForInitialization();

// Evaluate flag with user context
const user = {
  kind: 'user',
  key: userId,
  email: userEmail,
  plan: userPlan,
  country: 'US'
};

const showNewFeature = await ldClient.variation('new-payment-flow', user, false);
// false = default value if flag doesn't exist or SDK fails
```

## Feature Flag Rollout Sequence

```
Phase 1 - Internal (0% users):
  Target: email matches "*@mycompany.com"
  Monitor: 1 week, zero errors

Phase 2 - Canary (1%):
  Target: random 1% by user ID hash
  Monitor: 48 hours, error rate < 0.1%

Phase 3 - Beta (10%):
  Target: random 10%
  Monitor: 1 week, p99 latency unchanged

Phase 4 - Wide (50%):
  Target: random 50%
  Monitor: 3 days

Phase 5 - General Availability (100%):
  Target: everyone
  Keep flag for 2 weeks as kill switch
  Then: remove flag + dead code path
```

## Config Schema Validation

```typescript
// TypeScript: Zod schema for application config
import { z } from 'zod';

const ConfigSchema = z.object({
  // Required fields -- fail at startup if missing
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  JWT_SECRET: z.string().min(32, 'JWT secret must be at least 32 characters'),

  // Optional with defaults
  PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  MAX_WORKERS: z.coerce.number().int().positive().default(4),

  // Feature flags
  FEATURE_NEW_CHECKOUT: z.coerce.boolean().default(false),
});

// Validate at startup -- throws if invalid
const config = ConfigSchema.parse(process.env);

export type Config = z.infer<typeof ConfigSchema>;
export { config };
```

```python
# Python: Pydantic settings with validation
from pydantic import BaseSettings, validator, AnyUrl
from typing import Optional

class AppSettings(BaseSettings):
    # Required
    database_url: AnyUrl
    redis_url: str
    jwt_secret: str

    # Optional with defaults
    port: int = 3000
    log_level: str = "info"
    max_workers: int = 4

    # Feature flags
    feature_new_checkout: bool = False

    @validator('jwt_secret')
    def secret_must_be_long(cls, v):
        if len(v) < 32:
            raise ValueError('JWT secret must be at least 32 characters')
        return v

    @validator('log_level')
    def valid_log_level(cls, v):
        valid = ['debug', 'info', 'warning', 'error', 'critical']
        if v.lower() not in valid:
            raise ValueError(f'log_level must be one of {valid}')
        return v.lower()

    class Config:
        env_prefix = 'MYAPP_'
        case_sensitive = False

# Module-level singleton (raises ValidationError at import if invalid)
settings = AppSettings()
```

## Consul Template for Dynamic Config

```hcl
# consul-template.hcl
template {
  source      = "/etc/consul-template/nginx.conf.tpl"
  destination = "/etc/nginx/nginx.conf"
  command     = "nginx -s reload"
  perms       = 0644
  wait {
    min = "2s"
    max = "10s"
  }
}

# nginx.conf.tpl
upstream backend {
  {{- range service "myapp.production" }}
  server {{ .Address }}:{{ .Port }};
  {{- end }}
}

# Consul KV for config values
server {
  listen {{ key "nginx/production/listen_port" | default "80" }};
  proxy_read_timeout {{ key "nginx/production/timeout" | default "60" }}s;
}
```
