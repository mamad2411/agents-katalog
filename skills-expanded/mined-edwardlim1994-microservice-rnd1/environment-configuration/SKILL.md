# Environment Configuration

## Purpose
Configures environment variables for local development, ensuring correct split between local and SIT services.

## Role
Backend Developer

## Phase
Development

## Triggered By
New service setup or environment changes.

## Inputs
- Local infra components (from `per-service-infra-setup`)
- SIT shared infra endpoints

## Process
Configure `.env.local` (NEVER commit this file):
```
# Local infra (runs in docker compose)
DATABASE_URL=postgresql://{user}:{pass}@localhost:{port}/{db_name}
REDIS_URL=redis://localhost:6379

# SIT shared infra (never run locally)
KAFKA_BROKERS={SIT_KAFKA_HOST}:9092
AUTHENTIK_URL=https://{SIT_AUTHENTIK_HOST}
APICURIO_URL=http://{SIT_APICURIO_HOST}:8080
VAULT_ADDR=https://{SIT_VAULT_HOST}
OTEL_EXPORTER_OTLP_ENDPOINT={SIT_OTEL_HOST}:4317
```

Configure `.env.example` (ALWAYS commit with placeholder values):
```
DATABASE_URL=postgresql://user:password@localhost:5432/service_db
REDIS_URL=redis://localhost:6379
KAFKA_BROKERS=kafka.sit.internal:9092
AUTHENTIK_URL=https://auth.sit.internal
APICURIO_URL=http://apicurio.sit.internal:8080
VAULT_ADDR=https://vault.sit.internal
OTEL_EXPORTER_OTLP_ENDPOINT=otel.sit.internal:4317
```

NEVER hardcode URLs in code. ALWAYS use environment variables. Vault handles secrets in deployed environments — `.env.local` is local dev only.

## Outputs
`.env.local` (gitignored) and `.env.example` (committed) per service.

## Quality Gates
- [ ] .env.local exists and is gitignored
- [ ] .env.example committed with placeholder values
- [ ] No hardcoded URLs in application code
- [ ] SIT endpoints correctly configured for shared infra

## References
- `.claude/skills/backend-developer/per-service-infra-setup/SKILL.md`
