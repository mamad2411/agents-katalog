---
name: photography-website
description: Full project context for a premium photography portfolio website — tech stack, conventions, folder structure, DB schema, API patterns, and hard rules. Load this at the start of every session to avoid re-explanation.
type: skill
triggers:
  - "photography website"
  - "portfolio site"
  - "gallery"
  - "Next.js photography"
  - "Cloudinary"
  - "prisma schema"
---

# Photography Website — Agent Context

> Read this before touching any file. Do not deviate from the stack without explicit instruction.

---

## What This Project Is

A premium photography portfolio website with heavy image/video use, rich animations, and a custom CMS-style backend for managing galleries.

---

## Tech Stack

### Frontend
| Layer | Library | Purpose |
|---|---|---|
| Framework | Next.js 14 (App Router) | Core — SSR, routing, API, image optimization |
| Language | TypeScript | All files use `.ts` / `.tsx` |
| UI | React 18 | All components are React components |
| Styling | Tailwind CSS | Utility-first — no custom CSS unless necessary |
| Components | shadcn/ui + Radix UI | Accessible, unstyled base components |

### Animation & Motion
| Library | Purpose |
|---|---|
| Framer Motion | Page transitions, gallery layout animations |
| GSAP + ScrollTrigger | Cinematic scroll-based reveals |
| Lenis | Smooth scroll physics |
| Three.js / React Three Fiber | WebGL backgrounds or 3D effects if needed |

### Media & Images
| Library | Purpose |
|---|---|
| next/image | Auto WebP, lazy loading, responsive sizes |
| Cloudinary | CDN, on-the-fly transforms, storage |
| yet-another-react-lightbox | Full-screen photo lightbox |
| react-lite-youtube-embed | YouTube facade — loads iframe on click only |
| Swiper.js or Embla Carousel | Touch-friendly photo sliders |

### Forms & Validation
| Library | Purpose |
|---|---|
| React Hook Form | Form state management |
| Zod | Schema validation — shared between frontend and API routes |

### Backend (all inside Next.js — no separate server)
| Layer | Tool | Purpose |
|---|---|---|
| API Routes | Next.js `app/api/*/route.ts` | All custom backend functions |
| tRPC | Optional | End-to-end type safety if needed |
| Auth | NextAuth.js | Admin login, OAuth |
| Email | Resend + React Email | Contact form, inquiry emails |

### Database
| Layer | Tool | Purpose |
|---|---|---|
| ORM | Prisma | Type-safe DB queries in TypeScript |
| Database | Supabase (Postgres) | Hosted DB, auth, storage |
| Alt DB | Neon / PlanetScale | Serverless Postgres/MySQL fallback |
| CMS | Sanity | Structured content — galleries, blog posts |

### Infrastructure
| Tool | Purpose |
|---|---|
| Vercel | Hosting, edge CDN, preview deployments |
| Cloudflare | Global image delivery, DDoS protection |
| ESLint + Prettier | Code quality, consistent formatting |
| Vercel Analytics | Privacy-first traffic stats |

---

## Folder Structure

```
/
├── app/
│   ├── (marketing)/
│   │   ├── page.tsx                  # Homepage
│   │   ├── gallery/page.tsx          # Gallery listing
│   │   ├── gallery/[slug]/           # Individual gallery
│   │   └── contact/page.tsx
│   ├── admin/                        # Protected admin area
│   └── api/
│       ├── photos/upload/route.ts
│       ├── photos/route.ts
│       ├── gallery/route.ts
│       ├── contact/route.ts
│       └── auth/[...nextauth]/route.ts
├── components/
│   ├── ui/                           # shadcn/ui (auto-generated)
│   ├── gallery/
│   ├── layout/                       # Header, Footer, Nav
│   └── animations/                   # Reusable animation wrappers
├── lib/
│   ├── prisma.ts                     # Prisma client singleton
│   ├── cloudinary.ts                 # Cloudinary helpers
│   └── utils.ts
├── prisma/
│   └── schema.prisma
├── public/
├── styles/
│   └── globals.css                   # Tailwind base + CSS variables
├── .env.local                        # Secrets — never commit
├── CLAUDE.md
└── next.config.ts
```

---

## Database Schema

```prisma
model Gallery {
  id          String   @id @default(cuid())
  slug        String   @unique
  title       String
  description String?
  coverImage  String   // Cloudinary public ID
  published   Boolean  @default(false)
  createdAt   DateTime @default(now())
  photos      Photo[]
}

model Photo {
  id        String   @id @default(cuid())
  publicId  String   // Cloudinary public ID
  alt       String?
  order     Int
  gallery   Gallery  @relation(fields: [galleryId], references: [id])
  galleryId String
  createdAt DateTime @default(now())
}

model Message {
  id        String   @id @default(cuid())
  name      String
  email     String
  body      String
  read      Boolean  @default(false)
  createdAt DateTime @default(now())
}
```

