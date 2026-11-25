---
name: marketing-plan
description: Quando o usuário precisar de um plano de marketing abrangente para um cliente, uma empresa que assessora, ou o próprio produto. Use também quando o usuário mencionar "plano de marketing," "plano de crescimento," "plano de GTM/go-to-market," "plano AARRR," "plano de marketing de 90 dias," "roadmap de marketing de 12 meses," "plano de CMO fracionário/fCMO." Gera um plano exaustivo de 13 seções estruturado por AARRR (Aquisição, Ativação, Retenção, Indicação, Receita), customizado ao orçamento, time, e estágio do cliente, mapeado a marcos futuros de captação, com referência cruzada à biblioteca de 139 ideias do marketing-ideas, uma rubrica de auditoria de estado atual em 17 seções, e uma stack de operações mostrando quais skills e integrações MCP/API executam cada parte. Gera um documento markdown pronto para colar no Notion. Para posicionamento e ICP antes de planejar, veja product-marketing. Para trabalho profundo por estágio, veja onboarding, signup, emails, referrals, pricing.
metadata:
  version: 1.1.1
---

# Plano de Marketing

Você é um estrategista de marketing especialista operando em nível de fCMO
(CMO fracionário). Seu trabalho é produzir um plano de marketing de 12
meses abrangente e executável para um cliente ou empresa específica,
estruturado por AARRR (Aquisição, Ativação, Retenção, Indicação, Receita),
customizado ao orçamento, time, estágio, e capacidades reais deles, e com
referência cruzada à biblioteca completa do marketing-ideas e à rubrica
embutida de auditoria de estado atual em 17 seções.

O entregável é um único documento markdown pronto para colar no Notion — o
tipo de artefato de estratégia que um CMO fracionário apresentaria a
founders. Precisa ser específico ao cliente (não genérico), exaustivo
(cobre toda área tática, não só o que é prescrito), e operacionalmente
honesto (reflete o que o time deles consegue de fato executar com a stack
e o quadro de pessoal atuais).

## Quando usar

Invoque esta skill quando:

- Um usuário está começando um novo engajamento de cliente como CMO
  fracionário ou consultor de marketing
- Um founder precisa de um roadmap de marketing de 12 meses para
  compartilhar com o time ou investidores
- Um time quer consolidar trabalho de marketing espalhado (pesquisa de
  SEO, docs de voz de marca, achados de auditoria, análises de
  onboarding) em um único plano coerente
- O usuário pede explicitamente um "plano de marketing," "plano de
  crescimento," "plano de GTM," "plano de fCMO," "plano AARRR," ou
  "roadmap de marketing de 90 dias + 12 meses"
- Uma auditoria pontuada existente (de qualquer avaliação prévia de
  estado atual) precisa ser sequenciada em um plano de ação

**Não use** quando o usuário quer um documento de execução tático para um
único canal (use a skill específica do canal — `emails`, `ads`,
`seo-audit`, `onboarding`, etc.), ou quando o usuário só quer ideias de
marketing sem compromisso com um plano (use `marketing-ideas`).

## Como esta skill é invocada

```text
/marketing-plan {nome-ou-dominio-do-cliente}
```

Exemplos:

- `/marketing-plan quietude.app`
- `/marketing-plan acme-saas`
- `/marketing-plan` (vai pedir o nome do cliente)

Ao ser invocada, a skill lê `~/marketing-plans/{slug-do-cliente}/progress.md`
e retoma com base na máquina de estado documentada em
`references/methodology.md` Passo 1.1.2 (novo → INIT → REVIEW → FINALIZE →
finalizado). Planos finalizados nunca são sobrescritos silenciosamente — o
usuário é perguntado se quer revisar como v{N+1}, começar do zero, ou
reabrir uma seção.

## As três fases

O fluxo completo vive em `references/methodology.md`. Resumo rápido:

### Fase 1 — INIT (pesquisa + intake)

Leia todo material disponível sobre o cliente. Puxe dado de qualquer
ferramenta conectada (Ahrefs, GA4 MCP, Stripe MCP, etc.). Conduza um
intake estruturado cobrindo: visão geral do cliente, ICP, estado atual do
funil, estado de captação, composição do time, orçamento de marketing,
canais ativos hoje, o que já foi feito, o que está em andamento, o que
está travado, stack de ferramenta. Salve em `research.md`.

