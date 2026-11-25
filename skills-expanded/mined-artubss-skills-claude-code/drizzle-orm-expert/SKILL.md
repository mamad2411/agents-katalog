---
name: drizzle-orm-expert
description: "Especialista em Drizzle ORM para TypeScript — design de schema, queries relacionais, migrations e integração com bancos de dados serverless. Use ao construir camadas de banco de dados type-safe com Drizzle."
risk: safe
source: community
date_added: "2026-03-04"
---

# Especialista Drizzle ORM

Você é um especialista Drizzle ORM de nível produção. Ajuda desenvolvedores a construir camadas de banco de dados type-safe e performáticas usando Drizzle ORM com TypeScript. Conhece design de schemas, a API de query relacional, migrations com Drizzle Kit e integrações com Next.js, tRPC e bancos de dados serverless (Neon, PlanetScale, Turso, Supabase).

## Quando Usar Esta Habilidade

- Use quando o usuário pede para configurar Drizzle ORM em um projeto novo ou existente
- Use ao projetar schemas de banco de dados com a abordagem TypeScript-first do Drizzle
- Use ao escrever queries relacionais complexas (joins, subqueries, aggregations)
- Use ao configurar ou solucionar problemas com migrations do Drizzle Kit
- Use ao integrar Drizzle com Next.js App Router, tRPC ou Hono
- Use ao otimizar performance do banco de dados (prepared statements, batching, connection pooling)
- Use ao migrar de Prisma, TypeORM ou Knex para Drizzle

## Conceitos Principais

### Por Que Drizzle

Drizzle ORM é um ORM TypeScript-first que gera zero overhead de runtime. Diferente de Prisma (que usa um binário query engine), Drizzle compila para SQL bruto — tornando-o ideal para edge runtimes e serverless. Principais vantagens:

- **API similar a SQL**: Se você conhece SQL, você conhece Drizzle
- **Zero dependências**: Bundle pequeno, funciona em Cloudflare Workers, Vercel Edge, Deno
- **Inferência de tipo completa**: Schema → tipos → queries são todos conectados em tempo de compilação
- **API de Query Relacional**: Similar a Prisma com includes aninhados sem problemas de N+1

## Padrões de Design de Schema

### Definições de Tabelas

```typescript
// db/schema.ts
import { pgTable, text, integer, timestamp, boolean, uuid, pgEnum } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// Enums
export const roleEnum = pgEnum("role", ["admin", "user", "moderator"]);

// Users table
export const users = pgTable("users", {
  id: uuid("id").defaultRandom().primaryKey(),
  email: text("email").notNull().unique(),
  name: text("name").notNull(),
  role: roleEnum("role").default("user").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Posts table with foreign key
export const posts = pgTable("posts", {
  id: uuid("id").defaultRandom().primaryKey(),
  title: text("title").notNull(),
  content: text("content"),
  published: boolean("published").default(false).notNull(),
  authorId: uuid("author_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
```

### Relations

```typescript
// db/relations.ts
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

### Inferência de Tipo

```typescript
// Infira tipos diretamente do seu schema — sem necessidade de arquivos de tipos separados
import type { InferSelectModel, InferInsertModel } from "drizzle-orm";

export type User = InferSelectModel<typeof users>;
export type NewUser = InferInsertModel<typeof users>;
export type Post = InferSelectModel<typeof posts>;
export type NewPost = InferInsertModel<typeof posts>;
```

## Padrões de Query

### Select Queries (API similar a SQL)

```typescript
import { eq, and, like, desc, count, sql } from "drizzle-orm";

// Select básico
const allUsers = await db.select().from(users);

// Filtrado com condições
const admins = await db.select().from(users).where(eq(users.role, "admin"));

// Select parcial (apenas colunas específicas)
const emails = await db.select({ email: users.email }).from(users);

// Query com join
const postsWithAuthors = await db
  .select({
    title: posts.title,
    authorName: users.name,
  })
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id))
  .where(eq(posts.published, true))
  .orderBy(desc(posts.createdAt))
  .limit(10);

// Aggregation
const postCounts = await db
  .select({
    authorId: posts.authorId,
    postCount: count(posts.id),
  })
  .from(posts)
  .groupBy(posts.authorId);
```

### Relational Queries (API similar a Prisma)

```typescript
// Includes aninhados — Drizzle resolve em uma única query
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: {
      where: eq(posts.published, true),
      orderBy: [desc(posts.createdAt)],
      limit: 5,
    },
  },
});

// Encontre um com dados aninhados
const user = await db.query.users.findFirst({
  where: eq(users.id, userId),
  with: { posts: true },
});
```

### Insert, Update, Delete

```typescript
// Insert com returning
const [newUser] = await db
  .insert(users)
  .values({ email: "dev@example.com", name: "Dev" })
  .returning();

// Batch insert
await db.insert(posts).values([
  { title: "Post 1", authorId: newUser.id },
  { title: "Post 2", authorId: newUser.id },
]);

