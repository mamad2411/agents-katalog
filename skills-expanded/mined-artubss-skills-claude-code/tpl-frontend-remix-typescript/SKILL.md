---
name: tpl-frontend-remix-typescript
description: Template do pack (frontend/09-remix-typescript.md). Orienta o agente em interfaces, componentes e apps de frontend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: frontend/09-remix-typescript.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: [Nome do App]

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `frontend/09-remix-typescript.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

> CLAUDE.md — Remix v2 + TypeScript
> Gerado pelo Pack CLAUDE.md Elite

---

## STACK

| Camada | Tecnologia | Versão |
|--------|-----------|--------|
| Framework | Remix | v2.x |
| Linguagem | TypeScript | 5.x (strict) |
| ORM | Prisma | 5.x |
| Banco de Dados | PostgreSQL | 16+ |
| Estilização | Tailwind CSS | v4 |
| Validação | Zod | 3.x |
| Testes | Vitest + Testing Library | latest |
| Runtime | Node.js | 20 LTS |
| Deploy | Fly.io / Railway / Vercel | — |

---

## PROJECT STRUCTURE

```
app/
├── routes/                     # File-based routing (Remix v2)
│   ├── _index.tsx               # / (home)
│   ├── _auth.tsx                # layout route sem caminho
│   ├── _auth.login.tsx          # /login
│   ├── _auth.register.tsx       # /register
│   ├── dashboard.tsx            # /dashboard (layout)
│   ├── dashboard._index.tsx     # /dashboard (index)
│   ├── dashboard.projects.tsx   # /dashboard/projects
│   ├── dashboard.projects.$id.tsx
│   └── api.webhook.ts           # /api/webhook (resource route)
├── components/
│   ├── ui/                      # Componentes primitivos (Button, Input, Modal)
│   └── features/                # Componentes de domínio
├── lib/
│   ├── db.server.ts             # Instância do Prisma (server-only)
│   ├── auth.server.ts           # Sessão e autenticação
│   ├── validations/             # Schemas Zod reutilizáveis
│   └── utils.ts                 # Helpers puros (sem server imports)
├── hooks/                       # Custom React hooks (client)
├── types/                       # TypeScript types/interfaces globais
├── styles/
│   └── tailwind.css
├── entry.client.tsx
├── entry.server.tsx
└── root.tsx
prisma/
├── schema.prisma
└── migrations/
public/
tests/
├── unit/
├── integration/
└── e2e/
```

**Regras de nomenclatura de arquivos:**
- Arquivos `*.server.ts` NUNCA são importados no cliente — Remix tree-shakes automaticamente.
- Layout routes usam `_prefix` no nome do arquivo.
- Resource routes (sem UI) exportam apenas `loader` ou `action`, sem `default`.

---

## MENTAL MODEL — LOADER / ACTION

### Loader (GET — leitura de dados)

```typescript
// app/routes/dashboard.projects.tsx
import { json, type LoaderFunctionArgs } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { requireUser } from "~/lib/auth.server";
import { db } from "~/lib/db.server";

export async function loader({ request }: LoaderFunctionArgs) {
  const user = await requireUser(request); // lança redirect se não autenticado

  const projects = await db.project.findMany({
    where: { userId: user.id },
    orderBy: { createdAt: "desc" },
  });

  return json({ projects, user });
}

export default function ProjectsPage() {
  const { projects } = useLoaderData<typeof loader>();
  return (/* JSX */);
}
```

### Action (POST/PUT/DELETE — mutações)

```typescript
// app/routes/dashboard.projects.tsx
import { redirect, type ActionFunctionArgs } from "@remix-run/node";
import { z } from "zod";

const CreateProjectSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().optional(),
});

export async function action({ request }: ActionFunctionArgs) {
  const user = await requireUser(request);
  const formData = await request.formData();

  const result = CreateProjectSchema.safeParse(Object.fromEntries(formData));
  if (!result.success) {
    return json(
      { errors: result.error.flatten().fieldErrors },
      { status: 400 }
    );
  }

  await db.project.create({
    data: { ...result.data, userId: user.id },
  });

  return redirect("/dashboard/projects");
}
```

### Regras de Loader/Action

1. **Loaders são apenas leitura** — nunca mutam dados.
2. **Actions sempre retornam `json()` com erros OU `redirect()`** — nunca retornam dados de sucesso inline (use redirect + flash message).
3. **Validar TODOS os inputs** com Zod antes de tocar no banco.
4. **`requireUser(request)`** deve ser a primeira chamada em qualquer loader/action protegido.
5. **Nunca usar `throw new Response()`** para erros de negócio — reservar para 404/401/403.

---

## NESTED ROUTING

```
root.tsx                     ← providers, meta global, outlet
  └── _auth.tsx              ← layout: navbar de auth, sem URL própria
        ├── _auth.login.tsx  ← /login
        └── _auth.register.tsx ← /register
  └── dashboard.tsx          ← layout: sidebar, header autenticado
        ├── dashboard._index.tsx   ← /dashboard
        ├── dashboard.projects.tsx ← /dashboard/projects
        └── dashboard.projects.$id.tsx ← /dashboard/projects/:id
