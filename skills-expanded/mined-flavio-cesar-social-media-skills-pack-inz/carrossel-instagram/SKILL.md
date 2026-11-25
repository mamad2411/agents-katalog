---
name: carrossel-instagram
description: "Cria carrosseis completos para Instagram em HTML interativo com slides exportaveis como imagens individuais. Use esta skill sempre que alguem pedir para criar um carrossel, carousel, slides para Instagram, post com multiplas imagens para Instagram, conteudo swipeable, ou qualquer conteudo visual com multiplos slides para redes sociais. Tambem aciona quando mencionarem 'criar carrossel', 'fazer slides pro Instagram', 'post carrossel', 'carousel design', ou pedirem um design de multiplas paginas para feed. Funciona para qualquer nicho: marketing, educacional, pessoal, corporativo, lifestyle, etc."
---

# Gerador de Carrossel para Instagram

Voce e um sistema de design de carrosseis para Instagram. Quando alguem pedir para criar um carrossel, gere um arquivo HTML completo, autonomo e interativo onde **cada slide e projetado para ser exportado como imagem individual** para postagem no Instagram.

---

## Passo 1: Coletar informacoes da marca

Antes de gerar qualquer carrossel, pergunte ao usuario o seguinte (se ainda nao tiver sido fornecido):

1. **Nome da marca** — exibido no primeiro e ultimo slides
2. **@ do Instagram** — mostrado no header do frame e na legenda
3. **Cor principal da marca** — a cor de destaque principal (codigo hex ou descricao)
4. **Logo** — pergunte se tem um SVG, quer usar a inicial do nome, ou prefere pular
5. **Preferencia de fonte** — serif nos titulos + sans no corpo (estilo editorial), tudo sans-serif (moderno/limpo), ou fontes especificas do Google Fonts
6. **Tom de voz** — profissional, casual, divertido, ousado, minimalista, etc.
7. **Tema do carrossel** — sobre o que sera o conteudo
8. **Imagens** — pergunte se ha imagens para incluir no carrossel

Se o usuario fornecer uma URL de site ou materiais da marca, derive as cores e o estilo a partir deles.

Se o usuario simplesmente disser "faz um carrossel sobre X" sem detalhes da marca, **pergunte antes de gerar**. Nao assuma valores padrao.

---

## Passo 2: Gerar o sistema completo de cores

A partir da **unica cor principal** fornecida pelo usuario, gere a paleta completa de 6 tokens:

```
BRAND_PRIMARY   = {cor do usuario}                   // Destaque principal — barra de progresso, icones, tags
BRAND_LIGHT     = {primary clareada ~20%}             // Destaque secundario — tags em fundo escuro, pills
BRAND_DARK      = {primary escurecida ~30%}           // Texto do CTA, ancora do gradiente
LIGHT_BG        = {off-white quente ou frio}          // Fundo dos slides claros (nunca #fff puro)
LIGHT_BORDER    = {levemente mais escuro que LIGHT_BG} // Divisores nos slides claros
DARK_BG         = {quase-preto com tom da marca}      // Fundo dos slides escuros
```

**Regras para derivar as cores:**

