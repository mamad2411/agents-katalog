---
name: tpl-dominio-api-publica-rate-limiting
description: Template do pack (dominio/07-api-publica-rate-limiting.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/07-api-publica-rate-limiting.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: API Pública com Rate Limiting

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/07-api-publica-rate-limiting.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
API pública é produto — não apenas infraestrutura. Desenvolvedores são seus usuários.
Rate limiting mal implementado quebra clientes legítimos; versionamento incorreto
quebra integrações sem aviso. A maioria dos times implementa rate limit global e
ignora estratégias por endpoint e por tier de cliente.

## STACK ASSUMPTIONS
- Gateway: Kong, AWS API Gateway, Nginx, ou rate limiting na aplicação
- Rate Limit Storage: Redis (single source of truth para contadores)
- Auth: API Key (Bearer token no header) ou OAuth2 para terceiros
- Docs: OpenAPI 3.x (gerado a partir de código, não mantido manualmente)
- SDK: gerado automaticamente a partir do OpenAPI spec

## CORE CONCEPTS
- **Fixed Window**: contador reiniciado a cada janela (ex: 100 req/minuto)
- **Sliding Window**: janela deslizante usando sorted set no Redis (mais justo, mais caro)
- **Token Bucket**: bucket de tokens reabastecido continuamente (permite burst dentro do limite)
- **Leaky Bucket**: processa requests em rate fixo independente de burst
- **API Key Tiers**: free (100/h), starter (1k/h), pro (10k/h), enterprise (unlimited + SLA)
- **API Versioning**: semver aplicado a contratos de API (breaking change = major version)
- **Idempotency Key**: header para operações mutantes (POST/PATCH) — safe para retry

## ARCHITECTURE RULES

### Rate Limiting Strategy
- Aplicar em camadas: global IP → API key → endpoint específico
- Headers obrigatórios em TODA response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- Status 429 com `Retry-After` header (em segundos)
- Sliding window para endpoints críticos (auth, checkout)
- Token bucket para bulk endpoints (permite burst controlado)
- Whitelist para IPs internos e health checks

### API Key Management
- Gerar: `prefix_base64urlsafe(32bytes)` — ex: `sk_live_aBcD1234...`
- Armazenar apenas hash SHA-256 no banco — nunca o plaintext
- Exibir chave completa APENAS no momento da criação
- Escopos: `read`, `write`, `admin` — chave pode ter múltiplos escopos
- Rotação: permitir criar nova key antes de revogar a antiga (zero downtime)
- Associar ao workspace/org, não ao usuário individual

### Versionamento de URL
```
/v1/users     → versão estável
/v2/users     → nova versão com breaking changes
/users        → NUNCA (sem versão = problema)
```
- Major version para breaking changes: remover campo, mudar tipo, alterar comportamento
- Minor changes (additive): novos campos opcionais, novos endpoints — sem nova versão
- Deprecation: header `Deprecation: true`, `Sunset: Sat, 31 Dec 2025 23:59:59 GMT`
- Suporte a versão anterior por mínimo 12 meses após deprecação

### OpenAPI Spec
- Spec gerada a partir de anotações no código (não mantida manualmente)
- Validação de request payload contra spec antes de chegar ao handler
- Spec versionada junto com o código
- Exemplos de request/response em cada operação
- Erros documentados com schema: `{ code, message, details }`

### Breaking Change Policy
- Nunca remover campo de response sem versão major
- Nunca mudar tipo de campo sem versão major
- Nunca alterar comportamento de endpoint existente sem versão major
- Adicionar campo novo a response: OK sem nova versão (clients devem ignorar unknown)
- Adicionar query param opcional: OK sem nova versão

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| Toda request com API key | Verificar hash → checar escopo → aplicar rate limit do tier |
| Rate limit excedido | 429 + `Retry-After` + headers `X-RateLimit-*` |
| GET /v1/openapi.json | Retornar spec OpenAPI atualizada |
| POST /v1/api-keys | Criar key → retornar plaintext UMA VEZ → armazenar hash |
| DELETE /v1/api-keys/:id | Revogar key → invalidar cache |
| GET /v1/api-keys/:id/usage | Estatísticas de uso da key (calls/dia, endpoints) |
| POST /v1/resources (idempotent) | Verificar `Idempotency-Key` header → deduplicar → processar |
| GET /v1/rate-limit-status | Retornar status atual de rate limit da key autenticada |
| POST /admin/api-keys/:id/reset-limits | Reset manual de contador (suporte tier enterprise) |
| GET /v1/health | Sem auth, sem rate limit, retornar status e build info |
| GET /v1/changelog | Listar breaking changes por versão |
| POST /webhooks/register | Registrar endpoint para receber eventos via push |

## CRITICAL RULES
1. API key NUNCA armazenada em plaintext — somente hash SHA-256
2. Rate limit em Redis, não em memória da aplicação (múltiplas instâncias)
3. Headers `X-RateLimit-*` presentes em 100% das responses
4. Breaking change = nova versão major, sem exceção
5. Versão antiga mantida por mínimo 12 meses após deprecação com aviso
6. Validação do request body contra OpenAPI spec antes do handler
7. Idempotency key obrigatória em POST mutantes de recursos (documentar no spec)
8. Nunca retornar API key completa após a criação inicial
9. Rate limit por API key + por IP (proteção contra roubo de key)
10. `Retry-After` header obrigatório em todas as responses 429

## COMMON PITFALLS

### ❌ Rate limit em memória com múltiplos workers
```javascript
// ERRADO: cada processo tem seu próprio contador — limite efetivo = N * limit
const counts = new Map(); // memória local
function checkRateLimit(key) {
  const count = counts.get(key) || 0;
  counts.set(key, count + 1);
  return count < 100;
}

// CORRETO: Redis como contador compartilhado
async function checkRateLimit(key: string, limit: number, windowSeconds: number) {
  const count = await redis.incr(`rl:${key}`);
  if (count === 1) await redis.expire(`rl:${key}`, windowSeconds);
  return count <= limit;
}
```

### ❌ Armazenar API key em plaintext
```javascript
// ERRADO: leak do banco expõe todas as keys
await db.apiKeys.create({ key: rawKey, userId });

// CORRETO: armazenar hash, exibir apenas uma vez
const hash = crypto.createHash('sha256').update(rawKey).digest('hex');
await db.apiKeys.create({ keyHash: hash, prefix: rawKey.slice(0, 8), userId });
return { key: rawKey }; // único momento que o cliente vê a chave completa
```

### ❌ Remover campo de response sem versão
```javascript
// ERRADO: v1 users retornava { id, name, email } — remover email quebra clients
// Solução: manter email em v1, remover apenas em v2

// CORRETO: deprecar antes de remover
res.set('Deprecation', 'true');
res.set('Sunset', 'Sat, 31 Dec 2025 23:59:59 GMT');
res.json({ id, name, email }); // mantém por mais 12 meses
```

## QUALITY GATES
- [ ] API keys armazenadas somente como hash SHA-256
- [ ] Rate limit em Redis (não memória local)
- [ ] Headers `X-RateLimit-*` em 100% das responses
- [ ] OpenAPI spec gerada automaticamente e válida
- [ ] Request body validado contra spec antes do handler
- [ ] Versão em cada URL (`/v1/`, `/v2/`)
- [ ] Deprecation headers em endpoints obsoletos
- [ ] `Retry-After` in 429 responses
- [ ] Idempotency key documentada e verificada em POST mutantes
- [ ] Health endpoint sem auth e sem rate limit

## FORBIDDEN
- Armazenar API key em plaintext em qualquer storage
- Rate limiting com contadores em memória do processo
- Breaking changes sem bump de versão major
- Remover versão de API com < 12 meses de aviso
- Response sem headers `X-RateLimit-*`
- Endpoint de produção sem versionamento na URL
- Receber dados de request sem validação contra schema
