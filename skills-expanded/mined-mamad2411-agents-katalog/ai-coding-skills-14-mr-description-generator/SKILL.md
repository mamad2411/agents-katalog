---
description: Gera descrições padronizadas de Merge Request (MR/PR) no GitLab a partir de diffs, commits ou texto explicativo.
globs: ["**/*"]
alwaysApply: false
---

# GitLab Merge Request Description Generator (.cursorrules)

Gera descrições de MR de alto padrão técnico para revisão no GitLab ou GitHub.

## 🛑 Diretrizes Obrigatórias
1. **Sempre pergunte o contexto se faltar o ticket**: Se o usuário não mencionar a issue/ticket Jira/GitLab, inclua `[PREENCHER: Ticket ID]`.
2. **Divida em seções claras**: Contexto & Motivação, O Que Foi Feito, Como Testar, Riscos & Rollback, Checklist.
3. **Seja específico nos testes**: Forneça comandos (`curl`, scripts, chamadas de fila ou comandos gradle/maven) para validação.
4. **Alinhe com tags de deploy**: Lembre o desenvolvedor se o commit final precisa das tags `#deployuat #auto`.

## 📋 Formato de Saída (Markdown)
Gere sempre o bloco markdown pronto para ser copiado e colado na descrição do MR no GitLab:

```markdown
## 🎯 Contexto e Motivação
- **Issue/Ticket:** [ID-DO-CARD]
- **Tipo:** [Feature | Bugfix | Refactor | Performance | Infra]
- **Resumo:** [Explicação direta do objetivo]

---

## 🛠️ O que foi feito?
- [Módulo/Camada]: [Descrição técnica precisa da mudança]

---

## 🧪 Como Testar / Evidências
1. [Passo a passo com curl ou payloads de teste]
- [ ] Testes unitários executados
- [ ] Testes de integração validados

---

## ⚠️ Avaliação de Risco & Rollback
- **Risco:** [Baixo | Médio | Alto]
- **Breaking Change:** [Sim | Não]
- **Plano de Rollback:** [Estratégia de reversão]

---

## 🚢 Checklist Pré-Merge
- [ ] Padrões de código e lint validados
- [ ] Sem secrets ou variáveis sensíveis expostas
- [ ] Deploy UAT planejado (#deployuat #auto)
```
