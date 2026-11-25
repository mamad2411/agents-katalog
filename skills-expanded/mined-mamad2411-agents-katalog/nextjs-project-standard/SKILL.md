---
name: nextjs-project-standard
description: "Estándar para crear apps web nuevas con Next.js 16 (App Router, React 19.2), TypeScript estricto, Tailwind v4, Zustand, TanStack Query, react-hook-form + zod y vertical slices. Usar al crear un proyecto Next.js desde cero, al decidir dónde va un archivo o al revisar que un proyecto cumple el estándar antes de entregar."
---

# nextjs-project-standard

Guía para crear apps web nuevas con Next.js. Es la contraparte web de `mobile:expo-project-standard`: mismo stack de estado, formularios y validación, y misma estructura por vertical slices.

> **Proyectos existentes**: si el proyecto ya tiene convenciones (`CLAUDE.md`, estructura, librerías), **síguelas**. Este estándar aplica a proyectos nuevos y a lo que no esté definido. Verifica siempre la versión de `next` en `package.json`; el detalle de caché, `proxy` y `error.tsx` por versión está en `frontend:nextjs-app-router`.

---

## 📁 1. Project Setup

### Tecnologías base

- **Next.js 16** (App Router, Turbopack por defecto) + **React 19.2**
- **TypeScript** con `strict: true`
- **Tailwind CSS v4** (configuración CSS-first con `@theme`) para estilos
- **Zustand** (estado de UI/cliente) + **TanStack Query** (datos remotos en cliente)
- **react-hook-form + zod** para formularios y validación
- **ESLint (flat config) + Prettier** para formato

### Creación del proyecto

```bash
# App Router + TypeScript + Tailwind + ESLint + src/ + alias @/*
npx create-next-app@latest my-app --ts --tailwind --eslint --app --src-dir --import-alias "@/*"

cd my-app
npm install zustand @tanstack/react-query react-hook-form @hookform/resolvers zod server-only
npm install clsx tailwind-merge
npm install -D prettier prettier-plugin-tailwindcss
```

Usa el gestor de paquetes que marque el lockfile del equipo (`pnpm`, `npm`, `bun`); no mezcles lockfiles.

### Archivos de configuración mínimos

```
next.config.ts       # typedRoutes, reactCompiler, images.remotePatterns
tsconfig.json        # strict: true, alias @/*
eslint.config.mjs    # eslint-config-next (flat config); en Next 16 se ejecuta con `eslint`, no `next lint`
.prettierrc          # con prettier-plugin-tailwindcss
src/app/globals.css  # @import "tailwindcss" + @theme con los tokens del design system
src/env.ts           # validación de variables de entorno con zod
.env.example         # todas las variables, sin valores reales
```

```ts
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  typedRoutes: true,
  reactCompiler: true,
  images: {
    remotePatterns: [{ protocol: 'https', hostname: 'cdn.example.com' }],
  },
};

export default nextConfig;
```

---

## 🗂️ 2. Folder Structure

Estructura por **vertical slices** (si el proyecto tiene un ADR de arquitectura, ese manda): el routing vive en `src/app/` y cada dominio agrupa todo lo suyo en `src/features/<dominio>/`. Las páginas son delgadas: componen piezas de las features.

```
my-app/
├── src/
│   ├── app/                          # App Router (rutas = carpetas)
│   │   ├── layout.tsx                # Root layout (<html>, <body>, providers, fuentes)
│   │   ├── page.tsx                  # "/"
│   │   ├── globals.css               # Tailwind + tokens
│   │   ├── not-found.tsx             # 404 global
│   │   ├── global-error.tsx          # Errores del root layout
│   │   ├── (marketing)/              # Route group público
│   │   │   └── about/page.tsx
│   │   ├── (app)/                    # Route group autenticado
│   │   │   ├── layout.tsx
│   │   │   ├── loading.tsx
│   │   │   ├── error.tsx
│   │   │   └── users/[id]/page.tsx
│   │   ├── api/                      # Route handlers (solo para consumidores externos / webhooks)
│   │   │   └── webhooks/route.ts
│   │   └── .well-known/              # AASA / assetlinks para deep linking de la app móvil
│   ├── features/                     # Vertical slices por dominio
│   │   └── auth/
│   │       ├── components/           # UI propia del dominio (server y client)
│   │       ├── hooks/                # Hooks cliente (useLoginForm, etc.)
│   │       ├── actions.ts            # Server Actions ('use server')
│   │       ├── queries.ts            # Acceso a datos en servidor (import 'server-only')
│   │       ├── api.ts                # Hooks TanStack Query (solo si hay datos en cliente)
│   │       ├── store.ts              # Estado Zustand del dominio
│   │       ├── schema.ts             # Esquemas zod (compartidos cliente/servidor)
│   │       └── types.ts              # Tipos del dominio
│   ├── components/                   # UI compartida y reutilizable
│   │   └── Button/
│   │       ├── Button.tsx
│   │       └── index.ts
│   ├── lib/                          # Clientes y utilidades (query client, cn, fetcher)
│   ├── hooks/                        # Hooks globales
│   ├── stores/                       # Stores Zustand globales
│   ├── types/                        # Tipos compartidos
│   ├── env.ts                        # Variables de entorno validadas
│   └── proxy.ts                      # Proxy (antes middleware), si hace falta
├── public/                           # Assets estáticos
└── next.config.ts
```

