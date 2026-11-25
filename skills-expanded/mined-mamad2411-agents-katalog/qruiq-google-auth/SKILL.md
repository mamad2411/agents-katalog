---
name: qruiq-google-auth
description: |
  Add Google OAuth login to a Next.js app using NextAuth.js v4 + PrismaAdapter + JWT sessions.
  Use when asked to "add Google login", "add auth", "add authentication", or "setup NextAuth".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# qruiq-google-auth

> NextAuth.js v4 + PrismaAdapter + Google OAuth + JWT Session + route protection middleware.

## Parameters

Collect before execution:

| Parameter | Required | Description | Example |
|---|---|---|---|
| `GOOGLE_CLIENT_ID` | Yes | Google OAuth Client ID | `xxx.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Yes | Google OAuth Client Secret | `GOCSPX-xxx` |
| `DATABASE_URL` | Yes | Prisma database connection string | `mysql://user:pass@host:3306/db` |
| `NEXTAUTH_URL` | Yes | App external URL (with scheme) | `https://my-app.qruiq.app` |

> `NEXTAUTH_SECRET` is auto-generated during setup.

## Steps

**Execute all steps directly. Do not list as TODOs.**

### 1. Install dependencies

```bash
yarn add next-auth @auth/prisma-adapter @prisma/client
yarn add -D prisma
```

### 2. Copy template files

```bash
cp -r ~/.qruiq/skills/skills/qruiq-google-auth/template/app/api/auth app/api/
cp -r ~/.qruiq/skills/skills/qruiq-google-auth/template/app/api/health app/api/
cp ~/.qruiq/skills/skills/qruiq-google-auth/template/middleware.ts .
```

### 3. Initialize Prisma

```bash
npx prisma init
```

Edit `prisma/schema.prisma` — add the four NextAuth tables (Account, Session, User, VerificationToken). See "Prisma Schema" section below.

```bash
npx prisma db push
```

### 4. Create `.env`

```env
NEXTAUTH_SECRET=<run: openssl rand -base64 32>
NEXTAUTH_URL=<NEXTAUTH_URL>
GOOGLE_CLIENT_ID=<GOOGLE_CLIENT_ID>
GOOGLE_CLIENT_SECRET=<GOOGLE_CLIENT_SECRET>
DATABASE_URL=<DATABASE_URL>
```

### 5. Add SessionProvider to `app/providers.tsx`

```tsx
import { SessionProvider } from "next-auth/react";

export function Providers({ children, themeProps, session }) {
  const router = useRouter();
  return (
    <SessionProvider session={session}>
      <HeroUIProvider navigate={router.push}>
        <NextThemesProvider {...themeProps}>{children}</NextThemesProvider>
      </HeroUIProvider>
    </SessionProvider>
  );
}
```

## Core files

### `app/api/auth/[...nextauth]/lib/options.ts`

```typescript
import { PrismaAdapter } from '@auth/prisma-adapter';
import type { NextAuthOptions } from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import prisma from '@/lib/prisma';

export const authOptions: NextAuthOptions = {
  secret: process.env.NEXTAUTH_SECRET,
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID ?? '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? '',
      authorization: {
        params: {
          prompt: 'consent',
          access_type: 'offline',
          response_type: 'code',
          redirect_uri: `${process.env.NEXTAUTH_URL}/api/auth/callback/google`,
        },
      },
      checks: ['state', 'pkce'],
      profile(profile) {
        return {
          id: profile.sub,
          name: profile.name,
          email: profile.email,
          image: profile.picture,
          emailVerified: profile.email_verified,
        };
      },
    }),
  ],
  pages: { signIn: '/', error: '/' },
  session: { strategy: 'jwt', maxAge: 30 * 24 * 60 * 60 },
  callbacks: {
    async jwt({ token, user, account }) {
      if (user) token.sub = user.id;
      if (account) token.provider = account.provider;
      return token;
    },
    async session({ session, token }) {
      if (session.user) session.user.id = token.sub as string;
      return session;
    },
    async redirect({ url, baseUrl }) {
      if (url.startsWith('/')) return new URL(url, baseUrl).toString();
      if (url.startsWith(baseUrl)) return url;
      return baseUrl;
    },
  },
};
```

### `middleware.ts` — Route protection

```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';

const PUBLIC_PATHS = ['/', '/api/auth'];

export async function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;
  if (path.startsWith('/api/auth/callback/')) return NextResponse.next();
  const isPublic = PUBLIC_PATHS.some(p => path === p || path.startsWith(p + '/'));
  if (isPublic || path.startsWith('/api/')) return NextResponse.next();
  const token = await getToken({ req: request, secret: process.env.NEXTAUTH_SECRET });
  if (token) return NextResponse.next();
  const callbackUrl = encodeURIComponent(request.url);
  return NextResponse.redirect(new URL(`/?callbackUrl=${callbackUrl}`, request.url));
}

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*'],
};
```

## Prisma Schema

```prisma
model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?
  user              User    @relation(fields: [userId], references: [id], onDelete: Cascade)
  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model User {
  id            String    @id @default(cuid())
  name          String?
  email         String?   @unique
  emailVerified DateTime?
  image         String?
  accounts      Account[]
  sessions      Session[]
}

model VerificationToken {
  identifier String
  token      String   @unique
  expires    DateTime
  @@unique([identifier, token])
}
```

## Google Cloud Console setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials
2. Create **OAuth 2.0 Client ID** (Web application)
3. **Authorized JavaScript origins**: `http://localhost:3000` + `https://your-domain.com`
4. **Authorized redirect URIs**: `http://localhost:3000/api/auth/callback/google` + `https://your-domain.com/api/auth/callback/google`

## Notes

- `NEXTAUTH_URL` must be injected via K8s Secret when deploying — must match external domain exactly
- Google Console callback URL must exactly match `NEXTAUTH_URL`, otherwise `redirect_uri_mismatch`
- `checks: ['state', 'pkce']` is a security best practice — do not remove
- Multiple domains (dev/prod) each need separate entries in Google Console
