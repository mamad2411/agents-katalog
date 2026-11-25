---
name: sky-handoff
description: >-
  Projeyi müşteriye veya başka ekibe teslim etme: teslim paketi (erişimler, hesaplar, alan adı,
  barındırma, ödeme ve e-posta sağlayıcıları sahipliği), README ve işletim kılavuzu, env ve
  sırların güvenli devri, içerik düzenleme rehberi ve kısa eğitim videosu, bakım planı ve
  SLA, garanti süresi, son kontrol listesi ve kabul tutanağı. "Projeyi müşteriye teslim
  edeceğim", "devir", "bakım anlaşması", "freelance proje bitti" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Teslim

İyi teslim, müşterinin "bir sorun olursa ne yapacağım?" korkusunu bitirir ve sonraki işi getirir.

## 1. Sahiplik (en kritik)

Hesaplar **müşterinin** adına açılmış olsun (veya teslimde devredilsin); sen yalnızca davetli üye ol:
- [ ] Alan adı (registrar) — müşteri hesabında, otomatik yenileme açık
- [ ] Barındırma (Vercel/Netlify/VPS) — müşteri takımı, sen üye
- [ ] Veritabanı (Supabase/Neon) — müşteri organizasyonu
- [ ] E-posta gönderimi (Resend/Postmark), SMS (Netgsm), ödeme (iyzico/Stripe — **mutlaka müşteri adına**)
- [ ] Google İşletme, Search Console, Analytics — müşteri sahip, sen yönetici
- [ ] GitHub reposu — müşteri org'unda veya transfer
- [ ] Sentry, uptime izleme, durum sayfası
Kredi kartı müşterinin. Hiçbir kritik hesap kişisel e-postanda kalmasın.

## 2. Sırlar

Env değerlerini e-posta/WhatsApp ile gönderme. Parola yöneticisinin paylaşımlı kasası (1Password/Bitwarden) veya
platform üzerinde doğrudan müşteri ekler. Teslimden sonra senin kullandığın anahtarları döndür.

## 3. Dokümanlar

- **README**: ne, nasıl çalıştırılır, nasıl deploy edilir, mimari özet (bkz. `sky-architecture-docs` kalıbı).
- **İşletim kılavuzu** (`docs/operations.md`): yedekler nerede ve nasıl geri yüklenir, alarmlar kime gider, sık sorunlar ve çözümleri, kim aranır.
- **CLAUDE.md** (bkz. `sky-claude-md`) — sonraki geliştirici (veya AI) hızlı başlasın.
- **Env listesi** (`docs/ENV.md`): ad, amaç, nereden alınır.

## 4. Müşteri eğitimi

- 1 sayfalık "İçeriğini nasıl düzenlersin" rehberi (ekran görüntülü, Türkçe): giriş, metin/görsel değiştir, yeni sayfa/hizmet ekle, yayınla.
- 3–5 dakikalık ekran videoları (Loom) — her ana görev için bir tane. Müşteriler yazılı rehberden çok videoyu izler.
- 30 dakikalık canlı tanıtım + soru-cevap.

## 5. Son kontrol (`/sky:sky-check` + aşağısı)

- [ ] Prod'da test verisi/test kullanıcısı yok; test ödeme anahtarı yok
- [ ] İletişim formları müşterinin e-postasına gidiyor (test edildi)
- [ ] Yasal sayfalar ve çerez onayı yerinde, KVKK metinleri müşteriden/hukukçudan
- [ ] Yedekler çalışıyor ve bir kez geri yükleme denendi
- [ ] Lighthouse, erişilebilirlik ve SEO raporları ekte
- [ ] Hata izleme ve uptime alarmları müşterinin (ve bakımdaysa senin) e-postasına

## 6. Bakım ve garanti

- Garanti süresi (ör. 30 gün): kapsam (hatalar) ve kapsam dışı (yeni özellik).
- Bakım paketi: aylık bağımlılık güncellemeleri, güvenlik yamaları, yedek kontrolü, uptime takibi, X saat küçük değişiklik, yanıt süresi.
- Değişiklik talebi süreci (e-posta/form → tahmin → onay).

## 7. Kabul

Teslim tutanağı: teslim edilenler listesi, erişimlerin devredildiği, bilinen kısıtlar, garanti başlangıcı. İmza/onay e-postası.
Teşekkür + "memnun kaldıysanız Google yorumu / referans" ricası.