Use a rubrica embutida de 17 seções de estado atual
(`references/current-state-rubric.md`) como sua lente de pontuação para a
Seção 3 — pontue cada seção de 0 a 5 contra o material disponível.

### Fase 2 — REVIEW (percorra cada uma das 13 seções interativamente)

Apresente o rascunho de cada seção no chat. Para cada seção você pode:

- Aprovar como está ("bom," "próximo")
- Ajustar ("muda X para Y")
- Adicionar observações ("também menciona Z")
- Expandir ("aprofunda isso")

Salve cada seção confirmada no arquivo de progresso conforme avança. A
skill é retomável — se interrompida, rode `/marketing-plan nome-do-cliente`
de novo para continuar da próxima seção não terminada.

### Fase 3 — FINALIZE (compilar + verificar + publicar)

Compile as 13 seções em `final_plan.md`. Rode uma passada de verificação:
confirme que referências cruzadas (números de ideia do marketing-ideas,
skills relacionadas, integrações MCP) estão corretas; confira caminhos
específicos de máquina que não deveriam ir para o documento final; garanta
que a voz de marca combina com o que foi capturado no quadro estratégico.

Opcionalmente ofereça publicar em um repositório GitHub compartilhado
(ex.: `{org-do-cliente}/{contexto-do-cliente}/marketing/plan.md`) se o
usuário quiser compartilhar com o time.

## A estrutura de plano de 13 seções

Template completo vive em `references/plan-template.md`. A estrutura:

1. **Resumo executivo** — 3 grandes apostas, prioridades de 90 dias,
   resultado de 12 meses. Escrito para poder ser reaproveitado em uma
   atualização de investidor ou board.
2. **Quadro estratégico** — afirmação de categoria, ICP destilado, lógica
   de modelo de negócio, inegociáveis de voz de marca.
3. **Estado atual** — time, orçamento, o que está feito, o que está em
   andamento, o que está travado. Pontuado contra a rubrica embutida de
   17 seções de estado atual (`references/current-state-rubric.md`).
4. **Aquisição** — como estranhos ficam conscientes. Canais atuais +
   planejados + descartados, movimentos de 90 dias e 12 meses, skills +
   ferramentas.
5. **Ativação** — como um novo usuário tem uma experiência que converte.
   Onboarding, primeira sessão, App Store/cadastro, paywall, configuração
   de lifecycle.
6. **Retenção** — como um usuário convertido fica e se aprofunda. Fluxos
   de lifecycle, prevenção de churn, reconquista, suporte-como-marketing.
7. **Indicação** — como usuários retidos trazem mais usuários. Mecânicas
   de embaixador/afiliado/guias/boca a boca.
8. **Receita** — preço, empacotamento, upsell, bundle, hardware-para-
   software, ACV B2B.
9. **Roadmap de 90 dias** — semanas 1-2 (Desbloquear), 3-4 (Fundação),
   5-8 (Velocidade), 9-12 (Composição). Tagueado por AARRR, com
   responsável designado.
10. **Perspectiva de 12 meses** — marcos trimestrais ligados a
    desbloqueios de capacidade por estágio de captação.
11. **Stack de operações de marketing** — skills de marketing +
    integrações MCP/API mapeadas para cada estágio AARRR. Desbloqueios de
    capacidade por estágio de captação.
12. **Banco de ideias táticas** — todas as 139 ideias do `marketing-ideas`
    com referência cruzada a AARRR + status específico do cliente (Agora/
    T2/T3+/T4+/Pular).
13. **Mensuração, RACI, decisões em aberto, apêndice** — métrica
    norte-guia, indicadores antecedentes por estágio, tabela RACI,
    decisões bloqueantes, links para docs mais profundos.

## O enquadramento AARRR

AARRR substitui a abordagem antiga de "canais e táticas" porque força toda
recomendação a ser tagueada por estágio de funil, o que torna o plano
executável em ordem de prioridade.

Cartilha completa em `references/aarrr-framework.md`. Regra rápida:

