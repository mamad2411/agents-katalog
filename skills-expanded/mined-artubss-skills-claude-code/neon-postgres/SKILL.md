---
name: neon-postgres
description: "Padrões especializados para Postgres serverless Neon, branching, connection pooling e integração Prisma/Drizzle Use quando: banco Neon, postgres serverless, database branching, neon postgres, postgres serverless."
source: vibeship-spawner-skills (Apache 2.0)
---

# Neon Postgres

## Padrões

### Prisma com Conexão Neon

Configure o Prisma para Neon com connection pooling.

Use duas connection strings:
- DATABASE_URL: Conexão pooled para o Prisma Client
- DIRECT_URL: Conexão direta para Prisma Migrate

A conexão pooled usa PgBouncer para até 10K conexões.
Conexão direta necessária para migrações (operações DDL).


### Drizzle com Neon Serverless Driver

Use Drizzle ORM com o driver HTTP serverless do Neon para
ambientes edge/serverless.

Duas opções de driver:
- neon-http: Consultas únicas via HTTP (mais rápido para queries pontuais)
- neon-serverless: WebSocket para transações e sessões


### Connection Pooling com PgBouncer

Neon fornece connection pooling integrado via PgBouncer.

Limites principais:
- Até 10.000 conexões simultâneas para o pooler
- Conexões ainda consomem conexões Postgres subjacentes
- 7 conexões reservadas para superuser Neon

Use endpoint pooled para aplicação, direto para migrações.


## ⚠️ Casos Problemáticos

| Problema | Severidade | Solução |
|----------|-----------|---------|
| Problema | alta | Veja documentação |
| Problema | alta | Veja documentação |
| Problema | alta | Veja documentação |
| Problema | média | Veja documentação |
| Problema | média | Veja documentação |
| Problema | baixa | Veja documentação |
| Problema | média | Veja documentação |
| Problema | alta | Veja documentação |