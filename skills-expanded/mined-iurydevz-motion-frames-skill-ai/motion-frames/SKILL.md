---
name: motion-frames
description: Criar vídeos de motion design profissionais (promos de app/produto, anúncios verticais TikTok/Reels, tipografia cinética, vídeos sincronizados com narração) como animação HTML que é função pura do número do quadro, renderizada quadro a quadro em navegador sem tela para MP4 1080x1920 a 60fps. Usar sempre que o pedido envolver vídeo, motion, animação, edit, promo ou abertura — mesmo sem a palavra "motion". Inclui pipeline pronto (template, renderizador, preview, kit de SFX), 4 gramáticas de estilo destiladas de referências reais e o checklist anti-genérico.
---

# Motion Frames — sistema de motion design por quadros

Método completo para produzir motion design de nível profissional sem software de vídeo: a animação inteira é **uma página HTML cuja cena é função pura do número do quadro**, fotografada quadro a quadro por um Chromium sem tela e montada em MP4 com ffmpeg. Tudo é determinístico: mesmo input, mesmos pixels — dá para renderizar em paralelo, retomar de qualquer quadro e sincronizar som e imagem com precisão de 1/60s.

## 1. Regra inviolável: função pura do quadro

- A cena inteira vive em `renderFrame(n)`, onde `n` é o número do quadro (60fps).
- **Proibido** relógio (`Date.now`, `performance.now`, estado acumulado via `requestAnimationFrame`) e **proibido** aleatório sem semente: aleatoriedade só via `hash(i)` determinístico do índice/quadro.
- Movimento = fórmulas fechadas do tempo decorrido desde o início do evento:
  - **Spring analítico** (subamortecido): `spring(t, freq, damp)` com overshoot — é a física padrão de tudo (entradas, pops, empilhamento).
  - **Easings nomeados**: `easeOutCubic`, `easeInOutCubic`, `easeOutBack`.
  - **Segmentos**: `seg(n, a, b)` = progresso 0→1 de um trecho de quadros; `clamp`, `lerp` para interpolar qualquer grandeza (posição, cor, geometria de morph).
- Formato padrão: **1080x1920, 60fps**. Duração decidida pelo conteúdo (teste rápido: 8s = 480 quadros).

## 2. Pipeline (pasta `pipeline/` desta skill)

| Arquivo | O que é |
|---|---|
| `pipeline/template.html` | Página-base com os helpers (`T`, `seg`, `spring`, easings, `hash`) e o esqueleto `renderFrame(n)` |
| `pipeline/render.mjs` | Renderizador CDP sem dependências: `node render.mjs <pagina.html> <dir> <num_quadros> 1080 1920 [quadro_inicial]` |
| `pipeline/preview.mjs` | Renderiza só quadros escolhidos em PNG: `node preview.mjs <pagina.html> <dir> "0,60,160,300" <total> 1080 1920` |
| `pipeline/sfx_kit.py` | Kit de efeitos sonoros sintetizados (numpy/scipy) amarrados ao número do quadro |

- **Chromium**: o renderizador procura `CHROME_BIN`, depois um `chrome-headless-shell` ao lado do script, depois o caminho conhecido do workspace. Nem todo Chromium serve: builds com política de domínio/WebGL (ex.: o Chromium gerenciado do Hatch) recusam rodar standalone — use um **chrome-headless-shell** avulso.
- **Velocidade**: `FMT=jpeg` (qualidade 90) é ~2x mais rápido que PNG e indistinguível no resultado. PNG só para preview.
- **Shards**: vídeos longos renderizam em 2 processos paralelos (metades do intervalo, usando o argumento `quadro_inicial`), cada um com sua `PORT` (CDP). **Máximo 2 em paralelo** em máquinas de ~8GB — 3 estoura a RAM.
- **Montagem**: `ffmpeg -framerate 60 -i dir/f%04d.jpg -i audio.wav -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -b:a 192k -movflags +faststart out.mp4`.
- **Fontes e imagens locais**: referencie por caminho relativo ao HTML (funciona via `file://`). Fontes da marca: baixe os `.woff2` e gere um CSS `@font-face` local — não dependa da rede em tempo de render. Imagens usadas nas cenas: inclua um `<img>` oculto de preload no corpo da página, senão os primeiros quadros saem sem ela.

## 3. Fluxo de produção (nesta ordem)

