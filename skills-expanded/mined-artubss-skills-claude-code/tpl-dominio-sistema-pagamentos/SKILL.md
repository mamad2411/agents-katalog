---
name: tpl-dominio-sistema-pagamentos
description: Template do pack (dominio/05-sistema-pagamentos.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/05-sistema-pagamentos.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Sistema de Pagamentos

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/05-sistema-pagamentos.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Pagamentos são o domínio onde um bug custa dinheiro real e pode ser crime (PCI DSS).
A complexidade não é técnica — é de fluxo: 3DS2, split payment, captura parcial,
reconciliação. A maioria dos times implementa o happy path e esquece os estados
de falha, que são os que aparecem em produção às 23h.

## STACK ASSUMPTIONS
- Gateway: Stripe, Adyen, Cielo, PagSeguro, Braintree ou Checkout.com
- Backend: qualquer (a lógica de estado é agnóstica)
- DB: PostgreSQL com transações ACID (obrigatório)
- Queue: BullMQ / SQS para processar webhooks e jobs de reconciliação
- Vault: Hashicorp Vault ou AWS Secrets Manager para chaves PCI

## CORE CONCEPTS
- **Payment Intent**: objeto que rastreia ciclo de vida do pagamento (created → processing → succeeded | failed | canceled)
- **Authorization vs Capture**: pré-autorizar (reservar limite) separado de captura (cobrar)
- **3DS2**: autenticação adicional de segurança — redireciona para banco emissor
- **Tokenização**: trocar dados de cartão por token opaco armazenado no gateway
- **Split Payment**: distribuir valor entre múltiplas contas (marketplace)
- **Reconciliação**: validar que o que foi cobrado no gateway bate com o que foi criado no sistema
- **Chargeback**: reversão iniciada pelo banco emissor do cartão (você perde o dinheiro)
- **Refund vs Reversal**: refund é nova transação; reversal cancela antes da captura

## ARCHITECTURE RULES

### PCI DSS Compliance
- Nunca transmitir ou armazenar PAN (número de cartão), CVV ou PIN
- Todo tráfego de dados de cartão via TLS 1.2+
- Coletar dados de cartão diretamente pelo SDK do gateway (Stripe.js, Adyen Web Components)
- Não logar request bodies que possam conter dados de cartão
- Segmentar servidores de pagamento da rede geral (PCI scope)

### Máquina de Estados do Pagamento
```
created → processing → authorized → captured → succeeded
                  ↓           ↓          ↓
              failed    void/reversal  partially_refunded → fully_refunded
                              ↓
                           expired (captura não feita em 7 dias)
```

### Idempotência
- Cada operação de pagamento tem `idempotency_key` própria (UUID v4, por tentativa)
- Armazenar `idempotency_key` no banco — checar antes de criar novo Payment Intent
- Gateway calls: incluir idempotency key no header — gateway deduplica automaticamente
- Retentar com a MESMA key em caso de timeout — não gerar nova key

### 3DS2 Flow
1. Criar Payment Intent → verificar se 3DS é necessário
2. Se `requires_action`: retornar `client_secret` para frontend
3. Frontend executa MPI (autenticação no banco emissor)
4. Frontend confirma payment com resultado do 3DS
5. Backend recebe webhook `payment_intent.succeeded` (ou `payment_intent.payment_failed`)
6. NUNCA confiar no frontend para informar resultado do 3DS — aguardar webhook

### Split Payment (Marketplace)
- Definir destinatários e percentuais na criação do Payment Intent
- Taxa de plataforma: marketplace retém percentual antes dos splits
- Cada conta destinatária precisa ser verificada no gateway (KYC)
- Refund em split: decrementar de cada destinatário proporcionalmente

### Reconciliação
- Job diário: buscar todas transactions do gateway → comparar com tabela local
- Alertar se: transaction no gateway sem registro local, ou vice-versa
- Alertar se: valor diverge (possível proration incorreta)
- Nunca corrigir manualmente — criar registro de discrepância para revisão humana

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| POST /payments/intent | Criar Payment Intent no gateway → salvar localmente → retornar client_secret |
| POST /payments/:id/capture | Capturar autorização → atualizar estado → notificar sistema |
| POST /payments/:id/void | Cancelar autorização antes de captura → liberar reserva |
| POST /payments/:id/refund | Criar refund no gateway → atualizar estado → notificar |
| POST /payments/:id/partial-capture | Capturar valor parcial → registrar saldo não capturado |
| GET /payments/:id | Detalhe com estado atual (buscado do banco + sync se stale) |
| POST /webhooks/payment | Verificar assinatura → enfileirar → processar estado |
| GET /admin/reconciliation | Relatório de divergências do dia |
| POST /admin/payments/:id/flag | Marcar para investigação de fraude |
| GET /admin/fraud-signals/:userId | Sinais de risco agregados por usuário |
| POST /payments/tokenize | Criar setup intent para salvar cartão sem cobrança |
| GET /payments/methods | Listar métodos de pagamento salvos do usuário |
| DELETE /payments/methods/:id | Remover payment method do gateway + banco |

## CRITICAL RULES
1. **NUNCA** receber, transmitir ou logar PAN, CVV ou dados de cartão
2. **SEMPRE** verificar assinatura do webhook antes de processar
3. **SEMPRE** usar idempotency key em toda criação de Payment Intent
4. Resultado de 3DS2 confirmado APENAS via webhook, não via frontend
5. Captura deve ocorrer em até 7 dias após autorização (varia por gateway)
6. Refund parcial: não exceder valor total capturado (validar no código)
7. Nunca processar pagamento de conta bloqueada ou em chargeback ativo
8. Reconciliação diária obrigatória — discrepância detectada = alerta imediato
9. Logs de pagamento: incluir `payment_intent_id` e `idempotency_key`, nunca PAN/CVV
10. Chargeback: pausar conta do usuário automaticamente se > 1% de chargeback rate

## COMMON PITFALLS

### ❌ Confiar no frontend para 3DS
```javascript
// ERRADO: frontend pode ser manipulado para dizer que 3DS passou
app.post('/confirm', async (req) => {
  const { paymentIntentId, confirmed3DS } = req.body;
  if (confirmed3DS) await fulfillOrder(paymentIntentId); // PERIGO
});

// CORRETO: aguardar webhook do gateway
// Webhook: payment_intent.succeeded → fulfillOrder
// O frontend apenas redireciona — quem confirma é o webhook
```

### ❌ Refund sem validação de valor
```javascript
// ERRADO: permite refund maior que o capturado
await gateway.refunds.create({ payment_intent: id, amount: refundAmount });

// CORRETO
const payment = await db.payments.findOne(id);
const alreadyRefunded = await db.refunds.sum({ paymentId: id });
const maxRefundable = payment.captured_amount - alreadyRefunded;
if (refundAmount > maxRefundable) throw new BusinessError('REFUND_EXCEEDS_CAPTURED');
```

### ❌ Nova idempotency key em retry
```javascript
// ERRADO: gera double charge se request chegou mas response se perdeu
async function createPayment(data) {
  const key = uuid(); // nova key a cada tentativa
  return gateway.paymentIntents.create(data, { idempotencyKey: key });
}

// CORRETO: reusar key da tentativa original
async function createPayment(data, idempotencyKey: string) {
  return gateway.paymentIntents.create(data, { idempotencyKey }); // mesma key
}
```

## QUALITY GATES
- [ ] Zero menções a PAN, CVV em qualquer log ou banco de dados
- [ ] Verificação de assinatura em 100% dos webhooks de pagamento
- [ ] Idempotency key armazenada e verificada antes de criar Payment Intent
- [ ] 3DS2 validado exclusivamente via webhook (não via frontend)
- [ ] Máquina de estados implementada com transições explícitas
- [ ] Refund valida valor máximo refundável antes de chamar gateway
- [ ] Reconciliação diária com alertas de divergência
- [ ] Captura ocorre dentro do prazo de expiração da autorização
- [ ] Chargeback rate monitorado com alertas automáticos
- [ ] Dados de pagamento em logs contém apenas IDs de referência

## FORBIDDEN
- Armazenar PAN, CVV, PIN sob qualquer circunstância
- Logar request body de endpoints de pagamento sem sanitização
- Confiar em dados do frontend para confirmar resultado de 3DS2
- Criar nova idempotency key em retry de request com timeout
- Receber dados de cartão em endpoints próprios (sem SDK do gateway)
- Processar pagamentos em background sem persistência de estado intermediário
