---
name: tpl-dominio-integracao-crm-erp
description: Template do pack (dominio/14-integracao-crm-erp.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/14-integracao-crm-erp.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Integração com CRM/ERP Externo

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/14-integracao-crm-erp.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Integrações com sistemas externos falham silenciosamente, processam o mesmo evento duas vezes,
ou ficam fora de sincronia após uma falha de rede. O maior erro é tratar a integração como
um simples HTTP call em vez de um fluxo distribuído com falhas parciais, retries, e
reconciliação periódica. O segundo maior erro é não ter dead letter queue com alertas.

## STACK ASSUMPTIONS
- Protocolo: REST (maioria dos CRMs) ou SOAP/XML (ERPs legados como SAP)
- Queue: BullMQ / SQS / RabbitMQ para processamento assíncrono
- Cache: Redis para deduplicação e rate limiting de chamadas externas
- DB: PostgreSQL para registro de eventos, sync state e dead letter
- Transformer: camada de mapeamento entre schemas internos e externos

## CORE CONCEPTS
- **Webhook Ingestion**: receber eventos do sistema externo via HTTP
- **Idempotency Key**: identificador único por evento para evitar processar duas vezes
- **Polling**: buscar mudanças periodicamente via API (quando push/webhook não disponível)
- **Adapter Pattern**: camada de transformação que isola o schema externo do interno
- **Incremental Sync**: sincronizar apenas registros modificados desde última sync
- **Dead Letter Queue**: fila de eventos que falharam após N retentativas
- **API Contract Versioning**: versão da API do sistema externo pode mudar

## ARCHITECTURE RULES

### Webhook Ingestion
```
1. Receber webhook → verificar assinatura/HMAC → retornar 200 imediatamente
2. Enfileirar evento raw com {event_id, source, payload, received_at}
3. Worker processa: checar idempotency → transform → apply → mark processed
```

### Idempotency
```javascript
async function processEvent(eventId: string, payload: unknown) {
  // Checar se já processado
  const existing = await db.integrationEvents.findOne({ externalId: eventId });
  if (existing?.status === 'processed') {
    logger.info({ eventId }, 'Event already processed, skipping');
    return; // idempotente — não processa novamente
  }
  
  // Processar — dentro de transaction para garantir atomicidade
  await db.transaction(async (trx) => {
    await applyEvent(payload, trx);
    await trx.integrationEvents.upsert({
      externalId: eventId,
      status: 'processed',
      processedAt: new Date()
    });
  });
}
```

### Adapter Pattern (Transform Layer)
```javascript
// CRM retorna seu schema interno — adapter isola isso do domínio interno
interface CrmContact { first_name: string; last_name: string; email_address: string; }
interface InternalUser { id: string; fullName: string; email: string; }

class HubSpotContactAdapter {
  toInternal(crm: CrmContact): Partial<InternalUser> {
    return {
      fullName: `${crm.first_name} ${crm.last_name}`,
      email: crm.email_address
    };
  }
  toExternal(user: InternalUser): CrmContact {
    const [first_name, ...rest] = user.fullName.split(' ');
    return { first_name, last_name: rest.join(' '), email_address: user.email };
  }
}
```

### Conflict Resolution
- Timestamp wins: o registro mais recentemente modificado vence
- Source wins configurável: definir por entidade qual sistema é authoritative
- Conflict log: registrar toda divergência detectada para revisão manual
- Nunca silenciosamente sobrescrever se não houver regra clara

### Incremental Sync
```javascript
// Buscar apenas registros modificados desde última sync
async function incrementalSync(source: string) {
  const state = await db.syncStates.findOne({ source });
  const cursor = state?.lastSyncCursor ?? new Date(0).toISOString();
  
  const records = await crmClient.getContacts({ modifiedAfter: cursor });
  for (const record of records) {
    await processUpsert(record);
  }
  
  await db.syncStates.upsert({ source, lastSyncCursor: new Date().toISOString() });
}
```

### Dead Letter Queue
- Job falha após 5 retentativas → move para dead_letter_jobs table + alerta
- Alerta contém: event_id, source, últimos erros, payload original
- Interface admin para visualizar e re-processar manualmente
- SLA: dead letter verificado e tratado em < 4h

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| POST /webhooks/:source | Verificar HMAC → registrar raw event → enfileirar → 200 |
| Queue job: process_event | Checar idempotency → transform → apply → marcar processado |
| Queue job: sync_crm | Incremental sync → upsert → atualizar cursor |
| Business event: user.created | Enfileirar job: create_contact_in_crm |
| Business event: order.completed | Enfileirar job: sync_order_to_erp |
| POST /admin/integrations/:source/sync | Trigger manual de sync completo (reset cursor) |
| GET /admin/integrations/:source/status | Status da integração: last_sync, lag, error_rate |
| GET /admin/dead-letter | Listar eventos falhos com detalhes de erro |
| POST /admin/dead-letter/:id/retry | Re-enfileirar evento específico |
| POST /admin/dead-letter/retry-all | Re-enfileirar todos os eventos falhos de uma fonte |
| GET /admin/integrations/events?source=...&status=... | Log de eventos com filtros |
| PATCH /admin/integrations/:source/pause | Pausar processamento de uma fonte |

## CRITICAL RULES
1. Retornar HTTP 200 do webhook IMEDIATAMENTE — nunca processar de forma síncrona
2. Idempotency check antes de qualquer processamento (usar `external_id` do evento)
3. Adapter pattern obrigatório — nenhum schema externo no domínio interno
4. Dead letter com alertas — evento parado silenciosamente = dado desincronizado
5. Rate limiting ao chamar APIs externas (respeitar limites do CRM/ERP)
6. Retry com backoff exponencial — APIs externas caem e voltam
7. HMAC/assinatura do webhook verificada antes de qualquer parsing do payload
8. Conflito de dados: nunca sobrescrever silenciosamente sem regra de resolução
9. Cursor de sync armazenado atomicamente com o resultado do sync
10. Timeout em chamadas externas (ex: 10s) — nunca aguardar indefinidamente

## COMMON PITFALLS

### ❌ Processar webhook sincronamente
```javascript
// ERRADO: se o processamento demorar > 30s, CRM vai reenviar o webhook
app.post('/webhooks/crm', async (req) => {
  await syncContactToDatabase(req.body); // pode demorar, pode falhar
  res.sendStatus(200);
});

// CORRETO: enfileirar e ack imediato
app.post('/webhooks/crm', async (req) => {
  await verifyHmac(req); // rápido
  await queue.add('process-crm-event', { eventId: req.body.id, payload: req.body });
  res.sendStatus(200); // < 50ms
});
```

### ❌ Schema externo vazando para o domínio
```javascript
// ERRADO: hubspot_contact_id e first_name no modelo interno
await db.users.create({ hubspot_contact_id: crm.id, first_name: crm.first_name });

// CORRETO: adapter isola tudo
const internal = hubSpotAdapter.toInternal(crmContact);
await db.users.create(internal);
// integrations table mapeia: { internal_id, external_source, external_id }
await db.crmMappings.create({ userId: user.id, source: 'hubspot', externalId: crm.id });
```

### ❌ Full sync whole do CRM a cada hora
```javascript
// ERRADO: 100k contatos × 1h = 2.4M chamadas/dia — rate limit do CRM
await crmClient.getAllContacts(); // 100k records, toda hora

// CORRETO: incremental com cursor
await crmClient.getContacts({ modifiedSince: lastSyncAt }); // 50-200 records
```

## QUALITY GATES
- [ ] Webhook responde em < 100ms antes de processar (ack imediato)
- [ ] HMAC verificado em 100% dos webhooks recebidos
- [ ] Idempotency key previne reprocessamento de eventos duplicados
- [ ] Adapter layer separa schema externo do domínio interno
- [ ] Dead letter queue com alertas configurados
- [ ] Sync cursor persistido atomicamente com os dados sincronizados
- [ ] Rate limiting respeitado ao chamar APIs externas
- [ ] Timeout configurado em todas as chamadas HTTP externas
- [ ] Conflict resolution com regra documentada por entidade
- [ ] Interface admin para visualizar e re-processar dead letter

## FORBIDDEN
- Processar lógica de negócio dentro do handler HTTP do webhook
- Schema de sistema externo (field names, types) em models internos
- Full sync sem cursor incremental em fontes com > 10k registros
- Silenciosamente sobrescrever dados em conflito sem log
- Chamadas HTTP externas sem timeout e sem retry com backoff
- Ignorar dead letter queue sem alertas (dados silenciosamente perdidos)