1. **Roteiro e referências**: defina a frase de cada cena. Estude as referências quadro a quadro (extraia uma contact sheet com ffmpeg) e anote a *gramática* — não copie a superfície.
2. **Áudio primeiro** (se houver narração): detecte silêncios (`ffmpeg -af silencedetect`) antes de decidir cortar; transcreva com **faster-whisper** (`small`, `word_timestamps=True`, passar o áudio como array numpy lido de WAV 16k — o decode interno do faster-whisper quebra em algumas versões de PyAV) e transforme os tempos das palavras-chave em **landmarks de quadro** (`segundo × 60`). Nunca invente a duração da fala.
3. **Recon de marca** (vídeos de produto): pegue a identidade real — baixe o HTML/CSS do site e extraia logo (arquivo de imagem), paleta (hex mais frequentes no CSS) e fontes. Use a logo e as fontes oficiais no vídeo.
4. **Design por cenas**: uma função por cena (`s1(n)`, `s2(n)`…), fronteiras nos landmarks da fala. Cada cena nasce com o seu evento principal já sincronizado.
5. **Preview obrigatório**: contact sheet de 15–30 quadros com o `preview.mjs` para checar ritmo e composição — **e sempre confira 2–3 quadros-chave em tamanho real**: contact sheet engana (esconde colisões de texto, estouros de largura e detalhes pequenos).
6. **SFX por micro-evento** (seção 8), com os mesmos números de quadro da animação.
7. **Render em shards + montagem + QA**: extraia quadros do **MP4 final** (não dos frames soltos) e confira antes de entregar.

## 4. Linguagem de movimento (o que separa profissional de genérico)

- **Abertura com cara de cinema**: o primeiro segundo é um título — tipografia grande entrando com spring e câmera, fundo com profundidade. Nada de tela estática.
- **A câmera nunca para**: drift lento de escala (1→1.03–1.09) em todo plano; cortes disfarçados por movimento (dolly/zoom/pan com parallax entre camadas).
- **Densidade**: um micro-evento a cada 0,5–1,5s. Se um trecho passa 2s sem nada acontecer, está errado.
- **Física em tudo**: springs com overshoot, squash & stretch em quedas e quiques, antecipação antes do movimento principal. Movimento linear é proibido por omissão.
- **Transições são eventos, não cortes**: morph do objeto (a pílula vira barra, a barra vira card), zoom-through com blur, ou zoom-punch (escala cruzando 1→1.09 com crossfade de ~18 quadros nas fronteiras de cena).
- **Paleta enxuta**: fundo de uma família + UMA cor de destaque com glow; tipografia pesada; muito respiro.

## 5. Fundos: nunca chapados, sempre vivos

Fundo preto chapado (ou qualquer cor chapada) está proibido — o fundo tem vida própria, fluxo e parallax entre fundo/meio/frente. Três receitas provadas:

- **Estúdio vivo** (promos escuros): gradiente com tinta da cor de destaque, 2 blobs de cor desfocados derivando devagar, cone de luz no topo, partículas bokeh flutuantes (hash determinístico), chão com grade de pontos em perspectiva + linha de horizonte luminosa + reflexo sob o elemento central.
- **Aurora líquida** (cenas contínuas): 3–4 fitas de gradiente radial alongadas, `mix-blend-mode: screen`, blur forte, derivando em Lissajous e girando devagar; duas paletas com crossfade quando um comando muda a "cor" da cena; poeira de partículas por cima.
- **Gelo da marca** (kinetic claro): gradiente claro da cor da marca, seda menta fluindo (mesma técnica da aurora, em claro), grade de pontos sutil e poeira — limpo, mas respirando.

## 6. 3D de verdade (capriche — é onde os vídeos mais ficam atrás das referências)

- CSS `perspective` + `rotateX/rotateY` em telefones, cards e dashboards; o elemento **flutua** com sombra viva que reage ao tilt.
- **Parallax real**: fundo, meio e frente em velocidades diferentes em todo zoom/pan.
- Cubos e caixas 3D em CSS: cada face é um div posicionado com `translateZ = metade da largura/altura` (errar isso abre as arestas).
- Escadas/blocos isométricos subindo, pilhas com profundidade, vidro (`backdrop-filter` quando o fundo atrás é simples) e brilho especular varrendo.
- Regra prática: se a cena pode ser descrita como "texto + retângulo plano", falta 3D. Adicione tilt, camada ou profundidade até ela parecer fotografada, não desenhada.

## 7. As quatro gramáticas (estruturas plano a plano)

### A. Cinema/morph (aberturas e testes de estilo)
Título cinematográfico → objeto com squash & stretch em trajetória pontilhada → câmera mergulha e o objeto faz **morph** (círculo→pílula→tela) → elemento 3D girando com zoom na face → tipografia cinética com círculo desenhado à mão → painel de vidro com gráfico em spring → fecho retornando ao ponto inicial (loop perfeito, se for o caso).

### B. App promo premium (referências tipo Opal/Qwix)
1. Fundo ambiente vivo + spotlight; UMA cor de destaque com glow/bloom.
2. Abertura: UI/telefone em perspectiva 3D flutuando, dolly-in com **pull focus** (começa desfocado, foca).
3. Mergulho da câmera num detalhe (barra do gráfico) que vira o próximo plano.
4. Pílulas de vidro com ícone + **número contando** (easeOut) + rótulo; borda com arco de luz viajante.
5. Agregação: linhas-suporte se desenham das pílulas e convergem num número gigante com ▲.
6. Ícone do app com morph + explosão de partículas.
7. Sheet do app + botão-pílula gigante de CTA com varredura de luz.
8. Logo reveal: símbolo se desenha (SVG dash) + wordmark + URL pequena.

