# Contrato de entrega verificável

Este contrato vale para Manager, Developer, DevOps e validadores. Comentário,
diagnóstico, plano, handoff textual ou mudança local não são entrega.

## O que conta como mutação real

Toda rodada que declare `DONE` precisa produzir e comprovar uma mutação
compatível com a prioridade:

- **Código:** commit novo publicado em uma ref remota, merge da task no destino
  previsto e verificação do SHA remoto.
- **Teste automatizado:** o arquivo de teste e seu runner devem estar
  versionados no commit e integrados na ref remota prevista. Screenshot, PNG,
  vídeo, trace, relatório, manifesto ou índice gerado são evidência opcional ou
  específica de aceite visual; nunca substituem o teste automatizado nem
  constituem sozinhos a entrega da task.
- **Validação:** decisão nova (`agent:<papel>:accepted` ou
  `agent:<papel>:rejected`), remoção da solicitação anterior e coluna coerente.
- **DevOps/board:** merge ou promoção da task individual e mudança confirmada
  de coluna/labels.
- **Governança (`agents-mcp`):** commit publicado no `agents-mcp`, issue
  associada ao Project #1 e estado/coluna atualizados. Esta é uma entrega
  direta: não aguarda QA, Security, Design, UX ou aprovação humana.

Um comentário só pode acompanhar a mutação. Nunca pode substituí-la.

## Nova entrega somente em `dev`: reset obrigatório de validação

Após reconstrução ou correção, se os novos SHAs chegaram somente em `dev`, o
estado obrigatório é **`Working`**. O Manager deve remover as labels históricas
`agent:*:accepted` e `agent:*:rejected` da entrega anterior e reativar as
solicitações aplicáveis `agent:qa`, `agent:security`, `agent:design` e
`agent:ux`. Os validadores devem decidir novamente sobre os SHAs novos.

`In Review` só é coerente depois de merge da task individual em `staging` e
dos quatro novos aceites. Aceites antigos não autorizam `In Review` nem
substituem a nova validação.

## Fechamento obrigatório

Antes de emitir `DONE`, registre na issue a ação executada, SHA(s)/ref(s)
remotos ou IDs das labels/coluna, verificação pós-ação e próximo papel/coluna.
Se qualquer item faltar, o resultado não é `DONE`.

Para governança do próprio `agents-mcp`, o fechamento ocorre após a publicação
remota do commit e a atualização verificável da issue/board. Não se cria
handoff para validadores e não se mantém a issue em `Working` aguardando
aprovação.

## Bloqueio operacional

Quando uma dependência impedir a ação:

1. tente a correção objetiva disponível (permissão, conflito, credencial,
   checkout, runtime ou API);
2. repita a verificação somente depois da correção;
3. se a dependência continuar impedindo o avanço, registre `NEXT_ACTION` com
   responsável, tentativa, evidência e ação externa necessária; não crie,
   aplique ou solicite a tag `agent:*:blocked` do GitHub e não mova a issue do
   Project #1 para `Blocked`.

Este limite aplica-se ao **GitHub Project #1**: `Blocked`/`Backlog` sao estados
de board sob controle humano; nenhum agent, worker ou automacao pode comentar,
validar, rotular, editar ou mover issues nessas colunas. O status `blocked` no
Paperclip e uma fila operacional separada de recuperacao: Manager/CTO devem
prioriza-la, diagnosticar e retomar/corrigir a task/execucao Paperclip com
readback. Isso nao autoriza mutar a issue/board GitHub caso ela tambem esteja
em `Blocked`.

## Anti-repetição

Uma nova rodada não pode selecionar a mesma issue quando o estado de entrada é
igual ao da última tentativa: mesmos SHAs, labels, coluna e evidência. Exige-se
um novo delta publicado ou uma mudança externa verificável. Sem isso, registre
`NEXT_ACTION`; não publique outro comentário, não repita o handoff e não
aplique tag ou estado de bloqueio.

O comentário de encerramento deve conter:
`DELIVERY_PROOF: action=<...> refs=<...> state=<...>`.
