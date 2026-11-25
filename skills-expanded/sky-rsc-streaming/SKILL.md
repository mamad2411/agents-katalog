---
name: sky-rsc-streaming
description: >-
  React Server Components ve streaming ileri seviye: Suspense sınırı tasarımı, veri
  waterfall'larını yok etme, paralel veri çekme, preload kalıbı, use() ile promise geçirme,
  Partial Prerendering (PPR) kabuk/delik ayrımı, iskelet tasarımı, hata sınırları ve sayfanın
  "anında açılıyormuş" hissettirmesi. "Sayfa geç açılıyor", "waterfall", "Suspense nereye",
  "loading.tsx yetmiyor" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · RSC & Streaming

Hedef: kullanıcı **ilk 200ms'de** anlamlı bir kabuk görür, yavaş parçalar kendi yerlerinde akar,
hiçbir yavaş sorgu bütün sayfayı rehin almaz.

## Waterfall avı

```tsx
// ✗ sıralı: toplam = a + b + c
const user = await getUser();
const posts = await getPosts();
const stats = await getStats();

// ✓ paralel: toplam = max(a, b, c)
const [user, posts, stats] = await Promise.all([getUser(), getPosts(), getStats()]);
```
Bağımlı olanlar (posts → user.id) sıralı kalır; bağımsızları ayır. İç içe bileşenlerdeki gizli
waterfall: ebeveyn `await` ederken çocuk henüz başlamadı → çocuğun verisini ebeveynde başlat
ve **promise** olarak geçir:

```tsx
// page.tsx
const statsPromise = getStats();          // await YOK — hemen başlar
return (
  <>
    <Header user={await getUser()} />
    <Suspense fallback={<StatsSkeleton />}>
      <Stats promise={statsPromise} />
    </Suspense>
  </>
);
// Stats.tsx (client da olabilir)
export function Stats({ promise }: { promise: Promise<StatsData> }) {
  const stats = use(promise);
  return <StatGrid data={stats} />;
}
```

## Suspense sınırı tasarımı

- Her **bağımsız yavaş** parça kendi sınırında: grafik, öneriler, yorumlar, "benzer ürünler".
- Kritik içerik (başlık, ana metin, birincil CTA) Suspense dışında veya en hızlı sınırda.
- Çok küçük sınırlar → "patlamış mısır" etkisi (parçalar ayrı ayrı pat pat belirir). Görsel olarak
  bir arada duranları tek sınırda grupla.
- İç içe sınırlar: dış kabuk hızlı, iç detay sonra.
- `loading.tsx` = route segmentinin tamamı için tek sınır; ince ayar için bileşen seviyesinde `<Suspense>`.

## İskelet (skeleton) kuralları

- Gerçek içeriğin **aynı boyutu ve düzeni**: başlık çizgisi, satır sayısı, avatar dairesi. CLS = 0.
- Hafif `pulse` animasyonu (reduced-motion'da sabit).
- Metin yerine "Yükleniyor…" yazan kutu değil, şekil.
- 300ms'den kısa sürecek parçalar için iskelet gösterme (yanıp sönme) — gezintilerde `startTransition`
  ile eski içeriği tut.

## Preload kalıbı

```ts
// lib/data.ts
export const getProduct = cache(async (id: string) => db.query.products.findFirst({ where: eq(products.id, id) }));
export const preloadProduct = (id: string) => void getProduct(id);
```
Layout'ta veya üst bileşende `preloadProduct(id)` çağır → alt bileşen `await getProduct(id)` dediğinde
istek zaten yolda. `cache()` aynı istek içinde tekilleştirir.

## Partial Prerendering (PPR) zihniyeti

Sayfayı **statik kabuk + dinamik delikler** olarak düşün:
- Statik: layout, navigasyon, ürün açıklaması, görseller, footer.
- Dinamik delik (`Suspense` içinde): sepet sayısı, kişisel öneriler, "merhaba Ayşe", stok durumu.
Kabuk CDN'den anında; delikler aynı yanıtta akar. Dinamik API'yi (`cookies()`) deliğin **içinde** çağır.

## Hata sınırları

- `error.tsx` segment başına; bileşen seviyesinde `react-error-boundary` ile sadece widget'ı düşür:
  "Öneriler yüklenemedi · Tekrar dene" — sayfanın kalanı yaşar.
- Kritik veri hatası → `notFound()` veya segment hata sayfası.
- Hata sınırı `Suspense`in **dışında** sarar (hem bekleme hem hata).

## Gezinti hissi

- `<Link prefetch>` görünürdeki bağlantıları önceden getirir; ağır sayfalarda `prefetch={false}` + hover'da `router.prefetch`.
- `useTransition` / `startTransition` ile filtre değişimlerinde eski liste soluk kalsın, boş ekran olmasın.
- `useLinkStatus` / `useFormStatus` ile tıklanan bağlantıda/butonda anında geri bildirim.

## Ölçüm

- DevTools Network → "Doc" isteğinde akan parçaları gör (Response'un zamanla büyümesi).
- `next build` çıktısında route türleri; Server Timing başlığı ile sorgu süreleri.
- Hedef: TTFB < 200ms (kabuk), LCP < 2.5s, en yavaş delik < 1.5s.