Reglas:

- Una feature **no importa** internals de otra feature; si algo se comparte, sube a `components/`, `lib/` o `types/`.
- `app/` no contiene lógica de negocio: solo routing, layouts, metadata y composición.

---

## 📝 3. Naming Conventions

### Carpetas y archivos

- **Componentes**: PascalCase → `Button`, `UserCard`
- **Hooks**: camelCase con prefijo `use` → `useLoginForm.ts`
- **Segmentos de ruta**: lowercase y kebab-case → `about-us/`, `[id]/`, `(marketing)/`
- **Archivos especiales de Next**: nombre exacto → `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`, `route.ts`
- **Features**: lowercase por dominio → `features/auth/`
- **Server Actions**: verbo + entidad → `createUser`, `updateProfile`

```
✅ Correcto:
- src/components/UserCard/UserCard.tsx
- src/features/auth/hooks/useLoginForm.ts
- src/app/(app)/user-settings/page.tsx

❌ Incorrecto:
- src/components/user-card/user-card.tsx
- src/features/Auth/hooks/LoginForm.ts
- src/app/(app)/UserSettings/Page.tsx
```

---

## 🧩 4. Component Rules

### Estructura

- **Server Components por defecto**; `'use client'` solo en hojas con estado, efectos, eventos o APIs del navegador
- No marques un layout o una página entera como cliente para un solo botón: extrae el botón
- **Separar lógica de UI**: un hook (`useX`) por componente cliente cuando haya lógica
- Mantener componentes pequeños (<150 líneas); preferir **composición** (pasar Server Components como `children` a Client Components)
- Tipar siempre las props con `interface` o `type`; props de Server a Client deben ser serializables

### Patrón recomendado

```tsx
// src/features/users/components/UserCard.tsx (Server Component)
import { getUser } from '../queries';
import { FollowButton } from './FollowButton';

interface UserCardProps {
  userId: string;
}

export async function UserCard({ userId }: UserCardProps) {
  const user = await getUser(userId);

  return (
    <article className="rounded-lg bg-white p-4 shadow">
      <h2 className="text-lg font-semibold">{user.name}</h2>
      <FollowButton userId={user.id} />
    </article>
  );
}
```

```tsx
// src/features/users/components/FollowButton.tsx (Client Component, hoja)
'use client';

import { useFollow } from '../hooks/useFollow';

export function FollowButton({ userId }: { userId: string }) {
  const { follow, isPending } = useFollow(userId);

  return (
    <button type="button" onClick={follow} disabled={isPending} className="mt-2 rounded bg-primary px-3 py-1 text-white">
      Seguir
    </button>
  );
}
```

---

## 🧭 5. Routing, Navigation & SEO

### Routing

- **App Router** como sistema único; no crear `pages/` en proyectos nuevos
- Route groups `(group)/` para layouts distintos sin afectar la URL
- `params` y `searchParams` son **Promises**: siempre `await`; tipar con `PageProps<'/ruta'>`
- Navegar con `<Link>` (prefetch automático) o `useRouter()` en cliente; `redirect()` en servidor
- Habilitar **typed routes** (`typedRoutes: true`)
- `proxy.ts` solo para redirecciones, rewrites o headers; **no** es la única capa de autorización