### C. Cena contínua interativa (referência "Built with Claude")
Uma cena só, sem cortes, sobre aurora líquida: símbolo se desenha → pílulas de comando entram → **cursor viaja e clica** numa pílula → a pílula faz **morph** para barra de prompt → prompt **digitado palavra por palavra** (caret piscando, última palavra em destaque) → a barra faz morph para o resultado (card que se constrói por dentro: anel, barras, play, progresso %) → segundo comando digitado muda a cor do fundo inteiro → fecho com símbolo + assinatura. A história é "alguém usando o produto".

### D. Kinetic type claro (anúncios PT-BR de tipografia)
Fundo gelo da marca; **tipografia pesada da fonte da marca como protagonista**, palavra por palavra no beat da fala, palavra-chave com cor de destaque, sombra-fantasma colorida e rabiscos à mão (riscado, círculo, swoosh — SVG dash). Intercalado com UI real que conta a história: notificações **empilhando com física**, comparativo de barras, sistema **orbital** de nós em volta da logo, chat com bolhas conversando, card de status com gráfico, contador gigante. Fronteiras de cena por zoom-punch; beat de inversão escura no meio ("E não para por aí!"); slogan em 3 golpes com ícone; fecho com logo + CTA clicado pelo cursor + URL.

## 8. Som: SFX por micro-evento

- Trilha montada no `sfx_kit.py`: cada evento sonoro usa **o mesmo número de quadro** do evento visual.
- Vocabulário: `pop` (cliques, cards, palavras grandes), `tick` (digitação, barras, contadores), `whoosh` (transições e morphs), `shimmer` (confirmações, reveals), `pad` (cama harmônica discreta sob tudo).
- Densidade igual à do vídeo: se tem micro-evento visual, tem som. Sob narração, mixar a trilha a ~0,5 e deixar a voz dominar.
- Nunca gere nem substitua a voz do usuário: narração é sempre a dele, intacta (cortes de silêncio só com o áudio analisado e a sincronia refeita depois do corte).

## 9. Checklist anti-genérico (conferir antes de entregar)

1. A tipografia é protagonista ou só rótulo de UI? (tem que ser protagonista)
2. Há micro-evento a cada 0,5–1,5s em TODAS as cenas?
3. Alguma coisa empilha, cai ou colide com física — ou tudo flutua isolado?
4. Existe interação (cursor clicando, prompt digitado, produto sendo usado)?
5. Tem camada de rabiscos desenhados (círculo, sublinhado, seta, riscado)?
6. Pelo menos uma transição é morph de objeto, não só zoom?
7. O fundo flui com vida própria e parallax entre camadas?
8. A UI tem conteúdo "real" que conta a história (valores, conversas, nomes) em vez de placeholders abstratos?
9. Tem sistema orbital, texto em trajetória ou outro elemento "assinatura"?
10. O 3D passa no teste da seção 6?
11. SFX em cada micro-evento?

## 10. Verdade comercial (não invente números)

- Número que vira promessa comercial (taxa %, % de aprovação, preço) **não se inventa**: se a marca não publica, use comparativo visual sem número (barra alta × barra baixa), contadores de volume/crescimento como recurso de motion e linguagem qualitativa ("alta", "bem menor").
- Fato incerto sobre o produto se sinaliza ANTES de roteirizar, nunca depois de renderizar.

## 11. Erros que já aconteceram (não repetir)

- **Contact sheet engana**: miniaturas escondem colisão de texto e estouro de largura. Sempre validar quadros-chave em tamanho real.
- **Atributo duplicado em SVG**: dois `stroke-dasharray` no mesmo elemento — o primeiro vence e o draw-on morre silenciosamente. Um atributo por elemento.
- **Índice de cena hardcoded**: função que retorna cena fixa (`return 5`) quebra a última cena quando o número de cenas muda. Derive do array de fronteiras.
- **Cubo 3D aberto**: faces com `translateZ` errado (≠ metade da dimensão) deixam frestas nas arestas.
- **3 shards em paralelo = OOM** em máquina pequena. Máximo 2.
- **Chromium do sistema pode não servir** (política de domínio/WebGL): use chrome-headless-shell avulso.
- **Imagem sem preload** aparece só depois dos primeiros quadros: `<img>` oculto no corpo resolve.
- **Cena "quase certa"**: medir texto largo em fonte grande — frase de slogan em 118px pode passar de 1080px e quebrar feio; confira a largura real no preview grande.

## 12. Projetos-exemplo (produções reais deste sistema)

- `~/workspace/motion-frames/teste_8s.mp4` — gramática A: bola/morph/cubo/tipografia em loop, 8s.
- `~/workspace/iphone18/iphone18_pro.mp4` — narração sincronizada palavra por palavra (53s), iPhone 3D em CSS.
- `~/workspace/kalo/kalo_app_v2.mp4` — gramática B com fundo estúdio vivo + cena de scan de refeição por IA, 15s.
- `~/workspace/kalo/feito_com_muse.mp4` — gramática C: cena contínua, cursor, prompt digitado, morphs, aurora com crossfade, 14s.
- `~/workspace/turtle/turtlepags.mp4` — gramática D completa com narração, identidade real da marca (logo/paleta/fontes do site), 53s.
