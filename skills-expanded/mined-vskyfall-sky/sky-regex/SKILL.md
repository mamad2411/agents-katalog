---
name: sky-regex
description: >-
  Düzenli ifadeler: Türk telefon numarası, TCKN, IBAN, plaka, posta kodu kalıpları, Türkçe karakterler
  (\p{L}, u bayrağı), ReDoS'tan kaçınma. "Regex yaz", "desen eşleştir" dendiğinde kullan.
---

# Sky · Regex

## Okunurluk

```ts
const PHONE_TR = /^(?:\+90|0)?(?<operator>5\d{2})(?<rest>\d{7})$/;
const m = normalized.match(PHONE_TR);
m?.groups?.operator; // "532"
```
- Adlandırılmış gruplar (`(?<ad>…)`), kalıbı sabit olarak adlandır, yanına örnek eşleşen/eşleşmeyen yorum yaz.
- Karmaşık kalıbı parçalara böl ve birleştir (`new RegExp(`^${DATE}T${TIME}$`)`), ya da regex yerine birkaç basit kontrol.
- Doğrulamada her zaman `^…$` (kısmi eşleşme sürprizi olmasın).

## Türkiye kalıpları (önce normalize et: boşluk, tire, parantez sil)

| Ne | Kalıp | Not |
|---|---|---|
| Cep telefonu | `^(?:\+90|0)?5\d{9}$` | E.164'e çevir: `+90` + 10 hane |
| Sabit hat | `^(?:\+90|0)?[2-4]\d{9}$` | alan kodu 2xx–4xx |
| IBAN (biçim) | `^TR\d{24}$` | + mod-97 kontrolü (bkz. `sky-tr-integrations`) |
| TCKN (biçim) | `^[1-9]\d{10}$` | + algoritma kontrolü |
| VKN | `^\d{10}$` | + algoritma kontrolü |
| Posta kodu | `^(0[1-9]|[1-7]\d|8[01])\d{3}$` | ilk iki hane il kodu 01–81 |
| Araç plakası | `^(0[1-9]|[1-7]\d|8[01])\s?[A-Z]{1,3}\s?\d{2,4}$` | büyük harfe çevirerek |
| Tarih GG.AA.YYYY | `^(0[1-9]|[12]\d|3[01])\.(0[1-9]|1[0-2])\.\d{4}$` | geçerliliği (31 Şubat) ayrıca kontrol et |

E-posta: regex ile "mükemmel" doğrulama yok — basit kontrol (`^[^\s@]+@[^\s@]+\.[^\s@]+$`) + doğrulama e-postası. URL: regex yerine `new URL(input)` + şema kontrolü.

## Unicode ve Türkçe

```ts
/^[\p{L}\p{M}' -]{2,60}$/u          // ad soyad: tüm diller dahil harfler (Ç, Ğ, İ, ı …)
/[çğıöşüÇĞİÖŞÜ]/                     // Türkçe karakter içeriyor mu
"İstanbul".match(/i/i)               // dikkat: büyük/küçük harf duyarsızlık Türkçe İ/ı kurallarını bilmez
```
- `u` bayrağı (Unicode kod noktaları, `\p{…}` sınıfları) her zaman; `v` bayrağı küme işlemleri için (`[\p{L}--[a-z]]`).
- `\w` yalnızca ASCII harf/rakam/alt çizgi — Türkçe kelimeleri bölüştürür; `[\p{L}\p{N}_]` kullan.
- `\b` ASCII'ye göre çalışır → Türkçe kelime sınırı için lookaround: `(?<![\p{L}])kelime(?![\p{L}])` (u bayrağıyla).
- `i` bayrağı "I/ı/İ/i" eşlemesini Türkçe kurallara göre yapmaz → karşılaştırmadan önce `toLocaleLowerCase("tr-TR")` (bkz. `sky-i18n`).

## Araçlar

- Lookahead `(?=…)`/`(?!…)`, lookbehind `(?<=…)`/`(?<!…)`: parola kuralları (`^(?=.*\d)(?=.*[a-z]).{8,}$`), bağlam koşulu.
- Açgözlü `.*` vs tembel `.*?`: `<b>a</b><b>b</b>` üzerinde `<b>.*</b>` hepsini alır.
- `matchAll` + `g` ile tüm eşleşmeler ve gruplar; `replaceAll` + fonksiyon ile dönüşüm; `split` ile ayrıştırma.
- `String.raw` ile ters eğik çizgi kaçışlarını azalt.

## ReDoS (felaket geri izleme)

İç içe nicelikler `(a+)+`, `(.*)*`, örtüşen alternatifler `(a|aa)+` + eşleşmeyen uzun girdi → üstel süre, sunucu donar.
- Kullanıcı girdisine uygulanan regex'lerde iç içe nicelikten kaçın, girdi uzunluğunu sınırla.
- Sunucuda güvenilmeyen kalıp çalıştırma (kullanıcının yazdığı regex) → **RE2** (`re2` paketi, doğrusal zaman) veya hiç.
- Lint: `eslint-plugin-regexp` (güvenli olmayan kalıpları yakalar), `safe-regex`.

## Ne zaman regex DEĞİL

HTML/XML ayrıştırma (parser kullan: cheerio, DOMParser), JSON (JSON.parse), CSV (Papa Parse — tırnaklı virgüller), tarih ayrıştırma (kütüphane),
karmaşık dil bilgisi (parser combinator / PEG). Okunurluğu öldüren tek satırlık canavar yerine 5 satırlık açık kod.

## Test

Her kalıp için eşleşmesi ve eşleşmemesi gereken örnek tablosu (`test.each`); regex101.com (açıklama + hata ayıklama, ECMAScript seçili).
