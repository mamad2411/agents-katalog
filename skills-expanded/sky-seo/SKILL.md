---
name: sky-seo
description: >-
  SEO: Türkçe karakterli slug, yerel SEO (Türkiye), metadata, JSON-LD, sitemap, hreflang, Core Web
  Vitals. "SEO", "Google'da çıksın", "meta etiketleri" dendiğinde kullan.
---

# Sky · SEO

Landing metni ve dönüşüm `sky-landing`; hız `sky-perf`; çok dillilik `sky-i18n`. Burada
arama motorlarının sayfayı **bulması, anlaması ve tercih etmesi** için gerekenler var.

## Taranabilirlik

- **robots.txt** (`app/robots.ts`): prod'da `allow: /`, özel alanlar `disallow: /api/, /dashboard/, /hesap/`;
  sitemap URL'i. Preview/staging'de **tamamen engelle** + `X-Robots-Tag: noindex`.
- **sitemap.xml** (`app/sitemap.ts`): yalnızca indekslenebilir, 200 dönen, canonical sayfalar; `lastModified`
  gerçek; 50k URL üstünde sitemap index. Dinamik içerik için DB'den üret.
- **canonical**: her sayfada kendisi (parametreli varyantlar ana URL'e); `metadata.alternates.canonical`.
- **noindex**: arama sonuç sayfaları, filtreli listeler, teşekkür sayfaları, kullanıcı profili (gizliyse), sayfalama 2+ (duruma göre).
- Giriş gerekli sayfalar bot için 200 boş kabuk **dönmesin**; yönlendir veya `noindex`.
- 404 gerçekten `404` dönsün (soft 404 yok); kalıcı kaldırılan içerik `410`.

## Render

İndekslenecek içerik **sunucuda HTML olarak** gelsin (SSR/SSG/ISR). İstemci tarafı render edilen
ürün listesi/blog yazısı riskli ve yavaş indekslenir. "View Source"ta içerik görünüyorsa tamam.

## Metadata (Next.js)

```ts
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);           // sayfa ile aynı fetch → memoize edilir
  if (!post) return {};
  return {
    title: post.title,                               // layout'ta template: "%s · Sky"
    description: post.excerpt,                       // 150–160 karakter
    alternates: { canonical: `/blog/${post.slug}`, languages: { tr: `/blog/${post.slug}`, en: `/en/blog/${post.slugEn}` } },
    openGraph: { type: "article", publishedTime: post.publishedAt, authors: [post.author.name], images: [`/blog/${post.slug}/opengraph-image`] },
    twitter: { card: "summary_large_image" },
    robots: post.draft ? { index: false, follow: false } : undefined,
  };
}
```
- **Title:** 50–60 karakter, ana anahtar kelime başta, marka sonda (`template`), her sayfa benzersiz.
- **Description:** 150–160 karakter, değer önerisi + eylem; Google yine de kendi snippet'ini seçebilir.
- `metadataBase` kök layout'ta → göreli OG URL'leri mutlak olur.
- `opengraph-image.tsx` ile dinamik OG (1200×630, `ImageResponse`); fontu `latin-ext` ile yükle (Türkçe).
- `app/icon.tsx`/`favicon.ico`, `apple-icon`, `manifest.ts`.

## Yapılandırılmış veri (JSON-LD)

Sayfaya `<script type="application/ld+json">` (Server Component'te `dangerouslySetInnerHTML` ile JSON.stringify — `<` karakterini `<` yap).

| Sayfa | Tür |
|---|---|
| Ana sayfa | `Organization` (logo, sameAs sosyal), `WebSite` (+ `SearchAction` varsa) |
| Yerel işletme (klinik, salon) | `LocalBusiness` alt türü (`MedicalClinic`, `HairSalon`): adres, telefon, `openingHoursSpecification`, `geo` |
| Ürün | `Product` + `Offer` (fiyat, `priceCurrency: "TRY"`, stok), `AggregateRating` yalnızca gerçek yorum varsa |
| SaaS | `SoftwareApplication` + `Offer` |
| Blog yazısı | `Article`/`BlogPosting`: headline, image, datePublished, dateModified, author (`Person`) |
| SSS | `FAQPage` (yalnızca görünür SSS içeriğiyle aynı) |
| Gezinme | `BreadcrumbList` |
| Etkinlik, tarif, iş ilanı | `Event`, `Recipe`, `JobPosting` |

Doğrula: Rich Results Test / Schema Validator. Görünür içerikle **eşleşmeyen** yapılandırılmış veri ceza riskidir.

## URL ve slug

- Kısa, okunur, küçük harf, tire ile: `/blog/next-js-onbellek-rehberi`. Türkçe karakterleri dönüştür
  (`ş→s, ç→c, ğ→g, ı→i, İ→i, ö→o, ü→u`); stop word'leri atmak şart değil.
- Slug değişirse **301** eski → yeni (`next.config redirects()` veya DB tabanlı yönlendirme tablosu). Slug'ı
  ID'den bağımsız tut ki içerik başlığı değişince URL sabit kalabilsin (ya da eski slug'ları sakla).
- Sondaki `/` tutarlı (`trailingSlash` tek tercih); `http→https`, `www` tek yöne 301.
- Parametreler (`?utm_`, `?sort=`) canonical ile ana URL'e.

## Sayfa içi hijyen

- Tek `<h1>` (sayfanın konusu), mantıklı `h2/h3`; başlıklar stil için değil yapı için.
- İlk 100 kelimede konu net; paragraflar kısa; listeler ve tablolar (featured snippet şansı).
- Görseller: anlamlı dosya adı (`randevu-takvimi.webp`), `alt` açıklayıcı, boyutlu (CLS), lazy (hero hariç).
- İç bağlantılar: ilgili içeriğe anlamlı anchor metniyle ("randevu hatırlatma SMS'i nasıl kurulur");
  her önemli sayfaya ana sayfadan ≤ 3 tık.
- Dış bağlantı: güvenilir kaynak; sponsorlu/UGC için `rel="sponsored"/"ugc"`.
- Breadcrumb görünür + JSON-LD.
- Sayfalama: `?page=2` indekslenebilir ama canonical kendisi; "tümünü gör" sayfası alternatifi.

## Core Web Vitals

Sıralama faktörü; hedefler ve çözümler `sky-perf`. SEO açısından kritik: mobil LCP < 2,5 s, CLS < 0,1,
INP < 200 ms **gerçek kullanıcı verisinde** (CrUX / Search Console "Deneyim" raporu).

## İçerik mimarisi (blog/rehber)

- **Konu kümeleri:** bir "pillar" sayfa (geniş rehber) + ona bağlanan alt yazılar; birbirlerine çapraz bağlantı.
- Arama niyetine göre sayfa türü: bilgi (rehber), karşılaştırma (X vs Y), işlem (fiyatlandırma, demo), yerel (şehir + hizmet).
- Her yazı: hedef sorgu, benzersiz başlık, meta, OG, yazar bilgisi (E-E-A-T), güncelleme tarihi, ilgili yazılar.
- İnce içerik (300 kelimelik etiket sayfaları, boş kategori) `noindex`.
- Yazar sayfaları + `Person` JSON-LD güven için.
- RSS (`/feed.xml`) ve `sitemap` güncel.

## Yerel SEO (Türkiye)

- **Google Business Profile** kaydı, kategorisi, saatleri, fotoğrafları; site ile NAP (ad-adres-telefon) **birebir** aynı.
- `LocalBusiness` JSON-LD + görünür adres/telefon (`tel:` bağlantısı) + harita gömme (lazy).
- Şehir/ilçe hizmet sayfaları yalnızca **gerçekten farklı** içerikle (aynı metin şehir adı değişmiş = doorway).
- Yorum toplama akışı (QR/SMS ile GBP yorum bağlantısı).
- Türkçe arama: hem "ğ/ş'li" hem "gs'siz" yazımlar aranır; URL'de ASCII, içerikte doğru Türkçe.

## Ölçüm

- **Google Search Console**: alanı doğrula (DNS TXT), sitemap gönder, kapsam/indeksleme raporu, CWV, zengin sonuç hataları.
- Bing Webmaster Tools (IndexNow ile anında bildirim; Yandex da destekler).
- Lighthouse SEO ≥ 95 sadece temel hijyen; gerçek ölçü Search Console tıklama/gösterim/pozisyon.
- `site:example.com` ile indekslenen sayfa sayısını kontrol et; fazlalık varsa (parametreli URL'ler) canonical/noindex.
- Analytics'te organik trafik ve dönüşüm ayrı segment (çerez onayına uygun; bkz. `sky-observability`).

## Kaçın

Anahtar kelime yığma, gizli metin, satın alınmış bağlantılar, otomatik üretilmiş ince içerik, doorway sayfalar,
cloaking (bota farklı içerik), aldatıcı yönlendirme, görünür içerikle uyuşmayan JSON-LD, iç arama sayfalarının indekslenmesi.

## Kontrol listesi

- [ ] robots/sitemap/canonical doğru; preview noindex
- [ ] İçerik sunucuda render ediliyor
- [ ] Her sayfa benzersiz title (50–60) + description (150–160) + OG görseli
- [ ] Uygun JSON-LD, doğrulandı
- [ ] Tek h1, alt'lı görseller, anlamlı iç bağlantılar
- [ ] Slug ASCII; eski URL'ler 301
- [ ] hreflang (çok dilliyse)
- [ ] CWV mobilde yeşil
- [ ] Search Console'a bağlı, sitemap gönderildi
