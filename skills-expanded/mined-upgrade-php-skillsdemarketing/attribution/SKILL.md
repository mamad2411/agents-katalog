---
name: attribution
description: Quando o usuário quiser descobrir qual marketing realmente gera conversões e receita, escolher ou interpretar um modelo de atribuição, ou reconciliar números conflitantes entre ferramentas. Use também quando o usuário mencionar "atribuição," "modelo de atribuição," "first-touch vs last-touch," "multi-touch," "que canal gera receita," "qual é meu CAC real," "meus dashboards não batem," "Google/Meta diz X mas o GA diz Y," "media mix model," "MMM," "incrementalidade," "geo lift," "teste holdout," "atribuição autodeclarada," "dark social," ou quiser instrumentar a atribuição sozinho — "conectar agendamentos à origem," "fechar a lacuna de identify," "rastrear conversões em domínio terceiro," "atribuição própria/self-hosted." Para setup de tracking e UTMs, veja analytics. Para pixels/CAPI de anúncio, veja ads. Para relatório de pipeline e receita, veja revops. Para o ponto cego de atribuição em busca por IA, veja ai-seo.
metadata:
  version: 1.1.0
---

# Atribuição

Você ajuda os usuários a responder a pergunta mais difícil do marketing:
**qual dos meus esforços realmente causou essa conversão e essa receita?**
Atribuição é onde o marketing mais perde dinheiro — para canais que parecem
bons em um dashboard e péssimos em outro, para "direto" e "busca de marca"
que escondem a origem real, e para modelos que silenciosamente codificam
uma opinião como se fosse fato.

Esta skill tem dois pilares. Saiba de qual o usuário precisa antes de
entrar de cabeça:

- **(A) Interpretação** — escolher um modelo de atribuição, escolher uma
  abordagem de mensuração, e *reconciliar os números conflitantes* que
  suas ferramentas reportam. Isso se aplica a todo mundo, mesmo sem
  nenhuma engenharia.
- **(B) Instrumente sua própria atribuição (first-party)** — instrumentar e
  costurar atribuição *você mesmo* quando você controla o site/app. Essa é
  a trilha de construção. Use quando o usuário disser "eu quero rastrear
  isso eu mesmo" ou estiver esbarrando em uma conversão que vive em um
  domínio que ele não é dono.

A maioria dos pedidos começa em (A). Recorra a (B) só quando eles controlam
a superfície e querem construir.

Contexto de produto: verifique se `.agents/product-marketing.md` existe e
leia-o se presente — tipo de negócio, ciclo de venda, e conversão principal
informam quase toda recomendação aqui.

## Limites — o que esta skill NÃO cobre

Declare isso logo de início para não reconstruir skills vizinhas:

- **Tracking geral de evento, planos de tracking, setup de UTM, GA4/GTM** →
  **analytics**. Atribuição *presume que o tracking já existe*. A linha:
  analytics = "que eventos e como dispará-los"; atribuição = "como os
  toques se juntam às conversões e sobrevivem até a receita."
- **Pixels de plataforma de anúncio, CAPI, tracking de conversão
  server-side** → **ads** (`references/conversion-tracking.md`).
  Atribuição consome os números reportados pela plataforma e corrige o
  viés deles; não configura os pixels.
- **Estágios de pipeline, lifecycle de lead, dashboards de receita do
  CRM** → **revops**. Atribuição alimenta o dado de pipeline; não define
  os estágios.
- **Aparecer em / medir busca por IA** → **ai-seo**. Atribuição só nomeia
  o tráfego de IA como um ponto cego.

---

## Pilar A — Interpretação

### 1. O que atribuição pode e não pode te dizer

Estabeleça expectativas antes de tocar em um número:

- **Atribuição é direcional, não verdade.** É um modelo de causalidade
  construído com dado incompleto (cookies expiram, sessões se fragmentam,
  toques offline desaparecem, pessoas pesquisam em um dispositivo e compram
  em outro). Trate como um forte indício, nunca um veredito.
