---
name: data-write-query
description: Escreve SQL otimizado para o stack Evolution (PostgreSQL primário) com boas práticas. Use quando precisar traduzir uma necessidade de dados em SQL, construir uma query com múltiplas CTEs, joins e agregações, otimizar uma query contra tabelas grandes, ou obter sintaxe específica para consultas no banco do Evo CRM, Evo AI, ou qualquer serviço do stack Evolution. Dialetos secundários disponíveis: Snowflake, BigQuery, MySQL, DuckDB.
argument-hint: "<descrição do que você precisa consultar>"
---

# data-write-query — Escrever SQL Otimizado

Escreve uma query SQL a partir de uma descrição em linguagem natural, otimizada para o dialeto PostgreSQL (stack padrão Evolution) e seguindo boas práticas.

## Uso

```
/data-write-query <descrição do que você precisa consultar>
```

## Fluxo de Trabalho

### 1. Entender a Requisição

Analisar a descrição do usuário para identificar:

- **Colunas de saída**: Quais campos devem estar no resultado?
- **Filtros**: Quais condições limitam os dados (intervalos de tempo, segmentos, status)?
- **Agregações**: Há operações GROUP BY, contagens, somas, médias?
- **Joins**: É necessário combinar múltiplas tabelas?
- **Ordenação**: Como os resultados devem ser classificados?
- **Limites**: Há um requisito de top-N ou amostragem?

### 2. Determinar o Dialeto SQL

**Dialeto primário do workspace:**

- **PostgreSQL** — padrão para todo o stack Evolution (Evo CRM, Evo AI, serviços internos, Aurora RDS, Supabase, Neon)

**Dialetos secundários (se explicitamente solicitados):**
- Snowflake
- BigQuery (Google Cloud)
- Redshift (Amazon)
- Databricks SQL
- MySQL / Aurora MySQL
- DuckDB
- SQLite

Se o usuário não especificar, assumir **PostgreSQL** como padrão.

### 3. Descobrir o Schema (Se Conectado)

Se a fonte de dados estiver disponível via MCP ou CLI:

1. Buscar tabelas relevantes com base na descrição do usuário
2. Inspecionar nomes de colunas, tipos e relacionamentos
3. Verificar índices, particionamento ou clustering que afetam a performance
4. Procurar views ou views materializadas que possam simplificar a query

**Queries de exploração de schema (PostgreSQL):**

```sql
-- Listar todas as tabelas no schema
SELECT table_name, table_type
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Detalhes das colunas de uma tabela
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'nome_da_tabela'
ORDER BY ordinal_position;

-- Tamanho das tabelas
SELECT relname AS tabela,
       pg_size_pretty(pg_total_relation_size(relid)) AS tamanho_total
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;

-- Índices de uma tabela
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'nome_da_tabela';
```

### 4. Escrever a Query

Seguir estas boas práticas:

**Estrutura:**
- Usar CTEs (cláusulas WITH) para legibilidade quando queries têm múltiplos passos lógicos
- Uma CTE por transformação lógica ou fonte de dados
- Nomear CTEs de forma descritiva (ex: `novos_clientes_diarios`, `usuarios_ativos`, `receita_por_plano`)

**Performance:**
- Nunca usar `SELECT *` em queries de produção — especificar apenas as colunas necessárias
- Filtrar cedo (push de cláusulas WHERE o mais próximo possível das tabelas base)
- Usar filtros de partição quando disponíveis (especialmente partições de data)
- Preferir `EXISTS` sobre `IN` para subconsultas com grandes conjuntos de resultados
- Usar os tipos corretos de JOIN (não usar LEFT JOIN quando INNER JOIN é o correto)
- Evitar subconsultas correlacionadas quando um JOIN ou window function funciona
- Atenção a joins explosivos (many-to-many)

**Legibilidade:**
- Adicionar comentários explicando o "porquê" para lógica não óbvia
- Usar indentação e formatação consistentes
- Criar aliases de tabelas com nomes abreviados significativos (não apenas `a`, `b`, `c`)
- Colocar cada cláusula principal em sua própria linha

