# Agent Handoff Governance

## Overview

Use esta skill para padronizar tags, transicao de etapa, handoff tecnico e desvio operacional entre agents.

Regra transversal: leia `delivery-proof-contract.md`. Comentário, diagnóstico,
handoff textual ou commit apenas local não são entrega.

## Workflow

1. confirme a tag `agent:*` esperada para a etapa atual
2. nunca atribua a task a pessoas, bots ou fallbacks tecnicos; assignee nao faz parte do fluxo
3. agentes nao fecham tasks fora do rito de colunas; humanos controlam `closed` quando aplicavel
4. se a task estiver em `Ready` ou `Working` sem `agent:*`, a entrada padrao e `Developer`
5. fluxo tecnico padrao:
   - `Developer` implementa em `task-{id}` (de `master`), **merge em `dev`**, task em `Working`
   - `Developer` entrega; o Manager aplica handoff `agent:qa` + `agent:security` + `agent:design` + `agent:ux` (paralelo)
   - `QA` registra `agent:qa:accepted` ou `agent:qa:rejected`
   - `Security` registra `agent:security:accepted` ou `agent:security:rejected`
   - `Design` registra `agent:design:accepted` ou `agent:design:rejected`
   - `UX` registra `agent:ux:accepted` ou `agent:ux:rejected`
   - quando a task tiver o quarteto `agent:qa:accepted` + `agent:security:accepted` + `agent:design:accepted` + `agent:ux:accepted` e revalidacao do Manager, o `Manager` aciona o `DevOps`; o DevOps cria/congela RC de 1 a 5 tasks, promove exatamente o manifesto para `staging` e o Manager move somente as tasks inventariadas para **`In Review`**
   - humano move a task/RC homologada para **`Deploy`**; a mudança é a autorização explícita de publicação
   - item em **`Deploy`** publica a **mesma RC congelada** em `master`; com Security aceito move para **`Done`**, sem Security/evidencia move para **`Working`** para segunda rodada de validação
   - documentacao (`tutorial-assistant` / `technical-documenter`): no publish (fail-closed) aplicar labels de solicitacao ausentes; so os documentadores marcam `:done`
6. **Pulo de etapa ja concluida:** se o passo ja estiver feito (evidencia no GitHub), pule, avance e comente a justificativa. Security ainda registra aceite/recusa da propria etapa.
7. qualquer etapa pode abrir task paralela de infraestrutura com `agent:sysadmin`; nunca substitui a tarefa-mae
8. quando o `Sysadmin` concluir a paralela, comenta na mae e aplica o handoff cabivel
9. cada agent so troca a tag da propria proxima etapa quando sua etapa estiver concluida (ou pulada com evidencia)
10. RC e artefato tecnico obrigatorio para staging/In Review. Nao criar task pai `RC X.Y.Z-rc.N`; congele manifesto `rc/X.Y.Z-rc.N` e nunca inclua task depois do freeze sem `rc.N+1`.
11. nao faca handoff sem evidencia concreta
12. o handoff só é válido com mutação verificável: commit/ref remoto e merge
    para entrega de código, decisão de label para validação, ou merge + coluna
    para DevOps/board;
13. se a tentativa falhar após correção objetiva, nao aplique labels GitHub
    `agent:<papel>:blocked` nem mova a issue no GitHub Project #1 para `Blocked`;
    ambos sao estados humanos e a issue/board ficam somente-leitura para agents.
    Registre `NEXT_ACTION` com responsavel, tentativa e evidencia. Se a task de
    execucao Paperclip receber `status=blocked` pelo fluxo operacional, ela
    passa para a inbox Paperclip de recuperacao e deve ser priorizada pelo
    Manager/CTO; esse status nao bloqueia nem altera o item no GitHub.
14. não repita a mesma issue sem SHA/label/coluna/evidência novos.

## Gate obrigatorio de entrega local

Se o agent alterou qualquer arquivo, submodulo, gitlink ou configuracao local, o handoff so pode ser feito depois de entregar o trabalho e registrar evidencia verificavel. Nao e permitido deixar mudanca local solta, commit apenas local ou resultado dependente de um checkout que nao foi publicado.

Antes do handoff, o agent deve:

1. inventariar todos os projetos principais e submodulos afetados;
2. publicar cada mudanca no branch remoto previsto pelo fluxo (`task-{id}`, `dev`, `staging` ou `master` conforme o papel), incluindo primeiro o commit do submodulo e depois o gitlink do projeto pai;
3. confirmar, para cada projeto principal e submodulo afetado, o estado de `origin/master` com `git fetch` direcionado, `git rev-list --count origin/master..HEAD` e `git rev-list --count HEAD..origin/master`, alem de confirmar ausencia de alteracoes staged, unstaged ou untracked;
4. quando o checkout precisar permanecer em uma branch de task ou integracao para a proxima etapa, registrar branch, SHA, remote ref e motivo no handoff, sem tratar isso como alinhamento a `origin/master`;
5. bloquear o handoff e registrar a pendencia se qualquer alteracao local nao puder ser publicada ou se algum projeto/submodulo afetado nao puder ser comprovadamente verificado.

O handoff deve declarar separadamente: (a) o que foi publicado, (b) o estado de cada projeto principal e submodulo em relacao a `origin/master`, e (c) qualquer excecao de branch exigida pelo fluxo. `git status` isolado, commit local ou branch local nao sao evidencia de entrega.

## Output Contract

- tag operacional atual
- proxima tag / coluna
- evidencia do handoff, bloqueio ou pulo
- se houve devolucao, por que

O comentário de conclusão deve conter `DELIVERY_PROOF:` com a ação, refs/IDs e
estado pós-ação.

## Quality Bar

- nao retenha task na fila errada
- nao use assignee como ownership
- nao trate conflito de merge como detalhe
- nao mova tarefa por aproximacao textual
- nao crie task pai de RC nem altere RC congelada
- nao refaca passo ja evidenciado; documente o pulo
