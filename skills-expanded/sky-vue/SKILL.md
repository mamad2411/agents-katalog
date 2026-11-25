---
name: sky-vue
description: >-
  Vue 3 ve Nuxt: Composition API ve <script setup>, ref/reactive/computed/watch doğru kullanımı,
  reaktivite tuzakları, composable'lar, Pinia ile durum, Vue Router, Nuxt 3/4 (dosya tabanlı
  route, useFetch/useAsyncData, server routes, SSR/SSG/hibrit render, Nitro), TypeScript ile
  props/emits, bileşen kalıpları, VueUse, test (Vitest + Vue Test Utils) ve performans. Vue veya
  Nuxt projesinde kullan.
disable-model-invocation: true
---

# Sky · Vue & Nuxt

## Composition API

```vue
<script setup lang="ts">
const props = defineProps<{ orgId: string; initialFilter?: "all" | "upcoming" }>();
const emit = defineEmits<{ select: [id: string] }>();
const filter = ref(props.initialFilter ?? "upcoming");
const { data: bookings, status, refresh } = await useFetch(() => `/api/orgs/${props.orgId}/bookings`, { query: { filter } });
const count = computed(() => bookings.value?.length ?? 0);
</script>

<template>
  <BookingSkeleton v-if="status === 'pending'" />
  <EmptyState v-else-if="!count" title="Henüz randevu yok" />
  <ul v-else><li v-for="b in bookings" :key="b.id" @click="emit('select', b.id)">{{ b.clientName }}</li></ul>
</template>
```

## Reaktivite kuralları

- İlkel değerler `ref`, nesneler de çoğu zaman `ref` (tek kalıp); `reactive`'i yapı bozarak (destructure) kullanma — reaktivite kaybolur (`toRefs`).
- Türetilmiş değer `computed` (yan etkisiz); yan etki `watch`/`watchEffect` (az kullan).
- Props'u doğrudan değiştirme; `defineModel()` ile iki yönlü bağlama.
- Büyük, değişmeyen veri için `shallowRef` / `markRaw` (performans).
- Liste `:key` kararlı ID.

## Composable'lar

`useX()` fonksiyonları — durum + mantık paylaşımı (`useBookings(orgId)`); VueUse (`useDebounceFn`, `useLocalStorage`, `useIntersectionObserver`) tekerleği yeniden icat etmeden.

## Durum ve routing

- **Pinia**: setup store (`defineStore("cart", () => { … })`), yalnızca gerçekten global durum; sunucu verisi için Nuxt `useFetch` veya TanStack Vue Query.
- Vue Router: tip güvenli rotalar (`unplugin-vue-router`), navigation guard'larda auth.

## Nuxt

- Dosya tabanlı `pages/`, `layouts/`, `components/` (otomatik import), `server/api/*.ts` (Nitro uç noktaları — `defineEventHandler`, `readValidatedBody(event, schema.parse)`).
- Veri: `useFetch`/`useAsyncData` (SSR'da çekilir, istemciye aktarılır — çift istek yok); anahtar ver, `watch` ile yeniden çek.
- Render: `routeRules` ile sayfa bazında SSR / SSG (`prerender`) / ISR (`swr`) / SPA.
- `runtimeConfig` (sırlar sunucuda, `public` istemcide); `useHead`/`useSeoMeta` ile SEO (bkz. `sky-seo`).
- Modüller: `@nuxt/image`, `@nuxtjs/i18n` (bkz. `sky-i18n`), `@pinia/nuxt`, `@nuxt/ui`.
- Sunucu tarafında yetki kontrolü her `server/api` handler'ında.

## Test ve kalite

Vitest + `@vue/test-utils` (+ `@nuxt/test-utils`), Testing Library Vue; `vue-tsc --noEmit` tip kontrolü; ESLint `eslint-plugin-vue`.
Performans: `v-memo`, `defineAsyncComponent`, `<KeepAlive>`, büyük listelerde sanallaştırma.
