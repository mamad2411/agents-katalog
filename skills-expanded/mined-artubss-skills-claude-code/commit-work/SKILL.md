---
name: commit-work
description: "Criar commits git de alta qualidade: revisar/preparar mudanças pretendidas, dividir em commits lógicos e escrever mensagens de commit claras (incluindo Conventional Commits). Use quando o usuário pedir para fazer commit, elaborar uma mensagem de commit, preparar mudanças ou dividir o trabalho em múltiplos commits."
---

# Fazer commit do trabalho

## Objetivo
Fazer commits que sejam fáceis de revisar e seguros para enviar:
- apenas as mudanças pretendidas estão incluídas
- commits têm escopo lógico (dividir quando necessário)
- mensagens de commit descrevem o que mudou e por quê

## Entradas a solicitar (se faltarem)
- Um único commit ou múltiplos commits? (Se em dúvida: padrão é múltiplos commits pequenos quando há mudanças não relacionadas.)
- Estilo de commit: Conventional Commits são obrigatórios.
- Qualquer regra: comprimento máximo do subject, escopos obrigatórios.

## Workflow (checklist)
1) Inspecionar a árvore de trabalho antes de preparar
   - `git status`
   - `git diff` (não preparado)
   - Se muitas mudanças: `git diff --stat`
2) Decidir limites de commits (dividir se necessário)
   - Dividir por: feature vs refactor, backend vs frontend, formatação vs lógica, testes vs código de produção, atualizações de dependências vs mudanças de comportamento.
   - Se mudanças estão misturadas em um arquivo, planejar usar patch staging.
3) Preparar apenas o que pertence ao próximo commit
   - Preferir patch staging para mudanças misturadas: `git add -p`
   - Para descartar hunk/arquivo: `git restore --staged -p` ou `git restore --staged <path>`
4) Revisar o que será realmente commitado
   - `git diff --cached`
   - Verificações de sanidade:
     - sem segredos ou tokens
     - sem logging de debug acidental
     - sem mudanças de formatação não relacionadas
5) Descrever a mudança preparada em 1-2 frases (antes de escrever a mensagem)
   - "O que mudou?" + "Por quê?"
   - Se você não conseguir descrever isso de forma clara, o commit é provavelmente muito grande ou misturado; voltar ao passo 2.
6) Escrever a mensagem de commit
   - Usar Conventional Commits (obrigatório):
     - `tipo(escopo): resumo breve`
     - linha em branco
     - corpo (o quê/por quê, não diário de implementação)
     - rodapé (BREAKING CHANGE) se necessário
   - Preferir um editor para mensagens multi-linha: `git commit -v`
   - Usar `references/commit-message-template.md` se útil.
7) Executar a verificação relevante mais pequena
   - Executar a verificação mais rápida e significativa do repositório (testes unitários, lint ou build) antes de prosseguir.
8) Repetir para o próximo commit até a árvore de trabalho estar limpa

## Entregável
Fornecer:
- a(s) mensagem(ns) de commit final(ais)
- um breve resumo por commit (o quê/por quê)
- os comandos usados para preparar/revisar (no mínimo: `git diff --cached`, mais testes executados)