---
name: sveltekit
description: "Construa aplicações web full-stack com SvelteKit — roteamento baseado em arquivos, SSR, SSG, rotas de API e ações de formulário em um único framework."
category: frontend
risk: safe
source: community
date_added: "2026-03-18"
author: suhaibjanjua
tags: [svelte, sveltekit, fullstack, ssr, ssg, typescript]
tools: [claude, cursor, gemini]
---

# Desenvolvimento Full-Stack com SvelteKit

## Visão Geral

SvelteKit é o framework full-stack oficial construído sobre Svelte. Oferece roteamento baseado em arquivos, renderização no servidor (SSR), geração de sites estáticos (SSG), rotas de API e ações de formulário progressivas — tudo com o modelo de reatividade em tempo de compilação do Svelte que não adiciona overhead de runtime ao navegador. Use essa skill ao construir aplicações web rápidas e modernas onde tanto a experiência do desenvolvedor quanto o desempenho importam.

## Quando Usar Essa Skill

- Use ao construir uma nova aplicação web full-stack com Svelte
- Use quando você precisa de SSR ou SSG com controle fino por rota
- Use ao migrar uma SPA para um framework com capacidades de servidor
- Use ao trabalhar em um projeto que necessite roteamento baseado em arquivos e endpoints de API colocados
- Use quando o usuário pergunta sobre `+page.svelte`, `+layout.svelte`, funções `load` ou ações de formulário

## Como Funciona

### Passo 1: Configuração do Projeto

```bash
npm create svelte@latest my-app
cd my-app
npm install
npm run dev
```

Escolha **Skeleton project** + **TypeScript** + **ESLint/Prettier** quando solicitado.

Estrutura de diretórios após scaffolding:

```
src/
  routes/
    +page.svelte        ← Componente de página raiz
    +layout.svelte      ← Layout raiz (envolve todas as páginas)
    +error.svelte       ← Limite de erro
  lib/
    server/             ← Código exclusivo do servidor (nunca agrupado ao cliente)
    components/         ← Componentes compartilhados
  app.html              ← Shell HTML
static/                 ← Ativos estáticos
```

### Passo 2: Roteamento Baseado em Arquivos

Cada arquivo `+page.svelte` em `src/routes/` mapeia diretamente para uma URL:

```
src/routes/+page.svelte          → /
src/routes/about/+page.svelte    → /about
src/routes/blog/[slug]/+page.svelte  → /blog/:slug
src/routes/shop/[...path]/+page.svelte → /shop/* (catch-all)
```

**Grupos de rotas** (sem segmento de URL): envolva em pasta `(group)/`.
**Rotas privadas** (não acessíveis como URLs): prefixe com `_` ou `(group)`.

### Passo 3: Carregando Dados com Funções `load`

Use um arquivo `+page.ts` (universal) ou `+page.server.ts` (exclusivo do servidor) ao lado da página:

```typescript
// src/routes/blog/[slug]/+page.server.ts
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
  const post = await fetch(`/api/posts/${params.slug}`).then(r => r.json());

  if (!post) {
    error(404, 'Post not found');
  }

  return { post };
};
```

```svelte
<!-- src/routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';
  export let data: PageData;
</script>

<h1>{data.post.title}</h1>
<article>{@html data.post.content}</article>
```

### Passo 4: Rotas de API (Server Endpoints)

Crie arquivos `+server.ts` para endpoints no estilo REST:

```typescript
// src/routes/api/posts/+server.ts
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
  const limit = Number(url.searchParams.get('limit') ?? 10);
  const posts = await db.post.findMany({ take: limit });
  return json(posts);
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();
  const post = await db.post.create({ data: body });
  return json(post, { status: 201 });
};
```

### Passo 5: Ações de Formulário

Ações de formulário são a maneira nativa do SvelteKit para lidar com mutações — sem necessidade de fetch no cliente:

```typescript
// src/routes/contact/+page.server.ts
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    const email = data.get('email');

    if (!email) {
      return fail(400, { email, missing: true });
    }

    await sendEmail(String(email));
    redirect(303, '/thank-you');
  }
};
```

```svelte
<!-- src/routes/contact/+page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';
  export let form: ActionData;
</script>

<form method="POST" use:enhance>
  <input name="email" type="email" />
  {#if form?.missing}<p class="error">Email is required</p>{/if}
  <button type="submit">Subscribe</button>
</form>
```