**Otimizações específicas do PostgreSQL:**

```sql
-- Usar EXPLAIN ANALYZE para entender o plano de execução
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ...;

-- Usar LIMIT + OFFSET para paginação
SELECT * FROM tabela
ORDER BY criado_em DESC
LIMIT 50 OFFSET 0;

-- Window functions eficientes no PostgreSQL
SELECT
    cliente_id,
    valor,
    SUM(valor) OVER (PARTITION BY cliente_id ORDER BY data_pagamento) AS valor_acumulado,
    ROW_NUMBER() OVER (PARTITION BY cliente_id ORDER BY data_pagamento DESC) AS rn
FROM pagamentos;

-- DISTINCT ON (específico do PostgreSQL) — mais eficiente que ROW_NUMBER
SELECT DISTINCT ON (cliente_id)
    cliente_id, plano, criado_em
FROM assinaturas
ORDER BY cliente_id, criado_em DESC;

-- Funções de data no PostgreSQL
DATE_TRUNC('month', criado_em)           -- Início do mês
EXTRACT(DOW FROM criado_em)              -- Dia da semana (0=domingo)
NOW() AT TIME ZONE 'America/Sao_Paulo'  -- Hora atual em BRT
criado_em AT TIME ZONE 'UTC' AT TIME ZONE 'America/Sao_Paulo' -- Converter para BRT
INTERVAL '30 days'                       -- Subtração de intervalo
DATE_PART('epoch', fim - inicio)        -- Diferença em segundos

-- JSON/JSONB (comum no stack Evolution)
dados->>'campo'                          -- Extrair como texto
dados->'campo'                           -- Extrair como JSON
jsonb_array_elements(dados->'lista')    -- Expandir array JSON
dados @> '{"status": "active"}'::jsonb  -- Contém (usa índice GIN)

-- Array operations
ANY(ARRAY['active', 'trial'])           -- In array
array_agg(campo ORDER BY data)          -- Agregar em array
unnest(tags)                            -- Expandir array em linhas
```

**Padrões de query para as fontes do workspace:**