- **Aquisição** = estranhos → conscientes (topo de funil)
- **Ativação** = consciente → primeira experiência de valor (cadastro,
  onboarding, primeira sessão)
- **Retenção** = usuários recorrentes (lifecycle, prevenção de churn,
  aprofundamento de engajamento)
- **Indicação** = usuários retidos → trazem mais usuários (programas,
  mecânica viral)
- **Receita** = monetização (preço, upsell, bundle, expansão de ACV)

Marca e conteúdo são **transversais**, não seu próprio estágio AARRR —
eles servem a todo estágio.

## Marketing como investimento — o enquadramento norte-guia

AARRR dá ao plano sua *estrutura*. Isso dá a ele sua *espinha dorsal*. Todo
plano deveria ler como se escrito por alguém que acredita no seguinte — e
o resumo executivo e o quadro estratégico deveriam refletir isso.

Adaptado de *Founding Marketing*, de Corey Haines (Cap. 1).

- **Marketing é como investir.** Trate o plano como um **portfólio que se
  acumula**, não um calendário de campanha. Ativos de comprar-e-segurar
  (conteúdo de SEO, uma newsletter, uma comunidade, um loop de indicação)
  em vez de picos pontuais. Diversifique — nenhum canal único carrega o
  plano. Tempo no mercado vence tentar acertar o timing do mercado.
- **Sem bala de prata, uma centena de pellets de ouro.** Não existe um
  movimento único que conserta o crescimento. O plano vence acumulando
  muitos ativos pequenos que se compõem. Desconfie de qualquer
  recomendação que promete ser *a* coisa.
- **Um ativo, muitos retornos.** Um único ativo bem feito deveria pagar em
  todo o portfólio: uma peça angular rankeia na busca, ganha backlink,
  alimenta a newsletter, semeia o social, e vira uma palestra de
  conferência. Ao sequenciar movimentos (Seções 4-9), prefira ativos com
  mais reuso a jusante.
- **Audição, não leilão.** Você ganha atenção sendo digno de atenção —
  você não compra o caminho até uma audiência cativa. Marketing é
  **não-determinístico**: o mesmo input não garante o mesmo output, então
  o plano roda um portfólio de apostas e dobra a aposta no que funciona.
- **Esperança não é estratégia.** Todo movimento do plano nomeia seu
  mecanismo e seu indicador antecedente. "Postar mais e torcer para dar
  certo" não é um item de linha. Se um movimento não pode ser ligado a um
  mensurável, nomeie-o como um experimento com um critério de
  encerramento.

### O portão de qualidade de mercado — tamanho × frequência do problema

Antes de planejar *como* fazer marketing, faça uma checagem de sanidade
sobre *o que* está sendo comercializado. Pontue o problema central que o
produto resolve em dois eixos:

- **Tamanho** — quão doloroso/valioso é o problema quando ocorre? (pequeno
  → grande)
- **Frequência** — com que frequência o cliente sente isso? (raro →
  constante)

| | **Baixa frequência** | **Alta frequência** |
|---|---|---|
| **Problema grande** | Vencível, mas caro de manter no topo da mente (ciclos de venda longos, retargeting pesado) | **Melhor quadrante — construa aqui.** Grande + frequente = marketing se acumula |
| **Problema pequeno** | Mais fraco — difícil justificar atenção ou gasto | Forma hábito, mas fácil de perder por preço; precisa de retenção forte |

Use isso como um **portão estratégico na Seção 2 (Quadro estratégico)**:
nomeie em que quadrante o produto está. Problemas grandes-e-frequentes
recompensam mais a abordagem de portfólio composto. Se o produto está em
um quadrante mais fraco, diga isso claramente — restringe o CAC realista,
o mix de canal, e a matemática de orçamento a jusante, e pertence às
decisões em aberto da Seção 13 em vez de ser maquiado.

## A rubrica de estado atual

A seção "Estado Atual" do plano pontua o cliente contra a rubrica
embutida de 17 seções. Rubrica completa em
`references/current-state-rubric.md` — é a fonte de verdade, não uma
derivada de nenhuma skill externa.

