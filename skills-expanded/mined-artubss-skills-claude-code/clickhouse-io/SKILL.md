---
name: clickhouse-io
description: Padrões de banco de dados ClickHouse, otimização de consultas, analytics e melhores práticas de engenharia de dados para cargas de trabalho analíticas de alto desempenho.
author: affaan-m
version: "1.0"
---

# Padrões de Analytics com ClickHouse

Padrões específicos do ClickHouse para analytics de alto desempenho e engenharia de dados.

## Visão Geral

ClickHouse é um sistema de gerenciamento de banco de dados (DBMS) orientado por colunas para processamento analítico online (OLAP). É otimizado para consultas analíticas rápidas em grandes conjuntos de dados.

**Principais Características:**
- Armazenamento orientado por colunas
- Compressão de dados
- Execução de consultas paralela
- Consultas distribuídas
- Analytics em tempo real

## Padrões de Design de Tabelas

### Motor MergeTree (Mais Comum)

```sql
CREATE TABLE markets_analytics (
    date Date,
    market_id String,
    market_name String,
    volume UInt64,
    trades UInt32,
    unique_traders UInt32,
    avg_trade_size Float64,
    created_at DateTime
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(date)
ORDER BY (date, market_id)
SETTINGS index_granularity = 8192;
```

### ReplacingMergeTree (Deduplicação)

```sql
-- Para dados que podem ter duplicatas (ex: de múltiplas fontes)
CREATE TABLE user_events (
    event_id String,
    user_id String,
    event_type String,
    timestamp DateTime,
    properties String
) ENGINE = ReplacingMergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (user_id, event_id, timestamp)
PRIMARY KEY (user_id, event_id);
```

### AggregatingMergeTree (Pré-agregação)

```sql
-- Para manter métricas agregadas
CREATE TABLE market_stats_hourly (
    hour DateTime,
    market_id String,
    total_volume AggregateFunction(sum, UInt64),
    total_trades AggregateFunction(count, UInt32),
    unique_users AggregateFunction(uniq, String)
) ENGINE = AggregatingMergeTree()
PARTITION BY toYYYYMM(hour)
ORDER BY (hour, market_id);

-- Consultar dados agregados
SELECT
    hour,
    market_id,
    sumMerge(total_volume) AS volume,
    countMerge(total_trades) AS trades,
    uniqMerge(unique_users) AS users
FROM market_stats_hourly
WHERE hour >= toStartOfHour(now() - INTERVAL 24 HOUR)
GROUP BY hour, market_id
ORDER BY hour DESC;
```

## Padrões de Otimização de Consultas

### Filtragem Eficiente

```sql
-- ✅ BOM: Use colunas indexadas primeiro
SELECT *
FROM markets_analytics
WHERE date >= '2025-01-01'
  AND market_id = 'market-123'
  AND volume > 1000
ORDER BY date DESC
LIMIT 100;

-- ❌ RUIM: Filtre em colunas não indexadas primeiro
SELECT *
FROM markets_analytics
WHERE volume > 1000
  AND market_name LIKE '%election%'
  AND date >= '2025-01-01';
```

### Agregações

```sql
-- ✅ BOM: Use funções de agregação específicas do ClickHouse
SELECT
    toStartOfDay(created_at) AS day,
    market_id,
    sum(volume) AS total_volume,
    count() AS total_trades,
    uniq(trader_id) AS unique_traders,
    avg(trade_size) AS avg_size
FROM trades
WHERE created_at >= today() - INTERVAL 7 DAY
GROUP BY day, market_id
ORDER BY day DESC, total_volume DESC;

-- ✅ Use quantile para percentis (mais eficiente que percentile)
SELECT
    quantile(0.50)(trade_size) AS median,
    quantile(0.95)(trade_size) AS p95,
    quantile(0.99)(trade_size) AS p99
FROM trades
WHERE created_at >= now() - INTERVAL 1 HOUR;
```

### Window Functions

