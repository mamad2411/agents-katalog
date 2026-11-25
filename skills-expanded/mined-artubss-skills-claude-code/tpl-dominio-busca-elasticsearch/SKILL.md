---
name: tpl-dominio-busca-elasticsearch
description: Template do pack (dominio/10-busca-elasticsearch.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/10-busca-elasticsearch.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Sistema de Busca com Elasticsearch

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/10-busca-elasticsearch.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Elasticsearch é poderoso e fácil de usar de forma errada. Mapping definido incorretamente
não pode ser corrigido sem reindexar. Relevância sem tuning retorna resultados ruins que
destroem a experiência. Sincronização com banco de dados gera eventual consistency —
os times esquecem que buscas mostram dados potencialmente stale.

## STACK ASSUMPTIONS
- Search: Elasticsearch 8.x / OpenSearch 2.x
- Client: @elastic/elasticsearch (Node.js) ou elasticsearch-py
- DB: PostgreSQL como source of truth
- Sync: CDC (Debezium) ou event-driven via queue
- Cache: Redis para queries repetitivas de alta frequência

## CORE CONCEPTS
- **Index**: equivalente a uma tabela no Elasticsearch
- **Mapping**: schema do index — define tipos dos campos (keyword, text, integer, etc.)
- **Analyzer**: como o texto é tokenizado para busca (standard, portuguese, custom)
- **Inverted Index**: estrutura interna que torna busca full-text rápida
- **Relevance Score (_score)**: pontuação de relevância calculada por BM25
- **Aggregation**: facets, contagens, histogramas — usado em filtros de e-commerce
- **Boost**: multiplicar score de campos específicos (título > descrição)
- **Alias**: apontar para index real — permite blue-green reindex sem downtime

## ARCHITECTURE RULES

### Mapping Strategy
- Definir mapping EXPLICITAMENTE antes de indexar qualquer documento
- Nunca usar dynamic mapping em produção (campos inesperados criam mapping ruim)
- `keyword` para campos filtráveis/aggregáveis (id, status, category)
- `text` para campos de busca full-text (title, description)
- `keyword` + `text` no mesmo campo: use `fields` multi-field
- Campos numéricos: `integer`/`float`/`double` (não `text`)
- Datas: `date` com formato explícito

```json
"title": {
  "type": "text",
  "analyzer": "portuguese",
  "fields": {
    "keyword": { "type": "keyword" }
  }
}
```

### Analyzer Configuration
- Português: `portuguese` analyzer com stemming
- Autocomplete: `edge_ngram` tokenizer (min 2, max 10 chars)
- Search-as-you-type: tipo nativo `search_as_you_type` ou custom edge_ngram
- Synonyms: synonym token filter com arquivo de sinônimos externos (sem reindex para atualizar)
- Test analyzers: `POST /{index}/_analyze` antes de criar index

### Relevance Tuning
- Boost por campo: título (3x) > categoria (2x) > tags (1.5x) > descrição (1x)
- Boost por recência: `gauss` decay function no `published_at`
- Boost por popularidade: field `view_count` com `field_value_factor`
- Function score combinado: relevância textual + decay temporal + popularidade
- A/B test relevance: log query + resultado + click para medir CTR

### Reindex Strategy (Zero Downtime)
```
1. Criar novo index: products_v2 (com novo mapping)
2. Iniciar reindex: POST /_reindex (source: products_v1, dest: products_v2)
3. Durante reindex: novos documentos indexados em AMBOS indexes
4. Aguardar reindex completar → validar contagem + spot check
5. Atualizar alias: products → products_v2
6. Parar de indexar em products_v1
7. Deletar products_v1 após verificação de 24h
```

### Sync Strategy (DB → ES)
- **Event-driven**: após escribas no DB, enfileirar job de reindex do documento
- **CDC (Debezium)**: capturar changes do WAL do PostgreSQL → publicar em Kafka → worker indexa
- **Polling**: job periódico (a cada 30s) buscando `updated_at > last_sync` — simples mas com lag
- Nunca indexar diretamente no ES dentro de transaction de banco
- Sempre indexar assincronamente (em falha do ES, o dado está no DB)

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| GET /search?q=...&category=...&sort=... | Query ES com filtros + facets + paginação |
| GET /search/autocomplete?q=... | Query `search_as_you_type` ou edge_ngram |
| Business event: product.created | Enfileirar job: index document no ES |
| Business event: product.updated | Enfileirar job: partial update (`_update`) no ES |
| Business event: product.deleted | Enfileirar job: delete document do ES |
| GET /search/facets?category=... | Aggregations: contagem por filtro |
| POST /admin/search/reindex | Iniciar reindex completo (via job, não síncrono) |
| GET /admin/search/reindex/:jobId | Status do reindex em andamento |
| GET /admin/search/health | Status do cluster ES + lag de sincronização |
| POST /admin/search/analyzers/test | Testar analyzer em texto específico |
| GET /admin/search/mapping | Exibir mapping atual do index |

## CRITICAL RULES
1. Mapping explícito SEMPRE — nunca dynamic mapping em produção
2. Usar alias (não nome do index direto) em todas as queries da aplicação
3. Reindex sempre via alias swap — nunca recriar index com mesmo nome
4. ES não é fonte de verdade — banco de dados sempre é authoritative
5. Falha ao indexar no ES não deve falhar a operação principal (async)
6. Nunca deletar o index sem ter backup ou possibilidade de reindexar
7. Queries de busca sempre com `timeout` configurado (ex: 5s)
8. Aggregation em campos `text` é proibido (usar `keyword` sub-field)
9. Paginação profunda (`from: 10000`) proibida — usar search_after
10. Logs de query com tempo de execução para monitorar regressões de performance

## COMMON PITFALLS

### ❌ Dynamic mapping cria campo text onde deveria ser keyword
```json
// ERRADO: produto es indexado sem mapping → status vira "text"
PUT /products/_doc/1 { "status": "published" }
// Agora `status` é "text" e não pode ser usado em aggregations/filters eficientemente

// CORRETO: mapping explícito antes de indexar
PUT /products { "mappings": { "properties": { "status": { "type": "keyword" } } } }
```

### ❌ Paginação com `from` alto (deep pagination)
```json
// ERRADO: ES lê e descarta 10.000 documentos — caro e lento
GET /products/_search { "from": 10000, "size": 20 }

// CORRETO: search_after com sort
GET /products/_search {
  "size": 20,
  "sort": [{ "created_at": "desc" }, { "_id": "asc" }],
  "search_after": ["2024-01-15T10:00:00", "last-seen-id"]
}
```

### ❌ Indexar dentro de transaction de banco
```javascript
// ERRADO: se ES falhar, a transaction faz rollback desnecessário
await db.transaction(async (trx) => {
  await trx.products.create(product);
  await es.index({ index: 'products', document: product }); // falha aqui = rollback
});

// CORRETO: salvar no banco → disparar evento → worker indexa assincronamente
await db.products.create(product);
await queue.add('index-product', { productId: product.id });
```

## QUALITY GATES
- [ ] Mapping explícito definido antes do primeiro documento indexado
- [ ] Todos os queries usam alias (não nome do index diretamente)
- [ ] Paginação usando search_after (não from/size para páginas > 100)
- [ ] Aggregations apenas em campos `keyword`
- [ ] Queries com timeout configurado
- [ ] Lag de sincronização monitorado (alerta se > 60s)
- [ ] Procedure de reindex zero-downtime documentada e testada
- [ ] Analyzers testados com conteúdo real antes de criar index
- [ ] Falha no ES não quebra a operação principal
- [ ] Relevance score validado com queries de teste regulares

## FORBIDDEN
- Dynamic mapping em produção
- Aggregations em campos do tipo `text`
- `from` > 1000 em queries de busca (deep pagination)
- Índice direto por nome (sem alias) em código de aplicação
- Indexar documentos dentro de transações de banco de dados
- Usar ES como banco de dados principal (sem DB relacional como fallback)
- Deletar e recriar index com o mesmo nome (perda do alias + downtime)
