---
name: supabase-postgres-best-practices
description: Otimização de performance do Postgres e boas práticas da Supabase. Use essa skill ao escrever, revisar ou otimizar queries Postgres, designs de schema ou configurações de banco de dados.
license: MIT
metadata:
  author: supabase
  version: "1.0.0"
---

# Supabase Postgres Best Practices

Guia abrangente de otimização de performance para Postgres, mantido pela Supabase. Contém regras em 8 categorias, priorizadas por impacto para orientar otimização de queries e design de schema automatizados.

## Quando Aplicar

Consulte essas diretrizes quando:
- Escrever queries SQL ou projetar schemas
- Implementar índices ou otimização de queries
- Revisar problemas de performance do banco de dados
- Configurar connection pooling ou scaling
- Otimizar para recursos específicos do Postgres
- Trabalhar com Row-Level Security (RLS)

## Categorias de Regras por Prioridade

| Prioridade | Categoria | Impacto | Prefixo |
|----------|----------|--------|--------|
| 1 | Query Performance | CRÍTICO | `query-` |
| 2 | Connection Management | CRÍTICO | `conn-` |
| 3 | Security & RLS | CRÍTICO | `security-` |
| 4 | Schema Design | ALTO | `schema-` |
| 5 | Concurrency & Locking | MÉDIO-ALTO | `lock-` |
| 6 | Data Access Patterns | MÉDIO | `data-` |
| 7 | Monitoring & Diagnostics | BAIXO-MÉDIO | `monitor-` |
| 8 | Advanced Features | BAIXO | `advanced-` |

## Como Usar

Leia arquivos de regras individuais para explicações detalhadas e exemplos SQL:

```
rules/query-missing-indexes.md
rules/schema-partial-indexes.md
rules/_sections.md
```

Cada arquivo de regra contém:
- Explicação breve do por que é importante
- Exemplo de SQL incorreto com explicação
- Exemplo de SQL correto com explicação
- Output de EXPLAIN opcional ou métricas
- Contexto adicional e referências
- Notas específicas da Supabase (quando aplicável)

## Documento Compilado Completo

Para o guia completo com todas as regras expandidas: `AGENTS.md`