---
name: sky-auth-ux
description: >-
  Giriş ve kayıt ekranlarının UX'i: tek ekran e-posta önce akışı, sosyal giriş butonları
  sırası ve tasarımı, passkey önerisi, magic link bekleme ekranı ("e-postanı kontrol et"),
  OTP kod girişi (otomatik doldurma, yapıştırma, 6 kutu), parola alanı (göster/gizle, güç
  göstergesi), hata metinleri, "beni hatırla", parola sıfırlama akışı, kayıt sonrası yönlendirme
  ve güven unsurları. "Giriş sayfası tasarla", "kayıt formu", "OTP ekranı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Giriş & Kayıt UX'i

Güvenlik kuralları `sky-auth`'ta; burada **hissiyat ve akış**.

## Düzen

- Ortalanmış dar kart (max 400px) veya bölünmüş ekran (sol form, sağ marka görseli/yorum — masaüstünde).
- Logo, tek başlık ("Tekrar hoş geldin" / "Hesap oluştur"), kısa alt metin.
- Giriş ↔ kayıt geçiş bağlantısı altta ("Hesabın yok mu? Kaydol").
- Gereksiz menü/footer yok; dikkat formda.

## E-posta önce akışı

1. Sosyal butonlar (Google, Apple; B2B'de Microsoft) **üstte**, ardından "veya" ayracı.
2. E-posta alanı → "Devam" → sistem hesabın türüne göre: parola alanı, magic link veya SSO yönlendirmesi.
Tek ekranda giriş ve kayıt birleşebilir ("E-postanı gir" → yoksa kayıt adımına geç) — bilgi sızdırmamak için
kayıtta da "doğrulama bağlantısı gönderdik" mesajı (bkz. `sky-auth`).

## Sosyal butonlar

- Sağlayıcının resmi logosu ve marka kuralları (Google: beyaz/koyu tema varyantları, "Google ile devam et").
- Tam genişlik, aynı boyut, simge solda; en çok kullanılan üstte (TR tüketici: Google; iOS ağırlıklı kitle: Apple).
- 3'ten fazla sağlayıcı karar yorgunluğu yaratır.

## Passkey

E-posta alanında `autocomplete="username webauthn"` → tarayıcı kayıtlı passkey'i önerir (conditional UI); giriş
sonrası "Bir dahaki sefere parmak izinle gir" teklifi (bkz. `sky-browser-apis`). Kullanıcılar bu hızı çok sever.

## Magic link bekleme ekranı

"📬 E-postanı kontrol et — **ayse@ornek.com** adresine giriş bağlantısı gönderdik."
- Gmail/Outlook'u aç butonları (e-posta alanından tahminle) — küçük ama çok sevilen detay.
- "Gelmedi mi? Spam klasörüne bak · 30 sn sonra tekrar gönder" (geri sayımlı).
- "Farklı e-posta kullan" bağlantısı. Bağlantı açılınca diğer sekme de otomatik giriş yapsın (BroadcastChannel/polling).

## OTP kod girişi

```html
<input inputmode="numeric" autocomplete="one-time-code" pattern="\d{6}" maxlength="6">
```
- Görsel olarak 6 kutu ama **tek gerçek input** (input-otp kütüphanesi) → yapıştırma ve SMS otomatik doldurma çalışır.
- 6. hane girilince otomatik gönder; hata olursa kutular sallanır + temizlenir.
- iOS/Android SMS'ten otomatik doldurma: SMS şablonunun sonunda `@site.com #123456` (WebOTP biçimi) Android Chrome'da tek dokunuşla doldurur.
- Yeniden gönder geri sayımı, numarayı düzenle bağlantısı.

## Parola alanı

- Göster/gizle (göz ikonu, `aria-label="Parolayı göster"`), `autocomplete="current-password"` / `new-password`.
- Kayıtta güç göstergesi (zxcvbn) ve kural listesi canlı ✓ (karmaşık kural yerine uzunluk + sızıntı kontrolü).
- Caps Lock açık uyarısı (`getModifierState("CapsLock")`).
- Parola tekrar alanı yerine göster/gizle yeterli.

## Hata metinleri

- "E-posta veya parola hatalı." (hangisi olduğunu söyleme)
- "Çok fazla deneme yaptın. 5 dakika sonra tekrar dene." (süre söyle)
- "Bu bağlantının süresi dolmuş. Yeni bağlantı gönderelim mi? [Gönder]" (çıkış yolu sun)
- Alan altında, kırmızı + ikon; genel hatalar formun üstünde.

## Diğer

- "Beni hatırla" yerine varsayılan uzun oturum + "Tüm cihazlardan çık" ayarı (çoğu ürün için).
- Kayıt sonrası doğrudan onboarding'in ilk adımına (bkz. `sky-onboarding`), boş panele değil.
- Davetle gelen kullanıcıda e-posta önceden dolu ve kilitli, "Acme Kliniği'ne katılıyorsun" bağlamı.
- Güven: gizlilik politikası bağlantısı, KVKK onayı kayıtta (ön işaretsiz), "Kartın istenmez".
- Klavye: Enter ile gönderim, otomatik odak ilk alanda, sekme sırası doğru.
