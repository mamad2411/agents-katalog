---
name: termos-ui-ux
description: Traduz "problema de tela" em pedido técnico de UI/UX. Pega o que a pessoa descreve com as próprias palavras ou mostra num print ("sobra espaço vazio do lado", "o botão some quando eu rolo", "os cards ficam um em cima do outro", "no celular a tabela sai pro lado", "a foto ficou esticada", "o menu abre atrás", "não sei o nome disso"), acha o termo técnico certo, explica em linguagem simples e devolve um prompt pronto para colar em qualquer IA de programação, com as restrições que impedem a IA de quebrar a tela. Também audita um print, especifica uma tela nova e revisa pedidos. Use sempre que alguém quiser mudar, corrigir ou criar a aparência ou o comportamento de uma tela, site, landing page, dashboard, formulário, tabela, card, botão ou menu e não souber explicar tecnicamente; quando perguntar "o que é X" sobre layout/design; ou quando disser que a IA "não entende" o que quer no visual. Works in English too (UI/UX terms, "fix my layout" requests).
---

# Termos de UI/UX: do problema ao pedido certo

Muita gente sabe **o que** está errado na tela, mas não sabe **como pedir**. Quando o pedido é vago ("deixa mais bonito", "arruma o layout", "deixa responsivo"), a IA de desenvolvimento chuta, muda o que não devia e quebra o que estava certo. Esta skill fecha essa lacuna: traduz o sintoma para o termo técnico, ensina o termo em uma linha e entrega um pedido completo que a IA consegue executar sem estragar o resto.

**UI** é a aparência e a organização da interface. **UX** é como a pessoa entende, navega e conclui uma tarefa. Um bom pedido descreve os dois: como deve parecer e como deve funcionar.

## Quem vai ler sua resposta

Na maioria das vezes, quem usa esta skill **não programa**. Escreva de forma simples e **no idioma da pessoa**: se ela escrever em inglês ou espanhol, traduza também os rótulos do formato de saída (os termos técnicos já são em inglês). Sempre que aparecer um termo técnico, explique ao lado, em poucas palavras e com algo do dia a dia ("*sticky*: gruda no topo enquanto o resto rola"). O prompt pronto pode (e deve) conter os termos técnicos e até CSS, porque ele é para a IA ler, não para a pessoa. Já a explicação em volta dele é para a pessoa.

## Modos de uso

Descubra pelo pedido qual destes a pessoa quer. Na dúvida, use o modo 1.

### 1. "Tenho um problema na tela" → pedido pronto (modo principal)

1. **Entenda o sintoma.** Leia a descrição e/ou o print. Use o **Índice de sintomas** abaixo para chegar a 1–3 termos. Se nenhum encaixar, procure no `references/16-glossario-checklist.md` ou nos arquivos do capítulo mais próximo.
2. **Abra o arquivo de referência** de cada termo escolhido e use o conteúdo dele (o "Peça assim", o "Cuidado" e, se ajudar, o exemplo técnico). Não invente termos que não estão lá. O guia foi pensado para que cada termo leve a um comportamento concreto.
3. **Veja se falta algo essencial.** O que mais importa é: qual tela, o que está errado e o que já está certo. Se faltar, faça **no máximo 1–2 perguntas** curtas. Se a pessoa estiver com pressa, entregue mesmo assim, com `[colchetes]` onde ela deve completar.
4. **Entregue no formato de saída** descrito mais abaixo.

### 2. "O que é X?" → explicação

Os arquivos de referência são técnicos. Aqui o seu trabalho é traduzir, com uma analogia do dia a dia quando ajudar. Use esta estrutura:

```
**[Termo]** ([tradução, se for inglês]): [o que é, em 1–2 frases simples + analogia]

**Você vai querer isso quando** [situações concretas que a pessoa reconhece na tela].

**Diferença que costuma confundir:** [só se houver par: sticky x fixed, disabled x read-only, wrapping x truncation, responsive x adaptive, tabs x stepper, modal x drawer]

**Peça assim (para a IA):**
> [o "Peça assim" do guia, adaptado com um exemplo]

**Cuidado:** [o "Cuidado" do guia, em linguagem simples, se houver]
```

