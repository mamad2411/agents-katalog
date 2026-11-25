---
name: project-sdd-context
description: 'Use quando a tarefa estiver ancorada em um escopo de projeto dentro de project/ que já tenha 00-START-HERE.md, 01-WORKFLOW.md, spec, batches e validation checklist. Ajuda a operar SDD local sem tentar converter o repositório inteiro.'
user-invocable: false
---

# SDD local em projeto privado

Esta skill existe para frentes dentro de `project/` que já operam com artefatos de spec, batch, review, decision e validation, mesmo que o repositório inteiro não seja SDD.

## Quando usar

- tarefa ancorada em `project/<frente>/`
- leitura ou edição de spec, batch, review, decision, change request ou validation
- implementação de código que depende de batch ou checklist já existente naquela frente

## Procedimento

1. Confirme pelo [checklist de escopo local](./references/escopo-local.md) se aquela frente realmente opera em SDD.
2. Se a tarefa apontar para `project/<frente>/human-requests/*.md` ou para a pasta `human-requests/`, leia primeiro esse intake humano. Quando vier apenas a pasta, use `CURRENT.md`, depois `README.md`, depois o arquivo `.md` mais recente.
3. Releia `00-START-HERE.md`, `01-WORKFLOW.md`, a spec principal, `implementation/BATCH-INDEX.md` e `validation/VALIDATION-CHECKLIST.md` antes de propor código.
4. Trate `human-requests/` como entrada não normativa e `antigo/` apenas como insumo histórico, nunca como fonte atual de verdade.
5. Edite a spec principal somente quando requisito, aceite ou decisão estrutural mudar.
6. Use reviews, change-requests, decisions, implementation e validation para o restante do trabalho incremental.
7. Se a frente não tiver esses artefatos, volte ao fluxo normal do projeto privado e não tente retrofitar SDD para o repositório inteiro dentro da mesma tarefa.

## Saída esperada

- escopo local reconhecido corretamente
- batch atual e validação usados como âncora operacional
- nenhuma reescrita desnecessária da spec principal
- nenhum retrofit amplo de SDD fora da frente que já usa esse modelo