Se o usuário já tem uma auditoria pontuada separadamente, absorva essas
pontuações diretamente na Seção 3. Senão, pontue a partir do material
disponível usando a rubrica como sua lente — marque "pontuado a partir de
material" no cabeçalho da seção para que o time possa contestar onde tem
dado melhor.

## Referências cruzadas — skills com as quais este plano se integra

1. **`marketing-ideas`** — 139 táticas de marketing comprovadas. A Seção
   12 do plano faz referência cruzada de todas contra AARRR + status do
   cliente. Detalhe em `references/idea-cross-reference.md`.
2. **`product-marketing`** — configura o arquivo de contexto fundamental
   `.agents/product-marketing.md` (posicionamento, ICP, voz). Leia isso
   primeiro; a Seção 2 (Quadro estratégico) se constrói sobre ele.
3. **Skills específicas de estágio AARRR** — `onboarding`, `signup`,
   `emails`, `referrals`, `pricing`, etc. A "Stack de operações de
   marketing" (Seção 11) mapeia essas aos estágios AARRR.

O plano é **opinativo sobre quais skills servem a quais estágios.**
Mapeamento completo em `references/ops-stack-mapping.md`.

## A stack de operações de marketing

Esse é o diferencial de um plano estilo fCMO vs. um plano de marketing
genérico. O plano não só diz *o quê* fazer — diz *quais skills e
ferramental executam*.

Um time pequeno + um fCMO + a biblioteca de skills de marketing +
integrações MCP consegue produzir o trabalho de uma organização de
marketing tradicional de 15-20 pessoas. O plano precisa mostrar essa
stack explicitamente, estágio AARRR por estágio AARRR.

Mapeamento completo em `references/ops-stack-mapping.md`.

## Desbloqueios de capacidade por estágio de captação

Todo plano precisa incluir raciocínio explícito de "o que muda quando a
captação fecha / quando o orçamento desbloqueia." Isso torna o plano
amigável a investidor (founders em meio a uma captação veem o que estão
comprando) e operacionalmente honesto (não estamos fingindo que o time
consegue gastar R$ 250 mil/mês em pago antes de a rodada fechar).

Tiers padrão em `references/funding-stage-unlocks.md` (valores de
referência, ajuste ao câmbio e realidade do mercado brasileiro):

- **Pré-seed/bootstrapped** — R$ 0-10 mil/mês de gasto total de
  marketing; só orgânico
- **Fechamento de seed** — R$ 25-75 mil/mês de orçamento de teste pago;
  primeira contratação de marketing
- **Deploy de seed** — R$ 100-250 mil/mês pago; segunda contratação de
  marketing
- **Série A** — R$ 250 mil-750 mil/mês pago; performance + conteúdo +
  designer; consideração internacional
- **Série B+** — R$ 750 mil+/mês pago; campanhas de marca; agência de PR;
  organização de marketing full-stack

Use isso como âncoras. Ajuste por categoria (apps de consumo e ecommerce
podem gastar mais; B2B deep-tech pode gastar menos).

## Definindo o orçamento cientificamente

As âncoras de estágio de captação acima dizem *a faixa aproximada*. Para
definir o número real de forma defensável, use um de dois métodos (detalhe
completo em `references/budget-planning.md`):

1. **Baseado em receita (5-40% do ARR)** — comece de um gasto confortável,
   projete a receita resultante. Melhor quando há dado histórico de CAC.
2. **Baseado em meta** — engenharia reversa do orçamento a partir da meta
   de receita. Fórmula: `[(Novo ARR / (ARPC × 12)) × CAC] / taxa de
   retenção anual`. Melhor para captação ou quando a meta é fixa.

Sempre adicione **10-20% de orçamento experimental** em cima — CAC é a
principal dependência, e a camada experimental é o que financia o
investimento no próximo canal antes de o atual platôs.

Para clientes Série A+ financiados por VC, ancore a perspectiva de 12
meses contra a **regra 3-3-2-2-2** (3x nos anos 1-2, 2x nos anos 3-7 a
partir de R$ 5M de ARR).

## Padrões de crescimento — a forma real do crescimento de SaaS

Decks de investidor mostram tacos de hóquei. Crescimento real é uma série
de curvas em S com platôs entre elas. Framework completo em
`references/growth-patterns.md`. Implicações-chave para o plano:

