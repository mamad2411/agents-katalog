---
name: hono
description: "Construa APIs web ultra-rápidas e aplicativos full-stack com Hono — funciona em Cloudflare Workers, Deno, Bun, Node.js e qualquer runtime compatível com WinterCG."
category: backend
risk: safe
source: community
date_added: "2026-03-18"
author: suhaibjanjua
tags: [hono, edge, cloudflare-workers, bun, deno, api, typescript, web-standards]
tools: [claude, cursor, gemini]
---

# Framework Web Hono

## Visão Geral

Hono (炎, "chama" em japonês) é um framework web pequeno e ultrarrápido construído sobre Web Standards (`Request`/`Response`/`fetch`). Funciona em qualquer lugar: Cloudflare Workers, Deno Deploy, Bun, Node.js, AWS Lambda e qualquer runtime compatível com WinterCG — com o mesmo código. O roteador do Hono é um dos mais rápidos disponíveis, e seu sistema de middleware, suporte JSX nativo e cliente RPC o tornam uma escolha forte para APIs de borda, BFFs e aplicativos full-stack leves.

## Quando Usar Essa Habilidade

- Use ao construir uma API REST ou RPC para deploy em borda (Cloudflare Workers, Deno Deploy)
- Use quando você precisa de um framework de servidor minimalista mas type-safe para Bun ou Node.js
- Use ao construir uma camada Backend for Frontend (BFF) com requisitos de baixa latência
- Use ao migrar do Express mas querendo melhor suporte TypeScript e compatibilidade com borda
- Use quando o usuário pergunta sobre roteamento Hono, middleware, `c.req`, `c.json`, ou cliente RPC `hc()`

## Como Funciona

### Passo 1: Configuração do Projeto

**Cloudflare Workers (recomendado para borda):**
```bash
npm create hono@latest my-api
# Selecione: cloudflare-workers
cd my-api
npm install
npm run dev    # Wrangler local dev
npm run deploy # Deploy para Cloudflare
```

**Bun / Node.js:**
```bash
mkdir my-api && cd my-api
bun init
bun add hono
```

```typescript
// src/index.ts (Bun)
import { Hono } from 'hono';

const app = new Hono();

app.get('/', c => c.text('Hello Hono!'));

export default {
  port: 3000,
  fetch: app.fetch,
};
```

### Passo 2: Roteamento

```typescript
import { Hono } from 'hono';

const app = new Hono();

// Métodos básicos
app.get('/posts', c => c.json({ posts: [] }));
app.post('/posts', c => c.json({ created: true }, 201));
app.put('/posts/:id', c => c.json({ updated: true }));
app.delete('/posts/:id', c => c.json({ deleted: true }));

// Parâmetros de rota e query strings
app.get('/posts/:id', async c => {
  const id = c.req.param('id');
  const format = c.req.query('format') ?? 'json';
  return c.json({ id, format });
});

// Wildcard
app.get('/static/*', c => c.text('static file'));

export default app;
```

**Roteamento encadeado:**
```typescript
app
  .get('/users', listUsers)
  .post('/users', createUser)
  .get('/users/:id', getUser)
  .patch('/users/:id', updateUser)
  .delete('/users/:id', deleteUser);
```

### Passo 3: Middleware

O middleware Hono funciona exatamente como interceptadores `fetch` — handlers antes e depois:

```typescript
import { Hono } from 'hono';
import { logger } from 'hono/logger';
import { cors } from 'hono/cors';
import { bearerAuth } from 'hono/bearer-auth';

const app = new Hono();

// Middleware nativo
app.use('*', logger());
app.use('/api/*', cors({ origin: 'https://myapp.com' }));
app.use('/api/admin/*', bearerAuth({ token: process.env.API_TOKEN! }));

// Middleware customizado
app.use('*', async (c, next) => {
  c.set('requestId', crypto.randomUUID());
  await next();
  c.header('X-Request-Id', c.get('requestId'));
});
```

**Middleware nativo disponível:** `logger`, `cors`, `csrf`, `etag`, `cache`, `basicAuth`, `bearerAuth`, `jwt`, `compress`, `bodyLimit`, `timeout`, `prettyJSON`, `secureHeaders`.

### Passo 4: Helpers de Request e Response

```typescript
app.post('/submit', async c => {
  // Parse body
  const body = await c.req.json<{ name: string; email: string }>();
  const form = await c.req.formData();
  const text = await c.req.text();

  // Headers e cookies
  const auth = c.req.header('authorization');
  const token = getCookie(c, 'session');

  // Responses
  return c.json({ ok: true });                        // JSON
  return c.text('hello');                             // texto simples
  return c.html('<h1>Hello</h1>');                    // HTML
  return c.redirect('/dashboard', 302);              // redirecionamento
  return new Response(stream, { status: 200 });       // Response raw
});
```

### Passo 5: Middleware Validador Zod

```typescript
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  body: z.string().min(1),
  tags: z.array(z.string()).default([]),
});

app.post(
  '/posts',
  zValidator('json', createPostSchema),
  async c => {
    const data = c.req.valid('json'); // totalmente tipado
    const post = await db.post.create({ data });
    return c.json(post, 201);
  }
);
```

### Passo 6: Grupos de Rotas e Composição de Apps

```typescript
// src/routes/posts.ts
import { Hono } from 'hono';

const posts = new Hono();

posts.get('/', async c => { /* listar posts */ });
posts.post('/', async c => { /* criar post */ });
posts.get('/:id', async c => { /* obter post */ });

export default posts;
```

```typescript
// src/index.ts
import { Hono } from 'hono';
import posts from './routes/posts';
import users from './routes/users';

const app = new Hono().basePath('/api');

app.route('/posts', posts);
app.route('/users', users);

export default app;
```

