---
name: saas-multi-tenant
description: "Design e implemente arquiteturas multi-tenant de SaaS com row-level security, queries com escopo de tenant, isolamento de schema compartilhado e padrões seguros de admin entre tenants em PostgreSQL e TypeScript."
risk: safe
source: community
date_added: "2026-03-28"
tags: [multi-tenancy, saas, row-level-security, postgresql, tenant-isolation]
tools: [claude, cursor, gemini]
---

# Arquitetura Multi-Tenant de SaaS

## Quando Usar Esta Habilidade

- O usuário está construindo uma aplicação SaaS onde múltiplos clientes compartilham o mesmo banco de dados
- O usuário pergunta sobre isolamento de tenants, row-level security ou prevenção de vazamento de dados
- O usuário precisa fazer escopo de cada query do banco de dados para um tenant específico sem cláusulas WHERE manuais
- O usuário pergunta sobre tradeoffs entre shared-schema, schema-per-tenant e database-per-tenant
- O usuário está implementando endpoints de admin que devem acessar dados entre tenants
- O usuário precisa adicionar colunas `tenant_id` a uma aplicação single-tenant existente
- O usuário pergunta sobre políticas PostgreSQL RLS para isolamento de tenants
- O usuário está construindo middleware tenant-aware em Express, Fastify ou Next.js API routes

NÃO use esta habilidade quando:
- O usuário está construindo uma aplicação single-user sem infraestrutura compartilhada
- O usuário pergunta apenas sobre autenticação sem escopo de tenant (use uma habilidade de auth)
- O usuário precisa de design geral de schema de banco de dados sem requisitos multi-tenant

## Fluxo de Trabalho Central

1. Determine o modelo de tenancy. Pergunte ao usuário sobre suas expectativas de escala e requisitos de isolamento. Para a maioria das apps SaaS com menos de 1000 tenants, shared-schema com uma coluna `tenant_id` em toda tabela é o padrão correto. Schema-per-tenant adiciona overhead operacional (migrações rodam N vezes). Database-per-tenant só é justificado quando tenants têm requisitos de residência de dados regulatória.

2. Adicione `tenant_id` a toda tabela tenant-scoped. A coluna deve ser `NOT NULL`, tipo `UUID` ou `TEXT`, e incluída em todo índice composto. Nunca permita que uma tabela tenant-scoped exista sem esta coluna — um `tenant_id` faltando é um vazamento de dados esperando para acontecer.

3. Configure PostgreSQL Row-Level Security (RLS). Crie uma política em cada tabela tenant-scoped que filtre linhas por `current_setting('app.current_tenant_id')`. Isto funciona como uma rede de segurança ao nível de banco de dados — mesmo se o código da aplicação esquecer uma cláusula WHERE, RLS bloqueia leituras entre tenants.

4. Construa middleware tenant-aware. No início de cada request, extraia o `tenant_id` da sessão autenticada ou claims de JWT. Defina-o na conexão do banco de dados usando `SET LOCAL app.current_tenant_id = '...'` dentro de uma transação. Toda query subsequente naquele request herda automaticamente o escopo de tenant.

5. Faça escopo de todas as queries ORM por tenant. Se usar Prisma, aplique um middleware global que injete `where: { tenantId }` em toda chamada `findMany`, `findFirst`, `update` e `delete`. Se usar Drizzle, crie um query builder base que inclua o filtro de tenant. Nunca dependa de desenvolvedores lembrando de adicionar o filtro manualmente.

6. Lide com migrações tenant-aware. Toda nova migração de tabela deve incluir `tenant_id` como coluna. Escreva uma regra de linting ou verificação de CI que rejeite qualquer migração criando uma tabela sem `tenant_id` a menos que a tabela seja explicitamente marcada como global (ex: `plans`, `feature_flags`).

7. Construa rotas de admin entre tenants separadamente. Endpoints de admin que agregam dados entre tenants devem contornar RLS explicitamente usando `SET LOCAL role = 'admin_bypass'` ou uma role de banco de dados dedicada. Estas rotas devem ser protegidas por um fluxo de autenticação admin separado — nunca reutilize sessões de usuários tenant para acesso admin.

8. Implemente tenant provisioning. Quando um novo cliente se inscreve, crie seu registro de tenant, seed dados padrão (roles, settings, estado de onboarding), e atribua o usuário fundador. Envolva isto em uma transação de banco de dados para que provisioning parcial nunca deixe registros órfãos.

## Exemplos

### Exemplo 1: Política PostgreSQL RLS para Isolamento de Tenant

