---
name: estado-compartilhado-multi-agente
description: Como não estragar o ambiente de outras sessões que trabalham na MESMA árvore — worktree derivado de main local desatualizado, arquivo inteiro sobrescrito por versão antiga, rm que atravessa symlink, npm install que materializa node_modules compartilhado, branch de escopo que vira segundo trunk (§1c), e o HEAD que outra sessão move debaixo de você. Carregar antes de criar git worktree, antes de qualquer rm/mv fora do seu diretório, antes de npm install/update, antes de publicar na main com o checkout principal sujo de outra sessão (§7), antes de interpretar um erro de build que "apareceu do nada", e antes de escolher qual checkout ler quando duas árvores se dizem "o trabalho de X".
---

# Estado compartilhado — o que quebra quando vários agentes usam a mesma árvore

Nenhum destes casos é falta de conhecimento técnico. Todos são a mesma falha de método:

> operar sobre um estado compartilhado presumindo que ele é o que você espera, em vez de conferir que é.

A conferência custa um comando. O erro custa o trabalho de outra sessão — e costuma aparecer disfarçado de outra coisa.

## 1. Worktree derivado de `main` LOCAL herda o atraso dele

O `main` local de um repositório cujo diretório principal está na branch de outra sessão não é atualizado — você não pode dar `checkout main && pull` ali sem sequestrar o trabalho dela.

```bash
git fetch origin && git worktree add -b <agente>/<slug> <caminho> origin/main
```

Correção importante, medida: a branch atrasada NÃO reverte o que `main` ganhou — o merge de três vias preserva os dois lados. O custo real é trabalhar sobre base velha (conflito, divergência entre repositórios).

## 1b. O caso que realmente apaga trabalho: arquivo inteiro sobrescrito com versão antiga

Uma branch EM DIA com `main` cujo commit sobrescreve um arquivo inteiro com uma versão velha (um `cp` malfeito) carrega a remoção explícita no diff; o merge a aplica sem conflito. Não há gate possível — é indistinguível de remoção deliberada. Defesa: olhar o `git diff` depois de qualquer `cp`/`mv`/geração por script.

## 1c. Branch de escopo vira segundo trunk

Branch cujo nome descreve **escopo** (`feature/resto-do-projeto`, `feature/R1-restante`) em vez de uma unidade de trabalho entregável sobrevive à entrega que a criou e vira um segundo trunk: acumula assuntos, envelhece e continua se apresentando como "o checkout daquele trabalho" para toda sessão que a lê.

Caso medido (projeto de origem, 2026-11-20): a branch `feature/R1-restante` era **ancestral** da `main` — 0 commits exclusivos, 3 commits atrás — e o worktree apontava para ela enquanto o checkout principal estava na `main`. Duas árvores se apresentavam como "o trabalho da R1"; a sessão leu `git status` repetidamente no checkout errado e relatou estado que não correspondia ao repositório (branch atrás, módulo "faltando").

O custo não é hipotético: é o preço de não saber qual checkout é o trabalho.

**Regra:** um nome de branch = uma unidade de trabalho entregável. Escopo pertence ao roadmap, não ao ref. Ao entregar, a branch é apagada no mesmo passo: `git branch -d` (recusa se não estiver integrada) e `git branch -D` só depois de provar que não há conteúdo exclusivo.

**Antes de ler estado, distinga trabalho de sombra:**

```bash
git rev-list --count <branch>..main   # >0 = a branch está atrás: sombra
git diff --name-status <branch> main  # vazio = nenhum arquivo exclusivo
git branch -vv                        # quem está em cada worktree
```

O `saude` do `quadro.sh` lista branches com conteúdo fora da `main` e as já publicadas que só faltam apagar; onde o projeto tem `worktrees.sh` + `docs/Worktrees.md`, o `ler` mostra também o registro de worktrees. Rode-o ao ler o quadro, em vez de confiar no `git status` do checkout em que você caiu.

## 2. `rm` atravessa symlink e apaga o alvo

O `node_modules` de um worktree costuma ser symlink para o do diretório principal. `rm -f "$WT/node_modules/pacote"` apaga o pacote da sessão vizinha. Antes de escrever fora do seu diretório: `readlink -f <caminho>`. Se sair da sua área, não é seu.

## 3. `npm install`/`update` num worktree materializa o `node_modules`

Substitui o symlink por diretório real, quebra links relativos internos e produz erros de tipagem que parecem do seu diff (caso de origem: 24 erros falsos). Instale no diretório principal.

## 4. O `HEAD` do diretório principal se move sem aviso

Entre criar a branch e commitar, outra sessão pode ter feito checkout no mesmo diretório. Caso de origem: o commit foi para `main` e a branch ficou vazia. Confirme `git branch --show-current` imediatamente antes de cada `git add`.

## 5. O index compartilhado tem trabalho alheio staged

Nunca `git add -A`/`git add .`. Adicione por nome; antes do commit confira `git diff --cached --stat` (o que vai) e `git diff` (o que falta). Para commitar um único arquivo sem levar o staged alheio: `git commit <caminho> -m ...`.

## 6. A pilha de stash é compartilhada

