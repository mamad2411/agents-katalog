---
name: tpl-dominio-relatorios-analytics
description: Template do pack (dominio/13-relatorios-analytics.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/13-relatorios-analytics.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Relatórios e Analytics

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/13-relatorios-analytics.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Reports quebram de formas sutis: um join de 5 tabelas que funciona em dev com 100 rows
entra em timeout em produção com 10M rows. Export de 500k linhas faz OutOfMemoryError.
Timezone incorreto faz relatório de "vendas de ontem" incluir dados de hoje.
A distinção entre OLTP e OLAP não é acadêmica — escolher errado tem consequências de performance.

## STACK ASSUMPTIONS
- OLTP: PostgreSQL (transações, writes, reads operacionais)
- OLAP: Read replica PostgreSQL, ou Redshift/BigQuery para analytics pesado
- Materialized Views: PostgreSQL (refresh periódico)
- Export: streaming para CSV/Excel (via csv-stringify ou ExcelJS em stream mode)
- Queue: BullMQ / SQS para relatórios assíncronos
- Storage: S3 para relatórios gerados (link temporário por email)

## CORE CONCEPTS
- **OLTP** (Online Transaction Processing): banco de produção — otimizado para writes e reads unitários
- **OLAP** (Online Analytical Processing): orientado a agregações e scans de grandes datasets
- **Read Replica**: cópia read-only do banco primário — lag de replicação de 0-100ms
- **Materialized View**: resultado de query persistido no banco, atualizado periodicamente
- **Streaming**: processar dados em chunks, nunca carregar tudo em memória
- **Report Job**: geração assíncrona com status tracking e entrega por email/link
- **Date Range**: intervalo de datas com timezone correto — armadilha comum

## ARCHITECTURE RULES

### OLTP vs OLAP Decision
```
Query simples (< 50k rows, com índices): OLTP OK
Agregação com JOINs (50k-500k rows): Read Replica ou Materialized View
Analytics complexo (> 500k rows, full scan): DW (Redshift/BigQuery/ClickHouse)
Report recorrente com mesma query: Materialized View com refresh
Export de dados em bulk: sempre streaming, sempre assíncrono
```

### Read Replica Strategy
- Conectar à replica para: todos os SELECTs de reports e dashboards
- Conectar ao primário para: writes e reads que precisam de consistência imediata
- Lag de replicação: monitorar, alertar se > 30s
- Fallback: se replica indisponível, falar para usuário que pode ter dados stale

### Materialized Views
```sql
-- Criar view materializada
CREATE MATERIALIZED VIEW sales_by_day AS
  SELECT 
    DATE(created_at AT TIME ZONE 'America/Sao_Paulo') as day,
    SUM(amount_cents) / 100.0 as total,
    COUNT(*) as order_count
  FROM orders
  WHERE status = 'completed'
  GROUP BY 1;

-- Índice na view para queries rápidas
CREATE INDEX ON sales_by_day (day);

-- Refresh sem lock (CONCURRENT) — produção
REFRESH MATERIALIZED VIEW CONCURRENTLY sales_by_day;
```

### Date Range Pitfalls
```javascript
// ERRADO: "hoje" em UTC quando usuário está em São Paulo
const today = { gte: new Date().setHours(0,0,0,0) };

// CORRETO: timezone do usuário/tenant
const tz = tenant.timezone; // 'America/Sao_Paulo'
const today = {
  gte: DateTime.now().setZone(tz).startOf('day').toUTC().toJSDate(),
  lt: DateTime.now().setZone(tz).endOf('day').toUTC().toJSDate()
};
```

### Large Export Strategy
```javascript
// ERRADO: OOM para > 50k rows
const rows = await db.orders.findMany({ where: filters });
const csv = rows.map(toCSV).join('\n');
res.send(csv); // 500k rows × 200 bytes = 100MB em RAM

// CORRETO: streaming
const cursor = db.orders.stream({ where: filters });
const csvStream = cursor.pipe(new Transform({ objectMode: true, transform(row, _, cb) {
  cb(null, formatCSV(row) + '\n');
}}));
csvStream.pipe(res); // chunk a chunk, memória constante
```

### Async Report Generation
```
1. POST /reports/generate → criar report job → retornar { jobId }
2. Worker processa → gera CSV/Excel → faz upload para S3
3. Worker atualiza job: status=ready, downloadUrl (signed, TTL 24h)
4. Enviar email ao usuário com link de download
5. GET /reports/:jobId/status → polling de status
```

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| GET /reports/dashboard | Buscar de materialized views (rápido, pode ser stale < 5min) |
| GET /reports/sales?from=...&to=... | Query em read replica com timezone correction |
| POST /reports/export | Criar async job → retornar jobId → processar em background |
| GET /reports/jobs/:id/status | Status do job (queued/processing/ready/failed) + downloadUrl |
| GET /reports/jobs | Listar exports do usuário atual |
| POST /admin/reports/schedule | Configurar relatório recorrente (daily/weekly/monthly) |
| GET /admin/reports/scheduled | Listar relatórios agendados |
| PATCH /admin/materialized-views/refresh | Trigger manual de refresh (admin) |
| GET /reports/metrics/realtime | Métricas em tempo real (últimos 5 min) — do primário com cache |
| GET /reports/cohort | Cohort analysis — read replica (pode demorar, mostrar loading) |

## CRITICAL RULES
1. Reports nunca no banco de produção primário — usar read replica ou DW
2. Export de dados SEMPRE assíncrono se estimado > 1000 rows
3. Timezone SEMPRE explícito em todas as queries com `DATE` ou range de datas
4. Materialized view refresh com `CONCURRENT` para evitar lock na tabela
5. Streaming para CSV/Excel — nunca buffer completo em memória
6. Link de download temporário (S3 signed, TTL 24h) — não armazenar em servidor web
7. Limite de exports simultâneos por usuário (max 3 concurrent) — fila caso exceda
8. Relatórios agendados: alert se falhar 2x consecutivas
9. Estimativa de tempo/progresso mostrada ao usuário para exports longos
10. Nunca expor SQL raw para o usuário mesmo que seja "apenas para reports"

## COMMON PITFALLS

### ❌ Timezone errado no agrupamento
```sql
-- ERRADO: agrupa por dia em UTC → vendas de 21h SP aparecem "amanhã"
SELECT DATE(created_at) as day, SUM(amount) as total
FROM orders GROUP BY 1;

-- CORRETO: converter para timezone local antes de agrupar
SELECT DATE(created_at AT TIME ZONE 'America/Sao_Paulo') as day, SUM(amount) as total
FROM orders GROUP BY 1;
```

### ❌ COUNT/SUM em tabela de produção sem índice
```sql
-- ERRADO: full table scan em produção → bloqueia queries OLTP
SELECT COUNT(*), SUM(amount) FROM orders WHERE status = 'completed';
-- 10M rows = seq scan de 30s enquanto checkout está tentando ler a mesma tabela

-- CORRETO: usar materialized view atualizada periodicamente
SELECT * FROM order_stats_daily WHERE day = CURRENT_DATE;
-- retorna em < 1ms
```

### ❌ Report entregue como JSON para 500k rows
```javascript
// ERRADO: serializar 500k objetos JS em JSON + string = GBs de RAM
const data = await db.transactions.findMany({ where: lastYear });
res.json(data); // process crash

// CORRETO: stream CSV diretamente para o cliente / S3
const stream = db.transactions.stream({ where: lastYear });
const upload = new PassThrough();
stream.pipe(csvStringify({ header: true })).pipe(upload);
await s3.upload({ Body: upload, Key: reportKey }).promise();
```

## QUALITY GATES
- [ ] Queries de relatório rodam em read replica (não no primário)
- [ ] Timezone explícito em todas as queries com DATE/range
- [ ] Exports > 1000 rows são assíncronos com job tracking
- [ ] Streaming implementado para geração de CSV/Excel
- [ ] Materialized views com índices e refresh CONCURRENT configurado
- [ ] Relatórios agendados com alertas de falha
- [ ] Limite de exports simultâneos por usuário
- [ ] Lag da read replica monitorado com alertas
- [ ] Download links com TTL (não permanentes)
- [ ] Estimativa de tempo/progresso para exports longos

## FORBIDDEN
- Queries analíticas pesadas no banco de produção primário
- Carregar dataset completo em memória antes de exportar
- Timezone implícito (UTC do servidor) em queries de date range para usuário
- `REFRESH MATERIALIZED VIEW` sem `CONCURRENTLY` em produção
- SQL gerado dinamicamente a partir de input do usuário sem whitelist de campos
- Export síncrono de datasets grandes em request HTTP