- LIGHT_BG deve ser um off-white com leve tom que complemente a cor principal (cor quente → creme, cor fria → cinza-azulado)
- DARK_BG deve ser quase-preto com um tom sutil que combine com a temperatura da marca (quente → #1A1918, frio → #0F172A)
- LIGHT_BORDER e sempre ~1 tom mais escuro que LIGHT_BG
- O gradiente da marca usado nos slides 3 e 7 e: `linear-gradient(165deg, BRAND_DARK 0%, BRAND_PRIMARY 50%, BRAND_LIGHT 100%)`

---

## Passo 3: Configurar a tipografia

Com base na preferencia de fonte do usuario, escolha uma **fonte de titulo** e uma **fonte de corpo** do Google Fonts.

**Combinacoes sugeridas:**

| Estilo | Fonte do Titulo | Fonte do Corpo |
|--------|----------------|----------------|
| Editorial / premium | Playfair Display | DM Sans |
| Moderno / limpo | Plus Jakarta Sans (700) | Plus Jakarta Sans (400) |
| Acolhedor / amigavel | Lora | Nunito Sans |
| Tecnico / afiado | Space Grotesk | Space Grotesk |
| Ousado / expressivo | Fraunces | Outfit |
| Classico / confiavel | Libre Baskerville | Work Sans |
| Arredondado / simpatico | Bricolage Grotesque | Bricolage Grotesque |

**Escala de tamanhos de fonte (fixa para todas as marcas):**

- Titulos: 28–34px, peso 600, letter-spacing -0.3 a -0.5px, line-height 1.1–1.15
- Corpo: 14px, peso 400, line-height 1.5–1.55
- Tags/rotulos: 10px, peso 600, letter-spacing 2px, caixa alta
- Numeros de etapa: fonte de titulo, 26px, peso 300
- Texto pequeno: 11–12px

Aplique via classes CSS `.serif` (fonte do titulo) e `.sans` (fonte do corpo) em todos os slides.

---

## Arquitetura dos Slides

### Formato

- Proporcao: **4:5** (padrao de carrossel do Instagram)
- Cada slide e autonomo — todos os elementos de UI estao incorporados na imagem
- Alterne fundos LIGHT_BG e DARK_BG para criar ritmo visual

### Elementos obrigatorios em TODOS os slides

#### 1. Barra de Progresso (parte inferior de cada slide)

Mostra ao usuario onde ele esta no carrossel. Preenche conforme avanca.

- Posicao: absolute na parte inferior, largura total, 28px de padding horizontal, 20px de padding inferior
- Trilha: 3px de altura, cantos arredondados
- Largura do preenchimento: `((slideIndex + 1) / totalSlides) * 100%`
- Adapta-se ao fundo do slide:
  - Slides claros: trilha `rgba(0,0,0,0.08)`, preenchimento BRAND_PRIMARY, contador `rgba(0,0,0,0.3)`
  - Slides escuros: trilha `rgba(255,255,255,0.12)`, preenchimento `#fff`, contador `rgba(255,255,255,0.4)`
- Rotulo do contador ao lado da barra: formato "1/7", 11px, peso 500

```javascript
function progressBar(index, total, isLightSlide) {
  const pct = ((index + 1) / total) * 100;
  const trackColor = isLightSlide ? 'rgba(0,0,0,0.08)' : 'rgba(255,255,255,0.12)';
  const fillColor = isLightSlide ? BRAND_PRIMARY : '#fff';
  const labelColor = isLightSlide ? 'rgba(0,0,0,0.3)' : 'rgba(255,255,255,0.4)';
  return `<div style="position:absolute;bottom:0;left:0;right:0;padding:16px 28px 20px;z-index:10;display:flex;align-items:center;gap:10px;">
    <div style="flex:1;height:3px;background:${trackColor};border-radius:2px;overflow:hidden;">
      <div style="height:100%;width:${pct}%;background:${fillColor};border-radius:2px;"></div>
    </div>
    <span style="font-size:11px;color:${labelColor};font-weight:500;">${index + 1}/${total}</span>
  </div>`;
}
```

#### 2. Seta de Arraste (lado direito — em todos os slides EXCETO o ultimo)

Um chevron sutil no lado direito indicando ao usuario para continuar arrastando. No **ultimo slide e removido** para que o usuario saiba que chegou ao fim.

- Posicao: absolute a direita, altura total, 48px de largura
- Fundo: gradiente sutil de transparente → leve tom
- Chevron: SVG 24x24, tracos arredondados
- Adapta-se ao fundo do slide:
  - Slides claros: fundo `rgba(0,0,0,0.06)`, stroke `rgba(0,0,0,0.25)`
  - Slides escuros: fundo `rgba(255,255,255,0.08)`, stroke `rgba(255,255,255,0.35)`

```javascript
function swipeArrow(isLightSlide) {
  const bg = isLightSlide ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.08)';
  const stroke = isLightSlide ? 'rgba(0,0,0,0.25)' : 'rgba(255,255,255,0.35)';
  return `<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,${bg});">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M9 6l6 6-6 6" stroke="${stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>`;
}
```

---

## Padroes de Conteudo dos Slides

### Regras de layout

- Padding do conteudo: `0 36px` padrao
- Slides com alinhamento inferior e barra de progresso: `0 36px 52px` para liberar espaco da barra
- **Slides hero/CTA:** `justify-content: center`
- **Slides com muito conteudo:** `justify-content: flex-end` (texto na parte inferior, espaco de respiro acima)

### Tag / Rotulo de Categoria

Rotulo pequeno em caixa alta acima do titulo em cada slide para categorizar o conteudo.

```html
<span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{cor};margin-bottom:16px;">{TEXTO DA TAG}</span>
```

- Slides claros: cor = BRAND_PRIMARY
- Slides escuros: cor = BRAND_LIGHT
- Slides com gradiente da marca: cor = `rgba(255,255,255,0.6)`

### Logotipo (primeiro e ultimo slides)

Icone da marca + nome da marca exibidos juntos.

- Se icone do logo fornecido: circulo de 40px (fundo BRAND_PRIMARY) com icone centralizado, nome da marca ao lado
- Se iniciais: circulo de 40px com a primeira letra do nome da marca em branco
- Nome da marca: 13px, peso 600, letter-spacing 0.5px

### Marca d'agua (opcional)

Se o usuario forneceu um icone de logo, use-o como marca d'agua sutil no fundo de slides-chave (hero, CTA, gradiente da marca) com opacidade 0.04–0.06. Pule se nao houver logo.

---

## Sequencia Padrao dos Slides

Siga este arco narrativo. O numero de slides pode variar (5–10), mas **7 e o ideal**.

| # | Tipo | Fundo | Proposito |
|---|------|-------|-----------|
| 1 | Hero | LIGHT_BG | Gancho — frase de impacto, logotipo, marca d'agua opcional |
| 2 | Problema | DARK_BG | Dor — o que esta quebrado, frustrante ou ultrapassado |
| 3 | Solucao | Gradiente da marca | A resposta — o que resolve, caixa de citacao/prompt opcional |
| 4 | Recursos | LIGHT_BG | O que voce recebe — lista de features com icones |
| 5 | Detalhes | DARK_BG | Profundidade — personalizacao, specs, diferenciais |
| 6 | Como funciona | LIGHT_BG | Passo a passo — fluxo de trabalho numerado |
| 7 | CTA | Gradiente da marca | Chamada para acao — logo, tagline, botao CTA. **Sem seta. Barra de progresso cheia.** |

**Regras:**

- Comece com um gancho em LIGHT_BG
- Termine com um CTA no gradiente da marca — sem seta de arraste, barra de progresso em 100%
- Alterne fundos claros e escuros
- Adapte a sequencia ao tema — nem todo carrossel precisa de um slide de "problema"
- Para carrosseis educativos, substitua "Problema/Solucao" por "Contexto/Dica principal"
- Para carrosseis de lista, cada slide do meio pode ser um item da lista
- Para storytelling, siga uma progressao narrativa natural

---

## Componentes Reutilizaveis

### Pills com tachado (riscado)

Para mensagens de "o que esta sendo substituido" em slides de problema.

```html
<span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#6B6560;text-decoration:line-through;">{Ferramenta antiga}</span>
```

### Pills de tag

Para rotulos de features, opcoes ou categorias.

```html
<span style="font-size:11px;padding:5px 12px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">{Rotulo}</span>
```

### Caixa de citacao / prompt

Para mostrar exemplos de inputs, citacoes ou depoimentos.

```html
<div style="padding:16px;background:rgba(0,0,0,0.15);border-radius:12px;border:1px solid rgba(255,255,255,0.08);">
  <p class="sans" style="font-size:13px;color:rgba(255,255,255,0.5);margin-bottom:6px;">{Rotulo}</p>
  <p class="serif" style="font-size:15px;color:#fff;font-style:italic;line-height:1.4;">"{Texto da citacao}"</p>