```sql
-- Calcular totais acumulados
SELECT
    date,
    market_id,
    volume,
    sum(volume) OVER (
        PARTITION BY market_id
        ORDER BY date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_volume
FROM markets_analytics
WHERE date >= today() - INTERVAL 30 DAY
ORDER BY market_id, date;
```

## Padrões de Inserção de Dados

### Bulk Insert (Recomendado)

```typescript
import { ClickHouse } from 'clickhouse'

const clickhouse = new ClickHouse({
  url: process.env.CLICKHOUSE_URL,
  port: 8123,
  basicAuth: {
    username: process.env.CLICKHOUSE_USER,
    password: process.env.CLICKHOUSE_PASSWORD
  }
})

// ✅ Inserção em lote (eficiente)
async function bulkInsertTrades(trades: Trade[]) {
  const values = trades.map(trade => `(
    '${trade.id}',
    '${trade.market_id}',
    '${trade.user_id}',
    ${trade.amount},
    '${trade.timestamp.toISOString()}'
  )`).join(',')

  await clickhouse.query(`
    INSERT INTO trades (id, market_id, user_id, amount, timestamp)
    VALUES ${values}
  `).toPromise()
}

// ❌ Inserções individuais (lento)
async function insertTrade(trade: Trade) {
  // Não faça isso em um loop!
  await clickhouse.query(`
    INSERT INTO trades VALUES ('${trade.id}', ...)
  `).toPromise()
}
```

### Streaming Insert

```typescript
// Para ingestão contínua de dados
import { createWriteStream } from 'fs'
import { pipeline } from 'stream/promises'

async function streamInserts() {
  const stream = clickhouse.insert('trades').stream()

  for await (const batch of dataSource) {
    stream.write(batch)
  }

  await stream.end()
}
```

## Materialized Views

### Agregações em Tempo Real

```sql
-- Criar view materializada para estatísticas horárias
CREATE MATERIALIZED VIEW market_stats_hourly_mv
TO market_stats_hourly
AS SELECT
    toStartOfHour(timestamp) AS hour,
    market_id,
    sumState(amount) AS total_volume,
    countState() AS total_trades,
    uniqState(user_id) AS unique_users
FROM trades
GROUP BY hour, market_id;

-- Consultar a view materializada
SELECT
    hour,
    market_id,
    sumMerge(total_volume) AS volume,
    countMerge(total_trades) AS trades,
    uniqMerge(unique_users) AS users
FROM market_stats_hourly
WHERE hour >= now() - INTERVAL 24 HOUR
GROUP BY hour, market_id;
```

## Monitoramento de Desempenho

### Performance de Consultas

```sql
-- Verificar consultas lentas
SELECT
    query_id,
    user,
    query,
    query_duration_ms,
    read_rows,
    read_bytes,
    memory_usage
FROM system.query_log
WHERE type = 'QueryFinish'
  AND query_duration_ms > 1000
  AND event_time >= now() - INTERVAL 1 HOUR
ORDER BY query_duration_ms DESC
LIMIT 10;
```

### Estatísticas de Tabelas

```sql
-- Verificar tamanhos de tabelas
SELECT
    database,
    table,
    formatReadableSize(sum(bytes)) AS size,
    sum(rows) AS rows,
    max(modification_time) AS latest_modification
FROM system.parts
WHERE active
GROUP BY database, table
ORDER BY sum(bytes) DESC;
```

## Consultas de Analytics Comuns

### Análise de Série Temporal

```sql
-- Usuários ativos diários
SELECT
    toDate(timestamp) AS date,
    uniq(user_id) AS daily_active_users
FROM events
WHERE timestamp >= today() - INTERVAL 30 DAY
GROUP BY date
ORDER BY date;

-- Análise de retenção
SELECT
    signup_date,
    countIf(days_since_signup = 0) AS day_0,
    countIf(days_since_signup = 1) AS day_1,
    countIf(days_since_signup = 7) AS day_7,
    countIf(days_since_signup = 30) AS day_30
FROM (
    SELECT
        user_id,
        min(toDate(timestamp)) AS signup_date,
        toDate(timestamp) AS activity_date,
        dateDiff('day', signup_date, activity_date) AS days_since_signup
    FROM events
    GROUP BY user_id, activity_date
)
GROUP BY signup_date
ORDER BY signup_date DESC;
```

