---
name: ui-tasarim
description: dusukbutce.com'un görsel tasarım/UX işlerinde kullan — düzen, renk, tipografi, tutarlılık, responsive, erişilebilirlik, marka görünümü. Kullanıcı "tasarım", "ui", "ux", "görünüm", "renk", "düzen" dediğinde.
---
# UI Tasarım rolü — dusukbutce.com

## En önemli kural
⚠️ **Kullanıcı açıkça istemeden mevcut tasarımı DEĞİŞTİRME.** Bir refactor/POC bile olsa, görsel değişiklik önce ekran görüntüsüyle gösterilip onay alınmadan uygulanmaz. (Bu, geçmişte yaşanmış bir hata — ram sayfası izinsiz değiştirilmişti.)

## Mevcut görünüm
- Stil **inline style** ile yazılıyor (Tailwind v4 kurulu ama kullanılmıyor). Yeni görsel iş mevcut desene uymalı; karışık sistem kullanma.
- Marka: `dusukbutce.com` logosu, mavi header, yeşil "BİZE SAT" CTA, kart tabanlı düzen. Kullanıcı metinleri **Türkçe**.
- Responsive: `isMobile` (window.innerWidth <= 768) deseni yaygın.
- Ana akışlar: ana sayfa (kategoriler + satılık ilanlar), bize-sat formları, teklif/teslimat, teknik servis.

## Yaklaşım
- Değişiklik önerini **önce görsel olarak sun** (ekran görüntüsü / mockup), sonra uygula.
- Tutarlılık: yeni bileşenler mevcut kart/buton/spacing diliyle uyumlu olsun.
- Erişilebilirlik: yeterli kontrast, tıklanabilir alan boyutu, form etiketleri.
- Light/dark: proje tek görünüm; gereksiz tema ekleme.

## Kontrol listesi
- [ ] Görsel değişiklik için kullanıcı onayı alındı mı?
- [ ] Mevcut stil sistemine (inline) uyumlu mu?
- [ ] Mobil + masaüstü kontrol edildi mi?
- [ ] Metinler Türkçe ve tutarlı mı?
- [ ] Değişiklik tarayıcıda ekran görüntüsüyle gösterildi mi?
