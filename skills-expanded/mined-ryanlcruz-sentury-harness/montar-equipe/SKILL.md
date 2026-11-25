---
name: montar-equipe
# Como a skill aparece na lista do "o que sei fazer".
vitrine:
  grupo: 'Trabalho'
  rotulo: 'montar uma equipe de residentes'
description: "Montar residentes que trabalham juntos: papéis que não se sobrepõem, cada um com o que defende e o que não é com ele, vozes diferentes que debatem de verdade na Mesa, ferramentas mínimas e a pessoa aprovando antes de criar."
version: 1.0.0
author: Sentury
license: MIT
metadata:
  # Só frase que pede gente nova; "agente" sozinho roubaria pedidos de tarefa comum.
  gatilhos:
    - '(mont|cri|form)\w* (uma |um |a |o )?(equipe|time|squad)'
    - '(cri|mont)\w* (os |uns |alguns |novos? )?(residentes|colegas)'
    - '(cri|mont)\w* (um |uns |alguns |novos? )?agentes? (residentes?|que (cuide|acompanhe|trabalhe))'
    - 'quero (uma |um )?(equipe|time) (de|para|pra)'
    # Acrescentar alguém a uma equipe que já existe também é montar a equipe.
    - '(complet|refor[cç]|aument)\w* (a |o )?(equipe|time)'
    - '(mais um|outro|novo|quinto|sexto|s[eé]timo) (residente|colega|agente)\b'
  category: cognitive
---

# Montar uma equipe de residentes

Residente é um colega que continua existindo: tem fila, memória, orçamento e
participa da Mesa. Uma equipe boa não é a soma de bons residentes; é um grupo em
que cada um enxerga uma parte que os outros não enxergam, e por isso discorda
deles no momento certo. Esta skill é o caminho para chegar nela, do pedido ao
cartão que a pessoa aprova.

## 1. Entender o trabalho antes de pensar em papéis

Pergunte a si mesmo, a partir do que a pessoa disse, o que essa equipe entrega e
para quem. "Ajudar o time de CX" ainda não é trabalho; "achar as causas de
contato repetido e propor correções com custo e prazo" é. Se o pedido não deixa
isso claro, pergunte uma vez com `perguntar_usuario`, com duas ou três opções do
que a equipe poderia entregar. Não pergunte o que dá para decidir sozinho, como
nomes, aparência e quantidade de residentes.

Antes de criar alguém novo, veja quem já existe com `pedir_ao_agente` e
`acao: listar`. Um residente que já cobre a parte entra na equipe como está;
dois com o mesmo papel se confundem na Mesa e dividem o orçamento à toa.

## 2. Papéis que não se sobrepõem

Entre três e cinco residentes. Com dois, a Mesa vira conversa a dois e quase
não há o que mediar; acima de cinco, cada rodada fica longa e cara, e alguém
sempre repete o outro.

Para cada um, defina três coisas, e escreva-as no manifesto:

| campo | o que diz | exemplo |
|---|---|---|
| `papel` | o que ele é, numa linha | analista financeira do time de CX |
| `objetivo` | o que ele persegue, de um jeito que dá para verificar | toda melhoria proposta tem custo, retorno e folga calculados |
| `instrucoes` | o que não é com ele, e para quem vai | cronograma é do Tito e texto ao cliente é da Vera; ela pede a eles |

O "não é com ele" evita o defeito mais comum de equipe montada às pressas: todos
opinando sobre tudo. Se você não consegue dizer o que um residente recusa, o
papel dele ainda está largo demais.

Um deles conduz. Quem conduz abre as conversas, media a rodada da Mesa quando
há divergência e fecha com a decisão e os próximos passos. Dê a ele um papel de
coordenação e diga isso nas `instrucoes` dele.

## 3. Vozes que discordam por motivos reais

A Mesa só debate de verdade quando os residentes otimizam coisas diferentes.
Se todos querem "o melhor para o cliente", todos concordam, e a conversa vira
uma fila de "concordo". Escolha para cada papel o que ele defende quando há
escolha difícil:

- um defende a velocidade e o outro, a segurança;
- um defende o cliente e o outro, o custo;
- um quer o diagnóstico completo antes de agir e o outro, um teste pequeno já.

A `personalidade` diz isso em duas ou três frases, até 400 caracteres: o jeito
de falar, a convicção do ofício e como ele reage quando discordam dele. Por
exemplo: "Desconfia de número solto: pede a fonte e refaz a conta. Fala curto e
direto. Quando discordam dela, mostra a conta em vez de repetir a opinião."
Evite três adjetivos genéricos ("organizado, proativo, colaborativo"): eles
servem para qualquer um e produzem falas iguais.

Faça as quatro vozes diferentes entre si, e diferentes dos residentes que já
existem. Discordância encenada não ajuda; o contraste vem do que cada um
defende, não de ordem para brigar.

## 4. Ferramentas, skills e limites mínimos

`ferramentas` é a lista inteira do que ele pode usar, e nada fora dela. Comece
pelo que o trabalho pede de fato: quem só analisa e escreve não precisa de
navegador; quem pesquisa na web precisa de `rede: internet`. Ferramenta que
faltar ele pede depois com `pedir_ferramenta`, e a pessoa aprova na hora. É mais
seguro começar curto do que tirar depois.

Se uma skill instalada descreve o trabalho de alguém, ponha em `skills`: ela
entra carregada em toda tarefa dele.

`orcamento` e `cerebro` só quando a pessoa falar deles. O padrão é US$ 1 e 60
turnos por dia, e a Mesa consome turnos de todos os participantes: uma equipe
que vai conversar muito pode precisar de mais turnos, e isso vale dizer à
pessoa em uma frase, sem decidir por ela.

`familia` sai do papel e escolhe a coruja. `nome` é de colega, curto e próprio,
escolhido por você quando a pessoa não der um, e diferente dos que já existem.

## 5. Propor tudo junto e esperar a aprovação

Chame `criar_agente` uma vez com a equipe inteira: o primeiro residente nos
campos de cima e os outros em `colegas`, cada um com o manifesto completo. A
pessoa vê a equipe num cartão só, lê cada manifesto e escolhe quem entra. Uma
chamada por residente para o turno no primeiro cartão, e ela aprovaria um de cada
vez. Criar é propor; nada existe até ela aprovar.

Na resposta, em poucas linhas, diga por que essa composição: o que cada um
defende e onde você espera que eles discordem. É isso que ajuda a pessoa a
decidir se falta alguém ou se alguém sobra.

## 6. Depois de criados

Se a pessoa pediu um primeiro trabalho, abra um assunto na Mesa com todos e com
quem conduz chamado primeiro, ou peça a cada um a sua parte com
`pedir_ao_agente`, quando as partes forem independentes. A Mesa é para decidir
junto; trabalho que cada um faz sozinho vai direto para a fila dele, e eles
trabalham ao mesmo tempo.

## O que evitar

- Um residente para cada verbo do pedido ("um busca, um lê, um resume"): isso é
  um passo de tarefa, não um colega.
- Papéis que mudam só no nome ("analista de dados" e "analista de métricas").
- Personalidade que descreve competência ("experiente, eficiente") em vez de
  jeito de falar e de discordar.
- Criar sem mostrar: o cartão existe para a pessoa ver a equipe inteira antes.
