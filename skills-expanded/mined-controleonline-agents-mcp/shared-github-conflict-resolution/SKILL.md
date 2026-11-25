# Resolução de conflitos de integração

## Objetivo

Esta skill se aplica sempre que uma task, submódulo ou branch de integração
apresentar conflito, divergência ampla ou um diff que não possa ser revisado
semanticamente com segurança.

## Regra principal

Conflito não é autorização para escolher `ours`, `theirs`, fazer force-push ou
mesclar diretamente em `master`. Quando a task precisa ser refeita sem
`agent:security:accepted` e revalidacao do Manager, o estado operacional é
**Working**, respeitando o limite atual configurado para essa coluna no Project
#1; **In Review** continua reservado às tasks inventariadas em RC congelada que
chegou a staging.

Se em qualquer etapa o merge, rebase ou reaplicação ficar confuso a ponto de o
delta não poder ser revisado semanticamente com segurança, a preferência
obrigatória é apagar a branch descartável da task, recriá-la a partir do
`master` remoto atualizado e executar novamente a task desde os passos iniciais.
Não se deve preservar uma branch contaminada só porque o conflito pode ser
resolvido textualmente.

## Fluxo obrigatório

1. Pare antes do merge final e registre origem, destino, SHAs, merge-base,
   arquivos conflitantes e o requisito afetado.
2. Aborte o merge/rebase e preserve a evidência; não publique a branch
   conflitante em `dev`, `staging` ou `master`.
3. Para uma task que será refeita, retroceda o item no Notion/Project #1 para
   os passos iniciais do fluxo (no mínimo **Working**, ou a etapa inicial
   equivalente quando o board exigir), remova decisões/aceites/evidências que
   dependam da versão descartada e reative os validadores aplicáveis. Essa
   movimentação de recuperação é permitida e prevalece sobre a regra geral de
   não movimentar colunas; não use a proibição de higiene para deixar uma task
   descartada em `Done`, `Deploy` ou `In Review`.
4. Se a branch for aproveitável, atualize-a a partir de `origin/master`,
   resolva manualmente preservando as duas intenções e valide o diff final.
5. Se a branch estiver muito divergente, contaminada por commits de outras
   tasks, ou se a revisão semântica continuar confusa em qualquer passo,
   descarte a branch local e remota, registre os SHAs antigos e recrie
   `task-{id}` a partir de `origin/master`.
6. Reimplemente a correção do zero, sem copiar gitlink, sem herdar labels,
   evidências ou aceites, e execute novamente os testes do escopo.
7. Faça a entrega pelo caminho obrigatório de merge ou PR em `dev`, depois
   `staging` e finalmente `master`. Em submódulos, mescle primeiro o módulo e
   depois o pai com o pin do commit já integrado.
8. Antes de cada promoção, confira o diff semântico, requisitos negativos,
   submódulos, CI e estado da task. Só depois permita a próxima transição.

## Reinício deliberado da task

Apagar e recriar a branch não é falha de processo: é o caminho correto quando
a continuidade da branch aumenta o risco de misturar intenções. O reinício
pode ocorrer antes do primeiro merge, durante a correção de uma rejeição, na
preparação de `dev`, `staging` ou `master`, ou quando a evidência revelar que
a entrega anterior não é confiável. Depois do reinício, trate a task como uma
execução nova: nova base em `master`, novos commits, novos testes, novos SHAs,
novo merge e nova validação no Notion. Nunca herde labels, accepts, screenshots
ou status terminal da execução apagada.

## Critérios de segurança

- Um PR com `mergeable: false`, conflito ou CI incompleto não pode ser
  mesclado para contornar o bloqueio.
- A ausência de marcadores de conflito não prova que o resultado está correto;
  compare sempre `master`, merge-base, origem e o commit final.
- Force-push só pode ocorrer na branch descartável de task, após registro da
  evidência e com `--force-with-lease`; nunca em `master`, `dev` ou `staging`.
- `TESTADO:ALE` e quaisquer labels de validação não substituem revisão do
  resultado recriado e não podem ser herdadas automaticamente.
- Fora do reinício deliberado descrito acima, agents não movem tasks entre
  colunas. A passagem para `In Review` só ocorre para tasks presentes no
  manifesto da RC congelada publicada em staging; durante a recuperação, o
  retorno aos passos iniciais é a exceção autorizada e obrigatória.
