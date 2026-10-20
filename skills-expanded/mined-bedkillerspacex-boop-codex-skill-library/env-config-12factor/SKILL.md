---
name: env-config-12factor
description: >
  Twelve-factor style application config: store config in the environment,
  separate code from config, typed/validated env loading, fail-fast on missing
  required vars, and no secrets in git or images. Use when dotenv, DATABASE_URL,
  stage/prod config split, 环境变量配置, or reviewing service configuration.
---

# Env Config 12-Factor

## Scope And Authorization

- **In scope:** Application configuration for services you own.
- **Out of scope:** Extracting env secrets from systems without authorization.
- Secrets in env vars still need vault injection and rotation—env is transport, not a full secrets program.
- Never commit `.env` with production credentials.
- Pair with `secrets-management-hygiene` and `code-quality-standards`.

## When To Use

- Refactoring hardcoded URLs, feature flags, or credentials out of code.
- Standardizing config across dev/stage/prod.
- Adding schema validation for environment variables at process boot.
- Reviewing Docker/K8s env and ConfigMap/Secret split.
- Debugging “works on my machine” config drift.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org-wide secrets rotation | `secrets-management-hygiene` |
| Feature flag product design | `feature-flag-patterns` |
| K8s ExternalSecrets | `external-secrets-operator` |
| 12-factor logging/metrics only | observability skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Code vs config | Same artifact; config differs per deploy |
| Backing services | URLs via env (`DATABASE_URL`, `REDIS_URL`) |
| Validation | Parse once at startup; typed struct |
| Defaults | Safe dev defaults only; prod required without weak defaults |
| Secrets | Inject at runtime; not bake into image layers |
| Docs | `.env.example` without real secrets |

## Workflow

### 1. Confirm scope and success criteria

1. Services and environments in scope.
2. Success: boot fails on missing/invalid prod config; no secrets in git history plan.

### 2. Inventory config sources

```bash
rg -n "process\\.env|os\\.Getenv|os\\.environ|dotenv|viper|envconfig" --glob '!node_modules'
rg -n "password|api_key|secret" -i --glob '*.go' --glob '*.ts' | head
```

1. List hardcoded endpoints and credentials.
2. List ConfigMaps, compose `environment:`, and CI variables.

### 3. Baseline problems

| Smell | Fix |
| --- | --- |
| `prod` branch with different code | Same code, different env |
| Secrets in Dockerfile `ENV` | Runtime secret mount |
| Silent default to localhost in prod | Fail if `ENV=production` and missing |
| Untyped `os.Getenv` scattered | Central config module |

### 4. Central typed config

```go
// Go sketch with envconfig / cleanenv style
type Config struct {
  HTTPAddr    string `env:"HTTP_ADDR" envDefault:":8080"`
  DatabaseURL string `env:"DATABASE_URL,required"`
  LogLevel    string `env:"LOG_LEVEL" envDefault:"info"`
  Env         string `env:"APP_ENV" envDefault:"development"`
}
```

```ts
// Zod sketch
const Config = z.object({
  DATABASE_URL: z.string().url(),
  APP_ENV: z.enum(['development', 'staging', 'production']),
  HTTP_PORT: z.coerce.number().default(8080),
});
export const config = Config.parse(process.env);
```

1. Single `loadConfig()` called from `main`.
2. Feature flags: env for simple on/off; full flag system → feature-flag skill.
3. `.env` files: local dev only; load explicitly; gitignore `.env`.

### 5. Platform wiring

| Platform | Pattern |
| --- | --- |
| Docker Compose | `env_file` + secrets |
| Kubernetes | Secret/ConfigMap → env or file; prefer files for large values |
| CI | Masked variables; OIDC to cloud secrets |
| Twelve-factor strict | No per-env config files in the repo for secrets |

### 6. Verify with evidence

```bash
# Expect non-zero exit when required missing
env -u DATABASE_URL ./myapp ; echo $?
# Secret scan
gitleaks detect -v  # or org equivalent
```

1. Stage deploy with intentional bad var → crash loop with clear log (no secret echo).
2. Confirm image history has no prod credentials.
3. Document required vars in README/`.env.example`.

### 7. Hand off

1. Owners for each secret and rotation path.
2. Chart/values or terraform for env injection.
3. Link secrets skill for vault/KMS.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secrets | Runtime inject | `ENV API_KEY=sk-...` in Dockerfile |
| Validation | Fail fast typed | `getenv or ""` deep in request path |
| Example file | `.env.example` placeholders | Committed `.env` prod |
| Code | One config module | 50 scattered Getenv |
| Prod defaults | None for secrets | Default password “admin” |

## Output Checklist

- [ ] Config sources inventoried
- [ ] Central typed loader with required fields
- [ ] `.env` gitignored; example committed
- [ ] Prod missing-var failure demonstrated
- [ ] No secrets in images/git (scan evidence)
- [ ] Platform injection documented
- [ ] Residual risk (env var visibility in process list) noted

## Rules

- Code and config separated; secrets never in git.
- Fail fast on invalid production config.
- Env vars are not encrypted-at-rest by themselves—use secret stores.
- Do not log full config structs containing secrets.
- Broader secrets program → `secrets-management-hygiene`.
