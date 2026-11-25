---
name: tpl-dominio-ecommerce-completo
description: Template do pack (dominio/02-ecommerce-completo.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/02-ecommerce-completo.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: E-commerce Completo

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/02-ecommerce-completo.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
E-commerce parece simples até o primeiro pedido com problema. Inventário que vende negativo,
carrinho que não persiste entre dispositivos, tax calculation incorreta, estado de pedido
inconsistente entre sistemas — são os bugs que chegam às 2h da manhã em produção.
O coração do e-commerce é uma máquina de estados de pedido — modelar errado gera dívida técnica impossível de pagar.

## STACK ASSUMPTIONS
- Backend: Node.js / Laravel / Django / Rails
- DB: PostgreSQL (transações, locks otimistas/pessimistas, constraints)
- Cache: Redis (carrinho, sessions, rate limiting)
- Storage: S3/GCS para imagens de produto
- Search: Elasticsearch ou Algolia para catálogo
- Queue: BullMQ / SQS para processamento de pedidos assíncrono
- Tax: TaxJar / Avalara ou cálculo próprio (ICMS BR)

## CORE CONCEPTS
- **SKU vs Product**: Product é entidade de catálogo; SKU é a unidade vendável (cor+tamanho)
- **Cart Session**: carrinho anônimo (session/Redis) vs carrinho autenticado (DB) — merge no login
- **Inventory Hold**: reservar estoque no add-to-cart vs no checkout vs no pagamento
- **Order State Machine**: pending → confirmed → processing → shipped → delivered | canceled | refunded
- **Proration/Return**: pedido de devolução cria novo fluxo, não desfaz o original
- **Tax Calculation**: deve ocorrer no checkout final, não no carrinho (endereço pode mudar)
- **Checkout Session**: snapshot imutável do carrinho no momento do checkout (preços podem mudar)

## ARCHITECTURE RULES

### Catálogo de Produtos
- Separar `Product` (info de catálogo) de `ProductVariant` (SKU, preço, estoque)
- Imagens: armazenar URLs do CDN, nunca base64 em banco
- Slug único global para SEO (não apenas por categoria)
- Soft delete produtos — pedidos antigos precisam referenciar produto deletado

### Carrinho
- Carrinho anônimo: `cart_id` em cookie + dados no Redis (TTL 7 dias)
- Carrinho autenticado: salvar no banco ao fazer login (merge com anônimo)
- Ao merge: se mesmo produto em ambos, somar quantidades respeitando estoque
- Nunca confiar no preço do carrinho para cobrança — sempre recalcular na hora do checkout

### Gestão de Estoque
- Usar `SELECT ... FOR UPDATE` (pessimistic lock) ao decrementar estoque
- Reserva temporária no add-to-cart: decremento em `reserved_quantity`, não em `quantity`
- Liberar reserva se checkout não completado em 15 min (job agendado)
- Confirmar decremento em `quantity` apenas com pagamento confirmado
- Nunca permitir quantidade negativa — constraint no banco + validação na aplicação

### Máquina de Estados do Pedido
```
pending → payment_processing → confirmed → processing → shipped → delivered
                ↓                    ↓           ↓
           payment_failed        canceled    return_requested → returned → refunded
```
- Transições de estado via eventos (domain events ou state machine lib)
- Cada transição dispara: email, inventory update, webhook para ERP
- Nunca saltar estados — validar transição antes de executar

### Checkout Flow
1. Criar CheckoutSession (snapshot de carrinho: produtos, preços, quantidades)
2. Calcular tax com endereço de entrega final
3. Reservar estoque
4. Processar pagamento
5. Em sucesso: confirmar pedido, decrementar estoque real, liberar reserva
6. Em falha: liberar reserva, notificar usuário

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| GET /products?category=X&sort=price | Buscar com filtros, paginação cursor-based |
| GET /products/:slug | Retornar produto com todas as variantes e estoque |
| POST /cart/items | Adicionar ao carrinho (criar se não existe, verificar estoque) |
| PATCH /cart/items/:sku | Atualizar quantidade (verificar disponibilidade) |
| DELETE /cart/items/:sku | Remover item do carrinho |
| POST /cart/merge | Merge carrinho anônimo com autenticado no login |
| POST /checkout/session | Criar checkout session (snapshot + tax calc + reserva) |
| POST /checkout/complete | Processar pagamento → confirmar ou falhar pedido |
| GET /orders/:id | Detalhe do pedido (com linha do tempo de estados) |
| POST /orders/:id/cancel | Cancelar se estado permite → liberar estoque → estorno |
| POST /orders/:id/return | Iniciar fluxo de devolução → gerar label → aguardar recebimento |
| POST /admin/inventory/adjust | Ajuste manual de estoque com motivo (auditoria) |
| GET /admin/orders?status=pending | Listar com filtros, server-side pagination |
| POST /webhooks/shipping | Atualizar tracking status → notificar cliente |
| POST /admin/products/:id/variants | Criar nova variante (SKU, preço, estoque inicial) |

## CRITICAL RULES
1. **NUNCA** decrementar estoque sem transação de banco de dados com lock
2. **NUNCA** confiar no preço enviado pelo frontend — sempre buscar do banco no checkout
3. **SEMPRE** criar CheckoutSession como snapshot imutável antes de cobrar
4. **SEMPRE** usar idempotency key no gateway de pagamento para evitar double charge
5. Cancelamento só é possível em estados: `pending`, `payment_failed`, `confirmed`
6. Pedido em `shipped` não pode ser cancelado — apenas devolvido
7. Tax calculation com endereço final, não endereço salvo no perfil
8. Imagens de produto: gerar thumbnails no upload (não on-the-fly)
9. Variant sem estoque deve retornar `available: false`, não 404
10. Carrinho abandonado (>1h sem checkout): disparar email automation
11. Multi-currency: armazenar preço base em centavos + moeda base; converter na exibição
12. Soft delete em produtos: nunca deletar produto com pedido associado

## COMMON PITFALLS

### ❌ Race condition de estoque
```sql
-- ERRADO: dois usuários podem comprar o último item simultaneamente
SELECT quantity FROM product_variants WHERE id = $1;
-- (aqui outro usuário lê quantity = 1 também)
UPDATE product_variants SET quantity = quantity - 1 WHERE id = $1;

-- CORRETO: pessimistic lock
BEGIN;
SELECT quantity FROM product_variants WHERE id = $1 FOR UPDATE;
-- agora apenas esta transaction lê o valor
UPDATE product_variants SET quantity = quantity - 1 WHERE id = $1 AND quantity > 0;
COMMIT;
```

### ❌ Preço salvo no carrinho sem re-validação
```javascript
// ERRADO: usar preço do carrinho/frontend diretamente
const total = cartItems.reduce((sum, item) => sum + item.price * item.qty, 0);

// CORRETO: buscar preço atual do banco
const variants = await db.productVariants.findMany({ where: { id: { in: cartItemIds } } });
const total = cartItems.reduce((sum, item) => {
  const variant = variants.find(v => v.id === item.variantId);
  return sum + variant.price * item.qty; // preço do banco
}, 0);
```

### ❌ Cancelar pedido já enviado
```javascript
// ERRADO: permite cancelar qualquer pedido
await order.update({ status: 'canceled' });

// CORRETO: validar transição
const cancelableStates = ['pending', 'payment_failed', 'confirmed'];
if (!cancelableStates.includes(order.status)) {
  throw new BusinessError('ORDER_NOT_CANCELABLE', `Cannot cancel order in state: ${order.status}`);
}
```

## QUALITY GATES
- [ ] Estoque nunca fica negativo (constraint no DB + validação na aplicação)
- [ ] Preço sempre re-validado no checkout a partir do banco
- [ ] Lock pessimista implementado no decremento de estoque
- [ ] Máquina de estados com transições validadas explicitamente
- [ ] Carrinho anônimo faz merge correto ao autenticar
- [ ] CheckoutSession é imutável após criação
- [ ] Tax calculado com endereço final de entrega
- [ ] Idempotency key usado em chamadas ao gateway de pagamento
- [ ] Email disparado em cada mudança de estado relevante do pedido
- [ ] Produtos soft-deleted mas visíveis em pedidos históricos

## FORBIDDEN
- Armazenar preço do produto apenas no carrinho sem re-validação
- Decrementar estoque fora de uma transação de banco com lock
- Permitir transições de estado de pedido sem validação (ex: de `delivered` para `pending`)
- Deletar fisicamente produtos com histórico de pedidos
- Calcular tax com endereço do perfil do usuário em vez do endereço de entrega do checkout
- Pular a etapa de CheckoutSession e cobrar diretamente a partir dos dados do carrinho
