---
name: revisar-seguranca-backend
description: "Checklist shift-left de segurança para NestJS — injeção, JWT, DTOs de response, anti-IDOR, helmet e rate limit — como parte do DoD do dev. Use quando o dev-backend, o dev-bff ou o dev-security valida segurança antes do merge."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-seguranca-backend

Checklist shift-left de segurança para serviços NestJS, executado pelo próprio dev como parte do DoD antes de abrir o PR.

**Agente:** `dev-backend`, `dev-bff`, `dev-security`  
**Output:** Checklist preenchido + lista de itens a corrigir antes do PR (se houver).  
**Referências rápidas:** `References/security-checklist.md`

---

## Quando usar

Antes de abrir PR de backend ou BFF. O próprio agente de dev executa este checklist como parte do DoD — não precisa esperar o `dev-security` para validar o básico.

---

## Contexto

Esta skill implementa uma camada de segurança "shift left": o dev verifica a própria implementação antes do PR. Reduz achados na auditoria do `dev-security` e acelera o ciclo de merge. Cobre os vetores mais comuns em NestJS — vetores mais complexos (SSRF, supply chain, ameaças de design) ficam para o `dev-security`.

---

## Checklist

Execute cada item e marque: ✅ Conforme | ⛔ Violação (corrija antes de PR)

### §1 — Injeção

- [ ] **Sem concatenação SQL:** Toda query usa Prisma ORM ou `$queryRaw` com template literals parametrizados. Zero concatenação de string em queries.
- [ ] **Sem concatenação NoSQL:** Parâmetros passados a consultas MongoDB/DynamoDB são validados por tipo (string, não objeto) antes do uso.
- [ ] **Sem execução de comando com entrada do usuário:** `child_process.exec/spawn` não recebe parâmetros do request sem sanitização completa.

```typescript
// ✅ Correto
await prisma.user.findFirst({ where: { id: userId } })
await prisma.$queryRaw`SELECT * FROM logs WHERE userId = ${userId}`

// ⛔ Violação
await prisma.$queryRawUnsafe(`SELECT * FROM logs WHERE userId = '${userId}'`)
```

### §2 — Autenticação e sessão

- [ ] **JWT com expiração:** Todo `signOptions` tem `expiresIn` ≤ 1h para access token.
- [ ] **Algoritmo explícito:** `algorithm: 'HS256'` ou `'RS256'` — nunca aceitar `none`.
- [ ] **Guard global ativo:** `JwtAuthGuard` aplicado globalmente no `AppModule`. Endpoints públicos marcados com `@Public()`.
- [ ] **Rate limit em auth:** Endpoint de login tem `@Throttle(5, 60)` ou equivalente.
- [ ] **Senha com hash forte:** `bcrypt.hash(password, 12)` ou `argon2.hash(password)`. Zero MD5/SHA1/texto plano.
- [ ] **Refresh token httpOnly:** Se implementado, cookie com `httpOnly: true, secure: true, sameSite: 'strict'`.

### §3 — Exposição de dados

- [ ] **DTO de response explícito:** Nunca retornar a entidade Prisma diretamente — sempre um `ResponseDto` com campos selecionados.
- [ ] **Sem campos sensíveis na response:** `password`, `passwordHash`, tokens internos estão ausentes do DTO.
- [ ] **Exception filter global:** `AllExceptionsFilter` configurado para generalizar erros antes de enviar ao cliente.
- [ ] **Sem stack trace na response:** Mensagens de erro ao cliente são genéricas. Stack trace vai apenas para o logger.
- [ ] **Logs sem dados sensíveis:** Nenhum `logger.log/debug/warn` com `Authorization` header, `password`, CPF ou número de cartão.

```typescript
// ✅ Correto
export class UserResponseDto {
  id: string;
  email: string;
  name: string;
  // sem passwordHash
}

// ⛔ Violação
return user; // retorna entidade Prisma com passwordHash incluso
```

### §3b — Mass assignment e serialização (API3:2023)

