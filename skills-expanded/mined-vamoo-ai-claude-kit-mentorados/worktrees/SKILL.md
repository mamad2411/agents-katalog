---
name: worktrees
description: >-
  Como trabalhar em paralelo no mesmo projeto sem uma sessão atrapalhar a
  outra: worktrees isolados, commit seguro quando várias abas compartilham o
  mesmo clone, e limpeza no fim. Use quando abrir mais de um terminal/sessão no
  mesmo repositório, antes de criar um worktree, ou antes de commitar num clone
  que outra sessão também usa. Gatilhos: "worktree", "paralelo no mesmo repo",
  "outra aba/sessão", "limpar branch".
allowed-tools:
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-gc.sh" --verificar *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/worktree-gc.sh --verificar *)'
---

# Terminais paralelos & worktrees

## Isolamento

- Sessão que vai **escrever**, com outra sessão possivelmente ativa no repo: worktree
  próprio com o `EnterWorktree` (cria em `<repo>/.claude/worktrees/`). O clone principal fica
  na `main`, só leitura.
- Arquivo **versionado** se restaura de `origin` (`git restore --source=origin/<branch> <arq>`),
  nunca copiado do clone principal: ele pode estar commits atrás. O SessionStart do kit
  (`warn-branch-worktree`) avisa quando a branch está atrás do upstream: `git pull --ff-only`
  antes de copiar arquivo ou criar worktree.
- **Em worktree, todo caminho de Read/Edit/Write leva o prefixo
  `<repo>/.claude/worktrees/<nome>/`**, nunca o do clone principal. Confira o prefixo antes do
  primeiro write: escrever no clone por engano suja o repo compartilhado e mistura versões.
