---
name: tpl-dominio-dashboard-admin-rbac
description: Template do pack (dominio/03-dashboard-admin-rbac.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/03-dashboard-admin-rbac.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Admin Dashboard com RBAC

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/03-dashboard-admin-rbac.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
RBAC implementado errado é uma vulnerabilidade de segurança, não só um bug de UX.
Times costumam criar enums hardcoded de roles e if/else espalhado pelo código — isso não escala
e garante que qualquer nova feature quebre o controle de acesso. O modelo correto é
resource + action + conditions, com verificação consistente em API e UI.

## STACK ASSUMPTIONS
- Backend: qualquer framework com middleware support
- DB: PostgreSQL (com Row Level Security opcional, mas recomendado)
- Cache: Redis para cache de permissões por sessão
- Export: streams para CSV/Excel grandes (não buffer em memória)
- Frontend: React/Vue/Angular com route guards baseados em permissões

## CORE CONCEPTS
- **Role**: agrupamento de permissions (admin, editor, viewer, billing_manager)
- **Permission**: `resource:action` — ex: `users:read`, `orders:write`, `reports:export`
- **Resource**: entidade do sistema (users, orders, products, reports)
- **Action**: operação (read, write, delete, export, impersonate)
- **Condition**: restrição contextual (only_own, same_organization, same_region)
- **Role Hierarchy**: admin herda todas as permissions de editor que herda de viewer
- **Row-Level Security**: filtrar rows automaticamente baseado no contexto do usuário
- **Audit Log**: registro imutável de toda ação sensitiva com before/after state

## ARCHITECTURE RULES

### Modelo de Permissões
```
Role (admin, editor, viewer)
  └── has many Permissions
        └── resource: string (users, orders, reports)
        └── action: string (read, write, delete, export)
        └── conditions: jsonb (opcional: { scope: 'own' })
```

### Verificação de Permissão
- Sempre verificar no backend — frontend faz UX, não segurança
- Criar `PermissionService` centralizado (não if/else inline)
- Verificação: `can(user, 'orders:write')` para ações simples
- Verificação com condição: `can(user, 'orders:read', { resourceOwnerId: order.userId })`
- Cache de permissões resolvidas por `userId` no Redis (invalididar no PATCH de role)

### Audit Logging
- Log antes e depois de toda mutação em recursos sensitivos
- Campos obrigatórios: `actor_id`, `action`, `resource_type`, `resource_id`, `before`, `after`, `ip`, `user_agent`, `timestamp`
- Audit logs são **imutáveis** — sem UPDATE/DELETE na tabela de audit
- Particionamento da tabela por mês se volume alto

### Data Tables (Server-Side)
- Paginação por cursor (não offset) para tabelas grandes
- Filtros e sorts via query string validados contra lista de campos permitidos
- Nunca permitir ordenação/filtro em campo não indexado sem aviso
- Export máximo de 100k rows por requisição — acima disso, async com email

### Bulk Operations
- Operações em bulk sempre assíncronas via queue
- Retornar `job_id` imediatamente, status via polling ou WebSocket
- Validar cada item individualmente — retornar relatório de sucessos/falhas
- Bulk delete deve exigir confirmação explícita com count no frontend

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| GET /api/admin/users?page=...&filter=... | Listar com server-side pagination/filter/sort |
| PATCH /api/admin/users/:id/role | Alterar role → invalidar cache → audit log |
| POST /api/admin/users/bulk-action | Enfileirar bulk op → retornar job_id |
| GET /api/admin/audit-logs?actor=...&resource=... | Listar audit log com filtros |
| GET /api/admin/reports/export?format=csv | Stream response para exports grandes |
| GET /api/admin/permissions/check | Verificar permissão para ação/recurso específico |
| POST /api/admin/roles | Criar role com permissions → audit log |
| PATCH /api/admin/roles/:id/permissions | Atualizar permissions → invalidar caches |
| GET /api/admin/jobs/:id/status | Polling de status de bulk operation |
| POST /api/admin/users/:id/impersonate | Requer `users:impersonate` permission + audit log obrigatório |
| DELETE /api/admin/users/:id | Soft delete → cascata de desativação → audit log |
| GET /api/admin/roles | Listar roles com permission count (não expand permissions por default) |

## CRITICAL RULES
1. Verificação de permissão SEMPRE no backend — guard de rota no frontend é apenas UX
2. Audit log para toda ação que modifica dados (não só deletes)
3. Cache de permissões invalidado imediatamente ao alterar role do usuário
4. Super-admin não é um role — é uma flag separada para evitar herança acidental
5. Bulk operations sempre assíncronas, nunca processar > 1000 items em request síncrono
6. Export de dados: stream, nunca carregar tudo em memória (OutOfMemory em produção)
7. Impersonation requer: permission específica + log do admin que fez + TTL de sessão curto
8. Row-level security: aplicar via `WHERE` clause automática no repository layer
9. Nunca expor IDs sequenciais de usuários na URL — usar UUIDs
10. Permissões deny-by-default: se não tem permissão explícita, nega

## COMMON PITFALLS

### ❌ Role check hardcoded espalhado
```javascript
// ERRADO: if/else com strings mágicas em todo lugar
if (user.role === 'admin' || user.role === 'super_admin') {
  await deleteUser(id);
}

// CORRETO: permission check centralizado
await permissionService.authorize(user, 'users:delete');
await deleteUser(id);
```

### ❌ Export carregado em memória
```javascript
// ERRADO: OOM para 500k rows
const users = await db.users.findMany({ where: filters }); // 500k objects in RAM
res.json(users);

// CORRETO: stream
const cursor = db.users.stream({ where: filters });
res.setHeader('Content-Type', 'text/csv');
cursor.pipe(csvTransformer).pipe(res);
```

### ❌ Audit log como afterthought
```javascript
// ERRADO: lembrar de logar manualmente em cada endpoint
await deleteUser(id);
await auditLog.create({ action: 'delete_user' }); // esquecido em 30% dos casos

// CORRETO: middleware/decorator automático
@Audited('users:delete')
async deleteUser(id: string, actor: User) { ... }
```

## QUALITY GATES
- [ ] Zero verificações de role hardcoded fora do PermissionService
- [ ] Toda rota de admin tem middleware de autenticação + autorização
- [ ] Audit log cobre 100% das mutações em recursos sensitivos
- [ ] Export usa streaming (não load em memória)
- [ ] Bulk operations retornam job_id e processam assincronamente
- [ ] Cache de permissões invalidado ao alterar role
- [ ] Impersonation tem log obrigatório e TTL de sessão
- [ ] Paginação cursor-based (não offset) em tabelas grandes
- [ ] Frontend exibe/oculta elementos baseado em permissões (UX) mas não confia nisso para segurança
- [ ] Filtros e sorts validados contra whitelist de campos permitidos

## FORBIDDEN
- If/else de role hardcoded fora do PermissionService centralizado
- Audit log opcional ou condicional em ações sensitivas
- Carregar dataset completo em memória para export
- Bulk operations síncronas em request HTTP
- Deletar fisicamente audit logs
- Expor stack trace ou SQL errors para usuários admin (use errorId para referência)
- Frontend como última linha de defesa para controle de acesso
