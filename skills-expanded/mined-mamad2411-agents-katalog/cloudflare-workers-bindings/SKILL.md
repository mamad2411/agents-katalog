---
name: cloudflare-workers-bindings
description: >
  Configure Cloudflare Workers bindings safely: KV, R2, D1, Queues, Durable Objects,
  service bindings, secrets vs vars, environments, and least-privilege resource access.
  Use for owned Workers when wiring platform resources — complements cloudflare-d1-basics
  and cloudflare-r2-public-access; not a substitute for application authz.
---

# Cloudflare Workers Bindings

## Scope And Authorization

- **In scope:** Workers and bindings on accounts you own.
- **Out of scope:** reading other accounts’ secrets; deploying malware Workers.
- Separate prod/preview bindings; never point preview at prod data stores without review.
- Secrets via `wrangler secret`; never commit secret values.
- Pair with `code-quality-standards` and resource-specific skills (D1/R2).

## When To Use

- Declaring `[[kv_namespaces]]`, `[[r2_buckets]]`, `[[d1_databases]]`, queues, DO, AI, etc.
- Splitting `vars` (non-secret) vs `secrets`.
- Multi-env wrangler configs (`[env.prod]`).
- Tokens: wrangler bindings, env.SECRET, service binding, hyperdrive, analytics engine.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| D1 schema/migrations | `cloudflare-d1-basics` |
| R2 public exposure | `cloudflare-r2-public-access` |
| Access Zero Trust | `cloudflare-access-policies` |
| Tunnel | `cloudflare-tunnel-ops` |
| Generic secrets program | `secrets-management-hygiene` |

## Binding Types (practical)

| Binding | Typical use | Sensitivity |
| --- | --- | --- |
| `vars` | Feature flags, public config | Non-secret only |
| `secrets` / `secret_text` | API keys, signing keys | High |
| KV | Config/session cache | Medium (data dependent) |
| R2 | Objects | High if private data |
| D1 | SQL | High |
| Queues | Async work | Medium |
| Durable Objects | Coordination | Medium–high |
| Service bindings | Worker-to-Worker | Trust boundary |
| Analytics Engine | Metrics | Low–medium |

## Workflow

### 1. Confirm scope and success criteria

1. Worker name, environments, required resources, data classification.
2. Success: correct resources bound per env; secrets not in git; least privilege tokens.
3. Rollback: previous wrangler.toml + secret versions if retained.

### 2. Inventory current bindings

```bash
npx wrangler deployments list
npx wrangler secret list
# Review wrangler.toml / wrangler.jsonc for all [[bindings]]
```

1. Map each binding to resource ID and environment.
2. Find plaintext secrets mistakenly in `vars`.

### 3. Structure config

```toml
name = "api"
main = "src/index.ts"
compatibility_date = "2024-11-01"

[vars]
FEATURE_X = "false"
PUBLIC_API_BASE = "https://api.example.com"

[[kv_namespaces]]
binding = "CACHE"
id = "prod-kv-id"
preview_id = "preview-kv-id"

[[r2_buckets]]
binding = "ASSETS"
bucket_name = "assets-public"

[[d1_databases]]
binding = "DB"
database_name = "app-db-prod"
database_id = "REDACTED"

[env.staging]
name = "api-staging"
vars = { FEATURE_X = "true" }
# override bindings for staging resources...
```

```bash
npx wrangler secret put STRIPE_KEY
# prompt types value; stored at CF, not in git
```

### 4. Type-safe usage

```typescript
export interface Env {
  CACHE: KVNamespace;
  ASSETS: R2Bucket;
  DB: D1Database;
  STRIPE_KEY: string;
  FEATURE_X: string;
}

export default {
  async fetch(req: Request, env: Env, ctx: ExecutionContext) {
    if (!env.STRIPE_KEY) return new Response("misconfigured", { status: 500 });
    // never console.log(env.STRIPE_KEY)
    return new Response("ok");
  },
};
```

1. Service bindings: treat callee as separate trust; validate auth if multi-tenant.
2. Do not expose binding contents on public debug routes.

### 5. Least privilege and isolation

| Practice | Why |
| --- | --- |
| Separate KV/D1/R2 per env | Prevent preview wiping prod |
| Minimal R2 API tokens for CI | Deploy only needed buckets |
| No Admin binding if read-only | Blast radius |
| Preview_id for KV | Local/preview isolation |
| Disable unused bindings | Smaller attack surface |

### 6. Verify

```bash
npx wrangler deploy --env staging
npx wrangler secret list --env staging
curl -sS https://api-staging.example.com/healthz
# Negative: ensure /debug/env does not dump secrets
```

1. Confirm staging Worker cannot read prod D1/R2.
2. Rotate one secret; old value fails; app still works with new.
3. CI uses scoped API token, not global account key.

### 7. Operate

1. Document binding → resource → owner matrix.
2. Alert on deploy of Worker with new binding to sensitive buckets.
3. Rotate secrets on schedule and after staff changes.
4. Review `wrangler tail` logs for accidental secret printouts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secrets | `wrangler secret put` | `vars.API_KEY` in git |
| Envs | Distinct resource IDs | Same prod D1 on preview |
| Logs | Redacted | `JSON.stringify(env)` |
| CI | Scoped token | User global API key |
| Service binding | Explicit authz | Trust all callers |

## Output Checklist

- [ ] Binding inventory per environment complete
- [ ] Secrets removed from vars/git
- [ ] Env-isolated resource IDs
- [ ] Typed `Env` interface matches wrangler
- [ ] Deploy verified staging/prod
- [ ] No debug secret leakage
- [ ] CI tokens scoped
- [ ] Rotation/runbook documented
- [ ] Residual shared-resource risks noted

## Rules

- Owned Workers only.
- Never commit secret values or dump env in responses.
- Prefer reversible env-specific deploys.
- Focus on **bindings and secret wiring**; deep D1/R2/Access topics are sibling skills.
