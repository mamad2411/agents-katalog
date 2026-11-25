---
name: sky-tailwind
description: >-
  Tailwind CSS v4 derinlemesine: CSS-first yapılandırma (@import "tailwindcss", @theme, @utility,
  @variant, @custom-variant), token'ları tema değişkenlerine bağlama, dark mode stratejileri,
  container queries ve yeni varyantlar, özel yardımcılar ve eklentiler, sınıf sıralama ve
  okunurluk (cn, cva, prettier-plugin-tailwindcss), keyfi değerlerden kaçınma, v3'ten geçiş,
  performans ve sık hatalar. Tailwind kullanan projede kullan.
disable-model-invocation: true
---

# Sky · Tailwind CSS v4

## Kurulum (CSS-first)

```css
/* app.css */
@import "tailwindcss";
@source "../node_modules/@acme/ui";          /* otomatik algılanmayan sınıf kaynakları */
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));   /* sınıf/öznitelik tabanlı dark mode */

@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --color-brand-500: oklch(0.6 0.18 262);
  --color-brand-600: oklch(0.53 0.19 262);
  --radius-card: 0.75rem;
  --breakpoint-3xl: 120rem;
  --animate-fade-in: fade-in 0.2s var(--ease-out);
  @keyframes fade-in { from { opacity: 0; translate: 0 4px; } }
}
```
`tailwind.config.js` gerekmez; Vite'ta `@tailwindcss/vite`, diğerlerinde `@tailwindcss/postcss`. Semantik token eşlemesi (`@theme inline` ile CSS değişkenlerine) `sky-design-system`'de.

## Özel yardımcı ve varyant

```css
@utility container-narrow { max-width: 65ch; margin-inline: auto; padding-inline: 1rem; }
@utility scrollbar-none { scrollbar-width: none; &::-webkit-scrollbar { display: none; } }
@variant hocus (&:hover, &:focus-visible);
```

## Yeni ve faydalı

- Container queries yerleşik: `@container` + `@md:grid-cols-2`.
- `not-*`, `in-*`, `has-*`, `group-has-*`, `peer-*`, `aria-*`, `data-*` varyantları (`data-[state=open]:rotate-180`, `aria-invalid:border-danger`).
- `starting:` (giriş animasyonu), `inert:`, `open:`, `user-invalid:`, `pointer-coarse:` (dokunmatik cihaz).
- `size-10`, `inset-shadow-*`, `text-shadow-*` (sürüme göre), 3D dönüşümler, `bg-linear-to-r` ve `in-oklch` gradyan ara değerlemesi.
- Dinamik değerler: `grid-cols-15`, `mt-17` gibi değerler ölçekten türetilir (keyfi `[...]` gereksiz).

## Okunurluk

- `cn()` (clsx + tailwind-merge) ile koşullu sınıflar ve üzerine yazma; tekrar eden kombinasyon → bileşen + `cva` (bkz. `sky-design-system`), `@apply` değil.
- `prettier-plugin-tailwindcss` ile sınıf sıralaması otomatik.
- Keyfi değer (`p-[13px]`, `text-[#333]`) = token eksikliği işareti → `@theme`'e ekle (Sky hook'u uyarır).
- Uzun sınıf listesini satırlara böl veya varyant nesnesine taşı.

## Dinamik sınıf tuzağı

```tsx
// ✗ derleyici göremez:  `bg-${color}-500`
// ✓ tam sınıf adları:
const colors = { success: "bg-success", danger: "bg-danger" } as const;
```

## v3 → v4

`npx @tailwindcss/upgrade` (bkz. `sky-upgrades`): yapılandırma CSS'e taşınır, bazı ölçek adları değişti (`shadow-sm`→`shadow-xs`, `rounded-sm`→`rounded-xs`, `ring` varsayılan 1px), `bg-opacity-*` yerine `bg-black/50`. Görsel regresyon testiyle doğrula.

## Sık hatalar

Sınıflar çalışmıyor → kaynak dosya taranmıyor (`@source`); dark mode çalışmıyor → varyant stratejisi (medya vs sınıf); üçüncü parti bileşen stilleri ezilmiyor → katman sırası (`@layer`) veya `!` önemli işareti dikkatli.
