---
name: database-design
description: Princípios de design de banco de dados e tomada de decisão. Design de schema, estratégia de indexação, seleção de ORM, bancos de dados serverless.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Design de Banco de Dados

> **Aprenda a PENSAR, não copiar padrões SQL.**

## 🎯 Regra de Leitura Seletiva

**Leia APENAS arquivos relevantes para a solicitação!** Verifique o mapa de conteúdo, encontre o que você precisa.

| Arquivo | Descrição | Quando Ler |
|---------|-----------|-----------|
| `database-selection.md` | PostgreSQL vs Neon vs Turso vs SQLite | Escolhendo banco de dados |
| `orm-selection.md` | Drizzle vs Prisma vs Kysely | Escolhendo ORM |
| `schema-design.md` | Normalização, chaves primárias, relacionamentos | Projetando schema |
| `indexing.md` | Tipos de índice, índices compostos | Otimização de performance |
| `optimization.md` | N+1, EXPLAIN ANALYZE | Otimização de query |
| `migrations.md` | Migrações seguras, bancos serverless | Alterações de schema |

---

## ⚠️ Princípio Central

- PERGUNTE ao usuário sobre preferências de banco de dados quando for incerto
- Escolha banco de dados/ORM baseado no CONTEXTO
- Não use PostgreSQL como padrão para tudo

---

## Lista de Verificação de Decisão

Antes de projetar o schema:

- [ ] Perguntou ao usuário sobre a preferência de banco de dados?
- [ ] Escolheu banco de dados para ESTE contexto?
- [ ] Considerou o ambiente de deploy?
- [ ] Planejou estratégia de indexação?
- [ ] Definiu tipos de relacionamento?

---

## Anti-Padrões

❌ Usar PostgreSQL por padrão em apps simples (SQLite pode ser suficiente)
❌ Pular indexação
❌ Usar SELECT * em produção
❌ Armazenar JSON quando dados estruturados são melhores
❌ Ignorar queries N+1