```tsx
// src/app/(app)/users/[id]/page.tsx
import type { Metadata } from 'next';
import Link from 'next/link';
import { UserCard } from '@/features/users/components/UserCard';

export async function generateMetadata({ params }: PageProps<'/users/[id]'>): Promise<Metadata> {
  const { id } = await params;
  return { title: `Usuario ${id}` };
}

export default async function UserPage({ params }: PageProps<'/users/[id]'>) {
  const { id } = await params;
  return (
    <>
      <UserCard userId={id} />
      <Link href="/users">Volver</Link>
    </>
  );
}
```

### SEO y metadata

- Toda ruta pública con `metadata` o `generateMetadata`; título con `template` en el root layout
- `sitemap.ts`, `robots.ts` y `opengraph-image.tsx` en rutas públicas
- Fuentes con `next/font` en el root layout; imágenes con `next/image`

### Puente web → app (solo si existe app móvil)

Si el producto tiene app móvil, los enlaces web deben poder abrirla o llevar a instalarla (ver `mobile:expo-project-standard`, sección 5). El web es responsable de:

- Servir `/.well-known/apple-app-site-association` (sin extensión, `application/json`) y `/.well-known/assetlinks.json` para Universal Links / App Links
- **Smart app banner** (`itunes.appId` en `metadata`) y un CTA de instalación claro en Android
- Mantener rutas web equivalentes a las de la app (`/profile/123` ↔ `myapp://profile/123`) para que el mismo enlace funcione en ambos lados
- Conservar parámetros de atribución (`utm_*` y los que use el equipo) al redirigir a la tienda o a la app

```ts
// src/app/.well-known/apple-app-site-association/route.ts
export function GET() {
  return Response.json({
    applinks: { details: [{ appIDs: ['<TEAM_ID>.<bundle.id>'], components: [{ '/': '/profile/*' }] }] },
  });
}
```

---

## 📊 6. State & Data Management

### Estrategia

- **Datos del servidor**: leer en Server Components desde `features/<dominio>/queries.ts` (`import 'server-only'`); nunca llamar a tus propios route handlers desde el servidor
- **Mutaciones**: Server Actions en `features/<dominio>/actions.ts` + invalidación de caché (`revalidatePath` / `updateTag` / `revalidateTag`)
- **Datos remotos en cliente** (polling, scroll infinito, datos que cambian con la interacción): TanStack Query
- **Estado global de UI/cliente**: Zustand (consistente con la app móvil)
- **Estado en la URL** (filtros, paginación, tabs): `searchParams`
- **Estado local**: `useState` / `useContext` cuando sea suficiente
- **Evitar**: Redux como default y duplicar en Zustand datos que ya vienen del servidor
- Peticiones independientes en paralelo (`Promise.all`) o streaming con `<Suspense>`; sin cascadas

### Ejemplo

```ts
// src/features/users/queries.ts
import 'server-only';
import { env } from '@/env';
import { userSchema } from './schema';

export async function getUser(id: string) {
  const res = await fetch(`${env.API_URL}/users/${id}`, { headers: { Authorization: `Bearer ${env.API_TOKEN}` } });
  if (!res.ok) throw new Error('No se pudo cargar el usuario');
  return userSchema.parse(await res.json());
}
```

```tsx
// src/features/users/api.ts (cliente)
'use client';

import { useQuery } from '@tanstack/react-query';

export function useUserActivity(userId: string) {
  return useQuery({
    queryKey: ['users', userId, 'activity'],
    queryFn: async () => {
      const res = await fetch(`/api/users/${userId}/activity`);
      if (!res.ok) throw new Error('Error de red');
      return res.json();
    },
  });
}
```

El `QueryClientProvider` va en un componente cliente `src/app/providers.tsx` que envuelve `children` en el root layout.

---

## 📋 7. Forms & Validation

- **react-hook-form** para formularios con interacción rica; `<form action>` + `useActionState` para formularios simples
- **zod** para esquemas en `features/<dominio>/schema.ts`, **compartidos** entre cliente y Server Action
- Validación en cliente para feedback inmediato **y siempre de nuevo en el servidor**
- Cada Server Action: valida con zod, verifica autenticación y autorización, retorna un resultado serializable

```ts
// src/features/auth/schema.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});
export type LoginInput = z.infer<typeof loginSchema>;
```

