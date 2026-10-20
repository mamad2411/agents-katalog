---
name: equipe-agil-data-engineer-knowledge
description: Conhecimento específico do Data Engineer da Equipe Backend Ágil Kanban+XP. Cobre evolução de schema relacional sem downtime (Ambler & Sadalage — expand-contract / transition phase) com Flyway/Liquibase em CI, Hibernate ORM Panache + Envers, modelos de dados (Kleppmann — relacional vs documento vs grafo), modelagem dimensional (Kimball), Change Data Capture (Debezium → Kafka), event sourcing, contratos de dataset (Data Mesh), data reliability (Majors), particionamento, índices, transactional outbox visto do lado do banco. Owner técnico das migrações no pipeline. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# Data Engineer — Conhecimento específico

Skill carregada pelo agente `equipe-agil-data-engineer` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`. Cobre o conhecimento de **dados** que o time precisa para evoluir schema, modelar persistência e integrar dados entre serviços, mantendo zero downtime e contratos estáveis.

## 1. Conceitos centrais

### 1.1 Mandato do Data Engineer na equipe

- **Owner técnico das migrações de banco** — toda mudança de schema passa por ele (A/R).
- **Modelagem de persistência** dos agregados (com Arquiteto App e Tech Lead).
- **CDC, outbox, inbox** vistos do lado do banco (com Arquiteto Sis).
- **Contratos de dataset** quando dado sai do serviço para consumo analítico (Data Mesh).
- **Performance de query** — N+1, índices, particionamento, plan de execução.
- **Não decide** estilo arquitetural (Arquiteto Sis) nem código de aplicação (Tech Lead), mas é **C** em ambos quando há impacto em dado.
- RACI: A/R em schema/migration/observabilidade-de-dado; C em modelagem de agregado e em decisões inter-serviço que envolvem fluxo de dado.

### 1.2 Stack default

- **Postgres** como banco relacional default da equipe (ajustável por projeto — Oracle/DB2 em alguns legados).
- **Flyway** (`quarkus-flyway`) como migration tool — scripts SQL versionados em `src/main/resources/db/migration/V<n>__<descricao>.sql`.
- **Hibernate ORM com Panache** + **Hibernate Envers** (auditoria) — vide `tech-lead-knowledge` §1.6.
- **Debezium** para Change Data Capture (read replica → Kafka).
- **Kafka** via SmallRye Reactive Messaging para fluxo de eventos de dado.
- Para analítico (quando aplicável): warehouse externo (BigQuery/Snowflake/Redshift) alimentado por CDC + dbt; raramente responsabilidade da equipe de produto (pode ser plataforma de dados).

### 1.3 Refactoring Databases (Ambler & Sadalage) — expand-contract / transition phase

**Problema**: schema mudou. Como migrar sem downtime e sem quebrar consumidores em rolling deploy?

**Padrão expand-contract (também chamado *parallel change*, *transition phase*)**:

1. **Expand** — adicione o novo (coluna, tabela, índice) **sem remover** o antigo. Schema compatível com **versão antiga e nova** do código.
2. **Migrate** — backfill (preencher novo a partir do antigo); triggers para manter sincronizado durante o período de transição.
3. **Contract** — quando todas as instâncias do código usam o novo, remova o antigo em outra migração separada.

**Exemplo concreto — renomear coluna `nome_cliente` para `cliente_nome`**:

```sql
-- V20260523_1__add_cliente_nome.sql  (EXPAND)
ALTER TABLE pedido ADD COLUMN cliente_nome VARCHAR(200);

UPDATE pedido SET cliente_nome = nome_cliente WHERE cliente_nome IS NULL;

CREATE OR REPLACE FUNCTION sync_cliente_nome() RETURNS trigger AS $$
BEGIN
  IF NEW.cliente_nome IS NULL THEN NEW.cliente_nome := NEW.nome_cliente; END IF;
  IF NEW.nome_cliente IS NULL THEN NEW.nome_cliente := NEW.cliente_nome; END IF;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_cliente_nome BEFORE INSERT OR UPDATE ON pedido
  FOR EACH ROW EXECUTE FUNCTION sync_cliente_nome();
