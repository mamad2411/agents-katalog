---
name: design-web-premium
description: >
  Crie designs de websites premium com qualidade Awwwards como componentes React (.jsx) que pareçam ter sido construídos por uma agência de primeira linha cobrando R$250k+ por projeto. Use esta skill sempre que o usuário pedir um website, landing page, portfólio, ou componente web que deve parecer caro, premium, luxo, editorial, high-end, ou de qualidade agência. Também dispare quando o usuário mencionar Awwwards, FWA, design premiado, ou referenciar marcas como Apple, Aesop, Bottega Veneta, Stripe, ou qualquer marca luxury/fashion/design-forward. Dispare quando o usuário disser coisas como "faça parecer profissional", "faça parecer caro", "quero que fique realmente bom", "design de alta qualidade", "não genérico", ou expressar insatisfação com aesthetics típicos de websites gerados por IA. NÃO dispare para dashboards, admin panels, ferramentas internas, ou UI funcional onde aesthetics são secundárias à utilidade — a skill padrão frontend-design cuida disso.
---

# Design Web Premium

Crie componentes React (.jsx) que pareçam pertencer ao Awwwards — o tipo de trabalho que faz as pessoas perguntarem "quem design isso?". Estes são sites onde cada pixel é intencional, cada animação é coreografada, e a impressão geral é que talento criativo sério e orçamento foram envolvidos.

## O Problema da Aesthetica IA

A maioria dos websites gerados por IA compartilham um DNA reconhecível. Evitá-lo requer saber exatamente como se vê.

### A Blacklist — Nunca Faça Isso

**Pecados tipográficos**
- Inter, Poppins, Montserrat, Raleway, Space Grotesk, Outfit como fontes principais — gritam "template de IA". (Nota: *Inter Tight* é uma família de fontes separada com métricas diferentes e é permitida.)
- Usar uma família tipográfica para tudo
- Tamanhos de fonte uniformes com hierarquia previsível (64px → 32px → 18px → 14px)
- Letter-spacing e line-height padrão em tudo
- Texto centralizado em blocos por toda parte, especialmente parágrafos com múltiplas linhas

**Pecados de cor**
- Gradientes roxo-para-azul (o maior cliché de design IA)
- Índigo/violeta como cor de marca primária sem razão contextual
- Fundo branco + uma cor de destaque + texto cinza (o kit inicial SaaS)
- Gradientes em botões ou cards sem razão
- Usar opacidade ou overlays semi-transparentes como substituto para escolhas de cor reais
- Cores neon em fundos escuros (o look "developer portfolio")

**Pecados de layout**
- Hero → grid de 3 colunas de features → testemunhos → CTA → footer (a landing page SaaS padrão)
- Hero → barra de stats → grid de trabalhos → split de sobre → CTA → footer (a "landing page premium IA" — igualmente formulaic)
- QUALQUER ordenação previsível de cima para baixo entre seções que poderia ser trocada entre sites. Cada site deve ter seu próprio DNA estrutural único — número diferente de seções, lógica de ordenação diferente, seções que não se encaixam perfeitamente em categorias
- Grids perfeitamente simétricos com cards de tamanho igual
- Tudo centralizado, tudo contido em um container max-width
- Retângulos arredondados com box-shadows como elemento UI principal
- Cards de icon + heading + parágrafo em linha de 3 ou 4
- Hero genérico com headline + subheadline + dois botões lado a lado
- Seções hero planas e estáticas com apenas texto — seções hero devem ser experiências espaciais imersivas

**Pecados de movimento**
- Elementos desaparecendo de baixo ao scroll (o efeito AOS sobreusado)
- Transições idênticas em tudo (mesma duração, mesmo easing, mesma direção)
- Hover effects que apenas aumentam ou adicionam sombra
- Spinners de loading em vez de skeleton screens ou reveals coreografados

