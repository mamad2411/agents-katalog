---
name: sky-upgrades
description: >-
  Sürüm yükseltme ve göç rehberi: Next.js sürüm yükseltmeleri (Pages → App Router dahil),
  React 18 → 19, CRA → Vite, JavaScript → TypeScript, Tailwind v3 → v4, ESLint flat config,
  Prisma ↔ Drizzle, Node sürüm yükseltme, resmi codemod'lar, adım adım göç planı, kırılma
  noktaları ve doğrulama. "Next'i güncelle", "Tailwind 4'e geç", "TypeScript'e çevir",
  "eski proje", "upgrade" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Yükseltmeler & Göçler

## Genel yöntem

1. **Sürüm notlarını oku** (resmi upgrade guide) — güncel bilgi için dokümana bak, ezberden yapma.
2. Temiz başlangıç: testler yeşil, ayrı branch, kilit dosyası commit'li.
3. **Resmi codemod** varsa önce onu çalıştır.
4. Bir seferde bir büyük yükseltme (Next + React + Tailwind aynı PR'da değil).
5. Doğrula: `typecheck`, `lint`, `test`, `build`, E2E, kritik sayfaları tarayıcıda gez, prod build'i dene.
6. Kademeli dağıt (preview → prod), geri alma yolu hazır.

## Next.js

- `npx @next/codemod@latest upgrade latest` — sürüm atlamalarında yaygın değişiklikleri (async `params`/`cookies()`, config adları) dönüştürür.
- Cache varsayılanlarındaki değişikliklere dikkat (fetch'in varsayılan önbelleklenmesi sürümden sürüme değişti — bkz. `sky-nextjs`).
- `middleware.ts` → `proxy.ts` gibi ad değişikliklerini sürüm notundan kontrol et.

## Pages Router → App Router

Kademeli: iki router aynı projede birlikte çalışır.
1. `app/layout.tsx` (kök layout, `_app` + `_document` karşılığı).
2. En basit sayfadan başlayarak tek tek taşı; `getServerSideProps` → Server Component içinde doğrudan veri çekme;
   `getStaticProps` + `revalidate` → `fetch` cache / `revalidate` export; `getStaticPaths` → `generateStaticParams`.
3. `next/router` → `next/navigation` (`useRouter`, `usePathname`, `useSearchParams`).
4. API routes kalabilir (`pages/api`) veya route handler'a taşı.
5. Hook kullanan bileşenlere `"use client"`; sınırı yaprağa it.

## React 18 → 19

`npx codemod@latest react/19/migration-recipe`; kaldırılan API'ler (string ref, `defaultProps` fonksiyon bileşenlerde, legacy context),
`forwardRef` artık gereksiz (`ref` prop), `useFormState` → `useActionState`. Üçüncü parti kütüphanelerin React 19 uyumunu kontrol et.

## CRA → Vite

`vite.config.ts` + `index.html` köke (script etiketiyle), `REACT_APP_*` → `VITE_*` (`import.meta.env`), `public/` aynı,
Jest → Vitest (çoğu test değişmeden çalışır), SVG import'ları için `vite-plugin-svgr`. Build ve dev hızı çarpıcı biçimde artar.

## JS → TS (kademeli)

1. `tsconfig` `allowJs: true`, `checkJs: false`, `strict: true` (yeni dosyalar için).
2. Yapraklardan başla (utils, tipler), dosya dosya `.ts/.tsx`'e çevir.
3. Dış sınırlara Zod şemaları (API, env, form) — tiplerin kaynağı (bkz. `sky-typescript`).
4. `any`leri geçici olarak `// TODO(ts)` ile işaretle, sayısını CI'da takip et ve azalt.

## Tailwind v3 → v4

`npx @tailwindcss/upgrade` — `tailwind.config.js` → CSS `@theme`, `@tailwind` direktifleri → `@import "tailwindcss"`,
bazı yardımcı adları değişti (gölge/yuvarlama ölçekleri, `ring` varsayılanı), PostCSS eklentisi `@tailwindcss/postcss` veya Vite eklentisi.
Token'ları `@theme inline` ile CSS değişkenlerine bağla (bkz. `sky-design-system`). Görsel regresyon testi burada çok işe yarar.

## ESLint flat config

`.eslintrc` → `eslint.config.mjs`; `npx @eslint/migrate-config .eslintrc.json`. Ya da tek araç: **Biome** (lint + format, çok hızlı).

## ORM göçü

Prisma → Drizzle (veya tersi): önce mevcut şemadan introspect (`drizzle-kit pull`), sorguları modül modül taşı, iki ORM bir süre birlikte
yaşayabilir (aynı DB), migration sahipliğini tek araca ver.

## Node

`.nvmrc` / `engines` güncelle, CI ve platform (Vercel ayarları) aynı sürüm, native bağımlılıkları yeniden derle, LTS sürümlerini takip et.
