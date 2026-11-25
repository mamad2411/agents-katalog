---
name: varredura-git-multi-repo
description: Encontrar trabalho órfão (commit, stash, worktree, branch) espalhado por vários repositórios git, classificar antes de agir e provar por dois métodos antes de qualquer deleção. Carregar ao fechar uma sessão longa, antes de declarar "está tudo mergeado", e SEMPRE antes de apagar branch ou worktree.
---

# Varredura git multi-repo — achar o que ficou para trás, e provar antes de apagar

## Por que o ritual normal não pega

`git status` + "estou à frente do remote?" olham só a branch atual do repositório atual.

| Esconderijo | Comando que revela |
|---|---|
| branch local em OUTRO repo, nunca publicada | `git branch --no-merged main` |
| branch remota que ninguém mergeou | `git branch -r --no-merged origin/main` |
| stash | `git stash list` |
| worktree com branch própria | `git worktree list` |
| HEAD solto | `git symbolic-ref -q HEAD` |
| arquivo novo nunca adicionado | `git status --porcelain \| grep '^??'` |

Rode em laço explícito sobre todos os repositórios, nunca um comando "global" ambíguo:

```bash
for d in <repo1> <repo2> ...; do (cd "$d" && echo "== $d" && git status -sb | head -1 \
  && git branch --no-merged main && git stash list && git worktree list); done
```

## Achado não é sinônimo de trabalho perdido — classifique

1. **Commit real órfão** → publique, PR, merge.
2. **Stash/branch já superado** → a `main` já tem o conteúdo por outro caminho? Confira o CONTEÚDO (grep no arquivo atual), não só a ancestralidade — um fix pode ter chegado reescrito por outro commit. Não apague stash: pode ser de outra sessão e não custa ficar.
3. **Ruído** (metadado de sistema de arquivos, `test-results/`) → confirme que não é versionado e siga.

## Antes de apagar: dois métodos independentes, e nunca confie no nome

```bash
# Método 1 — commits fora da main, branch a branch
for b in $(git branch --format='%(refname:short)' | grep -v '^main$'); do
  echo "$b -> $(git rev-list --count main..$b) commit(s) fora da main"; done
# Método 2 — independente, tem de concordar
git branch --no-merged main | wc -l     # precisa dar 0
```

Para branch remota: `git merge-base --is-ancestor <sha> origin/main` E `git branch -r --contains <sha> | grep origin/main`. Com squash merge, os commits da branch não são ancestrais: prove pela árvore (`git diff <branch> origin/main --stat` vazio) ou pelo estado `MERGED` do PR com o head igual ao SHA local.

Se os dois métodos discordam, **pare**. Use `git branch -d` (não `-D`): o git recusa branch não mergeada — terceira rede.

## O HEAD pode se mover debaixo de você

Outra sessão pode trocar a branch do diretório principal entre a sua criação de branch e o seu commit. Confirme a branch antes de cada commit, não só no início.

## Worktree: verifique se está viva antes de remover

Worktree com processo ativo, arquivo não versionado ou branch sem merge não é lixo. Confira `git -C <wt> status --porcelain`, procure arquivos que só existem ali, e só então `git worktree remove`.

## Fechamento de ciclo

Branch mergeada que sobrevive faz outra sessão refazer o trabalho ou derivar de ponto atrasado. Mergeou: apague local e remota no mesmo passo, com a prova acima, e atualize o quadro de trabalho.