**Pecados de imagery e decoração**
- Formas blob como decorações de background
- Formas geométricas flutuantes (círculos, triângulos) como "elementos de design"
- Fundos mesh gradient genéricos
- Grids de fotos de stock com aspect ratios uniformes
- Emoji ou ícones genéricos de linha como marcadores de seção

---

## O Que Realmente Caro Parece

Design web premium comunica craft através de restraint, surpresa, e atenção obsessiva aos detalhes.

### Tipografia como Identidade

Tipografia é o #1 diferenciador entre um website de R$2.500 e um de R$250.000.

**Filosofia de seleção de fontes:**
- Use fontes serif ou display distintivas para headlines — fontes com personalidade e opinião. Bons pontos de partida: *Playfair Display, Cormorant Garamond, DM Serif Display, Fraunces, Instrument Serif* para serifs. Para sans-serifs que não são sobreusados: *Syne, General Sans, Satoshi, Switzer, Cabinet Grotesk, Nacelle, Inter Tight, IBM Plex Sans, Manrope, Archivo, Work Sans, Instrument Sans*.
- Pair uma fonte display característica com uma fonte body neutral-mas-refinada.
- Fontes monoespacadas como tipografia de destaque (para labels, categorias, datas) adicionam qualidade editorial — *JetBrains Mono, IBM Plex Mono, Space Mono*.
- Mix weights dramaticamente — um headline de peso 900 próximo a um body de peso 300 cria tensão visual.

**Execução tipográfica:**
- `clamp()` para escala de tipo fluido ao invés de jumps de breakpoint
- Contraste de tamanho dramático — headlines podem ser 8vw+ no desktop
- Negative letter-spacing em headlines grandes (`-0.03em` a `-0.06em`)
- Line-height generoso em body (1.6–1.8), tight em headlines (0.9–1.1)
- Alinhamento misto — body alinhado à esquerda com occasional labels alinhados à direita ou headings assimétricos
- `max-width` em parágrafos (45–75ch) e `text-wrap: balance` em headings
- Uppercase micro-labels com wide letter-spacing (`0.1em`+) para categorias, datas, metadata

### Cor como Atmosfera

- Comece com preto e branco. Adicione cor apenas quando ela ganhar seu lugar.
- Uma hue dominante com intenção — "que território emocional esta cor reclama?"
- Off-whites e grays quentes (não puro `#ffffff` ou `#000000`) parecem mais designed — tente `#FAFAF8`, `#F5F0EB`, `#1A1A1A`, `#0D0D0D`
- Paletas monocromáticas ou análogas com um momento de contraste leem como mais sofisticadas que esquemas arco-íris
- Dark themes feitos certo: não apenas "white on dark gray" mas layering de background considerado com subtle warm ou cool tints
- Cor usada esparsamente bate mais forte — um único link vermelho em um mar de preto-e-branco é mais poderoso que vermelho em toda parte

### Layout como Narrativa

O #1 failure mode desta skill é produzir sites que *parecem diferentes na superfície mas compartilham a mesma estrutura subjacente* — um hero, três seções editoriais, uma pull quote, um form, um colophon. Ao longo de um lote de sites isso começa a parecer um template com cores diferentes. Combata isso ativamente, e deliberadamente.

**A regra de unicidade do DNA estrutural:**

Antes de escrever qualquer markup, **nomeie o conceito estrutural primário em voz alta** — uma frase nominal única, como *"índice manuscrito"* ou *"diorama horizontal sticky"*. Dentro de um lote de sites, **não há dois sites que compartilhem o mesmo conceito estrutural primário.** Se o site anterior era uma narrativa sticky-scroll, este não é. Se o site anterior era um split vertical 33/67, este não é. A ideia estrutural é a primeira coisa que o usuário nota — variar cor sem variar estrutura é cosmético.

#### Catálogo de DNA Estrutural

Estes são conceitos primários distintos. Cada invocação de skill deve escolher um conceito e se comprometer com ele. **Não misture duas estruturas em um site** (dilui ambas).

