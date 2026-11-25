---
name: sky-astro
description: >-
  Astro ile içerik odaklı siteler: adalar (islands) mimarisi ve client: yönergeleri, content
  collections (tip güvenli Markdown/MDX, Zod şemaları, loader'lar), statik/SSR/hibrit render,
  server islands, Actions, View Transitions, entegrasyonlar (React/Vue/Svelte, Tailwind, MDX,
  sitemap), görsel optimizasyonu, i18n routing, Starlight doküman sitesi ve dağıtım. Blog,
  portfolyo, doküman, pazarlama sitesi veya Astro projesinde kullan.
disable-model-invocation: true
---

# Sky · Astro

## Ne zaman Astro?

İçerik ağırlıklı (blog, doküman, pazarlama, portfolyo, kurumsal site) — varsayılan **sıfır JS**, Lighthouse 100'e yakın.
Uygulama ağırlıklı (panel, gerçek zamanlı) → Next/SvelteKit.

## Adalar

```astro
---
import Hero from "../components/Hero.astro";          // sunucuda render, JS yok
import BookingWidget from "../components/BookingWidget.tsx";
import Reviews from "../components/Reviews.svelte";
---
<Hero />
<BookingWidget client:visible orgSlug="acme" />       <!-- görününce hidrate -->
<Reviews client:idle />                               <!-- tarayıcı boşta kalınca -->
```
`client:load` (hemen), `client:idle`, `client:visible`, `client:media`, `client:only="react"` — en geç olanı seç.
Farklı framework bileşenleri aynı sayfada yaşar.

## Content collections

```ts
// src/content.config.ts
const blog = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/blog" }),
  schema: ({ image }) => z.object({ title: z.string().max(70), description: z.string().max(160), date: z.coerce.date(),
    cover: image(), draft: z.boolean().default(false), tags: z.array(z.string()).default([]) }),
});
export const collections = { blog };
```
`getCollection("blog", ({ data }) => !data.draft)`, `render(entry)`; frontmatter hatası build'de yakalanır. Uzak içerik (CMS, API) için özel loader.

## Render ve sunucu

- Varsayılan statik; `output: "server"` veya sayfa bazında `export const prerender = false` → SSR (adaptör: Vercel/Node/Cloudflare/Netlify).
- **Server islands** (`server:defer`): statik sayfada kişisel parça (sepet, kullanıcı adı) ayrı yüklenir.
- **Actions** (`astro:actions`): tip güvenli sunucu fonksiyonları + Zod doğrulama (formlar).
- Middleware (`src/middleware.ts`) ile oturum.

## Diğer

- `<Image />` / `<Picture />` (`astro:assets`) otomatik boyut/format; `<ClientRouter />` ile View Transitions.
- i18n routing (`i18n: { locales: ["tr", "en"], defaultLocale: "tr" }`) — bkz. `sky-i18n`.
- Entegrasyonlar: `@astrojs/mdx`, `@astrojs/sitemap`, `@astrojs/react`; Tailwind v4 Vite eklentisiyle.
- Doküman sitesi: **Starlight** (bkz. `sky-docs-site`). RSS: `@astrojs/rss`.
