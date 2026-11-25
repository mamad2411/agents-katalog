---
name: sky-search
description: >-
  Uygulama içi arama: Postgres full-text (tsvector, ts_rank) ve pg_trgm bulanık arama,
  Meilisearch/Typesense/Algolia ne zaman, Türkçe'ye özgü sorunlar (İ/ı, ekler, aksan
  duyarsızlığı), autocomplete/typeahead UI, ⌘K arama, sonuç vurgulama, filtre+facet, sıralama,
  "sonuç yok" deneyimi, arama analitiği ve semantik/vektör arama. "Arama ekle", "arama çalışmıyor",
  "Türkçe arama", "autocomplete" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Arama

## Hangi motor?

| Ölçek / ihtiyaç | Seçim |
|---|---|
| < 100k kayıt, basit "içerir" araması | **Postgres `pg_trgm`** (ILIKE + trigram indeks) |
| Metin ağırlıklı (blog, doküman), sıralama önemli | **Postgres full-text** (`tsvector`) |
| Yazım hatası toleransı, facet, anında sonuç, 1M+ kayıt | **Meilisearch** (self-host kolay) / **Typesense** |
| Yönetilen, bütçe var | Algolia |
| "Anlama göre" arama (benzer içerik, soru-cevap) | **pgvector** + embedding, hibrit (FTS + vektör) |

Önce Postgres; motor gerçekten gerekince ekle (ek senkronizasyon yükü getirir).

## Türkçe sorunları ve çözümleri

- **Büyük/küçük harf:** `lower()` locale'e göre çalışmayabilir; normalize edilmiş arama sütunu tut.
- **Aksan/özel harf duyarsızlığı:** kullanıcı "cagri" yazar, kayıt "Çağrı". Çözüm: normalize sütun:
```sql
create extension if not exists pg_trgm;
alter table clients add column search text generated always as (
  lower(translate(coalesce(name,'') || ' ' || coalesce(phone,''), 'ÇĞİIÖŞÜçğıöşü', 'cgiiosucgiosu'))
) stored;
create index clients_search_trgm on clients using gin (search gin_trgm_ops);
-- sorgu: aynı normalizasyonu girdiye uygula
select * from clients where search like '%' || $1 || '%' order by similarity(search, $1) desc limit 20;
```
- **Ekler:** "randevularım" araması "randevu"yu bulsun. Postgres'in yerleşik `turkish` sözlüğü
  (snowball) kök bulur: `to_tsvector('turkish', body)`. Mükemmel değil; trigram ile birleştir.
- Meilisearch: `typoTolerance` açık, `stopWords`: "ve, ile, bir, bu, için, da, de".
- Telefon araması: girdiden boşluk/parantez/+90 sil, son 10 haneyi eşle.

## Full-text (Postgres)

```sql
alter table posts add column tsv tsvector generated always as (
  setweight(to_tsvector('turkish', coalesce(title,'')), 'A') ||
  setweight(to_tsvector('turkish', coalesce(body,'')),  'B')
) stored;
create index posts_tsv on posts using gin (tsv);
select id, title, ts_rank(tsv, q) rank, ts_headline('turkish', body, q, 'MaxFragments=2') snippet
from posts, websearch_to_tsquery('turkish', $1) q where tsv @@ q order by rank desc limit 20;
```
`websearch_to_tsquery` kullanıcı dostu sözdizimi verir (`"tam ifade"`, `-hariç`).

## Autocomplete / typeahead UI

- 150–250ms debounce; 2 karakterden sonra başla; önceki isteği `AbortController` ile iptal et.
- Combobox ARIA kalıbı (bkz. `sky-a11y`): ok tuşları, Enter seçer, Esc kapatır.
- Sonuçları **gruplara** ayır: "Müşteriler", "Randevular", "Sayfalar" — her grupta ilk 3–5.
- Eşleşen kısmı **vurgula** (`<mark>`).
- Son aramalar + popüler aramalar (boş durumda).
- Klavye kısayolu `/` veya `⌘K` ile odak (bkz. `sky-dashboard` komut paleti).
- Mobilde tam ekran arama katmanı, klavye otomatik açılsın.

## Sonuç sayfası

- Arama terimi URL'de (`?q=`), paylaşılabilir; filtreler/facet'ler de URL'de.
- Facet sayıları ("Kadıköy (12)"), seçili filtreler chip olarak.
- Sıralama: "En alakalı" varsayılan, sonra tarih/fiyat.
- **"Sonuç yok" deneyimi:** yazım önerisi ("Bunu mu demek istedin: *kuaför*?"), filtreleri gevşet
  önerisi, popüler içerik, "bulamadığını bize söyle" bağlantısı. Boş beyaz sayfa asla.

## Senkronizasyon (harici motor)

- Kaynak DB'dir; motor türetilmiş indeks. Yazma sonrası olay → kuyruk → indeksle (bkz. `sky-jobs`).
- Gece toplu yeniden indeksleme + tutarsızlık raporu.
- Yetki: kullanıcı yalnızca görebildiği kayıtları bulmalı → motor tarafında `tenant_id` filtresi
  zorunlu (Meilisearch tenant token, Typesense scoped API key).

## Semantik arama

- Çok dilli embedding (Türkçe'de iyi olanları seç) → `pgvector` + HNSW indeks.
- **Hibrit:** FTS skoru + vektör benzerliği, Reciprocal Rank Fusion ile birleştir. Saf vektör, isim/kod aramada kötüdür.
- Detay için `sky-ai`.

## Analitik

`search_performed { q_length, results_count }`, `search_result_clicked { position }`.
Sıfır sonuçlu aramaların listesi = ürün yol haritası. Sorgu kişisel veri içerebilir; kısalt/hashle.