### 3. "Revisa meu pedido" → checklist

A pessoa cola um pedido que já escreveu. Compare com o checklist do `references/16-glossario-checklist.md`, aponte o que falta em linguagem simples e devolva a versão melhorada no formato de saída.

### 4. "Olha meu print" → auditoria

A pessoa manda um print e pergunta "o que está errado?" ou "o que dá para melhorar?". Olhe a imagem com atenção e liste os problemas que **realmente aparecem nela**, sem chutar o que não dá para ver (se é hover, código ou comportamento no celular, diga que precisa conferir). Ordene por impacto:

1. **Quebrado**: sobreposição, texto cortado, rolagem lateral, conteúdo inacessível.
2. **Atrapalha a tarefa**: ação principal escondida ou sem destaque, falta de feedback, pessoa sem saber onde está.
3. **Acabamento**: espaçamentos irregulares, hierarquia fraca, cores e fontes inconsistentes.

Para cada item, dê uma linha: *o que se vê → termo → arquivo*. Limite a ~7 itens. Mais do que isso vira lista de desejos. Depois entregue **um pedido pronto para o item mais grave** e diga que os outros vêm em seguida, um de cada vez. Motivo: uma mudança de layout por pedido é muito mais segura. Pedidos com dez correções ao mesmo tempo são os que mais quebram a tela. Se a pessoa quiser tudo de uma vez, junte em um pedido numerado, com um único bloco de Preserve, Não use e Validação.

### 5. "Quero criar uma tela" → especificação

Quando a pessoa quer **criar** algo novo ("quero uma tela de pedidos", "uma landing page para minha pousada"), não há defeito para descrever. Use o formato de especificação abaixo. Para sites, use 17-sites-landing e 18-imagens-midia. Para sistemas, use 01 a 09. Faça no máximo 2 perguntas sobre o conteúdo (o que a tela precisa mostrar e qual ação importa mais). O resto você sugere.

Os **estados** são o que quase todo mundo esquece. Em sistemas, são os de 12-estados (carregando, vazio, erro, sucesso). Em sites, são os do formulário e do CTA (enviando, enviado, erro), o carregamento das imagens sem a página pular e o fallback do vídeo.

```
**O que você quer:** [a tela ou o site em 1 frase, e para quem]

**Termos que vão aparecer:** [3–6 termos com explicação curta]

**Pedido pronto (copie e cole na sua IA de programação):**

> Crie **[a tela/página]** para [público e objetivo]. A ação principal é **[CTA]**.
> **Estrutura, em ordem de importância:**
> 1. [área/seção] — [o que mostra] ([termo])
> 2. …
> **Desktop:** [composição]. **Mobile:** [o que empilha, o que vira carrossel ou menu].
> **Estados:** [carregando / vazio / erro / sucesso aplicáveis].
> **Conteúdo que eu vou fornecer:** [textos, fotos, logo, dados]. Não invente dados, avaliações nem números.
> **Não use:** [lista padrão]. **Validação:** [bloco padrão, com os critérios desta tela].

**Antes de enviar, complete:** [os colchetes]
```

### 6. "Pode aplicar" → executar no código (só quando pedirem)

Se você estiver dentro de um projeto de código e a pessoa pedir para você mesmo fazer a mudança, siga o prompt que você montou como se fosse para você: mude só o escopo combinado, respeite a lista de proibições e valide olhando a tela renderizada (print) nas resoluções combinadas antes de dizer que terminou. Nunca faça isso por conta própria. O padrão é entregar o pedido.

## Formato de saída (modos 1, 3, 4 e 5)

Use esta estrutura. Ela é curta de propósito: a pessoa precisa entender e copiar.

