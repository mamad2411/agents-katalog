---
name: sky-design-system
description: >-
  Bileşen kütüphanesi ve tasarım sistemi mimarisi: üç katmanlı token (primitive → semantic →
  component), Tailwind v4 @theme ile token eşlemesi, cva / tailwind-variants ile varyantlar,
  cn() yardımcısı, compound component ve asChild (Radix Slot), kontrollü/kontrolsüz API,
  bileşen API ilkeleri, erişilebilirlik tabanı, dokümantasyon (Storybook veya /design route),
  görsel regresyon, sürümleme ve yeni bileşen kontrol listesi. "Tasarım sistemi kur",
  "bileşen kütüphanesi", "Button varyantları", "shadcn'i özelleştir" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Tasarım Sistemi

Görsel kararlar (tipografi, renk, boşluk) `sky-ui-craft`ta; burada bunları **yeniden kullanılabilir,
tutarlı ve belgelenmiş bileşenlere** dönüştürme mimarisi var.

## Katmanlar

```
1. Primitive token   --blue-600, --space-4, --radius-md        (ham palet; bileşen asla doğrudan kullanmaz)
2. Semantic token    --accent, --fg-muted, --surface, --ring   (anlam; tema burada değişir)
3. Component token   --button-bg, --button-fg, --card-padding  (isteğe bağlı; yalnızca çok temalı sistemlerde)
```
Bileşenler **semantic** katmanı tüketir. Dark mode = semantic token'ların yeniden tanımı
([tokens.css](../sky-ui-craft/references/tokens.css) buna göre kurulu).

## Tailwind v4 ile token eşlemesi

```css
/* globals.css */
@import "tailwindcss";
@theme inline {
  --color-bg: var(--bg);
  --color-surface: var(--surface);
  --color-fg: var(--fg);
  --color-fg-muted: var(--fg-muted);
  --color-accent: var(--accent);
  --color-accent-fg: var(--accent-fg);
  --color-border: var(--border);
  --color-danger: var(--danger);
  --radius-sm: var(--radius-sm);
  --radius-md: var(--radius-md);
  --font-sans: var(--font-sans);
  --ease-out: var(--ease-out);
}
```
Artık `bg-surface text-fg border-border rounded-md` çalışır ve tema CSS değişkeniyle değişir.
`@theme inline` kullan ki sınıflar `var(--bg)`e işaret etsin (runtime tema değişimi için şart).
Keyfi değerler (`bg-[#fff]`, `p-[13px]`) yasak — `sky-quality` hook'u uyarır.

## Varyantlar: cva

```tsx
import { cva, type VariantProps } from "class-variance-authority";

const button = cva(
  "inline-flex items-center justify-center gap-2 font-medium rounded-md transition-colors duration-fast " +
  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 " +
  "disabled:opacity-50 disabled:pointer-events-none select-none",
  {
    variants: {
      variant: {
        primary: "bg-accent text-accent-fg hover:bg-accent-hover",
        secondary: "bg-surface-2 text-fg hover:bg-border",
        ghost: "text-fg hover:bg-surface-2",
        danger: "bg-danger text-white hover:bg-danger/90",
      },
      size: { sm: "h-8 px-3 text-sm", md: "h-10 px-4", lg: "h-12 px-6 text-lg", icon: "size-10" },
    },
    defaultVariants: { variant: "primary", size: "md" },
  }
);

type ButtonProps = React.ComponentPropsWithoutRef<"button"> & VariantProps<typeof button> & { asChild?: boolean; loading?: boolean };

export function Button({ className, variant, size, asChild, loading, children, disabled, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button";
  return (
    <Comp className={cn(button({ variant, size }), className)} disabled={disabled || loading} aria-busy={loading || undefined} {...props}>
      {loading && <Spinner className="size-4" aria-hidden />}
      {children}
    </Comp>
  );
}
```
- `cn = (...i) => twMerge(clsx(i))` — dışarıdan `className` ile üzerine yazmaya izin ver, çakışmaları `twMerge` çözer.
- Varyant adları **anlam** söyler (`primary/secondary/danger`), renk değil (`blue/gray`).
- Boolean prop sayısını sınırla; 3+ boolean → `variant` enum'u.
- React 19'da `ref` normal prop; eski sürümde `forwardRef`.
- `tailwind-variants` alternatifi: `slots` desteğiyle çok parçalı bileşenlerde (Card) kullanışlı.

## Compound component

