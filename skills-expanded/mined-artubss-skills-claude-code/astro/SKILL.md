---
name: astro
description: "Construa sites focados em conteúdo com Astro — zero JS por padrão, arquitetura de ilhas, componentes multi-framework e suporte a Markdown/MDX."
category: frontend
risk: safe
source: community
date_added: "2026-03-18"
author: suhaibjanjua
tags: [astro, ssg, ssr, islands, content, markdown, mdx, performance]
tools: [claude, cursor, gemini]
---

# Framework Web Astro

## Visão Geral

Astro é um framework web projetado para sites ricos em conteúdo — blogs, documentação, portfólios, páginas de marketing e e-commerce. Sua inovação central é a **Arquitetura de Ilhas**: por padrão, Astro não envia JavaScript para o navegador. Componentes interativos são seletivamente hidratados como "ilhas" isoladas. Astro suporta React, Vue, Svelte, Solid e outros frameworks UI simultaneamente no mesmo projeto, permitindo que você escolha a ferramenta certa para cada componente.

## Quando Usar Esta Habilidade

- Use ao construir um blog, site de documentação, página de marketing ou portfólio
- Use quando desempenho e Core Web Vitals são a prioridade principal
- Use quando o projeto é pesado em conteúdo com arquivos Markdown ou MDX
- Use quando você quer saída SSG (estática) com SSR opcional para rotas dinâmicas
- Use quando o usuário pergunta sobre arquivos `.astro`, `Astro.props`, coleções de conteúdo ou diretivas `client:`

## Como Funciona

### Passo 1: Configuração do Projeto

```bash
npm create astro@latest my-site
cd my-site
npm install
npm run dev
```

Adicione integrações conforme necessário:

```bash
npx astro add tailwind        # Tailwind CSS
npx astro add react           # Suporte a componentes React
npx astro add mdx             # Suporte a MDX
npx astro add sitemap         # Gerar sitemap.xml automaticamente
npx astro add vercel          # Adaptador SSR Vercel
```

Estrutura do projeto:

```
src/
  pages/          ← Roteamento baseado em arquivo (.astro, .md, .mdx)
  layouts/        ← Shells de página reutilizáveis
  components/     ← Componentes UI (.astro, .tsx, .vue, etc.)
  content/        ← Coleções de conteúdo com segurança de tipo (Markdown/MDX)
  styles/         ← CSS global
public/           ← Ativos estáticos (copiados como-estão)
astro.config.mjs  ← Configuração do framework
```

### Passo 2: Sintaxe de Componentes Astro

Arquivos `.astro` têm uma cerca de código no topo (apenas no servidor) e um template abaixo:

```astro
---
// src/components/Card.astro
// Este bloco executa apenas no servidor — nunca no navegador
interface Props {
  title: string;
  href: string;
  description: string;
}

const { title, href, description } = Astro.props;
---

<article class="card">
  <h2><a href={href}>{title}</a></h2>
  <p>{description}</p>
</article>

<style>
  /* Automaticamente escopo para este componente */
  .card { border: 1px solid #eee; padding: 1rem; }
</style>
```

### Passo 3: Páginas Baseadas em Arquivo e Roteamento

```
src/pages/index.astro          → /
src/pages/about.astro          → /about
src/pages/blog/[slug].astro    → /blog/:slug (dinâmico)
src/pages/blog/[...path].astro → /blog/* (catch-all)
```

Rota dinâmica com `getStaticPaths`:

```astro
---
// src/pages/blog/[slug].astro
export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<h1>{post.data.title}</h1>
<Content />
```

### Passo 4: Coleções de Conteúdo

Coleções de conteúdo fornecem acesso com segurança de tipo a arquivos Markdown e MDX:

```typescript
// src/content/config.ts
import { z, defineCollection } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

```astro
---
// src/pages/blog/index.astro
import { getCollection } from 'astro:content';

const posts = (await getCollection('blog'))
  .filter(p => !p.data.draft)
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
---

<ul>
  {posts.map(post => (
    <li>
      <a href={`/blog/${post.slug}`}>{post.data.title}</a>
      <time>{post.data.date.toLocaleDateString()}</time>
    </li>
  ))}
</ul>
```

### Passo 5: Ilhas — Hidratação Seletiva

Por padrão, componentes de frameworks UI renderizam como HTML estático sem JS. Use diretivas `client:` para hidratar:

```astro
---
import Counter from '../components/Counter.tsx';  // Componente React
import VideoPlayer from '../components/VideoPlayer.svelte';
---

<!-- HTML estático — nenhum JavaScript enviado ao navegador -->
<Counter initialCount={0} />

<!-- Hidratar imediatamente no carregamento da página -->
<Counter initialCount={0} client:load />

<!-- Hidratar quando o componente entra na visualização -->
<VideoPlayer src="/demo.mp4" client:visible />

<!-- Hidratar apenas quando o navegador está ocioso -->
<Analytics client:idle />