```

Deploy do código que lê/escreve em `cliente_nome` (passa por todas as instâncias).

```sql
-- V20260530_1__drop_nome_cliente.sql  (CONTRACT — semanas depois)
DROP TRIGGER trg_sync_cliente_nome ON pedido;
DROP FUNCTION sync_cliente_nome();
ALTER TABLE pedido DROP COLUMN nome_cliente;
```

**Heurística**: nunca faça expand + contract no mesmo deploy. Sempre janela de transição cobrindo ≥ 1 release completo.

### 1.4 Catálogo de mudanças seguras vs perigosas (Postgres)

| Mudança | Custo | Bloqueia? | Padrão |
|---------|-------|-----------|--------|
| `ADD COLUMN` (sem default) | barato | breve lock metadata | direto |
| `ADD COLUMN ... DEFAULT <constant>` (PG 11+) | barato | breve | direto |
| `ADD COLUMN ... DEFAULT <volatile>` | rewrite | longo | EVITAR; backfill em lote |
| `ALTER COLUMN ... TYPE` | rewrite | longo | expand-contract |
| `ALTER COLUMN ... SET NOT NULL` | scan | médio | adicionar coluna nova + backfill + swap |
| `DROP COLUMN` | barato | breve | expand-contract (deploy primeiro) |
| `CREATE INDEX` | longo | bloqueia escrita | `CREATE INDEX CONCURRENTLY` |
| `DROP INDEX` | barato | breve | `DROP INDEX CONCURRENTLY` |
| `ADD CONSTRAINT` (FK, CHECK) | scan | médio | `NOT VALID` + `VALIDATE` em duas etapas |
| `RENAME` | barato | breve | expand-contract (view de compat) |

### 1.5 Flyway no pipeline da equipe

- Scripts em `src/main/resources/db/migration/V<timestamp>__<descricao>.sql`.
- Quarkus aplica no startup (`quarkus.flyway.migrate-at-start=true` em dev/test; em produção via job/init container).
- **Imutabilidade**: script já aplicado **não muda**. Erro? Nova migração que corrige.
- **Sem `R__` (repeatable)** para schema produtivo (perigoso em rolling).
- Validação no pipeline:
  - Lint SQL (estilo, perigos comuns).
  - Análise de bloqueio (estática quando possível; manual no review).
  - Dry-run em snapshot de produção sintético (Testcontainers + dump fake).
  - `flyway:validate` no CI.

### 1.6 Hibernate ORM com Panache (DataE perspective)

Vide `tech-lead-knowledge` §1.6 para sintaxe básica. Aqui o DataE pensa em:

- **Mapeamento de Value Object** em campo (use `@Embeddable` ou converter custom).
- **Coleções**: `@OneToMany` vs `@ElementCollection` — `@ElementCollection` para coleção de Value Objects, evita entidade fantasma.
- **Lazy vs Eager**:
  - **Default**: lazy (`@ManyToOne(fetch=LAZY)` é o desejável; JPA default eager para `@ManyToOne` — corrigir).
  - **Resolver N+1**: `JOIN FETCH` em queries que precisam do colaborador, ou `@BatchSize`/`@Fetch(SUBSELECT)`.
- **Identidade**: UUID v7 (time-ordered) é melhor que UUID v4 para B-tree; `IDENTITY` evita roundtrip de sequence.
- **Versionamento otimista**: `@Version` em agregados que sofrem concorrência.

### 1.7 Hibernate Envers — auditoria automática

- Anotar entidade com `@Audited`.
- Cria tabela `<entidade>_AUD` que registra cada versão (revision id, action, valores).
- Útil para auditoria regulatória; **não confundir** com event sourcing (Envers persiste estado, não eventos de domínio).
- Custo: 2× espaço; queries de auditoria via `AuditReader`.

### 1.8 Modelos de dados (Kleppmann)

- **Relacional** — default para dados transacionais, com integridade referencial.
- **Documento** — bom para agregado autocontido sem joins complexos; perde flexibilidade ad-hoc.
- **Grafo** — relacionamentos densos e queries de N graus (recomendação, social).
- **Key-value** — cache, contadores, sessão; sem schema.
- **Wide-column** — escala horizontal massiva (Cassandra) com queries previsíveis.

**Heurística da equipe**: Postgres resolve **a maioria** dos casos (relacional + JSONB para flexibilidade pontual + extensões PostGIS/full-text). Adotar outro modelo exige ASR/risco que justifique.

### 1.9 Modelagem dimensional (Kimball) — quando o time toca analítico

- **Fact table** — eventos mensuráveis (pedido, pagamento, clique). Tem chaves + métricas.
- **Dimension table** — contexto (cliente, produto, tempo, geografia). Tem atributos descritivos.
- **Star schema** — fact no centro, dimensions ao redor. Performance e legibilidade ótimas.
- **Slowly Changing Dimensions (SCD)**:
  - Type 1 — sobrescreve (histórico se perde).
  - Type 2 — nova linha com `valid_from`/`valid_to` (mantém histórico).
  - Type 3 — coluna extra `old_value` (limita).

Na equipe de produto: raramente modelamos warehouse diretamente. Geralmente expomos eventos via CDC e plataforma de dados modela o star schema downstream.

### 1.10 Change Data Capture (CDC) com Debezium

- Lê o WAL (write-ahead log) do Postgres via replication slot (sem load adicional na tabela).
- Publica eventos `c` (create), `u` (update), `d` (delete), `r` (read snapshot inicial) em tópicos Kafka.
- **Outbox Event Router** (extensão Debezium): lê tabela `outbox` e roteia como evento de domínio (sem expor dado raw da tabela do agregado) — vide `arquiteto-sis-knowledge` §1.11.
- **Cuidados**:
  - Replication slot acumula WAL se consumidor parar — risco de encher disco. Monitorar.
  - Schema evolution: registro Avro/Protobuf com schema registry; mudança breaking quebra consumer.
  - Snapshot inicial pode ser longo em tabela grande — usar *incremental snapshot* (Debezium 2+).

### 1.11 Event Sourcing — quando faz sentido

- Estado é **derivado** de log imutável de eventos.
- Bom para auditoria forte, replay para reconstruir estado, time travel.
- **Custo alto**: queries precisam de projeção (read model); schema de evento é contrato eterno; refactor pesado.
- **Heurística**: não adote por padrão. Adote quando ASR explicitamente exige (regulatório, BI fino, replay para correção em massa). Vide `arquiteto-sis-knowledge` §1.12.

### 1.12 Contratos de dataset (Data Mesh — vide `arquiteto-sis-knowledge` §1.17)

Quando o time publica dado para consumo analítico ou para outros bounded contexts:

- **Schema versionado** (Avro/Protobuf/JSON Schema) no registry.
- **SLA do dataset**: frescor (latency de atualização), completude, precisão.
- **Documentação**: dicionário (cada coluna com semântica e domínio de valores).
- **Política de retenção** explícita.
- **Owner** declarado (o time).
- **Compatibilidade** declarada (backward/forward).

### 1.13 Data reliability (Majors et al.)

- Toda métrica precisa de **observabilidade**: lag de replicação, lag de CDC, idade da última transação, tamanho do replication slot, índices não usados, queries lentas (`pg_stat_statements`).
- **Backup + restore** — não basta backup; teste restore mensalmente (ou o backup é teatro).
- **PITR (Point-In-Time Recovery)** — capacidade de voltar a qualquer ponto via WAL.
- **Read replicas** para reduzir carga no primário; ler-de-réplica é decisão de design (consistência eventual).
- **Capacity planning** — projetar crescimento de dado/IO ao longo de N meses; pré-provisionar antes do gargalo.

### 1.14 N+1, índices, planos de execução — armadilhas comuns

- **N+1**: detectar com Hibernate statistics ou logs de SQL; resolver com `JOIN FETCH`, `@BatchSize` ou query dedicada.
- **Índice ausente**: `EXPLAIN ANALYZE` mostra seq scan em tabela grande; criar índice (concurrent em prod).
- **Índice em coluna de baixa cardinalidade**: Postgres ignora; use parcial (`WHERE status = 'PENDENTE'`) ou expression index.
- **Atualização de toda a linha**: HOT update precisa que a coluna alterada **não** seja indexada — toda mudança gera bloat.
- **Bloat**: `VACUUM` regular; `pg_repack` quando bloat alto.
- **Sequential scan em tabela grande**: pode ser melhor que index scan dependendo da seletividade — ler `EXPLAIN`.

## 2. Práticas e heurísticas operacionais

### 2.1 Workflow de toda migração de schema

1. **PR `pr-*` na `feature/*` do time** com o script Flyway.
2. **Lint SQL + revisão** — DataE é reviewer obrigatório.
3. **CI roda migração** em container vazio (Testcontainers) — verifica que não quebra.
4. **CI roda migração contra snapshot** de produção sintético — verifica que migra dado real sem perda.
5. **Quando expand-contract**: PR só com `expand`; deploy completo; nova PR após semanas com `contract`.
6. **Documentação no ADR** se a mudança altera contrato externo (evento, dataset publicado).

### 2.2 Checklist "essa mudança de schema é segura?"

- [ ] Aplica `CREATE INDEX CONCURRENTLY` em vez de `CREATE INDEX`?
- [ ] `ADD CONSTRAINT` em duas etapas (`NOT VALID` + `VALIDATE`)?
- [ ] `ALTER COLUMN TYPE` foi quebrado em expand + backfill + contract?
- [ ] `DROP COLUMN` espera deploy de código novo primeiro?
- [ ] Compatível com versão **anterior** do código (rolling deploy)?
- [ ] Backfill é **idempotente** (pode rodar duas vezes sem corromper)?
- [ ] Lock estimado < 1 segundo? Se não, plano de janela.
- [ ] Sem `SELECT *` no backfill (limita batch).
- [ ] Backup recente confirmado antes da migração em produção.

### 2.3 Anti-padrões frequentes

- ❌ **Migração que altera dado em massa sem batch** — lock longo, replicação atrasa.
- ❌ **`CREATE INDEX` sem CONCURRENTLY** em produção — bloqueia escrita.
- ❌ **`UPDATE` sem `WHERE` em milhões de linhas** — bloat catastrófico.
- ❌ **`SELECT *` em código de aplicação** — quebra ao adicionar coluna; pega bytes a mais.
- ❌ **Compartilhar banco entre serviços** — acoplamento por dado (vide `arquiteto-sis-knowledge` §2.7).
- ❌ **Schema livre em produção** (sem migration versionada) — drift entre ambientes.
- ❌ **Evento na fila com dado mutável referenciado** — consumidor vê estado inconsistente.
- ❌ **Replication slot sem alarme de lag** — encheu disco, sistema parou.
- ❌ **`COUNT(*)` em tabela grande** — caro; usar tabela de contador atualizada por trigger ou aproximação `pg_stat_user_tables.n_live_tup`.

### 2.4 Quando o DataE entra no Replenishment

- Item que cria/altera tabela, índice, constraint, view → DataE C obrigatório.
- Item que adiciona dado novo a evento → DataE C (schema compatibility).
- Item que muda contrato de dataset publicado → DataE A/R no contrato.
- Item que cria report novo → conversa sobre origem (CDC? batch? on-demand?).

### 2.5 Colaboração com outros papéis

- **Arquiteto App** — onde mora a entidade JPA, repository, agregado.
- **Arquiteto Sis** — outbox/CDC/contrato de evento.
- **Tech Lead** — Hibernate idiomático, performance de query.
- **SRE** — observabilidade de banco (golden signals do DB).
- **AppSec** — encriptação em repouso/trânsito, mascaramento, retenção.
- **DevOps** — provisionamento de banco, backup, monitoração.

## 3. Templates e checklists

### 3.1 Convenção de nomes Flyway

```
V<yyyymmdd>_<seq>__<descricao_em_snake_case>.sql

Ex.:
  V20260523_1__create_pedido.sql
  V20260523_2__add_pedido_status_index.sql
  V20260601_1__expand_cliente_nome.sql
  V20260615_1__contract_drop_nome_cliente.sql
```

Sufixo numérico (`_1`, `_2`) evita colisão quando dois PRs no mesmo dia.

### 3.2 Template de migração com index concurrent

```sql
-- V<ts>__add_index_pedido_cliente.sql
-- Postgres exige CONCURRENTLY fora de bloco transacional.
-- Flyway: use prefixo "I" ou marca de "transactional=false" (consultar versão).
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_pedido_cliente_id
  ON pedido (cliente_id);
```

### 3.3 Template de adição de coluna NOT NULL (3 migrações)

```sql
-- 1) V<ts1>__add_email_nullable.sql
ALTER TABLE cliente ADD COLUMN email VARCHAR(200);

-- (deploy do código que escreve email)

-- 2) V<ts2>__backfill_email.sql
UPDATE cliente SET email = 'desconhecido+' || id || '@local' WHERE email IS NULL;

-- 3) V<ts3>__email_not_null.sql
ALTER TABLE cliente ALTER COLUMN email SET NOT NULL;
```

### 3.4 Template de contrato de dataset publicado

```yaml
dataset: pedidos.aprovados.v1
owner: time-aco-pedidos
schema: AsyncAPI/Avro v1
sla:
  frescor: < 5 min
  completude: ≥ 99,99%
  precisao: 100% (atomicidade outbox + Debezium)
retencao: 30 dias em tópico Kafka; archive em datalake
compatibilidade: backward (consumidores leem v1 sem mudança ao surgir v1.1)
breaking_change_policy: novo tópico .v2; janela mínima de 90 dias antes de descontinuar .v1
```

### 3.5 Checklist de readiness operacional de um banco

- [ ] Monitoração: conexões ativas, locks, queries longas, replication lag, replication slot, bloat por tabela.
- [ ] Alerta: lag > X seg, slot > Y MB, conexões > Z%.
- [ ] Backup automático com PITR; restore testado mensalmente.
- [ ] Plan de capacity (crescimento por 6/12 meses).
- [ ] Documentação: ERD atualizado em `/arquitetura/diagramas/`.
- [ ] `pg_stat_statements` habilitado (top-N queries lentas).

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-data-engineer`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`.

O Data Engineer usa esta skill para:
- Revisar/escrever toda migração Flyway no pipeline do time.
- Modelar persistência junto com Tech Lead / Arquiteto App.
- Desenhar outbox/CDC junto com Arquiteto Sis.
- Documentar contratos de dataset publicado.
- Monitorar saúde do banco e propor capacity planning.

Outros papéis técnicos **consultam** o DataE em qualquer toque em schema, índice ou contrato de dado.

## References

Bibliografia da seção 3.7 do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Refactoring Databases* — Ambler & Sadalage
- *Designing Data-Intensive Applications* — Kleppmann
- *Database Reliability Engineering* — Campbell & Majors
- *The Data Warehouse Toolkit* (3ª ed.) — Kimball & Ross
- *SQL Antipatterns* (e ed. revisada) — Karwin
- *PostgreSQL: Up and Running* (3ª ed.) — Obe & Hsu
- *Streaming Systems* — Akidau, Chernyak & Lax
- *Designing Event-Driven Systems* — Stopford
- *Debezium Documentation* — Red Hat
- *Building Event-Driven Microservices* — Bellemare
- *Fundamentals of Data Engineering* — Reis & Housley
- *Data Mesh* — Dehghani *(quando aplicável)*
