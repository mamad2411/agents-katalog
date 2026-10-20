---
name: otimizar-performance
description: "Aplica estratégias de otimização nos tempos de resposta do BFF, como agregação, cache e paralelização. Use quando o dev-bff precisa reduzir a latência de um endpoint agregador."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: otimizar-performance

Aplica estratégias de **melhoria de performance em serviços BFF e backend Node.js**: cache de resposta, paralelização de chamadas upstream, redução de payload, compressão e identificação de gargalos de latência.

**Agente:** dev-bff  
**Guardrails aplicáveis:** `00-core.md`, `backend.md`, `dados.md`  
**Referências rápidas:** `References/performance-checklist.md`

---

## Quando usar

- Quando o SLA de latência do endpoint não está sendo cumprido
- Para reduzir carga em serviços upstream chamados com alta frequência
- Ao identificar payload de response desnecessariamente grande
- Antes de escalar horizontalmente — primeiro otimizar o que existe

---

## Processo de execução

### Passo 1 — Medir antes de otimizar

Nunca otimizar sem dados. Identificar:
- Qual endpoint está lento? (p50, p95, p99 de latência)
- Onde está o tempo? (tempo de resposta do upstream vs tempo de processamento local)
- Qual é o volume? (req/min — justifica cache?)
- Qual é o payload? (KB de response — justifica compressão/projeção?)

```bash
# Medir tempo de resposta localmente
curl -o /dev/null -s -w "Total: %{time_total}s\n" http://localhost:3000/api/v1/endpoint
```

### Passo 2 — Paralelizar chamadas upstream independentes

É a otimização de maior impacto no BFF — custo zero, ganho imediato.

```typescript
// ⛔ sequencial — latência total = A + B + C
const user = await this.userClient.getUser(userId);
const orders = await this.orderClient.getOrders(userId);
const addresses = await this.addressClient.getAddresses(userId);
// Tempo total: 150ms + 200ms + 100ms = 450ms

// ✅ paralelo — latência total = max(A, B, C)
const [user, orders, addresses] = await Promise.all([
  this.userClient.getUser(userId),
  this.orderClient.getOrders(userId),
  this.addressClient.getAddresses(userId),
]);
// Tempo total: max(150ms, 200ms, 100ms) = 200ms
```

**Quando NÃO paralelizar:** quando a segunda chamada depende do resultado da primeira.

### Passo 3 — Implementar cache em memória para leitura frequente

Para dados que mudam com pouca frequência (configurações, catálogo de produtos, dados de referência):

```typescript
import { CACHE_MANAGER } from '@nestjs/cache-manager';
import { Inject, Injectable } from '@nestjs/common';
import { Cache } from 'cache-manager';

@Injectable()
export class ProductService {
  constructor(
    private readonly productClient: ProductClient,
    @Inject(CACHE_MANAGER) private cacheManager: Cache,
  ) {}

  async getProduct(id: string): Promise<ProductResponseDto> {
    const cacheKey = `product:${id}`;
    const cached = await this.cacheManager.get<ProductResponseDto>(cacheKey);

    if (cached) return cached;

    const product = await this.productClient.getProduct(id);
    // TTL em segundos — definir baseado em quão desatualizado o dado pode ficar
    await this.cacheManager.set(cacheKey, product, 300); // 5 minutos

    return product;
  }
}
```

**Configurar CacheModule no AppModule:**
```typescript
import { CacheModule } from '@nestjs/cache-manager';

@Module({
  imports: [
    CacheModule.register({ ttl: 60, max: 100 }), // TTL padrão 60s, máx 100 entradas
  ],
})
export class AppModule {}
```

**Regras de cache:**
- Cache apenas em endpoints de leitura (GET)
- TTL adequado ao contexto: dados de catálogo (5min), dados de usuário (30s), dados em tempo real (sem cache)
- Nunca cachear dados pessoais sem necessidade explícita (`seguranca.md §1`)
- Invalidar cache quando o dado muda (evento de atualização ou TTL curto)

### Passo 4 — Reduzir payload da response

Enviar apenas os campos que o frontend efetivamente usa:

```typescript
// ⛔ passa todos os campos do upstream — frontend recebe 40 campos, usa 8
async getOrderCard(orderId: string) {
  return this.orderClient.getOrder(orderId); // retorna objeto completo
}

// ✅ projeta apenas o necessário para a tela "card de pedido"
async getOrderCard(orderId: string): Promise<OrderCardDto> {
  const order = await this.orderClient.getOrder(orderId);
  return {
    id: order.id,
    status: order.status,
    total: order.totalAmount,
    itemCount: order.lineItems.length,
    createdAt: order.createdAt,
  };
}
```

### Passo 5 — Compressão HTTP

Habilitar compressão gzip/brotli para responses grandes (> 1KB):

```bash
npm install compression
npm install --save-dev @types/compression
```

`main.ts`:
```typescript
import * as compression from 'compression';
app.use(compression());
```

Impacto: responses JSON de 50KB comprimem para ~8KB — reduz tempo de transferência, especialmente em mobile.

### Passo 6 — Timeout e circuit breaker em chamadas upstream

Prevenir que upstream lento trave o BFF:

```typescript
// Timeout por chamada — não esperar mais que o SLA permite
const { data } = await firstValueFrom(
  this.http.get(url, { timeout: 3000 }), // 3 segundos máx
);

// Para circuit breaker, usar biblioteca como `opossum`
import CircuitBreaker from 'opossum';

const breaker = new CircuitBreaker(this.orderClient.getOrder.bind(this.orderClient), {
  timeout: 3000,
  errorThresholdPercentage: 50, // abre circuito se 50% das chamadas falharem
  resetTimeout: 30000,          // tenta fechar após 30s
});
```

### Passo 7 — Paginação e limite de campos em chamadas upstream

Se o upstream suporta paginação e projeção de campos, usar para trazer menos dados:

```typescript
// ⛔ busca todos os pedidos do usuário
await this.orderClient.getOrders(userId);

// ✅ busca apenas os últimos 5, apenas os campos necessários
await this.orderClient.getOrders(userId, {
  limit: 5,
  sort: 'createdAt:desc',
  fields: 'id,status,total,createdAt',
});
```

---

## Decisão: quando usar cada estratégia

| Problema | Estratégia | Quando aplicar |
|---|---|---|
| Múltiplas chamadas sequenciais | Paralelização | Sempre que as chamadas forem independentes |
| Mesmo dado buscado N vezes por minuto | Cache em memória | Volume > 10 req/min e dado pode ter TTL |
| Response muito grande (> 10KB) | Projeção de campos + compressão | Sempre — nunca passar objeto completo |
| Upstream lento ou instável | Timeout + circuit breaker | Quando latência do upstream impacta SLA |
| Lista sem paginação | Paginar na chamada upstream (`dados.md §3`) | Sempre — nunca trazer coleção ilimitada |

---

## Saída produzida

- Código com otimizações aplicadas
- Medição antes e depois (curl ou log de latência)
- Documentação do TTL escolhido para cada cache e justificativa
- Testes unitários que validam comportamento do cache (hit e miss)