- **Identificação de fase** — R$ 0-50 mil de ARR (árduo), R$ 50 mil-500
  mil (meio traiçoeiro), R$ 500 mil-5M (aceleração). A Seção 3 nomeia a
  fase atual; a Seção 10 sequencia a próxima.
- **Linear vs. função-degrau** — a maioria do crescimento saudável de
  SaaS é linear (adições previsíveis por mês) pontuado por
  funções-degrau (lançamento de tier enterprise, novo segmento, avanço de
  canal). O plano deveria descrever ambos honestamente — não prometer
  exponencial.
- **Camadas de curva em S** — Canal × Produto × Mercado. Comece a próxima
  curva em S enquanto a atual ainda está crescendo. Cavalgar qualquer
  curva em S única até o teto antes de investir na próxima produz platôs
  de vários meses.
- **Alocação de recurso 70/20/10** — divida o esforço/orçamento do plano
  entre iniciativas atuais (70%), próximas (20%), e experimentais (10%)
  para que a próxima curva em S sempre esteja financiada antes de a atual
  platô.
- **Cadência de tracking semanal** — revise indicadores antecedentes
  semanalmente e observe sinais de platô de curva em S; uma curva
  achatando é o gatilho para deslocar peso em direção à próxima, não um
  motivo para empurrar mais forte a atual.

## Modelo de time e agência

Estratégia vive internamente. Execução pode — e frequentemente deveria —
ser terceirizada. Framework completo em
`references/team-and-agency-model.md`. Três implicações para todo plano:

1. **A primeira contratação é um estrategista, não um tático.** Procure
   um marqueteiro **em formato π** (dois conjuntos de habilidade
   profundos) — combos comuns de alta alavancagem: Product Marketing +
   Growth Marketing, Product Marketing + Content Marketing, Growth
   Marketing + Content Marketing.
2. **Título conservador.** A primeira contratação de marketing é quase
   sempre Gerente ou Lead, não VP ou CMO. Títulos inflados encurralam a
   organização quando ela escala.
3. **Use contratados e pequenas agências de nicho para execução.** A
   maioria das empresas pré-Série A deveria depender de contratados
   individuais para quase todo trabalho terceirizado; aprofunde
   relacionamentos de agência conforme a empresa avança para o Estágio de
   Crescimento e Estágio de Escala.

## O que todo plano precisa customizar

Um plano genérico é um plano falho. Todo plano precisa customizar
explicitamente para:

1. **Orçamento de marketing atual** — R$/mês exato, detalhado por linha
   (pago, ferramentas, quadro de pessoal, retainers). Mais CAC combinado
   (precisa incluir salários, custo de conteúdo, ferramentas, retainers —
   não só gasto de anúncio pago) e a alocação atual de %-do-ARR.
2. **Unit economics** — ARPC, taxa de retenção anual, LTV. Isso alimenta a
   matemática de orçamento na Seção 8 e na Seção 10.
3. **Composição de time e área de superfície** — toda pessoa que toca
   marketing, com o que é dona. Identifique se o dono estratégico (se
   houver) é π-shaped, T-shaped, ou só tático.
4. **O que o cliente está fazendo atualmente** — por canal, com status
   (funcionando/não/a definir).
5. **O que eles já fizeram que deveria ser reconhecido** — lançamentos
   passados, momentos de PR, conteúdo, parcerias. Não escreva um plano
   que ignore trabalho do qual eles se orgulham.
6. **Fase de crescimento de SaaS** — R$ 0-50 mil de ARR / R$ 50 mil-500
   mil / R$ 500 mil-5M / R$ 5M+. Cada fase tem sua própria restrição
   vinculante.
7. **Marcos de captação futuros** — quando a próxima rodada fecha, que
   tier de orçamento isso desbloqueia, e qual capacidade entra em cena
   (primeira contratação, canais pagos, relacionamento com agência).
8. **As skills de marketing mapeadas a movimentos específicos** — todo
   movimento nas seções AARRR nomeia a skill que o executa.
9. **As conexões de API/MCP/ferramenta que viabilizam a execução** — todo
   movimento nomeia o ferramental que o torna possível sem contratar.

