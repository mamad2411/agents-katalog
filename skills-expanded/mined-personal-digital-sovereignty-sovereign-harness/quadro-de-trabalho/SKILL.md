---
name: quadro-de-trabalho
description: Protocolo do quadro de trabalho multi-agente — o único lugar onde uma sessão enxerga a outra em tempo real. Ler e reservar antes de começar, manter a entrada viva durante, mover para o histórico ao terminar; caminho canônico único, commit só do quadro, timestamp medido. Carregar no início de QUALQUER tarefa não trivial, ao mudar de repositório/branch/escopo, ao terminar, e ao encontrar entrada órfã.
---

# Quadro de trabalho — quem está fazendo o quê, agora

Aplicar quando o projeto adota coordenação por quadro. Em repo de uma pessoa ou
sem fonte configurada, não impor quadro, helper ou metarrepositório. O helper Git
e seus gates abaixo pertencem ao perfil opcional github-rust-node; outro projeto
pode declarar outra fonte/processo. Não afirmar que um gate está ativo sem verificá-lo.

Regras de coexistência dizem para não atropelar a outra sessão, mas nenhuma mostra **onde ela está**. O quadro fecha esse buraco. Escrever nele custa 30 segundos; descobrir o conflito depois custa a rodada inteira.

## O caminho canônico é UM só

O quadro vive na branch principal, no diretório principal do repositório de coordenação (o caminho está em `[quadro].canonico` do `.harness.toml`). **Sempre esse caminho absoluto, mesmo dentro de um worktree**: cada worktree carrega uma cópia congelada do arquivo, e editar a cópia é escrever onde ninguém lê — e ainda gera conflito no merge. O guard do agente bloqueia a edição da cópia (`quadro-copia`).

É o único arquivo que se commita direto na branch principal, sem branch de agente: isolado numa branch, ele deixaria de existir para as outras sessões.

Use o helper:

```bash
quadro.sh ler                 # sempre a versão da branch principal, nunca a do disco
quadro.sh agora               # timestamp UTC
quadro.sh editar              # imprime o arquivo a editar — edite ESSE
quadro.sh commit "docs(quadro): <o que mudou>"
quadro.sh saude [--estrito]   # o que está fora da main e o que está parado
```

O `ler` termina com o relatório de `saude` em stderr (o quadro em stdout fica intacto): branches do repositório de coordenação com conteúdo fora da principal — separando as que só faltam apagar das órfãs sem entrada ativa — entradas de "Em andamento" sem data nova há mais de 3 dias, e arquivos alterados no checkout principal sem declaração em "Paths sob edição". Não bloqueia; trate o que for seu.

O `commit` usa `git commit <caminho>`, que leva só o quadro (o index costuma ter trabalho alheio staged). Com o diretório principal na branch de outra sessão, o helper commita por plumbing (`hash-object` + index temporário + `commit-tree` + `update-ref` com compare-and-swap), sem tocar no working tree dela, e recusa se a branch principal avançou desde a sua leitura.

## Os três momentos obrigatórios

1. **Antes**: leia o quadro inteiro. Se outra sessão já declarou o repositório, a branch ou — o que mais importa — os **paths** que você ia editar, não duplique: escolha outro item ou combine em "Notas entre agentes". Depois acrescente sua entrada em "Em andamento".
2. **Durante**: atualize ao mudar de repositório, criar branch ou crescer o escopo. Entrada parada com escopo desatualizado é pior que nenhuma: a vizinha decide com base nela.
3. **Ao terminar**: mova para "Concluído recentemente" com PRs e o que ficou aberto, e limpe as branches mergeadas (com prova por dois métodos). Entrega fechada vai para a branch principal no mesmo passo (skill `encerrar-documentacao`); a `saude` deve deixar de listar a sua branch.

## Formato da entrada

```markdown
### <agente>/<slug> — <título curto>
- **Início**: AAAA-MM-DD HH:MM (UTC) · **Última atualização**: AAAA-MM-DD HH:MM (UTC)
- **Repositórios**: ...
- **Branches**: `<agente>/<slug>` · **Worktrees**: ...
- **Demanda**: ...
- **Paths sob edição**: ...
- **Status**: em andamento | aguardando decisão do dono | em revisão | bloqueado
- **PRs**: ...
```

- **Timestamp sempre de `date -u '+%F %H:%M'`**, nunca de memória: timestamp errado faz a próxima sessão tratar trabalho vivo como órfão, ou o contrário.
- **Paths sob edição** é o campo de maior valor: a colisão aparece antes de os dois lados commitarem, o único momento em que ainda é barata.

## Entrada órfã

Timestamp velho, sem PR aberto, sessão sumida: verifique (`git branch -a`, lista de PRs, worktrees) e mova para "Interrompido" com o que achou. Nunca apague sem verificar.

## Guardas que já existem (e por quê)

- O pre-commit recusa commitar o quadro de um worktree, fora da branch principal, ou de carona com arquivos de outro assunto.
- E recusa commit que APAGA entrada sem readicioná-la (mover para "Concluído" readiciona o título). Caso de origem: um rascunho deixado por outra sessão horas antes subiu por cima da branch principal e apagou 46 linhas do quadro.
- `git merge` não dispara pre-commit: depois de merge que toque o diretório do quadro, confira as entradas (`grep -c '^### '`).
- No perfil legado, o pre-commit também recusa commit direto na branch principal que não seja só o quadro ou a conclusão de um merge; o `reference-transaction` recusa recuo e deleção da principal e árvore nova que reprove os verificadores de documentação, inclusive por `merge` e `update-ref`. Caso de origem: cinco publicações seguidas entraram por `update-ref` sem gate nenhum, e uma edição em lote não declarada de 3 skills ficou a um `commit -a` de entrar.
- A `saude` acusa arquivo alterado ou novo no checkout principal que nenhuma entrada de "Em andamento" declara em "Paths sob edição" — o git não impede escrita em disco. Se é seu, declare; se não é, não sobrescreva nem descarte sem dono.