```ts
// src/features/auth/actions.ts
'use server';

import { loginSchema } from './schema';

export async function login(input: unknown) {
  const parsed = loginSchema.safeParse(input);
  if (!parsed.success) return { ok: false, errors: parsed.error.flatten().fieldErrors } as const;
  // ... autenticar, set cookie httpOnly
  return { ok: true } as const;
}
```

```ts
// src/features/auth/hooks/useLoginForm.ts
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema, type LoginInput } from '../schema';

export function useLoginForm() {
  return useForm<LoginInput>({ resolver: zodResolver(loginSchema) });
}
```

---

## 🎨 8. Styling (Tailwind v4)

- Usar **clases utilitarias** en `className` directamente en los componentes
- Tokens del design system del proyecto definidos en `globals.css` con `@theme`; si hay app móvil, mismos nombres que en NativeWind para mantener paridad web/móvil
- Combinar clases dinámicas con `cn()` (clsx + tailwind-merge)
- **No** mezclar CSS Modules, CSS-in-JS y Tailwind para lo mismo; `style` inline solo para valores realmente dinámicos
- Orden de clases automático con `prettier-plugin-tailwindcss`

```css
/* src/app/globals.css */
@import 'tailwindcss';

@theme {
  --color-primary: <color-primario>;
  --font-sans: var(--font-inter);
}
```

```tsx
import { cn } from '@/lib/cn';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
}

export function Button({ variant = 'primary', className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-lg px-4 py-2 font-medium',
        variant === 'primary' ? 'bg-primary text-white' : 'bg-gray-200 text-gray-900',
        className,
      )}
      {...props}
    />
  );
}
```

---

## ⚠️ 9. Error Handling

- `error.tsx` (Client Component) por segmento relevante; `global-error.tsx` para el root layout
- `notFound()` + `not-found.tsx` para recursos inexistentes
- Server Actions retornan errores esperados como datos (`{ ok: false, errors }`); solo lanzan en errores inesperados
- `redirect()` y `notFound()` **fuera** de `try/catch`
- Mostrar mensajes amigables (no errores crudos ni stack traces); en producción Next oculta el mensaje y expone `digest`
- **Sin `console.error` residual** en el proyecto final

```tsx
// src/app/(app)/error.tsx — Next 16.3+: retry (en versiones previas: reset)
'use client';

export default function Error({ retry }: { error: Error & { digest?: string }; retry: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-20">
      <p className="text-lg font-bold text-red-600">Algo salió mal</p>
      <button type="button" onClick={() => retry()} className="rounded bg-primary px-4 py-2 text-white">
        Reintentar
      </button>
    </div>
  );
}
```

---

## ⚡ 10. Performance Rules

- Mínimo JavaScript en cliente: Server Components por defecto y `'use client'` en hojas
- Aprovechar **React Compiler** (`reactCompiler: true`); evitar `useMemo`/`useCallback` manual innecesario
- Streaming con `loading.tsx` y `<Suspense>` alrededor de lo lento
- Caché explícita según versión (`'use cache'` + `cacheLife` con `cacheComponents`); no usar `force-dynamic` como parche
- Imágenes con `next/image` (dimensiones o `fill` + `sizes`); fuentes con `next/font`
- Carga diferida de componentes pesados con `next/dynamic`
- Scripts de terceros con `next/script` y `strategy` adecuada
- Medir **Core Web Vitals** (LCP, INP, CLS) antes y después de optimizar

---

## 🔒 11. Security Rules

- Secretos solo en servidor, en módulos con `import 'server-only'`; en cliente solo `NEXT_PUBLIC_*`
- Validar variables de entorno con zod en `src/env.ts` (falla el build si faltan)
- Tokens de sesión en **cookies `httpOnly`, `secure`, `sameSite`**; nunca en `localStorage`
- Autorización **dentro** de cada Server Action y route handler, no solo en `proxy.ts` o en el layout
- **Validar siempre** la entrada con `zod` (formularios, params, searchParams, bodies)
- Headers de seguridad (CSP, `X-Frame-Options`, `Referrer-Policy`) en `next.config.ts` o `proxy.ts`
- No registrar datos sensibles en logs

```bash
# ✅ Seguro de exponer
NEXT_PUBLIC_API_URL=https://api.example.com

# ❌ Nunca con prefijo NEXT_PUBLIC_ (solo servidor)
API_TOKEN=...
```

---

