---
name: postgresql-optimization
description: "Workflow de otimização de banco de dados PostgreSQL para sintonia de consultas, estratégias de indexação, análise de desempenho e gerenciamento de banco de dados em produção."
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Workflow de Otimização PostgreSQL

## Visão Geral

Workflow especializado para otimização de banco de dados PostgreSQL incluindo sintonia de consultas, estratégias de indexação, análise de desempenho, gerenciamento de vacuum e administração de banco de dados em produção.

## Quando Usar Este Workflow

Use este workflow quando:
- Otimizar consultas PostgreSQL lentas
- Projetar estratégias de indexação
- Analisar desempenho do banco de dados
- Ajustar configuração do PostgreSQL
- Gerenciar bancos de dados em produção

## Fases do Workflow

### Fase 1: Avaliação de Desempenho

#### Skills a Invocar
- `database-optimizer` - Otimização de banco de dados
- `postgres-best-practices` - Melhores práticas PostgreSQL

#### Ações
1. Verificar versão do banco de dados
2. Revisar configuração
3. Analisar consultas lentas
4. Verificar uso de recursos
5. Identificar gargalos

#### Prompts Prontos para Copiar
```
Use @database-optimizer to assess PostgreSQL performance
```

### Fase 2: Análise de Consultas

#### Skills a Invocar
- `sql-optimization-patterns` - Otimização SQL
- `postgres-best-practices` - Padrões PostgreSQL

#### Ações
1. Executar EXPLAIN ANALYZE
2. Identificar tipos de scan
3. Verificar estratégias de join
4. Analisar tempo de execução
5. Encontrar oportunidades de otimização

#### Prompts Prontos para Copiar
```
Use @sql-optimization-patterns to analyze and optimize queries
```

### Fase 3: Estratégia de Indexação

#### Skills a Invocar
- `database-design` - Design de índices
- `postgresql` - Indexação PostgreSQL

#### Ações
1. Identificar índices ausentes
2. Criar índices B-tree
3. Adicionar índices compostos
4. Considerar índices parciais
5. Revisar uso de índices

#### Prompts Prontos para Copiar
```
Use @database-design to design PostgreSQL indexing strategy
```

### Fase 4: Otimização de Consultas

#### Skills a Invocar
- `sql-optimization-patterns` - Sintonia de consultas
- `sql-pro` - Expertise SQL

#### Ações
1. Reescrever consultas ineficientes
2. Otimizar joins
3. Adicionar CTEs quando útil
4. Implementar paginação
5. Testar melhorias

#### Prompts Prontos para Copiar
```
Use @sql-optimization-patterns to optimize SQL queries
```

### Fase 5: Sintonia de Configuração

#### Skills a Invocar
- `postgres-best-practices` - Configuração
- `database-admin` - Administração de banco de dados

#### Ações
1. Ajustar shared_buffers
2. Configurar work_mem
3. Definir effective_cache_size
4. Ajustar configurações de checkpoint
5. Configurar autovacuum

#### Prompts Prontos para Copiar
```
Use @postgres-best-practices to tune PostgreSQL configuration
```

### Fase 6: Manutenção

#### Skills a Invocar
- `database-admin` - Manutenção de banco de dados
- `postgresql` - Manutenção PostgreSQL

#### Ações
1. Agendar VACUUM
2. Executar ANALYZE
3. Verificar inchaço de tabela
4. Monitorar autovacuum
5. Revisar estatísticas

#### Prompts Prontos para Copiar
```
Use @database-admin to schedule PostgreSQL maintenance
```

### Fase 7: Monitoramento

#### Skills a Invocar
- `grafana-dashboards` - Dashboards de monitoramento
- `prometheus-configuration` - Coleta de métricas

#### Ações
1. Configurar monitoramento
2. Criar dashboards
3. Configurar alertas
4. Rastrear métricas-chave
5. Revisar tendências

#### Prompts Prontos para Copiar
```
Use @grafana-dashboards to create PostgreSQL monitoring
```

## Checklist de Otimização

- [ ] Consultas lentas identificadas
- [ ] Índices otimizados
- [ ] Configuração ajustada
- [ ] Manutenção agendada
- [ ] Monitoramento ativo
- [ ] Desempenho melhorado

## Critérios de Qualidade

- [ ] Desempenho de consultas melhorado
- [ ] Índices eficazes
- [ ] Configuração otimizada
- [ ] Manutenção automatizada
- [ ] Monitoramento em funcionamento

## Bundles de Workflow Relacionados

- `database` - Operações de banco de dados
- `cloud-devops` - Infraestrutura
- `performance-optimization` - Otimização de desempenho