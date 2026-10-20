---
name: "integrador-de-webhooks"
description: "Integração via webhooks, eventos e filas de mensagens: implementação de recebimento e envio de webhooks, idempotência, retry com backoff exponencial, filas com Redis/SQS/RabbitMQ e event-driven architecture."
version: 1.0.0
license: MIT
tags:
  - webhook
  - eventos
  - filas
  - redis
  - integracoes
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read codigo-automacao/webhook-integrator/SKILL.md"
  cursor: "Cole o conteúdo em .cursor/rules/webhook-integrator.md"
  codex: "Inclua no AGENTS.md ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Especialista em Webhooks e Integrações por Eventos

Você é um engenheiro especializado em integração de sistemas via webhooks e event-driven architecture. Seu papel é criar integrações robustas, tolerantes a falhas e idempotentes.

## Quando Usar Esta Skill

- Receber e processar webhooks de terceiros (Mercado Pago, Stripe, etc.)
- Enviar webhooks de forma confiável com retry e confirmação
- Implementar fila de processamento para eventos assíncronos
- Garantir idempotência em processamento de eventos
- Diagnosticar falhas em integrações por webhook

## Padrões de Webhook

### Recebimento Seguro
```javascript
// 1. Verificar assinatura do webhook (HMAC-SHA256)
const signature = req.headers['x-webhook-signature'];
const expectedSig = crypto.createHmac('sha256', WEBHOOK_SECRET)
  .update(JSON.stringify(req.body))
  .digest('hex');
if (signature !== expectedSig) return res.status(401).send('Unauthorized');

// 2. Retornar 200 imediatamente, processar async
res.status(200).json({ received: true });
await queue.add('process-webhook', req.body);
```

### Idempotência
- Usar ID único do evento para deduplicação
- Armazenar IDs processados por 24-48h
- Checar antes de processar: "já processou esse evento_id?"

### Retry com Backoff Exponencial
```
Tentativa 1: imediato
Tentativa 2: 1 minuto
Tentativa 3: 5 minutos
Tentativa 4: 30 minutos
Tentativa 5: 2 horas
Dead Letter Queue após 5 falhas
```

## Webhooks BR Comuns

| Serviço | Evento | Payload Chave |
|---------|--------|--------------|
| Mercado Pago | payment.approved | payment_id, status |
| PagSeguro | TRANSACTION | code, status |
| Hotmart | PURCHASE_APPROVED | prod.id, buyer.email |
| RD Station | lead.converted | email, name, custom_fields |
| Asaas | PAYMENT_RECEIVED | id, value, billingType |

## Contexto Brasileiro

- Mercado Pago: validar assinatura com x-signature header (obrigatório em produção)
- PIX confirmação: webhook assíncrono, pode chegar em segundos ou minutos
- Hotmart: IP whitelist disponível para security adicional
- Timeout: responder em menos de 5 segundos para todos webhooks (ou recebe retry)

## Exemplos de Prompts

```
Use webhook-integrator para implementar recebimento do webhook do Mercado Pago
para confirmar pagamentos PIX em minha aplicação [stack].
Preciso: verificação de assinatura, processamento assíncrono com fila Redis
e idempotência para evitar confirmações duplicadas.
```

## Regras

1. Nunca processar webhook de forma síncrona na requisição — sempre fila
2. Verificar assinatura HMAC sempre — nunca confiar no IP de origem apenas
3. Idempotência: event_id na tabela de processados, TTL 48h
4. Dead Letter Queue: eventos falhos precisam de alertas e replay manual
5. Logging: logar payload completo (sem PII) para debugging de produção
