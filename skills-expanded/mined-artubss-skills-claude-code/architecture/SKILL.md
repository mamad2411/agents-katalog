---
name: architecture
description: Framework de tomada de decisão arquitetural. Análise de requisitos, avaliação de trade-offs, documentação de ADR. Use ao tomar decisões de arquitetura ou analisar design de sistemas.
allowed-tools: Read, Glob, Grep
---

# Framework de Decisão Arquitetural

> "Requisitos direcionam arquitetura. Trade-offs informam decisões. ADRs capturam a lógica."

## 🎯 Regra de Leitura Seletiva

**Leia APENAS arquivos relevantes para a solicitação!** Verifique o mapa de conteúdo, encontre o que você precisa.

| Arquivo | Descrição | Quando Ler |
|---------|-----------|-----------|
| `context-discovery.md` | Perguntas a fazer, classificação do projeto | Iniciando design arquitetural |
| `trade-off-analysis.md` | Templates de ADR, framework de trade-off | Documentando decisões |
| `pattern-selection.md` | Árvores de decisão, anti-padrões | Escolhendo padrões |
| `examples.md` | Exemplos de MVP, SaaS, Enterprise | Implementações de referência |
| `patterns-reference.md` | Lookup rápido de padrões | Comparação de padrões |

---

## 🔗 Skills Relacionadas

| Skill | Use Para |
|-------|---------|
| `@[skills/database-design]` | Design de schema de banco de dados |
| `@[skills/api-patterns]` | Padrões de design de API |
| `@[skills/deployment-procedures]` | Arquitetura de deployment |

---

## Princípio Principal

**"Simplicidade é a sofisticação máxima."**

- Comece simples
- Adicione complexidade APENAS quando comprovado necessário
- Você sempre pode adicionar padrões depois
- Remover complexidade é MUITO mais difícil que adicioná-la

---

## Checklist de Validação

Antes de finalizar a arquitetura:

- [ ] Requisitos claramente compreendidos
- [ ] Restrições identificadas
- [ ] Cada decisão tem análise de trade-off
- [ ] Alternativas mais simples consideradas
- [ ] ADRs escritas para decisões significativas
- [ ] Expertise do time alinhada com padrões escolhidos