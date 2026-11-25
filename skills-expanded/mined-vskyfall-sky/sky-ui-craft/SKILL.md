---
name: sky-ui-craft
description: >-
  Arayüz zanaatı: görsel hiyerarşi, tipografi ölçeği, renk sistemi ve tasarım token'ları,
  boşluk ritmi, yarıçap/gölge, bileşen durumları, dark mode, responsive düzen ve "cilalı
  hissettiren" detaylar. UI tasarlarken, bir ekranı güzelleştirirken, "daha profesyonel
  görünsün", "tasarımı düzelt", "dark mode ekle" dendiğinde kullan. Ayrıntılı token
  şablonu için references/tokens.css dosyasına bak.
disable-model-invocation: true
---

# Sky · UI Zanaatı

## Önce yön seç

Kod yazmadan önce bir cümleyle tasarım yönünü belirle: **ton** (sakin/kurumsal, oyunbaz,
editoryal, teknik), **yoğunluk** (ferah / kompakt), **vurgu rengi** ve **font eşleşmesi**.
Varsayılan "gri kartlar + mor gradyan" görünümünden kaçın; bilinçli bir karakter seç.

## Token sistemi

Tüm görsel değerler `:root` üzerinde token olarak tanımlanır ve dark mode'da yeniden tanımlanır.
Hazır şablon: [references/tokens.css](references/tokens.css). Bileşende ham `#hex`, `px` boşluk
veya rastgele `box-shadow` görürsen token'a çevir.

## Tipografi

- Ölçek (1.25 oran): 12 · 14 · 16 (gövde) · 20 · 24 · 30 · 36 · 48 · 60.
- Gövde 16px, satır yüksekliği 1.5–1.6; başlıklar 1.1–1.25 ve hafif negatif harf aralığı
  (`-0.01em` ~ `-0.02em`).
- Satır uzunluğu 60–75 karakter (`max-width: 65ch`).
- En fazla 2 font ailesi; ağırlıkları sınırlı tut (400, 500, 600/700).
- Sayılar tablolarda `font-variant-numeric: tabular-nums`.
- Başlıklarda `text-wrap: balance`, paragraflarda `text-wrap: pretty`.
- Hiyerarşiyi önce **ağırlık ve renk** ile kur, sonra boyutla.

## Renk

- Nötr skala (50–950) + 1 vurgu + anlamsal renkler (success, warning, danger, info).
- Metin: birincil (`--fg`), ikincil (`--fg-muted`), üçüncül; her biri arka planla ≥ 4.5:1
  (büyük metin ≥ 3:1).
- Vurgu rengini az kullan: birincil eylem, aktif durum, odak halkası.
- Dark mode'da saf siyah (#000) yerine koyu nötr; yüzeyler yükseldikçe hafif açılır;
  doygun renkleri biraz kıs.
- Bilgiyi yalnızca renkle iletme (ikon/metin ekle).

## Boşluk ve düzen

- 4px taban ölçek: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96.
- İlişkili öğeler yakın, gruplar arası daha geniş (yakınlık ilkesi).
- İç boşluk ≤ dış boşluk; iç içe yarıçap: `iç = dış − padding`.
- Izgara: içerik genişliği `max-width: 1200px` civarı, kenar boşluğu mobilde 16px.
- Hizalama tutarlı: tek bir sol kenar çizgisi.
- `gap` kullan; margin zincirlerinden kaçın.

## Yüzey, kenarlık, gölge

- Derinlik için gölge yerine çoğu zaman 1px yarı saydam kenarlık yeter.
- Gölgeler katmanlı ve düşük opaklıklı (2–3 katman); token'dan gelsin.
- Yarıçap ölçeği: 6 (input/buton) · 10 (kart) · 16 (modal) · 9999 (pill). Tutarlı olsun.

## Bileşen durumları (hepsi tasarlanmalı)

| Durum | Gereken |
|---|---|
| Varsayılan / hover / active | Hover renk farkı ince; active hafif basılma (`scale(0.98)`) |
| Focus-visible | 2px vurgu halkası + 2px ofset; asla `outline: none` tek başına |
| Disabled | %50 opaklık + `cursor: not-allowed`; neden devre dışı olduğu anlaşılır olsun |
| Loading | Buton genişliği sabit, spinner + metin; iskelet ekranlar içerik biçiminde |
| Boş | İllüstrasyon/ikon + kısa açıklama + birincil eylem |
| Hata | Ne oldu + ne yapmalı + tekrar dene |
| Uzun içerik | Taşma, `truncate`/`line-clamp`, uzun kelime kırma (`overflow-wrap: anywhere`) |

## Cilalı hissettiren detaylar

- İkon + metin dikey hizası optik olarak ortalı; ikonlar tek bir setten ve aynı çizgi kalınlığında.
- Tıklanabilir alan görünenden büyük (≥ 44px), küçük ikon butonlarda görünmez padding.
- Görsellerde `aspect-ratio` ile yer ayır (CLS yok); `object-fit: cover`.
- Seçim rengi (`::selection`) ve kaydırma çubuğu temaya uygun.
- Modal açıkken arka plan kaydırması kilitli; ESC kapatır; odak içeride.
- Toast'lar kısa, eyleme dönük, ekran okuyucuya `role="status"`.
- Sayı ve tarihler yerelleştirilmiş (`Intl.NumberFormat("tr-TR")`, `Intl.DateTimeFormat`).

## Responsive

- Mobil önce yaz; kırılma noktaları: 640 · 768 · 1024 · 1280.
- Kapsayıcıya göre değişen bileşenlerde **container queries**.
- Akışkan tipografi: `clamp(2rem, 1.2rem + 3vw, 3.75rem)`.
- 375px'te kontrol: yatay taşma yok, butonlar sığıyor, tablolar kaydırılabilir veya kartlaşıyor.

## Doğrulama

Tarayıcıda aç; 375px ve 1280px genişlikte, açık ve koyu temada ekran görüntüsü al ve
yukarıdaki tabloya göre kontrol et. Gerekirse `sky-ui-reviewer` yöntemini çalıştır.