- **Todo modelo é uma opinião.** "First-touch" diz que o primeiro anúncio
  leva todo o crédito; "last-touch" diz que o clique que fecha leva. Os
  dois estão errados em direções opostas. Escolher um modelo é escolher em
  qual história acreditar — diga isso em voz alta.
- **A lacuna de atribuição é normal.** A soma das conversões reportadas por
  canal quase sempre excede as conversões reais, porque toda plataforma
  reivindica crédito pela mesma venda. Seu trabalho é encolher e explicar
  a lacuna, não fazer os números baterem perfeitamente. Eles não vão bater.

Quando um usuário exigir um único número verdadeiro, reformule: "Podemos
te dar um número *defensável e consistente* e uma leitura de quais canais
estão em alta. Uma única verdade objetiva não existe — aqui está o
porquê, e aqui está o que usamos para decidir mesmo assim."

### 2. Modelos de atribuição

Os seis modelos padrão e quando cada um mente:

| Modelo | Regra de crédito | Melhor para | Como mente |
|---|---|---|---|
| **First-touch** | 100% para o primeiro toque conhecido | Avaliação de topo de funil/demand-gen; ciclos curtos | Ignora tudo que fechou o negócio; supercredita canais de reconhecimento |
| **Last-touch** | 100% para o último toque antes da conversão | Resposta direta, e-commerce rápido | Supercredita fundo de funil + busca de marca/direto; ignora o que criou a demanda |
| **Last non-direct** | 100% para o último toque, pulando "direto" | Uma correção barata para a poluição do "direto" | Ainda é single-touch; só move o ponto cego |
| **Linear** | Crédito igual para todo toque | Jornadas longas e multi-toque onde todo passo importa | Trata uma visita descartável como uma demo; favorece canais de alta frequência |
| **Time-decay** | Mais crédito para toques mais perto da conversão | Ciclos mais longos onde a recência importa | Subcredita o topo de funil; ainda é uma suposição, não uma medição |
| **Baseado em posição (U-shaped)** | 40% primeiro, 40% último, 20% no meio | B2B com momentos claros de "criou" + "fechou" | A divisão 40/40/20 é arbitrária; os toques do meio saem perdendo |
| **Orientado por dado (algorítmico/Shapley)** | Crédito da contribuição marginal modelada | Contas de alto volume com conversões suficientes | Uma caixa-preta; precisa de volume; não vê toques offline/escuros que nunca foram alimentados |

**Regras de ouro:**

- Nunca reporte um único modelo isoladamente para um ciclo de venda longo.
  Mostre **first-touch e last-touch lado a lado** — a verdade vive entre
  os dois, e a lacuna entre eles *é* o insight.
- Atribuição orientada por dado precisa de volume (o Google Ads
  historicamente exigia ~3.000 interações de anúncio e ~300 conversões em
  30 dias; desde então relaxou os mínimos e tornou o DDA padrão, mas
  volume baixo ainda vira ruído disfarçado de ciência). Use baseado em
  posição em vez disso quando o volume for baixo.
- O modelo importa muito menos do que ser **consistente** e combiná-lo com
  uma checagem de sanidade fora do modelo (Pilar A §4, autodeclarado).

Para a matemática dos modelos, exemplos resolvidos de uma jornada pontuada
de seis formas, e Shapley explicado de forma simples, veja
`references/attribution-models.md`.

### 3. Os três paradigmas de mensuração

Modelos dividem crédito *dentro* do seu dado rastreado. Paradigmas são como
você chega perto da *causalidade* — cada vez mais rigorosos, cada vez mais
caros:

| Paradigma | O que é | Responde | Precisa | Cuidado |
|---|---|---|---|---|
| **MTA** (atribuição multi-touch) | Costura toques no nível do usuário, aplica um modelo | "Que touchpoints aparecem em jornadas que convertem?" | Tracking limpo cross-device no nível do usuário | Perda de cookie + privacidade destruíram o dado no nível do usuário; subestima silenciosamente |
| **MMM** (modelagem de mix de mídia) | Regressão top-down de gasto vs. resultados ao longo do tempo | "Qual é a contribuição agregada de cada canal, incluindo offline/marca?" | 2-3 anos de dado semanal, variação de gasto | Correlacional; reage devagar; precisa de variações reais de orçamento para aprender |
| **Incrementalidade** (geo holdout, PSA, ghost ads, on/off) | Experimento controlado: exposto vs. retido | "Esse canal *causou* um ganho que eu não teria de qualquer forma?" | Capacidade de reter; volume suficiente para significância | O padrão-ouro, mas você só consegue testar algumas coisas por vez |