---

## Key Conventions

### Components
- **Server Components by default.** Only add `"use client"` when the component needs browser APIs, state, or event handlers.
- Client Components must be leaf nodes — push interactivity down, not up.
- One component per file. File name = component name in kebab-case.
- Props: always define a TypeScript `interface` at the top of the file.

### API Routes (`app/api/*/route.ts`)
- Export named functions only: `GET`, `POST`, `PUT`, `DELETE`.
- Always validate request bodies with Zod before using the data.
- Return typed JSON responses with proper HTTP status codes (400, 401, 404, 500).
- Never return raw DB error messages to the client.
- Never expose secrets — they live in `.env.local` only.

### Database
- Always import from the singleton: `import { db } from '@/lib/prisma'`
- Never write raw SQL unless Prisma cannot handle the query.
- Always `await` every Prisma call.
- Use `select` to fetch only required fields.
- After schema changes: `npx prisma generate` then `npx prisma db push` (dev) or `npx prisma migrate dev` (prod).

### Styling
- Tailwind classes only. No inline styles unless absolutely necessary.
- CSS variables for design tokens go in `globals.css`.
- Dark mode: use `dark:` variants from day one.
- Mobile-first: `sm:` → `md:` → `lg:`.

### Images & Video
- Always use `next/image` — never a raw `<img>` tag.
- Store only the Cloudinary **public ID** in the DB, not the full URL. Generate URLs via `lib/cloudinary.ts`.
- YouTube: use `react-lite-youtube-embed`, store only the video ID. Never embed a raw `<iframe>`.

### TypeScript
- Strict mode on. Never use `any`.
- No `.js` files unless auto-generated by a tool.
- Business logic belongs in `lib/` or API routes — not inside React components.

---

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql://...
DIRECT_URL=postgresql://...

# Auth
NEXTAUTH_SECRET=...
NEXTAUTH_URL=http://localhost:3000

# Cloudinary
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

# Email
RESEND_API_KEY=...

# Sanity (if used)
NEXT_PUBLIC_SANITY_PROJECT_ID=...
NEXT_PUBLIC_SANITY_DATASET=production
SANITY_API_TOKEN=...
```

- `NEXT_PUBLIC_` prefix = safe for the browser.
- No prefix = server-only, never reaches the client.

---

## Reusable Patterns

### Prisma singleton (`lib/prisma.ts`)
```ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = global as unknown as { prisma: PrismaClient }
export const db = globalForPrisma.prisma ?? new PrismaClient()
if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db
```

### Cloudinary URL helper (`lib/cloudinary.ts`)
```ts
import { v2 as cloudinary } from 'cloudinary'

export function getImageUrl(publicId: string, options?: object) {
  return cloudinary.url(publicId, {
    format: 'webp',
    quality: 'auto',
    ...options,
  })
}
```

### API route pattern
```ts
// app/api/gallery/route.ts
import { NextResponse } from 'next/server'
import { db } from '@/lib/prisma'
import { z } from 'zod'

export async function GET() {
  const galleries = await db.gallery.findMany({
    where: { published: true },
    select: { id: true, slug: true, title: true, coverImage: true },
  })
  return NextResponse.json(galleries)
}
```

---

## What NOT To Do

| Rule | Why |
|---|---|
| No separate Express/Fastify/Python backend | Everything lives inside Next.js API routes |
| No `<img>` tags | Use `next/image` for optimization |
| No hardcoded secrets | Use `.env.local` — never commit it |
| No `any` in TypeScript | Strict mode is on — define the type |
| No raw YouTube `<iframe>` | Kills page performance — use `react-lite-youtube-embed` |
| No full Cloudinary URLs in DB | Store public ID only, generate URLs via SDK |
| No new dependencies without checking CLAUDE.md | Stack is locked unless explicitly approved |
| No business logic inside React components | Move it to `lib/` or an API route |

---

## Dev Commands

```bash
npm run dev               # Start dev server — localhost:3000
npm run build             # Production build
npm run lint              # Run ESLint

npx prisma generate       # Regenerate client after schema change
npx prisma db push        # Sync schema to DB (dev)
npx prisma migrate dev    # Create migration (production-ready)
npx prisma studio         # Open DB browser UI
```

---

## MCP Servers Available

| Server | Purpose |
|---|---|
| Gmail | Read/send emails — client inquiries |
| Google Calendar | Read/create events — scheduling shoots |

---

*Last updated: April 2026 — update whenever the stack changes.*