```
**O que está acontecendo:** [o sintoma traduzido em 1–2 frases simples]

**Nome técnico:** [termo 1] — [explicação em linguagem do dia a dia]
[termo 2, se houver] — [explicação]

**Pedido pronto (copie e cole na sua IA de programação, junto com o print da tela):**

> Na tela **[nome da tela]**, [problema atual e impacto].
> Aplique [termo técnico]: [comportamento esperado, com o "Peça assim" do guia adaptado ao caso].
> **Preserve:** [o que já está certo e não pode mudar].
> **Desktop:** [comportamento]. **Mobile:** [comportamento].
> **Não use:** transform: scale(), zoom, fontes minúsculas, position: absolute para montar a estrutura, margens negativas, overflow: hidden só para esconder o defeito (é permitido no contêiner externo quando existe uma área interna que rola, e para recortar mídia com cantos arredondados), nem alturas fixas menores que o conteúdo. [+ cuidados específicos do termo]
> **Validação:** não considere concluído só porque compilou. Renderize a tela e confira prints em [1366x768, 1440x900, 1920x1080, a resolução do monitor/print da pessoa e um celular ~390px]. Confirme: nada sobreposto, nenhum texto cortado, nenhuma rolagem horizontal, [critério específico do pedido]. Informe os arquivos alterados e a causa raiz do problema.

**Antes de enviar, complete:** [lista curta dos colchetes que a pessoa precisa preencher, se houver]
```

Por que cada parte existe:
- **Preserve** e **Não use**: é o que mais evita que a IA "resolva" o problema estragando outra coisa (por exemplo, virar o dashboard inteiro em uma coluna só ao tirar um limite de largura, ou encolher tudo com zoom para caber).
- **Desktop / Mobile**: "responsivo" sozinho não diz nada. A IA precisa saber o que muda e em que tamanho de tela.
- **Validação**: sem critério objetivo, a IA declara vitória sem olhar a tela.

Quem não é técnico quase nunca diz o que está certo. Se a pessoa não disser, use um **Preserve padrão seguro**: "a organização atual dos componentes, cores, fontes e o comportamento das outras telas", e peça no "Antes de enviar" que ela complete se quiser. Se a tela for enorme (ultrawide) ou o problema aparecer "só no meu monitor", inclua essa resolução na validação: muitos defeitos só aparecem nela.

**A validação muda conforme o tipo de problema.** Não copie sempre as mesmas cinco resoluções. Pergunte-se como o defeito poderia voltar:
- **Layout, grid, largura:** as resoluções padrão + a do print.
- **Scroll:** a lista com poucos e com muitos itens; o último item não pode ficar coberto.
- **Camadas (menu atrás, cortado):** abrir o elemento perto da borda inferior, dentro de um modal rolado e no celular.
- **Formulário:** enviar vazio, com erro e com sucesso; navegar só com o teclado.
- **Imagens:** fotos em retrato e em paisagem, e uma foto bem pequena.
- **Celular:** um iPhone (Safari) e um Android reais ou emulados, com o teclado aberto quando houver digitação.

**Em inglês**, use estes blocos no lugar dos padrões:
> **Don't use:** transform: scale(), zoom, tiny fonts, position: absolute to build the structure, negative margins, overflow: hidden just to hide the defect (fine on an outer container that has an inner scrolling area, or to clip media with rounded corners), or fixed heights smaller than the content.
> **Validation:** don't consider it done just because it compiles. Render the screen and check screenshots at [resolutions]. Confirm: nothing overlaps, no text is cut off, no horizontal scroll, [request-specific criteria]. List the changed files and the root cause.

Adapte ao caso. Se o problema é só em botões ou textos (hierarquia, estados, mensagens de erro), a parte de resoluções pode ser mais curta. Se não há diferença entre desktop e mobile, diga isso em uma linha. Mas nunca tire o **Preserve**, o **Não use** e a **Validação** em pedidos de layout, grid, scroll ou responsividade.

## Fórmula do pedido (a base de tudo)

1. **Contexto:** qual tela ou componente muda.
2. **Problema atual:** o defeito visível e o impacto.
3. **Termo técnico:** o padrão de UI/UX desejado.
4. **Comportamento:** o que acontece no desktop e no mobile.
5. **Restrições:** o que não pode ser quebrado, cortado ou removido.
6. **Critérios de aceite:** como provar que ficou certo.