**Como escolher:** orçamento pequeno / ciclo curto → boa UTM + last-non-
direct + uma pesquisa autodeclarada vence um modelo chique. Orçamento
médio, vários canais → MTA para o dia a dia + testes de incrementalidade
periódicos nos maiores itens de linha. Orçamento grande, gasto offline +
marca → MMM para o portfólio + incrementalidade para validar os
coeficientes do MMM. Incrementalidade é o desempate sempre que dois canais
reivindicam as mesmas conversões.

Tabela de decisão por orçamento × ciclo de venda × contagem de canal, e
como *ler* um teste geo-holdout/PSA (não um tutorial de estatística), em
`references/measurement-paradigms.md`.

### 4. Atribuição autodeclarada

O sinal mais subutilizado, e frequentemente o mais honesto para ciclos
longos e dark social. Uma pesquisa pós-conversão "Como você conheceu a
gente?" captura o que o tracking estruturalmente não consegue: podcasts,
boca a boca, comunidades no Slack, um tweet do founder, "um amigo me
contou."

- **Quando vence o tracking:** ciclos de consideração longos, alto boca a
  boca, marca/comunidade forte, ou muito dark social (veja §5). Se uma
  fatia grande das suas jornadas é "direto," você tem um buraco no
  formato de autodeclarado.
- **Pergunte no momento da conversão** (cadastro, primeira compra,
  solicitação de demo) — recall mais alto, antes da memória desbotar.
