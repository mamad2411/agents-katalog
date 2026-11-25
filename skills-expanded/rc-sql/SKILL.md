---
name: rc-sql
description: "Relational query and schema work — indexes, EXPLAIN, N+1, modeling. Read-only by default. Use when reviewing SQL. Not for infra admin."
model: sonnet
effort: medium
---

# Banco de dados (SQL) — guias por tarefa

Guias práticos de SQL. Leia o guia da tarefa em `references/` antes de agir — cada um traz
o checklist, os comandos de verificação e os critérios de aceite. Sempre leia o schema e os
índices reais (via `\d`, `information_schema` ou o DDL do repo) antes de recomendar qualquer
mudança; não presuma a estrutura. Os exemplos usam PostgreSQL, mas os princípios valem para
qualquer banco relacional.

## Roteamento

| Tarefa | Guia |
| ------ | ---- |
| Otimização de queries (EXPLAIN, índices, N+1, paginação) | `references/query-optimization.md` |
| Design de schema (normalização, tipos, constraints, chaves) | `references/schema-design.md` |
| Segurança e execução (transações, locks, migrations, produção) | `references/safety.md` |

## Princípios sempre válidos

- **Meça com EXPLAIN antes de otimizar — não adivinhe.** Nenhum ajuste de índice ou query se justifica sem o plano de execução real na frente.
- **O índice certo bate a query esperta.** Antes de reescrever uma query complexa, verifique se falta um índice.
- **Read-only por padrão (Rule 9).** Para análise, só `SELECT`/`EXPLAIN`; escrita e DDL vão no relatório como recomendação, para o usuário executar ou autorizar. O hook `db-guard` bloqueia escrita via `psql`/`mysql`/`sqlite3` no Bash — é rede de segurança, não a regra: acesso via MCP passa por fora dele.
- **O schema é o alicerce.** Corrija o schema antes de contornar sua falha em código (validação duplicada, joins gambiarra, etc.).

## Error Handling

- Sem acesso ao banco: analise o schema/DDL e as queries do repositório estaticamente e diga explicitamente que o `EXPLAIN` real e a verificação de índices ficaram pendentes.
