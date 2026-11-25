---
name: grilling
description: >-
  Interroga o usuário sobre um plano até fechar cada ramo de decisão antes de
  codar. Acione em implementação GRANDE (multi-sistema, schema/auth/infra,
  irreversível); não em tarefa pequena e vaga. Também em "me interroga",
  "fecha o plano".
---

# Grilling — interrogatório de plano

Transforma "instruções vagas → pergunte" (regra passiva) num loop ativo que
**não deixa começar** enquanto houver ramo de decisão em aberto. É o Target Lock
levado a sério.

## Antes de começar: projeto com `.context/`?

Se o projeto tem `.context/` e o plano toca regra de negócio, automação
(n8n/Pipedrive) ou dado sensível, **ancore o loop na doc**:

1. **Leia antes de perguntar:** `AGENTS.md` da raiz, `.context/docs/` e a memória
   do projeto. Não pergunte o que a doc já responde; traga como fato.
2. **Respeite estado intencional.** Nó n8n desabilitado, flag, decisão de negócio
   registrada no projeto: não desfaça sem autorização explícita. Acordo verbal não
   basta; vale o que está escrito no `AGENTS.md` ou no `.context/`.

## O loop

Interrogue o usuário até chegarem a entendimento compartilhado sobre cada
decisão que muda o que vai ser tocado (arquivo, tabela, endpoint,
comportamento), resolvendo as dependências entre elas uma a uma. Ramo que não
muda isso não vira pergunta: o limite é o de "Quando parar".

Regras do loop:

1. **Uma pergunta por vez — a não ser que sejam independentes.** A dependência é
   o critério, não a quantidade: pergunta cuja resposta muda a próxima (ou muda
   se a próxima faz sentido) vai **sozinha** e espera. Perguntas do mesmo nível
   da árvore, em que nenhuma resposta altera as outras, podem ir juntas numa
   **rodada de até 3** — pelo `AskUserQuestion`, uma por bloco, cada uma com sua
   recomendação. Na dúvida, é dependente: vai sozinha.

   A diferença nem sempre é óbvia. "Que banco usar?" vai **sozinha**: a resposta
   muda o que faz sentido perguntar depois (tabela, permissão, migração). As
   três do parágrafo abaixo cabem numa rodada porque nenhuma resposta mexe nas
   outras.

   O que a rodada resolve é o vaivém de sete mensagens para fechar coisas
   ortogonais (nome da tabela, quem pode ler, o que acontece no erro). O que ela
   **não** pode virar é despejo de perguntas: três é teto, não meta, e uma rodada
   com pergunta dependente dentro devolve resposta que o usuário vai querer
   mudar depois — pior que o vaivém.
2. **Para cada pergunta, dê a sua recomendação.** Nunca pergunte "aberto" —
   pergunte com um default proposto ("eu faria X porque Y — concorda?").
3. **Fato → busque; decisão → pergunte.** Se dá pra descobrir explorando o
   código (qual arquivo de rota, que tipo, existe tal função), NÃO pergunte:
   faça grep/read e traga o fato. As *decisões* são do usuário — ponha cada
   uma e espere a resposta.
4. **Não execute o plano até o usuário confirmar** que chegaram a
   entendimento compartilhado.

## Quando parar

Pare de interrogar quando não restar ramo de decisão que mude o que você vai
tocar (arquivo, tabela, endpoint, comportamento). Aí feche com o plano em
passos curtos, cada um com o check que o prova: o comando, o teste que falha
antes e passa depois, ou o comportamento que se observa (na tela, no log, no
banco). Passo sem check está vago demais; quebre até ter um. Peça "go".

O plano fechado leva três coisas além dos passos:

- **Premissas com recibo.** Todo fato em que o plano se apoia (a função existe,
  a coluna tem esse tipo, a rota já checa sessão, o número de linhas) vem com o
  `arquivo:linha` ou o comando que o mostrou agora. Premissa sem recibo volta a
  ser busca; se a busca não resolve, vira pergunta.
- **Foco do review: até 5 entradas ou modos de falha** que as decisões implicam
  e nenhum passo testa (lista vazia, valor duplicado, usuário sem permissão,
  chamada repetida, campo nulo). Cada um vira um teste no passo que toca aquele
  código. É o input que ninguém nomeou que passa por todos os gates.
- **Decisão, não código.** Cada passo diz o arquivo, a assinatura, os valores
  combinados, as asserções do teste e o comando com a saída esperada. Corpo de
  código só entra para um algoritmo que isso não determina. Plano várias vezes
  maior que o pedido virou transcrição: troque os corpos por assinatura e teste.

Fechado o entendimento, grave cada decisão no lugar dela: regra dura do projeto →
`AGENTS.md` da raiz (o `CLAUDE.md` do projeto só importa `@AGENTS.md`); decisão e
conhecimento do projeto → `.context/docs/`; fato durável → memória. O histórico da
conversa não vai para o `AGENTS.md`: ele cresce com regra, não com changelog.

## Modo EXECUTE (atalho)

Se o usuário responder "sim/faz/manda" a um plano já claro, NÃO reabra o
grilling — execute. O grilling é pra quando há ambiguidade real, não pra
carimbar decisão já tomada.