### Passo 6: Layouts e Rotas Aninhadas

```svelte
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import type { LayoutData } from './$types';
  export let data: LayoutData;
</script>

<nav>
  <a href="/">Home</a>
  <a href="/blog">Blog</a>
  {#if data.user}
    <a href="/dashboard">Dashboard</a>
  {/if}
</nav>

<slot />  <!-- página filha renderiza aqui -->
```

```typescript
// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  return { user: locals.user ?? null };
};
```

### Passo 7: Modos de Renderização

Controle renderização por rota com opções de página:

```typescript
// src/routes/docs/+page.ts
export const prerender = true;   // Estática — gerada em tempo de build
export const ssr = true;         // Padrão — renderizada no servidor por requisição
export const csr = false;        // Desabilite hidratação no lado do cliente inteiramente
```

## Exemplos

### Exemplo 1: Rota de Dashboard Protegida

```typescript
// src/routes/dashboard/+layout.server.ts
import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  if (!locals.user) {
    redirect(303, '/login');
  }
  return { user: locals.user };
};
```

### Exemplo 2: Hooks — Middleware de Sessão

```typescript
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';
import { verifyToken } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get('session');
  if (token) {
    event.locals.user = await verifyToken(token);
  }
  return resolve(event);
};
```

### Exemplo 3: Pré-carregamento e Invalidação

```svelte
<script lang="ts">
  import { invalidateAll } from '$app/navigation';

  async function refresh() {
    await invalidateAll(); // re-executa todas as funções load da página
  }
</script>

<button on:click={refresh}>Refresh</button>
```

## Melhores Práticas

- ✅ Use `+page.server.ts` para lógica de banco de dados/autenticação — nunca é enviada ao cliente
- ✅ Use `$lib/server/` para módulos compartilhados exclusivos do servidor (cliente de BD, helpers de auth)
- ✅ Use ações de formulário para mutações em vez de `fetch` no lado do cliente — funciona sem JS
- ✅ Digite todos os valores de retorno de `load` com `$types` gerados (`PageData`, `LayoutData`)
- ✅ Use `event.locals` em hooks para passar contexto do lado do servidor para funções load
- ❌ Não importe código exclusivo do servidor em `+page.svelte` ou `+layout.svelte` diretamente
- ❌ Não armazene estado sensível em stores — use `locals` no servidor
- ❌ Não pule `use:enhance` em formulários — sem ele, os formulários perdem aprimoramento progressivo

## Notas de Segurança e Segurança

- Todo código em `+page.server.ts`, `+server.ts` e `$lib/server/` executa exclusivamente no servidor — seguro para queries de BD, secrets e validação de sessão.
- Sempre valide e sanitize dados de formulário antes de writes de banco de dados.
- Use `error(403)` ou `redirect(303)` de `@sveltejs/kit` em vez de retornar objetos de erro brutos.
- Defina `httpOnly: true` e `secure: true` em todos os cookies de autenticação.
- A proteção CSRF é integrada para ações de formulário — não desabilite `checkOrigin` em produção.

## Armadilhas Comuns

- **Problema:** `Cannot use import statement in a module` em `+page.server.ts`
  **Solução:** O arquivo deve ser `.ts` ou `.js`, não `.svelte`. Arquivos de servidor e componentes Svelte são separados.

- **Problema:** Valor de store é `undefined` na primeira renderização SSR
  **Solução:** Popule a store a partir do valor retornado pela função `load` (prop `data`), não de `onMount` no lado do cliente.

- **Problema:** Ação de formulário não redireciona após envio
  **Solução:** Use `redirect(303, '/path')` de `@sveltejs/kit`, não um `return` simples. 303 é necessário para redirecionamentos POST.

- **Problema:** `locals.user` é undefined dentro de uma função load de `+page.server.ts`
  **Solução:** Defina `event.locals.user` em `src/hooks.server.ts` antes da chamada `resolve()`.

## Skills Relacionadas

- `@nextjs-app-router-patterns` — Quando você prefere React ao Svelte para SSR/SSG
- `@trpc-fullstack` — Adicione type safety de ponta a ponta às rotas de API do SvelteKit
- `@auth-implementation-patterns` — Padrões de autenticação utilizáveis com hooks do SvelteKit
- `@tailwind-patterns` — Estilize aplicações SvelteKit com Tailwind CSS