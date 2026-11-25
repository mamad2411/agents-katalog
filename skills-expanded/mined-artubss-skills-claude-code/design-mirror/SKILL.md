---
name: design-mirror
description: "Replique o estilo visual de qualquer site e aplique-o ao seu código existente. Use essa habilidade sempre que o usuário quiser corresponder ao design de um site, espelhar uma estética de UI, fazer seu app parecer como outro site ou replicar um estilo visual específico de uma URL. Ative em frases como 'quero que pareça com', 'corresponder ao design de', 'copiar o estilo de', 'quero que meu app pareça com X', 'espelhar esse design', 'inspirado em [url]', ou sempre que o usuário apontar para um site e disser que quer que seu frontend corresponda."
---

# Design Mirror

Capture a linguagem de design visual de qualquer site e aplique-a ao seu código existente — cores, tipografia, espaçamento, ritmo de layout, formas de componentes e estética geral — tudo extraído em tempo real via Bright Data Web Unlocker.

## O Que Essa Habilidade Faz

1. **Capturar** — Screenshot + scrape HTML do site de inspiração via Bright Data
2. **Extrair** — Identificar o sistema de design completo: cores, fontes, escala de espaçamento, border radius, sombras, padrões de componentes
3. **Analisar** — Estudar o screenshot visualmente e o CSS estruturalmente para entender a linguagem de design
4. **Aplicar** — Traduzir esse sistema de design para o código existente do usuário (seu framework, seus componentes)

Você não está copiando conteúdo ou funcionalidade. Está entendendo a *linguagem de design* — a paleta, a escala tipográfica, as formas de cards, os hover states, a sensação estética geral.

> **Importante:** Essa habilidade é para inspiração de design e aprendizado — extração de design tokens publicamente visíveis (cores, fontes, espaçamento) para informar seu próprio trabalho de UI. Sempre use-a respeitosamente e de acordo com os termos de serviço dos sites que você referenciar.

## Configuração