</div>
```

### Lista de features

Linhas com icone + titulo + descricao para slides de features/beneficios.

```html
<div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
  <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;">{icone}</span>
  <div>
    <span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">{Titulo}</span>
    <span class="sans" style="font-size:12px;color:#8A8580;">{Descricao}</span>
  </div>
</div>
```

### Etapas numeradas

Para slides de fluxo de trabalho ou passo a passo.

```html
<div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
  <span class="serif" style="font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;">01</span>
  <div>
    <span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">{Titulo da etapa}</span>
    <span class="sans" style="font-size:12px;color:#8A8580;">{Descricao da etapa}</span>
  </div>
</div>
```

### Amostras de cores

Para slides de personalizacao ou branding.

```html
<div style="width:32px;height:32px;border-radius:8px;background:{cor};border:1px solid rgba(255,255,255,0.08);"></div>
```

### Botao CTA (somente no ultimo slide)

```html
<div style="display:inline-flex;align-items:center;gap:8px;padding:12px 28px;background:{LIGHT_BG};color:{BRAND_DARK};font-family:'{BODY_FONT}',sans-serif;font-weight:600;font-size:14px;border-radius:28px;">
  {Texto do CTA}
</div>
```

---

## Frame do Instagram (Preview)

Ao exibir o carrossel no chat, envolva-o em um frame estilo Instagram para que o usuario possa pre-visualizar a experiencia:

- **Header:** Avatar (circulo BRAND_PRIMARY + logo) + @ + subtitulo
- **Viewport:** proporcao 4:5, trilha arrastavel/swipeable com todos os slides
- **Dots:** Pequenos indicadores de pontos abaixo do viewport
- **Acoes:** Icones SVG de curtir, comentar, compartilhar e salvar
- **Legenda:** @ + descricao curta do carrossel + "2 HORAS ATRAS"

Inclua interacao de arrastar/swipe baseada em pointer para o preview, mas os slides em si sao imagens autonomas prontas para exportacao.

---

## Principios de Design

1. **Cada slide e exportavel** — seta e barra de progresso fazem parte da imagem do slide, nao sao overlay de UI
2. **Alternancia claro/escuro** — cria ritmo visual e mantem a atencao ao longo dos swipes
3. **Combinacao titulo + corpo** — fonte display para impacto, fonte corpo para legibilidade
4. **Paleta derivada da marca** — todas as cores derivam de uma unica cor principal, mantendo coesao
5. **Revelacao progressiva** — barra de progresso preenche e seta guia o usuario para frente
6. **Ultimo slide e especial** — sem seta (sinaliza o fim), barra de progresso cheia, CTA claro
7. **Componentes consistentes** — mesmo estilo de tag, mesmo estilo de lista, mesmo espacamento em todos os slides
8. **Padding do conteudo respeita a UI** — texto do corpo nunca sobrepoe barra de progresso ou seta
9. **Mobile-first** — todo o design e pensado para visualizacao no celular, onde 95%+ dos usuarios verao o conteudo

---

## Dicas extras para carrosseis de alta performance

- **Primeiro slide e tudo**: se o gancho nao prende em 1.5 segundo, ninguem arrasta. Priorize frases curtas, diretas e que gerem curiosidade
- **Texto grande nos slides**: lembre que as pessoas veem no celular — corpo minimo de 14px, titulos de 28px+
- **Maximo 3-4 linhas de texto por slide**: menos e mais. Se tem muito texto, divida em mais slides
- **Use numeros e dados quando possivel**: "73% das pessoas..." prende mais que generalidades
- **CTA especifico**: "Salve pra consultar depois" funciona melhor que "Siga-nos"
- **Emojis com moderacao**: 1-2 por slide no maximo, usados como marcadores visuais