**Regra de ouro:** não peça só para deixar "bonito", "moderno" ou "responsivo". Diga qual estrutura deve existir, como cada área se comporta, o que não pode mudar e como o resultado será validado.

## Índice de sintomas

Frases como as pessoas falam → termo → onde está o detalhe (`references/`). Em geral, um sintoma leva a um termo principal e mais um ou dois de apoio.

### Espaço, largura e altura da tela
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "sobra um espaço vazio enorme do lado direito", "o conteúdo fica espremido no meio do monitor" (sistema/painel) | Full-width fluid layout | 01-layout |
| o mesmo, mas num **site** com texto corrido | Content container + Readable line length (em site, largura limitada é o certo para texto) | 17-sites-landing |
| "todas as páginas têm o mesmo problema de largura/altura" | App shell | 01-layout |
| "tenho que diminuir o zoom pra ver a tela toda", "queria que coubesse no monitor" | Fit-to-viewport | 01-layout |
| "o atendente perde os botões lá embaixo", "tela de caixa/pedido/atendimento precisa de tudo à vista" | Single-screen layout | 01-layout |
| "a barra lateral não vai até embaixo", "sobra espaço em branco no rodapé" | Full-height app shell | 01-layout |
| "no celular fica só uma versão encolhida do computador" | Responsive x Adaptive layout | 01-layout |
| "tem espaço demais, queria ver mais informação de uma vez" | Compact UI / High-density | 01-layout |
| "a IA deixou tudo pequenininho pra caber" | Compact UI (densidade ≠ miniaturização) | 01-layout |

### Colunas, alinhamento e coisas se encavalando
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "quero a lista de um lado e o painel do outro", "dividir a tela em colunas" | CSS Grid | 02-grid |
| "o título e os botões do cabeçalho ficam desalinhados" | Flexbox | 02-grid |
| "um texto grande empurra a coluna pra fora da tela" | minmax(0, 1fr) + min-width: 0 | 02-grid |
| "os cards não se ajeitam sozinhos conforme o tamanho da tela" | repeat(auto-fit, minmax()) | 02-grid |
| "o espaço entre os itens é diferente em cada lugar" | Gap | 02-grid |
| "nome comprido empurra o preço pra fora do card" | min-width: 0 (02-grid) + Wrapping x Truncation (10-responsividade) | 02-grid, 10-responsividade |
| "os filtros invadem o título quando a tela é menor" | Flex-wrap | 02-grid |
| "um card fica em cima do outro", "linhas se sobrepõem", "texto por cima de texto" | Normal document flow + Content-driven height (+ Responsive card grid se forem cards) | 14-nao-quebrar, 04-cards; prompt #8 em 15-prompts-prontos |

### Rolagem (scroll)
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "a página inteira desce e o menu/cabeçalho some" | No page-level scrolling | 03-scroll |
| "queria que só a lista rolasse" | Controlled internal scrolling | 03-scroll |
| "quando chego no fim da lista a página de trás começa a rolar" | Scroll containment | 03-scroll |
| "aparecem duas (ou três) barras de rolagem" | Avoid nested scrollbars | 03-scroll |
| "tem coisa cortada / transbordando / uma rolagem que não devia" | Overflow management | 03-scroll |
| "quero que o cabeçalho fique parado enquanto rolo", "o cabeçalho fixo cobre o conteúdo" | Sticky x Fixed | 03-scroll |
| "a lista com milhares de itens trava" | Virtualized list | 03-scroll |
| "a tela treme pro lado", "rola pro lado no celular" | No horizontal scrolling | 10-responsividade |

### Cards
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "o card é uma bagunça de informação", "botões misturados com o texto" | Card anatomy | 04-cards |
| "cards ficam estreitos demais / empilham cedo / deixam buracos" | Responsive card grid | 04-cards |
| "os cards da mesma linha têm alturas diferentes", "os botões não ficam alinhados" | Equal-height cards | 04-cards |
| "quero caixinhas com os números do painel (total, vendas, %)" | KPI / Stat card | 04-cards |
| "não dá pra saber que o card é clicável / qual está selecionado" | Interactive card states | 04-cards |
| "tudo no card tem o mesmo tamanho, não sei pra onde olhar" | Content hierarchy inside cards | 04-cards |