- [ ] **DTO de input explícito:** Nenhum `@Body() body: any` — todo endpoint usa DTO com campos declarados e validados. Campos privilegiados (`role`, `isAdmin`) estão ausentes do DTO de input do usuário.
- [ ] **DTO de response com whitelist:** Respostas usam `plainToInstance(ResponseDto, entity)` — a entidade Prisma bruta nunca é retornada diretamente.

```typescript
// ⛔ Violação — mass assignment
create(@Body() body: any) { return this.service.create(body); }

// ✅ Correto
create(@Body() dto: CreateOrderDto) { return this.service.create(dto); }
```

### §4 — Controle de acesso

- [ ] **Anti-IDOR:** Toda busca por ID inclui `userId: req.user.id` no WHERE. Nunca buscar só pelo ID do parâmetro.
- [ ] **Guards em rotas admin:** Rotas com prefixo `/admin` ou que retornam dados de outros usuários têm `@Roles` + `RolesGuard`.
- [ ] **Deleção/edição com ownership:** Operações que modificam ou removem recursos verificam que pertencem ao usuário autenticado antes de executar.
- [ ] **Guard por função (API5:2023):** Funções sensíveis (bulk, export, alteração de permissão) têm `@Roles` declarado individualmente — não apenas no controller.

```typescript
// ✅ Correto — anti-IDOR
const order = await this.ordersService.findOne({
  id: orderId,
  userId: req.user.id,
});

// ⛔ Violação
const order = await this.ordersService.findOne(orderId); // qualquer userId pode acessar
```

### §5 — Configuração de segurança

- [ ] **Helmet configurado:** `app.use(helmet())` está no `main.ts`.
- [ ] **CORS restritivo:** `app.enableCors({ origin: [...] })` com lista explícita — não `enableCors()` sem parâmetros.
- [ ] **Limite de payload:** `express.json({ limit: '1mb' })` ou equivalente configurado.
- [ ] **Variáveis de ambiente validadas:** `ConfigModule` com `validate` usando zod ou class-validator — sem `process.env.X` solto no código.

### §9 — Logging de segurança

- [ ] **Falha de autenticação logada:** Tentativa de login falhada gera log com `ip`, `email`, `motivo`.
- [ ] **Acesso negado logado:** Resposta 403 gera log com `userId`, `recurso`.
- [ ] **Sem catch vazio:** Nenhum `catch {}` ou `catch (e) {}` silenciando erros de autenticação/autorização.

### §12 — Rate limiting

- [ ] **ThrottlerModule configurado:** Presente no `AppModule` com `ttl` e `limit` definidos.
- [ ] **Endpoints sensíveis com throttle específico:** Login, registro, recuperação de senha têm `@Throttle` com limite menor.
- [ ] **Paginação com limite máximo:** `take: Math.min(pageSize ?? 20, 100)` em todas as listagens.
- [ ] **Fluxos de negócio sensíveis (API6:2023):** Checkout, uso de cupom e reserva de item limitado têm rate limit específico além do global. Cupons têm limite de uso por conta além de por IP.

---

## Como usar o resultado

**Todos os itens ✅:** Registrar no checklist de DoD e abrir PR.

**Algum item ⛔:** Corrigir antes de abrir PR. Não deixar para o `dev-security` corrigir o que é responsabilidade do dev.

**Dúvida sobre um item:** Consultar `Guardrails/appsec.md` na seção correspondente ou acionar o `dev-security` para orientação antes de implementar.

---

## Formato de inclusão no DoD

Adicionar ao checklist de conclusão do `dev-backend` e `dev-bff`:

```markdown
### Checklist de segurança (revisar-seguranca-backend)
- [x] §1 Injeção — sem concatenação em queries
- [x] §2 Auth — JWT com exp, guard global, rate limit
- [x] §3 Exposição — DTO de response sem campos sensíveis, logs limpos
- [x] §3b Mass assignment — DTO de input explícito, sem @Body() body: any
- [x] §4 Controle de acesso — anti-IDOR + guard por função (admin/bulk)
- [x] §5 Configuração — helmet, CORS restritivo, payload limit
- [x] §9 Logging — eventos de segurança logados
- [x] §12 Rate limiting — paginação com limite máximo, fluxos sensíveis com throttle próprio
```
