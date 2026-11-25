---
name: aeo-geo-bestpractices
description: >-
  Otimiza qualquer landing page ou aplicação web (React, Vite, Next.js, Angular,
  Vue, Nuxt, Astro, HTML) para
  atingir nota máxima (98-100) no Google Lighthouse 13 em Performance, Accessibility,
  Best Practices, SEO e Agentic Browsing, aplicando técnicas avançadas de SEO,
  AEO (Answer Engine Optimization) e GEO (Generative Engine Optimization para ChatGPT,
  Perplexity, Claude e Gemini). Use quando o usuário pedir para melhorar SEO, AEO,
  GEO, ser encontrado por IAs/buscadores, criar llms.txt/ard.json ou bater nota 100
  no Google Lighthouse.
---

# /aeo-geo-bestpractices — SEO + AEO + GEO + Lighthouse 100 Playbook

Workflow completo para transformar qualquer página ou SPA em uma máquina de descoberta orgânica (**SEO**), motores de resposta (**AEO**) e motores generativos/agentes de IA (**GEO**), garantindo simultaneamente **98–100 no Google Lighthouse 13** (Desktop e Mobile) nas 5 categorias: `Performance`, `Accessibility`, `Best Practices`, `SEO` e `Agentic Browsing`.

Caminhos: `<skill>` é a pasta onde este `SKILL.md` está localizado.

---

## 0. Alinhamento Rápido Antes de Executar

### 0.1. Detecte a stack e leia o guia correspondente

As regras deste arquivo valem para qualquer site. O que muda entre frameworks (onde fica o `<head>`, a pasta pública, como pré-renderizar, como otimizar imagens e evitar TBT, qual comando sobe o preview) está em `references/frameworks/`. Identifique a stack pelo projeto e **leia o guia antes de aplicar as etapas 1 a 5**:

| Sinal no projeto | Stack | Guia |
| --- | --- | --- |
| `angular.json` ou `@angular/core` | Angular | [`references/frameworks/angular.md`](./references/frameworks/angular.md) |
| `next.config.*` ou `next` | Next.js | [`references/frameworks/nextjs.md`](./references/frameworks/nextjs.md) |
| `nuxt.config.*` ou `nuxt` / `vite.config.*` + `vue` | Nuxt / Vue + Vite | [`references/frameworks/vue-nuxt.md`](./references/frameworks/vue-nuxt.md) |
| `astro.config.*` ou `astro` | Astro | [`references/frameworks/astro.md`](./references/frameworks/astro.md) |
| `vite.config.*` + `react` | Vite + React | [`references/frameworks/vite-react.md`](./references/frameworks/vite-react.md) |
| `index.html` sem framework | HTML estático | [`references/frameworks/html-estatico.md`](./references/frameworks/html-estatico.md) |

Se a stack não estiver na lista (ex.: SvelteKit, Remix, Gatsby, WordPress), aplique as regras gerais deste arquivo e use o guia mais parecido como referência: frameworks com SSR/SSG seguem a lógica de Next/Nuxt; SPAs seguem a de Vite + React.

### 0.2. Confirme com o usuário

Antes de alterar o código, confirme (ou extraia do próprio projeto se já estiver explícito):
1. **Domínio canônico de produção** (ex.: `https://meusite.com.br/`). Se ainda não houver domínio definido, pergunte ou use um placeholder claro e avise o usuário.
2. **FAQ Visível vs. Invisível (apenas AEO/GEO)**:
   - Pergunte se o usuário quer a seção de **Perguntas Frequentes (FAQ)** visível no layout da página (`<details>/<summary>`) **ou** apenas invisível nos bastidores (dentro do `@graph` JSON-LD + `llms.txt` + `<noscript>`) para não alterar o design visual.
3. **Preferência de rastreamento para treino (ao criar ou alterar `robots.txt`)**:
   - Verifique se o site já definiu uma preferência. Se não houver uma escolha clara, ofereça duas opções: permitir busca e bloquear o rastreamento para treino da OpenAI e da Anthropic; ou permitir também esse rastreamento para treino. Preserve as demais regras do site.

---

## 1. SEO Técnico Completo (`index.html`, `robots.txt`, `sitemap.xml`)

Consulte os templates prontos em [`references/templates.md`](./references/templates.md).