```sql
-- Habilite RLS na tabela
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects FORCE ROW LEVEL SECURITY;

-- Política: usuários podem ver apenas linhas onde tenant_id corresponde à variável de sessão
CREATE POLICY tenant_isolation ON projects
  USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- Política para INSERT: novas linhas devem corresponder ao tenant atual
CREATE POLICY tenant_insert ON projects
  FOR INSERT
  WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

### Exemplo 2: Middleware Express que Define Contexto de Tenant por Request

```typescript
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function tenantMiddleware(req, res, next) {
  const tenantId = req.auth?.tenantId; // extraído de JWT durante auth
  if (!tenantId) return res.status(403).json({ error: "No tenant context" });

  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    // Use set_config — SET LOCAL não aceita bind placeholders ($1)
    await client.query("SELECT set_config('app.current_tenant_id', $1, true)", [tenantId]);
    req.db = client;
    req.tenantId = tenantId;

    // Cleanup on response finish — garante release mesmo se handler pula next()
    res.on("finish", async () => {
      try { await client.query("COMMIT"); } catch { await client.query("ROLLBACK"); }
      client.release();
    });

    next();
  } catch (err) {
    await client.query("ROLLBACK").catch(() => {});
    client.release();
    next(err);
  }
}
```

### Exemplo 3: Middleware Prisma para Tenant Scoping Automático

```typescript
import { PrismaClient } from "@prisma/client";

// Tabelas que NÃO têm tenant_id (tabelas globais)
const GLOBAL_TABLES = new Set(["Plan", "FeatureFlag", "SystemConfig"]);

function createTenantPrisma(tenantId: string): PrismaClient {
  const prisma = new PrismaClient();

  prisma.$use(async (params, next) => {
    if (GLOBAL_TABLES.has(params.model ?? "")) return next(params);

    // Inicialize args.where — Prisma passa undefined args para chamadas como findMany()
    params.args = params.args ?? {};
    params.args.where = params.args.where ?? {};

    // Injete filtro de tenant em leituras (pule findUnique — aceita apenas seletores de campos únicos)
    if (["findMany", "findFirst", "count", "aggregate"].includes(params.action)) {
      params.args.where = { ...params.args.where, tenantId };
    }

    // Injete tenant_id em creates
    if (["create", "createMany"].includes(params.action)) {
      params.args.data = params.args.data ?? {};
      if (params.action === "createMany") {
        params.args.data = params.args.data.map((d: any) => ({ ...d, tenantId }));
      } else {
        params.args.data = { ...params.args.data, tenantId };
      }
    }

    // Faça escopo de updates e deletes
    if (["update", "updateMany", "delete", "deleteMany"].includes(params.action)) {
      params.args.where = { ...params.args.where, tenantId };
    }

    return next(params);
  });

  return prisma;
}
```

## Nunca Faça Isto

1. **Nunca faça query em uma tabela tenant-scoped sem um filtro `tenant_id`.** Mesmo se seu middleware ORM cuide disso, raw SQL queries contornam middleware inteiramente. Toda raw query deve incluir `WHERE tenant_id = $1` ou depender de RLS. Um único `SELECT * FROM invoices` não scoped vaza dados de cobrança de cada cliente.

2. **Nunca armazene `tenant_id` apenas na sessão de aplicação sem impor no nível de banco de dados.** Filtragem na camada de aplicação é uma sugestão. RLS é imposição. Se um bug no seu middleware pula o filtro de tenant, apenas RLS previne o vazamento de dados. Rode ambas as camadas.

3. **Nunca use IDs auto-incrementados inteiros para recursos tenant-scoped.** IDs sequenciais (`invoice #1042`) deixam atacantes enumerar recursos de outros tenants incrementando o ID. Use UUIDs para todas as chaves primárias tenant-scoped. Reserve IDs inteiros para tabelas apenas-internas.

4. **Nunca deixe usuários tenant acessarem endpoints de agregação admin.** Uma rota como `GET /admin/metrics` que faz query entre todos os tenants nunca deve ser alcançável com um JWT regular de tenant. Use um mecanismo de autenticação separado (API key, admin role claim com um issuer diferente) para rotas entre tenants.

5. **Nunca rode migrações com RLS habilitado na conexão de migração.** O usuário de migração precisa criar tabelas, adicionar colunas e modificar políticas. Se RLS estiver ativo na conexão de migração, comandos `ALTER TABLE` podem silenciosamente falhar ou afetar apenas a visão do "tenant atual". Use um usuário superuser dedicado ou role `bypassrls` para migrações.

