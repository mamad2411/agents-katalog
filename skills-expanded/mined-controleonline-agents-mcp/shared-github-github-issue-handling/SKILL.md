# GitHub Issue Handling

## Overview

Use esta skill para centralizar as regras de uso do GitHub no contexto operacional de sysadmin.

Ela cobre:

- abertura, atualizacao e organizacao de issues operacionais
- classificacao correta por coluna
- prevencao de duplicacao
- uso de labels compativeis com o papel de sysadmin
- regras de acesso e uso tecnico no GitHub
- uso de repositorios como contexto operacional
- uso de GitHub Actions como sinal tecnico complementar

## Core GitHub Policy

Ao interagir com GitHub para gestao operacional, issues, acompanhamento, organizacao de trabalho ou consulta de estruturas de projeto:

- nao use assignee como mecanismo de captura, triagem ou ownership
- nao feche issues em nome de agents; `closed` pertence apenas a humanos
- pode usar qualquer consulta, API, ferramenta, busca, endpoint, viewer, listagem, mutacao ou superficie do GitHub que estiver disponivel na sessao
- trate o app do GitHub conectado ao agent como caminho principal para operacoes no GitHub, mas sem restringir a consulta a uma unica API ou superficie quando houver outras disponiveis
- escolha livremente entre GraphQL, REST, search, listagens, consultas por repositório, issues, PRs, reviews, workflows, jobs, checks, branches, commits, comments, labels e ProjectV2 sempre que isso ajudar a obter a evidência correta
- se uma superficie estiver bloqueada por limitacao de infraestrutura, rede, proxy, egress, autenticacao da sessao ou erro operacional semelhante, use qualquer outra superficie do GitHub que estiver disponivel e siga a execucao
- trate bloqueio pontual de uma API ou superficie como limitacao operacional do ambiente, nao como falha fatal do repositorio, do projeto ou da rotina
- quando um caminho alternativo for usado, continue a execucao pelo meio mais seguro e registre a limitacao e o impacto no historico operacional quando isso for relevante
- se o ambiente exigir autenticacao baseada em arquivo sensivel para uma chamada direta necessaria, use apenas a credencial operacional ja definida para o agent e nunca exponha seu valor

## GitHub As Operational Context

Use o GitHub como fonte complementar de contexto tecnico e operacional dos projetos, nunca como substituto da verificacao do ambiente real.

Use o GitHub para:

- identificar repositorios relacionados ao servidor, servico ou rotina em analise
- entender estrutura do projeto, scripts, servicos auxiliares e pontos de atencao
- localizar documentacao, runbooks, arquivos de configuracao, workflows, manifests e instrucoes operacionais
- descobrir peculiaridades do projeto que afetem diagnostico, manutencao e operacao segura

Se houver divergencia entre o estado do ambiente e o estado aparente do repositorio, priorize a validacao do ambiente real e trate o GitHub apenas como contexto complementar.

## GitHub Actions As Supporting Signal

Ao checar GitHub Actions:

- examine as execucoes mais recentes dos workflows relevantes ao projeto ou servico afetado
- verifique status, etapas com falha, recorrencia e relacao temporal com o problema operacional observado
- avalie possivel causa e possivel solucao com base nos logs do workflow, no contexto do repositorio e nos sintomas do ambiente
- trate falhas de workflow como sinal tecnico importante, mas nao como prova unica da causa raiz
- se houver problema relevante sem acompanhamento claro no GitHub, abra ou atualize a issue correspondente por esta mesma skill

## Issue Creation And Update Workflow

1. antes de abrir nova issue, verifique se ja existe acompanhamento claro para o mesmo assunto
2. se ja existir issue, investigacao, pull request ou acompanhamento equivalente, prefira atualizar, comentar ou referenciar em vez de duplicar
3. nunca atribua responsavel
4. nunca exponha credenciais, segredos, tokens, conteudo sensivel de arquivos de ambiente, dados pessoais ou trechos sensiveis de logs
5. se citar logs, resuma ou sanitize o conteudo
6. registre contexto suficiente para entendimento tecnico, rastreabilidade e continuidade operacional
7. quando outro agent ficar bloqueado por infraestrutura, abra ou atualize uma issue separada em `Ready` com tag `agent:sysadmin`, referencie a issue original e descreva apenas o bloqueio operacional necessario para destravar a trilha
8. a issue paralela de `Sysadmin` deve continuar separada da tarefa-mãe; quando o impedimento for resolvido ou diagnosticado, o `Sysadmin` deve comentar na tarefa-mãe e trocar a issue paralela para `agent:security`

## Column Policy

Use as colunas desta forma:

