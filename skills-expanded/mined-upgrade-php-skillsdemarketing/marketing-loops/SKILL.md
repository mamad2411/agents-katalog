---
name: marketing-loops
description: "Quando o usuário quiser configurar um fluxo de trabalho de marketing recorrente e autônomo — um loop repetível que um agente de IA roda em uma cadência (semanal, diária, por gatilho) em vez de uma tarefa pontual. Use também quando o usuário mencionar 'loop de marketing,' 'fluxo de marketing recorrente,' 'automatizar meu marketing,' 'marketing no piloto automático,' 'revisão semanal de marketing,' 'checagem de fadiga de anúncio,' 'loop de atualização de conteúdo,' 'monitoramento de churn,' 'alerta de queda de ranking,' 'marketing sempre ativo,' 'fluxo de automação de marketing,' ou 'roda isso toda semana.' Use isso para escolher, adaptar, e agendar um loop de marketing contínuo que orquestra as outras skills de marketing. Para ideias de marketing pontuais, veja marketing-ideas. Para o loop de experimentação especificamente, veja ab-testing."
metadata:
  version: 1.2.0
---

# Loops de Marketing

Você ajuda a configurar **loops de marketing** — fluxos de trabalho de
marketing repetíveis que um agente de IA roda em uma cadência, cada um com
um gatilho definido, um conjunto delimitado de passos, uma autoverificação,
e uma condição de parada explícita. Um loop transforma uma tarefa de
marketing que você faria manualmente de outra forma (e esqueceria) em um
sistema sempre ativo: a varredura semanal de oportunidade de SEO, a
atualização de fadiga de anúncio, o monitoramento de sinal de churn.

Esse é o primo operacional do `marketing-ideas`. Ideias dizem *o que
tentar uma vez*. Loops dizem *o que continuar fazendo em uma agenda* — e
conectam as outras skills de marketing para fazer isso.

## Como usar esta skill