### Passo 7: Cliente RPC (Segurança de Tipo End-to-End)

O modo RPC do Hono exporta tipos de rota que o cliente `hc` consome — similar ao tRPC mas usando convenções fetch:

```typescript
// servidor: src/routes/posts.ts
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const posts = new Hono()
  .get('/', c => c.json({ posts: [{ id: '1', title: 'Hello' }] }))
  .post(
    '/',
    zValidator('json', z.object({ title: z.string() })),
    async c => {
      const { title } = c.req.valid('json');
      return c.json({ id: '2', title }, 201);
    }
  );

export default posts;
export type PostsType = typeof posts;
```

```typescript
// cliente: src/client.ts
import { hc } from 'hono/client';
import type { PostsType } from '../server/routes/posts';

const client = hc<PostsType>('/api/posts');

// Totalmente tipado — autocompletar em rotas, parâmetros e respostas
const { posts } = await client.$get().json();
const newPost = await client.$post({ json: { title: 'New Post' } }).json();
```

## Exemplos

### Exemplo 1: Middleware de Autenticação JWT

```typescript
import { Hono } from 'hono';
import { jwt, sign } from 'hono/jwt';

const app = new Hono();
const SECRET = process.env.JWT_SECRET!;

app.post('/login', async c => {
  const { email, password } = await c.req.json();
  const user = await validateUser(email, password);
  if (!user) return c.json({ error: 'Invalid credentials' }, 401);

  const token = await sign({ sub: user.id, exp: Math.floor(Date.now() / 1000) + 3600 }, SECRET);
  return c.json({ token });
});

app.use('/api/*', jwt({ secret: SECRET }));
app.get('/api/me', async c => {
  const payload = c.get('jwtPayload');
  const user = await getUserById(payload.sub);
  return c.json(user);
});

export default app;
```

### Exemplo 2: Cloudflare Workers com Database D1

```typescript
// src/index.ts
import { Hono } from 'hono';

type Bindings = {
  DB: D1Database;
  API_TOKEN: string;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get('/users', async c => {
  const { results } = await c.env.DB.prepare('SELECT * FROM users LIMIT 50').all();
  return c.json(results);
});

app.post('/users', async c => {
  const { name, email } = await c.req.json();
  await c.env.DB.prepare('INSERT INTO users (name, email) VALUES (?, ?)')
    .bind(name, email)
    .run();
  return c.json({ created: true }, 201);
});

export default app;
```

### Exemplo 3: Resposta em Streaming

```typescript
import { stream, streamText } from 'hono/streaming';

app.get('/stream', c =>
  streamText(c, async stream => {
    for (const chunk of ['Hello', ' ', 'World']) {
      await stream.write(chunk);
      await stream.sleep(100);
    }
  })
);
```

## Boas Práticas

- ✅ Use grupos de rotas (sub-apps) para manter handlers em arquivos separados — `app.route('/users', usersRouter)`
- ✅ Use `zValidator` para toda validação de corpo da requisição, query e parâmetros
- ✅ Digite bindings do Cloudflare Workers com o genérico `Bindings`: `new Hono<{ Bindings: Env }>()`
- ✅ Use o cliente RPC (`hc`) quando seu frontend e backend compartilham o mesmo repositório
- ✅ Prefira retornar `c.json()`/`c.text()` em vez de `new Response()` para código mais limpo
- ❌ Não use APIs específicas do Node.js (`fs`, `path`, `process`) se você quer portabilidade de borda
- ❌ Não adicione dependências pesadas — o valor do Hono é seu footprint minúsculo em runtimes de borda
- ❌ Não pule a tipagem de middleware — use genéricos (`Variables`, `Bindings`) para manter `c.get()` type-safe

## Notas de Segurança e Segurança

- Sempre valide entrada com `zValidator` antes de usar dados de requisições.
- Use o middleware `csrf` nativo do Hono em endpoints de mutação ao servir HTML/formulários.
- Para Cloudflare Workers, armazene segredos em `[vars]` em `wrangler.toml` (não-secreto) ou `wrangler secret put` (secreto) — nunca os coloque no código-fonte.
- Ao usar `bearerAuth` ou `jwt`, garanta que tokens sejam validados do lado servidor — não confie em IDs de usuário fornecidos pelo cliente.
- Rate-limit endpoints sensíveis (autenticação, reset de senha) com Cloudflare Rate Limiting ou middleware customizado.

## Armadilhas Comuns

- **Problema:** Handler retorna `undefined` — resposta fica vazia
  **Solução:** Sempre `return` uma response de handlers: `return c.json(...)` não apenas `c.json(...)`.

- **Problema:** Middleware executa depois que a resposta é enviada
  **Solução:** Chame `await next()` antes da lógica pós-resposta; Hono executa código após `next()` conforme a resposta sobe a cadeia.

- **Problema:** `c.env` é undefined no Node.js
  **Solução:** Os bindings `env` do Cloudflare existem apenas em Workers. Use `process.env` no Node.js.

- **Problema:** Rota não bate — retorna 404
  **Solução:** Verifique que `app.route('/prefix', subRouter)` usa o mesmo prefixo que seu cliente chama. Sub-routers **não** devem repetir o prefixo em suas próprias rotas.

## Habilidades Relacionadas

- `@cloudflare-workers-expert` — Mergulho profundo nas especificidades da plataforma Cloudflare Workers
- `@trpc-fullstack` — Abordagem RPC alternativa para aplicativos full-stack TypeScript
- `@zod-validation-expert` — Padrões de esquema Zod detalhados usados com `@hono/zod-validator`
- `@nodejs-backend-patterns` — Quando você precisa de um backend específico do Node.js (não borda)