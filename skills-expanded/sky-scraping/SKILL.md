---
name: sky-scraping
description: >-
  Etik ve sağlam web kazıma (scraping) ve veri toplama: önce resmi API/açık veri, robots.txt ve
  kullanım şartları, kişisel veri ve KVKK, kibar tarama (hız sınırı, User-Agent, önbellek), araç
  seçimi (fetch + cheerio, Playwright, Crawlee), dinamik sayfalar, sayfalama ve kuyruk, veri
  temizleme ve doğrulama, değişiklik izleme, zamanlama, kırılganlığı azaltma ve neyin yapılmaması
  gerektiği. "Siteden veri çek", "scraper yaz", "fiyat takibi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Web Kazıma

## Önce: yapmalı mıyım?

1. **Resmi API veya açık veri** var mı? (çoğu zaman var — daha güvenilir ve izinli)
2. **robots.txt** ve **kullanım şartları** kazımaya izin veriyor mu?
3. **Kişisel veri** topluyor muyum? (KVKK/GDPR: hukuki dayanak gerekir — isim, telefon, e-posta toplamak çoğu durumda sorunlu)
4. Telif/veritabanı hakları: içeriği yeniden yayınlamak ≠ fiyat/istatistik toplamak.
Yapılmaz: giriş gerektiren alanlara başkasının hesabıyla girmek, CAPTCHA/bot korumasını aşmak, ödeme duvarını delmek, sunucuyu yormak.
Emin olmadığın durumda kullanıcıya riski açıkça söyle.

## Kibar tarama

- Hız sınırı (ör. alan adı başına saniyede 1 istek), eşzamanlılık düşük, gece saatleri.
- Tanımlayıcı User-Agent + iletişim (`SkyBot/1.0 (+https://site.com/bot)`).
- Yanıtları önbelleğe al (aynı sayfayı tekrar çekme), `If-Modified-Since`/ETag kullan.
- 429/503'te geri çekil (`Retry-After`), 4xx'te tekrar deneme.

## Araç seçimi

| Sayfa türü | Araç |
|---|---|
| Statik HTML | `fetch` + **cheerio** (hızlı, hafif) |
| JS ile render edilen | **Playwright** (headless) — önce Network sekmesinde arka plandaki JSON API'yi ara (çoğu zaman daha kolay ve hafif) |
| Büyük tarama (kuyruk, yeniden deneme, oturum, depolama) | **Crawlee** (Cheerio/Playwright crawler) |
| Python | httpx + selectolax/BeautifulSoup, Scrapy (büyük ölçek) |

```ts
import * as cheerio from "cheerio";
const html = await (await fetch(url, { headers: { "User-Agent": UA }, signal: AbortSignal.timeout(10_000) })).text();
const $ = cheerio.load(html);
const items = $("[data-testid='product-card']").map((_, el) => ({
  title: $(el).find("h3").text().trim(),
  price: parsePrice($(el).find(".price").text()),     // "1.249,90 TL" → 124990 (kuruş)
  url: new URL($(el).find("a").attr("href")!, url).toString(),
})).get();
```

## Sağlamlık

- Seçiciler: anlamlı öznitelikler (`data-*`, `itemprop`, aria etiketleri, yapılandırılmış veri JSON-LD) → CSS sınıflarından daha kalıcı.
  JSON-LD/Open Graph varsa önce oradan oku.
- Her kaydı **şema ile doğrula** (Zod); boş/değişmiş alan oranı artınca alarm (site değişti).
- Ham HTML'i (veya özetini) sakla → ayrıştırıcı değişince yeniden işleyebilirsin.
- Sayfalama: "sonraki" bağlantısını izle, üst sınır koy, ziyaret edilen URL kümesi (sonsuz döngü yok).

## Veri temizleme

Türkçe para/tarih biçimlerini normalize et (`1.249,90` → 1249.90; "5 Kas 2026" → ISO), boşlukları/HTML varlıklarını temizle, birimleri ayır, tekilleştir
(bkz. `sky-import-export`, `sky-date-time`).

## Zamanlama ve izleme

Cron/arka plan işi (bkz. `sky-jobs`); değişiklik tespiti (fiyat düştü → bildirim — insanların en sevdiği kullanım); başarısızlık oranı ve
"0 kayıt döndü" alarmı (bkz. `sky-observability`).