## 🧱 12. Backend for Frontend & Integraciones

- La lógica de negocio vive en el backend (NestJS/FastAPI); Next actúa como **BFF**: compone, valida y adapta datos para la UI
- Route handlers (`app/api/**/route.ts`) solo para consumidores externos, webhooks o clientes que no pueden usar Server Actions (p. ej. la app móvil)
- Un cliente HTTP por servicio en `src/lib/` con base URL, timeouts y manejo de errores centralizado
- No añadir dependencias sin justificarlo; preferir APIs nativas de la plataforma (`fetch`, `URL`, `Intl`)

---

## 🧪 13. Testing Rules

- **Unit / componentes**: Vitest + React Testing Library (componentes cliente, hooks, schemas, Server Actions)
- **Mock de red**: MSW
- **E2E**: Playwright para flujos críticos y async Server Components
- **QA del puente web → app** (si hay app): probar enlaces, smart banner y redirección a tienda en los navegadores y WebViews in-app desde los que llega el tráfico

Detalle de configuración en `frontend:frontend-testing`.

```tsx
// Button.test.tsx
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renderiza el texto', () => {
    render(<Button>Guardar</Button>);
    expect(screen.getByRole('button', { name: 'Guardar' })).toBeInTheDocument();
  });
});
```

---

## 📈 14. Observability & Analytics

- **Error tracking** con Sentry (con source maps) o la plataforma del equipo; `instrumentation.ts` para inicializar en servidor
- **Web Vitals** reportados (`useReportWebVitals` o la integración del proveedor)
- Registrar **atribución de origen** (`utm_*`, referrer, campaña) para medir la adquisición
- Definir eventos de producto clave; no registrar datos sensibles

---

## ♿ 15. Accessibility Rules

- HTML semántico (`button`, `nav`, `main`, `label`) antes que ARIA
- Todo input con `label` asociado; imágenes con `alt` significativo (vacío si es decorativa)
- Navegación completa con teclado y foco visible
- Contraste de color accesible (tokens del design system), mín. WCAG 2.2 AA
- `lang` en `<html>` y títulos de página únicos

---

## 🎨 16. Code Style Rules

- **TypeScript estricto** y componentes funcionales (sin clases)
- Tipar props con `interface` o `type`
- Imports absolutos con alias `@/*`
- Orden de imports: librerías externas → módulos internos (`@/`) → relativos
- Archivos terminan con newline

```tsx
// 1. Externas
import Link from 'next/link';
import { useQuery } from '@tanstack/react-query';

// 2. Internas
import { Button } from '@/components/Button';
import { useLoginForm } from '@/features/auth/hooks/useLoginForm';

// 3. Relativas
import { helper } from '../utils/helper';
```

---

## 🚀 17. Build & Deployment

- `next build` debe pasar en CI (detecta errores de prerender y tipos)
- Ambientes `development`, `preview` (una URL por PR) y `production`
- Variables de entorno por ambiente en la plataforma, nunca commiteadas
- Deploy en la plataforma del equipo (plataforma gestionada o contenedor con `output: 'standalone'`; ver `devops:docker`)
- El detalle de integración DevOps (pipelines, secretos de CI, CDN/invalidaciones) queda **por documentar**

```bash
npx tsc --noEmit
npx eslint .
npx vitest run
npx next build
```

---

## 📋 18. Final Checklist

Antes de entregar / publicar:

- [ ] Estructura por vertical slices (`src/app/` + `src/features/`) respetada
- [ ] TypeScript estricto, sin errores (`tsc --noEmit`)
- [ ] Server Components por defecto; `'use client'` solo en hojas
- [ ] Estilos solo con Tailwind (tokens del design system)
- [ ] Rutas tipadas y metadata en todas las rutas públicas
- [ ] AASA / assetlinks servidos y smart banner configurado (si hay app móvil)
- [ ] Datos del servidor en `queries.ts` (`server-only`); estado cliente con Zustand y TanStack Query
- [ ] Server Actions con zod + auth + invalidación de caché
- [ ] Secretos solo en servidor; env validado en `src/env.ts`
- [ ] Manejo de errores (`error.tsx`, `not-found.tsx`) y sin `console.error` residual
- [ ] Accesibilidad básica implementada
- [ ] Tests pasan (`vitest`, `playwright`) y lint limpio (`eslint`)
- [ ] `next build` exitoso