### Botões e ações
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "todos os botões são iguais, não sei qual é o principal" | Action hierarchy | 05-botoes |
| "cliquei em salvar e não aconteceu nada / cliquei duas vezes e salvou duas" | Button states (loading) | 05-botoes |
| "o botão Salvar some quando eu rolo", "tenho que descer tudo pra salvar" | Sticky action bar | 05-botoes |
| "tem um ícone que ninguém sabe o que faz", "o botão é pequeno demais pra clicar" | Icon button with accessible label + Touch target | 05-botoes / 13-acessibilidade |
| "apaguei sem querer", "o 'tem certeza?' não diz nada" | Destructive action confirmation | 05-botoes |

### Formulários
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "o nome do campo some quando eu começo a digitar" | Persistent label | 06-formularios |
| "o usuário não sabe o formato certo", "o erro só aparece no final", "o erro é só uma borda vermelha" | Helper text + Inline validation | 06-formularios |
| "não dá pra ver se o campo está bloqueado, com erro ou preenchido" | Form field states | 06-formularios |
| "o formulário fica espremido em duas colunas no celular" | Responsive form layout | 06-formularios |
| "não sei se uso caixinha, bolinha, chave liga/desliga ou lista" | Control selection | 06-formularios |
| "o campo está cinza e não dá nem pra copiar o valor" | Disabled x Read-only | 06-formularios |
| "o formulário tem campos demais, assusta" | Progressive disclosure | 06-formularios |

### Navegação e "onde eu estou?"
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "o menu lateral muda de lugar / some", "no celular o menu ocupa tudo" | Persistent sidebar | 07-navegacao |
| "quero separar Todos / Ativos / Inativos na mesma tela" | Tabs | 07-navegacao |
| "o usuário se perde em telas dentro de telas" | Breadcrumbs | 07-navegacao |
| "não dá pra saber qual menu/aba/filtro está selecionado" | Active state | 07-navegacao |
| "a lista é enorme, queria dividir em páginas" | Pagination | 07-navegacao / 08-tabelas |

### Tabelas e listas
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "a tabela está feia/confusa, números desalinhados" | Data table | 08-tabelas |
| "rolo a tabela e esqueço o que é cada coluna" | Sticky table header | 08-tabelas |
| "no celular a tabela sai pro lado / fica ilegível" | Column priority (+ No horizontal scrolling) | 08-tabelas |
| "cada linha tem botões demais" | Row actions | 08-tabelas |
| "não entendo por que aparecem poucos resultados", "não sei quais filtros estão ligados" | Search, filters and filter chips | 08-tabelas |
| "paginação, rolagem infinita ou 'carregar mais'?" | Tabela de decisão | 08-tabelas |

### Janelas, painéis e avisos
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "janelinha que abre por cima pra confirmar algo" | Modal / Dialog | 09-sobreposicoes |
| "queria ver os detalhes sem sair da lista" | Drawer / Side panel | 09-sobreposicoes |
| "aviso rápido que aparece e some (salvo com sucesso)" | Toast notification | 09-sobreposicoes |
| "caixinha de explicação quando passo o mouse" | Tooltip | 09-sobreposicoes |
| "balãozinho que abre ao clicar com opções/filtros" | Popover | 09-sobreposicoes |
| "menu de três pontinhos", "lista de ações que abre do botão" | Dropdown menu | 09-sobreposicoes |

### Tamanhos de tela (celular, notebook, monitor grande)
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "em qual tamanho de tela deve mudar?" | Breakpoint | 10-responsividade |
| "no celular a ordem das coisas fica estranha" | Reflow / Stacking | 10-responsividade |
| "funciona no meu monitor e quebra no notebook" | Fluid sizing | 10-responsividade |
| "texto cortado com '...'", "título enorme deixa o card gigante" | Wrapping x Truncation | 10-responsividade |
| "no monitor grande virou tudo uma coluna só" | Preserve the existing composition | 14-nao-quebrar |

