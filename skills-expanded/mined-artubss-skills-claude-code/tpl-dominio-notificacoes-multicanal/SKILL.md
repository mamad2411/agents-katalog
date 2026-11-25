---
name: tpl-dominio-notificacoes-multicanal
description: Template do pack (dominio/08-notificacoes-multicanal.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/08-notificacoes-multicanal.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Sistema de Notificações (Email + Push + SMS + In-App)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/08-notificacoes-multicanal.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Notificações mal implementadas destroem a experiência: duplicatas, spam de retry,
sem opção de opt-out, notificação de sistema em produção às 3h por mensagem errada.
O desafio técnico é a entrega confiável com at-least-once sem duplicatas percebidas,
e o desafio de produto é respeitar as preferências do usuário em todos os canais.

## STACK ASSUMPTIONS
- Email: AWS SES, SendGrid, Resend ou Postmark
- Push: Firebase Cloud Messaging (web + Android) + APNs (iOS)
- SMS: Twilio, AWS SNS ou Vonage
- In-App: WebSocket (Socket.io) ou SSE + banco de dados
- Queue: BullMQ / SQS com dead letter queue
- Templates: Handlebars / MJML para email, i18n via i18next ou similar

## CORE CONCEPTS
- **Notification Event**: o que aconteceu no sistema (`order.confirmed`, `payment.failed`)
- **Channel**: meio de entrega (email, push, sms, in_app)
- **Template**: conteúdo parametrizado por canal e idioma
- **Preference**: configuração do usuário por tipo de notificação e canal
- **Delivery**: tentativa de entrega de uma notificação para um canal específico
- **Digest**: agrupamento de notificações similares em período (ex: "5 novos comentários")
- **Dead Letter**: fila de notificações que falharam após N retentativas
- **Provider Failover**: trocar de provider automaticamente se taxa de erro > threshold

## ARCHITECTURE RULES

### Event-Driven Pipeline
```
Business Event → NotificationService.dispatch(event)
                        ↓
               Resolver: quais users notificar?
                        ↓
               Check preferences per user per channel
                        ↓
               Enqueue delivery jobs per channel
                        ↓
         [EmailWorker] [PushWorker] [SMSWorker] [InAppWorker]
                        ↓
               Track delivery + update UI
```

### Template System
- Templates armazenados em banco de dados (editáveis sem deploy)
- Fallback: template de banco → template de arquivo → template default hardcoded
- Variables validadas antes de render (não permitir `undefined` em template)
- Email: MJML para componentes, compilar para HTML na geração (não no envio)
- i18n: template por locale, fallback para `en` se locale não existe
- Preview em admin: render template com variáveis de exemplo

### Delivery Tracking
```
Delivery states: queued → sending → sent → delivered | failed | bounced | unsubscribed
```
- Tracking por webhook do provider (bounce, open, click, unsubscribe)
- Hard bounce: marcar email como inválido, não enviar novamente
- Soft bounce (3x): marcar como temporariamente inválido, tentar depois
- Unsubscribe via webhook do provider: honrar imediatamente

### Retry Strategy
- Attempt 1: imediato
- Attempt 2: 1 min
- Attempt 3: 5 min
- Attempt 4: 30 min
- Attempt 5: 2h
- Após 5 falhas → Dead Letter Queue + alert para ops
- Idempotency: verificar se já foi enviado antes de entregar (evitar duplicatas em retry)

### User Preferences
- Granularidade: por tipo de evento (`order.confirmed`) e por canal (`email`, `push`)
- Opt-out global: desabilitar todas as notificações (exceto transacionais obrigatórias)
- Opt-out por tipo: desabilitar tipo específico em todos os canais
- Horário silencioso: não enviar push/SMS entre 22h-8h (respeitar timezone do usuário)
- Frequency cap: máximo N notificações por canal por dia

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| Business event emitted | dispatch() → resolver recipients → check prefs → enqueue per channel |
| Queue job: send_email | Render template → send via provider → track delivery |
| Queue job: send_push | Build FCM/APNs payload → send → handle token invalidation |
| Queue job: send_sms | Build message → send via Twilio → track delivery |
| Queue job: send_in_app | Persist to DB → emit via WebSocket if connected |
| Provider webhook: bounce | Marcar email como hard/soft bounce → suspender se hard |
| Provider webhook: unsubscribe | Atualizar preferências → honrar imediatamente |
| POST /notifications/preferences | Atualizar preferências do usuário |
| GET /notifications | Listar notificações in-app (com paginação cursor-based) |
| PATCH /notifications/:id/read | Marcar como lida |
| PATCH /notifications/read-all | Marcar todas como lidas |
| GET /notifications/unread-count | Count para badge (cacheável por 30s) |
| POST /admin/notifications/test | Enviar notificação de teste para email/phone específico |
| GET /admin/notifications/:id/status | Status atual de entrega com histórico de tentativas |

## CRITICAL RULES
1. Opt-out global sempre respeitado — nunca enviar para usuário que optou por sair
2. Notificações transacionais (reset de senha, confirmação de compra) ignoram opt-out de marketing
3. Hard bounce: nunca mais enviar email para aquele endereço sem ação manual do usuário
4. Idempotency key por delivery — não enviar duplicatas em retry
5. Timezone do usuário para cálculo de horário silencioso
6. FCM token inválido: remover da base de dados imediatamente (token rotacionado pelo device)
7. Dead letter: alertar ops com conteúdo da mensagem e erro específico
8. Templates com variáveis undefined devem falhar com erro claro (não enviar template quebrado)
9. Frequência cap: contar notificações por tipo por usuário por dia antes de entregar
10. Provider failover: testar fallback em staging regularmente

## COMMON PITFALLS

### ❌ Retry sem idempotency — usuário recebe email duplicado
```javascript
// ERRADO: cada falha + retry envia novo email
async function sendEmailJob(data) {
  await emailProvider.send(data); // sem verificar se já enviou
}

// CORRETO: verificar antes de enviar
async function sendEmailJob(data) {
  const delivery = await db.deliveries.findOne({ id: data.deliveryId });
  if (delivery.status === 'sent') return; // já foi, pular
  await emailProvider.send(data);
  await delivery.update({ status: 'sent', sentAt: new Date() });
}
```

### ❌ Ignorar opt-out
```javascript
// ERRADO: enviar para todos sem verificar preferências
const users = await db.users.findAll();
for (const user of users) {
  await sendEmail(user.email, template);
}

// CORRETO: filtrar por preferências antes de enfileirar
const users = await db.users.findAll({
  where: { 
    emailNotificationsEnabled: true,
    emailVerified: true,
    emailBounced: false
  }
});
```

### ❌ Push token inválido não removido
```javascript
// ERRADO: continua tentando enviar para token expirado
await fcm.send({ token: user.pushToken, ... });
// se 404/InvalidRegistration, ignora

// CORRETO: limpar token inválido
try {
  await fcm.send({ token: user.pushToken, ... });
} catch (err) {
  if (err.code === 'messaging/invalid-registration-token') {
    await db.users.update({ id: user.id, pushToken: null });
  }
}
```

## QUALITY GATES
- [ ] Opt-out global e por tipo respeitado em 100% dos canais
- [ ] Idempotency verificada antes de cada tentativa de envio
- [ ] Hard bounce marca email como inválido imediatamente
- [ ] Templates validam variáveis antes de render
- [ ] Retry com backoff exponencial, máx 5 tentativas antes de DLQ
- [ ] FCM token inválido removido ao receber erro de token
- [ ] Horário silencioso respeita timezone do usuário
- [ ] Dead letter queue com alertas configurados
- [ ] Notificações transacionais não afetadas por opt-out de marketing
- [ ] Provider failover testado em staging

## FORBIDDEN
- Enviar notificações sem verificar preferências do usuário
- Retry ilimitado — máximo N attempts antes de dead letter
- Armazenar FCM/APNs tokens inválidos sem limpeza
- Templates que aceitam variáveis `undefined` silenciosamente
- Notificações não-transacionais para usuários que optaram por sair
- Envio em horário silencioso sem verificar timezone do receptor
