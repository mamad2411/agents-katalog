---
name: fullstack-app-generator
description: Generate complete, production-ready full-stack applications from a single prompt. Scaffolds projects with the right framework, database schema, API layer, frontend components, authentication, and deployment config. Covers Vite + React, Next.js, Express + React, static sites, and monorepo setups. Use when building a new application from scratch or scaffolding a major feature.
---

# Full-Stack Application Generator

## Framework Selection Matrix

| Requirement | Recommended Stack |
|-------------|-------------------|
| Static site / landing page | Vite + React (or plain HTML/CSS/JS) |
| SaaS with auth + dashboard | Next.js + Prisma + NextAuth |
| API-only backend | Express/Fastify + Prisma |
| Real-time app (chat, collab) | Next.js + WebSocket + Redis |
| Mobile + Web | Next.js (web) + React Native (mobile) |
| CLI tool | Node.js + Commander/Yargs |
| Prototyping | Vite + React + JSON file/SQLite |

## Application Architecture Blueprint

### Full-Stack App (Next.js)
```
project/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout (fonts, providers)
│   │   ├── page.tsx            # Home page
│   │   ├── globals.css         # Design system
│   │   ├── (auth)/             # Auth routes
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── dashboard/          # Protected routes
│   │   │   ├── layout.tsx      # Dashboard shell
│   │   │   └── page.tsx
│   │   └── api/                # API routes (webhooks only)
│   │       └── webhooks/route.ts
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── layout/             # Header, Sidebar, Footer
│   │   └── features/           # Feature-specific components
│   ├── lib/
│   │   ├── db.ts               # Prisma client singleton
│   │   ├── auth.ts             # Auth helpers
│   │   └── utils.ts            # cn() and shared utils
│   ├── actions/                # Server Actions
│   │   ├── auth.ts
│   │   └── [feature].ts
│   └── types/                  # Shared type definitions
│       └── index.ts
├── prisma/
│   └── schema.prisma           # Database schema
├── public/                     # Static assets
├── .env.example
├── .env.local
├── package.json
├── tsconfig.json
├── next.config.ts
└── README.md
```

### API Backend (Express)
```
project/
├── src/
│   ├── routes/                 # Route handlers
│   ├── middleware/              # Auth, validation, errors
│   ├── services/               # Business logic
│   ├── repositories/           # Data access
│   ├── models/                 # Types and schemas
│   ├── lib/                    # Config, clients, utils
│   ├── jobs/                   # Background processors
│   └── index.ts                # Server bootstrap
├── prisma/
│   └── schema.prisma
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── package.json
```

## Generation Workflow

### Step 1: Analyze Requirements
```
Parse user prompt to determine:
- What type of app (SaaS, blog, e-commerce, dashboard, API)
- What data models are needed
- What user flows exist
- What authentication is required
- What third-party integrations are needed
```

### Step 2: Scaffold Foundation
```
1. Initialize project with framework CLI
2. Install core dependencies
3. Set up TypeScript configuration
4. Create design system (globals.css with tokens)
5. Set up database schema
6. Configure environment variables
```

### Step 3: Build Data Layer
```
1. Design Prisma schema with all models and relations
2. Generate initial migration
3. Create database client singleton
4. Implement repository functions for each model
```

### Step 4: Build API / Server Actions
```
1. Create Zod schemas for all inputs
2. Implement server actions or API routes
3. Add validation middleware
4. Add error handling
5. Add authentication checks
```

### Step 5: Build UI
```
1. Create root layout with fonts, theme, metadata
2. Build reusable components (Header, Sidebar, Footer)
3. Create page layouts for each route
4. Implement forms with validation
5. Add loading and error states
6. Polish with animations and micro-interactions
```

### Step 6: Finalize
```
1. Add SEO metadata to all pages
2. Create .env.example with all required variables
3. Add README with setup instructions
4. Create Dockerfile if deployment target needs it
5. Test complete user flow
```

## Auth Pattern (NextAuth.js)
```ts
import NextAuth from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import Credentials from "next-auth/providers/credentials";
import { prisma } from "@/lib/db";
import bcrypt from "bcrypt";

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GitHub({ clientId: process.env.GITHUB_ID!, clientSecret: process.env.GITHUB_SECRET! }),
    Google({ clientId: process.env.GOOGLE_ID!, clientSecret: process.env.GOOGLE_SECRET! }),
    Credentials({
      async authorize(credentials) {
        const user = await prisma.user.findUnique({ where: { email: credentials.email as string } });
        if (!user?.passwordHash) return null;
        const valid = await bcrypt.compare(credentials.password as string, user.passwordHash);
        return valid ? user : null;
      },
    }),
  ],
  session: { strategy: "jwt" },
  pages: { signIn: "/login", error: "/login" },
});
```

## Quality Checklist
- [ ] All pages have proper metadata and SEO
- [ ] Authentication protects all required routes
- [ ] All forms have client-side and server-side validation
- [ ] Error boundaries on all dynamic content
- [ ] Loading states for all async operations
- [ ] Responsive design tested at mobile/tablet/desktop
- [ ] Dark mode support
- [ ] Accessible (keyboard nav, screen reader, contrast)
- [ ] .env.example documents ALL required env vars
- [ ] README has complete setup instructions