### Aparência geral ("tá feio", "tá bagunçado")
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "não sei pra onde olhar primeiro", "tudo parece igual de importante" | Visual hierarchy | 11-visual |
| "cada tela usa um tamanho de letra" | Typography scale | 11-visual |
| "os espaçamentos parecem aleatórios" | Spacing system | 11-visual |
| "cada botão tem um azul diferente", "o sistema parece feito por várias pessoas" | Design tokens | 11-visual |
| "vermelho/verde confundem", "não dá pra saber se é erro ou sucesso" | Semantic colors | 11-visual |
| "tudo parece flutuar", "sombra demais", "os cards somem no fundo" | Elevation and surface hierarchy | 11-visual |

### Carregando, vazio, erro, sucesso
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "fica tudo branco enquanto carrega", "a tela pula quando termina de carregar" | Skeleton loading | 12-estados |
| "aparece só 'não há dados'", "tela vazia sem explicação" | Empty state | 12-estados |
| "dá erro e o usuário não sabe o que fazer" | Error state + Recovery action | 12-estados |
| "não sei se salvou" | Success feedback | 12-estados |
| "demora pra reagir quando clico em favoritar/curtir" | Optimistic UI | 12-estados |
| "fica girando e não sei se travou", "importação sem saber quanto falta" | Progress indicator | 12-estados |

### Acessibilidade (teclado, leitura, toque)
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "usando Tab não sei onde estou" | Focus-visible | 13-acessibilidade |
| "não dá pra usar sem mouse", "o Esc não fecha" | Keyboard navigation | 13-acessibilidade |
| "o leitor de tela lê só 'botão'" | Accessible name / ARIA label | 13-acessibilidade |
| "texto cinza clarinho difícil de ler" | Color contrast | 13-acessibilidade |
| "no celular erro o toque, botões pequenos e grudados" | Touch target | 13-acessibilidade |
| "animação demais / dá enjoo" | Reduced motion | 13-acessibilidade |

### Quando a IA quebra a tela ao corrigir
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "estava quase certo, só queria corrigir uma coisa e a IA mudou tudo" | Preserve the existing composition + Scope-limited change | 14-nao-quebrar |
| "a IA mexeu num componente e quebrou outras páginas" | Scope-limited change | 14-nao-quebrar |
| "a IA diz que terminou mas a tela continua errada" | Visual regression check | 14-nao-quebrar |

### Sites e landing pages
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "o topo do site não diz o que é", "o botão de reservar está lá embaixo" | Hero section / Above the fold | 17-sites-landing |
| "tem botão demais", "ninguém clica em 'Enviar'" | CTA (Call to action) | 17-sites-landing |
| "quero o menu sempre visível", "o menu some na foto" | Sticky header / Navbar | 17-sites-landing |
| "clico no menu e o título fica escondido atrás do cabeçalho" | Anchor links + scroll-margin-top | 17-sites-landing |
| "no celular o menu quebra em duas linhas", "quero aquele menu de três risquinhos" | Mobile menu / Hamburger menu | 17-sites-landing |
| "o texto atravessa a tela toda e cansa ler", "cada seção tem uma largura" | Content container + Readable line length | 17-sites-landing |
| "o site parece um amontoado de blocos", "espaços diferentes entre as partes" | Section rhythm | 17-sites-landing |
| "quero mostrar as avaliações/depoimentos" | Social proof | 17-sites-landing |
| "botão do WhatsApp flutuando", "o botão flutuante cobre outras coisas" | Floating action button (FAB) | 17-sites-landing |
| "o rodapé não tem contato/endereço" | Footer | 17-sites-landing |

