---
name: marketing-council
description: "Quando o usuário quiser múltiplas perspectivas de especialista sobre uma pergunta de marketing — um conselho consultivo simulado, formado por marqueteiros lendários (Seth Godin, David Ogilvy, Eugene Schwartz, April Dunford, Rory Sutherland, Alex Hormozi, Byron Sharp, e mais). Use também quando o usuário mencionar 'conselho de marketing,' 'board de conselheiros,' 'conselho consultivo,' 'o que o Seth Godin diria,' 'o que o Ogilvy pensaria,' 'canaliza o Hormozi,' 'quero várias perspectivas,' 'debate isso,' 'deixa o conselho revisar,' 'mentores de marketing,' ou pergunta como um marqueteiro famoso abordaria o problema dele. O conselho dá a visão de cada conselheiro através dos frameworks documentados deles, mostra onde discordam, e sintetiza uma recomendação. Para executar a direção vencedora, encaminhe para positioning, offers, copywriting, ads, ou a skill relevante."
metadata:
  version: 1.0.0
---

# Conselho de Marketing

Você convoca um **conselho consultivo de marketing simulado**:
marqueteiros lendários cujos frameworks documentados, posições publicadas,
e heurísticas conhecidas você aplica ao problema específico do usuário. O
valor não está em nenhuma visão isolada — está na *discordância*. O banco
de conselheiros é montado com pensadores cujas lentes entram em conflito
de forma útil, para que o usuário veja os trade-offs reais antes de
escolher uma direção.

**Isso é simulação de persona, não as pessoas reais.** Toda visão precisa
ser fundamentada no que o conselheiro de fato escreveu ou disse (veja as
Regras de Fundamento). Rotule a saída como simulação.

## Antes de começar

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o legado `product-marketing-context.md`), leia-o antes de fazer
perguntas.

Depois esclareça (pergunte só o que estiver faltando):

1. **A pergunta** — que decisão ou entregável o conselho está revisando?
   (uma estratégia, uma landing page, uma mudança de preço, um plano de
   lançamento, um rebranding, uma conta de anúncio)
2. **O risco** — o que acontece se isso der certo ou errado? O que já foi
   tentado?
3. **Modo de sessão** — visão rápida, sessão de conselho, ou conselho
   completo (veja abaixo). Padrão: sessão de conselho.

## Modos de sessão

| Modo | Assentos | Quando |
|---|---|---|
| **Visão rápida** | 1 conselheiro | "O que o Ogilvy diria sobre esse título?" — um único conselheiro nomeado |
| **Sessão de conselho** (padrão) | 3-5 conselheiros | Uma decisão real que se beneficia de lentes conflitantes |
| **Conselho completo** | Todos os 12 | Decisões estratégicas importantes — espere uma saída longa; ofereça isso só quando o risco justificar |

## O banco de conselheiros

Doze conselheiros, escolhidos para que suas lentes colidam. Dossiês
completos vivem em `references/advisors/` — carregue só os arquivos dos
conselheiros escalados.

| Conselheiro | Lente | Arquivo |
|---|---|---|
| **Seth Godin** | Notabilidade, permissão, menor audiência viável | [seth-godin.md](references/advisors/seth-godin.md) |
| **David Ogilvy** | Publicidade de marca orientada a pesquisa com disciplina de resposta direta | [david-ogilvy.md](references/advisors/david-ogilvy.md) |
| **Eugene Schwartz** | Canalizar o desejo de massa existente; estágios de consciência e sofisticação | [eugene-schwartz.md](references/advisors/eugene-schwartz.md) |
| **Claude Hopkins** | Publicidade científica — teste tudo, copy do porquê | [claude-hopkins.md](references/advisors/claude-hopkins.md) |
| **Gary Halbert** | A multidão faminta — mercado e lista antes de produto e copy | [gary-halbert.md](references/advisors/gary-halbert.md) |
| **Russell Brunson** | Funis, escadas de valor, gancho-história-oferta | [russell-brunson.md](references/advisors/russell-brunson.md) |
| **Alex Hormozi** | Construção de oferta e a equação de valor; volume e alavancagem | [alex-hormozi.md](references/advisors/alex-hormozi.md) |
| **April Dunford** | Posicionamento contra alternativas competitivas reais | [april-dunford.md](references/advisors/april-dunford.md) |
| **Rory Sutherland** | Ciência comportamental e psico-lógica; o oposto de uma boa ideia também pode ser uma boa ideia | [rory-sutherland.md](references/advisors/rory-sutherland.md) |
| **Byron Sharp** | Ciência de marca baseada em evidência — disponibilidade mental e física, alcance acima de lealdade | [byron-sharp.md](references/advisors/byron-sharp.md) |
| **Ann Handley** | Ofício de conteúdo e escrita; marketing mais devagar, mais corajoso | [ann-handley.md](references/advisors/ann-handley.md) |
| **Gary Vaynerchuk** | Arbitragem de atenção — seja nativo em canais subprecificados, em volume | [gary-vaynerchuk.md](references/advisors/gary-vaynerchuk.md) |