- problemas operacionais, de desenvolvimento, de seguranca e demais encaminhamentos de trabalho devem ir para a coluna `Ready` ou `Working`
- `Ready` e a fila canonica de entrada; `Working` e o estado transitorio da execucao ativa
- itens que existem para validacao manual posterior devem ir para a coluna `In Review`
- tarefas de `DevOps` devem ser lidas na coluna `Deploy`
- agents documentais externos ao nucleo, como `Documentor`, leem suas tasks na coluna `Done`
- nao use coluna `Security` neste fluxo

## Classification Rules

### Ready

Use a coluna `Ready` ou `Working` quando houver:

- bug
- regressao
- falha de aplicacao
- erro recorrente de software
- comportamento incorreto de codigo
- incidente operacional que precise acompanhamento tecnico
- indicio de problema de seguranca, vulnerabilidade, exposicao indevida, comportamento suspeito, acesso anomalo ou possivel incidente
- bloqueio de infraestrutura que precise acompanhamento do `Sysadmin`
- melhoria
- novo recurso


- crie/atualize no repositorio afetado, nao necessariamente no repositorio pai do RC
- coluna: `Ready`
- labels obrigatorias: `hotfix`, `bug` e `agent:developer`
- label de pagina obrigatoria quando a rota/tela for identificavel
- nao cole tokens, headers sensiveis, screenshots com dados reais ou logs brutos contendo segredo
- nao use assignee para direcionar; a label `agent:developer` e o roteamento oficial
- nao marque como bloqueio da publicacao se a falha for flaky, fora do delta publicado ou tiver sido explicitamente diferida; nesse caso, registre que a correcao segue na **P5 Developer** do Manager, com prioridade de `hotfix`

Em casos de seguranca, mantenha a issue em `Ready`, mas reduza detalhes exploraveis e preserve somente o contexto seguro necessario.

Toda issue criada para trabalho tecnico deve receber uma label de tipo correspondente:

- `bug` para bug, regressao, falha, erro recorrente ou comportamento incorreto
- `enhancement` para melhoria
- `feature` para novo recurso

### In Review

Use a coluna `In Review` quando houver:

- necessidade de validacao manual posterior
- acompanhamento apos hotfix
- confirmacao operacional pendente depois de correcao, ajuste ou propagacao entre branches

## Labels By Role

Ao criar ou atualizar issues:

- use tags compativeis com o papel responsavel pela proxima etapa
- use uma label de tipo obrigatoria (`bug`, `enhancement` ou `feature`) em toda task nova
- no backlog novo, use `agent:developer` como classificador de entrada
- combine labels de papel com labels de tipo de problema quando isso ajudar a triagem
- **label de página (obrigatória quando identificável):** ao criar issue a partir de erro, relato ou URL de tela, aplique label com o slug da página
  - URL: usar o segmento de path relevante (ex.: `/client-details?...` → `client-details`)
  - sem URL: inferir pelo texto do relato quando possível
  - kebab-case; sem domínio, query, hash ou IDs
  - se a label não existir no repositório, criá-la (é permitido criar labels oficiais ausentes)
  - se a página não for identificável, não inventar label; documentar no corpo
- nao invente labels que nao existam (exceto a de página e demais labels oficiais do fluxo, que podem ser criadas quando ausentes)
- se a lista de labels disponivel nao estiver clara para labels opcionais, siga sem label adicional em vez de presumir uma label inexistente

## Security Handling Inside GitHub

Quando houver indicio de problema de seguranca:

- faca o registro no GitHub por esta skill, sem criar fluxo separado fora dela
- coloque a issue em `Ready` ou `Working`
- descreva risco, impacto potencial, sintomas observados, escopo afetado e evidencias nao sensiveis
- omita detalhes que aumentam risco de exploracao ou revelem segredos desnecessariamente
- preserve rastreabilidade suficiente para continuidade da investigacao

## Output Contract

Ao concluir, entregue um resumo operacional curto com:

- issue criada, atualizada ou referenciada
- coluna aplicada
- tags aplicadas, quando houver
- motivo da classificacao
- limitacao tecnica relevante, se houve troca de superficie no acesso ao GitHub
- indicacao de validacao manual pendente, quando existir
- achado relevante de repositorio ou workflow, quando isso tiver sido parte da analise
- se houve tarefa-mãe relacionada, confirmação de que ela recebeu comentário do `Sysadmin`

## Quality Bar

- nao duplique issues sem necessidade
- nao atribua responsavel por padrao nem por excecao
- nao feche issues como substituto de mudanca de coluna ou tag
- nao use a coluna `Security`
- nao exponha dados sensiveis
- nao trate GitHub como substituto do estado real do ambiente
- nao deixar issue nova com página/URL identificável sem a label de página
- sempre mantenha tudo relacionado a GitHub centralizado nesta skill