**Primeiro, verifique se há contexto de produto:** se
`.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o legado `product-marketing-context.md`), leia-o antes de fazer
perguntas. Use esse contexto e só pergunte o que estiver faltando.

Depois:

1. **Esclareça o trabalho.** Que resultado esse loop deve proteger ou
   crescer? (rankings, eficiência de anúncio, ativação, retenção, receita,
   indicação)
2. **Escolha um loop** do catálogo em `references/loop-catalog.md` — ou
   adapte o mais próximo.
3. **Ajuste a cadência** à velocidade real de mudança do sinal subjacente
   (veja a regra de cadência abaixo).
4. **Confirme o checkpoint humano.** Decida o que o loop faz autonomamente
   vs. o que ele deixa pronto para aprovação humana antes de publicar ou
   gastar — veja `references/loop-guardrails.md`.
5. **Agende-o** (veja "Agendando um loop" abaixo).

Construindo mais de um loop, ou um sistema operacional de marketing
inteiro? Veja `references/loop-orchestration.md` para como os loops se
compõem e a ordem para adotá-los (comece com tracking + uma revisão
semanal; não construa 43 de uma vez).

## Anatomia de um loop de marketing

Todo loop no catálogo tem essas nove partes. Ao autorar ou adaptar um,
preencha todas — um loop sem condição de parada, autoverificação, ou
tratamento de estado é um passivo, não um ativo.

| Parte | O que define |
|---|---|
| **Cadência de checagem** | Com que frequência o loop *olha* (semanal/diária/por gatilho). Combine com a velocidade do sinal. |
| **Age quando** | A condição de ação — o que precisa ser verdade para de fato *fazer* algo, vs. só checar e pular. A maioria das execuções de um bom loop é "checado, nada a fazer." |
| **Propósito** | O único resultado que esse loop existe para mover. |
| **Skills usadas** | Quais skills de marketing o loop orquestra a cada iteração. |
| **Corpo do loop** | Os passos ordenados executados a cada iteração. |
| **Autoverificação** | A verificação feita *antes* de agir — para que o loop não aja sobre ruído, sazonalidade, ou um bug de tracking. |
| **Estado/idempotência** | O que o loop lembra entre execuções: marcador de última execução, chave de dedupe, janela de cooldown, conjunto "já tratado." Sem isso, loops agem em dobro, incomodam de novo as mesmas pessoas, ou alertam de novo a mesma coisa. Não-negociável para qualquer coisa agendada — veja `references/loop-state.md` para onde o estado vive e os padrões de idempotência. |
| **Parada/saída de emergência** | Quando o loop pula, para, escala para um humano, ou se desativa — mais o que faz em caso de erro. Todo loop precisa de um, incluindo loops de heartbeat (a parada deles é "desativação manual + parada em erro," nunca "n/a"). |
| **Saída** | Para onde os resultados vão: um arquivo, um PR, um rascunho preparado, uma notificação, um relatório. |

A divisão **Cadência de checagem / Age quando** importa: um loop de sinal
de churn pode *checar* diariamente mas só *agir* quando uma conta cruza um
limiar de risco com o qual ainda não foi contatada dentro da janela de
cooldown. Confundir os dois produz loops que ou perdem a janela ou
incomodam demais.

## A regra de cadência

Combine a cadência com a velocidade real de mudança do sinal — não com a
frequência que você *gostaria* de uma atualização.

| Sinal | Cadência realista | Por quê |
|---|---|---|
| Rankings, backlinks, autoridade de domínio | Semanal | Mudam devagar; checagens diárias são ruído |
| Fadiga de criativo de anúncio, deriva de CPA | A cada 2-3 dias | Os loops de feedback de Meta/Google são de dias, não horas |
| Funil de ativação/onboarding | Semanal | Precisa de cadastros suficientes para ser significativo |
| Sinais de churn | Diário ou por gatilho | A janela de intervenção precoce é curta |
| Decaimento de conteúdo/copy | Mensal | A erosão de tráfego é gradual |
| Mudanças de concorrente | Semanal | Mudanças de preço/posicionamento são infrequentes mas importam |
| Escuta social/menções | Diário | Janelas de engajamento fecham rápido |

Loops frequentes demais são o modo de falha mais comum: geram trabalho
inútil, queimam orçamento, e te treinam a ignorar a saída.

## Quando NÃO fazer um loop

Nem tudo deveria ser automatizado em cadência. Pule um loop — ou adicione
um checkpoint humano obrigatório — quando:

- **Estratégia ou direção criativa é o trabalho de verdade.** Loops
  mantêm e otimizam; não definem posicionamento, não inventam campanha,
  nem tomam decisão de marca.
- **A ação publica ou gasta sem revisão.** Auto-*rascunhar* um anúncio,
  e-mail, ou post é ok. Auto-*publicar* ou auto-*mudar orçamento* precisa
  de um checkpoint humano, a menos que o usuário tenha autorizado
  explicitamente ação autônoma e definido guardrails (tetos, listas
  permitidas).
- **O sinal é ralo demais para ser significativo.** Um loop semanal de
  taxa de conversão com 40 visitantes/semana está medindo ruído.
- **É um loop de vaidade.** Se ninguém age sobre a saída, apague o loop.
  Um loop que manda por e-mail um dashboard que ninguém lê é pior que
  nada.

Para qualquer loop que envia, gasta, publica, ou toca dado pessoal,
aplique `references/loop-guardrails.md` — o modelo de ação em duas
camadas (seguro-autônomo vs. travado), tetos de gasto/envio, regras de
CAN-SPAM/LGPD/FTC/ToS, a lista sempre-escale, e um kill switch
obrigatório.

## Agendando um loop

Esses loops são agnósticos de agente: o *corpo* funciona em qualquer
agente. O *agendamento* depende do seu ambiente:

- **Claude Code** — opções nativas: `/loop` (ritmo próprio, até uma
  condição), `ScheduleWakeup` (ritmo dinâmico que reage ao estado), e
  `CronCreate` (agenda cron fixa). Se você tem uma skill de mecânica de
  loop como `loopify` instalada, use-a para escolher entre elas e ajustar
  os atrasos; senão a orientação abaixo já basta.
- **Qualquer agente + cron** — embrulhe o corpo do loop como um
  prompt/script agendado (`0 9 * * 1` para segundas 9h, etc.).
- **Cadência manual** — para loops de alto julgamento, "roda essa skill
  toda segunda" é um loop perfeitamente bom. O valor está no *corpo*
  repetível, não na automação.

Padrão para cron de horário fixo para loops de estilo revisão (revisão
semanal, monitoramento de ranking) e ritmo dinâmico para loops de
monitorar-até-limiar (monitoramento de churn, tracking de dia de
lançamento).

## O catálogo

`references/loop-catalog.md` guarda a biblioteca completa — 43 loops de
marketing com cobertura completa de funil: SEO & Conteúdo, Pago, Ganho/
Social/Parceria, Ativação, Retenção, Receita, Indicação & Defesa, e
Operações Contínuas. Cada um é uma especificação completa e adaptável.
Comece por lá, escolha o mais próximo, e ajuste ao produto, estágio, e
ferramental do usuário.

## Autorando um loop novo

Quando nada no catálogo encaixa, autore um loop novo a partir de
`references/loop-template.md` — um template de copiar-colar com prompts
de preenchimento, um exemplo resolvido de antes/depois, e um checklist de
lançamento. Preencha as nove partes da anatomia; se você não conseguir
responder a autoverificação, o estado/idempotência, e a parada/saída de
emergência concretamente, o loop não está pronto para rodar.

## Antipadrões

- Fazer loop sem condição de parada → gasto descontrolado ou churn
  infinito.
- Mesma cadência para todo loop → a maioria roda com frequência demais e
  é ignorada.
- Sem autoverificação → o loop age sobre ruído, sazonalidade, ou um bug de
  tracking.
- Sem checkpoint humano em ações de gasto/publicação.
- Construir 10 loops de uma vez → comece com um, prove que ele vale a
  pena, depois adicione o próximo.

## Vocabulário banido

Evite: "configure e esqueça," "marketing totalmente autônomo," "a IA faz
tudo," "10x no piloto automático," "máquina de growth hacking." Loops são
sistemas disciplinados com checkpoints, não mágica. Descreva-os
honestamente.

## Skills relacionadas

- **marketing-ideas** — táticas e inspiração pontuais (o que tentar). Loops operacionalizam as que valem a pena repetir.
- **ab-testing** — o loop de experimentação especificamente (hipótese → teste → promover o vencedor → repetir).
- **analytics** — a maioria dos loops lê do analytics para decidir se age.
- Skills de canal individuais (`ads`, `seo-audit`, `emails`, `social`, `churn-prevention`, `pricing`, `referrals`) — os corpos de loop orquestram essas.
