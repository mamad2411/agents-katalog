---
name: sky-event-site
description: >-
  Etkinlik ve davet siteleri: düğün/nişan davetiyesi, doğum günü, konferans, meetup, mezuniyet,
  lansman; geri sayım, program/akış, konum ve yol tarifi, LCV/RSVP formu (kişi sayısı, menü
  tercihi, not), misafir listesi paneli, takvime ekle, QR bilet ve girişte okutma, fotoğraf
  yükleme galerisi, hediye/IBAN bilgisi, müzik, çok dilli ve paylaşım önizlemesi. "Düğün
  davetiyesi sitesi", "etkinlik sayfası", "RSVP", "konferans sitesi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Etkinlik & Davet Sitesi

İnsanların en çok sevdiği ve paylaştığı site türlerinden. Duygusal bir ürün: tipografi, fotoğraf ve hareket önemli,
ama misafir 70 yaşında ve telefonda — sadelik şart.

## Davet (düğün/nişan/doğum günü)

1. **Kapak**: isimler büyük ve zarif (serif başlık, bkz. `sky-web-fonts`), tarih, şehir; arka planda fotoğraf veya ince doku.
   İsteğe bağlı açılış animasyonu (zarf açılır, mühür kırılır) — reduced-motion'da atla.
2. **Geri sayım** ("42 gün 06:13:20", tabular-nums — bkz. `sky-date-time`).
3. **Program**: tören, kokteyl, yemek — saatlerle zaman çizelgesi.
4. **Konum**: mekân adı, adres, harita + "Yol tarifi" (Google/Apple/Yandex — bkz. `sky-maps-geo`), otopark bilgisi.
5. **LCV**: form (aşağıda).
6. **Hikâyemiz / galeri** (isteğe bağlı).
7. **Hediye**: IBAN (kopyala butonu, banka adı otomatik — bkz. `sky-tr-integrations`) veya hediye listesi bağlantısı.
8. **Takvime ekle** (.ics + Google), WhatsApp'ta paylaş.

## LCV / RSVP

```
Ad soyad · Katılıyor musunuz? (Evet / Hayır / Belki) · Kaç kişi? (1–5) · Menü tercihi (her kişi için) ·
Alerji/not · Telefon (isteğe bağlı) · [Gönder]
```
- Kişiye özel bağlantı (`/d/ABC123`) → ad önceden dolu, aile için kişi sınırı; genel bağlantı da olabilir.
- Gönderince sıcak teşekkür ekranı (+ konfeti, bkz. `sky-canvas`) ve "Takvime ekle".
- Cevabı değiştirme bağlantısı; son LCV tarihi.
- Bot koruması (honeypot + rate limit).

## Misafir paneli (sahipler için)

Katılım sayısı özeti (Evet 142 · Hayır 18 · Belki 9 · Yanıtsız 31), menü dağılımı, alerjiler listesi, CSV/Excel dışa aktar
(bkz. `sky-import-export`), hatırlatma SMS/WhatsApp (yanıt vermeyenlere), masa planı (sürükle-bırak, bkz. `sky-drag-drop`).
Basit parola veya magic link ile korumalı.

## Konferans / meetup

Konuşmacılar (fotoğraf, unvan, konu), program (salonlara göre sekmeli, "şu an" vurgusu, favorilere ekle), bilet türleri
(ücretsiz/ücretli — bkz. `sky-payments`), sponsorlar, SSS, ulaşım/konaklama, `Event` JSON-LD (bkz. `sky-seo`).

## QR bilet ve giriş

- Kayıt sonrası e-postada QR kodlu bilet (PDF + Apple/Google Wallet isteğe bağlı — bkz. `sky-print-pdf`).
- Girişte görevli telefonuyla tarama sayfası (kamera ile QR okuma `BarcodeDetector` / `@zxing`), anında "✓ Geçerli · Ayşe Yılmaz" veya "Zaten giriş yaptı" uyarısı, çevrimdışı çalışabilen liste.

## Etkinlik sonrası: fotoğraf galerisi

Misafirler QR ile galeri sayfasına girip fotoğraf yükler (giriş gerektirmeden, kısa kodla), sahipler onaylar, toplu indirme (ZIP).
EXIF temizliği ve KVKK notu (bkz. `sky-media`). İnsanların en çok sevdiği özelliklerden biri.

## Detaylar

- Arka plan müziği **otomatik çalmasın**; şık bir ♪ butonu.
- OG paylaşım kartı: isimler + tarih + fotoğraf (WhatsApp önizlemesi çok önemli).
- Çok dilli (yabancı misafirler) — bkz. `sky-i18n`.
- Etkinlikten sonra site "teşekkürler + galeri" moduna geçsin.