### Imagens, vídeo e ícones
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "a foto ficou esticada / achatada / deformada" | object-fit: cover x contain | 18-imagens-midia |
| "as fotos da grade têm alturas diferentes" | aspect-ratio | 18-imagens-midia |
| "a foto corta a parte importante (cabeça, cama, fachada, produto)" | object-position | 18-imagens-midia |
| "o site demora pra abrir no celular", "fotos pesadas" | Responsive images (srcset) + Lazy loading | 18-imagens-midia |
| "a página pula enquanto carrega", "fui clicar e o botão mudou de lugar" | Layout shift (CLS) | 18-imagens-midia |
| "não dá pra ler o texto em cima da foto" | Text over image / Scrim | 18-imagens-midia |
| "quero vídeo no fundo do topo", "o vídeo não toca no iPhone" | Background video | 18-imagens-midia |
| "quero cards deslizando pro lado no celular", "carrossel/slider" | Carousel / Slider (scroll-snap) | 18-imagens-midia |
| "quero clicar na foto e ela abrir grande" | Lightbox / Gallery | 18-imagens-midia |
| "os ícones parecem de estilos diferentes / borrados" | Icon system | 18-imagens-midia |

### Tema escuro e cores
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "quero modo escuro" | Dark mode | 19-tema-cores |
| "o site pisca branco antes de ficar escuro" | Theme flash (FOUC) | 19-tema-cores |
| "cada tela tem um azul diferente", "cores demais" | Color palette (brand + neutrals) + Design tokens | 19-tema-cores / 11-visual |
| "a barra do navegador no celular fica de outra cor" | theme-color | 19-tema-cores |

### Animação e movimento
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "a tela parece parada, não sei se o clique funcionou" | Micro-interaction | 20-movimento |
| "as animações são lentas / moles / robóticas" | Transition duration & easing | 20-movimento |
| "a animação engasga no celular" | Animate transform & opacity only | 20-movimento |
| "no computador aparece ao passar o mouse, no celular não aparece" | Hover x Touch | 20-movimento |
| "quero que as coisas apareçam suavemente ao rolar" | Scroll-triggered animation | 20-movimento |

### Celular e camadas
| A pessoa diz… | Termo | Arquivo |
|---|---|---|
| "o site aparece minúsculo no celular, tenho que dar zoom" | Viewport meta tag | 21-mobile-camadas |
| "no iPhone, ao tocar no campo, a tela dá zoom" | iOS input zoom | 21-mobile-camadas |
| "o teclado cobre o campo / o botão de enviar" | Virtual keyboard overlap | 21-mobile-camadas |
| "o botão fica atrás da barrinha do iPhone", "some atrás da câmera" | Safe area | 21-mobile-camadas |
| "o menu/dropdown abre atrás de outra coisa", "o modal fica atrás do cabeçalho" | z-index / Stacking context | 21-mobile-camadas |
| "abre a janela mas o fundo continua clicável/rolando" | Overlay / Backdrop | 21-mobile-camadas |
| "os botões demoram pra responder ao toque" | Tap delay | 21-mobile-camadas |

Para prompts completos de situações comuns (dashboard em largura total, lista com scroll interno, cards, dois painéis, botões, formulário, tabela no celular, sobreposição, modal, validação), veja `references/15-prompts-prontos.md` e adapte ao caso da pessoa, em vez de montar do zero.

## Arquivos de referência

