# Issue Queue Discovery

Skill compartilhada pelos agents documentais (`technical-documenter`, `tutorial-assistant`), de revisao (`qa`, `security`), `sysadmin` (modo `resolve`) e reutilizavel por outros papeis que precisem da mesma fila.

## Objetivo

Esta skill define o protocolo de descoberta e captura na fila para quando o prompt **não informar** qual tarefa deve ser executada.

- **Regra primordial:** se o prompt informar a tarefa a ser executada (`owner/repo#issue`, link, número ou escopo direto), o agent deve trabalhar **diretamente nessa tarefa** (validando a elegibilidade do papel), **sem buscar prioridade na fila**.
- **Apenas se o prompt NÃO tiver informado qual a tarefa a ser executada:** o agent deve buscar e selecionar a próxima prioridade na fila seguindo as regras abaixo.
- A fonte primaria da fila sao **issues + labels** (e estado open/closed).
- **QA e Security:** quando buscando na fila, podem selecionar e processar **varias** issues elegiveis na mesma execucao/rodada (cada uma com decisao e comentario completos).
- **Demais papeis** (Developer, DevOps, Manager board, Documentacao, etc.): selecionar **exatamente uma** issue elegivel por execucao quando buscando na fila, salvo prompt ou fonte canonica do papel que ordene o contrario.

## ProjectV2