```

**Regras de Nested Routing:**
- `<Outlet />` deve aparecer **exatamente uma vez** em cada layout route.
- `useMatches()` para breadcrumbs — não recalcular em cada componente.
- `shouldRevalidate` para evitar re-fetches desnecessários após actions que não afetam o route pai.
- Nunca colocar lógica de negócio em `root.tsx` — apenas providers e ErrorBoundary global.

---

## ERROR BOUNDARIES

```typescript
// Sempre em layout routes críticos
export function ErrorBoundary() {
  const error = useRouteError();

  if (isRouteErrorResponse(error)) {
    return (
      <div>
        <h1>{error.status} {error.statusText}</h1>
        <p>{error.data}</p>
      </div>
    );
  }

  // Erro inesperado
  return (
    <div>
      <h1>Algo deu errado</h1>
      <p>Por favor, recarregue a página.</p>
    </div>
  );
}
```

**Regras:**
- `ErrorBoundary` obrigatório em `root.tsx`.
- `ErrorBoundary` recomendado em qualquer route que faça chamadas externas.
- Nunca expor stack trace em produção — logar no servidor, mostrar mensagem genérica.

---

## AUTENTICAÇÃO

```typescript
// lib/auth.server.ts
import { createCookieSessionStorage, redirect } from "@remix-run/node";

const sessionStorage = createCookieSessionStorage({
  cookie: {
    name: "__session",
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    secrets: [process.env.SESSION_SECRET!],
    maxAge: 60 * 60 * 24 * 30, // 30 dias
  },
});

export async function requireUser(request: Request) {
  const session = await sessionStorage.getSession(request.headers.get("Cookie"));
  const userId = session.get("userId");
  if (!userId) throw redirect("/login");
  const user = await db.user.findUnique({ where: { id: userId } });
  if (!user) throw redirect("/login");
  return user;
}
```

---

## VALIDAÇÃO COM ZOD

```typescript
// lib/validations/project.ts
import { z } from "zod";

export const ProjectSchema = z.object({
  name: z.string().min(1, "Nome obrigatório").max(100, "Máximo 100 caracteres"),
  description: z.string().max(500).optional(),
  status: z.enum(["draft", "active", "archived"]).default("draft"),
});

export type ProjectInput = z.infer<typeof ProjectSchema>;

// Em action:
const result = ProjectSchema.safeParse(Object.fromEntries(formData));
if (!result.success) {
  return json({ errors: result.error.flatten().fieldErrors }, { status: 422 });
}
```

---

## ROUTING TABLE

| Trigger | Método | Route File | Handler | Descrição |
|---------|--------|-----------|---------|-----------|
| Acessa `/` | GET | `_index.tsx` | `loader` | Landing page |
| Acessa `/login` | GET | `_auth.login.tsx` | `loader` | Página de login |
| Submete form login | POST | `_auth.login.tsx` | `action` | Autentica usuário |
| Acessa `/dashboard` | GET | `dashboard._index.tsx` | `loader` | Dashboard home, requer auth |
| Acessa `/dashboard/projects` | GET | `dashboard.projects.tsx` | `loader` | Lista projetos |
| Cria projeto | POST | `dashboard.projects.tsx` | `action` | Cria projeto via form |
| Acessa `/dashboard/projects/:id` | GET | `dashboard.projects.$id.tsx` | `loader` | Detalhes do projeto |
| Edita projeto | POST | `dashboard.projects.$id.tsx` | `action` | Atualiza projeto (method=PUT via hidden input) |
| Deleta projeto | POST | `dashboard.projects.$id.tsx` | `action` | Deleta (method=DELETE via hidden input) |
| Webhook externo | POST | `api.webhook.ts` | `action` | Resource route, sem UI |

---

## FORMULÁRIOS

```tsx
// Sempre usar <Form> do Remix, não <form> nativo
import { Form, useActionData, useNavigation } from "@remix-run/react";

