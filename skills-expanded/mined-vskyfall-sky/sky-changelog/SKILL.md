---
name: sky-changelog
description: >-
  Değişiklik günlüğü ve "Yenilikler": herkese açık changelog sayfası (görselli, kategorili),
  uygulama içi yenilikler paneli ve okunmamış rozeti, sürüm notu yazımı (kullanıcı dilinde
  fayda), semver ve sürümleme, Conventional Commits'ten otomatik CHANGELOG, e-posta ile duyuru,
  RSS ve yol haritası (roadmap) / özellik oylama sayfası. "Changelog", "yenilikler", "sürüm
  notları", "roadmap sayfası" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Changelog & Yenilikler

Kullanıcılar ürünün **yaşadığını** görmek ister. Düzenli, güzel bir changelog güven ve heyecan yaratır; satış ekibinin de en iyi aracıdır.

## Herkese açık changelog sayfası

```
/changelog
┌ 4 Kasım 2026 ──────────────────────────────┐
│ [Yeni] WhatsApp ile randevu hatırlatma      │  görsel/GIF/kısa video
│ Müşterilerin artık hatırlatmaları WhatsApp'tan alabilir. Açılma oranı SMS'ten… │
│ [İyileştirme] Takvim 2× daha hızlı açılıyor │
│ [Düzeltme] Excel içe aktarmada Türkçe karakter sorunu │
└────────────────────────────────────────────┘
```
- Her giriş: tarih, etiket (Yeni / İyileştirme / Düzeltme), **fayda odaklı başlık**, 1–3 cümle, görsel, "Nasıl kullanılır" bağlantısı.
- Kendi sayfası (SEO + paylaşım için `/changelog/whatsapp-hatirlatma`), OG kartı.
- RSS ve e-posta aboneliği.
- Kaynak: MDX dosyaları veya CMS (bkz. `sky-cms`).

## Sürüm notu yazımı

✗ "feat(notifications): add whatsapp channel adapter"
✓ "Randevu hatırlatmaları artık WhatsApp'tan da gidebilir. Ayarlar → Bildirimler'den aç."
- Kullanıcının kazancıyla başla, teknik detayı sona veya hiç.
- Teşekkür et: "Bu özelliği isteyen 34 kullanıcımıza teşekkürler" — insanlar duyulduğunu hisseder.

## Uygulama içi "Yenilikler"

- Sidebar/üst barda 🎁 veya "Yenilikler" + **okunmamış nokta**; açılınca son 5 giriş (panel/popover).
- Büyük özellikte bir kerelik modal (görsel + "Dene" butonu) — en fazla ayda bir.
- İlgili ekranda bağlamsal "Yeni" rozeti (1–2 hafta), bkz. `sky-onboarding` ipuçları.
- Okundu bilgisi kullanıcı başına sunucuda (`last_seen_changelog_at`).

## Teknik changelog

- Conventional Commits (`feat:`, `fix:`, `perf:`) → `changesets` veya `release-please` ile otomatik `CHANGELOG.md` + semver.
- Semver: MAJOR kırıcı, MINOR yeni özellik, PATCH düzeltme. Uygulama için tarih bazlı sürüm de olur (`2026.11.04`).
- API değişiklikleri ayrı bölüm (bkz. `sky-public-api` sürümleme).
- Teknik changelog ≠ kullanıcı changelog'u; ikisini de tut, kullanıcıya teknik olanı gösterme.

## Yol haritası ve özellik oylama

- `/roadmap`: Planlanan / Üzerinde çalışılıyor / Yayında sütunları (kanban görünümü), her öğede oy sayısı.
- Özellik isteği gönder + oy ver (giriş gerekli, kişi başı bir oy); yayınlandığında oy verenlere otomatik e-posta: "İstediğin özellik yayında!" — en sevilen e-posta türlerinden.
- Araçlar: Canny, Featurebase, Productboard veya basit kendi tablon.
- Tarih vaadi verme; "üzerinde çalışılıyor" yeter.
