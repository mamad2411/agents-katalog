---
name: sky-react-router
description: >-
  React Router v7 (Remix'in devamı) framework modu: dosya/konfig tabanlı route'lar, loader ve
  action'lar, tip güvenli route modülleri (typegen), form ve fetcher ile mutasyonlar, iyimser UI,
  hata sınırları, nested layout'lar, SSR/SPA/prerender modları, oturum ve auth, streaming
  (defer/Await), dağıtım ve Remix v2'den geçiş; ayrıca kütüphane modunda (SPA) router kullanımı.
  React Router / Remix projesinde kullan.
disable-model-invocation: true
---

# Sky · React Router (framework modu)

## Route modülü

```tsx
// app/routes/bookings.tsx
import type { Route } from "./+types/bookings";

export async function loader({ request }: Route.LoaderArgs) {
  const user = await requireUser(request);
  return { bookings: await listBookings(user) };
}
export async function action({ request }: Route.ActionArgs) {
  const user = await requireUser(request);
  const form = Object.fromEntries(await request.formData());
  const parsed = CancelSchema.safeParse(form);
  if (!parsed.success) return data({ errors: parsed.error.flatten().fieldErrors }, { status: 422 });
  await cancelBooking(user, parsed.data.id);
  return { ok: true };
}
export default function Bookings({ loaderData }: Route.ComponentProps) {
  const fetcher = useFetcher();
  return loaderData.bookings.map((b) => (
    <fetcher.Form method="post" key={b.id}>
      <input type="hidden" name="id" value={b.id} />
      <button disabled={fetcher.state !== "idle"}>İptal et</button>
    </fetcher.Form>
  ));
}
export function ErrorBoundary({ error }: Route.ErrorBoundaryProps) { return <ErrorState error={error} />; }
```
- Typegen (`react-router typegen`) ile loader/action/params tipleri otomatik.
- Action sonrası loader'lar otomatik yeniden çalışır — elle cache invalidation yok.
- `useFetcher` sayfa geçişi olmadan mutasyon; iyimser UI için `fetcher.formData`'dan bekleyen değeri göster.
- `<Form>` JS'siz de çalışır (ilerlemeli geliştirme).

## Yapı ve render

`app/routes.ts` (konfig) veya `@react-router/fs-routes` (dosya tabanlı), nested layout'lar `<Outlet />`.
`react-router.config.ts`: `ssr: true/false`, `prerender: ["/", "/fiyatlar"]`. Yavaş veri için loader'dan promise dön + `<Suspense><Await>` (streaming).

## Auth ve oturum

`createCookieSessionStorage` (imzalı, HttpOnly çerez), `requireUser` yardımcısı loader/action'larda; yetki her loader/action'da (bkz. `sky-auth`).

## Dağıtım ve geçiş

Node (`@react-router/serve`), Vercel, Cloudflare, Netlify adaptörleri. Remix v2'den geçiş: future bayraklarını aç → `@remix-run/*` importlarını `react-router` ile değiştir (resmi codemod). Kütüphane modu (SPA): `createBrowserRouter` + loader'lar istemcide.
