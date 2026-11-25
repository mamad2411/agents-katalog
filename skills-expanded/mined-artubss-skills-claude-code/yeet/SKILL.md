---
name: "yeet"
description: "Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`)."
author: openai
---

## Pré-requisitos

- Requer GitHub CLI `gh`. Verifique com `gh --version`. Se não estiver instalado, peça ao usuário para instalar `gh` e pare.
- Requer sessão `gh` autenticada. Execute `gh auth status`. Se não estiver autenticado, peça ao usuário para executar `gh auth login` (e re-executar `gh auth status`) antes de continuar.

## Convenções de nomenclatura

- Branch: `codex/{description}` ao iniciar a partir de main/master/default.
- Commit: `{description}` (conciso).
- Título da PR: `[codex] {description}` resumindo o diff completo.

## Fluxo de trabalho

- Se estiver em main/master/default, crie uma branch: `git checkout -b "codex/{description}"`
- Caso contrário, permaneça na branch atual.
- Confirme o status, depois faça stage de tudo: `git status -sb` depois `git add -A`.
- Commit com descrição concisa: `git commit -m "{description}"`
- Execute verificações se ainda não tiver feito. Se as verificações falharem por falta de dependências/ferramentas, instale as dependências e execute novamente uma única vez.
- Faça push com rastreamento: `git push -u origin $(git branch --show-current)`
- Se git push falhar devido a erros de autenticação de workflow, faça pull de master e tente o push novamente.
- Abra uma PR e edite o título/corpo para refletir a descrição e as mudanças: `GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head $(git branch --show-current)`
- Escreva a descrição da PR em um arquivo temporário com quebras de linha reais (ex: pr-body.md ... EOF) e execute pr-body.md para evitar markdown com \\n escapados.
- A descrição da PR (markdown) deve ser uma prosa detalhada cobrindo o problema, a causa e o efeito para os usuários, a causa raiz, a correção e qualquer teste ou verificação usado para validar.