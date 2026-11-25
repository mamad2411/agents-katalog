---
name: sky-launch
description: >-
  Ürün lansmanı (teknik + iletişim): bekleme listesi ve davet sistemi (referans ile sırada
  yükselme), lansman günü trafik dayanıklılığı, Product Hunt / Hacker News / sosyal medya
  hazırlığı, lansman sayfası ve OG kartları, basın kiti, durum sayfası, destek kanalı,
  analitik huniler, ilk 100 kullanıcı taktikleri ve lansman sonrası ilk hafta. "Lansman
  yapacağız", "bekleme listesi", "Product Hunt", "yayına çıkıyoruz" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Lansman

## Lansmandan önce: bekleme listesi

- Tek alanlı form (e-posta) + "Sıradaki yerin: #1.248".
- **Referans döngüsü**: kişiye özel bağlantı; her davet eden sırada 10 basamak yükselir — "3 arkadaşını davet et, erken erişim kazan".
  Paylaş butonları (WhatsApp, X, LinkedIn, kopyala). İnsanlar sırada yükselmeyi oyun gibi sever (Robinhood kalıbı).
- Onay e-postası (çift onay, bkz. `sky-notifications`), güncelleme e-postaları (2 haftada bir, kısa, ekran görüntülü).
- Dalgalar halinde davet: "Erken erişimin açıldı 🎉" + davet kodu (bkz. `sky-feature-flags` beta).
- Veri modeli: `waitlist(email, ref_code, referred_by, position, invited_at)`; bot/sahte e-posta filtreleme.

## Teknik hazırlık (lansman günü çökme korkusu)

- [ ] Statik sayfalar CDN'de; landing SSG
- [ ] Yük testi: beklenen trafiğin 5×'i (bkz. `sky-perf`, k6 ile basit senaryo)
- [ ] DB bağlantı havuzu, rate limit'ler, önbellek (bkz. `sky-caching`)
- [ ] Kayıt akışı uçtan uca test (e-posta teslimatı dahil, spam klasörü kontrolü)
- [ ] Ödeme canlı modda test edildi (gerçek kartla küçük tutar + iade)
- [ ] Sentry, uptime, durum sayfası (bkz. `sky-observability`), alarmlar ekip telefonunda
- [ ] Feature flag ile kapatılabilir riskli özellikler; bakım modu hazır (bkz. `sky-resilience`)
- [ ] Destek kanalı: e-posta + canlı sohbet (bkz. `sky-chat-product`), hazır yanıtlar
- [ ] Yedekler doğrulandı

## İletişim varlıkları

- Lansman sayfası/landing (bkz. `sky-landing`), dinamik OG kartları.
- 30–60 sn demo videosu (sessiz izlenebilir, altyazılı), 3–5 ekran görüntüsü, GIF.
- **Basın kiti** (`/press` veya `/marka`): logo, ekran görüntüleri, kurucu fotoğrafları, kısa/uzun açıklama, iletişim (bkz. `sky-brand`).
- Product Hunt: tagline (≤ 60 karakter), açıklama, galeri, ilk yorum (kurucu hikâyesi), lansman günü 00:01 PST, destekçilere önceden haber (oy istemek yerine "yorum ve geri bildirim" iste).
- Türkiye: LinkedIn kurucu paylaşımı, X, Ekşi/Webrazzi/Startups.watch, ilgili Discord/Telegram toplulukları, hedef kitle WhatsApp grupları.

## Lansman günü

- Tek bir "savaş odası" kanalı; panoda canlı metrikler (kayıt/saat, hata oranı, p95).
- Her yoruma/soruya hızlı ve kişisel cevap.
- Kritik hata → feature flag kapat / geri al; mükemmel değil çalışır olsun.
- Gün sonunda teşekkür paylaşımı ve rakamlar.

## İlk hafta

- Her yeni kullanıcıya kurucudan kişisel e-posta ("Neden kaydoldun? Ne arıyordun?").
- Aktivasyon hunisini izle (bkz. `sky-onboarding`), en büyük düşüşü düzelt.
- Geri bildirimleri changelog'a dönüştür ("Lansmandan beri 14 iyileştirme", bkz. `sky-changelog`).
- İlk 10 ödeme yapan müşteriyle görüşme.
