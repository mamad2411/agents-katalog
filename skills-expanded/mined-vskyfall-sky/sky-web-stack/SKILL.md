---
name: sky-web-stack
description: >-
  Web/fullstack stack seçimi ve frontend mimarisi: React, Next.js (App Router), Vite,
  TypeScript, klasör yapısı, state yönetimi, veri çekme (TanStack Query, Server Components),
  routing ve proje iskeleti. Yeni proje kurulurken, React bileşeni/hook yazılırken veya
  "hangi stack", "proje yapısı", "state nerede tutulmalı" sorularında kullan.
disable-model-invocation: true
---

# Sky · Web Stack

## Stack seçimi (varsayılanlar)

Kullanıcı aksini söylemedikçe veya proje zaten başka bir şey kullanmıyorsa:

| İhtiyaç | Varsayılan | Ne zaman başka |
|---|---|---|
| SEO'lu, sunucu verili site/uygulama | **Next.js (App Router) + TS** | Statik içerik ağırlıklıysa Astro |
| Saf SPA / panel / oyun arayüzü | **Vite + React + TS** | — |
| Stil | **Tailwind CSS v4** + CSS değişkenleri | Proje CSS Modules kullanıyorsa ona uy |
| Bileşen temeli | **shadcn/ui (Radix)** | Özel tasarım sistemi varsa o |
| Sunucu state | **TanStack Query** (SPA) / Server Components (Next) | — |
| İstemci state | `useState` → `useReducer` → **Zustand** | Redux yalnızca mevcutsa |
| Form | **React Hook Form + Zod** | Basit formda native + server action |
| ORM | **Drizzle** veya **Prisma** | Supabase ise supabase-js + RLS |
| Auth | **Auth.js** / **Better Auth** / Supabase Auth / Clerk | — |
| Test | **Vitest + Testing Library**, E2E **Playwright** | — |
| Paket yöneticisi | Projede kilit dosyası ne ise (`pnpm-lock`, `package-lock`, `bun.lock`) | — |

## Klasör yapısı

**Next.js App Router**
```
src/
  app/                 # route'lar; layout.tsx, page.tsx, loading.tsx, error.tsx
    (marketing)/       # route grupları
    api/               # route handler'lar (gerekirse)
  components/
    ui/                # saf, tekrar kullanılabilir (button, input, dialog)
    <feature>/         # özelliğe özgü bileşenler
  lib/                 # db, auth, utils, env doğrulama
  server/              # yalnızca sunucu kodu (actions, services) — "server-only" import et
  styles/globals.css   # token'lar
```

**Vite SPA** — özellik bazlı:
```
src/
  features/<ad>/{components,hooks,api,types.ts}
  components/ui/
  lib/
  routes/
```

Kural: bir dosya iki farklı özellikten import ediliyorsa `components/` veya `lib/`e taşı.

## React kalıpları

- **Bileşen ≤ ~150 satır.** Büyürse alt bileşene veya hook'a böl.
- **State'i türet, kopyalama.** Prop'tan hesaplanabilen değeri state'e koyma; `useMemo` yalnızca
  ölçülmüş maliyet için.
- **`useEffect` son çare.** Veri çekme → Query/Server Component; olay sonucu → event handler;
  türetme → render içinde hesapla. Effect yalnızca dış sistemle senkronizasyon için.
- **Key'ler kararlı ID**, index değil (liste sıralanabiliyor/silinebiliyorsa).
- **Kontrollü vs kontrolsüz** bileşeni karıştırma; `value` + `onChange` ya da `defaultValue`.
- **Composition > prop patlaması:** 6+ boolean prop varsa `children`/slot kalıbına geç.
- **Hata sınırları:** Next'te `error.tsx`, SPA'da route başına `ErrorBoundary`.

## Next.js App Router kuralları

- Varsayılan **Server Component**. `"use client"` yalnızca etkileşim/hook/tarayıcı API'si gereken
  yaprak bileşende; sınırı mümkün olduğunca aşağı it.
- Veri çekmeyi sunucuda yap; istemciye yalnızca gereken alanları serileştirerek geç.
- Mutasyon için **Server Actions** + Zod doğrulama + `revalidatePath/Tag`.
- Her action'da kimlik ve yetki kontrolü — action'lar herkese açık POST uç noktasıdır.
- `loading.tsx` ve `Suspense` ile akış; `generateMetadata` ile SEO.
- Görsel: `next/image` (boyut zorunlu), font: `next/font`.
- Gizli kodu `import "server-only"` ile koru.

## Veri çekme (SPA)

```ts
// features/posts/api.ts
export const postKeys = { all: ["posts"] as const, detail: (id: string) => ["posts", id] as const };
export function usePost(id: string) {
  return useQuery({ queryKey: postKeys.detail(id), queryFn: () => api.get(`/posts/${id}`).then(PostSchema.parse) });
}
```
- Query key fabrikası kullan; mutasyon sonrası `invalidateQueries`.
- Yanıtı Zod ile parse et — backend sözleşmesi bozulursa sınırda patlasın.
- Yükleniyor/hata/boş durumlarını her tüketicide ele al.

## Env doğrulama

```ts
// lib/env.ts
import { z } from "zod";
export const env = z.object({
  DATABASE_URL: z.string().url(),
  AUTH_SECRET: z.string().min(32),
}).parse(process.env);
```
Uygulama eksik env ile açılmasın; `.env.example` güncel tutulsun.

## Proje başlangıç kontrol listesi

- [ ] TS `strict`, path alias (`@/`)
- [ ] ESLint + Prettier (veya Biome), `typecheck` / `lint` / `test` scriptleri
- [ ] `globals.css` içinde token'lar + dark mode (bkz. `sky-ui-craft`)
- [ ] `lib/env.ts`, `.env.example`, `.gitignore` içinde `.env*`
- [ ] Temel layout: header, main landmark, footer, skip-link
- [ ] Hata ve 404 sayfaları
- [ ] Bir smoke testi (Vitest) + bir E2E akışı (Playwright)
