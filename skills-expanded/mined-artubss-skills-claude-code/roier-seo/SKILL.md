---
name: roier-seo
description: Auditor técnico de SEO e corretor. Executa auditorias Lighthouse/PageSpeed em websites ou servidores locais de desenvolvimento, analisa pontuações de SEO/performance/acessibilidade e implementa automaticamente correções para meta tags, dados estruturados, Core Web Vitals e problemas de acessibilidade.
version: 1.0.0
author: Kemeny Studio
license: MIT
tags: [SEO, Lighthouse, PageSpeed, Accessibility, Performance, Meta Tags, Structured Data, Core Web Vitals, WCAG, Next.js, React, Vue]
dependencies: [lighthouse, chrome-launcher]
---

# Roier SEO - Auditor Técnico de SEO & Corretor

Skill de otimização de SEO com IA que audita websites e implementa automaticamente correções.

## Quando usar esta skill

**Use Roier SEO quando:**
- Usuário pede para "auditar meu site" ou "verificar SEO"
- Usuário quer "melhorar performance" ou "corrigir problemas de SEO"
- Usuário menciona "lighthouse", "pagespeed" ou "core web vitals"
- Usuário quer adicionar/corrigir meta tags, dados estruturados ou acessibilidade
- Usuário tem um servidor local de desenvolvimento e quer análise de SEO

**Recursos principais:**
- **Auditorias Completas**: Auditorias Lighthouse em qualquer URL (localhost ou ativo)
- **Correção Automática**: Implementa correções diretamente no codebase
- **Framework Consciente**: Detecta Next.js, React, Vue, Nuxt, HTML simples
- **Core Web Vitals**: Rastreia métricas FCP, LCP, TBT, CLS
- **Dados Estruturados**: Schemas JSON-LD para rich snippets
- **Acessibilidade**: Correções de conformidade WCAG

**Use alternativas em vez desta:**
- **React Best Practices**: Para otimização geral de performance em React
- **Lighthouse Manual**: Para auditorias pontuais sem correção automática

## Início rápido

### Instalação

Após instalar a skill, instale as dependências de auditoria:

```bash
cd ~/.claude/skills/roier-seo/scripts
npm install
```

### Executando uma Auditoria

Para um **website ativo**:
```bash
node ~/.claude/skills/roier-seo/scripts/audit.js https://example.com
```

Para um **servidor local de desenvolvimento** (deve estar rodando):
```bash
node ~/.claude/skills/roier-seo/scripts/audit.js http://localhost:3000
```

Formatos de saída:
```bash
# Saída JSON (padrão, para uso programático)
node ~/.claude/skills/roier-seo/scripts/audit.js https://example.com

# Resumo legível por humanos
node ~/.claude/skills/roier-seo/scripts/audit.js https://example.com --output=summary

# Salvar em arquivo
node ~/.claude/skills/roier-seo/scripts/audit.js https://example.com --save=results.json
```

## Categorias de auditoria

A auditoria retorna pontuações (0-100) para cinco categorias:

| Categoria | Descrição | Peso |
|-----------|-----------|------|
| **Performance** | Velocidade de carregamento da página, Core Web Vitals | Alto |
| **Acessibilidade** | Conformidade WCAG, suporte a leitores de tela | Alto |
| **Best Practices** | Segurança, padrões web modernos | Médio |
| **SEO** | Otimização para mecanismos de busca, rastreabilidade | Alto |
| **PWA** | Conformidade com Progressive Web App | Baixo |

## Padrões técnicos de correção de SEO

### Meta tags (HTML Head)

#### Tag title
```html
<!-- Ruim -->
<title>Home</title>

<!-- Bom -->
<title>Palavra-chave Principal - Palavra-chave Secundária | Nome da Marca</title>
```

**Regras:**
- Máximo 50-60 caracteres
- Incluir palavra-chave principal perto do início
- Única por página
- Incluir nome da marca no final

#### Meta description
```html
<meta name="description" content="Descrição atrativa com palavras-chave. 150-160 caracteres que encorajam cliques nos resultados de busca.">
```

**Regras:**
- 150-160 caracteres
- Incluir palavras-chave primárias e secundárias naturalmente
- Call-to-action atrativo
- Única por página

#### Meta tags essenciais
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<html lang="pt-BR">
```

### Open Graph tags (compartilhamento social)

```html
<meta property="og:title" content="Título da Página">
<meta property="og:description" content="Descrição da página">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Nome da Marca">
```

### Twitter Card tags

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Título da Página">
<meta name="twitter:description" content="Descrição da página">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

### URL Canônica

```html
<link rel="canonical" href="https://example.com/pagina-canonica">
```

### Meta robots

```html
<!-- Permitir indexação (padrão) -->
<meta name="robots" content="index, follow">

<!-- Prevenir indexação (para staging, páginas admin) -->
<meta name="robots" content="noindex, nofollow">
```

## Dados estruturados (JSON-LD)

### Schema de website
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Nome do Site",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
```

### Schema de organização
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Nome da Empresa",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/empresa",
    "https://linkedin.com/company/empresa"
  ]
}
</script>
```

### Schema BreadcrumbList
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com"},
    {"@type": "ListItem", "position": 2, "name": "Categoria", "item": "https://example.com/category"},
    {"@type": "ListItem", "position": 3, "name": "Página"}
  ]
}
</script>
```