- **Nao e proibido** usar GitHub Projects (ProjectV2).
- **Prefira nao usar** ProjectV2 quando labels e busca de issues bastarem (fila, elegibilidade, handoff).
- Use ProjectV2 quando for preciso: associar issue recem-criada ao board, ler status/coluna complementar, ou quando o prompt pedir explicitamente.
- Projeto operacional padrao da org: [ControleOnline Project #1](https://github.com/orgs/ControleOnline/projects/1/views/1) (`organization` `ControleOnline`, `number` `1`).

## Associacao obrigatoria ao Project #1 (hands-on — todos os agents)

**Regra transversal e hands-on:** todo agent do ecossistema (CTO, Developer, Manager, QA, Security, DevOps, Sysadmin, documentadores e qualquer outro papel) e **obrigado** a manter **issues e PRs** no **Project #1**. Tudo e Project #1. Nao e opcional, nao e so do Manager e nao pode ser adiado para “depois”.

Sempre que um agent **criar** uma issue/task **ou** abrir/atuar em uma PR:

1. Crie a issue no repositorio adequado (ou identifique a PR).
2. **Associe-a imediatamente** ao projeto `https://github.com/orgs/ControleOnline/projects/1/views/1` (ProjectV2 da org, number `1`) — **na mesma hora**.
3. Defina o Status do item no board (`Ready` na entrada padrao, ou a coluna coerente com o estado real se ja houver ownership/etapa).
4. Aplique as labels `agent:*` necessarias.
5. **Label de página:** se a criação for a partir de erro/relato com URL ou tela identificável, aplique na mesma hora a label com o slug da página (ex.: `client-details`). Detalhe canônico: `agents/skills/controleonline/shared-github-github-issue-handling/SKILL.md` e `agents/skills/controleonline/by-role-cto-github-backlog-task-creation/SKILL.md`.

Regras adicionais (todos os agents):

- Issue ou PR **sem** item no Project #1 e desvio operacional: o agent que a criar, capturar ou mutar deve **associar na mesma rodada/hora**.
- **Todas** as PRs `open` do escopo entram nessa regra (nao so as “ja no board”).
- Falha de permissao/API ao associar **nao e silenciosa**: comente no item a falha objetiva e tente de novo quando houver permissao; nao deixe solto sem tentativa registrada.
- Manager em P6 (higiene) audita e corrige itens soltos, mas isso **nao dispensa** a obrigacao hands-on dos demais agents.

## Outras regras

- Nao processe mais de uma issue na mesma execucao **exceto QA e Security** (e salvo prompt ou fonte canonica do papel que ordene o contrario).
- O agent pode **criar labels** oficiais ausentes no repositorio (incluindo labels de página no formato kebab-case do path).


## Filtro obrigatorio de coluna GitHub (fail-closed)

Antes de qualquer candidata:

1. Leia o Status no GitHub Project #1.
2. Se for **`Blocked`** ou **`Backlog`**: descarte a issue GitHub. Nao comente, nao mova, nao valide, nao documente.
3. RC/Deploy so considera **In Review** / **Deploy** / **Done** conforme o rito. Nunca varre Blocked/Backlog.

## Proibicao: Blocked e Backlog

Issues GitHub com Status no Project #1 **`Blocked`** ou **`Backlog`** **nao sao candidatas** em nenhum template de elegibilidade (Developer, QA, Security, DevOps, documentacao, Manager). Esta regra nao descreve a inbox nem o status de tasks no Paperclip.

- Filtro obrigatorio antes de selecionar: se a coluna for `Blocked` ou `Backlog`, **descarte**.
- Nao mover item para fora de `Blocked`/`Backlog` sem ordem humana explicita na issue.
- Nao usar `Backlog` como fila de recuperacao automatica.

## Fila de recuperacao Paperclip

O status `blocked` de uma task Paperclip e independente da coluna GitHub
`Blocked`. Para o Manager/CTO, a inbox Paperclip `/CON/inbox/blocked` e fila de
recuperacao prioritária: diagnostique e retome/corrija tasks e execucoes
Paperclip antes de capturar novo trabalho, com readback após cada mutacao.
Recuperar a task Paperclip nao autoriza qualquer mutacao na issue GitHub que
esteja na coluna `Blocked`; nesse caso, limite a acao a recuperacao operacional
Paperclip e aguarde a decisao humana sobre o board GitHub.

## Ownership de colunas por trilha

As colunas **`Ready`** e **`Working`** formam a fila operacional compartilhada
dos agents. Todos priorizam `Working` antes de `Ready`, respeitando o limite
atual lido no Project #1. O `DevOps` tem uma excecao de ordem: consulta
**`Deploy`** primeiro e, depois, `Working`.

Para todos os agentes, leia no Project #1 o limite configurado para a coluna
`Working` antes de capturar trabalho; neste ecossistema, esse limite é **5**.
Consulte primeiro as tasks em
`Working`; enquanto houver capacidade abaixo do limite lido, `Ready` continua
elegivel. Quando `Working` atingir o limite, nao capture outra task de `Ready`
nem mova qualquer task adicional para `Working` ate uma task sair. O limite é
fail-closed: uma mutacao que produziria `6/5` deve ser recusada por worker,
scheduler, supervisor ou runner. Para o DevOps, `Deploy` vem antes de
`Working` e é a única exceção de fila: publique tasks prontas em `Deploy` sem
aumentar `Working`. Nunca altere o limite fora da configuração canônica.

## Fonte de verdade da fila

- Issues do GitHub na org `ControleOnline` (ou escopo restrito pelo prompt).
- Labels oficiais do papel + estado da issue + comentarios.
- ProjectV2 como complemento (board), nao como unico criterio quando labels bastam.

## Descoberta

1. Se o prompt definir `owner/repo` + numero da issue (ou a tarefa a ser executada) → trabalhe **diretamente nela** (validando a elegibilidade do papel), sem varredura de fila.
2. **Somente se o prompt NAO definir qual tarefa deve ser executada**:
   - busque issues em **todos** os repositorios da org `ControleOnline` (preferencialmente por label/estado);
   - se util, complemente com itens do Project #1;
   - filtre pelas regras de elegibilidade do papel;
   - **QA/Security:** pode escolher **varias** elegiveis (ordenar por prioridade e `updated`); demais papeis: escolha **exatamente uma**;
   - aplique primeiro as prioridades funcionais definidas pelo pipeline e pelo papel;
   - dentro da mesma prioridade, selecione a issue elegivel mais antiga por `createdAt` crescente;
   - em empate de `createdAt`, selecione o menor numero da issue;
   - nunca use `updatedAt` para reposicionar trabalho: comentarios, labels ou atividade recente nao fazem uma task ultrapassar outra mais antiga da mesma prioridade.

## Template de elegibilidade — `Developer`

O `Developer` deve descobrir trabalho sozinho quando a issue nao vier no prompt. Nao peca ao usuario para escolher uma issue se o GitHub/Project #1 puder ser consultado.

Este template e exclusivo do fluxo paralelo do `Developer`. O Full Pipeline / Manager executa a captura de Developer na Prioridade 5 e a higiene residual na Prioridade 6.

Fonte primaria:

- issues `open` na org `ControleOnline`;
- labels de ownership/estado;
- Project #1 como complemento para coluna/status (`Ready` e `Working`).

Candidata se **qualquer** for verdadeira:

1. possui `agent:developer`;
2. esta em `Ready` sem nenhum `agent:*` (entrada padrao do fluxo);
3. esta em `Working` sem nenhum `agent:*`, quando nao houver evidencia de ownership humano exclusivo;
4. possui `agent:qa:rejected` ou `agent:security:rejected` e ainda precisa de correcao pelo Developer.

Nao candidata se houver decisao/revisao ativa que ainda pertenca a `QA`, `Security` ou `DevOps` (por exemplo, aguardando aceite/recusa com `agent:qa`, `agent:security` ou pacote de RC).

Ordem de prioridade do `Developer` (por **tipo**):

1. `hotfix`
2. `agent:qa:rejected` ou `agent:security:rejected`
3. `bug`
4. demais tipos (`enhancement`, `feature` ou sem tipo)

**Desempate dentro de cada linha de tipo** (nesta ordem):

1. labels de prioridade `p0`, `p1`, `p2`, … (menor número = maior prioridade; issue **sem** label `p*` depois das que têm)
2. `createdAt` crescente (mais antiga)
3. menor numero da issue

`updatedAt` nao altera a posicao. `p*` **nao** e faixa entre `bug` e demais — so desempate em cada tipo. Labels `p0`/`p1`/`p2`/… podem ser criadas pelo agent quando ausentes. Se nenhuma issue elegivel existir, registre o criterio de busca e pare com bloqueio objetivo.

## Template de elegibilidade — papeis documentais

| Label | Significado |
| --- | --- |
| `agent:<papel>` | Solicitacao/marcacao para o papel (**qualquer status**) |
| `agent:<papel>:done` | Trabalho deste papel ja concluido nesta issue |

Candidata se **qualquer** for verdadeira:

- possui `agent:<papel>`;
- esta `closed` e **nao** possui `agent:<papel>:done`.

Papeis: `technical-documenter`, `tutorial-assistant`.

Conclusao documental: comentar + `agent:<papel>:done` + remover `agent:<papel>`. Sem `accepted`/`rejected`.

## Template de elegibilidade — papeis de revisao (`qa`, `security`)

Estes papeis **nao alteram codigo**, branches, PRs nem arquivos de produto. So analisam e **notificam por labels + comentarios**.

| Label | Significado |
| --- | --- |
| `agent:qa` / `agent:security` | Solicitacao explicita de revisao (**qualquer status**) |
| `agent:qa:accepted` / `agent:security:accepted` | Revisao aprovada; trabalho daquele papel **encerrado** nesta passagem |
| `agent:qa:rejected` / `agent:security:rejected` | Revisao recusada; trabalho daquele papel **encerrado** nesta passagem |

Candidata para o papel se **qualquer** for verdadeira:

1. possui `agent:<papel>` e **ainda nao** tem decisao final daquele papel (`:accepted` ou `:rejected`);
2. esta `closed` e **ainda nao** possui a aprovacao daquele papel (`agent:qa:accepted` ou `agent:security:accepted` respectivamente).

Notas:

- `rejected` **encerra** o trabalho do revisor naquela passagem (nao fica em loop infinito na mesma evidencia).
- Issue `closed` **sem** `agent:qa:accepted` **e** `agent:security:accepted` e ilegal no fluxo: o revisor que a capturar deve **reabrir** a issue antes ou durante a analise.
- Uma tarefa so pode permanecer `closed` com as **duas** aprovacoes: `agent:qa:accepted` **e** `agent:security:accepted`.

### Gate dual (fechamento)

| Estado da issue | Labels de aprovacao | Acao do revisor |
| --- | --- | --- |
| `closed` | falta `agent:qa:accepted` e/ou `agent:security:accepted` | **Reabrir** a issue, analisar, decidir por labels |
| `closed` | tem `agent:qa:accepted` **e** `agent:security:accepted` | Nao e candidata por fechamento indevido |
| `open` | tem `agent:qa` / `agent:security` sem decisao | Analisar e decidir |

### Conclusao da revisao

Ao **aprovar**:

1. Comente resumo objetivo + checklist atendido (quando couber).
2. Adicione `agent:qa:accepted` ou `agent:security:accepted`.
3. Remova `agent:qa` ou `agent:security` se presente.
4. Remova eventual `:rejected` anterior do **mesmo** papel se estiver reavaliando apos correcao.

Ao **recusar**:

1. Comente motivos objetivos + checklist nao atendido.
2. Adicione `agent:qa:rejected` ou `agent:security:rejected`.
3. Remova `agent:qa` ou `agent:security` se presente.
4. Garanta que a issue fique **open** (reabra se estiver closed) para o Developer atuar.

Em ambos os casos o trabalho **daquele agent** naquela passagem termina. Nao mexa em codigo.

## Template de elegibilidade — `DevOps`

O `DevOps` descobre trabalho sozinho quando o prompt nao informar issue. Alem do pipeline de **RC**, deve capturar handoffs marcados com `agent:devops` (incluindo **PRs soltas** encaminhadas pela higiene do Manager).

Fonte primaria:

- issues `open` na org `ControleOnline` (ou escopo do prompt);
- labels `agent:devops`, estado de RC / dual-accepted / coluna Deploy;
- Project #1 como complemento (In Review, Deploy, Ready/Working);
- PRs abertas vinculadas a issues com `agent:devops` (ou mencionadas no handoff).

Candidata se **qualquer** for verdadeira:

1. publicacao: task pai de RC (ou hotfix elegivel) na coluna **`Deploy`** — a coluna e a autorizacao humana explicita para publicar em `master`;
2. RC aberto: desvio corrigivel de board/freeze/staging (pai/filhas fora de alinhamento);
3. montagem de RC: existe dual-accepted (`agent:qa:accepted` + `agent:security:accepted`) limpo e **nenhum** RC aberto;
4. handoff DevOps: issue com label **`agent:devops`** **ou** **qualquer** PR `open` marcada/encaminhada para DevOps (label `agent:devops`, vinculo a issue `agent:devops`, ou PR solta sem handoff apos higiene). Se a PR **nao** estiver no Project #1, **associar na mesma hora** antes ou junto da decisao.

Nao candidata se a acao pertencer exclusivamente a Developer/QA/Security sem handoff DevOps, ou se nao houver delta publicavel/acao operacional objetiva para o DevOps.

Ordem de prioridade do `DevOps` (uma issue/acao por execucao, salvo fonte canonica que permita lote no mesmo RC):

1. `hotfix` / publicacao em **`Deploy`** (acao executavel)
2. RC aberto (alinhar board, freeze, staging, promocao quando aplicavel)
3. montar novo RC (dual-accepted limpo, sem RC aberto)
4. **PRs/issues com `agent:devops`** (PRs soltas no board ou encaminhadas pela higiene) — a **PR** e objeto de trabalho, nao so a issue

Dentro do mesmo nivel, selecione a candidata mais antiga por `createdAt` crescente; em empate, menor numero (issue ou PR). `updatedAt` nao altera a posicao.

Ao capturar handoff `agent:devops` / PR solta:

1. leia issue (se houver) + **PR** + comentarios de handoff;
2. se so existir a PR sem issue, trate a PR diretamente (ou use a task criada pela higiene Manager);
3. **decida** com acao objetiva: merge no fluxo permitido, alinhar branches/labels/board, ou **fechar** a PR com justificativa;
4. atualize labels/Status no Project #1; remova ou conclua o handoff `agent:devops` quando a decisao estiver executada e documentada;
5. nao deixe a PR/issue sem comentario de evidencias.

## Output minimo da descoberta

- criterio usado (prompt explicito vs busca org; se usou ProjectV2)
- issue escolhida (`owner/repo#n`)
- labels e estado (`open`/`closed`) no momento da captura
- se reabriu a issue (sim/nao)
- se a issue foi associada ao Project #1 (ao criar)