Ela é a mesma para todos os worktrees. `git stash pop` pode pegar o trabalho de outra sessão. Prefira commit WIP; se precisar, `git stash push -u -m <tag-unica>`, guarde o SHA, `git stash apply <sha>`, e `drop` pela referência achada pela tag.

## 7. Publicar na `main` do repositório de coordenação com o checkout principal sujo de outra sessão

Num repositório de coordenação sem remote, "merge" é mover `refs/heads/main`, e o diretório principal fica sempre com a `main` em checkout. Quando outra sessão deixou sujo, sem commitar, um arquivo que o seu merge também altera, `git merge` ali **recusa** — por arquivo sujo, não por conflito. As saídas óbvias são ruins: `--autostash`/`stash` mexem na pilha compartilhada (§6) e no trabalho alheio; esperar pode levar horas. Caso de origem: uma correção de 6 arquivos travada porque um deles tinha 14 linhas de edição alheia que nem encostavam no trecho do merge.

```bash
# 1. No SEU worktree: traga a main, valide, confira o que a main vai receber
git merge main
git diff --stat main HEAD           # só os seus arquivos; se aparecer outro, pare

# 2. No principal, pré-checagem (nada é alterado ainda)
git status --porcelain -- <seus arquivos limpos>     # vazio
git diff main NEW -- <arquivo sujo> > p.patch
git apply --check p.patch                            # o seu trecho entra por cima do alheio

# 3. Tudo num comando só, ENCADEADO com && — nunca conte com `set -e` para
#    proteger este passo (o porquê está no parágrafo abaixo do bloco)
git update-ref refs/heads/main NEW OLD &&   # CAS: recusa se a main andou
git checkout NEW -- <seus arquivos limpos> &&
git reset -q -- <arquivo sujo> &&           # index ← nova main
git apply p.patch                           # working copy = nova main + edição alheia

# 4. Prova
git diff --cached --quiet                 # nada staged no checkout dela
git diff --stat <arquivo sujo>            # igual ao de antes: só a edição alheia
```

**Por que `&&` e não `set -e`**: o `set -e` **não é contrato entre harnesses**. Ele é uma opção do shell, e o shell a ignora por especificação quando o comando roda dentro de `if`, de `&&`/`||`, de `while`/`until` ou de substituição de comando — exatamente as formas como um harness pode embrulhar o que você digitou. O resultado medido foi oposto nos dois lados: no Claude Code (2026-10-23) `set -e; false; echo x` **imprimiu `x`**; no OpenCode (2026-10-25) o mesmo comando **abortou com rc=1**, inline, via `bash -c`, num arquivo `.sh` e sob o `rtk`. Mesmo shell, contextos diferentes — porque quem decide é o contexto de execução, não a sua linha. O `&&` vale nos dois: o encadeamento é do próprio comando, não do shell que o hospeda. Não registre "o `set -e` não funciona aqui" como lição: a lição é que ele não é uma garantia portável.

**O passo 3 precisa ser completo**: o `update-ref` move a `main`, mas não toca no index nem nos arquivos. Sem `checkout`/`reset`/`apply`, o index fica com as versões **velhas** dos seus arquivos, e o próximo `git commit -a` da outra sessão **reverte o seu trabalho** sem conflito e sem aviso.

**Com a guarda da ref instalada** (`.githooks/reference-transaction`, perfil legado), o `update-ref` do passo 3 só passa se a `main` estiver avançando e a árvore nova passar nos gates de documentação; recusado, nada mudou — corrija na branch e repita. Se você usar `git merge` e ele for recusado, o git **já terá escrito** o conteúdo na árvore de trabalho do checkout principal (só a ref fica parada). Restaure só os arquivos que a recusa lista (`git restore --source=main --staged --worktree -- ...`), **nunca** com `reset --hard`, que apaga o trabalho não commitado das outras sessões.

**Antes de concluir que o arquivo sujo é trabalho de alguém**, confira que não é cópia velha esquecida: `git log --all --find-object=$(git hash-object <arquivo>)` vazio = conteúdo que não existe em commit nenhum, ou seja, trabalho real. Timestamps idênticos em vários arquivos indicam escrita em lote, não edição à mão. O `quadro.sh saude` acusa arquivo alterado no checkout principal que nenhuma entrada declara em "Paths sob edição".

## Regra prática

| Vou... | Confira com |
|---|---|
| criar worktree | `git fetch origin` e derivar de `origin/main` |
| saber qual checkout é o trabalho | `git rev-list --count <branch>..main` (0 = sombra) e `git branch -vv` |
| apagar/mover arquivo | `readlink -f` no caminho |
| instalar dependência | `ls -la node_modules \| head -1` |
| commitar | `git branch --show-current` e `git diff --cached --stat` |
| publicar na `main` com checkout sujo alheio | §7, encadeado com `&&` |
| propagar o mesmo arquivo para N repos | `md5sum` nos N |

## A lição maior

Um guardrail construído sobre diagnóstico não testado herda o erro do diagnóstico e o impõe a todos, com autoridade de ferramenta. Caso de origem: o aviso "branch atrás de main" nasceu como gate bloqueante sobre a crença (falsa) da reversão; reprovava trabalho legítimo e não pegava o caso real (1b). Virou aviso. Antes de transformar uma conclusão em gate, refute a conclusão.