Requer:
- `BRIGHTDATA_API_KEY` — de [brightdata.com/cp](https://brightdata.com/cp) → Account Settings
- `BRIGHTDATA_UNLOCKER_ZONE` — crie uma zona Unlocker em brightdata.com/cp

```bash
export BRIGHTDATA_API_KEY="your-api-key"
export BRIGHTDATA_UNLOCKER_ZONE="your-zone-name"
```

## Processo Passo a Passo

### Passo 1: Capturar o Site de Inspiração

Execute ambas as capturas em paralelo — screenshot (para análise visual) e scrape HTML (para extração de CSS):

```bash
# Screenshot (salvar como PNG)
bash scripts/screenshot.sh "https://inspiration-site.com" "/tmp/target_screenshot.png"

# HTML + CSS scrape
bash scripts/scrape_html.sh "https://inspiration-site.com" "/tmp/target_page.html"
```

Leia `references/capture-guide.md` para aprender como extrair CSS do HTML bruto e lidar com problemas comuns.

### Passo 2: Analisar o Sistema de Design

Após capturar, analise ambos em paralelo:

**Análise visual (screenshot):** Leia a imagem PNG e identifique:
- Cores primária, secundária e de destaque
- Cores de background (bg da página, bg de card, hierarquia de surface)
- Tipografia: famílias de fontes visíveis, hierarquia de tamanho (h1 → body → caption)
- Layout: é centrado/width-constrito? Grid? Sidebar?
- Formas de card/container: tamanho de border radius, estilo de sombra (dura, suave, nenhuma, colorida)
- Estilos de botão: pill, retângulo, ghost, gradiente?
- Navegação: sticky? Efeito glass/blur? Dark ou light?
- Humor geral: dark, light, minimal, brutalista, glassmorphism, corporativo, startup?

**Análise de CSS (HTML):** Extraia de tags `<style>` e estilos inline:
- Propriedades customizadas CSS (`:root { --color-... }`) — design tokens declarados publicamente
- Importações de fonte (`@import` de Google Fonts, etc.)
- Tailwind config se presente
- Padrões de classes repetidas que revelam a escala de espaçamento

Leia `references/css-extraction.md` para o playbook de extração.

### Passo 3: Construir o Mapa de Design Tokens

Produza um mapa estruturado de design tokens antes de tocar em qualquer código:

```
DESIGN TOKENS FROM [site]
==========================
Colors:
  --bg-primary: #0a0a0f      (page background)
  --bg-surface: #13131a      (card/panel background)
  --text-primary: #ffffff
  --text-muted: #8888aa
  --accent: #7c3aed          (primary CTA color)
  --accent-hover: #6d28d9
  --border: rgba(255,255,255,0.08)

Typography:
  --font-heading: 'Inter', sans-serif
  --font-body: 'Inter', sans-serif
  font-scale: 12/14/16/20/24/32/48px
  heading-weight: 700
  body-weight: 400

Spacing:
  base-unit: 8px
  scale: 4/8/12/16/24/32/48/64px

Borders & Shadows:
  --radius-sm: 6px
  --radius-md: 12px
  --radius-lg: 20px
  --shadow: 0 4px 24px rgba(0,0,0,0.4)

Special effects:
  glass-blur: backdrop-filter: blur(16px)
  gradient: linear-gradient(135deg, #7c3aed, #2563eb)
```

Mostre esse mapa de tokens ao usuário antes de prosseguir. É a base — se estiver errado, o resultado será errado.

### Passo 4: Entender o Código do Usuário

Antes de escrever qualquer código, leia as partes relevantes do código do usuário:

- Qual framework? (React, Vue, Next.js, HTML puro?)
- Qual abordagem de styling? (Tailwind, CSS modules, styled-components, CSS puro?)
- Onde estilos globais são definidos? (globals.css, theme.ts, tailwind.config.js?)
- Quais componentes precisam ser restyled? (pergunte ao usuário se não estiver claro)

Não reescreva tudo — precisão cirúrgica. Aplique os design tokens à estrutura existente.

### Passo 5: Aplicar o Design

A estratégia de aplicação depende do seu stack:

**Se Tailwind:** Atualize `tailwind.config.js` com a nova paleta de cores, família de fontes, escala de border radius. Adicione variáveis CSS customizadas para qualquer coisa que Tailwind não consiga lidar nativamente.

**Se CSS/CSS Modules:** Crie ou atualize um bloco de variáveis `:root` em globals.css. Atualize stylesheets de componentes para usar as novas variáveis.

**Se styled-components/Emotion:** Atualize o objeto theme. Substitua valores hardcoded de cor/espaçamento por design tokens.

**Em todos os casos:**
- Aplique cores, tipografia e espaçamento globalmente primeiro
- Depois aborde detalhes em nível de componente (botões, cards, nav) um de cada vez
- Preserve toda funcionalidade e estrutura de layout existentes — apenas propriedades visuais mudam
- Adicione qualquer efeito especial (glass blur, gradientes, animações) que defina o caráter do site de inspiração

Leia `references/apply-guide.md` para padrões de implementação específicos do framework.

### Passo 6: Mostrar Antes/Depois

Após aplicar as mudanças, apresente claramente:
- Quais arquivos foram modificados
- O mapeamento de design tokens (origem → o que você configurou)
- Qualquer efeito especial adicionado
- O que o usuário deve verificar visualmente (hover states, dark/light mode, mobile)

Se o usuário tiver um servidor dev rodando, lembre-o de verificar. Ofereça-se para iterar em componentes específicos.

## Princípios-Chave

**Linguagem de design, não markup.** A estrutura HTML e conteúdo do site de inspiração são deles. Você está extraindo a *linguagem de design* — como cores se relacionam, como espaçamento flui, o que dá ao site seu caráter — para aplicar como sua própria base criativa.

**Design tokens primeiro, código segundo.** Apressar-se em aplicar cores antes de entender o sistema completo leva a resultados inconsistentes. Sempre construa o mapa de tokens primeiro.

**Pergunte sobre escopo.** "Aplicar o design em tudo" vs "apenas fazer a homepage parecer assim" vs "apenas restyle da navbar" são trabalhos muito diferentes. Esclareça antes de prosseguir.

**Não quebre o que funciona.** Os componentes do usuário funcionam. Mude apenas propriedades visuais. Se tiver dúvida sobre se uma mudança pode quebrar layout, erre pelo lado da cautela e sinalize.

**Iterativo é ok.** Frequentemente é melhor acertar a base (cores, tipo, espaçamento) e deixar o usuário revisar antes de abordar detalhes em nível de componente.

## O Que Fazer Quando...

**O site usa um design system (Material, shadcn, etc.):** Identifique, diga ao usuário e pergunte se eles querem adotar o mesmo sistema ou apenas extrair os design tokens visuais.

**O CSS está minificado/ofuscado:** Volte à análise visual do screenshot. Você ainda consegue extrair cores, espaçamento e formas da inspeção visual.

**O site de inspiração é JS-renderizado e o scrape HTML volta principalmente vazio:** Anote isso ao usuário — o screenshot ainda funcionará para análise visual, mas extração de CSS será limitada. Você ainda consegue inferir a maioria dos tokens visualmente.

**O código do usuário usa uma biblioteca de componentes (shadcn, Chakra, MUI):** Aplique o design customizando o theme/config da biblioteca em vez de sobrepor componentes individuais.

**Múltiplas páginas precisam corresponder:** Use a homepage para design tokens gerais, mas ofereça-se para verificar páginas internas (ex: `/pricing`, `/docs`) se o usuário quiser corresponder ao look de uma página específica.