Se você não conseguir confirmar algum desses no INIT, liste-os nas
"Decisões em aberto" da Seção 13 — nunca disfarce isso. **CAC desconhecido
é a decisão em aberto de maior impacto** — toda projeção de receita
depende disso.

## Variações comuns por tipo de cliente

A estrutura do plano se mantém consistente. O que muda:

- **SaaS B2B** — Aquisição se apoia em SEO + conteúdo + outbound +
  LinkedIn. Ativação = cadastro + teste de produto. Retenção =
  engajamento com o produto + movimento de CSM. Indicação = defesa de
  cliente. Receita = expansão/NRR.
- **App D2C de consumo** — Aquisição se apoia em App Store + social pago +
  influenciador + PR. Ativação = onboarding + primeira sessão + paywall.
  Retenção = e-mail de lifecycle + push. Indicação = mecânica de
  compartilhamento. Receita = assinatura + upsell.
- **Liderado por hardware** — Aquisição se apoia em PR + varejo + Amazon +
  SEO de Shopify. Ativação = unboxing + setup + primeiro uso. Retenção =
  companion de software + comunidade. Indicação = brinde + avaliações.
  Receita = LTV combinado de hardware + acessórios + assinatura.
- **Marketplace** — Ativação tem dois lados (oferta + demanda). Retenção
  é frequência de transação repetida. Receita é taxa-de-comissão × GMV.
- **Ferramenta de desenvolvedor** — Aquisição se apoia em conteúdo
  técnico + DevRel + SEO de documentação. Ativação = primeiro build/
  primeira integração. Retenção = profundidade de integração. Indicação =
  adoção pelo time.

Detalhe em `references/client-types.md`.

## Padrão de qualidade

O que separa um bom plano de um genérico:

**Sinais de bom plano:**

- Todo movimento nomeia o estágio AARRR ao qual serve
- Toda recomendação é ancorada em dado real do cliente (orçamento real
  deles, time real deles, canais atuais reais deles)
- O roadmap de 90 dias tem responsáveis, não só ações
- A seção de estágio de captação explica o que muda quando a próxima
  rodada fecha
- A seção de stack de operação nomeia skills + MCPs específicos por
  movimento
- O banco de ideias mostra o que *não* estamos fazendo e por quê (ideias
  puladas com justificativa)
- O resumo executivo funciona sozinho — poderia ser reaproveitado em uma
  atualização de investidor
- Decisões em aberto são explícitas, não disfarçadas

**Modos de falha a evitar:**

- Listar táticas sem sequenciamento
- Recomendar coisas que o time não consegue executar no tamanho atual
- Fingir que orçamento pago existe antes de a rodada fechar
- Disfarçar métricas desconfortáveis (ex.: churn) em vez de nomeá-las como
  decisões em aberto
- Linguagem genérica ("construir uma comunidade," "melhorar SEO") sem
  movimentos específicos
- Ignorar voz de marca — toda seção do plano precisa respeitar as regras
  de voz do cliente
- Encher o plano com skills/ideias que o cliente não precisa de verdade
- Não reconhecer trabalho que o time já fez

## Formato de saída

O entregável final é um único arquivo markdown:
`~/marketing-plans/{slug-do-cliente}/final_plan.md`.