```tsx
<Card>
  <Card.Header><Card.Title>Başlık</Card.Title><Card.Description>…</Card.Description></Card.Header>
  <Card.Content>…</Card.Content>
  <Card.Footer><Button>Kaydet</Button></Card.Footer>
</Card>
```
Prop patlaması (`title`, `description`, `footerActions`…) yerine slot'lar. Parçalar arası durum
gerekiyorsa (Tabs, Accordion) context ile; hazır erişilebilir davranış için **Radix / React Aria**
primitive'lerini sarmala, sıfırdan yazma.

## `asChild` (Radix Slot)

`<Button asChild><Link href="/x">Git</Link></Button>` → stil Button'dan, öğe Link. `as` prop'u ve
polimorfik generics yerine daha basit; tipler sade kalır.

## Kontrollü / kontrolsüz

Her etkileşimli bileşen ikisini de desteklesin: `value`/`onValueChange` **veya** `defaultValue`.
`@radix-ui/react-use-controllable-state` ya da küçük bir `useControllableState` hook'u.
İkisini birden geçmek geliştirme modunda uyarı versin.

## Bileşen API ilkeleri

1. Native öğenin tüm prop'larını geçir (`ComponentPropsWithoutRef<"button">`); `className` her zaman açık.
2. İsimler platform sözlüğüyle: `onChange` değil `onValueChange` (Radix uyumu) — proje içinde **tek** sözleşme seç.
3. `size: sm | md | lg`, `variant`, `intent` tutarlı; her bileşende aynı ölçek.
4. Erişilebilirlik içeride: `aria-*`, klavye, odak halkası, `disabled` + `aria-disabled` tutarlılığı.
5. Yükleniyor/boş/hata durumları prop ile desteklenir (`loading`, `emptyState`), tüketici elle yazmaz.
6. İkon slotları `leftIcon`/`rightIcon` yerine `children` içinde `<Icon aria-hidden />` + `gap`.
7. Varsayılanlar güvenli: `type="button"` (form içinde yanlışlıkla submit etmesin).
8. Bir bileşen bir şey yapar; "akıllı" bileşen (veri çeken) `features/` içinde, `components/ui/` saf kalır.

## Klasör

```
components/ui/
  button/
    button.tsx          # bileşen + cva
    button.stories.tsx  # Storybook (veya /design örnekleri)
    button.test.tsx     # davranış + axe
    index.ts
  index.ts              # barrel (ölçülü)
lib/cn.ts
styles/globals.css      # token + @theme
```
shadcn/ui kullanıyorsan: bileşenler **kopyalanır**, sahiplenirsin; token'ları `globals.css`te
Sky şemasına taşı, `components.json` ile üretim yolunu ayarla; güncellemeleri `diff` ile seçerek al.

## Dokümantasyon

- **Storybook** (büyük takım) veya **`/design` route'u** (küçük takım; prod'da `notFound`): her bileşenin
  tüm varyant × boyut × durum matrisi, açık/koyu yan yana, "yap / yapma" örnekleri.
- Her bileşen için 5 satırlık doc: ne zaman kullan, ne zaman kullanma, erişilebilirlik notu, ilgili bileşenler.
- Token sayfası: renk kontrast tablosu (otomatik hesapla), tip ölçeği, boşluk ölçeği.

## Görsel regresyon

Playwright `toHaveScreenshot` ile `/design` sayfasının her matris bloğu; `animations: "disabled"`,
`reducedMotion: "reduce"`, sabit viewport (1280 ve 375), açık + koyu. Font yüklenmesini bekle
(`document.fonts.ready`). Fark eşiği `maxDiffPixelRatio: 0.01`.

## Sürümleme ve değişiklik

- Monorepo'da `packages/ui` + changesets; tek repoda `CHANGELOG` bölümü.
- Kırıcı değişiklik (prop kaldırma): önce `@deprecated` JSDoc + konsol uyarısı, bir sürüm sonra kaldır.
- Codemod (jscodeshift) ile toplu prop yeniden adlandırma.

## Yeni bileşen kontrol listesi

- [ ] Mevcut bileşenle/varyantla çözülemediği gerekçelendirildi
- [ ] Erişilebilir primitive (Radix/React Aria) üzerine kurulu veya native öğe
- [ ] Semantic token'lar; keyfi değer yok; dark mode'da kontrol edildi
- [ ] Varyant/boyut ölçeği sistemle aynı; `className` birleştirme çalışıyor
- [ ] Tüm durumlar: hover, focus-visible, active, disabled, loading, hata, uzun içerik, RTL (mantıksal özellikler)
- [ ] Klavye ve ekran okuyucu ile denendi; axe testi yeşil
- [ ] Story/örnek sayfası + görsel regresyon ekran görüntüsü
- [ ] Doc: ne zaman kullan / kullanma
