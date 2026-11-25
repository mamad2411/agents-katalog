---
name: api-patterns
description: Princípios de design de API e tomada de decisão. Seleção REST vs GraphQL vs tRPC, formatos de resposta, versionamento, paginação.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Padrões de API

> Princípios de design de API e tomada de decisão para 2025.
> **Aprenda a PENSAR, não copie padrões fixos.**

## 🎯 Regra de Leitura Seletiva

**Leia APENAS os arquivos relevantes para a solicitação!** Verifique o mapa de conteúdo, encontre o que você precisa.

---

## 📑 Mapa de Conteúdo

| Arquivo | Descrição | Quando Ler |
|---------|-----------|-----------|
| `api-style.md` | Árvore de decisão REST vs GraphQL vs tRPC | Escolhendo tipo de API |
| `rest.md` | Nomenclatura de recursos, métodos HTTP, códigos de status | Projetando API REST |
| `response.md` | Padrão envelope, formato de erro, paginação | Estrutura de resposta |
| `graphql.md` | Design de schema, quando usar, segurança | Considerando GraphQL |
| `trpc.md` | Monorepo TypeScript, segurança de tipo | Projetos fullstack TS |
| `versioning.md` | Versionamento por URI/Header/Query | Planejamento de evolução de API |
| `auth.md` | JWT, OAuth, Passkey, API Keys | Seleção de padrão de autenticação |
| `rate-limiting.md` | Token bucket, janela deslizante | Proteção de API |
| `documentation.md` | Melhores práticas OpenAPI/Swagger | Documentação |
| `security-testing.md` | OWASP API Top 10, testes de autenticação/autorização | Auditorias de segurança |

---

## 🔗 Habilidades Relacionadas

| Necessidade | Habilidade |
|------------|-----------|
| Implementação de API | `@[skills/backend-development]` |
| Estrutura de dados | `@[skills/database-design]` |
| Detalhes de segurança | `@[skills/security-hardening]` |

---

## ✅ Checklist de Decisão

Antes de projetar uma API:

- [ ] **Perguntou ao usuário sobre os consumidores da API?**
- [ ] **Escolheu o estilo de API para ESTE contexto?** (REST/GraphQL/tRPC)
- [ ] **Definiu formato de resposta consistente?**
- [ ] **Planejou estratégia de versionamento?**
- [ ] **Considerou necessidades de autenticação?**
- [ ] **Planejou rate limiting?**
- [ ] **Abordagem de documentação definida?**

---

## ❌ Anti-Padrões

**NÃO FAÇA:**
- Use REST por padrão para tudo
- Use verbos em endpoints REST (/getUsers)
- Retorne formatos de resposta inconsistentes
- Exponha erros internos aos clientes
- Pule rate limiting

**FAÇA:**
- Escolha o estilo de API baseado no contexto
- Pergunte sobre os requisitos do cliente
- Documente minuciosamente
- Use códigos de status apropriados

---

## Script

| Script | Propósito | Comando |
|--------|----------|---------|
| `scripts/api_validator.py` | Validação de endpoint de API | `python scripts/api_validator.py <project_path>` |