1. **Índice Manuscrito** — Uma única coluna editorial longa, sem seções. Um ritmo tipográfico do topo ao fundo. A página inteira lê como um único manuscrito que acontece de ser um website. (Bom para: menu de chef, carta de perfumista, manifesto.)
2. **Diorama Horizontal Sticky** — A página é um scroll vertical longo, mas *o que você vê enquanto scrolls* é uma cena pan horizontal. Use `position: sticky` + `translateX` driven por scroll. (Bom para: timeline de comissões, processo em estágios, coleção de artefatos.)
3. **Split Permanente de Duas Panes** — A página é sempre um split 50/50 (ou 38/62); uma pane é sticky, a outra scrolls. Navegação acontece dentro de uma pane, nunca pelo scroll da página inteira. (Bom para: arquivo com índice live-updating, catálogo de bibliotecário.)
4. **Sequência de Slides** — Slides de altura viewport-cheio, um por screen, com snap scrolling. Cada slide é uma composição completamente diferente. (Bom para: monografia de fotógrafo, walkthrough de galeria, look-book editorial.)
5. **Objeto Staged em um Plinth** — Um único sujeito 3D/imagem fica centralizado, rotacionável, e o resto da página é marginalia que orbita o objeto. (Bom para: casa de produto único — um relógio, um flacon, uma garrafa.)
6. **Narrativa Pinned (Scrollytelling)** — Uma seção de 2–4-screen-tall pina em lugar enquanto seus conteúdos avançam através de states discretos (image swaps, text swaps, progress). Usada *uma vez* na página como seu centerpiece. (Bom para: perfil de missão, processo de produção, estudo de colapso de construção.)
7. **Navegação Horizontal** — O scroll de página primário é horizontal. Seções leem esquerda-para-direita. Scroll vertical é desabilitado ou reservado para detail reveals. (Bom para: arquivo horológico, ala de museu, slate de estúdio de filme.)
8. **Sidebar + Column** — Uma sidebar persistente à esquerda nunca scrolls (navegação, metadata, running footer); a coluna direita é o site inteiro. (Bom para: prática legal, instituto de pesquisa, editora académica.)
9. **Chapter Gates** — Full-viewport dividers de capítulo entre zonas tonais muito diferentes. Cada capítulo tem sua própria cor de background, peso tipográfico, e rhythm de layout. A página *muda de carácter* enquanto desces. (Bom para: estúdio multi-discipline, retrospectiva.)
10. **Ledger / Registry** — A página é apresentada como um documento old-school — um bill of lading, um registry, um ship's manifest. Linhas tabulares dominam; tipografia lê como um ledger. (Bom para: waiting list, batch register, expedition manifest.)
11. **Collage / Grid-Breaker** — Um grid de revista-estilo assimétrico com ruptures deliberadas — imagens oversized sangrando em colunas, pull-quotes cruzando gutters, footnotes nas margens. (Bom para: publicações editoriais, revistas culturais, estúdios criativos.)
12. **Objeto Único, Sem Chrome** — O site é *apenas* o sujeito, rotacionável, com uma única frase curta abaixo. Sem nav, sem footer, quase sem UI. (Bom para: release single de artista, work de statement.)
13. **UI de Produto Slate** — O hero é uma simulação realista da interface do próprio produto (tiles de dashboard, diff view, command palette). Usado por brands tech/AI cuja produto É uma UI. (Bom para: IDEs AI, dev tools.)
14. **Grid de Tile Dashboard** — Toda a página é estruturada como um live-feeling dashboard com live counters, sparklines, pulsing pips. (Bom para: infra, cybersecurity, observability.)
15. **Timeline de Conversa** — A página reproduz uma conversa/transcript/call simulada conforme o usuário scrolls. Feature callouts ancoram a moments específicos. (Bom para: voice AI, support platforms, legal interviews.)

