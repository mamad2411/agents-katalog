---
name: git-sync
description: >-
  Sincroniza clone e worktrees com o GitHub sem risco (fetch --prune, só fast-forward) e
  mostra o estado: ahead/behind, worktrees, PRs abertos. Use em "/git-sync", "atualiza
  com o github", "puxa o remote", "source control desatualizado", e no início ou fim de
  sessão em repo compartilhado ("meu colega mexeu?", "tem PR aberto?").
allowed-tools:
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh")'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh)'
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh" --status-only)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh --status-only)'
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh" --team)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh --team)'
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh" --cwd * --team)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh --cwd * --team)'
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh" --cleanup-dry-run)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh --cleanup-dry-run)'
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-gc.sh" --verificar *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/scripts/worktree-gc.sh --verificar *)'
---

# /git-sync — Atualizar local com o GitHub

Rode o script pelo caminho literal (dentro de worktree, o guard recusa `bash "$S"`):

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/git-sync/scripts/git-sync.sh"   # + --status-only, --team, --cleanup-dry-run...
```

(Instalação antiga pelo `install.sh`: `bash ~/.claude/skills/git-sync/scripts/git-sync.sh`.)
O output dele **é o relatório**: cole os trechos relevantes e acrescente só o `PENDENTE:`.
Flags e o que o `--cleanup-apply` remove: [references/flags.md](references/flags.md).

O alvo de cada checkout é o upstream próprio (`@{u}`), senão `origin/<default>`. Commit só local
é "push pendente", nunca skip. Clone principal fica na branch em que está; `--voltar-main` o
devolve à default (opt-in, ff-only, aborta com árvore suja ou operação em andamento).

## Ao abrir e ao fechar (repo de time)

O modo time liga sozinho com ≥2 autores na default em 30 dias (`--team` força, `--no-team`
desliga). Leia nesta ordem e não comece a codar antes de zerar:

1. `### mural da equipe`: o trecho sob `## Ativos` de `.context/docs/avisos-da-equipe.md`
   (ou `.context/avisos-da-equipe.md`, ou `AVISOS.md`; sem `## Ativos`, o arquivo inteiro).
   É o que o git não sabe: "não mexa nesse arquivo ainda", "mudei o formato, seu merge vai
   doer". Aviso sem data e sem dono não conta. Quem resolve, apaga no mesmo PR.
2. `### avisos (ação sua)`: cada `!` bloqueia até a pessoa decidir.
3. `--- risco de conflito ---`: arquivo listado → sincronize com a default antes de tocar nele.
   Para outro worktree, `--cwd <worktree> --team`.
4. `--- novidades em origin/<default> ---`, `### PRs abertos` e `--- branches remotas ativas ---`:
   o que entrou desde a sua base; PR na sua área, fale antes; `feat/x` que já existe no remoto,
   não crie outra.

Ao fechar, rode de novo: *"commit(s) sem push"* / *"NUNCA foi ao GitHub"* vai para o
`PENDENTE:`. Exceção: o aviso diz que um PR mergeado tem head igual ao tip → os commits já
estão na default (sobra do squash), **não pushe de volta**. O git-sync não sobe nada: o push é
do fluxo da tarefa (a `ship`, por exemplo).

## Regras duras

1. **Só fast-forward.** Nunca merge commit, `rebase` automático, `reset --hard` nem force-push.
2. Não commita, não faz `git add`, não apaga worktree/branch/remoto sem pedido ("pode limpar").
3. Árvore suja (modified/staged) → não puxa naquele checkout; untracked sozinho não bloqueia,
   só é reportado.
4. Em repo de time, `### avisos` não-vazio vem **antes** de tudo e é bloqueio. Não implemente
   por cima de branch divergida, nem de branch atrás cujo `risco de conflito` lista arquivo
   seu; atrás sem sobreposição não bloqueia. `git pull --rebase` para divergência é sugestão
   à pessoa, nunca execução.
5. "Tudo em dia" só com `### avisos` vazio, não porque o `fetch` passou.

## `gh` e conta

Sem `gh`, o relatório sai cego para PR, mas segue. Com duas contas no keyring, o script testa
as outras, usa a que enxerga o repo (sem trocar a ativa) e diz qual; nenhuma enxerga →
`nenhuma conta do gh enxerga <owner/repo>`. Repo de outra org com o PAT num `.env` da raiz
(`.env.tokens`, `.env.local` ou `.env`): o script usa o `GH_TOKEN`/`GITHUB_TOKEN` de lá só nesta
execução, e só quando o `gh` não enxerga o repo, e diz de qual arquivo veio. Não leve esse token
para o keyring (`gh auth login --with-token`): ele passaria a valer nos outros repos da máquina.
Repo onde o `gh` não pode rodar:
`git config git-sync.noGh true` + `git config git-sync.tokenVar <VAR>`, e PRs e prova do cleanup
saem da API REST. Detalhe: [references/flags.md](references/flags.md#gh-e-api-rest).

## Cleanup

`--cleanup-dry-run` lista; `--cleanup-apply` só com o pedido. A prova é PR mergeado com o tip
igual ao head do PR ou contido nele (os últimos commits do PR feitos noutro clone; o head que
falta é buscado em `refs/pull/<n>/head` sem gravar ref). A remoção à mão segue a skill
`worktrees` ("Limpeza no fim"), com a mesma prova e
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-gc.sh" --verificar <worktree>` saindo 0. Sem
prova, fica.

## Se o script falhar: só leitura

```bash
git fetch --prune origin && git worktree list
git -C <worktree> status -sb
git -C <worktree> rev-list --left-right --count HEAD...origin/<default>   # ahead behind
gh pr list --limit 20
```

Reporte o estado e o que puxaria; ff-only e limpeza ficam para o script.
