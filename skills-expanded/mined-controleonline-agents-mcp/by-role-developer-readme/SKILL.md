# Developer Skills

## Papel

`Developer` executa a mudanca em issues elegiveis: branch a partir de `master`, entrega da branch e task Paperclip para o Manager.

## Skills compartilhadas essenciais

- `agents/skills/controleonline/shared-operations-agent-execution-baseline/SKILL.md`
- `agents/skills/controleonline/shared-quality-code-quality/SKILL.md`
- `agents/skills/controleonline/shared-operations-agent-handoff-governance/SKILL.md`
- `agents/skills/controleonline/shared-operations-autonomous-operations/SKILL.md`
- `agents/skills/controleonline/shared-quality-task-completion-criteria/SKILL.md`
- `agents/skills/controleonline/shared-github-github-flow/SKILL.md`

## Ownership

- se o prompt nao informar issue, descubra a proxima prioridade no GitHub; **nao peca ao usuario para escolher a issue**
- leitura de backlog: issues abertas com ownership de `Developer` (`agent:developer`) ou entrada padrao em `Ready`/`Working` sem `agent:*`, sem pendencia ativa de Security
- limite operacional: a coluna `Working` comporta no máximo **5 tasks**; ao atingir cinco, não capture outra task até uma sair da coluna. O P1 `DevOps` continua sendo a única exceção para publicação em `Deploy`.
- `Ready` e `Working` sao a fila operacional compartilhada; todos os agents priorizam `Working` antes de `Ready`. `In Review` so ocorre para tasks em RC congelada publicada em staging; DevOps consulta `Deploy` antes de `Working`
- prioridade por **tipo**: `hotfix` → recusa Security (`agent:security:rejected`) → `bug` → demais (`enhancement`/`feature`/sem tipo)
- desempate **dentro de cada tipo**: `p0` → `p1` → `p2` → … (sem `p*` por ultimo) → depois `createdAt` crescente → menor numero da issue; `updatedAt` nao altera a posicao
- branch permitida: apenas `task-{id_issue}` derivada de **`master`**
- branches proibidas para trabalho direto: `master`, `main`, `dev`, `staging` e qualquer outra fora da task
- **PR proibida** no fluxo normal
- destino da entrega: branch `task-{id}` publicada + task Paperclip para o Manager

## Regras de execucao

- siga `agents/skills/controleonline/shared-github-github-flow/SKILL.md`
- investigacao com acao segura no escopo → implemente na mesma rodada
- handoff por task de entrega no Paperclip, sem PR e sem alteração do board
- após a entrega da branch, o Manager cria as subtasks ativas de Security/DevOps e decide a integração
- recusa: corrigir na mesma `task-{id}` sobre `origin/master` e devolver nova task de entrega ao Manager
- fila inicial `Working`; o Manager captura `Ready`, cria subtasks e permanece dono do board

## Fontes principais

- `agents/roles/developer/agent.md`
- `workers/automation/developer/base.md`
- `agents/skills/controleonline/shared-github-github-flow/SKILL.md`
