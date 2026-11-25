---
name: sky-docs-site
description: >-
  Dokümantasyon sitesi: Fumadocs / Starlight / Nextra / Mintlify seçimi, bilgi yapısı (başlangıç,
  rehberler, referans, örnekler — Diátaxis), MDX bileşenleri (uyarı kutuları, sekmeler, kod
  grupları, adımlar), arama (Algolia DocSearch/Orama), kod bloklarında kopyala ve dosya adı,
  API referansı (OpenAPI), sürümleme ve çok dil, "bu sayfa yardımcı oldu mu", llms.txt ve AI
  dostu dokümantasyon. "Dokümantasyon sitesi", "docs", "yardım merkezi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Dokümantasyon Sitesi

## Araç

| Durum | Seçim |
|---|---|
| Next.js projesi, esnek, güzel | **Fumadocs** |
| Astro, hızlı, çok dil yerleşik | **Starlight** |
| Barındırılan, API referansı güçlü, ekip düzenler | **Mintlify** |
| Basit Next.js | Nextra |
| Son kullanıcı yardım merkezi (SSS, makale) | Intercom/Crisp Help Center veya aynı araçlar |

## Bilgi yapısı (Diátaxis)

1. **Başlangıç** (tutorial): 5 dakikada ilk başarı — tek yol, kopyala-yapıştır adımlar.
2. **Nasıl yapılır** (how-to): görev odaklı rehberler ("Stripe ödemesi nasıl bağlanır").
3. **Referans**: API, yapılandırma seçenekleri, CLI — eksiksiz, kuru, aranabilir.
4. **Açıklama** (explanation): kavramlar, mimari, "neden böyle".
Karıştırma: rehberin içine 40 satırlık seçenek tablosu koyma, referansa bağla.

## Sayfa anatomisi

Başlık + 1 cümle ne öğreneceksin, ön koşullar, numaralı adımlar (`<Steps>`), kod blokları, sonuç/doğrulama
("Şunu görmelisin…"), sonraki adımlar bağlantıları. Sağda sayfa içi içindekiler, altta "Önceki / Sonraki".

## MDX bileşenleri (insanların sevdiği)

- `<Callout type="warning">` (bilgi/ipucu/uyarı/tehlike — renk + ikon), `<Tabs>` (npm/pnpm/bun sekmeleri — seçim tüm sayfada hatırlanır),
  kod bloğunda **dosya adı başlığı**, **kopyala butonu**, satır vurgulama (`{3-5}`), diff görünümü (`+`/`-`).
- `<Steps>`, `<Cards>` (bağlantı kartları), `<Accordion>`, `<FileTree>`, video gömme, etkileşimli canlı örnek (Sandpack/StackBlitz).
- Paket yöneticisi seçimi ve dil seçimi kullanıcı başına kalıcı.

## Arama

⌘K arama (Algolia DocSearch açık kaynak projelere ücretsiz, Orama/Pagefind yerel); sonuçlarda bölüm başlıkları;
arama sorgularını analiz et (bulunamayanlar = yazılacak sayfalar).

## API referansı

OpenAPI'den otomatik (Fumadocs OpenAPI, Scalar, Mintlify) — her uç nokta için örnek istek/yanıt, "Dene" konsolu,
çok dilli kod örnekleri (bkz. `sky-public-api`).

## Kalite

- "Bu sayfa yardımcı oldu mu? 👍 👎" + geri bildirim kutusu; "GitHub'da düzenle" bağlantısı.
- Son güncelleme tarihi; bozuk bağlantı kontrolü CI'da; kod örnekleri test edilir (doctest/örnek proje).
- Ekran görüntüleri yerine mümkünse metin + kod (güncel tutması kolay); gerekiyorsa koyu/açık versiyon.

## Sürüm ve dil

Sürüm seçici (v1/v2), eski sürüm bandı ("Eski sürümü görüntülüyorsun"); çok dil (TR/EN) için `sky-i18n`.

## AI dostu dokümantasyon

- `/llms.txt` (site haritası + kısa açıklamalar) ve `/llms-full.txt` (tüm içerik düz metin) — AI asistanları dokümanını doğru okur.
- Her sayfa için "Markdown olarak kopyala" / "ChatGPT/Claude'da aç" butonları — geliştiricilerin yeni favorisi.
- Temiz başlık yapısı, kısa paragraflar, tam kod örnekleri (eksik `...` yok).