| Arquivo | Conteúdo |
|---|---|
| `references/01-layout.md` | Largura, altura e ocupação da tela: full-width, app shell, fit-to-viewport, single-screen, full-height, responsive x adaptive, compact UI |
| `references/02-grid.md` | CSS Grid, Flexbox, minmax, auto-fit, gap, min-width: 0, flex-wrap |
| `references/03-scroll.md` | Scroll da página, scroll interno, containment, barras duplas, overflow, sticky x fixed, lista virtualizada |
| `references/04-cards.md` | Anatomia, grade responsiva, altura igual, KPI, estados, hierarquia |
| `references/05-botoes.md` | Tipos de botão, hierarquia de ações, estados, barra fixa, botão de ícone, confirmação destrutiva |
| `references/06-formularios.md` | Label, ajuda e validação, estados de campo, layout, escolha de controle, disabled x read-only, divulgação progressiva |
| `references/07-navegacao.md` | Sidebar, abas, breadcrumbs, estado ativo, paginação |
| `references/08-tabelas.md` | Tabela de dados, cabeçalho fixo, prioridade de colunas, ações por linha, busca e filtros, paginação x infinito x virtualização |
| `references/09-sobreposicoes.md` | Modal, drawer, popover, dropdown, tooltip, toast |
| `references/10-responsividade.md` | Breakpoint, reflow, tamanhos fluidos, quebra x corte de texto, sem rolagem horizontal |
| `references/11-visual.md` | Hierarquia visual, tipografia, espaçamento, design tokens, cores semânticas, elevação |
| `references/12-estados.md` | Skeleton, vazio, erro, sucesso, optimistic UI |
| `references/13-acessibilidade.md` | Foco, teclado, nomes acessíveis, contraste, área de toque, menos movimento |
| `references/14-nao-quebrar.md` | Termos para a IA não quebrar a tela + lista de proibições |
| `references/15-prompts-prontos.md` | 10 prompts completos por situação |
| `references/16-glossario-checklist.md` | Checklist antes de enviar + glossário de uma linha |
| `references/17-sites-landing.md` | Hero, CTA, header fixo, âncoras, menu mobile, container e largura de leitura, ritmo de seções, prova social, botão flutuante, rodapé |
| `references/18-imagens-midia.md` | aspect-ratio, object-fit, object-position, srcset, lazy loading, layout shift, texto sobre foto, vídeo de fundo, carrossel, lightbox, ícones |
| `references/19-tema-cores.md` | Dark mode, flash de tema, paleta, theme-color |
| `references/20-movimento.md` | Microinterações, duração e easing, animação leve, hover x toque, animação ao rolar |
| `references/21-mobile-camadas.md` | Meta viewport, zoom do iPhone, teclado cobrindo campo, safe area, z-index, backdrop, atraso do toque |

## Exemplo

**A pessoa escreve:** "no meu sistema quando eu rolo a lista de pedidos a página toda desce e o botão de finalizar some lá embaixo"

**Resposta:**

**O que está acontecendo:** a página inteira está rolando junto com a lista. Por isso o cabeçalho e o botão "Finalizar" saem da tela.

**Nome técnico:**
- *No page-level scrolling*: a página em si não rola, fica parada como um aplicativo.
- *Controlled internal scrolling*: só a lista rola, dentro do espaço dela.
- *Sticky action bar*: a barra com os botões fica sempre visível, grudada embaixo.

**Pedido pronto (copie e cole na sua IA de programação, junto com o print da tela):**

> Na tela **[Pedidos]**, ao rolar a lista a página inteira desce e o botão Finalizar sai da tela, obrigando o usuário a rolar até o fim para concluir.
> Elimine o page-level scrolling: o app shell fica dentro de 100dvh e somente a lista de pedidos tem controlled internal scrolling (min-height: 0 e overflow-y: auto no contêiner correto, com overscroll-behavior: contain). Crie uma sticky action bar no rodapé da área principal com Finalizar e as demais ações, com padding inferior para não cobrir o último item.
> **Preserve:** cabeçalho, filtros e a organização atual dos componentes.
> **Desktop:** só a lista rola; cabeçalho, filtros e ações ficam visíveis. **Mobile:** mesmo comportamento, com a barra de ações ocupando a largura toda.
> **Não use:** transform: scale(), zoom, fontes minúsculas, position: absolute para montar a estrutura, margens negativas, overflow: hidden só para esconder o defeito (é permitido no contêiner externo quando existe uma área interna que rola), nem alturas fixas menores que o conteúdo. Não crie barras de rolagem aninhadas.
> **Validação:** não considere concluído só porque compilou. Renderize a tela e confira prints em 1366x768, 1440x900, 1920x1080 e ~390px de largura. Confirme: uma única rolagem vertical (a da lista), Finalizar sempre visível, último pedido não coberto pela barra, nada sobreposto, nenhuma rolagem horizontal. Informe os arquivos alterados e a causa raiz.

**Antes de enviar, complete:** o nome exato da tela.
