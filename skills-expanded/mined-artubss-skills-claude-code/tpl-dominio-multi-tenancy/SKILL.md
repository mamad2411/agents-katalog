---
name: tpl-dominio-multi-tenancy
description: Template do pack (dominio/12-multi-tenancy.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/12-multi-tenancy.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Multi-tenancy

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/12-multi-tenancy.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Multi-tenancy é a decisão arquitetural mais cara de reverter. Escolher row-level
e depois precisar de isolamento de schema custa meses de migração. Data leakage
entre tenants é o pior bug possível — não é apenas técnico, é legal (GDPR, SOC2).
A decisão de isolamento tem trade-offs de custo, compliance e complexidade que devem
ser tomados ANTES da primeira linha de código.

## STACK ASSUMPTIONS
- DB: PostgreSQL (suporta RLS nativo, schemas e databases)
- Cache: Redis com namespace por tenant
- Backend: qualquer framework com middleware support
- DNS: wildcard DNS para subdomínio por tenant (*.app.com)
- Queue: particionamento por tenant_id nos jobs

## CORE CONCEPTS
- **Row-Level Isolation**: todos os tenants em um DB, diferenciados por `tenant_id` column
- **Schema Isolation**: cada tenant em seu próprio PostgreSQL schema (`tenant_abc.users`)
- **Database Isolation**: cada tenant em seu próprio banco de dados (máximo isolamento)
- **Tenant Context**: injetar `tenant_id` em cada request via middleware
- **RLS (Row Level Security)**: PostgreSQL enforça isolamento a nível de banco
- **Feature Flags per Tenant**: habilitar/desabilitar features por tenant (plano, beta, etc.)
- **Tenant Provisioning**: criar infra para novo tenant (DB schema, roles, configurações)
- **Subdomain Routing**: `acme.app.com` → resolve para tenant `acme`

## ARCHITECTURE RULES

### Escolha de Estratégia de Isolamento
| Estratégia | Isolamento | Custo | Complexidade | Quando usar |
|-----------|-----------|-------|-------------|------------|
| Row-level | Baixo | $ | Baixa | SMB, < 1000 tenants, sem compliance rígido |
| Schema | Médio | $$ | Média | 100-10k tenants, compliance moderado |
| Database | Alto | $$$ | Alta | Enterprise, compliance rigoroso, < 100 tenants |

### Row-Level com RLS (PostgreSQL)
```sql
-- Habilitar RLS na tabela
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Policy: usuário só vê rows do seu tenant
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

-- Na aplicação: setar o contexto antes de qualquer query
SET LOCAL app.tenant_id = 'uuid-do-tenant';
```

### Tenant Context Middleware
```javascript
// Injetar tenant_id em CADA request — nunca confiar no body/query
app.use(async (req, res, next) => {
  const tenantId = await resolveTenantFromSubdomain(req.hostname);
  // OU: fromJWT, fromHeader, fromPath
  if (!tenantId) return res.status(400).json({ error: 'Cannot resolve tenant' });
  req.tenantId = tenantId;
  // Para RLS: SET LOCAL no início de cada transaction
  next();
});
```

### Tenant-Aware Caching
- Cache key SEMPRE prefixado com `tenant_id`: `tenant:{id}:users:{page}`
- Flush de cache ao alterar configuração do tenant
- Nunca cachear cross-tenant (zero sharing de cache entre tenants)

### Feature Flags per Tenant
```javascript
// No banco: tenant_features table
// { tenant_id, feature_key, enabled, config_json }

// Na aplicação
async function isEnabled(tenantId: string, feature: string): Promise<boolean> {
  const cached = await redis.get(`features:${tenantId}:${feature}`);
  if (cached !== null) return cached === '1';
  const row = await db.tenantFeatures.findOne({ tenantId, feature });
  const result = row?.enabled ?? false;
  await redis.setex(`features:${tenantId}:${feature}`, 60, result ? '1' : '0');
  return result;
}
```

### Subdomain Routing
- Wildcard DNS: `*.app.com → load balancer`
- Resolver tenant via `req.hostname.split('.')[0]`
- Tenants inválidos: retornar 404 com página amigável
- Custom domains: mapear `acme.com → tenant_id` via DNS CNAME + tabela de mapeamento

### GDPR: Tenant Data Export/Deletion
- Export: gerar ZIP com todos os dados do tenant em < 24h (regulatório)
- Deletion: cascade completo de todos os dados do tenant (testar na staging!)
- Audit: log de quando export/deletion foi solicitado e executado
- Retenção: após cancelamento, reter dados por 30 dias antes de deletar

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| Toda request | Resolver tenant_id → injetar no contexto → configurar RLS |
| POST /admin/tenants | Provisionar novo tenant → criar schema/tabelas → seed config |
| DELETE /admin/tenants/:id | Iniciar soft delete → schedule job de cleanup em 30 dias |
| POST /admin/tenants/:id/features | Atualizar feature flags → invalidar cache |
| GET /admin/tenants/:id/usage | Métricas de uso (storage, API calls, users) |
| POST /tenants/:id/export | Iniciar export de dados → enviar email com link |
| POST /tenants/:id/purge | Admin: deletar todos os dados (após período de retenção) |
| GET /tenant-config | Retornar configurações públicas do tenant atual |
| POST /admin/tenants/:id/suspend | Suspender acesso → manter dados → notificar |
| GET /admin/tenants | Listar todos os tenants com métricas (super-admin only) |

## CRITICAL RULES
1. `tenant_id` resolvido do contexto autenticado, NUNCA do body da request
2. RLS ativado em TODAS as tabelas multi-tenant (sem exceção)
3. Toda query no ORM/repositório inclui `where: { tenantId }` explicitamente (defense in depth)
4. Cache key com prefixo de tenant obrigatório — zero sharing entre tenants
5. Tenant provisioning é uma operação transacional — falha = rollback completo
6. Feature flags com cache de 60s máximo — mudanças propagam em até 60s
7. Export de dados GDPR em formato aberto (JSON + CSV), não proprietary
8. Cross-tenant queries proibidas exceto para super-admin com audit log
9. Subdomain `admin`, `api`, `www`, `mail` são reservados — validar no provision
10. Test mode: usar tenant_id separado, nunca misturar dados de test com produção

## COMMON PITFALLS

### ❌ Esquecer tenant_id em uma query
```javascript
// ERRADO: retorna dados de TODOS os tenants
const orders = await db.orders.findMany({ where: { status: 'pending' } });
// Com 100k tenants = data leakage massivo

// CORRETO: tenant_id em toda query (+ RLS como fallback)
const orders = await db.orders.findMany({
  where: { tenantId: req.tenantId, status: 'pending' }
});
```

### ❌ Cache key sem tenant prefix
```javascript
// ERRADO: tenant A contamina cache do tenant B
const users = await cache.get(`users:${page}`);

// CORRETO: sempre prefixar
const users = await cache.get(`tenant:${tenantId}:users:${page}`);
```

### ❌ Provisioning parcial sem rollback
```javascript
// ERRADO: se step 3 falhar, tenant fica em estado inconsistente
await createTenantSchema(tenantId);
await seedDefaultData(tenantId);
await createDefaultAdmin(tenantId); // falha aqui → schema criado mas sem admin
await sendWelcomeEmail(tenantId);

// CORRETO: transação completa
await db.transaction(async (trx) => {
  await createTenantSchema(tenantId, trx);
  await seedDefaultData(tenantId, trx);
  await createDefaultAdmin(tenantId, trx);
}); // rollback automático se qualquer step falhar
await sendWelcomeEmail(tenantId); // fora da transaction (side effect)
```

## QUALITY GATES
- [ ] RLS ativado em 100% das tabelas multi-tenant
- [ ] Middleware de resolução de tenant_id testado com tenants inválidos
- [ ] Cache keys prefixadas com tenant_id em todo lugar
- [ ] Provisioning é transacional com rollback
- [ ] Export GDPR implementado e testado
- [ ] Subdomínios reservados bloqueados no provisioning
- [ ] Cross-tenant query proibida sem super-admin + audit log
- [ ] Feature flags com TTL de cache configurado
- [ ] Tenant deletion cascading testado em staging completo
- [ ] Zero queries sem filtro de tenant_id no repositório

## FORBIDDEN
- `tenant_id` recebido do body da request sem validação contra sessão autenticada
- Queries sem `tenant_id` em tabelas multi-tenant (mesmo com RLS ativo)
- Cache key sem prefixo de tenant
- Cross-tenant read/write fora de contexto de super-admin
- Provisioning de tenant sem transação e rollback
- Subdomínio `admin`, `api`, `www`, `mail`, `app` disponível para tenants
- Deletar dados de tenant sem período de retenção pós-cancelamento
