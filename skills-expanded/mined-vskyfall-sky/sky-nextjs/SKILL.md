---
name: sky-nextjs
description: >-
  Derin Next.js (App Router, 15/16): önbellek katmanları ve revalidation, statik/dinamik
  render, Server/Client Component sınırı ve serileştirme, Server Actions, proxy/middleware,
  route handler, paralel ve kesen (intercepting) route'lar, streaming, metadata, görsel/font,
  dağıtım notları ve sık hatalar. Next.js'e özgü bir soru, "neden yeniden render/fetch oluyor",
  "cache temizlenmiyor", "use client nereye" gibi durumlarda kullan.
disable-model-invocation: true
---

# Sky · Next.js

Genel React ve klasör yapısı için `sky-web-stack`; burada Next.js'in kendine özgü mekanikleri var.

## Render modeli

| Mod | Ne zaman | Tetikleyici |
|---|---|---|
| **Statik** (build'de) | İçerik istekten bağımsız | Varsayılan; `generateStaticParams` ile dinamik segmentler de statik olabilir |
| **Dinamik** (her istekte) | Kullanıcıya/isteğe bağlı içerik | `cookies()`, `headers()`, `searchParams`, `connection()`, `fetch(..., { cache: "no-store" })`, `export const dynamic = "force-dynamic"` |
| **Streaming** | Yavaş parça sayfayı bekletmesin | `loading.tsx` veya `<Suspense>` |
| **ISR** | Statik ama periyodik tazeleme | `export const revalidate = 3600` veya fetch `next: { revalidate }` |

Kural: bir sayfanın **tamamını** dinamik yapma. Kişisel kısmı (`"Merhaba Ayşe"`, sepet) `Suspense`
içinde ayrı bir Server Component'e al; kabuk statik kalsın (Partial Prerendering mantığı).

## Önbellek katmanları (karışıklığın kaynağı)

1. **Request memoization** — aynı render içinde aynı `fetch(url)` bir kez gider. Otomatik.
2. **Data Cache** — `fetch` sonuçları sunucuda kalıcı. Next 15+'ta varsayılan **cache'siz**;
   açmak için `fetch(url, { cache: "force-cache" })` veya `next: { revalidate, tags }`.
3. **Full Route Cache** — statik route'ların HTML/RSC çıktısı. Dinamik API kullanılınca devre dışı.
4. **Router Cache** (istemci) — ziyaret edilen segmentler bellekte; `router.refresh()`,
   `revalidatePath/Tag` sonrası Server Action, veya sayfa yenileme temizler.

Veri değiştiğinde:
```ts
// server action veya route handler içinde
revalidateTag("posts");          // fetch(..., { next: { tags: ["posts"] } }) ile eşleşir
revalidatePath("/blog/[slug]", "page");
```
ORM sorgularını (fetch değil) önbelleklemek için `unstable_cache` ya da Next 16'da
`"use cache"` direktifi + `cacheTag()` / `cacheLife()`.

Debug: `next build` çıktısındaki `○ (Static)` / `ƒ (Dynamic)` işaretlerine bak; beklenmedik `ƒ`
varsa hangi dinamik API'nin tetiklediğini bul.

## Server / Client sınırı

- Dosya varsayılan **Server Component**: doğrudan DB/ORM, `server-only` modüller, sır env'ler.
- `"use client"` bir **sınır** ilan eder: o dosya ve import ettiği her şey istemci bundle'ına girer.
  Sınırı yaprağa it: `<Header>` sunucu, içindeki `<ThemeToggle>` istemci.
- Server → Client prop'ları **serileştirilebilir** olmalı: fonksiyon, Date (string'e çevir), class
  örneği, Map/Set geçmez. Server Action'lar istisna — fonksiyon olarak geçilebilir.
- Client Component içine Server Component'i **children/prop** olarak geçebilirsin; import edemezsin.
- Sunucu kodunun istemciye sızmasını `import "server-only"` ile zorla (build hatası verir).
- Context provider'lar istemci bileşenidir; `layout.tsx` içinde `children`ı sarmala.

## Server Actions

```ts
"use server";
export async function createPost(_prev: ActionState, formData: FormData): Promise<ActionState> {
  const user = await requireUser();                       // kimlik
  const parsed = PostSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { errors: parsed.error.flatten().fieldErrors };
  await db.insert(posts).values({ ...parsed.data, authorId: user.id }); // yetki serviste
  revalidateTag("posts");
  redirect(`/posts/${slug}`);                             // try/catch dışında çağır
}
```
- Her action **herkese açık bir POST uç noktasıdır**: kimlik + yetki + doğrulama zorunlu.
- `redirect()` ve `notFound()` throw ile çalışır; `try/catch` içine alma.
- İstemcide `useActionState` (durum + pending) ve `useFormStatus` (buton) kullan.
- Büyük dosya yüklemelerinde action yerine imzalı URL ile doğrudan depolamaya yükle.

