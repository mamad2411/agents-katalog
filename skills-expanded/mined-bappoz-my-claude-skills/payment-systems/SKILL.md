---
name: payment-systems
description: >
  Integração de sistemas de pagamento production-grade: Stripe, PIX, cartões, assinaturas, webhooks,
  idempotência, PCI-DSS, 3DS/SCA, reconciliação e ledger de partidas dobradas. Use quando o usuário
  mencionar: "pagamento", "checkout", "Stripe", "PIX", "cobrança", "assinatura", "billing",
  "webhook de pagamento", "PCI", "reembolso", "split de pagamento", "gateway", "cartão de crédito".
---

# Payment Systems

Você atua como engenheiro de pagamentos. Objetivo: integrações **corretas antes de bonitas** — dinheiro não perdoa. Idempotência, consistência e trilha de auditoria vêm antes de qualquer feature.

## Leis inegociáveis

1. **Nunca confie no cliente para o valor** — preço e moeda são definidos/validados no servidor. O front só envia o *id* do que comprar.
2. **Idempotência em toda operação de escrita** — toda criação de cobrança/refund manda `Idempotency-Key`. Retry sem duplicar dinheiro.
3. **Webhook é a fonte da verdade, não o redirect** — o pagamento se confirma pelo evento assinado (`payment_intent.succeeded`), nunca pelo "voltou pra /success".
4. **Verifique a assinatura do webhook** — valide o header de assinatura; rejeite o resto. Endpoint de webhook é alvo.
5. **Nunca toque em PAN** — não armazene número de cartão. Use tokenização do provedor (Stripe Elements/Checkout) → PCI-DSS SAQ-A.
6. **Ledger imutável** — registre cada movimento como append-only (partidas dobradas). Saldo é derivado, nunca editado no lugar.

## Fluxo Stripe (cartão, server-driven)

```
1. Cliente escolhe item → front pede ao SEU backend
2. Backend cria PaymentIntent (valor/moeda no servidor) com Idempotency-Key
   → retorna client_secret
3. Front confirma com Stripe.js (Payment Element) → 3DS/SCA se exigido
4. Stripe processa → dispara webhook payment_intent.succeeded
5. Backend (webhook, assinatura verificada) marca pedido pago + escreve no ledger
6. Reconcilia depois com o balanço/payout do Stripe
```

```js
// Backend: criar intent idempotente, valor no servidor
const intent = await stripe.paymentIntents.create(
  { amount: priceFromDB.amountCents, currency: 'brl', metadata: { orderId } },
  { idempotencyKey: `order_${orderId}_v1` }
);

// Webhook: verificar assinatura ANTES de confiar
const event = stripe.webhooks.constructEvent(rawBody, sig, endpointSecret);
if (event.type === 'payment_intent.succeeded') { /* marcar pago (idempotente por event.id) */ }
```

## PIX (Brasil)

- **Assíncrono**: gere cobrança (QR estático/dinâmico via PSP ou API do banco/Pix) → cliente paga → **confirmação chega por webhook** do PSP. Nunca marque pago no "gerei o QR".
- **Idempotência por txid** — cada cobrança tem `txid` único; use-o como chave de idempotência e de reconciliação.
- **Expiração** — cobranças PIX expiram; trate o estado `expirada`.
- **Devolução** via API de devolução do PSP (não "estorno de cartão").

## Assinaturas / billing

- Estados: `trialing → active → past_due → canceled/unpaid`. Modele a máquina de estados explicitamente.
- **Dunning** — retries automáticos de fatura falha + comunicação; não corte acesso no 1º erro.
- **Proration** ao trocar de plano no meio do ciclo.
- Fonte da verdade do acesso = webhooks de `invoice.*` / `customer.subscription.*`, não o clique de "assinar".

## Segurança e conformidade

| Tema | Regra |
|---|---|
| PCI-DSS | Tokenize no cliente (Elements/Checkout) → escopo SAQ-A. Nunca logue PAN/CVV. |
| Idempotência | Chave por operação lógica; persista a resposta associada à chave. |
| Webhooks | Verifique assinatura; responda 2xx rápido; processe async; trate reentrega (dedupe por event id). |
| SCA/3DS | Suporte a autenticação forte (obrigatória na UE; boa prática sempre). |
| Segredos | Chaves secretas só no servidor; use chaves restritas; rotacione. |
| Valores | Inteiros em centavos; nunca float para dinheiro. |

## Reconciliação

- Concilie diariamente seus registros vs. os do provedor (payouts/balance transactions).
- Toda linha do seu ledger casa com um evento do provedor. Divergência = alarme.
- Guarde `provider_event_id` em cada movimento para auditoria.

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [Stripe Docs](https://docs.stripe.com/) | Referência de PaymentIntents, Checkout, Billing, Connect. |
| [Stripe — Idempotent requests](https://docs.stripe.com/api/idempotent_requests) | Como e por que usar Idempotency-Key. |
| [Stripe — Webhooks](https://docs.stripe.com/webhooks) | Verificação de assinatura, boas práticas, reentrega. |
| [Stripe — SCA / 3D Secure](https://docs.stripe.com/strong-customer-authentication) | Autenticação forte. |
| [Banco Central — Pix / API](https://www.bcb.gov.br/estabilidadefinanceira/pix) | Regras do arranjo Pix (txid, devolução, QR). |
| [PCI DSS Quick Reference](https://www.pcisecuritystandards.org/) | Escopo de conformidade e SAQ. |
| [Martin Kleppmann — DDIA (consistência)](https://dataintensive.net/) | Consistência/idempotência em sistemas distribuídos. |

## Do / Don't

| Do | Don't |
|---|---|
| Valor definido no servidor | Confiar no `amount` do front |
| Confirmar por webhook assinado | Confiar no redirect de sucesso |
| Idempotency-Key em toda escrita | Retry que duplica cobrança |
| Tokenizar cartão (Elements) | Tocar/armazenar PAN |
| Centavos em inteiro | Float para dinheiro |
| Ledger append-only | Editar saldo no lugar |

## Checklist

- [ ] Preço/moeda validados no servidor
- [ ] Idempotency-Key em criação de cobrança/refund
- [ ] Webhook com assinatura verificada + dedupe por event id
- [ ] Confirmação de pagamento vem do webhook, não do redirect
- [ ] Cartão tokenizado no cliente (sem PAN no backend)
- [ ] PIX/assinatura tratam estados assíncronos e expiração
- [ ] Ledger append-only + reconciliação diária com o provedor
- [ ] Dinheiro em inteiros (centavos), segredos só no servidor
