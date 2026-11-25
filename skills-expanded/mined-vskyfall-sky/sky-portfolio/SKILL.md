---
name: sky-portfolio
description: >-
  Kişisel site ve portfolyo: geliştirici, tasarımcı, fotoğrafçı, yazar veya serbest çalışan
  için akılda kalan kişisel site; kişilik taşıyan hero, proje vaka çalışmaları (problem →
  süreç → sonuç), CV/özgeçmiş sayfası ve PDF, blog/notlar, "şu an" (now) sayfası, iletişim,
  OG kartları, küçük etkileşimli sürprizler (easter egg), koyu/açık tema, hız ve SEO. "Portfolyo
  sitesi", "kişisel web sitesi", "CV sitesi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Portfolyo

Portfolyo şablonlarının hepsi birbirine benzer; insanlar **kişiliği olan** siteyi hatırlar. Hedef: 10 saniyede
"kim, ne yapıyor, neden onunla çalışmalıyım" + bir tane akılda kalan detay.

## Yapı

- **Hero**: ad + tek cümle ("İstanbul'da yaşayan, erişilebilir arayüzler yapan frontend geliştirici") + 2 CTA (Projeler, İletişim).
  Jenerik "Merhaba, ben X 👋" yerine kişisel ses.
- **Seçili işler**: 3–6 proje; her biri kart (görsel, başlık, rol, 1 satır sonuç) → vaka çalışması sayfası.
- **Hakkında**: kısa hikâye, fotoğraf, değerler, araçlar (logo yığını değil, kısa liste).
- **Yazılar/notlar** (isteğe bağlı ama SEO ve güven için çok değerli).
- **İletişim**: e-posta (kopyala butonu), takvim bağlantısı (Cal.com), sosyal.

## Vaka çalışması şablonu

1. Bağlam (müşteri/proje, rolün, süre, ekip)
2. Problem (rakamla mümkünse)
3. Süreç (araştırma, kararlar, reddedilen alternatifler — düşünce tarzın burada görünür)
4. Çözüm (ekran görüntüleri/videolar, etkileşimli demo)
5. Sonuç (metrikler, alıntı)
6. Öğrendiklerim
Okuyucular sonucu görmek ister; başa 3 maddelik özet ("TL;DR") koy.

## Akılda kalan detaylar (birini seç, abartma)

- İmleç takip eden hafif efekt veya manyetik butonlar (reduced-motion'da kapalı).
- Konami kodu / `⌘K` komut paleti ile sürpriz (bkz. `sky-dashboard` palet).
- Spotify'da şu an çalan şarkı, GitHub katkı ısı haritası, yerel saat ("İstanbul'da şu an 14:32").
- Ziyaretçi sayacının modern hali, misafir defteri.
- `/now` sayfası (şu an ne üzerinde çalışıyorsun) — sıcak ve güncel.
- El yazısı imza SVG'si çizilerek belirir (bkz. `sky-motion-assets`).

## CV

`/cv` HTML sayfası + yazdırılabilir (print CSS, bkz. `sky-print-pdf`) + PDF indir. ATS dostu düz metin yapısı; tek sayfa hedef.

## Teknik

- Astro veya Next (SSG), MDX içerik (bkz. `sky-cms` MDX seçeneği), görseller optimize.
- Dinamik OG görselleri (her yazı/proje için başlıklı kart, bkz. `sky-seo`).
- Koyu/açık tema anahtarı (sistem tercihi varsayılan), `View Transitions` ile sayfa geçişleri (bkz. `sky-browser-apis`).
- Lighthouse 100'e yakın; analitik çerezsiz (Plausible/Umami).
- RSS, sitemap, `Person` JSON-LD.
- Çok dilli (TR/EN) ise `sky-i18n`.
