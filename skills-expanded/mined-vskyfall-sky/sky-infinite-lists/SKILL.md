---
name: sky-infinite-lists
description: >-
  Uzun listeler ve akışlar: sonsuz kaydırma vs "Daha fazla göster" vs sayfalama kararı, cursor
  tabanlı sayfalama, useInfiniteQuery, IntersectionObserver tetikleyici, sanallaştırma
  (TanStack Virtual), kaydırma konumunu geri yükleme, "yeni gönderiler var" balonu, yukarı
  çekip yenileme, yukarı dön butonu, sohbet geçmişi ve iskelet/hata durumları. Feed, ürün
  listesi, mesaj geçmişi veya "sonsuz scroll" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Uzun Listeler & Akışlar

## Hangi kalıp?

| Kullanım | Kalıp |
|---|---|
| Keşif/akış (sosyal feed, ilham galerisi) | **Sonsuz kaydırma** |
| Ürün listesi, arama sonuçları (footer önemli) | **"Daha fazla göster" butonu** |
| Yönetim tablosu, belirli sayfaya gitme | **Sayfalama** (bkz. `sky-dashboard`) |
| Sohbet geçmişi | Ters yönde sonsuz (yukarı kaydırınca eskiler) |

## Cursor sayfalama (sunucu)

```ts
// GET /api/posts?cursor=<createdAt_id>&limit=20
const rows = await db.select().from(posts)
  .where(cursor ? or(lt(posts.createdAt, c.createdAt), and(eq(posts.createdAt, c.createdAt), lt(posts.id, c.id))) : undefined)
  .orderBy(desc(posts.createdAt), desc(posts.id)).limit(limit + 1);
const hasMore = rows.length > limit;
return { items: rows.slice(0, limit), nextCursor: hasMore ? encode(rows[limit - 1]) : null };
```
Sıralama alanı + benzersiz id ile bileşik cursor (aynı zaman damgalı kayıtlar kaybolmasın). Offset değil.

## İstemci (useInfiniteQuery)

```tsx
const q = useInfiniteQuery({
  queryKey: ["posts", filters],
  queryFn: ({ pageParam }) => fetchPosts({ cursor: pageParam, ...filters }),
  initialPageParam: null as string | null,
  getNextPageParam: (last) => last.nextCursor,
});
const sentinel = useRef<HTMLDivElement>(null);
useEffect(() => {
  const io = new IntersectionObserver(([e]) => e.isIntersecting && q.hasNextPage && !q.isFetchingNextPage && q.fetchNextPage(),
    { rootMargin: "600px" });                                // sona gelmeden yükle
  sentinel.current && io.observe(sentinel.current);
  return () => io.disconnect();
}, [q.hasNextPage, q.isFetchingNextPage]);
```
- `rootMargin` ile kullanıcı sona varmadan yükle → hiç beklemez.
- İlk sayfa sunucuda render (SEO + hız); sonrakiler istemcide.
- Hata: listenin sonunda "Yüklenemedi · Tekrar dene"; yüklenmiş öğeler kalır.
- Son: "Hepsi bu kadar 🎉" gibi net bitiş.

## Sanallaştırma

```tsx
const v = useWindowVirtualizer({ count: items.length, estimateSize: () => 120, overscan: 6 });
```
- Değişken yükseklik: `measureElement`.
- Izgara için satır başına N öğe gruplayıp satırları sanallaştır.
- Ctrl+F sanallaştırılmış öğeleri bulamaz — kritik listelerde arama kutusu ver.

## Kaydırma konumunu geri yükleme (en çok sevilen detay)

Kullanıcı ürüne tıklar, geri döner → **aynı yerde** olmalı, yüklenmiş sayfalar duruyor olmalı.
- TanStack Query cache'i sayfaları tutar (`gcTime` yeterli); App Router geri navigasyonda scroll'u genelde korur.
- Sanallaştırılmış listede `sessionStorage`'a offset kaydet, dönüşte `initialOffset`.
- Detayı modal/kesen route ile açmak (bkz. `sky-nextjs`) listeyi hiç bırakmaz — en iyi çözüm.

## Akış detayları

- **"Yeni gönderiler var ↑" balonu:** listeyi itme; balon göster, tıklayınca en üste kaydır ve ekle.
- **Yukarı çekip yenile** (mobil); masaüstünde "Yenile" butonu.
- **Yukarı dön butonu:** 2 ekran aşağı inince sağ altta; reduced-motion'da anlık kaydırma.
- Sohbet: altta başla; kullanıcı en alttaysa yeni mesajda otomatik kaydır, değilse "↓ 3 yeni mesaj" rozeti.

## Erişilebilirlik

- Liste `role="feed"`, öğeler `role="article"` + `aria-posinset`/`aria-setsize` (bilinmiyorsa -1).
- Yeni öğeler yüklenince `aria-live="polite"`: "20 gönderi daha yüklendi".
- Klavye kullanıcısı için "Daha fazla yükle" butonu odaklanabilir.
- Atlama bağlantısı: "Akışı atla, alt bilgiye git".
