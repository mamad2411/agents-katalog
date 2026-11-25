---
name: sky-i18n
description: >-
  Çok dillilik, öncelikle Türkçe/İngilizce: Türkçe İ/ı ve büyük harf tuzakları, ekler, Türkçe
  sıralama, Intl ile tarih/para biçimi. "Çok dilli yap", "Türkçe büyük harf sorunu" dendiğinde kullan.
---

# Sky · Uluslararasılaştırma (i18n)

## Mimari (Next.js + next-intl varsayılan)

```
src/
  i18n/
    routing.ts      # locales: ["tr", "en"], defaultLocale: "tr", localePrefix: "as-needed"
    request.ts      # getRequestConfig → messages/{locale}.json yükle
    navigation.ts   # Link, useRouter, usePathname (locale farkında)
  messages/
    tr.json
    en.json
  app/[locale]/layout.tsx   # <html lang={locale}>, NextIntlClientProvider
  proxy.ts (middleware.ts) # createMiddleware(routing) — locale tespiti ve yönlendirme
```
- `localePrefix: "as-needed"` → varsayılan dil ön eksiz (`/hakkimizda`), diğerleri `/en/about`.
- Yol çevirisi gerekiyorsa `pathnames` haritası (`/about: { tr: "/hakkimizda", en: "/about" }`).
- Sunucuda `getTranslations()`, istemcide `useTranslations()`; istemciye yalnızca gereken namespace'i gönder.
- SPA (Vite) için `react-i18next` veya `@lingui`; aynı ilkeler.

## Mesaj dosyaları

```json
{
  "Appointment": {
    "title": "Randevu al",
    "slots": "{count, plural, =0 {Uygun saat yok} one {# uygun saat} other {# uygun saat}}",
    "greeting": "Merhaba {name}",
    "updated": "Son güncelleme: {date, date, medium}",
    "price": "{amount, number, ::currency/TRY}"
  }
}
```
- Anahtarlar **anlam** söyler (`submitButton`), İngilizce metnin kopyası değil.
- Namespace = bileşen/sayfa. Ortak metinler `Common` altında (`save`, `cancel`, `loading`).
- ICU MessageFormat: `plural`, `select`, `selectordinal`; **string birleştirme yok**
  (`t("hello") + name` ✗ → `t("hello", { name })` ✓). Kelime sırası dilden dile değişir.
- Zengin metin: `t.rich("terms", { link: (chunks) => <Link href="/terms">{chunks}</Link> })`.
- Eksik anahtar → dev'de görünür uyarı; prod'da fallback dil. CI'da `tr.json` ve `en.json`
  anahtar kümelerini karşılaştıran bir test.

## Biçimlendirme: Intl her zaman

```ts
new Intl.DateTimeFormat("tr-TR", { dateStyle: "long" }).format(d);        // 3 Kasım 2026
new Intl.NumberFormat("tr-TR", { style: "currency", currency: "TRY" }).format(1234.5); // ₺1.234,50
new Intl.RelativeTimeFormat("tr", { numeric: "auto" }).format(-1, "day");  // dün
new Intl.ListFormat("tr", { type: "conjunction" }).format(["elma", "armut"]); // elma ve armut
new Intl.PluralRules("tr").select(3); // "other" — Türkçe'de sayıdan sonra çoğul eki yok
```
- Türkçe: ondalık virgül, binlik nokta, tarih `gg.aa.yyyy`, 24 saat, para birimi önde `₺` veya sonda `TL`
  (projede tek biçim seç). Haftanın ilk günü pazartesi.
- Sunucu ve istemci aynı locale ile biçimlendirsin; aksi halde hydration uyumsuzluğu.
  Tarihleri **UTC ISO** olarak taşı, gösterimde kullanıcı saat dilimine (`timeZone: "Europe/Istanbul"`) çevir.
- `next-intl` `useFormatter()` bunların sarmalayıcısı; doğrudan `toLocaleDateString()` string arg'sız kullanma.

## Türkçe'ye özgü tuzaklar

