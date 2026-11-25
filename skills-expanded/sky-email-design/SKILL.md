---
name: sky-email-design
description: >-
  HTML e-posta tasarımı ve kodlaması: react-email / MJML ile tablolu düzen, e-posta istemcisi
  farkları (Outlook, Gmail, Apple Mail), dark mode e-posta, web fontları ve fallback, görsel
  ve alt metin, kurşun geçirmez (bulletproof) buton, ön başlık (preheader), mobil uyum,
  işlemsel ve bülten şablonları, erişilebilirlik ve test (Litmus, Email on Acid). "E-posta
  şablonu tasarla", "bülten", "e-posta Outlook'ta bozuk", "güzel bir onay e-postası" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · E-posta Tasarımı

Gönderim altyapısı `sky-notifications`'ta; burada e-postanın **görünüşü ve kodu**.

## Gerçekler

- E-posta istemcileri 2005 tarayıcısı gibi davranır: **tablo düzeni**, satır içi stiller, sınırlı CSS.
- Outlook (Windows) Word motoru kullanır: `margin`, `background-image`, `border-radius` sınırlı.
- Gmail `<style>` bloklarını kısmen destekler, 102KB üstünü kırpar ("Mesajın tamamını görüntüle").
- Bu yüzden elle yazma: **react-email** (React bileşenleri) veya **MJML** kullan; doğru tablo HTML'ini üretirler.

## Düzen

- Genişlik 600px tek sütun (mobilde %100); kenar boşluğu 24px.
- Yapı: logo (küçük) → başlık → 1–3 kısa paragraf → **tek** birincil buton → ikincil bilgi → footer.
- Footer: şirket adı ve adresi, neden bu e-postayı aldığın, tercihler/abonelikten çık (pazarlamada zorunlu).

## Buton (kurşun geçirmez)

react-email `<Button>` VML fallback'li buton üretir; elle yapıyorsan dolgulu `<a>` + tablo hücresi (görsel buton değil —
görseller kapalıyken buton kaybolur). Min 44px yükseklik, net fiil: "Randevunu görüntüle".

## Tipografi ve font

- Web fontu (Google Fonts `<link>`) Apple Mail/iOS'ta çalışır, Gmail/Outlook'ta çalışmaz → her zaman güvenli yığın:
  `font-family: Inter, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.
- Gövde 16px, satır yüksekliği 1.5; Türkçe karakterler UTF-8 (`<meta charset="utf-8">`).

## Dark mode

- Apple Mail ve Outlook bazı modlarda renkleri **ters çevirir** (zorla).
- `<meta name="color-scheme" content="light dark">` + `@media (prefers-color-scheme: dark)` stilleri (destekleyenlerde).
- Logo: şeffaf PNG koyu zeminde kaybolur → logoya ince açık kenar/arka plan veya dark-mode versiyonu.
- Saf siyah metin / saf beyaz zemin yerine hafif kırık tonlar ters çevirmede daha iyi sonuç verir.

## Görseller

- Mutlak HTTPS URL, `width`/`height` öznitelikleri, anlamlı `alt` (görseller varsayılan kapalı istemciler çok).
- Metin görselin içinde değil HTML'de (erişilebilirlik + spam filtresi).
- Görsel/metin oranı dengeli; tek büyük görsel e-postası spam'e düşer.
- GIF animasyonu ilk karesi tek başına anlamlı olsun (Outlook ilk kareyi gösterir).

## Preheader

Konu satırının yanında görünen önizleme metni: `<Preview>` ile; konuyu tekrarlama, tamamla
("5 Kasım 14:30 · Kadıköy şubesi · İptal için bağlantı içeride"). Gizli dolgu ile istemcinin gövdeden metin çekmesini engelle.

## İnsanların sevdiği işlemsel e-postalar

- **Randevu onayı**: büyük tarih/saat bloğu, adres + harita bağlantısı, "Takvime ekle" (.ics ek + Google bağlantısı), "Ertele / İptal".
- **Sipariş/makbuz**: kalemler tablosu (sayılar sağa hizalı), toplamlar, fatura PDF bağlantısı, kargo takip butonu.
- **Hoş geldin**: kurucudan kısa, kişisel ton, tek eylem.
- **Parola sıfırlama**: sade, büyük buton, süre bilgisi, "Sen istemediysen yok say".
- **Haftalık özet**: 3 metrik kartı (bu hafta / geçen hafta), en önemli 3 olay, panele git butonu.

## Erişilebilirlik

`<html lang="tr">`, `role="presentation"` düzen tablolarında, mantıklı okuma sırası, yeterli kontrast,
bağlam bağımsız bağlantı metinleri, yalnızca görselden oluşan e-posta yok.

## Test

react-email önizleme sunucusu (`email dev`) → Litmus / Email on Acid ile istemci ekran görüntüleri (Outlook 2019/365,
Gmail web/Android/iOS, Apple Mail light/dark) → gerçek gönderimle Gmail ve Outlook.com'da kontrol → spam puanı (mail-tester.com).
