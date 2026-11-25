---
name: revisar-bff
description: "Revisa código BFF quanto a padrões de integração e tratamento de erros upstream. Use quando o dev-bff vai autorrevisar o código antes do PR."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-bff

Revisa **código de serviço BFF (Backend for Frontend)** antes de abertura de PR: verifica aderência aos guardrails, ausência de lógica de negócio indevida, qualidade das transformações de response, segurança dos dados expostos ao frontend e cobertura de testes.

**Agente:** dev-bff  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `seguranca.md`, `testes.md`, `operacional.md`

---

## Quando usar

- Antes de abrir PR com implementação BFF
- Ao revisar PR de outro desenvolvedor no code review
- Para auto-revisão antes de solicitar revisão do arquiteto

---

## Entrada esperada

- Diff ou conjunto de arquivos a revisar
- Contrato de response esperado pelo frontend
- Quais upstreams são chamados e quais endpoints

---

## Processo de execução

### Passo 1 — Verificar pré-condições (DoD obrigatório)

- [ ] Branch está atualizada com `main`/`master` — `operacional.md §1`
- [ ] `npm test` passando — `operacional.md §2`
- [ ] `npm run build` sem erros de tipo

### Passo 2 — Verificar que o BFF não tem banco de dados

O BFF **nunca** deve ter:

```typescript
// ⛔ Prisma em BFF
import { PrismaService } from './prisma/prisma.service';

// ⛔ TypeORM, Mongoose, Knex em BFF
import { InjectRepository } from '@nestjs/typeorm';

// ⛔ Variável de ambiente de banco no .env.example do BFF
DATABASE_URL=...
```

Se encontrado, bloquear o PR e indicar que a persistência pertence a um System API.

### Passo 3 — Verificar que o BFF não tem lógica de negócio

Lógica de negócio no BFF é o principal anti-padrão da camada:

```typescript
// ⛔ regra de negócio no BFF — pertence ao System ou Process API
async getOrderSummary(orderId: string) {
  const order = await this.orderClient.getOrder(orderId);
  // Cálculo de desconto é regra de domínio — não pertence ao BFF
  const discount = order.total > 1000 ? order.total * 0.1 : 0;
  return { ...order, discount };
}

// ✅ transformação de shape — pertence ao BFF
async getOrderSummary(orderId: string) {
  const order = await this.orderClient.getOrder(orderId);
  // Adaptar campos para o que a tela precisa
  return {
    id: order.id,
    status: order.status,
    total: order.totalAmount, // renomear campo
    items: order.lineItems.map(item => ({ name: item.productName, qty: item.quantity })),
  };
}
```

### Passo 4 — Verificar segurança dos dados expostos

Ver `seguranca.md §1` — o BFF é a última barreira antes dos dados chegarem ao frontend:

- [ ] CPF, RG, dados bancários nunca em claro na response — sempre mascarados ou ausentes
- [ ] `passwordHash`, tokens internos, IDs de infraestrutura nunca na response
- [ ] Campos que o frontend não precisa são removidos da response (não passar o objeto completo do upstream)
- [ ] Nenhum log com dados pessoais do usuário

```typescript
// ⛔ passa o objeto completo do upstream para o frontend
return upstreamResponse;

// ✅ projeta apenas o que a tela precisa
return {
  id: upstreamResponse.id,
  name: upstreamResponse.name,
  email: maskEmail(upstreamResponse.email), // seguranca.md §1
};
```

### Passo 5 — Verificar tratamento de erros upstream

```typescript
// ⛔ swallow de erro — upstream falhou silenciosamente
try {
  const data = await this.client.getUser(id);
  return data;
} catch {
  return null; // frontend não sabe que falhou
}

// ⛔ expõe detalhe interno do upstream
} catch (error) {
  throw new Error(error.response.data.message); // stack trace interno

// ✅ propaga status code sem expor detalhe interno
} catch (error) {
  if (error instanceof HttpException) throw error; // repropagar erro do upstream
  throw new ServiceUnavailableException('Serviço temporariamente indisponível');
}
```

### Passo 6 — Verificar chamadas upstream em paralelo quando possível

```typescript
// ⛔ chamadas sequenciais desnecessárias — dobra a latência
const user = await this.userClient.getUser(userId);
const orders = await this.orderClient.getOrders(userId); // espera user terminar

// ✅ chamadas independentes em paralelo
const [user, orders] = await Promise.all([
  this.userClient.getUser(userId),
  this.orderClient.getOrders(userId),
]);
```

**Quando sequencial é correto:** quando a segunda chamada depende do resultado da primeira.

### Passo 7 — Verificar guardrails de Node.js

Ver `backend.md`:

- [ ] Sem floating promises (`backend.md §2`)
- [ ] Sem `console.log` em código de produção (`backend.md §5`)
- [ ] Variáveis de ambiente validadas no startup (`backend.md §6`)
- [ ] URLs de upstream como variáveis de ambiente, não hardcoded

### Passo 8 — Verificar testes

- [ ] Service testada com mocks HTTP (`nock` para clients) — `testes.md §2`
- [ ] Casos cobertos: sucesso, upstream retorna 404, upstream indisponível (503), autenticação inválida
- [ ] Nenhum dado pessoal real em fixtures — `testes.md §7`

```typescript
// ✅ mock do upstream no teste
nock(env.USER_SYSTEM_URL)
  .get('/api/v1/users/123')
  .reply(404, { type: 'not-found', status: 404 });

await expect(service.getUserProfile('123')).rejects.toThrow(NotFoundException);
```

### Passo 9 — Verificar CORS

```typescript
// ⛔ CORS aberto para qualquer origem em produção
app.enableCors({ origin: '*' });

// ✅ origins configuradas por variável de ambiente
app.enableCors({ origin: env.ALLOWED_ORIGINS });
```

---

## Saída produzida

```markdown
## Revisão BFF: <nome do PR ou feature>

**Veredicto:** ✅ Aprovado | ⚠️ Aprovado com ressalvas | ⛔ Bloqueado

---

### Bloqueios (impedem merge)
- [ ] <arquivo>:<linha> — <descrição do problema> — `<guardrail citado>`

### Ressalvas (devem ser tratadas, não impedem merge)
- <descrição + recomendação>

### Pontos positivos
- <o que foi feito bem>

### Checklist DoD
- [x] Branch atualizada
- [x] Testes passando
- [x] Sem banco de dados no BFF
- [x] Sem lógica de negócio
- [x] Dados sensíveis não expostos ao frontend
- [x] Chamadas independentes em paralelo
- [x] CORS configurado com origins explícitas
- [x] `Dockerfile` multi-stage presente (`operacional.md §4.1`)
- [x] `.dockerignore` presente (`operacional.md §4.2`)
- [x] `docker-compose.yml` presente com `env_file` (`operacional.md §4.3`)
- [x] `docker compose up --build` executa sem erro
```