- **Env:** com um `.worktreeinclude` na raiz do projeto, o próprio Claude Code copia do clone
  os arquivos que casam com o padrão e que o git ignora, em todo worktree que ele cria
  (`--worktree`, subagent com `isolation: worktree`, sessão paralela do desktop;
  [doc](https://code.claude.com/docs/en/worktrees.md#copy-gitignored-files-into-worktrees)).
  O modelo é o `plugin/templates/worktreeinclude.exemplo`, e o
  `instrucoes-projeto.sh --apply` o copia quando falta; commite. `.npmrc`/`bunfig.toml` ficam de fora (token de registry). A doc não diz se o
  `EnterWorktree` aplica o arquivo, e worktree criado fora do Claude Code não recebe nada:
  confira e copie à mão. Sintoma da falta: login com **"Failed to fetch"**.
- **`node_modules`** não vem: `npm install` no worktree. Symlink quebra os binários do `.bin` e
  faz dois worktrees disputarem o mesmo lock do Playwright. Enquanto ele não existe, `npx`/`bunx`
  resolve uma versão **de fora do projeto**, sem aviso.
- **`e2e/.runtime-env.json`** (e todo arquivo gerado que guarda porta de dev server) não se
  copia: ressuscita a porta de outro worktree.

## Quando o guard recusa o comando

*"too complex to verify that it stays inside the worktree"* é do harness, não do kit. Formas
que ele recusa: `bash "$VAR/x.sh"` (o caminho literal passa), `source <arquivo>`,
`gh` com `VAR="$(…)"` somado a `-q`/`--jq` entre aspas, launcher antes do `git` (o `git` tem
de ser o primeiro token) e heredoc seguido de `&&`. Contorno: `Write` o comando num `.sh` no
scratchpad e `bash /caminho/absoluto.sh`. Segunda recusa idêntica → troque de ferramenta.

Da pasta onde a sessão abriu, `EnterWorktree path:` entra em qualquer worktree de
`git worktree list` (fora de `<repo>/.claude/worktrees/`, pedindo permissão). De dentro de um
worktree, só troca para outro do mesmo repo sob `.claude/worktrees/`. Precisa de outra branch
e o trabalho anterior já está pusheado ou mergeado: `git checkout -b <nova> origin/main` no
worktree que você já tem.

## Quando o `EnterWorktree` ou o `ExitWorktree` recusa

Medido em 7 dias de transcript (22/11/2026): 19 recusas, todas de procedimento.

- `EnterWorktree`, *"not in a git repository"*: a tool olha a pasta atual do shell, não o
  `path`, e um `cd` anterior (scratchpad, pasta sem git) ficou valendo. Um Bash só com
  `cd <repo>` e chame de novo.
- `EnterWorktree`, *"would not give this agent write access"*: subagente isolado num worktree
  não troca para outro. Edite a cópia do arquivo no seu; quem orquestra despacha um agente por
  worktree.
- `EnterWorktree`, *"is the current working directory"*: você já está nele. Siga.
- `ExitWorktree` `remove`, *"now on another branch, which has N commits"*: é o fluxo do kit
  (`git checkout -b feat/x` no worktree e commit), e o `remove` simples sempre recusa aí. Com a
  prova de "Limpeza no fim", chame já com `discard_changes: true`; sem ela, `action: "keep"`.
- `ExitWorktree` `remove`, *"has N uncommitted file"* ou *"N commit on worktree-…"*: trabalho
  sem commit ou sem push. Commite e suba, ou `keep`.
- `ExitWorktree`, *"no active EnterWorktree session"*: worktree de outra sessão ou do
  `git worktree add`. Sai com `git worktree remove <wt>` a partir do clone, com a mesma prova.

## Base velha

- O squash do GitHub não apaga arquivo que só existe na `main`. Diff de PR é de **três
  pontos** (`origin/main...HEAD`); dois pontos mostra o alheio como deleção.
- **O verde do CI é do seu SHA, não da `main` de agora.** Cruze `git diff --name-only
  origin/main...HEAD` com `git log --name-only HEAD..origin/main`: arquivo ou comportamento
  nas duas → traga a `main` (rebase se a branch é só sua, merge se outra pessoa commita nela) e
  rode os testes de novo. Sem sobreposição, siga: rebase por higiene vira esteira.
- Branch de **outra sessão viva**: não rebase por baixo dela. Worktree próprio de
  `origin/main` e `git cherry-pick` dos commits.

## Commit seguro em clone compartilhado

- Branch conferida no mesmo comando do commit
  (`[ "$(git branch --show-current)" = "feat/x" ] && git commit …`); `git add <arquivos>`,
  nunca `-A`/`-u`/`.`: o index é compartilhado, e o staged de outra sessão entra de carona.
- Depois de todo commit, `git log --oneline -1 --decorate` e confira a branch antes do push.
  Caiu errado → reporte antes de corrigir.
- O kit bloqueia `git commit` na `main` (`HOTFIX_MAIN=1` de propósito) e checa a branch
  **antes** do comando: crie a branch num comando, commite em outro.
- Nada no kit impede `checkout`/`switch`/`stash`/`reset --hard` no clone principal enquanto
  outra sessão trabalha nele: a proteção é cada sessão que escreve ter o seu worktree.

## O banco local NÃO é isolado por worktree

O `supabase start` (ou o Postgres em Docker) é um só na máquina: a migration de um worktree
aparece no banco do outro. O sintoma é um **`git push` recusado** por gate de schema que acha
tabela fora das suas migrations. A pergunta é "de quem são essas tabelas?":

```bash
git diff -- <caminho>/database.types.ts | grep -c '^-'   # 0 = drift só ADITIVO, nada seu mudou
grep -rln "<tabela-estranha>" <repo>/.claude/worktrees/*/supabase/migrations/
```

1. `git fetch && git log HEAD..origin/main`: quase sempre o outro já mergeou; traga a `main`.
2. Não mergeado: `--no-verify` é decisão da pessoa, com o motivo dito no PR.
3. **Nunca `db reset` para "limpar"**: apaga as migrations do outro worktree. Dado de teste
   que você inseriu, apague você, linha a linha.

## Limpeza no fim

Só com pedido da pessoa ("pode limpar") e com a **prova completa**:

```bash
gh pr list --state merged --head <branch> --json number,headRefOid   # MERGED
git cat-file -e <headRefOid> || git fetch --no-write-fetch-head origin refs/pull/<number>/head
git merge-base --is-ancestor <branch> <headRefOid>                   # exit 0: tip igual ou contido
bash "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-gc.sh" --verificar <worktree>   # exit 0
```

Tip atrás do head do PR é o caso dos últimos commits do PR feitos noutro clone: o head só
existe no GitHub, e o `fetch` acima o traz sem gravar ref. Head ancestral do tip (commit
depois do merge) ou que nem o origin tem não prova nada.

O `git worktree remove` apaga o que o git ignora sem recusar (`.env.local` editado,
`outputs/video.mp4`, repo clonado dentro). O `--verificar` não remove nada: sai 0 com
`pode remover:` ou 1 com `keep: <caminho> — <motivos>` (não commitado, env diferente do clone,
repo aninhado, ignorado de valor, branch não mergeada); exit 2 é uso errado. Quando o motivo
diz "sem gh nem token da API", a prova do PR acima vale à mão, com uma conta do `gh` que
enxergue o repo.

- Faltou um item (exit 1): o worktree fica (`ExitWorktree` com `action: "keep"`) e você diz à
  pessoa o que faltou, com a linha `keep:`.
- A única linha `keep:` que não segura o worktree é a de um symlink para fora dele (`.venv` ou
  `models` ligado ao clone principal), porque remover apaga o link, não o alvo. Só vale quando
  o motivo é "não commitado" e o `git status --porcelain` mostra apenas o link. Ignorado de
  valor (`outputs/…`), env e repo aninhado nunca entram nela, por mais fácil que seja refazer.
  Confira o alvo com `readlink <wt>/<link>` e desfaça com `unlink <wt>/<link>`, nunca
  `rm -r <link>/`: com a barra o `rm` segue o link e apaga o alvo.
- Prova completa: `git worktree remove <wt>` (nunca `--force`), `git branch -D`, `git worktree
  prune`. Worktree do `EnterWorktree`: `ExitWorktree` `action: "remove"`; `discard_changes:
  true` só com a prova completa e o `--verificar` rodado de novo **logo antes** (ele apaga
  ignorado sem listar).
- Vários: `git-sync --cleanup-dry-run`; `--cleanup-apply` só com o pedido.
- A pessoa mandou descartar **sem** a prova (limpeza em lote, worktree de outra sessão com algo
  não commitado que talvez valha): no macOS, `mv <wt> ~/.Trash/wt-<repo>-<nome>-<AAAAMMDD>` em
  vez de `worktree remove`, que apaga de vez, e depois `git worktree prune`. Confira pelo sumiço
  da origem (`[ -e <wt> ]`): sem Full Disk Access, `ls ~/.Trash` dá "Operation not permitted".
  A Lixeira não libera disco até ser esvaziada.

Depois, `git fetch --prune`; o clone principal se atualiza com `git pull --ff-only`, sem trocar
de branch.