**Como escolher o conceito:**
- Comece do fato central do cliente. Um restaurante cuja identidade inteira é um menu de nove pratos quer um *Índice Manuscrito*. Um relogeiro cuja identidade é precisão e um único calibre quer um *Objeto Staged em um Plinth*. Uma empresa de expedições cuja marca é uma jornada anual quer uma *Narrativa Pinned*.
- Rejeite o conceito se for o usado pela última vez nesta sessão. Escolha o próximo-melhor.
- Escreva o conceito e uma sentença de justificação *antes* de escrever qualquer JSX. Mantenha visível no arquivo prompt.

**Princípios de layout (aplicar dentro de qualquer conceito estrutural que você escolha):**
- Quebre o grid intencionalmente. Momentos full-width seguidos de colunas de texto narrow. Imagens oversized sangrando off-screen. Splits assimétricos de duas colunas (60/40, 70/30).
- Espaço em branco generoso não é espaço desperdiçado — é um sinal de luxo. Padding de `8rem`+ entre seções.
- Seções de scroll horizontal para portfolios ou galerias (feitas bem, não como padrão de navegação principal — a menos que você deliberadamente escolha *Navegação Horizontal*).
- Elementos overlapping — texto sobre imagens, imagens quebrando out of their containers, elementos que cruzam section boundaries.
- Elementos sticky que acompanham o scroll — um label que fica enquanto conteúdo scrolls past.

**Micro-patterns específicos que leem como premium:**
- Masonry ou staggered grids para conteúdo visual ao invés de grids uniformes.
- Texto que overlaps imagens com mix-blend-mode para efeito editorial.
- Seções numeradas ou indexadas com progressão visível.
- Um visible grid system (subtle lines ou columns) que o design ocasionalmente quebra.
- Conteúdo que transforma conforme você scrolls past ele — não apenas aparecendo, mas morphing, scaling, repositioning.
- Linhas tabulares / ledger para listas (batches, manifests, registries) ao invés de card grids.
- Form fields que parecem partes de um documento editorial, não um SaaS form — labels em small monospace acima de serif inputs, sem outlines, apenas bottom-borders.

**Bans de repetição (dentro de uma sessão de skill):**
- Não dê a dois sites ambos uma seção de processo *"coluna esquerda sticky + coluna direita scrolling"*. Escolha para um; invente outra coisa para o outro.
- Não abra dois sites com um *hero assimétrico 33/67*. Se um fez, o próximo abre com um stage centralizado, ou um backdrop full-bleed, ou um ledger, ou sem hero nenhum.
- Não termine dois sites com o mesmo par "enquiry form + grid de colophon". Varie o closing move.

**Variedade de nav-bar — um failure mode silencioso para observar.**

O padrão mais fácil é um `grid-template-columns: auto 1fr auto` top bar com "brand mark à esquerda, algo centrado, algo alinhado à direita, mix-blend-mode: difference". Após três sites, começa a ler como uma assinatura — não uma escolha de design. Em cada sessão, **varie a nav substancialmente**:

- *Sem nav nenhuma* (Single Object, No Chrome brands).
- *Nav incorporada no sticky sidebar* (Sidebar + Column brands).
- *Bottom-fixed command bar* estilizada como `⌘K` launcher (tech-product brands — Cursor / Linear / Arc).
- *Inline centred wordmark* com tabs spread beneath como strip secundária.
- *Full-width horizontal scroll index* que funciona também como nav.
- *Marquee nav* — ticker continuamente scrollando com section names.
- *Left-vertical nav* escrita bottom-to-top.
- *Status-bar nav* com um live-operational pip.
- *Strip marquee-ticker* (preços benchmark, métricas) plus um slim top bar.

Escolha a nav que pertence à marca e ao DNA estrutural — não padrão ao three-column top bar.

**Evite o default editorial-luxo.**

Esta skill gravita, sob pressão, para: ground cream quente, serif display (Fraunces / Cormorant), monospace metadata, um único accent brass, wide-tracked uppercase micro-labels, `◦` bullet symbols. É uma aesthetica real, apropriada para couture, parfumerie, haute cuisine, horlogerie. NÃO é apropriada para tech, AI, cybersecurity, eletrônicos de consumidor, SaaS, ou developer tooling — e repetidamente defaultar a ela faz cada site em um lote parecer que a mesma agência fez.

