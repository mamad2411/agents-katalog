---
name: sky-lms
description: >-
  Online kurs / eğitim platformu: kurs → bölüm → ders modeli, video ders (HLS, ilerleme
  kaydetme, kaldığın yerden devam), metin/quiz/ödev dersleri, ilerleme takibi ve tamamlama
  oranı, sertifika (QR doğrulamalı PDF), kurs satışı ve kupon, öğrenci paneli, eğitmen paneli,
  yorumlar ve soru-cevap, damla (drip) içerik, oyunlaştırma ve video içerik korumasının
  gerçekçi sınırları. "Kurs sitesi", "online eğitim", "Udemy gibi", "eğitim platformu" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Kurs Platformu

## Önce

Tek eğitmen, birkaç kurs → hazır platformlar (Teachable, Thinkific, Kajabi; TR'de çeşitli yerel çözümler) çoğu zaman yeter.
Özel platform: marka deneyimi, özel iş modeli (kurumsal eğitim, abonelik kütüphanesi), entegrasyon gerektiğinde.

## Veri modeli

```
courses      id, slug, title, subtitle, cover, level, price_minor, status, instructor_id
sections     id, course_id, title, position
lessons      id, section_id, kind (video|text|quiz|assignment), title, duration_s, position, free_preview bool, available_after_days
enrollments  user_id, course_id, source (purchase|coupon|admin|subscription), enrolled_at, completed_at
progress     user_id, lesson_id, status (started|completed), position_s, updated_at
quiz_attempts user_id, lesson_id, score, answers jsonb, created_at
certificates id (doğrulama kodu), user_id, course_id, issued_at
```

## Ders oynatıcı (deneyimin kalbi)

- Video: Mux / Cloudflare Stream / Bunny (HLS, imzalı URL, uyarlanabilir kalite — bkz. `sky-media`).
- **Kaldığın yerden devam**: her 10 sn'de `position_s` kaydet (debounce), dönüşte "Kaldığın yerden devam et (12:34)".
- %90 izlenince otomatik "tamamlandı" + sonraki derse geri sayım ("5 sn içinde sonraki ders").
- Hız (0.75–2×), altyazı (TR/EN), klavye kısayolları (Boşluk, ←/→ 5 sn), tam ekran, sinema modu.
- Sol/sağ panelde müfredat: bölümler, ✓ işaretli tamamlananlar, süreler, aktif ders vurgulu.
- Ders altı sekmeler: Notlar (zaman damgalı, tıklayınca o saniyeye git — öğrenciler bayılır), Kaynaklar (indirilebilir), Soru-cevap.

## İlerleme ve motivasyon

- Kurs kartında ilerleme çubuğu (%42), "Devam et" butonu panelin en üstünde.
- Bölüm tamamlama kutlaması, seri ve haftalık hedef (bkz. `sky-gamification`).
- Haftalık "kaldığın yerden devam et" e-postası (aktif değilse).

## Quiz ve ödev

- Quiz: çoktan seçmeli/çoklu seçim/doğru-yanlış; anında geri bildirim + açıklama; geçme notu; tekrar deneme hakkı.
- Ödev: dosya/bağlantı yükleme, eğitmen değerlendirmesi ve yorum.

## Sertifika

Kurs tamamlanınca (ve quiz geçme koşulu) → PDF sertifika (ad, kurs, tarih, eğitmen imzası, **doğrulama QR'ı** →
`site.com/sertifika/ABC123`) + LinkedIn'e ekle bağlantısı + paylaşılabilir OG kartı. Bkz. `sky-print-pdf`.

## Satış

- Kurs sayfası: tanıtım videosu, kazanımlar ("Bu kursun sonunda…"), müfredat (ücretsiz önizleme dersleri oynatılabilir), eğitmen, yorumlar, SSS, fiyat + kupon (bkz. `sky-landing`, `sky-payments`).
- Paketler, abonelik (tüm kütüphane), kurumsal toplu lisans (org + koltuk, bkz. `sky-multitenancy`).
- Damla içerik: `available_after_days` ile ders kayıt tarihinden N gün sonra açılır.

## Eğitmen paneli

Kurs oluşturucu (bölüm/ders sürükle-bırak sıralama — bkz. `sky-drag-drop`), video yükleme (bkz. `sky-storage`), öğrenci listesi ve ilerlemeleri,
soru-cevap gelen kutusu, gelir raporu (bkz. `sky-dashboard`), duyuru e-postası.

## İçerik koruma (gerçekçi ol)

İmzalı, kısa ömürlü video URL'leri, oturum başına cihaz sınırı, filigran (öğrenci e-postası videoda soluk) caydırıcıdır; ekran kaydını
**engelleyemezsin**. DRM yalnızca gerçekten gerekiyorsa (maliyetli). Kullanıcıya düşmanca önlemlerle deneyimi bozma.