- **Formulação:** aberta ("Como você conheceu a gente pela primeira
  vez?") captura dark social; uma lista curta de opções é mais fácil de
  quantificar mas pré-vicia a resposta. Melhor prática: lista dos seus
  canais conhecidos **mais um campo livre "outro/nos conte mais."**
- **Trate como um input de triangulação, não como verdade absoluta** — o
  recall é impreciso e as pessoas dão crédito ao toque *memorável*, não ao
  primeiro. É a checagem fora do modelo que mantém seus modelos rastreados
  honestos.
- No lado da construção, isso é um campo de formulário gravado como
  propriedade de pessoa no seu CRM/analytics — veja o Pilar B e
  `references/first-party-tracking.md`.

### 5. Reconciliando fontes conflitantes

O pedido por trás da maioria dos trabalhos de atribuição: **"o Google diz
50, o Meta diz 40, o GA diz 60, meu CRM diz 35 — quem está certo?"**
Ninguém. Aqui está o framework.

**Por que cada fonte mente sistematicamente:**

| Fonte | Viesada para | Porque |
|---|---|---|
| **Plataformas de anúncio** (Google/Meta/LinkedIn) | Superconta *a si mesma* | Reivindica conversões view-through + clique dentro da própria janela; toda plataforma conta a mesma venda; motivada a parecer boa |
| **GA / web analytics** | Último clique não-direto | Perde cross-device, perde usuários bloqueados por cookie, joga o desconhecido em "direto" |
| **CRM** | O que o vendedor digitou / o formulário capturou | Entrada humana, sobrescritas de fonte de lead, negócios offline sem rastro digital |
| **Pesquisa autodeclarada** | O toque *memorável* | Viés de recall; subconta toques chatos-mas-reais como retargeting |

**Como triangular:**

1. **Escolha uma fonte de verdade para a contagem de conversão** —
   geralmente seu CRM ou backend (o sistema onde o dinheiro é real). Tudo
   o mais explica *de onde vieram*, não redefine *quantas*.
2. **Nunca some entre plataformas.** Se o Google e o Meta reivindicam a
   mesma conversão, você tem uma conversão com dois reivindicantes, não
   duas conversões. Deduplique contra o total da fonte de verdade.
3. **Leia concordância direcional, não bate exato.** Se toda fonte diz que
   busca paga subiu e orgânico caiu esse trimestre, essa tendência é
   confiável mesmo que nenhum número bata.
4. **Use o autodeclarado como desempate** quando plataformas brigam pelas
   mesmas conversões, e **incrementalidade** quando o risco justifica um
   teste.
5. **Espere e orce para a lacuna.** Reporte "plataformas reivindicam N;
   podemos verificar M; a diferença é superclaim + view-through + não
   rastreado — aqui está nossa melhor alocação."

O resultado é uma alocação honesta com níveis de confiança, não uma falsa
reconciliação até a casa decimal.

### 6. Os pontos cegos

Onde as conversões se escondem, fazendo canais reais parecerem fracos:

- **Direto** — a gaveta de bagunça. Favoritos e URLs digitadas, sim, mas
  também referrers removidos, app-para-web, dark social, e qualquer toque
  que seu tracking perdeu. Uma fatia grande de "direto" é um problema de
  *mensuração*, não um canal.
- **Busca de marca** — pessoas que te descobriram em outro lugar e
  buscaram seu nome no Google. Last-touch entrega o crédito à busca de
  marca paga/orgânica; o driver real foi o que fez a pessoa buscar.
  Segmente busca de marca vs. não-marca ou você vai cortar o
  financiamento do topo de funil.
- **Dark social** — compartilhamento que não carrega referrer: DMs,
  Slack/Discord, podcasts, newsletters, screenshots — no Brasil, muito
  forte via WhatsApp. Estruturalmente invisível ao tracking; autodeclarado
  é a única forma de ver isso (§4).
- **Tráfego de IA** — assistentes e busca por IA cada vez mais influenciam
  compradores, e então os enviam via busca de marca ou direto, então o
  toque de IA é invisível no analytics. Nomeie isso e passe o trabalho
  mais profundo para **ai-seo**.

O fio condutor: **quando "direto" e "busca de marca" dominam, seu topo de
funil está funcionando e sua atribuição está escondendo isso.** Diga isso
explicitamente — é o erro de leitura mais comum no marketing.

### 7. Bifurcação por tipo de negócio

Os padrões diferem bastante. Resumo aqui; playbooks completos em
`references/by-business-type.md`.

- **SaaS B2B (ciclo longo, assistido por vendas):** jornadas se estendem
  por semanas-meses e várias pessoas, então modelos de único toque
  enganam muito. Ancore no **CRM como fonte de verdade**, use
  **first-touch + baseado em posição** lado a lado, apoie-se fortemente
  no **autodeclarado na demo/cadastro**, e trate a atribuição de
  **pipeline/receita** (→ revops) como o placar real. Toques offline
  (eventos, conversas de venda) tornam o MTA mais fraco e o autodeclarado
  mais forte aqui.
- **E-commerce / DTC (ciclo curto, self-serve):** jornadas rápidas, alto
  volume, gasto concentrado em social pago + busca. Ancore no **ROAS de
  plataforma mas desconfie dele** (inflação de iOS/CAPI), valide com
  **MMM assim que o gasto for material** e
  **incrementalidade/geo-holdouts** nos seus maiores canais, e use uma
  **pesquisa pós-compra** para capturar o que os pixels perdem.
  Last-touch é defensável para SKUs de giro rápido; MMM+incrementalidade
  é como você aloca o orçamento real.

---

## Pilar B — Instrumente sua própria atribuição (first-party)

Use isso quando o usuário **controla o site/app** e quer instrumentar a
atribuição ele mesmo — especialmente para uma conversão que acontece em um
**domínio que ele não é dono** (um agendamento SavvyCal/Calendly/Cal.com,
uma página de Checkout do Stripe). Este pilar é fundamentado em builds de
produção reais; o runbook completo com padrões de código está em
`references/first-party-tracking.md`. O essencial:

### O grafo de identidade

Atribuição first-party é uma ideia: **junte a navegação anônima à
conversão eventual.**

1. Um visitante chega anonimamente; sua ferramenta de analytics atribui um
   **`distinct_id` anônimo** e carimba as **propriedades de first-touch**
   (`$initial_referrer`, `$initial_utm_*`) nos eventos dele.
2. Na conversão (cadastro, agendamento, compra) você chama **`identify()`**
   com um id estável (e-mail ou UUID de usuário). Isso **mescla** o
   histórico anônimo em uma pessoa conhecida — o first-touch agora
   sobrevive até a conversão.
3. Todo evento de conversão agora pode ser detalhado por canal de
   first-touch. É o jogo inteiro.

### Fechando a lacuna do `identify()`

A falha first-party mais comum: **nada nunca chama `identify()`**, então
as conversões nunca se juntam ao histórico de navegação e todo cliente
parece ter aparecido do nada. (Enquadramento adaptado da abordagem PostHog
de Tessa Kriesel.) A correção é chamar identify em cada conversão real.
**Audite primeiro** — muitos apps SaaS já identificam no cadastro; não
reconstrua o que já funciona. Ache as conversões *específicas* não
instrumentadas e feche só essas.

### Costurando conversões em um domínio terceiro

O único caso que precisa de maquinário de verdade: uma conversão que se
completa em um domínio que você não controla (uma ferramenta de
agendamento, um checkout hospedado). Você não consegue rodar seu analytics
lá, então:

1. **No momento do clique**, um decorador de link em capture-phase anexa o
   `distinct_id` anônimo do visitante à URL de saída via o **passthrough
   de metadado** da ferramenta (ex.: `?metadata[ph_distinct_id]=<id>`). Um
   único listener no nível do documento cobre todo CTA — sem editar link
   por link.
2. A ferramenta terceira armazena esse metadado e o retorna no
   **webhook** dela.
3. Seu **handler de webhook** dispara uma **mesclagem de identidade**
   (`$identify` com o e-mail do agendamento como `distinct_id` e o id
   anônimo contrabandeado como `$anon_distinct_id`) mais um **evento de
   conversão** — juntando o agendamento de volta à jornada de marketing.

### Guardrails (não pule)

- **Guarda de anonimato — falhe fechado.** Só contrabandeie o id
  *anônimo*. Depois do `identify()`, o id atual vira o e-mail/UUID do
  usuário; vazar isso em uma URL terceira ou mesclar nele corrompe perfis
  (o e-mail da pessoa A se funde em quem quer que agende). Rejeite ids
  que parecem PII (contêm `@`), limite o tamanho, e quando a identidade
  for ambígua, **não envie nada**. Se o app identifica por UUID, teste
  `distinct_id === device_id` em vez de uma checagem de `@`.
- **Qualidade do dado de first-touch.** Redirecionamentos sobrescrevem o
  first-touch verdadeiro. Exclua referrers de OAuth/checkout
  (`accounts.google.com`, `checkout.stripe.com`, `login.*`), seus próprios
  subdomínios (autorreferência), e hosts de dev (`localhost`) da
  classificação de referrer. Geralmente é uma mudança de configuração,
  não código, e é a correção de maior confiança por esforço.
- **Costura cross-subdomain.** Site de marketing → app em um subdomínio
  precisa compartilhar um projeto de analytics + um cookie
  cross-subdomain, ou a jornada quebra na transição. Espere **números
  quase zero até a costura ser verificada em produção** — não entre em
  pânico com dado vazio; use um fallback heurístico de janela de campanha
  e faça backfill da coorte pré-costura enquanto isso (detalhes na
  referência).

### Relatório e a última milha

O primeiro ganho é um insight: seu **evento de conversão detalhado por
canal de first-touch** (`$initial_utm_source` / `$initial_referring_domain`),
e — juntado à receita — **canal → conversão → receita**. Confirme a
configuração de first-touch vs. last-touch na ferramenta (muitas usam
last-touch por padrão; atribuição first-party quer `$initial_*`).

Mas first-touch sozinho não consegue rodar os modelos multi-touch da §2.
**Armazene o caminho de toque completo e ordenado** (não só `$initial_*`)
e a trilha de construção alimenta a trilha de interpretação — você
consegue pontuar suas próprias jornadas baseado em posição / linear /
time-decay em vez de só ler sobre eles.

**A última milha — leve isso para o CRM** (refinamento de produção de
Tessa Kriesel). Um detalhamento em uma ferramenta de analytics é um
relatório; vendas e lifecycle agem sobre atribuição *escrita no registro*.
Sincronize um **campo `source` com `confidence` e `basis`** (ligado à
jornada vs. autodeclarado vs. fallback de janela de campanha) mais uma
**leitura Pago-vs-Orgânico** a partir do meio, **consolidado na conta**
(não só no contato — uma organização B2B é várias pessoas com e-mails
mistos de trabalho/pessoal). Como pipeline/lifecycle então *usam* isso é
trabalho de **revops**.

O padrão é agnóstico de ferramenta: identify + merge existe no PostHog,
Segment, Amplitude, e via user-id no GA4; a costura terceira funciona com
qualquer ferramenta que tenha passthrough de metadado + webhook. PostHog +
SavvyCal são o exemplo resolvido em
`references/first-party-tracking.md`.

---

## Formato de saída

Entregue uma **leitura de atribuição**, não um despejo de dado:

```markdown
# Leitura de Atribuição — [data]

## A pergunta
[Que decisão isso informa — ex.: "para onde deve ir o orçamento do próximo trimestre?"]

## Fonte de verdade
[Qual sistema define a contagem de conversão, e por quê]

## O que cada fonte diz
| Canal | Reportado pela plataforma | GA | CRM | Autodeclarado | Nossa leitura |
|---|---|---|---|---|---|
[Deduplicado contra a fonte de verdade; não somado]

## Comparação de modelo (para ciclos longos)
[First-touch vs. last-touch lado a lado; a lacuna é o insight]

## Confiança e lacunas
[A lacuna de atribuição, os pontos cegos, o que não conseguimos ver]

## Recomendação
[Decisão de alocação com níveis de confiança; o teste de desempate que vale a pena rodar]
```

## Integrações de ferramentas

Para implementação, veja o [registro de ferramentas](../../tools/REGISTRY.md).
Principais ferramentas:

| Ferramenta | Melhor para | MCP | Guia |
|---|---|:---:|---|
| **PostHog** | Atribuição first-party, identify/merge, funis | - | [posthog.md](../../tools/integrations/posthog.md) |
| **GA4** | Web analytics, comparação de modelo, costura de user-id | ✓ | [ga4.md](../../tools/integrations/ga4.md) |
| **Dub** | Link curto + atribuição de clique | ✓ | [dub-co.md](../../tools/integrations/dub-co.md) |
| **Segment** | CDP — roteia identify/track para todo destino | - | [segment.md](../../tools/integrations/segment.md) |
| **HubSpot** | Campos de fonte de lead + autodeclarado do CRM | ✓ | [hubspot.md](../../tools/integrations/hubspot.md) |
| **Salesforce** | CRM como fonte de verdade de receita | - | [salesforce.md](../../tools/integrations/salesforce.md) |
| **Supermetrics** | Puxa números de plataforma para um lugar só para reconciliar | ✓ | [supermetrics.md](../../tools/integrations/supermetrics.md) |
| **RB2B** | Desanonimizar visitantes de site B2B | - | [rb2b.md](../../tools/integrations/rb2b.md) |

---

## Skills relacionadas

- **analytics** — tracking de evento, planos de tracking, UTMs, setup de GA4/GTM. Faça isso *antes* da atribuição.
- **ads** — pixels de plataforma de anúncio, CAPI, tracking de conversão server-side (`references/conversion-tracking.md`).
- **revops** — estágios de pipeline, lifecycle de lead, relatório de receita do CRM. Atribuição alimenta isso.
- **ai-seo** — o ponto cego de atribuição em busca por IA em profundidade.
- **ab-testing** — experimentos controlados; a mentalidade de incrementalidade aplicada a mudanças no site.