### Schema de artigo (para posts de blog)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Título do Artigo",
  "author": {"@type": "Person", "name": "Nome do Autor"},
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20",
  "image": "https://example.com/article-image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Nome da Publicadora",
    "logo": {"@type": "ImageObject", "url": "https://example.com/logo.png"}
  }
}
</script>
```

## Otimizações de performance

### Otimização de imagens

```html
<!-- Adicionar width/height para prevenir CLS -->
<img src="image.jpg" alt="Descrição" width="800" height="600">

<!-- Adicionar lazy loading -->
<img src="image.jpg" alt="Descrição" loading="lazy">

<!-- Usar formatos modernos -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Descrição">
</picture>
```

### Otimização de fontes

```html
<!-- Preload de fontes críticas -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
```

```css
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
}
```

### Resource hints

```html
<!-- Preconnect para origens críticas de terceiros -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com">

<!-- DNS prefetch para origens não críticas -->
<link rel="dns-prefetch" href="https://analytics.example.com">

<!-- Preload de recursos críticos -->
<link rel="preload" href="/critical.css" as="style">
```

## Correções de acessibilidade

### Texto alternativo
```html
<!-- Bom (descritivo) -->
<img src="photo.jpg" alt="Membros da equipe colaborando no escritório">

<!-- Bom (decorativo) -->
<img src="decoration.jpg" alt="" role="presentation">
```

### Contraste de cores
- **4.5:1** razão de contraste para texto normal
- **3:1** razão de contraste para texto grande (18px+ ou 14px+ bold)

### Labels de formulário
```html
<label for="email">Endereço de Email</label>
<input type="email" id="email" name="email">
```

### Skip link
```html
<a href="#main-content" class="skip-link">Pular para conteúdo principal</a>

<style>
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  left: 0;
  top: 0;
  z-index: 9999;
  background: #000;
  color: #fff;
  padding: 8px 16px;
}
</style>
```

### Acessibilidade de botão
```html
<!-- Botão com ícone precisa de aria-label -->
<button aria-label="Fechar menu">
  <svg>...</svg>
</button>
```

## Padrões específicos de framework

### Next.js (App Router)

```tsx
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: {
    default: 'Nome do Site',
    template: '%s | Nome do Site'
  },
  description: 'Descrição do site',
  openGraph: {
    title: 'Nome do Site',
    description: 'Descrição do site',
    url: 'https://example.com',
    siteName: 'Nome do Site',
    type: 'website',
  },
}
```

### Next.js (Pages Router)

```jsx
import Head from 'next/head';

export default function Page() {
  return (
    <>
      <Head>
        <title>Título da Página | Marca</title>
        <meta name="description" content="Descrição da página" />
        <link rel="canonical" href="https://example.com/page" />
      </Head>
      <main>...</main>
    </>
  );
}
```

### React (com react-helmet)

```jsx
import { Helmet } from 'react-helmet';

function Page() {
  return (
    <>
      <Helmet>
        <title>Título da Página | Marca</title>
        <meta name="description" content="Descrição da página" />
      </Helmet>
      <main>...</main>
    </>
  );
}
```

### Vue.js (com useHead)

```vue
<script setup>
useHead({
  title: 'Título da Página | Marca',
  meta: [
    { name: 'description', content: 'Descrição da página' }
  ],
  link: [
    { rel: 'canonical', href: 'https://example.com/page' }
  ]
})
</script>
```

### Nuxt.js

```vue
<script setup>
useSeoMeta({
  title: 'Título da Página | Marca',
  description: 'Descrição da página',
  ogTitle: 'Título da Página',
  ogDescription: 'Descrição da página',
  ogImage: 'https://example.com/og-image.jpg'
})
</script>
```

## Fluxo de trabalho

### Passo 1: Auditoria
Execute o script de auditoria na URL alvo:
```bash
node ~/.claude/skills/roier-seo/scripts/audit.js <URL>
```

### Passo 2: Identificar framework
Verifique as dependências em `package.json` e arquivos específicos do framework.

### Passo 3: Priorizar correções
1. **Crítico** (vermelho): Corrigir imediatamente
2. **Sério** (laranja): Corrigir em breve
3. **Moderado** (amarelo): Corrigir quando possível
4. **Menor** (cinza): Bom ter

### Passo 4: Implementar
Use os padrões de correção acima, adaptados ao framework do usuário.

### Passo 5: Re-auditar
Execute a auditoria novamente para verificar as melhorias.

## Requisitos

- **Node.js 18+**
- **Chrome/Chromium** browser (para Lighthouse)
- Dependências do script de auditoria (instaladas via npm)

## Recursos

- [Google Lighthouse](https://developer.chrome.com/docs/lighthouse/)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Schema.org](https://schema.org/)
- [Diretrizes WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [Core Web Vitals](https://web.dev/vitals/)

## Histórico de versões

**v1.0.0** (Janeiro 2026)
- Lançamento inicial
- Integração de auditoria Lighthouse
- 50+ padrões de correção de SEO
- Suporte a framework para Next.js, React, Vue, Nuxt