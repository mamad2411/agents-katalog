# Per-Service Infra Setup

## Purpose
Configures the complete local infrastructure for a `*-grpc` service including PostgreSQL, Redis, and Debezium Server.

## Role
Backend Developer

## Phase
Development

## Triggered By
New `*-grpc` service created or new infrastructure needed.

## Inputs
- Scaffolded `*-grpc` service

## Process
Each `*-grpc` service runs locally in isolation:
- PostgreSQL: local docker compose (local data storage)
- Redis: local docker compose (local caching)
- Debezium Server: local docker compose (points at SIT Kafka)

SIT infra NEVER run locally: Kafka, Authentik, Apicurio, Vault, Traefik → all SIT cluster.

### docker-compose.yml Structure Per Service
```yaml
services:
  {service-name}:
    build: .
    env_file: .env.local
    depends_on: [postgres, redis]

  postgres:
    image: postgres:16-alpine
    volumes: [postgres-data:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine
    volumes: [redis-data:/data]

  debezium:
    image: debezium/server:latest
    depends_on: [postgres]
    environment:
      KAFKA_BOOTSTRAP_SERVERS: ${KAFKA_BROKERS}  # points at SIT
      # ... debezium connector config
```

## Outputs
Configured `docker-compose.yml` with postgres, redis, debezium services.

## Quality Gates
- [ ] All three local infra components configured (postgres, redis, debezium)
- [ ] Debezium points at SIT Kafka (not a local Kafka)
- [ ] docker-compose.yml uses env vars (not hardcoded values)

## References
- `.claude/skills/backend-developer/database-setup/SKILL.md`
- `.claude/skills/backend-developer/environment-configuration/SKILL.md`
