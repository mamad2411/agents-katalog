---
name: sky-dashboard
description: >-
  Panel ve admin arayüzleri: uygulama kabuğu (sidebar, topbar, içerik), bilgi hiyerarşisi ve
  yoğunluk, KPI kartları, TanStack Table ile veri tabloları (sunucu taraflı sıralama/filtre/
  sayfalama, sütun görünürlüğü, satır seçimi, toplu işlem, sanallaştırma, mobil davranış), URL
  durumlu filtreler (nuqs), komut paleti, klavye kısayolları, tarih aralığı, CSV dışa aktarma,
  yetkiye duyarlı UI ve performans. "Admin paneli", "dashboard", "tablo yap", "liste sayfası"
  dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Panel & Dashboard

Görsel kurallar `sky-ui-craft`, grafikler `sky-dataviz`, bileşen mimarisi `sky-design-system`.
Burada **yoğun, veri odaklı, her gün kullanılan** arayüzlerin kalıpları var.

## Uygulama kabuğu

```
┌ sidebar (240px, daraltılabilir 64px) ┬ topbar (56px: breadcrumb, arama/⌘K, bildirim, hesap) ┐
│ logo                                 │ içerik: max-width 1400px, padding 24px                 │
│ nav grupları (ikon + etiket)         │   sayfa başlığı + birincil eylem (sağ üst)             │
│ alt: org değiştirici, ayarlar        │   filtre çubuğu / sekmeler                             │
└──────────────────────────────────────┴───────────────────────────────────────────────────────┘
```
- Sidebar: aktif öğe net (`aria-current="page"`), gruplar ≤ 7 öğe, daraltılmışta tooltip; mobilde drawer.
- Topbar'da **tek** birincil eylem; sayfa başlığı `h1`.
- Yoğunluk: panellerde `--text-sm` (14px) gövde ve 4/8px boşluk kabul; ama dokunma hedefi ≥ 32px (masaüstü panel), mobilde 44px.
- Dark mode burada çok kullanılır; token'lar iki temada test edilmiş olsun.
- Düzen `grid-template-areas` ile; sidebar durumu `localStorage` + çerez (SSR'da zıplama olmasın).

## Bilgi hiyerarşisi

- Sol üst en önemli: önce **özet KPI'lar**, sonra trend, sonra detay tablo.
- Her ekran bir soruya cevap verir ("bugün ne ters gitti?"). Cevap vermeyen widget'ı kaldır.
- Boş panel ilk gün: örnek veri/illüstrasyon + "ilk kaydını oluştur" CTA, boş kutular değil.

## KPI kartı

```
Başlık (muted, sm)           ⓘ
₺124.500          ▲ %12,4 (geçen aya göre)
▁▂▃▅▆▇ sparkline
```
- Sayı `tabular-nums`, Türkçe biçim (`Intl`), kısaltma ≥ 1M için ("1,2M") tooltip'te tam değer.
- Delta renk + ok + metin (yalnızca renk değil); iyi/kötü yönü metrik tanımlar (maliyet artışı kırmızı).
- Yükleniyor: aynı boyutta iskelet; hata: kart içinde kısa mesaj + yenile.
- Tıklanabilirse tüm kart link, `focus-visible` halkası kartta.

## Veri tablosu (TanStack Table)

**Ne zaman tablo, ne zaman liste/kart:** 4+ karşılaştırılabilir sütun → tablo; mobilde veya 2–3 alan → kart listesi.

**Sunucu taraflı** (varsayılan, 1k+ satır): sıralama, filtre, sayfalama parametreleri URL'de, sunucu
sorguya çevirir, toplam sayı ile döner. İstemci taraflı yalnızca ≤ 500 satır ve veri zaten elde.

```ts
// URL ↔ durum (nuqs)
const [q, setQ] = useQueryState("q", parseAsString.withDefault(""));
const [page, setPage] = useQueryState("page", parseAsInteger.withDefault(1));
const [sort, setSort] = useQueryState("sort", parseAsString.withDefault("-createdAt"));
const [status] = useQueryState("status", parseAsArrayOf(parseAsString));
```
Paylaşılabilir, geri tuşu çalışır, yenilemede kalır. Arama girdisini 300ms debounce et; sayfa 1'e dön.

**Sütunlar**
- Metin sola, sayı/para **sağa** hizalı, tarih tutarlı biçim, durum için `Badge`.
- İlk sütun kimlik (ad/numara) ve tıklanabilir (detay). Son sütun eylemler (`…` menüsü; satırda en fazla 1–2 ikon).
- Sütun görünürlüğü menüsü; tercih `localStorage` (anahtar: tablo adı + sürüm).
- Uzun metin `truncate` + tooltip; sabit sütun genişlikleri `table-layout: fixed`.
- Yapışkan başlık (`position: sticky; top: 0`) ve geniş tablolarda yapışkan ilk sütun.

**Satır etkileşimi**
- Satır seçimi: checkbox sütunu, "tümünü seç" sayfa için (tüm sonuçlar için ayrı bağlantı: "Tüm 1.240 kaydı seç").
- Toplu işlem çubuğu seçim varken belirir: "3 seçildi · Dışa aktar · Sil".
- Satıra tıkla → detay (link); satırda buton varsa `stopPropagation`. Klavye: satırlar `tabIndex`, Enter açar.
- Satır içi düzenleme yalnızca basit alanlarda; aksi halde drawer/sheet.

**Durumlar**
- Yükleniyor: gerçek sütun sayısında 5–10 iskelet satır; sayfa geçişinde eski veriyi soluk tut (`placeholderData: keepPreviousData`).
- Boş (filtre yok): illüstrasyon + CTA. Boş (filtre var): "Eşleşen kayıt yok · Filtreleri temizle".
- Hata: tablo yerine mesaj + yeniden dene; filtreler kaybolmasın.

**Sanallaştırma**: istemcide 100+ satır görünürse `@tanstack/react-virtual`; sunucu sayfalamada gerek yok.

**Mobil**: ≤ 768px'te ya kart listesi (en önemli 3 alan) ya da yatay kaydırma + yapışkan ilk sütun;
`<table>` semantiğini koru.

**Erişilebilirlik**: `<caption>` (görsel gizli olabilir), `scope="col"`, sıralanabilir başlıkta `aria-sort`,
`<button>` olarak başlık, seçim checkbox'larında `aria-label="Satırı seç: {ad}"`.

## Filtreler

- Filtre çubuğu: arama + 2–4 hızlı filtre (select/çoklu) + "Daha fazla" popover; aktif filtreler **chip**
  olarak görünür ve tek tıkla kaldırılır; "Temizle" bağlantısı.
- Tarih aralığı: ön ayarlar (Bugün, Son 7 gün, Bu ay, Geçen ay) + özel aralık; saat dilimi kullanıcının.
- Kayıtlı görünümler (filtre + sütun + sıralama) ileri seviye; URL'yi kaydetmek en basit sürümü.

## Komut paleti ve kısayollar

- `⌘K` / `Ctrl+K` palet (cmdk): sayfalar, eylemler, kayıt arama; son kullanılanlar.
- Kısayollar: `?` listesi, `g d` (git dashboard) tarzı; girdi odaklıyken devre dışı; tooltip'te göster.
- `Esc` her overlay'i kapatır.

## Formlar panelde

- Oluştur/düzenle **sheet/drawer** (bağlam korunur) veya ayrı sayfa (uzun form). Dialog yalnızca kısa (≤ 4 alan).
- Kaydet sonrası liste `invalidateQueries`; yeni satırı kısa süre vurgula.
- Yıkıcı işlem: onay dialogu, nesne adı yazılı, buton "Sil" (Evet/Hayır değil); geri alma toast'u varsa onay istemeyebilirsin.

## Dışa aktarma

- CSV sunucuda üretilir (filtreler aynen), UTF-8 **BOM** ile (Excel Türkçe karakter), ayraç `;` (TR Excel varsayılanı) — ya da kullanıcıya seçtir.
- Büyük dışa aktarım (>10k satır) arka plan işi + e-posta/bildirim ile indirme bağlantısı.
- Tarih ISO veya kullanıcı locale'i tutarlı; para düz sayı (biçimsiz).

## Yetkiye duyarlı UI

- Göremeyeceği menü öğesi hiç render edilmez; yapamayacağı eylem **devre dışı + tooltip** ("Bu işlem için yönetici yetkisi gerekir") — tutarsızlık yaratmadan.
- Sunucu yine de kontrol eder (`sky-auth`).

## Performans

- Her widget kendi `Suspense` sınırında; yavaş biri sayfayı bekletmez.
- Sunucu sayfalama + `select` ile yalnızca gereken sütunlar; toplam sayıyı ayrı/yaklaşık hesapla (büyük tabloda `count(*)` pahalı).
- Polling varsa yalnızca sekme görünürken; gerçek zamanlı için `sky-realtime`.
- Grafik kütüphanelerini `dynamic()` ile; tablo için sütun tanımlarını `useMemo`.

## Kontrol listesi

- [ ] URL'de filtre/sıralama/sayfa; paylaşılabilir
- [ ] Yükleniyor/boş/hata/boş-filtreli durumlar tasarlandı
- [ ] Sayılar sağa, tabular-nums, Türkçe biçim
- [ ] Mobilde tablo kullanılabilir
- [ ] Klavye: palet, Esc, tablo gezinimi
- [ ] Toplu işlemler ve yıkıcı onaylar
- [ ] Yetki: gizle/devre dışı tutarlı, sunucu kontrolü var
