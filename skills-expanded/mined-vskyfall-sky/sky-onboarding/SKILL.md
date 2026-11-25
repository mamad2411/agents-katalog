---
name: sky-onboarding
description: >-
  Kullanıcı aktivasyonu ve ilk deneyim: "aha anı"nı tanımlama, kayıt sonrası akış, kişiselleştirme
  soruları, kurulum kontrol listesi (checklist), örnek veri ile başlatma, boş durumlar,
  bağlamsal ipuçları ve ürün turu, ilerleme kutlamaları, hoş geldin e-posta dizisi, aktivasyon
  metrikleri ve terk noktaları. "Kullanıcılar kayıt olup gidiyor", "onboarding", "ilk kullanım",
  "kurulum sihirbazı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Onboarding

## 1. Aha anını tanımla

Kullanıcının ürünün değerini **ilk hissettiği** eylem: randevu sistemi → "ilk online randevu geldi";
fatura uygulaması → "ilk fatura gönderildi"; ekip aracı → "ilk ekip arkadaşı katıldı".
Onboarding'in tek hedefi: kullanıcıyı **en kısa sürede** oraya götürmek. Ölçüt: kayıttan aha'ya geçen süre ve oran.

## 2. Kayıt → değer, sürtünmesiz

- Kayıt formunda minimum alan (e-posta veya Google ile giriş). Diğer bilgileri sonra, ihtiyaç anında iste.
- Kart bilgisi istemeden deneme (dönüşüm daha yüksek).
- Kayıttan sonra boş panele değil, **ilk adıma** yönlendir.

## 3. Kişiselleştirme (2–3 soru, isteğe bağlı)

"Ne tür işletmesin?" (Kuaför / Klinik / Danışman…), "Ekipte kaç kişi var?", "Öncelikle ne yapmak istiyorsun?"
→ cevaba göre varsayılan hizmetler, şablonlar, ipuçları. Kullanıcıya "bu ürün benim için yapılmış" hissi verir.
Atla seçeneği her zaman.

## 4. Kurulum kontrol listesi

```
Hesabını hazırla  ███████░░░ 3/5
✓ İşletme bilgilerini ekle
✓ İlk hizmetini oluştur
✓ Çalışma saatlerini ayarla
○ Rezervasyon bağlantını paylaş   →  [Bağlantıyı kopyala]
○ İlk randevunu al  🎉
```
- 3–6 madde, ilk 1–2 madde **önceden tamamlanmış** (kayıt) → başlama motivasyonu (ilerleme etkisi).
- Her maddede doğrudan eylem butonu; tamamlanınca anlık ✓ animasyonu.
- Kapatılabilir ama sidebar'da küçük ilerleme halkası olarak kalır.
- Hepsi bitince kutlama (konfeti, bkz. `sky-canvas`) ve kontrol listesi kaybolur.

## 5. Örnek veri

"Örnek verilerle keşfet" → demo müşteriler/randevularla dolu panel (açıkça "Örnek" etiketli, tek tıkla temizlenir).
Boş bir ürünün değerini hayal etmek zordur; dolu hali hemen anlatır.

## 6. Boş durumlar = onboarding

Her boş ekran bir eğitim fırsatı: ne işe yarar + ilk eylem + (ops.) 30 sn'lik video/GIF (bkz. `sky-ux-writing`,
`sky-states-library`).

## 7. Bağlamsal ipuçları ve tur

- Uzun ürün turu (10 adımlık "İleri › İleri") **yapma** — kimse okumaz.
- Bunun yerine: ilgili özelliğe ilk gelindiğinde tek bir ipucu balonu (hotspot), "Anladım" ile kapanır, bir daha çıkmaz.
- Kütüphane: Driver.js / Onborda / kendi Popover'ın; durumu sunucuda sakla (cihazlar arası).
- Yeni özellik duyurusu için aynı mekanizma + "Yenilikler" (bkz. `sky-changelog`).

## 8. Kutlamalar ve ilerleme

İlk randevu, 10. müşteri, ilk ödeme → küçük kutlama mesajı (abartmadan, bkz. `sky-gamification`). Kullanıcıya
"doğru gidiyorsun" sinyali.

## 9. E-posta dizisi (davranışa göre)

- Gün 0: hoş geldin + tek eylem ("Rezervasyon bağlantını paylaş").
- Gün 1: adımı tamamlamadıysa ipucu; tamamladıysa sonraki adım.
- Gün 3: başarı hikâyesi / kısa video.
- Gün 7: hâlâ aktive olmadıysa kişisel e-posta ("Yardım edebilir miyim?" — kurucudan, düz metin).
Akış tetikleyicileri `sky-jobs` (Inngest adımlı akış örneği), gönderim `sky-notifications`.

## 10. Ölçüm

Huni: kayıt → profil → ilk hizmet → bağlantı paylaşıldı → ilk randevu. Her adımın dönüşümü ve süresi
(bkz. `sky-observability` olay adları). En büyük düşüş noktasını iyileştir, sonra bir sonrakini.