```sql
-- Padrão: Análise de MRR mensal (típico para dados exportados do Stripe)
WITH receita_mensal AS (
    SELECT
        DATE_TRUNC('month', data_pagamento) AS mes,
        SUM(valor_cents) / 100.0 AS receita_total,
        COUNT(DISTINCT cliente_id) AS clientes_pagantes
    FROM pagamentos
    WHERE status = 'succeeded'
      AND data_pagamento >= NOW() - INTERVAL '12 months'
    GROUP BY 1
),
crescimento AS (
    SELECT
        mes,
        receita_total,
        clientes_pagantes,
        LAG(receita_total) OVER (ORDER BY mes) AS receita_anterior,
        ROUND(
            (receita_total - LAG(receita_total) OVER (ORDER BY mes)) /
            NULLIF(LAG(receita_total) OVER (ORDER BY mes), 0) * 100, 2
        ) AS crescimento_pct
    FROM receita_mensal
)
SELECT * FROM crescimento ORDER BY mes;

-- Padrão: Instâncias ativas com versão (típico para Licensing)
WITH instancias_ativas AS (
    SELECT
        instancia_id,
        versao,
        pais,
        criado_em,
        ultimo_ping
    FROM instancias
    WHERE ultimo_ping >= NOW() - INTERVAL '24 hours'
      AND status = 'active'
),
por_versao AS (
    SELECT
        versao,
        COUNT(*) AS total,
        COUNT(DISTINCT pais) AS paises_distintos
    FROM instancias_ativas
    GROUP BY 1
)
SELECT
    versao,
    total,
    paises_distintos,
    ROUND(total * 100.0 / SUM(total) OVER (), 2) AS percentual
FROM por_versao
ORDER BY total DESC;

-- Padrão: Análise de funil (Evo CRM)
WITH funil AS (
    SELECT
        DATE_TRUNC('week', criado_em) AS semana,
        COUNT(*) FILTER (WHERE etapa = 'lead') AS leads,
        COUNT(*) FILTER (WHERE etapa = 'qualificado') AS qualificados,
        COUNT(*) FILTER (WHERE etapa = 'proposta') AS propostas,
        COUNT(*) FILTER (WHERE etapa = 'fechado_ganho') AS fechados
    FROM oportunidades
    WHERE criado_em >= NOW() - INTERVAL '90 days'
    GROUP BY 1
)
SELECT
    semana,
    leads,
    qualificados,
    propostas,
    fechados,
    ROUND(qualificados * 100.0 / NULLIF(leads, 0), 1) AS taxa_qualificacao,
    ROUND(fechados * 100.0 / NULLIF(leads, 0), 1) AS taxa_fechamento
FROM funil
ORDER BY semana;

-- Padrão: Análise de cohort de retenção
WITH cohorts AS (
    SELECT
        cliente_id,
        DATE_TRUNC('month', primeira_assinatura) AS cohort_mes
    FROM clientes
),
atividade_mensal AS (
    SELECT DISTINCT
        cliente_id,
        DATE_TRUNC('month', data_evento) AS mes_ativo
    FROM eventos
),
retencao AS (
    SELECT
        c.cohort_mes,
        DATE_PART('month', AGE(a.mes_ativo, c.cohort_mes)) AS meses_depois,
        COUNT(DISTINCT c.cliente_id) AS clientes_retidos
    FROM cohorts c
    JOIN atividade_mensal a USING (cliente_id)
    WHERE a.mes_ativo >= c.cohort_mes
    GROUP BY 1, 2
),
tamanho_cohort AS (
    SELECT cohort_mes, COUNT(DISTINCT cliente_id) AS tamanho
    FROM cohorts
    GROUP BY 1
)
SELECT
    r.cohort_mes,
    r.meses_depois,
    r.clientes_retidos,
    tc.tamanho AS tamanho_cohort,
    ROUND(r.clientes_retidos * 100.0 / tc.tamanho, 1) AS taxa_retencao
FROM retencao r
JOIN tamanho_cohort tc USING (cohort_mes)
ORDER BY r.cohort_mes, r.meses_depois;
```

### 5. Apresentar a Query

Fornecer:

1. **A query completa** em bloco de código SQL com syntax highlighting
2. **Breve explicação** do que cada CTE ou seção faz
3. **Notas de performance** se relevantes (uso de índice, bottlenecks potenciais, custo esperado)
4. **Sugestões de modificação** — como ajustar para variações comuns (intervalo de tempo diferente, granularidade diferente, filtros adicionais)

### 6. Oferecer Execução

Se a fonte de dados estiver disponível via skill, oferecer executar a query e analisar os resultados. Se o usuário preferir executar manualmente, a query está pronta para copiar e colar.

## Exemplos

**Agregação simples:**
```
/data-write-query Contagem de assinaturas por plano nos últimos 30 dias
```

**Análise complexa:**
```
/data-write-query Análise de retenção por cohort — agrupar clientes pelo mês de assinatura, depois mostrar qual percentual ainda está ativo aos 1, 3, 6 e 12 meses
```

**Performance crítica:**
```
/data-write-query Temos uma tabela de eventos com 500M de linhas particionada por data. Encontrar os 100 usuários com mais eventos nos últimos 7 dias com o tipo de evento mais recente de cada um.
```

**Com timezone:**
```
/data-write-query Instâncias criadas esta semana, agrupadas por dia em BRT (America/Sao_Paulo)
```

## Dicas

- Mencionar o dialeto SQL upfront para obter a sintaxe correta imediatamente (PostgreSQL é o padrão)
- Se souber os nomes das tabelas, inclua-os — caso contrário, ajudaremos a encontrá-los
- Especificar se a query precisa ser idempotente (segura para re-executar) ou é para uso único
- Para queries recorrentes, mencionar se deve ser parametrizada para intervalos de datas
- Sempre especificar o fuso horário: o stack Evolution usa UTC no banco, BRT (America/Sao_Paulo) na exibição
- Mencionar se precisa de EXPLAIN ANALYZE para diagnóstico de performance