**Se o campo é tecnologia**, a aesthetica deveria skew para: grounds pure-white ou near-black (não cream); neo-grotesque sans-serifs (Söhne-feel, Inter Tight, IBM Plex Sans, Instrument Sans) como display type; monospace usado como *display*, não apenas metadata; gradient-glow edges, shipped UI screenshots, live-feeling dashboard tiles, keyboard-shortcut chips inline com copy, code blocks renderizados como hero, texturas iridescent/chrome/glass ao invés de brass-and-paper. Veja Vercel, Cursor, Linear, Windsurf, Stripe, Figma, Arc, Zed, Raycast, Supabase, v0.dev, Anthropic, OpenAI.

### 3D Components — O Diferenciador Core

Cada website construído com esta skill apresenta 3D components. Isto é o que faz estes sites se destacarem de designs planos. Mas o 3D deve parecer profissional e polished — 3D amador é pior que nenhum 3D.

**NÃO construa objetos 3D de primitivos geométricos Three.js** (boxes, cylinders, cones, esferas). Carros construídos de boxes parecem brinquedos. Rockets construídos de cylinders parecem diagramas. Fogo construído de cones parece horrível. Primitivos Three.js são aceitáveis apenas para subtle atmospheric background effects (particle fields, grid planes, floating dots) — nunca como visual hero principal.

#### Passo 1: Pesquise a Indústria — Profundamente

A maioria dos sites "premium" gerados por IA parecem genéricos porque o passo de pesquisa é pulado ou feito com profundidade de duas sentenças. Um real reference pull é o single biggest quality lever nesta skill.

**Requisito de profundidade:** Estude **pelo menos 5** sites de referência reais (não 2) — um mix dos industry leaders mais óbvios *e* operadores editoriais/culturais menos famosos no mesmo espaço. As referências menos famosas são geralmente onde os unique moves vêm; as famosas ancoram a palette.

**Starter reference sets (expanda, não pare aqui):**

- **AI tooling / dev tools / IDEs** → **Vercel**, **Cursor**, **Windsurf**, **Linear**, **Stripe**, **Figma**, **Arc Browser**, **Zed**, **Raycast**, **Supabase**, **Replit**, **v0.dev**, **Anthropic**, **OpenAI**. Nota: **dark-first ou pure-white**, **monospace usado como display** (não apenas metadata), **grids precisos**, **keyboard-shortcut chrome** (`⌘K`, `⌘↵`), **gradient glow edges**, **animated code blocks em hero**, **dashboard-tile grids**, **sub-section headers em small-caps monospace**, **`<code>`-styled callouts**. Interactive hero frequentemente = um animated product UI snapshot, não uma still image.
- **Cybersecurity / infrastructure** → **Cloudflare**, **Tailscale**, **1Password Business**, **Chainguard**, **CrowdStrike**, **Datadog Security**, **HashiCorp**, **Teleport**. Nota: **scanning-beam hero animations**, **tessellated defensive grids**, **live-feeling status indicators**, **green/amber "operational" pips**, **data-density densa sobre whitespace**.
- **Enterprise AI / voice** → **Anthropic**, **OpenAI Platform**, **ElevenLabs**, **Vapi**, **Retell AI**, **Bland AI**, **Cohere**, **Deepgram**, **Cartesia**. Nota: warm near-black grounds, serif display editorial, live transcripts como hero, latency numbers como elementos tipográficos.
- **Aerospace / Defense** → SpaceX, Rocket Lab, Blue Origin, Sierra Space, Axiom, The Planetary Society, Royal Aeronautical Society. Nota: dark themes, clean sans-serifs, full-bleed photography, mission-profile diagrams, minimal color accents.
- **Automotive** → Porsche, Rivian, Lucid, Singer Vehicle Design, Pagani, David Brown Automotive, Coachbuild.com. Nota: dramatic product photography, mechanical drawings, full-screen immersive heroes.
- **Fashion / Luxury** → Bottega Veneta, Celine, The Row, Margiela, Lemaire, A.P.C., Phoebe Philo, Hermès. Nota: extreme typographic restraint, serif display, near-silent whitespace.
- **Food / Restaurants** → Noma, Eleven Madison Park, Alinea, Central (Lima), Atomix, Chefs Club, René Redzepi's archive. Nota: editorial photography, muted tones, menu-as-manuscript typography, course-by-course pacing.
- **Fragrance / Parfumerie** → Le Labo, Byredo, Frédéric Malle, Lubin, Maison Francis Kurkdjian, Diptyque, Santa Maria Novella.
- **Architecture** → 2x4, Olson Kundig, Herzog & de Meuron, Kengo Kuma, SANAA, David Chipperfield.
- **Horology** → F.P. Journe, A. Lange & Söhne, Philippe Dufour, Akrivia, Grönefeld, Urban Jürgensen.
- **Art / Galleries** → David Zwirner, Gagosian, Hauser & Wirth, Galerie Lelong, White Cube, Pace.
- **Publishing / Editorial** → New York Review of Books, Granta, The Paris Review, Apartamento, Zeit Online, MIT Press.
- **Music / Record Labels** → ECM Records, Warp, Mute, Nonesuch, Erased Tapes, Kompakt, Sub Pop.
- **Private Wealth / Fintech** → Addepar, Masttro, Pictet, Edmond de Rothschild, BlackRock Aladdin, Stripe.