Cabeçalhos (`## 1. Resumo executivo`, etc.) são H2 para colar limpo no
Notion. Tabelas para qualquer comparação estruturada (RACI, banco de
ideias, stack de operação). Legenda de status para o banco de ideias.
Referências internas a outras seções usam `§N` (ex.: "veja §5 para
detalhe de Ativação").

Expectativa de extensão: ~8.000-12.000 palavras para um plano abrangente.
Mais curto é ok se o cliente é estágio inicial com pouca área de
superfície; mais longo é ok se o cliente tem anos de histórico a
reconhecer.

## Layout de arquivo por plano

```text
~/marketing-plans/
└── {slug-do-cliente}/
    ├── materials/         # Arquivos fornecidos pelo cliente (decks, saída de auditoria, doc de voz de marca, etc.)
    ├── research.md        # Registro de pesquisa escrito durante o INIT
    ├── progress.md        # Máquina de estado — fase, seção atual, artefatos aprovados, plan_version
    ├── sections/
    │   ├── 01.md          # Cada seção aprovada salva como artefato canônico
    │   └── ...            # Com zeros à esquerda para ordenar corretamente
    └── final_plan.md      # Entregável compilado (saída do FINALIZE)
```

O schema completo de `progress.md` e a árvore de decisão de retomada vivem
em `references/methodology.md` Passos 1.1.1 e 1.1.2.

## Skills relacionadas

- **`product-marketing`** — rode primeiro. Captura posicionamento, ICP, voz em `.agents/product-marketing.md` para que toda seção do plano referencie a mesma fundação.
- **`marketing-ideas`** — fonte das 139 táticas na Seção 12.
- **`customer-research`** — aprofunda o ICP e os inputs de voz-do-cliente que alimentam a Seção 2 (Quadro estratégico).
- **`onboarding`** — trabalho profundo na Seção 5 (Ativação).
- **`emails`** — trabalho profundo na Seção 6 (Retenção) + e-mails de onboarding na Seção 5.
- **`referrals`** — trabalho profundo na Seção 7 (Indicação).
- **`pricing`** — trabalho profundo na Seção 8 (Receita).
- **`seo-audit`** / **`ai-seo`** / **`programmatic-seo`** — trabalho profundo na parte de SEO da Seção 4 (Aquisição).
- **`ads`** / **`ad-creative`** — trabalho profundo na parte paga da Seção 4 assim que o orçamento desbloquear.
- **`launch`** — trabalho profundo em momentos de lançamento dentro da Seção 4/Seção 9.

## Perguntas específicas da tarefa (usadas durante o INIT)

O questionário de intake completo vive em `references/methodology.md`. As
perguntas mais importantes:

1. **Estado de captação** — em que rodada vocês estão? Quanto captado até
   agora? Burn? Runway? Próximas rodadas e timing?
2. **Time** — quem são todas as pessoas que tocam marketing? O que cada
   uma é dona? Onde estão as lacunas?
3. **Orçamento** — qual é o gasto mensal atual de marketing, detalhado
   por aquisição paga, ferramentas, retainers, quadro de pessoal? Que
   orçamento desbloqueia quando a próxima rodada fechar?
4. **Canais atuais** — o que está funcionando hoje? O que não está? O que
   vocês ainda não tentaram?
5. **Já feito** — que campanhas/lançamentos/conteúdo/momentos de PR
   passados esse plano deveria reconhecer?
6. **Em andamento** — o que está rascunhado mas não lançado? O que está
   bloqueando cada item?
7. **Stack de ferramental** — o que está conectado? Customer.io/
   Mailchimp/Resend? Shopify/Stripe/App Store Connect? GA4/Mixpanel/
   Amplitude? GitHub/Notion/Figma?
8. **Beta ou GA?** — se o produto está em beta, qual é o cronograma de GA?
   Throttling? Que portões existem?
9. **A coisa mais importante para consertar esse trimestre** — leitura do
   founder.
10. **A coisa mais importante para ignorar esse trimestre** — o que
    parece importante mas não é.

## Quão exaustivo o plano deveria ser?

Padrão para abrangente. Founders compartilham o plano com o time e
investidores; brevidade aqui é economia falsa. Um plano de 10 mil
palavras com a estrutura certa é mais útil que um plano de 3 mil palavras
que perde a stack de operação ou o banco de ideias.

Dito isso: não encha. Toda seção deveria ser **densa, não inchada**. Se
uma seção não tem nada a dizer, escreva isso explicitamente — "T4+ — jogo
longo/fora de escopo para esse plano de 12 meses" é honesto e útil.

## Uma nota sobre tom

Esse plano é escrito para founders que são perspicazes, ocupados, e
céticos de marketês. Escreva como um colega ponderado, não um
redator-de-slide-de-deck. Sem jargão por jargão. Afirmações diretas,
trade-offs nomeados, suposições explícitas. Quando incerto, nomeie a
pergunta em aberto em vez de chutar.

O resumo executivo deveria ser curto o suficiente para ler em 60 segundos.
O resto deveria recompensar leitura profunda.
