---
name: sky-landing
description: >-
  Landing ve pazarlama sayfaları: dönüşüm odaklı bölüm sırası, hero, değer önerisi metni,
  özellik ızgarası, sosyal kanıt, fiyat tablosu, SSS, CTA, SEO meta/OG etiketleri ve
  yapılandırılmış veri. Ürün tanıtım sayfası, portfolyo, ajans/klinik/işletme sitesi veya
  "landing page yap" isteğinde sky-ui-craft ile birlikte kullan.
disable-model-invocation: true
---

# Sky · Landing Sayfaları

## Bölüm sırası (varsayılan iskelet)

1. **Header** — logo, 3–5 bağlantı, tek birincil CTA. Mobilde menü.
2. **Hero** — başlık (ne + kime + sonuç, ≤ 10 kelime), alt başlık (1–2 cümle, nasıl),
   birincil + ikincil CTA, ürün görseli/ekran görüntüsü. Ekranın üst kısmında kalır.
3. **Güven şeridi** — müşteri logoları / kullanıcı sayısı / puan (gerçek verilerle).
4. **Problem → çözüm** — kullanıcının acısı, sonra senin yaklaşımın.
5. **Özellikler** — 3–6 madde; her biri ikon + fayda odaklı başlık + 1 cümle. Önemlileri
   görsel + metin dönüşümlü (zigzag) bölümlerle derinleştir.
6. **Nasıl çalışır** — 3 numaralı adım.
7. **Sosyal kanıt** — gerçek isim/rol/fotoğraflı yorumlar, vaka sonuçları (rakamla).
8. **Fiyatlandırma** — 2–3 plan, önerilen vurgulu, aylık/yıllık geçişi, plan karşılaştırması.
9. **SSS** — itirazları cevapla (fiyat, iptal, güvenlik, kurulum süresi). `<details>` ile.
10. **Son CTA** — tekrar değer önerisi + buton.
11. **Footer** — bağlantılar, iletişim, KVKK/gizlilik, sosyal medya.

Kısa sayfa (portfolyo, etkinlik) için 2, 5, 7, 10, 11 yeterli.

## Metin

- Özellik değil **sonuç** yaz: "Randevu iptallerini azaltın" > "SMS hatırlatma özelliği".
- Kullanıcının dilini kullan; jargon yok.
- CTA fiili net ve sonuçlu: "Ücretsiz dene", "Randevu al", "Demo iste".
- Sahte istatistik, uydurma müşteri yorumu veya gerçek bir markanın logosunu izinsiz koyma —
  yer tutucu kullan ve kullanıcıya belirt.

## Görsel

- Hero görseli gerçek ürün arayüzü veya bilinçli illüstrasyon; jenerik stok fotoğraf değil.
- Bölümler arası dikey boşluk geniş (`--space-24` masaüstü, `--space-16` mobil).
- Arka planı bölümler arasında hafifçe değiştir (bg / surface-2) ritim için.
- Hero görseli `priority`/`fetchpriority="high"`, diğer görseller lazy.
- Bir vurgu rengi; CTA'lar her yerde aynı stilde.

## SEO & paylaşım

```tsx
export const metadata = {
  title: "Ürün — tek cümlelik değer önerisi",
  description: "150–160 karakterlik açıklama.",
  openGraph: { images: ["/og.png"] },  // 1200×630
  alternates: { canonical: "https://site.com/" },
};
```
- Tek `<h1>`, mantıklı başlık hiyerarşisi.
- JSON-LD: `Organization`, `Product`/`SoftwareApplication`, yerel işletmede `LocalBusiness`, SSS'de `FAQPage`.
- `sitemap.xml`, `robots.txt`, favicon seti, `manifest.webmanifest`.
- Lighthouse: Performans ≥ 90, SEO ≥ 95, Erişilebilirlik ≥ 95.

## Dönüşüm detayları

- CTA birincil ekranda görünür; uzun sayfada yapışkan header CTA'sı.
- Form alanı sayısı minimum (e-posta tek başına çoğu zaman yeter).
- Analitik olaylar: CTA tıklaması, form gönderimi, fiyat sekmesi geçişi (çerez onayına uygun).
- Yükleme hızı dönüşümdür: bkz. `sky-perf`.
