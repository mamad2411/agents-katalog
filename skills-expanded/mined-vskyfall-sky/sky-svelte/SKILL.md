---
name: sky-svelte
description: >-
  Svelte 5 ve SvelteKit: rünler ($state, $derived, $effect, $props, $bindable), snippet'ler,
  bileşen kalıpları, SvelteKit routing (+page, +layout, +server), load fonksiyonları (sunucu/
  evrensel), form actions ve ilerlemeli geliştirme (use:enhance), hook'lar ve auth, adaptörler
  (Vercel, Node, Cloudflare), prerender/SSR ayarları, store'lardan rünlere geçiş, test ve
  performans. Svelte/SvelteKit projesinde kullan.
disable-model-invocation: true
---

# Sky · Svelte & SvelteKit

## Svelte 5 rünleri

```svelte
<script lang="ts">
  let { bookings, onSelect }: { bookings: Booking[]; onSelect: (id: string) => void } = $props();
  let query = $state("");
  const filtered = $derived(bookings.filter((b) => b.clientName.toLocaleLowerCase("tr").includes(query.toLocaleLowerCase("tr"))));
  $effect(() => { document.title = `${filtered.length} randevu`; });   // yan etki — az kullan
</script>

<input bind:value={query} placeholder="Müşteri ara" />
{#each filtered as b (b.id)}
  <button onclick={() => onSelect(b.id)}>{b.clientName}</button>
{:else}
  <p>Eşleşen randevu yok</p>
{/each}
```
- `$state` derin reaktif; türetme `$derived` (effect ile state senkronlama yapma); `$bindable()` iki yönlü prop.
- Snippet'ler (`{#snippet row(b)}…{/snippet}` + `{@render row(b)}`) slot'ların yerini alır.
- Paylaşılan durum: `.svelte.ts` dosyasında `$state` içeren sınıf/nesne (store'lara gerek kalmaz); eski kodda store'lar çalışmaya devam eder.

## SvelteKit

```
src/routes/
  +layout.svelte
  bookings/+page.server.ts   # load + actions (sunucu)
  bookings/+page.svelte
  api/health/+server.ts      # uç nokta
src/hooks.server.ts          # her istek: oturum → event.locals.user
```
```ts
// +page.server.ts
export const load = async ({ locals }) => {
  if (!locals.user) redirect(303, "/login");
  return { bookings: await listBookings(locals.user) };
};
export const actions = {
  cancel: async ({ request, locals }) => {
    const data = Object.fromEntries(await request.formData());
    const parsed = CancelSchema.safeParse(data);
    if (!parsed.success) return fail(422, { errors: parsed.error.flatten().fieldErrors });
    await cancelBooking(locals.user, parsed.data.id);
    return { ok: true };
  },
};
```
- Form'lar JS'siz çalışır; `use:enhance` ile SPA hissi (ilerlemeli geliştirme).
- `+page.server.ts` sunucuda (sırlar güvenli), `+page.ts` evrensel; `$env/static/private` ile sırlar.
- Yetki her `load`/`action`/`+server`'da; `hooks.server.ts` yalnızca oturumu çözer.
- Render: `export const prerender = true` (statik), `ssr = false` (SPA sayfası), adaptörler: `adapter-vercel`, `adapter-node`, `adapter-cloudflare`.

## Test ve kalite

Vitest + `@testing-library/svelte`, Playwright E2E; `svelte-check` tip kontrolü; `eslint-plugin-svelte`. Svelte'in derleme zamanı uyarıları (a11y dahil) ciddiye alınır.
