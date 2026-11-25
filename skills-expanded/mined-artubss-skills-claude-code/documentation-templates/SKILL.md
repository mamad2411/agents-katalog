---
name: documentation-templates
description: Templates e diretrizes de estrutura para documentação. README, docs de API, comentários em código e documentação amigável para IA.
allowed-tools: Read, Glob, Grep
---

# Modelos de Documentação

> Templates e diretrizes de estrutura para tipos comuns de documentação.

---

## 1. Estrutura de README

### Seções Essenciais (Ordem de Prioridade)

| Seção | Propósito |
|---------|---------|
| **Título + Descrição** | O que é isso? |
| **Quick Start** | Execução em <5 min |
| **Recursos** | O que posso fazer? |
| **Configuração** | Como personalizar |
| **Referência de API** | Link para docs detalhados |
| **Contribuindo** | Como ajudar |
| **Licença** | Legal |

### Template de README

```markdown
# Nome do Projeto

Breve descrição em uma linha.

## Quick Start

[Passos mínimos para executar]

## Recursos

- Recurso 1
- Recurso 2

## Configuração

| Variável | Descrição | Padrão |
|----------|-------------|---------|
| PORT | Porta do servidor | 3000 |

## Documentação

- [Referência de API](./docs/api.md)
- [Arquitetura](./docs/architecture.md)

## Licença

MIT
```

---

## 2. Estrutura de Documentação de API

### Template por Endpoint

```markdown
## GET /users/:id

Obtém um usuário por ID.

**Parâmetros:**
| Nome | Tipo | Obrigatório | Descrição |
|------|------|----------|-------------|
| id | string | Sim | ID do usuário |

**Resposta:**
- 200: Objeto de usuário
- 404: Usuário não encontrado

**Exemplo:**
[Exemplo de requisição e resposta]
```

---

## 3. Diretrizes de Comentários em Código

### Template JSDoc/TSDoc

```typescript
/**
 * Breve descrição do que a função faz.
 * 
 * @param paramName - Descrição do parâmetro
 * @returns Descrição do valor retornado
 * @throws ErrorType - Quando esse erro ocorre
 * 
 * @example
 * const result = functionName(input);
 */
```

### Quando Comentar

| ✅ Comente | ❌ Não Comente |
|-----------|-----------------|
| Por quê (lógica de negócio) | O quê (óbvio) |
| Algoritmos complexos | Toda linha |
| Comportamento não óbvio | Código auto-explicativo |
| Contratos de API | Detalhes de implementação |

---

## 4. Template de Changelog (Keep a Changelog)

```markdown
# Changelog

## [Unreleased]
### Added
- Novo recurso

## [1.0.0] - 2025-01-01
### Added
- Lançamento inicial
### Changed
- Dependência atualizada
### Fixed
- Correção de bug
```

---

## 5. Registro de Decisão de Arquitetura (ADR)

```markdown
# ADR-001: [Título]

## Status
Aceito / Descontinuado / Supersedido

## Contexto
Por que estamos tomando essa decisão?

## Decisão
O que decidimos?

## Consequências
Quais são os trade-offs?
```

---

## 6. Documentação Amigável para IA (2025)

### Template llms.txt

Para crawlers e agentes de IA:

```markdown
# Nome do Projeto
> Objetivo em uma linha.

## Arquivos Principais
- [src/index.ts]: Entrada principal
- [src/api/]: Rotas de API
- [docs/]: Documentação

## Conceitos-Chave
- Conceito 1: Breve explicação
- Conceito 2: Breve explicação
```

### Documentação Preparada para MCP

Para indexação RAG:
- Hierarquia clara de H1-H3
- Exemplos JSON/YAML para estruturas de dados
- Diagramas Mermaid para fluxos
- Seções auto-contidas

---

## 7. Princípios de Estrutura

| Princípio | Por quê |
|-----------|-----|
| **Escaneável** | Títulos, listas, tabelas |
| **Exemplos em primeiro lugar** | Mostrar, não apenas contar |
| **Detalhe progressivo** | Simples → Complexo |
| **Atualizado** | Desatualizado = enganoso |

---

> **Lembre-se:** Templates são pontos de partida. Adapte às necessidades do seu projeto.