<!-- Hidratar apenas em um media query específico -->
<MobileMenu client:media="(max-width: 768px)" />
```

### Passo 6: Layouts

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description?: string;
}
const { title, description = 'My Astro Site' } = Astro.props;
---

<html lang="pt-br">
  <head>
    <meta charset="utf-8" />
    <title>{title}</title>
    <meta name="description" content={description} />
  </head>
  <body>
    <nav>...</nav>
    <main>
      <slot />  <!-- conteúdo da página renderiza aqui -->
    </main>
    <footer>...</footer>
  </body>
</html>
```

```astro
---
// src/pages/about.astro
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="Sobre Nós">
  <h1>Sobre Nós</h1>
  <p>Bem-vindo à nossa empresa...</p>
</BaseLayout>
```

### Passo 7: Modo SSR (Renderização sob Demanda)

Habilite SSR para páginas dinâmicas definindo um adaptador:

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel/serverless';

export default defineConfig({
  output: 'hybrid',  // 'static' | 'server' | 'hybrid'
  adapter: vercel(),
});
```

Opte por páginas individuais em SSR com `export const prerender = false`.

## Exemplos

### Exemplo 1: Blog com Feed RSS

```typescript
// src/pages/rss.xml.ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog');
  return rss({
    title: 'Meu Blog',
    description: 'Últimas postagens',
    site: context.site,
    items: posts.map(post => ({
      title: post.data.title,
      pubDate: post.data.date,
      link: `/blog/${post.slug}/`,
    })),
  });
}
```

### Exemplo 2: Endpoint de API (SSR)

```typescript
// src/pages/api/subscribe.ts
import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  const { email } = await request.json();

  if (!email) {
    return new Response(JSON.stringify({ error: 'Email obrigatório' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  await addToNewsletter(email);
  return new Response(JSON.stringify({ success: true }), { status: 200 });
};
```

### Exemplo 3: Componente React como Ilha

```tsx
// src/components/SearchBox.tsx
import { useState } from 'react';

export default function SearchBox() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  async function search(e: React.FormEvent) {
    e.preventDefault();
    const data = await fetch(`/api/search?q=${query}`).then(r => r.json());
    setResults(data);
  }

  return (
    <form onSubmit={search}>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <button type="submit">Pesquisar</button>
      <ul>{results.map(r => <li key={r.id}>{r.title}</li>)}</ul>
    </form>
  );
}
```

```astro
---
import SearchBox from '../components/SearchBox.tsx';
---
<!-- Hidratada imediatamente — esta ilha é interativa -->
<SearchBox client:load />
```

## Melhores Práticas

- ✅ Mantenha a maioria dos componentes como arquivos estáticos `.astro` — hidrate apenas o que deve ser interativo
- ✅ Use coleções de conteúdo para todo conteúdo Markdown/MDX — você obtém segurança de tipo e validação automática
- ✅ Prefira `client:visible` em vez de `client:load` para componentes abaixo da dobra para reduzir o JS inicial
- ✅ Use `import.meta.env` para variáveis de ambiente — prefixe variáveis públicas com `PUBLIC_`
- ✅ Adicione `<ViewTransitions />` de `astro:transitions` para navegação suave de página sem SPA completa
- ❌ Não use `client:load` em cada componente — isso anula a vantagem de desempenho do Astro
- ❌ Não coloque segredos no frontmatter `.astro` que sejam usados em templates voltados para o cliente
- ❌ Não pule `getStaticPaths` para rotas dinâmicas em modo estático — as builds falharão

## Notas de Segurança

- Código no frontmatter de arquivos `.astro` executa apenas no servidor e nunca é exposto ao navegador.
- Use `import.meta.env.PUBLIC_*` apenas para valores não-sensíveis. Variáveis de ambiente privadas (sem prefixo `PUBLIC_`) nunca são enviadas ao cliente.
- Ao usar modo SSR, valide todas as entradas `Astro.request` antes de consultas a banco de dados ou chamadas de API.
- Desinfete qualquer conteúdo fornecido pelo usuário antes de renderizar com `set:html` — isso ignora escapamento automático.

## Armadilhas Comuns

- **Problema:** JavaScript de um componente React/Vue não executa no navegador
  **Solução:** Adicione uma diretiva `client:` (`client:load`, `client:visible`, etc.) — sem ela, componentes renderizam como HTML estático apenas.

- **Problema:** Dados `getStaticPaths` ficam desatualizados após atualizações de conteúdo durante o dev
  **Solução:** O servidor dev do Astro observa arquivos de conteúdo — reinicie se mudanças em `content/config.ts` não forem refletidas.

- **Problema:** Tipo de `Astro.props` é `any` — sem autocompletar
  **Solução:** Defina uma interface ou tipo `Props` no frontmatter e o Astro inferirá automaticamente.

- **Problema:** CSS de um componente `.astro` vaza para outros componentes
  **Solução:** Estilos em tags `<style>` de `.astro` têm escopo automático. Use `:global()` apenas quando intentar direcionar filhos.

## Habilidades Relacionadas

- `@sveltekit` — Quando você precisa de um framework full-stack com UI reativa (vs foco em conteúdo do Astro)
- `@nextjs-app-router-patterns` — Quando você precisa de um framework full-stack primeiro em React
- `@tailwind-patterns` — Estilizar sites Astro com Tailwind CSS
- `@progressive-web-app` — Adicionar capacidades PWA a um site Astro