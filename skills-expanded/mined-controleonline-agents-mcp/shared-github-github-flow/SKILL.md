# GitHub Flow

## Overview

Fonte canônica do fluxo de branches e entrega técnica do ecossistema ControleOnline.

Integração de desenvolvimento continua **por task**. A publicação usa Release Candidate técnica congelada para validar a composição. RC não é task pai, não cria issue agregadora e contém no máximo 5 tasks.

## Dependencias publicadas (Composer e npm)

Aplicacoes consumidoras devem depender somente de versoes estaveis numericas ja
publicadas no registry correspondente. Para pacotes ControleOnline, use a
versao exata no formato X.Y.Z. Exemplo de Composer:

```json
{
  "require": {
    "controleonline/people": "1.0.2"
  }
}
```

No Composer, use o Packagist padrao. E proibido adicionar repositories para
apontar para branches, repositorios Git, arquivos ZIP, URLs de arquivos ou
diretorios locais. Tambem sao proibidos dev-master, dev-main, dev-*, @dev,
aliases de branch e qualquer outra referencia de branch em composer.json ou
composer.lock.

No npm, dependencias @controleonline/* tambem devem usar exatamente X.Y.Z,
publicado no registry npm configurado. Dependencias GitHub/Git, URLs, caminhos
locais e sufixos de branch/tag nao substituem uma versao publicada. A versao
propria de um pacote npm tambem deve ser numerica X.Y.Z, sem sufixo RC.

Publique primeiro a versao do pacote no registry. Somente depois atualize o
manifesto do consumidor para essa versao. Isso vale em desenvolvimento,
staging e producao; nao use branch como atalho para consumir codigo ainda nao
publicado.

## Gate de origem das branches protegidas

- `dev`: origem obrigatória `task-{id_issue}`.
- `staging`: recebe RC congelada; depois da publicação, sua árvore de dependências aponta para branches `staging` dos submódulos.
- `master`: sua árvore de dependências deve apontar somente para branches `master` dos submódulos.
- `dev`, `staging`, `master`, `release/*`, branches multi-task manuais e tasks agregadoras nunca são origens válidas.
- A RC pode agregar tecnicamente de 1 a 5 tasks, mas somente pelo rito de freeze definido em `shared-github-release-candidate/SKILL.md`.

## Alinhamento obrigatório dos submódulos

O nome da branch do repositório agregador determina a branch de todos os seus
submódulos, em todos os níveis:

| Branch do agregador | Branch exigida em cada submódulo |
| --- | --- |
| `master` | `master` |
| `dev` | `dev` |
| `staging` | `staging` |

O gitlink registrado no commit pai continua sendo um SHA (é assim que Git
registra submódulos), mas esse SHA **deve ser exatamente a ponta da branch
homônima no repositório do submódulo**. Um pin em SHA antigo, mesmo que o
checkout local mostre uma branch, é divergência. O campo `branch` de cada
entrada em `.gitmodules` também deve declarar a branch correspondente para
que `git submodule update --remote` não escolha outra linha.

Antes de iniciar uma task no agregador, confirme recursivamente que o pai está
em `origin/master` e que cada gitlink corresponde a `origin/master` do
submódulo. Ao reconciliar `dev` ou `staging`, faça a mesma conferência usando
`origin/dev` ou `origin/staging` em todos os níveis. Se uma ref `dev` ou
`staging` não existir em um submódulo, crie-a a partir de `origin/master` e
atualize o gitlink do pai para o SHA dessa ref. Não declare alinhamento até
que toda a árvore recursiva passe; um reset apenas do repositório pai não é
suficiente.

## Regra inviolável de integração

Todo código que sair de uma branch de trabalho ou de integração para outra
branch deve chegar ao destino por **merge** ou por **Pull Request aprovado e
mergeado**. Isso vale para `dev`, `staging`, `master`, projetos agregadores e
submódulos.

Push direto em branch de integração, cherry-pick como substituto do merge,
atualização isolada de SHA e gitlink apontando diretamente para commit de task
**não são publicação**. Em repositórios com submódulos, primeiro faça o merge
da entrega no branch do submódulo; depois faça o merge do commit pai que atualiza
o gitlink para esse commit já integrado. Se o merge ou PR não puder ser
revisado semanticamente, aborte e registre o bloqueio.

## Branches

| Branch | Papel |
| --- | --- |
| `master` | Linha principal / produção |
| `dev` | Integração contínua, promovida pelo Manager/DevOps após a entrega |
| `staging` | RC congelada publicada para homologação; todos os gitlinks apontam para `staging` nos submódulos |
| `task-{id_issue}` | Branch de trabalho do Developer |

## Fluxo ponta a ponta

```text
master
  └─ task-{id}                         (Developer cria a partir de master)
       └─ task de entrega no Paperclip  (Developer → Manager)
            └─ subtasks Developer + Security + DevOps
                 └─ Manager organiza labels, status e board
                      └─ Security
                      └─ agent:security:accepted + revalidacao Manager
                      └─ DevOps publica RC congelada e alinha gitlinks staging → staging
                           └─ coluna In Review
                                └─ humano → coluna Deploy
                                     └─ DevOps integra task em master e alinha gitlinks master → master
                                          ├─ Security aceito → Done
                                          └─ sem Security/evidencia → Working
```

## Etapas já concluídas (pular com justificativa)

Se o estado real do GitHub mostrar que o passo **já foi feito**, o agent não refaz. Deve confirmar evidência (commits, merge-base, labels, coluna), pular só o concluído, avançar o próximo estágio e comentar a justificativa.

**Não** pule etapas por intuição. `QA`, `Security`, `Design` e `UX` estao ativos
em paralelo: o Manager solicita os quatro labels e o gate de RC exige o quarteto
`:accepted` de cada um.

## Gate de atenção redobrada antes de qualquer merge

Merge não é apenas uma operação textual nem fica validado porque o Git não
reportou conflito. Antes de confirmar **qualquer** merge entre uma task e uma
branch de integração, ou entre a RC homologada e `master`, o agent responsável deve:

1. confirmar a origem, o destino, os dois SHAs atuais e o `merge-base`; se a
   origem foi criada antes de uma alteração relevante já presente no destino,
   atualizar/revisar a task sobre o destino atual antes de promover;
2. inspecionar o diff do resultado final (`merge-base`/origem/destino e
   `git diff` do commit de merge), não somente a tela de conflitos;
3. conferir explicitamente que cada requisito negativo da task continua
   verdadeiro (por exemplo, uma aba removida não pode reaparecer), que nenhum
   arquivo fora do escopo foi restaurado e que as alterações independentes de
   outras tasks foram preservadas;
4. em projetos com submódulos, revisar cada diff e confirmar recursivamente
   que o gitlink aponta exatamente para a ponta remota da branch de mesmo nome
   (`master` → `master`, `dev` → `dev`, `staging` → `staging`); SHA antigo ou
   branch declarada divergente em `.gitmodules` bloqueia a entrega;
5. executar os testes/verificações focados no comportamento alterado e registrar
   a evidência do estado pós-merge antes do push.

Se qualquer item não puder ser confirmado, **não faça o merge nem o push**:
pare na fronteira segura, registre a divergência e atualize/rebaseie a origem
ou peça a correção ao responsável. Resolução automática de conflito, merge sem
conflito ou branch de origem aparentemente limpa não substitui este gate.

### Recuperação obrigatória de conflito grande

Quando a origem estiver muito divergente, apresentar conflito amplo ou não
permitir separar com segurança o delta da task, o agent deve interromper e não
forçar a resolução. Nesse caso:

1. aborte o merge/rebase e preserve a evidência do conflito;
2. confirme que a branch remota de task é descartável e, somente então, apague
   `task-{id_issue}`;
3. recrie `task-{id_issue}` a partir do `master` remoto atualizado;
4. reaplique a correção do zero, com escopo e testes da issue;
5. retorne a task para **`Working`**, remova as decisões/aceites herdados da
   entrega descartada e reative a solicitação de `Security`;
6. publique a nova branch e siga novamente o caminho obrigatório de merge ou PR
   em `dev`, `staging` e `master`.

Apagar e recriar a branch não autoriza copiar o gitlink, escolher “ours” ou
“theirs” cegamente, fazer force-push, ou marcar a task como concluída. O
resultado recriado deve passar pelo mesmo gate semântico e deixar comentário
com a branch descartada, a nova base `master`, os SHAs e os testes executados.
Uma task recriada não pode permanecer em `Done`, `Deploy` ou `In Review`, nem
ser validada com labels anteriores: a validação começa novamente após o novo
merge em `dev`.

### Regra explícita de status e revalidação após entrega em `dev`

Quando a task reconstruída ou corrigida tiver sido publicada somente em
`dev`, o Manager deve, na mesma rodada:

1. manter ou retornar o item do Project #1 para **`Working`**;
2. remover todas as decisões anteriores de `Security` daquela entrega
   (`agent:security:accepted`, `agent:security:rejected`);
3. reativar `agent:security` para validar os novos SHAs mergeados em `dev`;
4. só permitir **`In Review`** depois que a task individual tiver sido
   inventariada em RC congelada promovida a `staging` e possuir
   `agent:security:accepted`.

Não é suficiente remover apenas `agent:developer:done` ou reabrir a issue:
aceites e recusas de uma entrega descartada não podem acompanhar a nova
entrega.

## Developer

1. Captura issue elegível.
2. Cria ou reutiliza `task-{id_issue}` **a partir de `master`** atualizado.
3. Implementa e valida na branch da tarefa.
4. Sincroniza com `origin/master` antes de continuar/encerrar.
5. Publica somente `task-{id_issue}` e cria task de entrega no Paperclip para o Manager.
6. Executa o gate compartilhado de entrega local: toda alteração em projeto principal, submódulo ou gitlink deve estar publicada; cada checkout afetado deve ser conferido contra `origin/master` e ficar sem staged/unstaged/untracked. Registra exceções de branch com SHA e ref remoto.
7. O Manager cria as subtasks ativas de Security e DevOps, organiza labels/status/board e só então promove a integração.

### Proibições do Developer

- **Não** abre PR no fluxo normal.
- **Não** mergeia em `staging` nem em `master`.
- **Não** commit/push direto em `master`, `main`, `dev`, `staging`.
- Trabalho só na `task-{id_issue}`; chegada em `dev` é por **merge** da task branch.

### Entrega = branch publicada + task Paperclip

A entrega técnica é a branch `task-{id_issue}` publicada e a task de entrega no Paperclip. O Manager decide, por suas subtasks concluídas e pela checagem final, quando promover a integração e mover o board.

## Revisão ativa (Security)

- `Security` atua sobre a task/issue e a evidência da entrega (commits na task branch e o que foi mergeado em **`dev`**).
- Registra `agent:security:accepted` ou `agent:security:rejected`.
- **Não** abre PR; **não** finaliza task; **não** mexe em branches de integração.
- Recusa devolve prioridade ao Developer na mesma `task-{id_issue}`.

`QA`, `Security`, `Design` e `UX` capturam fila, aplicam labels e bloqueiam
RC/staging/Deploy ate o aceite (excecao hotfix).

Gate de staging/RC (task comum):

- `agent:qa:accepted`
- `agent:security:accepted`
- `agent:design:accepted`
- `agent:ux:accepted`

## DevOps — integração contínua por task (sem RC)

No Manager, DevOps é **P1**. Hotfix é **P2**.

### Entrada (P1)

1. Todas as tasks na coluna **`Deploy`** (cada delta publicado separadamente em
   `master`) — primeiro.
2. Task com `agent:security:accepted` e revalidacao do Manager ainda fora de RC / `staging` / `In Review`.
3. Issues/PRs com `agent:devops` com ação de merge restante.

Promoção de `hotfix` → staging é P2, não P1.

### Proibido

- Criar task pai `RC X.Y.Z-rc.N`.
- Freeze de pacote / inventário de filhas como rito novo.
- Mergear `dev` inteiro em `staging`.
- Abrir segundo “RC” paralelo.
- Promover task comum a staging fora de uma RC congelada ou sem `agent:security:accepted` (exceção: `hotfix` na P2).

### Promoção a staging

1. Staging parte de `master` atual + merge **somente** de `task-{id}`.
2. Pai + submódulos afetados (submódulos primeiro; pins coerentes).
3. Aplicar o **Gate de atenção redobrada antes de qualquer merge**. Conflito:
   abortar aquele merge, comentar, seguir a próxima task. Ausência de conflito
   não dispensa a revisão semântica do resultado.
4. Versão em `package.json` / `app.json` quando o bump for necessário: **somente números** (SemVer). Sem sufixo `-rc`.
5. Push em `staging` dispara deploy de conferência.
6. A passagem para **`In Review`** é feita pelo Manager somente para tasks
   presentes no manifesto da RC congelada que chegou a staging; o DevOps não
   move a task para essa coluna.

### `In Review`

Sinal de que a **task individual** esta no manifesto da RC congelada já
publicada em staging e aguarda revisão humana. Nenhuma task entra depois do
freeze da RC sem pedido humano explicito para gerar `rc.N+1`.

### Publicação (coluna Deploy)

1. Humano move a task para **`Deploy`**, com ou sem o quarteto; essa mudança
   de coluna é a autorização explícita para publicar em `master`.
2. DevOps aplica o **Gate de atenção redobrada antes de qualquer merge** e
   mescla somente o delta da task (`task-{id}`) → `master` (pai + submódulos).
3. devolva ao Manager o handoff com SHA, versão publicada, runtime e estado de
   `Security`.
4. O Manager decide a coluna final. Com `agent:security:accepted`, move para
   **`Done`** e cria no Paperclip as filhas documentais aplicáveis. Sem Security
   aceito, move para **`Working`** e reativa `agent:security`; com rejeição,
   aciona o Developer para corrigir e depois reencaminha a Security.

Nunca direto a `master` sem coluna `Deploy`, salvo correção estrutural de governança em `agents-mcp`.

Detalhes: `agents/skills/controleonline/shared-github-master-publication/SKILL.md`.

### O que o DevOps não faz

- Não implementa feature de produto no lugar do Developer.
- Não monta RC.
- Não inclui task comum sem `agent:security:accepted` e revalidacao do Manager (exceção `hotfix` na P2).

## Quem pode o que

| Acao | Developer | Validadores | DevOps |
|------|-----------|-------------|--------|
| Branch `task-{id}` a partir de `master` | sim | nao | so excecao |
| Merge `task-{id}` → `dev` | não | não | Manager/DevOps conforme subtask |
| Merge `task-{id}` → `staging` | **nao** | **nao** | **sim** |
| Abrir PR de produto / task | **nao** | **nao** | **nao** (salvo excecao) |
| Labels `:accepted` / `:rejected` | nao | sim | nao |
| Criar task pai RC | **nao** | **nao** | **nao** |
| Merge delta → `master` | **nao** | **nao** | **sim** (coluna Deploy) |

## Hotfix (P2 do Manager)

Label obrigatória: `hotfix`.

No Full Pipeline, hotfix vem **depois** do DevOps (P1).

```text
master
  └─ task-{id}
       └─ merge task-{id} → dev
            └─ DevOps cria RC de hotfix → staging [P2]
                 └─ In Review → humano Deploy → delta → master
                      ├─ Security aceito → Done
                      └─ sem Security/evidencia → Working → segunda validação
```

- Dual-gate **não** bloqueia entrada em `staging` no hotfix.
- `master` ainda exige coluna **Deploy**.
- Publica **somente o delta** da `task-{id}`.
- Manager P1 = DevOps. Manager P2 = hotfix. Manager **não** implementa produto; exceção estrutural em `agents-mcp` (docs/governança/runners).

## Quality Bar

- não derive task branch de `dev`/`staging` (sempre de `master`)
- não entregue Developer em `staging` (destino é `dev`)
- não faça handoff com mudança local, commit não publicado ou projeto/submódulo afetado sem conferência contra `origin/master`
- não promova para `master` sem coluna `Deploy` e passagem por `In Review`
- não monte RC, pai de RC ou freeze de pacote
- não pule etapa sem evidência verificável
- não mova `Deploy` de volta para `In Review` sem rejeição humana explícita

## Project Status: Blocked e Backlog

Esta regra se refere exclusivamente a colunas do **GitHub Project #1**:
agents nao selecionam, comentam, validam, rotulam, editam nem movem issues em
`Blocked` ou `Backlog`. O status `blocked` de tasks Paperclip e distinto e
constitui fila prioritária de recuperacao para Manager/CTO; essa recuperacao
operacional nao autoriza mutacao na issue/board GitHub `Blocked`.
