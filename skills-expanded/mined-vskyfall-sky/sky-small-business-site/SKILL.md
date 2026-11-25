---
name: sky-small-business-site
description: >-
  Türk küçük işletme siteleri (kuaför, klinik, restoran, emlakçı): randevu, QR menü, çalışma saatleri,
  WhatsApp butonu, yerel SEO. "Kuaför sitesi", "esnafa site" dendiğinde kullan.
---

# Sky · Küçük İşletme Sitesi

Ziyaretçinin 3 sorusu: **Ne yapıyorsunuz? Nerede/ne zaman açıksınız? Nasıl randevu/iletişim?** Her sayfa bu üçünü
5 saniyede cevaplasın.

## Ortak iskelet

1. Header: logo, menü, **"Randevu al"** / **"Ara"** butonu (mobilde yapışkan alt çubuk: 📞 Ara · 💬 WhatsApp · 📍 Yol tarifi).
2. Hero: işletme adı + ne yaptığı + konum ("Kadıköy'de diş kliniği"), gerçek mekân/ekip fotoğrafı, birincil CTA.
3. **Şimdi açık · 20:00'e kadar** rozeti (bkz. `sky-date-time`) — ziyaretçilerin en sevdiği küçük detay.
4. Hizmetler (fiyat aralığıyla — fiyat görmek güven verir), ekip, galeri, yorumlar (Google yorumları), SSS, iletişim + harita.
5. Footer: adres, telefon, çalışma saatleri, sosyal medya, KVKK/gizlilik.

## Sektör ekleri

| Sektör | Olmazsa olmaz |
|---|---|
| Klinik / diş | hekim profilleri (uzmanlık, eğitim), tedaviler sayfaları, online randevu, anlaşmalı kurumlar; sağlık reklamı mevzuatına dikkat (abartılı vaat, önce/sonra fotoğraf kuralları) |
| Kuaför / güzellik | hizmet + süre + fiyat, personel seçimli randevu, Instagram galerisi, kampanyalar |
| Restoran / kafe | **QR menü** (kategoriler, alerjen ikonları, fotoğraf, TL fiyat), rezervasyon, paket servis bağlantıları (Yemeksepeti/Getir), çalışma saatleri |
| Avukat / danışman | uzmanlık alanları, makaleler (SEO), iletişim formu (KVKK onaylı), randevu |
| Emlak | ilan listesi + filtre + harita, ilan detay galerisi, WhatsApp'tan sor |
| Oto servis | hizmetler, randevu, "aracım ne durumda" takip (isteğe bağlı) |
| Spor salonu | ders programı (haftalık takvim), üyelik paketleri, deneme dersi formu |

## Randevu ve iletişim

- Randevu motoru (bkz. `sky-scheduling`) veya basit form + WhatsApp yönlendirmesi (küçük bütçede).
- WhatsApp bağlantısı: `https://wa.me/905xxxxxxxxx?text=Merhaba,%20randevu%20almak%20istiyorum` (önceden dolu mesaj).
- Telefon `tel:+90…`; mesai dışı tıklamada "Şu an kapalıyız, WhatsApp'tan yazın" notu.

## Yerel SEO (en önemli büyüme kanalı)

Google İşletme profili ile NAP birebir aynı, `LocalBusiness` alt türü JSON-LD (`Dentist`, `HairSalon`, `Restaurant` +
`openingHoursSpecification`, `geo`, `priceRange`), hizmet × semt sayfaları yalnızca gerçek içerikle, yorum toplama QR'ı
(kasada/masada) — bkz. `sky-seo`.

## Hız ve maliyet

- Statik üretim (Next SSG / Astro), görseller optimize, harita tıklanınca yüklenir → mobil Lighthouse 95+.
- Barındırma: Vercel/Netlify/Cloudflare Pages ücretsiz katman çoğu zaman yeter; alan adı `.com.tr`.
- Müşteri içerik düzenleyecekse hafif CMS (Keystatic/Payload, bkz. `sky-cms`) — hizmetler, fiyatlar, saatler, kampanyalar.

## Teslim

Müşteriye kısa rehber + Google İşletme profili kontrolü + Search Console kurulumu (bkz. `sky-handoff`).
