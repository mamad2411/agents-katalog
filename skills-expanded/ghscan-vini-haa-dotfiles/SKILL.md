---
name: review-deep
description: Code review paralelo com múltiplos agentes especializados.
argument-hint: "[arquivo ou diretório]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent
model: opus
effort: high
context: fork
---

# Review Deep — Code Review Paralelo Multi-Agente

Review profundo com 4 revisores paralelos: `$ARGUMENTS`

## Escopo

### Se argumento fornecido
Revisar: `$ARGUMENTS`

### Se nenhum argumento
```bash
git diff --name-only HEAD
git diff --cached --name-only
```

## Processo

### Fase 1 — Preparação
1. Identificar arquivos a revisar
2. Ler cada arquivo para entender contexto
3. Montar briefing: arquivos, propósito, stack

### Fase 2 — Dispatch paralelo (4 agentes)

Despachar TODOS em paralelo:

#### Revisor 1 — Code Quality (backend/frontend)
- Correção lógica, edge cases, tipos
- Legibilidade, naming, SRP, dead code
- Padrões do projeto

#### Revisor 2 — Security (security)
- OWASP Top 10, input validation, injection
- Secrets, auth, headers, deps vulneráveis

#### Revisor 3 — Test Quality (backend/frontend)
- Cobertura: happy path + edge cases
- Nomes descritivos, AAA, mocks vs integração

#### Revisor 4 — Consequences (architect)
- Impacto em dependentes
- Breaking changes não documentados
- Efeitos cascata, compatibilidade

### Fase 3 — Consolidação
1. Coletar findings dos 4 revisores
2. Remover duplicatas
3. Marcar conflitos: "⚠️ Conflito" se revisores discordam
4. Classificar por severidade

### Fase 4 — Relatório

```
## Review Deep — Relatório Consolidado

### Revisores
| Revisor | Findings | Críticos | Importantes |
|---------|----------|----------|-------------|

### 🔴 Crítico (bloqueia merge)
- **[Revisor]** [arquivo:linha] Descrição
  - Impacto: [...]
  - Fix: [...]

### 🟡 Importante (deve corrigir)
### 🔵 Sugestão

### ⚠️ Conflitos entre revisores
- [Revisor A] diz X vs [Revisor B] diz Y

### ✅ Pontos positivos

## Veredicto: PASS | FAIL | NEEDS DISCUSSION
**Confiança: X/5**
```

## Quando usar
- `/review` = 1 pass sequencial, rápido, mudanças pequenas
- `/review-deep` = 4 agentes paralelos, PRs grandes ou críticos