1. **Meta Tags Essenciais no `<head>`**:
   - `<html lang="pt-BR">` (ou idioma do projeto).
   - `<title>` forte (50–65 caracteres) com Nome da Marca/Especialista + Proposta Principal.
   - `<meta name="description">` (140–165 caracteres) respondendo claramente *o que é*, *para quem é* e *o que inclui*.
   - `<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />`
   - `<link rel="canonical" href="https://dominio.com/" />` + `<link rel="alternate" hreflang="pt-BR" ... />` e `x-default`.
   - Open Graph completo (`og:type`, `og:locale`, `og:site_name`, `og:title`, `og:description`, `og:url`, `og:image`, `og:image:width`, `og:image:height`, `og:image:alt`) e Twitter Cards (`summary_large_image`).
2. **`public/robots.txt` Amigável para Buscadores e IAs**:
   - Para manter a possibilidade de aparecer nas buscas do ChatGPT e do Claude, permita `OAI-SearchBot` e `Claude-SearchBot`. `Claude-User` pode buscar páginas em resposta a pedidos de usuários; `ChatGPT-User` também é acionado por usuários, mas não controla a inclusão na busca do ChatGPT.
   - `GPTBot` e `ClaudeBot` são os bots documentados para possível uso do conteúdo em treino. Se o usuário optar por bloquear esse rastreamento, use grupos próprios com `Disallow: /` para ambos, sem bloquear os bots de busca. Se optar por permiti-lo, use `Allow: /` para ambos. Veja as duas variantes em [`references/templates.md`](./references/templates.md).
   - Trate controles de outros provedores, como `Google-Extended`, separadamente. Permitir acesso aos bots de busca aumenta a elegibilidade, mas não garante citação ou presença nas respostas. Consulte as [orientações da OpenAI](https://developers.openai.com/api/docs/bots) e da [Anthropic](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) ao atualizar a lista de bots.
   - Aponte `Sitemap: https://dominio.com/sitemap.xml`.
3. **`public/sitemap.xml` Rico (Imagens + Vídeo)**:
   - Inclua os namespaces `xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"` e `xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"` quando houver imagens de destaque e vídeo de vendas/apresentação.

---

## 2. AEO — Answer Engine Optimization (Featured Snippets, Voz e Crawlers sem JS)

Motores de resposta precisam de **entidades conectadas** e **HTML semântico legível sem executar JavaScript**:

1. **Grafo Conectado `@graph` em `Schema.org` JSON-LD**:
   - Em vez de scripts JSON-LD soltos, crie um único `<script type="application/ld+json">` com `@graph` conectando as entidades por `@id` (veja o modelo em [`references/templates.md`](./references/templates.md)):
     - `WebSite` (`#website`)
     - `Person` ou `Organization` (`#person` / `#org`) com `sameAs` para redes sociais oficiais
     - `WebPage` (`#webpage`) com `about` e `mainEntity`
     - `Product` / `SoftwareApplication` / `Service` (`#product`) com `offers`
     - `Course` (`#course`) quando houver curso/treinamento/bônus educacional
     - `VideoObject` (`#video`) quando houver VSL ou vídeo de apresentação
     - `FAQPage` (`#faq`) com 4 a 6 perguntas reais de alta intenção de busca e respostas diretas e completas (40–70 palavras cada).
2. **Fallback Semântico `<noscript>` para SPAs (React / Vue / Vite)**:
   - Só se aplica a SPAs sem pré-renderização. Em Next.js, Nuxt, Astro, Angular com SSR/prerender e HTML estático, o HTML já chega completo e o `<noscript>` é desnecessário (veja o guia da stack).
   - Crawlers de LLMs (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `OAI-SearchBot`) frequentemente fazem fetch apenas do HTML bruto e **não executam o bundle JavaScript**.
   - Em projetos SPA onde `<div id="root"></div>` vem vazio, adicione um bloco `<noscript><main>...</main></noscript>` no `index.html` contendo o `<h1>`, resumo da oferta, lista de entregáveis (`<ul><li>`) e link direto para o CTA/checkout.
   - **Importante para Performance**: Use `<noscript>` (e não elementos dentro de `<div id="root">` quando usar `createRoot().render()`), pois colocar DOM dentro de `#root` sem SSR faz o React desmontar e recriar toda a árvore no mount, atrasando o LCP e gerando TBT.

---

## 3. GEO & Agentic Browsing (Nota 100 no Lighthouse 13)

O Google Lighthouse 13 introduziu a categoria **Agentic Browsing**, que audita se a página está preparada para agentes autônomos e LLMs (`llms-txt` e `ard-schema`).

1. **`public/llms.txt` + Link no `<head>`**:
   - Crie `public/llms.txt` em Markdown estruturado (veja [`references/templates.md`](./references/templates.md)) contendo:
     - `# Nome do Produto / Marca`
     - `> Resumo em uma frase da proposta de valor`
     - Seções claras: `## Sobre`, `## O Que Está Incluído`, `## Bônus / Condições`, `## Perguntas Frequentes (AEO / GEO)`, `## Links Oficiais`.
   - No `<head>` do `index.html`, adicione:
     `<link rel="help" type="text/plain" href="/llms.txt" title="LLMs.txt — Informações estruturadas para IAs" />`
2. **`public/.well-known/ard.json` (Agent Resource Discovery v0.91)**:
   - Em SPAs (Vite, Next, etc.), rotas inexistentes como `/.well-known/ard.json` retornam o `index.html` (`<!doctype html>`) por fallback, fazendo a auditoria `ard-schema` do Lighthouse 13 falhar com erro de parse JSON.
   - Crie sempre o arquivo `public/.well-known/ard.json` seguindo o schema oficial ARD v0.91 (modelo exato em [`references/templates.md`](./references/templates.md)):
     - Deve conter `ardVersion: "0.91.0"` e `entries` com `identifier` no formato `urn:air:<dominio>:<tipo>:<slug>`, `displayName`, `type: "application/agent-skills+md"`, `url` apontando para `/llms.txt`, `description` e `representativeQueries`.

---

## 4. Google Lighthouse 100/100: Performance & Acessibilidade

Para atingir **98–100 no Mobile (4G Simulado + 4x CPU Throttling)** e **100 no Desktop**, aplique rigorosamente estas regras:

### 4.1. LCP (Largest Contentful Paint < 2.1s no Mobile)
1. **Preload no Topo do `<head>`**:
   - Coloque o `<link rel="preload" as="image" ... fetchpriority="high">` **logo abaixo do `<title>`** (nas primeiras 15 linhas do `index.html`), antes das dezenas de meta tags Open Graph e do JSON-LD.
2. **Calibragem de `srcSet` e `sizes` para o DPR `1.75x` do Lighthouse Mobile**:
   - O Lighthouse Mobile emula um **Moto G Power (`412px` de largura com `devicePixelRatio: 1.75`)**.
   - Se uma imagem tiver `sizes="(max-width: 767px) 260px, 500px"`, o Chrome calcula `260 * 1.75 = 455w`. Se a versão mobile no `srcSet` for declarada como `260w` (menor que `455w`), o Chrome **ignora a imagem mobile** e baixa a versão desktop pesada!
   - **Regra de ouro**: Declare a imagem mobile no `srcSet` com largura `>= ceil(largura_css_mobile * 1.8)` (ex.: `450w` para imagens de `240px`, ou `680w` para imagens de `360px` full-width no mobile) e comprima em WebP (`< 30 KB`).
3. **Evite que Imagens Decorativas de Fundo "Roubem" o LCP**:
   - Se a seção Hero tiver uma foto decorativa de fundo (`opacity: 0.15`) com caixa (`boundingRect`) maior que o retrato principal ou `<h1>`, o Chrome vai considerá-la o elemento LCP.
   - No mobile (`@media (max-width: 767px)`), oculte fotos de fundo gigantes puramente decorativas (`display: none`) ou reduza suas dimensões para que o elemento principal (pré-carregado com `fetchpriority="high"`) seja o único candidato a LCP.
4. **Não Faça Preload de Fontes que Competem com o JS/CSS Crítico em SPAs**:
   - Use `font-display: swap` no `@font-face` e deixe o navegador priorizar o download do CSS e do bundle JS inicial antes da fonte secundária.

### 4.2. TBT Zero (`0ms` Total Blocking Time)
1. **Substitua Animações Contínuas de JS por CSS Compositor + `IntersectionObserver`**:
   - Bibliotecas completas de animação no bundle inicial adicionam `50–150 KB` de JS e bloqueiam a main thread na hidratação.
   - Para reveals de scroll, use `IntersectionObserver` nativo alternando uma classe `.is-visible` com `transition: opacity, transform` acelerada por GPU (`translate3d`).
   - Para partículas ou rotações contínuas, use `@keyframes` em CSS com `transform: translate3d(...)` / `rotate(...)` e `will-change: transform`.
2. **Cuidado com Filtros SVG (`<feTurbulence>`, `drop-shadow`) e SMIL `<animate>` no Load**:
   - Nunca use `<feTurbulence>` em tela cheia sem dimensões fixas (ele recalcula ruído Perlin em milhões de pixels na CPU, gerando Long Tasks de `300ms+`). Prefira `radial-gradient` leve em CSS.
   - Nunca combine `filter: drop-shadow(...)` em um elemento pai cujo SVG filho sofre mutação de geometria a cada frame no carregamento inicial. Se houver morphing de `<path>` via `<animate attributeName="d">`, ative o morphing apenas após a primeira interação do usuário (`pointermove`, `touchstart`, `wheel`) ou após o carregamento inicial (`setTimeout` de `8000ms`), mantendo apenas a rotação CSS na GPU durante o load.
3. **Code-Splitting de Smooth Scroll (`Lenis`)**:
   - Carregue o `Lenis` dinamicamente (`await import("lenis")`) apenas no primeiro evento `wheel`, `touchstart` ou `keydown` (`{ passive: true, once: true }`). Assim ele pesa `0 KB` e `0ms` de CPU no carregamento inicial.
4. **Isole Timers (`setInterval` / Contadores de Urgência) em Componentes Folha**:
   - **Nunca** coloque um hook `useCountdown` (`setInterval` de 1s) no componente raiz `<App />`. Isso força o React a re-renderizar a página inteira a cada segundo durante o teste do Lighthouse. Isole o estado do relógio em um pequeno componente `<CountdownClock />` que renderiza apenas os dígitos.

### 4.3. Acessibilidade Nota 100 (WCAG AA)
1. **Contraste de Cores (`color-contrast`)**:
   - Textos pequenos sobre fundo escuro (`#10100f` / `#171512`) precisam de razão de contraste `>= 4.5:1`. Use tons claros para textos secundários (`#c4beb4`, `#d6c5b2`) e laranjas luminosos para destaques sobre fundo escuro (`#ff9452`, `#ffa36b`).
   - Botões com fundo laranja vibrante (`#ff772f`) devem usar texto escuro (`#140c06`) para contraste máximo.
2. **Consistência entre Texto Visível e Nome Acessível (`label-content-name-mismatch`)**:
   - Nunca coloque um `aria-label` em um link/botão que não contenha exatamente o texto visível dentro dele (ex.: se a logo diz `CF ZANELLA.`, não coloque `aria-label="Início"`).
3. **Semântica e Teclado**:
   - Inclua `<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>` como primeiro foco do `<body>`.
   - Use hierarquia estrita de títulos (`h1` -> `h2` -> `h3`), `aria-labelledby` em todas as `<section>`, e `aria-pressed` em seletores de estado.

---

## 5. Validação Automatizada com Google Lighthouse

Sempre valide as alterações rodando o script automatizado da skill:

```bash
# Projeto local: detecta a stack, roda `npm run build` (se existir) e sobe o preview na porta 4173
node <skill>/scripts/run-lighthouse.mjs

# Pular o build (quando a saída do build já está atualizada)
node <skill>/scripts/run-lighthouse.mjs --no-build

# Forçar a stack se a detecção errar: angular | next | nuxt | astro | vite | static
node <skill>/scripts/run-lighthouse.mjs --stack=angular

# Testar uma URL específica (local ou produção), sem build nem preview
node <skill>/scripts/run-lighthouse.mjs https://meusite.com.br
```

- Sem URL, o script detecta a stack, executa `npm run build` quando o `package.json` tiver um script `build`, sobe o servidor de preview adequado (`vite preview`, `next start`, `astro preview`, servidor do Nuxt ou `npx serve` na pasta de saída do Angular / HTML estático) e roda o **Google Lighthouse 13** em **Desktop** e **Mobile**. Com URL, testa direto o endereço informado.
- Ao final, exibe a tabela de notas das 5 categorias (`performance`, `accessibility`, `best-practices`, `seo`, `agentic-browsing`) e lista detalhadamente qualquer auditoria que não tenha atingido nota máxima para correção imediata.
- Requer o Google Chrome instalado. Se o projeto precisar de um servidor próprio (SSR com adapter específico, backend customizado), suba-o manualmente e passe a URL como argumento.