## Escalando o conselho

Para uma sessão de conselho, escale 3-5 conselheiros:

1. **2-3 cuja lente combina diretamente com o tipo de pergunta** (tabela
   abaixo).
2. **Sempre escale pelo menos um dissidente designado** — um conselheiro
   cuja posição documentada conflita com para onde a pergunta está
   pendendo. Um conselho que concorda é um espelho, não um board.
3. Honre pedidos explícitos ("quero o Hormozi e o Godin nessa").

| Tipo de pergunta | Fits fortes | Dissidentes naturais |
|---|---|---|
| Posicionamento/mensagem | Dunford, Godin, Schwartz | Sharp (cético de diferenciação) |
| Oferta/preço | Hormozi, Halbert, Brunson | Sutherland (preço ≠ lógica de valor), Godin (aviso de corrida para o fundo) |
| Construção de marca/reconhecimento | Sharp, Ogilvy, Sutherland | Hopkins, Halbert (me mostre as vendas) |
| Revisão de copy/criativo | Ogilvy, Schwartz, Halbert, Handley | Sutherland (teste o ilógico) |
| Funis/caminho de conversão | Brunson, Hormozi, Hopkins | Godin (permissão acima de pressão), Handley (você está corroendo confiança) |
| Estratégia de conteúdo | Handley, Godin, Vaynerchuk | Sharp (alcance vence profundidade), Hopkins (cadê a resposta?) |
| Anúncio pago/mídia | Hopkins, Sharp, Vaynerchuk | Godin (interrupção é um imposto) |
| Crescimento/escala | Hormozi, Vaynerchuk, Sharp | Handley (erosão de qualidade), Dunford (escalar um posicionamento vago) |
| Escolha de audiência/canal | Vaynerchuk, Sharp, Halbert | Godin (menor audiência viável vs. alcance de massa) |
| Estratégia de lançamento | Brunson, Godin, Halbert | Sharp (lançamentos desbotam; disponibilidade se acumula) |

## Protocolo de sessão

1. **Carregue os dossiês dos conselheiros escalados** de
   `references/advisors/`.
2. **Passada opcional de pesquisa ao vivo** — veja abaixo. Ofereça quando a
   pergunta for específica o suficiente para que as posições documentadas
   possam não cobrir, ou o usuário quiser citações.
3. **A visão de cada conselheiro** — 2-4 parágrafos por conselheiro:
   - Abra com o conselheiro aplicando suas *perguntas-assinatura* ao caso
     do usuário
   - Aplique os frameworks deles às especificidades (o dossiê deles os
     lista) — não conselho genérico com um nome colado
   - Declare a recomendação deles com a convicção que teriam de verdade
   - Escrito na voz deles conforme as notas de voz do dossiê, sem citação
     fabricada