// Update
await db.update(users).set({ name: "Updated" }).where(eq(users.id, userId));

// Delete
await db.delete(posts).where(eq(posts.authorId, userId));
```

### Transactions

```typescript
const result = await db.transaction(async (tx) => {
  const [user] = await tx.insert(users).values({ email, name }).returning();
  await tx.insert(posts).values({ title: "Welcome Post", authorId: user.id });
  return user;
});
```

## Fluxo de Migration (Drizzle Kit)

### Configuração

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### Comandos

```bash
# Gere SQL de migration a partir de alterações no schema
npx drizzle-kit generate

# Faça push do schema diretamente para o banco de dados (desenvolvimento apenas — pula arquivos de migration)
npx drizzle-kit push

# Execute migrations pendentes (produção)
npx drizzle-kit migrate

# Abra Drizzle Studio (navegador de banco de dados GUI)
npx drizzle-kit studio
```

## Configuração de Database Client

### PostgreSQL (Neon Serverless)

```typescript
// db/index.ts
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";
import * as schema from "./schema";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

### SQLite (Turso/LibSQL)

```typescript
import { drizzle } from "drizzle-orm/libsql";
import { createClient } from "@libsql/client";
import * as schema from "./schema";

const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN,
});
export const db = drizzle(client, { schema });
```

### MySQL (PlanetScale)

```typescript
import { drizzle } from "drizzle-orm/planetscale-serverless";
import { Client } from "@planetscale/database";
import * as schema from "./schema";

const client = new Client({ url: process.env.DATABASE_URL! });
export const db = drizzle(client, { schema });
```

## Otimização de Performance

### Prepared Statements

```typescript
// Prepare uma vez, execute muitas vezes
const getUserById = db.query.users
  .findFirst({
    where: eq(users.id, sql.placeholder("id")),
  })
  .prepare("get_user_by_id");

// Execute com parâmetros
const user = await getUserById.execute({ id: "abc-123" });
```

### Batch Operations

```typescript
// Use db.batch() para múltiplas queries independentes em um único round-trip
const [allUsers, recentPosts] = await db.batch([
  db.select().from(users),
  db.select().from(posts).orderBy(desc(posts.createdAt)).limit(10),
]);
```

### Indexing no Schema

```typescript
import { index, uniqueIndex } from "drizzle-orm/pg-core";

export const posts = pgTable(
  "posts",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    title: text("title").notNull(),
    authorId: uuid("author_id").references(() => users.id).notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
  },
  (table) => [
    index("posts_author_idx").on(table.authorId),
    index("posts_created_idx").on(table.createdAt),
  ]
);
```

## Integração Next.js

### Uso em Server Component

```typescript
// app/users/page.tsx (React Server Component)
import { db } from "@/db";
import { users } from "@/db/schema";

export default async function UsersPage() {
  const allUsers = await db.select().from(users);
  return (
    <ul>
      {allUsers.map((u) => (
        <li key={u.id}>{u.name}</li>
      ))}
    </ul>
  );
}
```

### Server Action

```typescript
// app/actions.ts
"use server";
import { db } from "@/db";
import { users } from "@/db/schema";

export async function createUser(formData: FormData) {
  const name = formData.get("name") as string;
  const email = formData.get("email") as string;
  await db.insert(users).values({ name, email });
}
```

## Melhores Práticas

- ✅ **Faça:** Mantenha todas as definições de schema em um único `db/schema.ts` ou divida por domínio (`db/schema/users.ts`, `db/schema/posts.ts`)
- ✅ **Faça:** Use `InferSelectModel` e `InferInsertModel` para type safety em vez de interfaces manuais
- ✅ **Faça:** Use a API de query relacional (`db.query.*`) para dados aninhados a fim de evitar problemas de N+1
- ✅ **Faça:** Use prepared statements para queries executadas frequentemente em produção
- ✅ **Faça:** Use `drizzle-kit generate` + `migrate` em produção (nunca `push`)
- ✅ **Faça:** Passe `{ schema }` para `drizzle()` a fim de habilitar a API de query relacional
- ❌ **Não:** Use `drizzle-kit push` em produção — pode causar perda de dados
- ❌ **Não:** Escreva SQL bruto quando o query builder do Drizzle suporta a operação
- ❌ **Não:** Esqueça de definir `relations()` se quiser usar `db.query.*` com `with`
- ❌ **Não:** Crie uma nova conexão de banco de dados por request em serverless — use connection pooling

## Solução de Problemas

**Problema:** `db.query.tableName` é undefined
**Solução:** Passe todos os objetos de schema (incluindo relations) para `drizzle()`: `drizzle(client, { schema })`

**Problema:** Conflitos de migration após alterações no schema
**Solução:** Execute `npx drizzle-kit generate` para criar uma nova migration, então `npx drizzle-kit migrate`

**Problema:** Erros de tipo em `.returning()` com MySQL
**Solução:** MySQL não suporta `RETURNING`. Use `.execute()` e leia `insertId` do resultado em vez disso.