**Como fazer o passe de pesquisa:**

1. **Encontre os 5 sites.** Use `web_search`: `"[field] award-winning website"`, `"[field] Awwwards"`, `site:awwwards.com [field]`, `"[field] FWA winner"`. Pelo menos 2 dos 5 devem ser referências editoriais/culturais menos óbvias, não os gigantes da indústria.
2. **Estude cada um com `web_fetch`.** Puxe patterns, não vibes. Para cada site, note especificamente: primary display font, secondary body font, palette como approximate hexadecimal, structural DNA (qual conceito do catálogo), um signature move único para esse site.
3. **Escreva um design brief de 6–10 linhas antes de codificar.** No prompt.md, escreva um bloco "Design reference pull" nomeando os 5 sites, os 3 padrões específicos que você está borrowing (e de qual site), a palette (em hex), o font stack, e o DNA estrutural que você escolheu.
4. **Não copie — combine.** Puxe uma coisa de cada referência; a combinação é o que faz o site parecer original ao invés de um clone.

O design que você constrói deve parecer que pertence ao lado destes competidores reais — não como que veio de um universo diferente, e não como um carbon copy de qualquer um.

#### Passo 2: Fonte Topic-Relevant 3D do Spline

**Spline (spline.design)** é uma platform de 3D design com uma grande biblioteca comunitária de cenas 3D profissionais e embeddable. Uma cena Spline somente ganha seu lugar em um site premium se um visitante, dando uma olhada nela, imediatamente entenda *o que ela representa*. Uma bela cena que nada tem a ver com o sujeito é **pior** que nenhuma cena — erode o sentido que todo pixel é intencional, e lê como "algum 3D legal que o designer encontrou," que é o oposto de premium.

##### Nunca cenas de produtos reais branded — nunca

Cenas da comunidade Spline frequentemente retratam **produtos reais, trademarked**: um Nike Air Jordan, um Sony WH-1000XM5, um Apple Watch, um Beats Studio, um Samsung Galaxy, um Tesla Cybertruck. **Estes não são usáveis para um website de uma marca fictícia.** Usá-los cria três problemas compostos:

1. **Legal.** Produtos reais branded têm trademarks, design patents, e licensing agreements. Colocar um Nike shoe em um website para uma fictícia marca "Trio Nord" de footwear é confusão de trademark na melhor das hipóteses, e infringement na pior.
2. **Narrativo.** Um viewer que reconheça o produto — e a maioria reconhecerá — imediatamente sabe que o site está mentindo. No momento em que esse reconhecimento acontece, a ilusão de luxo colapsa.
3. **Genérico.** Uma cena que existe *porque* um Nike designer ou Sony visualizer a fez lê como "alguém no Spline recriou um produto famoso." Nunca lê como *nosso* produto.

**Regra:** Antes de se comprometer com uma cena Spline, pergunte: *A objeto nesta cena é um produto real, identificável, de uma marca real?* Se sim — rejeite, não importa o quão bem-renderizado. Procure por cenas **abstratas, category-representative, ou de design original** ao invés:

- Ao invés de Nike Air Jordan → um generic hand-lasted leather shoe, ou uma abstract footwear silhouette.
- Ao invés de Sony headphones → abstract floating audio-ring geometry, ou uma generic minimalist over-ear.
- Ao invés de Apple Watch → um unbranded bezel/dial, ou um mechanical-movement diagram.

Se nenhuma alternativa non-branded existe para o sujeito, ou (a) caia para trás em photography de um generic, unbranded product, (b) construa uma SVG illustration, ou (c) escolha um campo diferente.

##### Field-first, não scene-first — a direção de sourcing importa

Um fácil failure mode: você tem uma usável Spline URL em mão, e você inventa um field para justificar usá-la. Isto lê como desespero. "Um fabricante de tinta de caneta-tinteiro" não existe como uma marca premium no mundo porque alguém quis — existe porque você tinha uma dark-fluid scene e construiu uma house of cards ao redor disso. O prompt a expõe.

**A ordem correta é:**

1. **Escolha o field.** Uma real, plausível luxury / premium industry — automotive, horology, haute couture, fragrance, spirits, footwear, audio, eyewear, furniture, hospitality, leather goods, cutlery, skincare, private medicine, etc. O field deve ser um que o usuário, mostrado o site terminado, imediatamente aceitaria como um negócio real. Tinta de caneta não é.
2. **Defina o produto dentro do field.** O que, especificamente, é o sujeito? Um anel, um sneaker, um set de over-ear headphones, uma chef's knife.
3. **Então procure Spline por esse produto.** Com a keyword-map expansion. Use ambas as URLs `my.spline.design/` e `prod.spline.design/`.
4. **Se nenhuma cena topic-relevant existe, mude field — não dobre o field para match uma scene que você já tem.**

Um saudável lote de sites abrange genuinely-different industries um reader reconhece. Um lote de sites cujo shared thread é "qualquer field que os disponíveis Spline URLs implicam" não é um portfolio — é uma rationalização.

##### Unicidade de cena — sem reuso dentro de uma sessão

**Dentro de uma única sessão / lote de sites, nenhum dois sites podem usar a mesma Spline scene URL.** Reusar uma cena entre múltiplas casas lê como uma biblioteca stock-photo mostrando-se, e desfaz o reivindicação inteira da SKILL que cada site é sua própria identidade.

- Se você usou `worldplanet` em um site, não use em próximo, não importa o quanto diretamente "fit" o novo field. Encontre uma cena diferente.
- Se você não pode encontrar uma cena única para o novo field, **caia para trás em photography** ou uma deterministic SVG/CSS illustration — nunca recicle.
- Mesmo cenas que pareçam intercambiáveis (duas cenas Earth diferentes, duas cenas fluid diferentes) não devem aparecer em um lote. Uma cena Earth por lote. Uma cena fluid por lote.
- No topo de cada novo `prompt.md`, liste as Spline URLs já usadas nesta sessão pelos sites anteriores. Confirme a URL do novo site NÃO está naquela lista.

##### A regra cardeal: topic-literal, não topic-metaphorical

Uma cena Spline é aceitável apenas quando ela **literalmente retrata o sujeito do site's brand.** Links metafóricos são rejeitados, mesmo se forem poéticos:

- Uma fluid scene é fine para um **ink maker** (o fluid É tinta)