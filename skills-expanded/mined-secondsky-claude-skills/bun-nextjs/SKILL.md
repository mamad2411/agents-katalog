---
name: bun-nextjs
description: This skill should be used when the user asks about "Next.js with Bun", "Bun and Next", "running Next.js on Bun", "Next.js development with Bun", "create-next-app with Bun", or building Next.js applications using Bun as the runtime.
metadata:
  version: "1.0.0"
license: MIT
---

# Bun Next.js

Run Next.js applications with Bun for faster development and builds.

## Quick Start

```bash
# Create new Next.js project with Bun
bunx create-next-app@latest my-app
cd my-app

# Install dependencies
bun install

# Development
bun run dev

# Build
bun run build

# Production
bun run start
```

## Secure Installation

Scaffolding tools like `bunx create-next-app` download and execute remote code. Multiple install contexts (local, Docker) require pinning versions in both. Before running, follow supply chain security best practices:

- **Block post-install scripts** — Bun disables them by default; allow specific packages via `trustedDependencies` in `package.json`
- **Cooldown period** — Configure `minimumReleaseAge` in `bunfig.toml` to wait 7 days for new versions
- **Audit before installing** — Run `socket package score npm <pkg>` or use `socket npm install <pkg>` to check packages

Load the `dependency-upgrade` skill for full security configuration including Socket CLI integration, cooldown setup, lockfile validation, and CI enforcement.

## Project Setup

### package.json

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint ."
  },
  "dependencies": {
    "next": "^16.2.0",
    "react": "^19.2.0",
    "react-dom": "^19.2.0"
  }
}
```

### Use Bun as Runtime

```json
{
  "scripts": {
    "dev": "bun --bun next dev",
    "build": "bun --bun next build",
    "start": "bun --bun next start"
  }
}
```

The `--bun` flag forces Next.js to use Bun's runtime instead of Node.js.

## Configuration

### next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Turbopack is the default bundler in Next.js 16 (top-level, not under experimental)
  turbopack: {},

  // Server-side Bun APIs
  serverExternalPackages: ["bun:sqlite"],

  // Note: a `webpack` key is no longer supported in Next.js 16 — Turbopack is the
  // default bundler and a `webpack` config will fail `next build`. Bun-specific
  // imports (`bun:sqlite`, `bun:ffi`) are handled via `serverExternalPackages`
  // above. If you truly need the webpack bundler, run `next build --webpack`.
};

module.exports = nextConfig;
```

## Using Bun APIs in Next.js

### Server Components

```typescript
// app/page.tsx (Server Component)
import { Database } from "bun:sqlite";

export default async function Home() {
  const db = new Database("data.sqlite");
  const users = db.query("SELECT * FROM users").all();
  db.close();

  return (
    <div>
      {users.map((user) => (
        <p key={user.id}>{user.name}</p>
      ))}
    </div>
  );
}
```

### API Routes

```typescript
// app/api/users/route.ts
import { Database } from "bun:sqlite";

export async function GET() {
  const db = new Database("data.sqlite");
  const users = db.query("SELECT * FROM users").all();
  db.close();

  return Response.json(users);
}

export async function POST(request: Request) {
  const body = await request.json();

  const db = new Database("data.sqlite");
  db.run("INSERT INTO users (name) VALUES (?)", [body.name]);
  db.close();

  return Response.json({ success: true });
}
```

### File Operations

```typescript
// app/api/files/route.ts
export async function GET() {
  const file = Bun.file("./data/config.json");
  const config = await file.json();

  return Response.json(config);
}

export async function POST(request: Request) {
  const data = await request.json();
  await Bun.write("./data/config.json", JSON.stringify(data, null, 2));

  return Response.json({ saved: true });
}
```

## Server Actions

```typescript
// app/actions.ts
"use server";

import { Database } from "bun:sqlite";
import { revalidatePath } from "next/cache";

export async function createUser(formData: FormData) {
  const name = formData.get("name") as string;

  const db = new Database("data.sqlite");
  db.run("INSERT INTO users (name) VALUES (?)", [name]);
  db.close();

  revalidatePath("/users");
}

export async function deleteUser(id: number) {
  const db = new Database("data.sqlite");
  db.run("DELETE FROM users WHERE id = ?", [id]);
  db.close();

  revalidatePath("/users");
}
```

## Proxy (formerly Middleware)

In Next.js 16, `middleware.ts` is renamed to `proxy.ts` (the `middleware` name still
works but is deprecated). Proxy runs on the Node.js runtime, not the Edge runtime.

> ⚠️ **Deploying to Cloudflare via OpenNext? Keep `middleware.ts`.**
> `@opennextjs/cloudflare` does not yet recognize the `proxy.ts` filename — renaming
> will silently disable your middleware on Cloudflare. Until OpenNext adds support,
> deploy with the classic `middleware.ts` (it still works in Next 16, just deprecated
> upstream). This caveat does not apply to Node.js/Vercel/Bun-native deployments.

```typescript
// proxy.ts (renamed from middleware.ts in Next.js 16)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  // Check auth
  const token = request.cookies.get("token");

  if (!token && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
```

## Environment Variables

```bash
# .env.local
DATABASE_URL=./data.sqlite
API_SECRET=your-secret-key
```

```typescript
// Access in server components/actions
const dbUrl = process.env.DATABASE_URL;
const secret = process.env.API_SECRET;

// Expose to client (prefix with NEXT_PUBLIC_)
// .env.local
NEXT_PUBLIC_API_URL=https://api.example.com
```

## Deployment

### Build for Production

```bash
bun run build
bun run start
```

### Docker

```dockerfile
FROM oven/bun:1

WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build

EXPOSE 3000

CMD ["bun", "run", "start"]
```

### Vercel

```bash
# Install Vercel CLI
bun add -g vercel

# Deploy
vercel
```

Note: Vercel's edge runtime uses V8, not Bun. Bun APIs work in:
- Server Components (Node.js runtime)
- API Routes (Node.js runtime)
- Server Actions (Node.js runtime)

## Performance Tips

1. **Turbopack is the default** in Next.js 16 (no flag needed):
   ```bash
   bun run dev
   ```

2. **Prefer Server Components** - Less JavaScript sent to client

3. **Use Bun SQLite** instead of external databases for simple apps

4. **Enable compression**:
   ```javascript
   // next.config.js
   module.exports = {
     compress: true,
   };
   ```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find bun:sqlite` | Wrong runtime | Use `bun --bun next dev` |
| `Module not found` | Missing dependency | Run `bun install` |
| `Hydration mismatch` | Server/client diff | Check data fetching |
| `Edge runtime error` | Bun API on edge | Use Node.js runtime |

## When to Load References

Load `references/app-router.md` when:
- App Router patterns
- Route groups
- Parallel routes

Load `references/caching.md` when:
- Data caching strategies
- Revalidation patterns
- Static generation