6. **Nunca compartilhe connection pools entre tenants ao usar `SET LOCAL`.** Se você usar `SET LOCAL app.current_tenant_id` dentro de uma transação, essa configuração é scoped à transação. Mas se a transação de um request anterior não foi corretamente comitada ou rolled back, a conexão retorna ao pool com contexto de tenant stale. Sempre `RESET app.current_tenant_id` no caminho de cleanup.

## Edge Cases

1. **Deleção de tenant e retenção de dados.** Quando um tenant cancela sua subscrição, você não pode simplesmente `DELETE FROM tenants WHERE id = $1`. Cascatas de foreign key podem dar timeout em datasets grandes. Ao invés, soft-delete o tenant (set `deleted_at`), revogue todas as sessões de usuário, depois rode um background job que deleta dados de tenant em batches ao longo de horas ou dias.

2. **Exportação de dados de tenant para GDPR/compliance.** Quando um tenant requisita uma exportação completa de dados, você precisa fazer query em toda tabela tenant-scoped para aquele `tenant_id` e empacotá-lo. Construa um registro de todas as tabelas tenant-scoped (parse seus arquivos de migração ou mantenha um manifesto) para que o job de exportação não perca tabelas adicionadas após o feature de exportação ter sido construído.

3. **Recursos compartilhados entre tenants.** Alguns features requerem estado compartilhado — ex: um marketplace onde produtos do Tenant A são visíveis para usuários do Tenant B. Estas tabelas precisam de uma política RLS diferente: acesso de leitura é público (sem filtro de tenant), mas acesso de escrita ainda é scoped ao tenant proprietário. Modele estes como `owner_tenant_id` ao invés de `tenant_id`.

4. **Background jobs tenant-aware.** Quando um cron job ou queue worker processa tasks, não há HTTP request para extrair `tenant_id` de. O payload de job deve incluir `tenant_id`, e o worker deve definir a variável de sessão do banco de dados antes de processar. Nunca rode background jobs sem contexto de tenant — eles vão ou falhar em RLS ou contorná-lo inteiramente.

5. **Exaustão de connection pool com schema-per-tenant.** Se você usar um PostgreSQL schema por tenant e cada schema requerer seu próprio connection pool, 500 tenants significa 500 pools. Isto esgota `max_connections` rapidamente. Use um connection pooler como PgBouncer em transaction mode, ou mude para shared-schema antes de bater nesta parede.

## Melhores Práticas

1. **Crie uma tabela `tenants` como a única fonte de verdade.** Toda foreign key `tenant_id` em toda tabela aponta de volta para `tenants.id`. Inclua colunas para `name`, `slug` (para tenant routing de subdomínio), `plan_id`, `created_at` e `deleted_at`. Esta tabela é a raiz de todo seu modelo de dados.

2. **Indexe `tenant_id` como a primeira coluna em todo índice composto.** PostgreSQL usa leftmost prefix matching para índices compostos. Um índice em `(tenant_id, created_at)` serve tanto "todos os items para tenant X" quanto "items para tenant X ordenados por data." Um índice em `(created_at, tenant_id)` só ajuda queries de range de data entre todos os tenants.

3. **Use subdomínios ou path prefixes para tenant routing.** `acme.yourapp.com` ou `yourapp.com/org/acme` — ambos funcionam. Mapeie o subdomínio ou path para um lookup de `tenant_id` na edge (middleware ou reverse proxy). Este lookup deve ser cacheado (Redis ou em-memória com 60s TTL) já que roda em todo único request.

4. **Separe tabelas tenant-scoped de tabelas globais explicitamente.** Mantenha uma lista (constante de código ou tabela de banco de dados) de quais tabelas são globais (sem `tenant_id`) e quais são tenant-scoped. Use esta lista no seu middleware ORM, seu linter de migração, e seu job de exportação de dados. Se uma tabela não estiver em nenhuma lista, a verificação de CI deve falhar.

5. **Teste com pelo menos 3 tenants em seus dados de seed.** Um único tenant em desenvolvimento esconde todo bug de multi-tenancy. Dois tenants esconde bugs onde os dados do primeiro tenant vazam para o segundo mas não vice-versa. Três tenants pega bugs de ordering e filtering que só aparecem com múltiplos peers.

6. **Rate-limit e quota por tenant, não globalmente.** Um rate limit global de 1000 requests/minuto significa um tenant barulhento pode esgotar a quota para todos. Implemente per-tenant rate limiting usando um padrão de chave Redis como `ratelimit:{tenant_id}:{endpoint}` com um counter de janela deslizante.