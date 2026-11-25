# Operational Security Guardrails

## Overview

Use esta skill quando o trabalho envolver dados sensiveis, credenciais, segredos, logs, ambientes operacionais, mudancas potencialmente destrutivas ou decisoes com risco de seguranca.

## Request Shapes

Use principalmente quando o pedido se parecer com:

- "investigue o incidente"
- "analise logs e ambiente com seguranca"
- "corrija o problema sem expor credenciais"

## Workflow

1. trate segredos, tokens, senhas, chaves, arquivos de ambiente e credenciais como informacao estritamente sensivel
2. nunca exponha valores sensiveis em respostas, resumos, issues, comentarios, registros ou saidas visiveis
3. nunca copie conteudo sensivel quando bastar referencia indireta ou descricao sanitizada
4. evite acoes destrutivas, irreversiveis ou de alto impacto sem necessidade operacional clara e evidencia forte
5. nao altere configuracoes sensiveis de acesso, firewall, permissoes, usuarios, chaves ou politicas sem base operacional solida
6. nao invente estados, credenciais, hosts, tabelas, resultados ou evidencias
7. se faltarem dados para agir com seguranca, registre a limitacao e pare no ponto seguro
8. quando nao houver outra superficie de escrita viavel, a chave do GitHub anexada a sessao pode ser usada como fallback operacional para mudancas autorizadas pelo usuario
9. ao usar essa chave, limite o uso ao escopo minimo necessario, prefira injecao temporaria em memoria ou ambiente de execucao e preserve rastreabilidade da acao sem revelar o segredo
10. nunca publique, versione, cole, ecoe ou replique essa chave em arquivo persistente, commit, issue, comentario, log ou resposta visivel

## Output Contract

Ao concluir, entregue um resumo curto com:

- risco ou cuidado principal observado
- acao segura executada ou explicitamente evitada
- limitacoes ou riscos residuais
- registro de que informacoes sensiveis foram preservadas

## Quality Bar

- nunca exponha segredos
- nunca normalize acoes inseguras por conveniencia
- nunca use evidencia fraca para justificar mudanca arriscada
- sempre preserve confidencialidade, integridade e rastreabilidade
- nunca trate a permissao de uso da chave anexada como autorizacao para divulgar o valor da credencial
