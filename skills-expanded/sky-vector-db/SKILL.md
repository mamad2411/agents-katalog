---
name: sky-vector-db
description: >-
  Vektör veritabanları ve benzerlik araması: pgvector (önce Postgres), Qdrant, Weaviate,
  Pinecone, Chroma, LanceDB, Turbopuffer seçimi; embedding modeli seçimi ve boyut, mesafe
  metrikleri, HNSW/IVF indeksleri ve ayarları, meta veri filtreleme ve kiracı izolasyonu,
  hibrit arama (vektör + tam metin, RRF), yeniden sıralama (rerank), parçalama ile ilişkisi,
  yeniden embed etme ve sürümleme, maliyet ve ölçek. RAG, semantik arama, benzer ürün/içerik
  önerisi yaparken kullan.
disable-model-invocation: true
---

# Sky · Vektör Veritabanları

## Seçim

| Durum | Seçim |
|---|---|
| Zaten Postgres var, < birkaç milyon vektör | **pgvector** (+ ilişkisel filtreler, transaction, tek sistem) |
| Büyük ölçek, gelişmiş filtreleme, self-host | **Qdrant** / Weaviate / Milvus |
| Yönetilen, sunucusuz | Pinecone, Turbopuffer, Upstash Vector |
| Gömülü / yerel / defter | Chroma, LanceDB, sqlite-vec |
Varsayılan: **pgvector** — ayrı sistem işletmeden çoğu ürün ihtiyacını karşılar.

## pgvector

```sql
create extension if not exists vector;
create table chunks (
  id bigserial primary key, org_id uuid not null, doc_id uuid not null, content text not null,
  embedding vector(1024) not null, model text not null default 'embed-v1', created_at timestamptz default now()
);
create index on chunks using hnsw (embedding vector_cosine_ops) with (m = 16, ef_construction = 64);
create index on chunks (org_id);
-- arama (kiracı filtresiyle)
set hnsw.ef_search = 100;
select id, content, 1 - (embedding <=> $1) as score from chunks where org_id = $2 order by embedding <=> $1 limit 20;
```
- Mesafe: çoğu metin embedding'i için kosinüs (`<=>`); normalize edilmişse iç çarpım (`<#>`) daha hızlı.
- Filtreli aramada HNSW sonuçları filtreden sonra azalabilir → `ef_search` artır, iterative scan (yeni sürümlerde) veya kiracı başına partition.
- Boyut maliyeti: 1024 boyut × 4 byte = 4KB/vektör; `halfvec` ile yarıya iner.

## Embedding modeli

Türkçe dahil çok dilli model seç (kendi verinle test et); belge ve sorgu için aynı model (bazı modellerde ayrı "query/document" önekleri); modeli değiştirmek = **tüm vektörleri yeniden üret** → `model` sütunu ile sürümle, yeni sütun/tabloya paralel üret, sonra geç.

## Kalite: hibrit + rerank

1. Vektör araması (anlamsal) + tam metin araması (anahtar kelime, isim, kod — bkz. `sky-search`) → **Reciprocal Rank Fusion** ile birleştir.
2. İlk 20–50 sonucu **reranker** (cross-encoder) ile yeniden sırala → ilk 5'i kullan.
3. Meta veri filtreleri (tarih, tür, dil, erişim izni) sorguya.
Saf vektör araması ürün kodları, isimler ve kısa sorgularda zayıftır.

## Güvenlik ve izolasyon

Her sorguda kiracı/izin filtresi (pgvector'da RLS de uygulanabilir); Qdrant/Pinecone'da namespace/payload filtresi zorunlu — bir müşterinin belgesi asla başkasının bağlamına girmesin (bkz. `sky-ai` RAG kuralları).

## İşletim

Toplu embed işleri kuyrukta (bkz. `sky-jobs`), belge değişince yalnızca değişen parçaları yeniden embed et (içerik hash'i), silinen belgelerin vektörlerini de sil; kalite metrikleri `sky-ai-eval` (recall@k).