## Proxy / Middleware

Next 16'da dosya adı `proxy.ts` (önceki sürümlerde `middleware.ts`); aynı iş: isteği yönlendir,
rewrite et, başlık ekle, locale tespiti, **kaba** oturum kontrolü (çerez var mı).
- Edge'de çalışır: Node API'leri, ORM, ağır kütüphane yok. Hafif tut (<1ms hedef).
- Gerçek yetki kontrolü **sayfada/action'da** yapılır; proxy yalnızca hızlı yönlendirme içindir.
- `matcher` ile statik dosyaları ve `_next` yollarını dışla.

## Route handler'lar (`app/api/**/route.ts`)

- `GET` dinamik API kullanmazsa statikleşir (sürpriz!). API için `export const dynamic = "force-dynamic"` ya da `request` nesnesini kullan.
- Webhook'larda ham gövde: `await request.text()` ile imzayı doğrula, sonra parse et.
- Sayfadan kendi API'ni `fetch` etmek yerine doğrudan servisi çağır; API dış tüketiciler içindir.

## Route düzenleri

- `(grup)` — URL'ye yansımayan gruplama, ayrı layout'lar (`(marketing)`, `(app)`).
- `[slug]`, `[...rest]`, `[[...opt]]` — dinamik segmentler; `generateStaticParams` ile önceden üret.
- `@slot` paralel route'lar — dashboard'da bağımsız yüklenen paneller; `default.tsx` şart.
- `(.)foto/[id]` kesen route — listeden modal açma, doğrudan URL'de tam sayfa.
- `loading.tsx`, `error.tsx` (`"use client"` olmalı), `not-found.tsx`, `template.tsx` segment başına.
- `error.tsx` layout hatalarını yakalamaz; kök için `global-error.tsx`.

## Metadata, görsel, font

- `export const metadata` statik; `generateMetadata` dinamik (fetch'i sayfa ile paylaşır — memoize).
- `opengraph-image.tsx` ile OG görseli kodla üret; `sitemap.ts`, `robots.ts` dosya tabanlı.
- `next/image`: uzak görseller için `remotePatterns`; `sizes` ver, LCP görseline `priority`.
- `next/font`: layout'ta yükle, CSS değişkenine bağla (`variable: "--font-sans"`), `subsets: ["latin", "latin-ext"]` (Türkçe için).

## Env ve yapılandırma

- `NEXT_PUBLIC_*` **build anında** bundle'a gömülür; değişince yeniden build gerekir. Sır koyma.
- Sunucu env'leri runtime'da okunur; `lib/env.ts` ile doğrula (bkz. `sky-web-stack`).
- `next.config.ts`: `images.remotePatterns`, `redirects()`, `headers()` (güvenlik başlıkları buraya),
  `experimental` bayraklarını gerekçesiz açma.

## Sık hatalar → tanı

| Belirti | Sebep | Çözüm |
|---|---|---|
| Hydration mismatch | `Date.now()`, `Math.random()`, `window`, locale farkı, geçersiz HTML iç içe (`<p><div>`) | Değeri `useEffect`te üret, `suppressHydrationWarning` yalnızca zaman damgası gibi yerlerde |
| "useState only works in a Client Component" | hook sunucu dosyasında | Hook'u kullanan yaprağa `"use client"` |
| Sayfa hep dinamik | `cookies()`/`searchParams` üst layout'ta | Dinamik kısmı `Suspense` altına taşı |
| Veri güncellenmiyor | Data Cache / Router Cache | `revalidateTag` + action; ya da `cache: "no-store"` |
| Env `undefined` | istemcide `NEXT_PUBLIC_` değil, veya dev server yeniden başlatılmadı | Ön ek + restart |
| Prod'da module not found | Edge runtime'da Node modülü | `export const runtime = "nodejs"` veya kütüphaneyi değiştir |
| Bundle büyük | `"use client"` çok üstte, ağır kütüphane istemcide | Sınırı indir, `dynamic(() => import(...))` |

## Doğrulama

- `next build` çıktısını oku: route listesi, statik/dinamik, First Load JS.
- `ANALYZE=true` ile bundle analizi (bkz. `sky-perf`).
- Prod modunda (`next start`) test et; dev modu cache davranışını gizler.
