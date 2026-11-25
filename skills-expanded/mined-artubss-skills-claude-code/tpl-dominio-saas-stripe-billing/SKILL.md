---
name: tpl-dominio-saas-stripe-billing
description: Template do pack (dominio/01-saas-stripe-billing.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/01-saas-stripe-billing.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: SaaS com Stripe Subscriptions

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/01-saas-stripe-billing.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Billing em SaaS é uma das áreas com mais bugs silenciosos. Webhooks chegam fora de ordem,
trials expiram sem notificação, proration calculation surpreende usuários. A maioria dos times
trata billing como feature simples — e quebra em produção no primeiro upgrade/downgrade.

## STACK ASSUMPTIONS
- Payment: Stripe (Billing, Customer Portal, Webhooks)
- Backend: Node.js/Python/Ruby (qualquer — lógica é agnóstica)
- DB: PostgreSQL (com suporte a transações)
- Queue: BullMQ / SQS / Sidekiq para processar webhooks assincronamente
- Cache: Redis para idempotency keys e feature gates

## CORE CONCEPTS
- **Subscription States**: trialing → active → past_due → canceled → unpaid
- **Plan Gates**: feature availability baseada em `price_id` ou metadata do plano
- **Proration**: crédito/débito calculado por Stripe no upgrade/downgrade mid-cycle
- **Billing Anchor**: dia do mês em que a cobrança recorre
- **Metered Billing**: cobrança por uso (API calls, seats, storage) — reportado via usage records
- **Payment Intent**: objeto que rastreia o ciclo de vida de um pagamento (3DS incluso)
- **Customer Portal**: UI hospedada pelo Stripe para self-service de billing
- **Idempotency Key**: header obrigatório em escritas Stripe para evitar duplicatas

## ARCHITECTURE RULES

### Webhook Handling
- NUNCA processar webhook na request HTTP — enfileirar imediatamente e retornar 200
- Verificar assinatura `stripe-signature` header ANTES de qualquer parsing
- Usar `event.id` como idempotency key no DB — checar antes de processar
- Handler deve ser **idempotente**: reprocessar o mesmo evento não deve ter efeito colateral

### Subscription Sync
- A fonte de verdade é o Stripe, não seu banco de dados
- Sincronizar estado via webhooks: `customer.subscription.updated`, `invoice.payment_failed`, etc.
- Manter localmente apenas o necessário: `stripe_customer_id`, `stripe_subscription_id`, `plan_id`, `status`, `current_period_end`
- Não confiar em `current_period_end` para gates — usar `status === 'active'`

### Plan Gates
- Implementar como middleware/decorator, não if/else espalhado pelo código
- Resolver permissão a partir do plano, não do role do usuário
- Cache de 60s aceitável para feature gates (Redis)
- Sempre retornar `402 Payment Required` com body `{ code: 'UPGRADE_REQUIRED', feature: 'X' }`

### Trial Periods
- Trial de 14 dias: cobrar cartão na criação do trial (validação sem cobrança)
- Enviar email D-7, D-3, D-1 antes do trial expirar
- Ao expirar trial sem cartão: status → `trialing` → `canceled` (não `past_due`)

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| POST /webhooks/stripe | Verificar assinatura → enfileirar evento → return 200 |
| invoice.payment_failed | Atualizar status → `past_due` → enviar email → iniciar grace period |
| invoice.payment_succeeded | Atualizar status → `active` → estender `current_period_end` |
| customer.subscription.deleted | Marcar como `canceled` → revogar acesso → enviar email |
| customer.subscription.trial_will_end | Disparar sequência de emails (3 dias antes) |
| checkout.session.completed | Criar/vincular customer → ativar subscription localmente |
| GET /api/billing/portal | Criar Billing Portal Session → redirect URL |
| POST /api/billing/upgrade | Criar proration preview → confirmar → atualizar via Stripe API |
| GET /api/billing/invoices | Listar via Stripe API (não armazenar invoices localmente) |
| POST /api/billing/cancel | Cancelar com `cancel_at_period_end: true` (nunca imediato por padrão) |
| Metered: POST /api/usage | Criar Usage Record no Stripe com timestamp do evento |
| GET /api/plan-features | Resolver feature gates do plano atual (cache Redis) |

## CRITICAL RULES
1. **NUNCA** confiar no frontend para informar o plano — sempre buscar do Stripe/DB no backend
2. **NUNCA** deletar Customer no Stripe — apenas cancelar subscription (histórico fiscal)
3. **SEMPRE** verificar `stripe-signature` — ignorar eventos sem verificação é CVE
4. **SEMPRE** usar `idempotency_key` em toda chamada de escrita à API do Stripe
5. **SEMPRE** processar webhooks assincronamente — timeout de 10s pode fazer Stripe reentregar
6. Ao fazer upgrade: calcular e mostrar proration ANTES de confirmar (`preview_invoice`)
7. `past_due` ≠ `canceled` — usuário ainda tem acesso por grace period (configurável no Stripe)
8. Metered billing precisa de Usage Record com `timestamp` exato — não hora atual do servidor
9. Nunca armazenar número de cartão — apenas `pm_` token do Stripe
10. Testar com Stripe CLI: `stripe listen --forward-to localhost:3000/webhooks/stripe`

## COMMON PITFALLS

### ❌ Processar webhook na request
```javascript
// ERRADO
app.post('/webhook', async (req, res) => {
  await processSubscriptionChange(req.body); // pode demorar, Stripe vai reenviar
  res.sendStatus(200);
});

// CORRETO
app.post('/webhook', async (req, res) => {
  await queue.add('stripe-event', req.body); // enfileira imediatamente
  res.sendStatus(200); // responde em < 1s
});
```

### ❌ Usar current_period_end como gate
```javascript
// ERRADO — usuário pode estar past_due mas dentro do período
if (subscription.current_period_end > Date.now()) { allowAccess(); }

// CORRETO
if (subscription.status === 'active' || subscription.status === 'trialing') { allowAccess(); }
```

### ❌ Cancelar imediatamente sem confirmação
```javascript
// ERRADO — cancela agora, usuário perde acesso
await stripe.subscriptions.cancel(subId);

// CORRETO — cancela no fim do período pago
await stripe.subscriptions.update(subId, { cancel_at_period_end: true });
```

## QUALITY GATES
- [ ] Webhook endpoint verifica `stripe-signature` antes de qualquer parsing
- [ ] Todos os eventos têm idempotency check no banco antes de processar
- [ ] Feature gates implementados como middleware centralizado
- [ ] Proration preview exibida antes de confirmar upgrade/downgrade
- [ ] Trial expiry emails agendados em D-7, D-3, D-1
- [ ] Cancelamento usa `cancel_at_period_end: true` por padrão
- [ ] Metered usage reportado com timestamp do evento, não do servidor
- [ ] Stripe CLI utilizado em desenvolvimento para simular webhooks
- [ ] Test mode e live mode com variáveis de ambiente separadas
- [ ] Logs estruturados para toda interação com Stripe API (para debugging de billing)

## FORBIDDEN
- Armazenar PAN (número de cartão) em qualquer storage
- Processar lógica de negócio dentro do handler de webhook HTTP
- Usar `event.data.object` sem verificar `event.type` primeiro
- Chamar Stripe API dentro de transaction de banco de dados (latência + deadlock risk)
- Cancelar subscription imediatamente sem fluxo de confirmação com o usuário
- Confiar em campos do frontend como `plan` ou `priceId` sem validar no backend
