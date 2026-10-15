---
name: wrangler-configuration
description: >
  Configure Cloudflare Workers projects with wrangler.jsonc, bindings, environment variables, secrets, compatibility flags, and generated TypeScript Env types. Use whenever code needs D1, R2, KV, Durable Objects, Queues, Workflows, Workers AI, Vectorize, Hyperdrive, assets, or service bindings.
compatibility: "Cloudflare Workers TypeScript projects using Wrangler; verify current Cloudflare APIs, limits, and pricing before production use."
metadata:
  source: "Architecting on Cloudflare plus official Cloudflare Developer Platform docs"
  generated: "2026-04-28"
---
# Wrangler Configuration

Use this skill when creating or editing `wrangler.jsonc`, binding Cloudflare resources, generating types, or deciding where configuration belongs.

## Rules

- Prefer `wrangler.jsonc` for new examples unless the repository already uses `wrangler.toml`.
- Add the `$schema` entry so editors can validate binding configuration.
- Bind Cloudflare resources through `env`, not ad-hoc REST API calls, when running inside a Worker.
- Run `npx wrangler types` after changing bindings and use generated `Env` types in handlers/classes.
- Store non-secret structured config in `vars`; store credentials with `wrangler secret put` or a secret store binding.
- Keep environment-specific bindings explicit. Do not accidentally point preview/dev at production data.
- Add compatibility flags only when needed, and document why they are needed.

## Minimal Worker config

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-04-28",
  "vars": {
    "APP_ENV": "production"
  }
}
```

## Binding examples

Use only the bindings required by the current project.

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "cloudflare-app",
  "main": "src/index.ts",
  "compatibility_date": "2026-04-28",

  "assets": {
    "directory": "./dist/client",
    "binding": "ASSETS"
  },

  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "app-prod",
      "database_id": "REPLACE_WITH_DATABASE_ID"
    }
  ],

  "r2_buckets": [
    {
      "binding": "BUCKET",
      "bucket_name": "app-prod-objects"
    }
  ],

  "kv_namespaces": [
    {
      "binding": "CACHE",
      "id": "REPLACE_WITH_KV_NAMESPACE_ID"
    }
  ],

  "durable_objects": {
    "bindings": [
      {
        "name": "ROOM",
        "class_name": "Room"
      }
    ]
  },

  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": ["Room"]
    }
  ],

  "queues": {
    "producers": [
      {
        "queue": "jobs",
        "binding": "JOBS"
      }
    ],
    "consumers": [
      {
        "queue": "jobs",
        "max_batch_size": 10,
        "max_batch_timeout": 5
      }
    ]
  },

  "ai": {
    "binding": "AI"
  },

  "vectorize": [
    {
      "binding": "VECTORIZE",
      "index_name": "documents"
    }
  ],

  "hyperdrive": [
    {
      "binding": "HYPERDRIVE",
      "id": "REPLACE_WITH_HYPERDRIVE_ID"
    }
  ],

  "compatibility_flags": ["nodejs_compat_v2"]
}
```

## TypeScript Env pattern

Prefer generated types, but when sketching code use explicit interfaces:

```ts
export interface Env {
  APP_ENV: string;
  DB: D1Database;
  BUCKET: R2Bucket;
  CACHE: KVNamespace;
  JOBS: Queue<JobMessage>;
  AI: Ai;
  VECTORIZE: VectorizeIndex;
  ROOM: DurableObjectNamespace<Room>;
  HYPERDRIVE: Hyperdrive;
  ASSETS: Fetcher;
}
```

## Environment separation

Use named environments for dev/staging/prod only when each binding and variable is intentionally mapped.

```jsonc
{
  "name": "app",
  "main": "src/index.ts",
  "compatibility_date": "2026-04-28",
  "env": {
    "staging": {
      "name": "app-staging",
      "vars": { "APP_ENV": "staging" },
      "d1_databases": [
        { "binding": "DB", "database_name": "app-staging", "database_id": "STAGING_DB_ID" }
      ]
    },
    "production": {
      "name": "app-prod",
      "vars": { "APP_ENV": "production" },
      "d1_databases": [
        { "binding": "DB", "database_name": "app-prod", "database_id": "PROD_DB_ID" }
      ]
    }
  }
}
```

## Review checklist

- [ ] No production IDs in local-only examples.
- [ ] `compatibility_date` is intentional and updated through change control.
- [ ] Secrets are not committed in `wrangler.jsonc`.
- [ ] Durable Object migrations are append-only and class names match exported classes.
- [ ] Queue producers and consumers are bound to the intended queues.
- [ ] `nodejs_compat_v2` is used only for libraries that require Node compatibility.
- [ ] Generated types match code references to `env.*`.