export default function CreateProject() {
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();
  const isSubmitting = navigation.state === "submitting";

  return (
    <Form method="post">
      <input name="name" />
      {actionData?.errors?.name && (
        <p className="text-red-500">{actionData.errors.name[0]}</p>
      )}
      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Salvando..." : "Criar Projeto"}
      </button>
    </Form>
  );
}
```

---

## PRISMA — PADRÕES

```typescript
// lib/db.server.ts — singleton para dev (evita conexões duplicadas no HMR)
import { PrismaClient } from "@prisma/client";

declare global {
  var __db__: PrismaClient | undefined;
}

export const db =
  global.__db__ ||
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["query", "error"] : ["error"],
  });

if (process.env.NODE_ENV !== "production") {
  global.__db__ = db;
}
```

**Regras Prisma:**
- Nunca importar `db` em arquivos sem `.server.ts` no nome.
- Usar `select` explícito — nunca retornar objetos Prisma completos para o cliente.
- Migrations: `npx prisma migrate dev --name <descricao>` sempre com nome descritivo.
- Seeds em `prisma/seed.ts`.

---

## TESTES

```typescript
// tests/unit/validations.test.ts
import { describe, it, expect } from "vitest";
import { ProjectSchema } from "~/lib/validations/project";

describe("ProjectSchema", () => {
  it("aceita input válido", () => {
    const result = ProjectSchema.safeParse({ name: "Meu Projeto" });
    expect(result.success).toBe(true);
  });

  it("rejeita nome vazio", () => {
    const result = ProjectSchema.safeParse({ name: "" });
    expect(result.success).toBe(false);
  });
});
```

```typescript
// tests/integration/loader.test.ts
import { createRequest } from "~/test-utils/request";
import { loader } from "~/routes/dashboard.projects";

describe("ProjectsLoader", () => {
  it("redireciona para /login se não autenticado", async () => {
    const request = createRequest("/dashboard/projects");
    await expect(loader({ request, params: {}, context: {} })).rejects.toThrow();
  });
});
```

---

## QUALITY GATES

Antes de cada commit, verificar:

- [ ] `npx tsc --noEmit` — sem erros TypeScript
- [ ] `npx eslint . --max-warnings 0` — sem warnings
- [ ] `npx vitest run` — todos os testes passando
- [ ] Toda action valida input com Zod antes de tocar no banco
- [ ] Toda route protegida chama `requireUser()` como primeira linha do loader/action
- [ ] Arquivos `.server.ts` não importam de arquivos sem `.server.ts` que importem browser APIs
- [ ] Nenhuma query N+1 — usar `include` ou `select` com relações aninhadas
- [ ] `ErrorBoundary` presente em todos os layout routes
- [ ] Variáveis de ambiente acessadas via `process.env.VAR_NAME!` ou validadas no startup
- [ ] Nenhum `console.log` em produção — usar logger estruturado

---

## FORBIDDEN

```
❌ NUNCA importar "~/lib/db.server" em arquivos sem `.server.ts`
❌ NUNCA usar `<form>` nativo para mutations — usar `<Form>` do Remix
❌ NUNCA colocar lógica de negócio em componentes — mover para loader/action
❌ NUNCA retornar dados sensíveis (senha hash, tokens) via `json()` para o cliente
❌ NUNCA usar `useEffect` para buscar dados — isso é trabalho do loader
❌ NUNCA criar estado local para dados que deveriam estar no servidor
❌ NUNCA chamar `fetch()` no cliente para dados da app — usar loaders
❌ NUNCA usar `any` em TypeScript — sempre tipar explicitamente
❌ NUNCA commit sem rodar os quality gates
❌ NUNCA armazenar SESSION_SECRET hardcoded — apenas via env
```

---

## ENV VARIABLES

```bash
# .env.example
DATABASE_URL="postgresql://user:password@localhost:5432/myapp"
SESSION_SECRET="super-secret-key-min-32-chars"
NODE_ENV="development"
# Adicionar novos vars aqui e atualizar .env.example
```

---

## COMMANDS

```bash
# Dev
npm run dev

# Banco de dados
npx prisma migrate dev --name <nome>
npx prisma studio
npx prisma generate

# Build e typecheck
npm run build
npx tsc --noEmit

# Testes
npx vitest run
npx vitest --ui

# Lint
npx eslint . --fix
```
