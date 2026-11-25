# Operational GitHub Workflow

## Overview

Use esta skill quando houver correcao direta de codigo que precise seguir o fluxo operacional padrao de hotfix.

## Workflow

1. crie um branch de hotfix a partir de `master`
2. registre explicitamente a correcao como hotfix
3. execute a correcao nesse branch
4. depois da correcao, propague a alteracao para `staging` e `dev`
5. registre quais branches foram atualizados e o que ainda depende de validacao manual
6. se a correcao exigir acompanhamento manual posterior, crie ou atualize a issue correspondente no GitHub
7. quando houver runner, wrapper ou script oficial do papel atual, use essa trilha para executar ou validar a mudanca sempre que isso for viavel
8. se a mutacao no GitHub depender de coluna, label, comentario, review, assignee ou outra escrita que o runtime local nao consiga concluir com confianca, prefira o `GitHub Operations Runner` em `workers/automate/github-operations.md`
9. se nao houver conector de escrita, sessao autenticada ou outra superficie viavel para concluir a mudanca no GitHub, o agent pode usar a chave do GitHub anexada a sessao como fallback operacional
10. ao usar esse fallback, injete a chave apenas no tempo da execucao, nunca replique o valor em arquivo versionado, issue, comentario, log ou resposta visivel

## GitHub Follow-through

Quando a correcao de codigo precisar de acompanhamento manual posterior:

- crie ou atualize a issue de acompanhamento
- coloque essa issue na coluna `In Review`
- registre o que foi corrigido, qual branch de hotfix foi criado e o que precisa ser validado manualmente
- mantenha apenas contexto nao sensivel
- se ja existir issue para o mesmo assunto, atualize ou referencie em vez de duplicar

Quando a correcao de codigo tambem precisar entrar no fluxo normal de trabalho tecnico:

- mantenha o acompanhamento tecnico principal na coluna `Ready` por meio da skill de manipulacao de issues do GitHub
- use `In Review` especificamente para a etapa de validacao manual posterior

## Quality Bar

- nao pule a criacao do branch de hotfix a partir de `master`
- nao pule a propagacao para `staging` e `dev`
- nao trate validacao manual como opcional quando ela for necessaria
- nao exponha informacoes sensiveis em issues, comentarios ou resumos
- nao ignore a chave anexada quando ela for o unico caminho operacional restante para concluir a mudanca autorizada