### Análise de Funnel

```sql
-- Funnel de conversão
SELECT
    countIf(step = 'viewed_market') AS viewed,
    countIf(step = 'clicked_trade') AS clicked,
    countIf(step = 'completed_trade') AS completed,
    round(clicked / viewed * 100, 2) AS view_to_click_rate,
    round(completed / clicked * 100, 2) AS click_to_completion_rate
FROM (
    SELECT
        user_id,
        session_id,
        event_type AS step
    FROM events
    WHERE event_date = today()
)
GROUP BY session_id;
```

### Análise de Cohort

```sql
-- Cohorts de usuários por mês de inscrição
SELECT
    toStartOfMonth(signup_date) AS cohort,
    toStartOfMonth(activity_date) AS month,
    dateDiff('month', cohort, month) AS months_since_signup,
    count(DISTINCT user_id) AS active_users
FROM (
    SELECT
        user_id,
        min(toDate(timestamp)) OVER (PARTITION BY user_id) AS signup_date,
        toDate(timestamp) AS activity_date
    FROM events
)
GROUP BY cohort, month, months_since_signup
ORDER BY cohort, months_since_signup;
```

## Padrões de Data Pipeline

### Padrão ETL

```typescript
// Extract, Transform, Load
async function etlPipeline() {
  // 1. Extrair de fonte
  const rawData = await extractFromPostgres()

  // 2. Transformar
  const transformed = rawData.map(row => ({
    date: new Date(row.created_at).toISOString().split('T')[0],
    market_id: row.market_slug,
    volume: parseFloat(row.total_volume),
    trades: parseInt(row.trade_count)
  }))

  // 3. Carregar no ClickHouse
  await bulkInsertToClickHouse(transformed)
}

// Executar periodicamente
setInterval(etlPipeline, 60 * 60 * 1000)  // A cada hora
```

### Change Data Capture (CDC)

```typescript
// Ouvir mudanças do PostgreSQL e sincronizar com ClickHouse
import { Client } from 'pg'

const pgClient = new Client({ connectionString: process.env.DATABASE_URL })

pgClient.query('LISTEN market_updates')

pgClient.on('notification', async (msg) => {
  const update = JSON.parse(msg.payload)

  await clickhouse.insert('market_updates', [
    {
      market_id: update.id,
      event_type: update.operation,  // INSERT, UPDATE, DELETE
      timestamp: new Date(),
      data: JSON.stringify(update.new_data)
    }
  ])
})
```

## Melhores Práticas

### 1. Estratégia de Particionamento
- Particionar por tempo (geralmente mês ou dia)
- Evitar muitas partições (impacto na performance)
- Use tipo DATE para chave de partição

### 2. Chave de Ordenação
- Coloque colunas mais frequentemente filtradas primeiro
- Considere cardinalidade (alta cardinalidade primeiro)
- A ordem impacta a compressão

### 3. Tipos de Dados
- Use o tipo apropriado mais pequeno (UInt32 vs UInt64)
- Use LowCardinality para strings repetidas
- Use Enum para dados categóricos

### 4. Evitar
- SELECT * (especifique colunas)
- FINAL (mescle dados antes da consulta)
- Muitos JOINs (desnormalize para analytics)
- Inserções pequenas e frequentes (agrupe em lote)

### 5. Monitoramento
- Rastrear performance de consultas
- Monitorar uso de disco
- Verificar operações de merge
- Revisar log de consultas lentas

**Lembre-se**: ClickHouse se destaca em cargas de trabalho analíticas. Projete tabelas para seus padrões de consulta, agrupe inserções em lote e aproveite materialized views para agregações em tempo real.