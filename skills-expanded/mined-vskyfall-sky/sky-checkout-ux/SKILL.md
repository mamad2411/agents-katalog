---
name: sky-checkout-ux
description: >-
  Türkiye'ye uygun ödeme akışı: il/ilçe adres formu, taksit, havale, kapıda ödeme, 3D Secure
  beklemesi, sepet terki. "Ödeme sayfası", "checkout" dendiğinde kullan.
---

# Sky · Checkout UX

Ödeme entegrasyonu `sky-payments`, sepet/sipariş modeli `sky-ecommerce`'de. Burada **akışın hissi**.

## Yapı

- **Tek sayfa, bölümlü** (iletişim → teslimat → kargo → ödeme) masaüstünde; mobilde aynı sıra, bölümler katlanır.
- Sağda (mobilde üstte katlanabilir) **sipariş özeti**: ürün görselleri, adet, ara toplam, kargo, indirim, KDV dahil toplam.
- Checkout'ta site menüsü ve footer gizli (odak); logo ana sayfaya değil sepete dönsün.
- İlerleme hissi: bölüm başlıklarında ✓.

## Misafir ödeme

Hesap oluşturmayı zorunlu kılma (en büyük terk sebeplerinden). E-posta ile devam → siparişten sonra
"Şifre belirle, siparişini takip et" tek tık hesap.

## İletişim ve adres

- E-posta + telefon (kargo için); `autocomplete` öznitelikleri tam (bkz. `sky-mobile-ux`).
- Adres: il → ilçe → mahalle bağımlı seçim, adres satırı, posta kodu otomatik (bkz. `sky-maps-geo`).
- Kayıtlı adresler kart olarak seçilir; "Fatura adresi teslimat adresiyle aynı" varsayılan işaretli.
- Kurumsal fatura seçeneği: firma unvanı, VKN, vergi dairesi (bkz. `sky-tr-integrations`).

## Kargo seçimi

Seçenek kartları: firma logosu, tahmini teslim ("Perşembe 6 Kasım'da kapında"), ücret; ücretsiz kargo eşiğine ne kaldığı.
Tarih göstermek "2–4 iş günü"nden daha ikna edicidir.

## Kupon

"İndirim kodun var mı?" bağlantısı → tıklanınca alan açılır (her zaman açık büyük alan, kodu olmayanları kod aramaya
gönderir). Uygulanınca özet anında güncellenir, kaldır (×) seçeneği; hata: "Bu kodun süresi 1 Kasım'da doldu."

## Ödeme yöntemleri

- Kart (sağlayıcı formu/iframe), **taksit tablosu** (kart BIN'ine göre, "3 × ₺333,33"), havale/EFT (IBAN kopyala butonu + açıklama kodu), kapıda ödeme (ek ücret açıkça), dijital cüzdanlar.
- Kart alanında kart türü logosu otomatik (Visa/Mastercard/Troy), boşluklu biçim, son kullanma `AA/YY`, CVC yardım tooltip'i.
- Kayıtlı kartlar (sağlayıcı tokenizasyonu ile) — tekrar alışverişte tek tık.

## Gönder butonu

"₺1.249,90 Öde" — tutar butonda. Tıklanınca devre dışı + "Ödeme işleniyor…"; çift tıklama engelli (bkz. `sky-payments` idempotency).
Yasal: mesafeli satış sözleşmesi ve ön bilgilendirme formu onay kutusu (metinleri modalda göster).

## 3D Secure

Banka sayfasına/iframe'e geçişte açıklama: "Bankanın doğrulama ekranına yönlendiriliyorsun. SMS kodunu gir."
Dönüşte bekleme ekranı ("Ödemen doğrulanıyor…"), sayfayı kapatma uyarısı.

## Hata kurtarma

- Kart reddi → anlaşılır neden ("Kart limitin yetersiz olabilir" / "Bankan işlemi onaylamadı") + başka kart / başka yöntem seçenekleri; **form verileri silinmez**.
- Zaman aşımı → durum belirsizse önce sunucudan sorgula, kullanıcıya "Ödemen alındıysa e-posta gelecek; tekrar deneme" gibi net yönlendirme (çift çekimi önle).

## Güven işaretleri

SSL/güvenli ödeme rozeti (sağlayıcı logosu), iade/değişim politikası özeti, iletişim (telefon/WhatsApp), gerçek yorum puanı.
Sahte "%100 güvenli" rozetleri değil, gerçek bilgi.

## Başarı sayfası

Büyük ✓, sipariş numarası, teslim tarihi tahmini, e-posta onayı bilgisi, sipariş özeti, "Siparişi takip et",
hesap oluşturma teklifi (misafirse), paylaş/öner (isteğe bağlı). Peak-end etkisi: son an güzel olsun (bkz. `sky-ux-heuristics`).

## Terk azaltma

Sürpriz maliyet yok (kargo ve KDV erkenden görünür), az alan, misafir ödeme, hızlı sayfa, mobil uyum, birden çok ödeme yöntemi,
sepeti kaydet (e-posta bıraktıysa terk edilmiş sepet e-postası, bkz. `sky-ecommerce`). Huni analitiği: her bölümün tamamlanma oranı.
