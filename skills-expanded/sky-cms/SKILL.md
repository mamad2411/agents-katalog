---
name: sky-cms
description: >-
  İçerik yönetimi: headless CMS seçimi (Payload, Sanity, Strapi, Keystatic, Contentful), içerik
  modeli tasarımı (sayfa bölümleri/blok tabanlı sayfa kurucu), Next.js ile entegrasyon, taslak
  önizleme (draft mode) ve canlı düzenleme, webhook ile anında yayın (revalidate), görsel
  yönetimi, çok dilli içerik, editör deneyimi ve rol yetkileri, Git tabanlı MDX alternatifi.
  "Müşteri içeriği kendisi düzenlesin", "CMS", "blog yönetimi", "admin'den sayfa ekle" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · İçerik Yönetimi (CMS)

## Seçim

| Durum | Seçim |
|---|---|
| Next.js içinde, kendi DB'n, tam kontrol, ücretsiz | **Payload** (Next'e gömülü admin) |
| Gerçek zamanlı ortak düzenleme, güçlü görsel düzenleyici | **Sanity** (barındırılan, cömert ücretsiz plan) |
| Geliştirici dışı küçük site, Git'te içerik | **Keystatic** / Decap (Markdown/MDX + UI) |
| Self-host, REST/GraphQL, klasik | Strapi / Directus |
| Kurumsal | Contentful / Storyblok (görsel düzenleyici) |
| Yalnızca geliştirici yazar | **MDX dosyaları** + content collections — CMS'e gerek yok |

## İçerik modeli

- **Sayfa = bloklar dizisi**: Hero, ÖzellikIzgarası, Referanslar, SSS, CTA, Görsel+Metin… Her blok bir
  React bileşeniyle eşleşir — müşteri sayfayı Lego gibi kurar, tasarım sistemi bozulmaz.
```ts
// Payload örneği
{ slug: "pages", fields: [
  { name: "title", type: "text", required: true, localized: true },
  { name: "slug", type: "text", unique: true, index: true },
  { name: "blocks", type: "blocks", blocks: [HeroBlock, FeaturesBlock, TestimonialsBlock, FaqBlock, CtaBlock] },
  { name: "seo", type: "group", fields: [{ name: "title", type: "text" }, { name: "description", type: "textarea" }, { name: "ogImage", type: "upload", relationTo: "media" }] },
]}
```
- Blok alanlarına sınır: başlık maks 60 karakter, görsel oranı zorunlu → tasarım her zaman düzgün görünür.
- Tekrar kullanılan içerik (hizmetler, ekip, SSS) ayrı koleksiyon + ilişki.
- Global ayarlar (logo, iletişim, sosyal bağlantılar, çalışma saatleri) tek "Settings" belgesi.

## Next.js entegrasyonu

- Sayfalar statik üretilir (`generateStaticParams`), CMS webhook'u → `revalidateTag("page:" + slug)` → saniyeler içinde canlı.
- **Draft mode**: editör "Önizle"ye basar → `/api/draft?secret=…&slug=…` → `draftMode().enable()` → taslak içerik görünür, üstte "Önizleme modundasın · Çık" bandı.
- Canlı önizleme (Payload Live Preview / Sanity Presentation): editör yazarken yan panelde site güncellenir — müşterilerin en sevdiği özellik.
- Görseller CMS'in görsel CDN'i veya `next/image` ile; odak noktası (hotspot) desteği kırpmada yüzü korur.

## Editör deneyimi

- Alan açıklamaları ve örnekler ("Başlık 6–10 kelime, sonucu söylesin").
- Karakter sayaçları, SEO önizleme (Google sonucu ve sosyal kart görünümü).
- Roller: Editör (yazar, yayınlayamaz), Yayıncı, Admin. Yayın akışı: taslak → incelemede → yayında, zamanlanmış yayın.
- Sürüm geçmişi ve geri dönme (bkz. `sky-audit-history`).
- Türkçe admin arayüzü (Payload i18n `tr`).

## Çok dilli

Alan bazlı yerelleştirme (`localized: true`); eksik çeviride varsayılan dile düşme; slug'lar dil başına
(bkz. `sky-i18n`, `sky-seo` hreflang).

## Teslim

Müşteriye 1 sayfalık "İçeriğini nasıl düzenlersin" rehberi + kısa ekran videosu (bkz. `sky-handoff`).
