# Email Reading Fallback

## Overview

Use esta skill para padronizar leitura e busca de e-mails quando o agent precisar localizar mensagens, confirmar recebimento, investigar ausencia de e-mail esperado ou revisar comunicacoes recentes.

## Request Shapes

Use principalmente quando o pedido se parecer com:

- "veja se chegou um e-mail sobre isso"
- "procure esse e-mail na caixa de entrada"
- "confirme se recebemos a mensagem"
- "ache o e-mail com esse assunto, remetente ou contexto"

## Workflow

1. comece pela caixa principal e procure pelos sinais mais provaveis, como remetente, assunto, palavras-chave, periodo e contexto
2. se encontrar o e-mail procurado, leia o conteudo relevante e responda com base nele
3. se nao encontrar o que procura na caixa principal, verifique sempre a pasta de `spam`
4. se ainda nao encontrar, verifique sempre a pasta de `lixeira`
5. so conclua que o e-mail nao foi encontrado depois de checar caixa principal, spam e lixeira
6. se houver multiplos resultados parecidos, use assunto, remetente, data e contexto para identificar a mensagem mais provavel
7. nao exponha conteudo sensivel alem do necessario para responder ao pedido

## Output Contract

Ao concluir, informe de forma objetiva:

- se o e-mail foi encontrado ou nao
- em qual pasta ele estava, quando encontrado
- remetente, assunto e data quando isso for util
- resumo curto do conteudo relevante, sem expor informacao sensivel desnecessaria

## Quality Bar

- nunca conclua ausencia de e-mail sem checar spam e lixeira
- nao trate a caixa principal como unica fonte
- nao exponha dados sensiveis do e-mail sem necessidade
- prefira resposta objetiva e rastreavel sobre onde o e-mail foi localizado
