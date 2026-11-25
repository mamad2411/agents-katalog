---
name: sst-aws
description: Guides building and deploying full-stack applications on AWS using SST v3 (Ion). Use when the user says "deploy to AWS with SST", "set up sst.config.ts", "add a Lambda function", "connect a queue or bucket", "manage SST secrets", "run sst dev", "set up multi-stage deployments", or "migrate from SST v2 to v3". Apply when working with any SST component: Function, ApiGatewayV2, Bucket, Queue, Cron, Postgres, Dynamo, or Nextjs.
---

# SST v3 (Ion) — AWS Deployment

Produces correct, production-safe SST v3 configurations. Defines resources in
`sst.config.ts`, links them with the SST SDK, manages secrets properly, and
applies safe defaults for each stage before delivery.

---

## Required Details

Collect or infer before writing config. Ask if critical ones are missing.

| Detail | Example |
|---|---|
| **App name** | `my-app` |
| **Stages** | `dev`, `staging`, `production` |
| **AWS region** | `us-east-1` |
| **Workload shape** | API + background jobs, or Next.js + DB |
| **Data stores** | Postgres, DynamoDB, S3, or combination |
| **Frontend** | Next.js, static, or API-only |
| **Secrets needed** | DB password, API keys, etc. |

---

## Instructions

### Step 1 — Set up sst.config.ts with safe defaults

```ts
/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "my-app",
      removal: input?.stage === "production" ? "retain" : "remove",
      home: "aws",
    };
  },
  async run() {
    // define resources here
  },
});
```

### Step 2 — Define resources using SST components

**API + Lambda**
```ts
const api = new sst.aws.ApiGatewayV2("Api", { cors: true });
api.route("GET /users", "packages/functions/src/users.list");
api.route("POST /users", {
  handler: "packages/functions/src/users.create",
  link: [table], // link resources — never hardcode ARNs
});
```

**Database**
```ts
// Postgres (Aurora Serverless v2)
const db = new sst.aws.Postgres("Database", {
  scaling: {
    min: isProd ? "2 ACU" : "0 ACU",
    max: isProd ? "16 ACU" : "4 ACU",
  },
});

// DynamoDB
const table = new sst.aws.Dynamo("Table", {
  fields: { pk: "string", sk: "string" },
  primaryIndex: { hashKey: "pk", rangeKey: "sk" },
});
```

**Queue, Cron, Bucket**
```ts
const queue = new sst.aws.Queue("Jobs");
queue.subscribe("packages/functions/src/worker.handler", {
  batch: { size: 10, window: "20 seconds" },
});

new sst.aws.Cron("Daily", {
  job: "packages/functions/src/cron.handler",
  schedule: "cron(0 8 * * ? *)",
});

const bucket = new sst.aws.Bucket("Uploads", { public: false });
```

**Next.js**
```ts
const site = new sst.aws.Nextjs("Web", {
  path: "packages/web",
  environment: { NEXT_PUBLIC_API_URL: api.url },
});
```

### Step 3 — Access linked resources via SST SDK (never hardcode)

```ts
// packages/functions/src/upload.ts
import { Resource } from "sst";
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

export const handler = async () => {
  await new S3Client({}).send(new PutObjectCommand({
    Bucket: Resource.Uploads.name, // ✅ type-safe, stage-aware
    Key: "file.txt",
    Body: "content",
  }));
};
```

### Step 4 — Manage secrets with sst.Secret

```bash
sst secret set DatabasePassword "my-password"
sst secret set DatabasePassword "prod-password" --stage production
```

```ts
// sst.config.ts
const dbPassword = new sst.Secret("DatabasePassword");
const fn = new sst.aws.Function("Fn", {
  handler: "src/handler.main",
  link: [dbPassword], // injected automatically
});

// src/handler.ts
import { Resource } from "sst";
const password = Resource.DatabasePassword.value; // ✅
```

---

## Non-Negotiable Acceptance Criteria

Do not deliver config until ALL of these are true:

- [ ] `removal: "retain"` is set for production — never `"remove"` on prod
- [ ] No hardcoded ARNs, bucket names, or connection strings — all via `Resource.*`
- [ ] Secrets use `sst.Secret` — never `environment: {}` for sensitive values
- [ ] Every Lambda that accesses a resource has it in `link: [...]`
- [ ] `cors: true` on any API consumed by a frontend
- [ ] Production databases have `min` ACU above zero (no cold starts)
- [ ] `$app.stage` is used to differentiate prod vs dev settings

---

## Output Format

Deliver in this exact structure:

~~~
## sst.config.ts

[complete, copy-paste-ready config]

## Lambda handler example (if applicable)

[handler using Resource.* — no hardcoded values]

## Deploy commands

sst dev                          # local dev
sst deploy --stage staging       # staging
sst deploy --stage production    # production

## Notes
- [any important caveats, e.g. VPC needed for RDS, sst secret set required]
~~~

---

## Project Structure

```
my-app/
├── sst.config.ts
├── packages/
│   ├── functions/src/     # Lambda handlers (thin — business logic in core)
│   ├── web/               # Frontend (Next.js or other)
│   └── core/src/          # Shared logic, no AWS deps — testable
└── .sst/                  # Auto-generated — do not edit
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Hardcoded ARN/name in Lambda | Use `Resource.X.name` after linking |
| Secret in `environment: {}` | Use `sst.Secret` + `link` |
| `removal: "remove"` in production | Always `"retain"` for stateful resources |
| No `cors: true` on API | Frontend will get CORS errors |
| RDS `min: "0 ACU"` in production | Set `min: "2 ACU"` to avoid cold starts |
| Lambda accesses resource without `link` | Add resource to `link: [...]` |

## SST v2 → v3 Key Changes

| v2 | v3 |
|---|---|
| `new Api(...)` | `new sst.aws.ApiGatewayV2(...)` |
| `new Table(...)` | `new sst.aws.Dynamo(...)` |
| `new NextjsSite(...)` | `new sst.aws.Nextjs(...)` |
| `stacks()` in config | `run()` in config |
| `process.env.NAME` | `Resource.Name.name` via SST SDK |
| CDK + CloudFormation | Pulumi + Terraform (faster deploys) |