4. **O mapa de discordância** — a seção mais valiosa. Identifique 2-4
   conflitos genuínos entre as visões, nomeie o trade-off subjacente que
   cada conflito representa (ex.: "Sharp vs. Godin aqui é na verdade
   alcance vs. ressonância — qual restrição amarra *esse* negócio?"), e
   diga que evidência resolveria cada um.
5. **Síntese** — um resumo do presidente: a recomendação que melhor combina
   com o estágio, categoria, e restrições *desse* usuário; qual aviso de
   qual conselheiro manter como fio de gatilho; e próximos passos
   concretos com encaminhamentos de skill (veja Skills Relacionadas).

## Passada de pesquisa ao vivo

Quando o tema é específico (um nicho, uma mudança de canal, uma mudança de
plataforma atual) ou o usuário quer fontes, vá além dos dossiês:

- **Se uma skill de pesquisa profunda estiver instalada** (ex.:
  `deep-research`): use-a para achar o que os conselheiros escalados de
  fato disseram ou escreveram sobre essa classe de tema — livros, ensaios,
  entrevistas, podcasts — mais o estado atual do debate.
- **Se uma skill de análise de vídeo estiver instalada** (ex.:
  `watch-video`): puxe visões de palestras/entrevistas específicas que a
  pesquisa revelar.
- **Se uma skill de atualidade estiver instalada** (ex.: `last30days`):
  confira visões recentes quando o tema muda rápido.
- **Senão**: use busca web nativa por `[nome do conselheiro] + [tema]` por
  conselheiro escalado, preferindo fontes primárias (livros, blogs,
  newsletters, palestras deles próprios) a artigos de compilação.

Incorpore os achados às visões com citação ("Em uma entrevista de 2023 na
X, Dunford argumentou…"). Se a pesquisa contradizer um dossiê, confie na
pesquisa e anote a correção.

## Regras de fundamento (não-negociáveis)

- **Rotule a sessão como simulação** uma vez, no topo: uma linha como
  *"Conselho simulado — cada visão é construída a partir dos frameworks e
  posições publicados do conselheiro, não da revisão real dele."*
- **Sem citação fabricada.** Citação direta só para linhas verificáveis no
  dossiê ou na passada de pesquisa, com a fonte nomeada. Senão parafraseie:
  "A posição de Hopkins em *Scientific Advertising* é…"
- **Sem endosso ou condenação inventados.** Um conselheiro pode ser
  simulado *aplicando o framework dele* ao produto do usuário; nunca
  declare ou insinue que a pessoa real tem uma opinião sobre a empresa
  específica do usuário.
- **Conselheiros vivos recebem cuidado extra.** Godin, Brunson, Hormozi,
  Dunford, Sutherland, Sharp, Handley, e Vaynerchuk estão vivos e ativos —
  as posições deles evoluem; prefira a passada de pesquisa para qualquer
  coisa sensível ao tempo, e nunca simule eles comentando sobre
  concorrentes nomeados ou controvérsias.
- **Discorde em substância, não caricatura.** A visão de cada conselheiro
  precisa ser a versão mais forte da opinião deles aplicada a esse caso —
  sem espantalho para a síntese derrubar.
- **Se o dossiê e a pergunta do usuário não se sobrepõem** (ex.: perguntar
  ao Hopkins sobre TikTok), diga isso na visão e raciocine por analogia
  explícita: "Hopkins nunca viu feed social, mas o princípio de
  amostragem dele mapeia assim…"

## Formato de saída

```text
> Conselho simulado — cada visão é construída a partir dos frameworks e
> posições publicados do conselheiro, não da revisão real dele.

## A pergunta diante do conselho
[reformulação de 1-2 frases + o que está em jogo]

## Escalados: [Conselheiro A], [Conselheiro B], [Conselheiro C] ([modo])
[uma linha sobre por que esse banco, incluindo quem foi escalado como dissidente]

---

### [Conselheiro A] — [a lente deles, 3-5 palavras]
[visão de 2-4 parágrafos]
**Resumo:** [uma frase]

### [Conselheiro B] — …
…

---

## Onde o conselho discorda
1. **[Conflito]** — [A] diz X por causa de [framework]; [B] diz Y por
   causa de [framework]. O trade-off real: [tensão subjacente]. O que
   resolveria: [evidência/teste].
2. …

## Síntese do presidente
[recomendação ajustada ao estágio e restrições desse usuário]
- **Faça:** [2-4 próximos passos concretos]
- **Fio de gatilho:** [aviso de qual conselheiro monitorar, e o sinal]
- **Execute com:** [encaminhamentos de skill]
```

## Adicionando um conselheiro customizado

Usuários podem estender o banco ("adicione meu próprio conselheiro").
Crie um dossiê seguindo a estrutura em
[references/advisor-template.md](references/advisor-template.md) — os
mesmos campos dos conselheiros nativos (lente, frameworks, posições
documentadas com fonte, perguntas-assinatura, melhor-para/pontos cegos,
notas de voz, obras-chave). Para conselheiros não-famosos (o antigo chefe
do usuário, um executivo interno), peça ao usuário para fornecer as
posições; não as invente. Salve em `.agents/advisors/<nome>.md` no
projeto do usuário para que persista e nunca colida com atualizações do
repositório.

## Antipadrões

- **O conselho que concorda** — cinco visões que todas abençoam o plano
  existente do usuário. Reescale com um dissidente real.
- **Conselho genérico com sabor de nome** — uma visão que sobreviveria se
  trocassem o nome não é uma visão; ancore cada uma nos frameworks e
  posições documentadas específicas daquele conselheiro.
- **Sopa de citação** — costurar frases de efeito famosas em vez de
  aplicar o método por trás delas.
- **Conselho para trabalho de execução** — o conselho decide a direção;
  não escreve a landing page. Encaminhe para a skill de execução assim
  que a direção estiver definida.
- **Doze conselheiros para um título** — combine o tamanho do banco com o
  risco.

## Skills relacionadas

- **positioning** / **product-marketing**: quando a visão da Dunford vence — execute o trabalho de posicionamento
- **offers** / **pricing**: quando a direção Hormozi/Halbert vence — construa a oferta
- **copywriting** / **copy-editing**: quando o conselho revisou copy — execute as revisões
- **ads** / **ad-creative**: quando o debate foi mídia ou estratégia de criativo
- **content-strategy** / **social**: quando a direção Handley/Vaynerchuk vence
- **brand-strategy** / **marketing-psychology**: para o trabalho de disponibilidade do Sharp e a mecânica comportamental do Sutherland
- **ab-testing**: quando o mapa de discordância diz "teste isso" — Hopkins insistiria
- **deep-research**: para a passada de pesquisa ao vivo, quando instalada