- **İ/ı sorunu:** `"istanbul".toUpperCase()` → `"ISTANBUL"` (yanlış); `toLocaleUpperCase("tr-TR")` → `"İSTANBUL"`.
  CSS `text-transform: uppercase` de `lang="tr"` ile doğru çalışır — `<html lang>` şart.
  Karşılaştırma/arama normalize ederken `toLocaleLowerCase("tr-TR")` kullan; `"I".toLowerCase()` ≠ `"ı"`.
- **Ekler:** `{name}'ın` gibi dinamik ek yazma (Ayşe'nin / Ali'nin / Umut'un). Cümleyi yeniden kur:
  "Ayşe için sipariş" veya "Sipariş sahibi: Ayşe".
- **Çoğul:** "3 öğe", "3 öğeler" değil. `plural` kuralı `other` tek dal.
- **Sıralama:** `arr.sort((a, b) => a.localeCompare(b, "tr"))` — ç, ğ, ı, ö, ş, ü doğru yere gider.
  Postgres'te `collate "tr-TR-x-icu"`.
- **Slug:** URL için `ş→s, ç→c, ğ→g, ı→i, ö→o, ü→u, İ→i`; `slugify` kütüphanesine Türkçe harita ver.
- **Fontlar:** `latin-ext` alt kümesi yoksa ğ/ş/İ fallback fonta düşer. `next/font` `subsets: ["latin", "latin-ext"]`.
- **Metin uzunluğu:** Türkçe çeviriler İngilizce'den ~%20–30 uzun; butonlara sabit genişlik verme, `min-width` ver.

## Locale değiştirici

- `<select>` veya menü; mevcut yolu koruyarak değiştir (`usePathname` + `router.replace(pathname, { locale })`).
- Dil adlarını **kendi dilinde** yaz: "Türkçe", "English" (çevirisi değil).
- Tercih çerezde (`NEXT_LOCALE`) saklanır; ilk ziyaret `Accept-Language`'a bakar, sonra çerez kazanır.
- Bayrak ikonu dil değildir (İngilizce ≠ 🇬🇧); metin kullan.

## SEO

- `<html lang="tr">` ve her sayfada `alternates.languages` → `hreflang` (`tr`, `en`, `x-default`).
- `metadata`'yı da çevir (`generateMetadata` içinde `getTranslations`).
- `sitemap.ts` her locale için URL + `alternates`.
- Otomatik yönlendirmeyi botlar için engelleme; içerik her locale URL'inde doğrudan sunulsun.

## RTL hazırlığı (ileride Arapça vb. gelirse maliyeti düşür)

- CSS'te fiziksel yerine **mantıksal** özellikler: `margin-inline-start`, `padding-inline`, `inset-inline-end`,
  `text-align: start`. Tailwind: `ms-4`, `pe-2`, `start-0`.
- Yön ikonlarını (`ChevronRight`) `rtl:rotate-180` ile çevir.
- `<html dir>` locale'e göre; layout'u `dir="rtl"` ile bir kez test et.

## Çeviri iş akışı

- Kaynak dil tek (`tr.json`); diğer diller ondan türer. Anahtar silinince her dilden silinir.
- Çevirmene bağlam: ayrı `description` alanı (Crowdin/Tolgee/Lokalise gibi araçlar destekler).
- Makine çevirisi taslak olabilir; UI metni insan gözden geçirmeden yayına çıkmaz.
- Sahte-yerelleştirme (pseudo-locale, metinleri %30 uzat + aksanlı harf) ile taşma testleri.
- CI testi: eksik/fazla anahtar, boş değer, ICU sözdizimi hatası (`@formatjs/cli` veya basit script).

## Kontrol listesi

- [ ] UI'da sabit yazılmış kullanıcı metni yok (grep: `>[A-ZÇĞİÖŞÜ][a-zçğıöşü]+` JSX içinde)
- [ ] Tarih/sayı/para `Intl` ile; locale sunucu ve istemcide aynı
- [ ] `lang` ve `dir` doğru; `hreflang` var
- [ ] Türkçe büyük/küçük harf `tr-TR` ile
- [ ] Mesaj anahtarları iki dilde eşit; CI testi var
- [ ] Uzun çevirilerde düzen kırılmıyor (375px'te kontrol)
